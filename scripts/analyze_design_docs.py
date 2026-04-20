#!/usr/bin/env python3
"""Mine /Users/gdc/stoa/docs/design/ for a thematic + temporal breakdown.

Walks every .md file in the design docs directory (flat, ~160 files,
naming convention `YYYY-MM-DD-TITLE.md` with older undated variants),
parses the leading date from the filename (falling back to mtime),
extracts a title (first H1 or derived from filename), counts lines,
tags each doc with one or more themes from a fixed taxonomy, buckets
docs into ISO months for a timeline view, and builds a global top-25
term frequency list plus a per-theme "3 most recent samples" block.

Keeps the theme taxonomy identical to analyze_implementation_docs.py so
downstream slides can show design-vs-impl side-by-side for each theme.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_DOCS_ROOT = Path("/Users/gdc/stoa/docs/design")

# Theme taxonomy. Each entry is (theme_key, regex). The regex runs
# against the combined filename + first 200 chars of body, so matching
# works whether the theme keyword is in the title or the opening
# paragraph. Order is significant: themes are evaluated top to bottom,
# and a doc can be tagged with any subset (themes are additive, not
# exclusive).
#
# Kept word-bounded ("\b...\b") to avoid e.g. "auth" matching "author".
# Some patterns use alternation to catch obvious variants (ui-ux, mouse,
# etc). "other" is a sentinel applied only when nothing else matched.
THEME_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("crdt", re.compile(r"\b(crdt|automerge)\b", re.IGNORECASE)),
    (
        "agents",
        re.compile(
            r"\b(agent|agents|arena|claude|multi[-_]agent|e2b|sandbox)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "ui_ux",
        re.compile(
            r"\b(ui|ux|design[-_]system|scanability|scrollspy|toolbar|cursor|mouse|markdown[-_]editor)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "p2p_sync",
        re.compile(
            r"\b(p2p|relay|sync|websocket|postsync|offline)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "version_history",
        re.compile(
            r"\b(version[-_]history|episode|timeline|snapshot|checkpoint)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "meetings_voice",
        re.compile(
            r"\b(meeting|meetings|voice|transcription|livekit|topics|collab)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "billing_auth",
        re.compile(
            r"\b(billing|stripe|auth|clerk|token|credit|credits|supabase)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "desktop",
        re.compile(
            r"\b(desktop|mac|windows|tauri|winui|webview)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "cli_terminal",
        re.compile(
            r"\b(cli|tui|shell|keyboard|palette)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "platform_arch",
        re.compile(
            r"\b(architecture|decision|ipc|daemon|event|journal|storage|ffi)\b",
            re.IGNORECASE,
        ),
    ),
    ("community_forum", re.compile(r"\b(community|forum)\b", re.IGNORECASE)),
    ("provenance", re.compile(r"\b(provenance|blame|trace)\b", re.IGNORECASE)),
]

# Order themes want to appear in the output (matches taxonomy order above
# plus "other" as the tail). Locked so downstream comparisons are stable.
THEME_ORDER = [key for key, _ in THEME_PATTERNS] + ["other"]

# English stopwords for the top-terms calculation. Deliberately short;
# we also drop words under 4 chars, which eliminates most function words
# without needing an exhaustive NLTK-grade list.
STOPWORDS = frozenset(
    """
    the and for with this that from have they been were will
    their what when which would could should about into upon
    also some more most such than then than only other over only
    each both these those where while there here just like very
    after before above below around across within without under
    between among against through during because because since
    being does done much many some every same still even more most
    does doing done back upon etc any all our your mine its his her
    one two three four five six seven eight nine ten
    note notes page pages file files line lines user users case cases
    example examples way ways thing things make makes made doing
    into onto including include includes included use uses used using
    see also only just much must need needs well say says said
    set sets really actually maybe often sometimes however therefore
    would could should might must will shall
    """.split()
)

# A filename stem prefix like "2025-09-15-" yields this date regex.
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z']{3,}")


@dataclass
class DocRecord:
    file: str
    title: str
    date: str
    lines: int
    themes: List[str] = field(default_factory=list)


def parse_filename_date(stem: str) -> Optional[dt.date]:
    """Pull a YYYY-MM-DD leading date off a filename stem, or None."""
    match = FILENAME_DATE_RE.match(stem)
    if match is None:
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def derive_title(stem: str, body: str) -> str:
    """Prefer the first H1 in the body; fall back to the filename stem.

    When deriving from the filename, strip the date prefix and clean up
    underscores/dashes so the title reads reasonably in the slide deck.
    """
    h1 = H1_RE.search(body)
    if h1 is not None:
        return h1.group(1).strip()
    # Strip leading date (`2025-09-15-`), then tidy separators.
    no_date = FILENAME_DATE_RE.sub("", stem)
    pretty = no_date.replace("_", " ").replace("-", " ").strip()
    return pretty or stem


def tag_themes(filename: str, body_head: str) -> List[str]:
    """Return 1+ themes. Falls back to ['other'] if nothing else matched."""
    haystack = f"{filename}\n{body_head}"
    hits: List[str] = []
    for theme, pat in THEME_PATTERNS:
        if pat.search(haystack):
            hits.append(theme)
    if not hits:
        hits.append("other")
    return hits


def tokenize_for_terms(text: str) -> List[str]:
    """Tokenize alphabetic words, lowercase, drop stopwords and short words.

    WORD_RE already excludes tokens shorter than 4 chars and non-alpha
    prefixes, so we only need the stopword filter here.
    """
    return [
        w.lower()
        for w in WORD_RE.findall(text)
        if w.lower() not in STOPWORDS
    ]


def scan_doc(path: Path) -> DocRecord:
    """Read one doc and produce its DocRecord.

    Reads only the first 200 chars for theme tagging (cheap and enough
    to catch the opening paragraph), but the line count and term
    tokenization use the full body.
    """
    stem = path.stem
    body = path.read_text(encoding="utf-8", errors="replace")
    body_head = body[:200]

    doc_date = parse_filename_date(stem)
    if doc_date is None:
        # Older undated docs (FLYIO.MD, LESSONS-FROM-TNYOFFICE.md, etc)
        # get filesystem mtime. Deterministic per checkout and close
        # enough to real "when was this written" for slide purposes.
        doc_date = dt.date.fromtimestamp(os.path.getmtime(path))

    lines = body.count("\n") + (0 if body.endswith("\n") else 1)
    title = derive_title(stem, body)
    themes = tag_themes(path.name, body_head)

    return DocRecord(
        file=path.name,
        title=title,
        date=doc_date.isoformat(),
        lines=lines,
        themes=themes,
    )


def build_payload(docs_root: Path) -> dict:
    if not docs_root.is_dir():
        raise FileNotFoundError(f"docs root not found: {docs_root}")

    # Flat dir: pick up .md at the top level only (ignore the `drafts/`
    # subdir that exists in design/, per the naming convention the
    # taxonomy describes).
    md_paths = sorted(p for p in docs_root.iterdir() if p.is_file() and p.suffix.lower() == ".md")

    records: List[DocRecord] = [scan_doc(p) for p in md_paths]

    if not records:
        raise RuntimeError(f"No markdown files found in {docs_root}")

    records.sort(key=lambda r: r.date)

    # Date range uses only date-parseable records (which is all of them,
    # thanks to the mtime fallback).
    date_range = {
        "first": records[0].date,
        "last": records[-1].date,
    }

    # Per-theme aggregation: count, total lines, most-recent samples.
    by_theme_records: Dict[str, List[DocRecord]] = defaultdict(list)
    for r in records:
        for t in r.themes:
            by_theme_records[t].append(r)

    themes_payload = []
    for theme in THEME_ORDER:
        theme_records = by_theme_records.get(theme, [])
        if not theme_records:
            # Keep the theme row even if empty so downstream diff-style
            # rendering can show a zero for it without KeyError.
            themes_payload.append(
                {
                    "theme": theme,
                    "doc_count": 0,
                    "total_lines": 0,
                    "samples": [],
                }
            )
            continue
        # Samples: most recent 3 (reverse-chronological).
        samples = sorted(theme_records, key=lambda r: r.date, reverse=True)[:3]
        themes_payload.append(
            {
                "theme": theme,
                "doc_count": len(theme_records),
                "total_lines": sum(r.lines for r in theme_records),
                "samples": [
                    {"title": r.title, "date": r.date, "file": r.file}
                    for r in samples
                ],
            }
        )

    # Monthly buckets for the timeline view.
    month_counts: Counter = Counter()
    for r in records:
        month_counts[r.date[:7]] += 1
    by_month = [
        {"month": m, "count": month_counts[m]}
        for m in sorted(month_counts)
    ]

    # Top-25 terms across the full corpus. We re-read each file once
    # here — small enough (<200 files, a few MB total) that caching in
    # memory would complicate the control flow without real payoff.
    term_counter: Counter = Counter()
    for path in md_paths:
        body = path.read_text(encoding="utf-8", errors="replace")
        term_counter.update(tokenize_for_terms(body))
    top_terms = [
        {"term": term, "count": count}
        for term, count in term_counter.most_common(25)
    ]

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "docs_root": str(docs_root),
        "doc_count": len(records),
        "date_range": date_range,
        "themes": themes_payload,
        "by_month": by_month,
        "top_terms": top_terms,
        "files": [asdict(r) for r in records],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=DEFAULT_DOCS_ROOT,
        help="Path to the design docs directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "design_docs_summary.json",
        help="Where to write the JSON payload.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args.docs_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {args.output} — {payload['doc_count']} docs, "
        f"{len(payload['themes'])} themes, "
        f"{len(payload['by_month'])} active months, "
        f"{payload['date_range']['first']} → {payload['date_range']['last']}.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
