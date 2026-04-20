#!/usr/bin/env python3
"""Mine /Users/gdc/stoa/docs/implementation/ — same shape as design scan.

Sibling to analyze_design_docs.py. Intentionally duplicates the theme
taxonomy, the tokenizer, and the stopword list so the two scripts stay
self-contained and downstream slides can load either JSON with the
same reader. Any taxonomy change has to be made in both files — worth
the duplication because each script stays a single runnable file with
no shared helper module to reason about.
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

DEFAULT_DOCS_ROOT = Path("/Users/gdc/stoa/docs/implementation")

# See analyze_design_docs.py for the rationale on taxonomy order and
# regex design. Kept character-for-character identical to that file on
# purpose.
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
THEME_ORDER = [key for key, _ in THEME_PATTERNS] + ["other"]

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
    match = FILENAME_DATE_RE.match(stem)
    if match is None:
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def derive_title(stem: str, body: str) -> str:
    h1 = H1_RE.search(body)
    if h1 is not None:
        return h1.group(1).strip()
    no_date = FILENAME_DATE_RE.sub("", stem)
    pretty = no_date.replace("_", " ").replace("-", " ").strip()
    return pretty or stem


def tag_themes(filename: str, body_head: str) -> List[str]:
    haystack = f"{filename}\n{body_head}"
    hits: List[str] = []
    for theme, pat in THEME_PATTERNS:
        if pat.search(haystack):
            hits.append(theme)
    if not hits:
        hits.append("other")
    return hits


def tokenize_for_terms(text: str) -> List[str]:
    return [
        w.lower()
        for w in WORD_RE.findall(text)
        if w.lower() not in STOPWORDS
    ]


def scan_doc(path: Path) -> DocRecord:
    stem = path.stem
    body = path.read_text(encoding="utf-8", errors="replace")
    body_head = body[:200]

    doc_date = parse_filename_date(stem)
    if doc_date is None:
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

    md_paths = sorted(p for p in docs_root.iterdir() if p.is_file() and p.suffix.lower() == ".md")
    records: List[DocRecord] = [scan_doc(p) for p in md_paths]

    if not records:
        raise RuntimeError(f"No markdown files found in {docs_root}")

    records.sort(key=lambda r: r.date)
    date_range = {
        "first": records[0].date,
        "last": records[-1].date,
    }

    by_theme_records: Dict[str, List[DocRecord]] = defaultdict(list)
    for r in records:
        for t in r.themes:
            by_theme_records[t].append(r)

    themes_payload = []
    for theme in THEME_ORDER:
        theme_records = by_theme_records.get(theme, [])
        if not theme_records:
            themes_payload.append(
                {
                    "theme": theme,
                    "doc_count": 0,
                    "total_lines": 0,
                    "samples": [],
                }
            )
            continue
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

    month_counts: Counter = Counter()
    for r in records:
        month_counts[r.date[:7]] += 1
    by_month = [
        {"month": m, "count": month_counts[m]}
        for m in sorted(month_counts)
    ]

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
        help="Path to the implementation docs directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent
        / "data"
        / "implementation_docs_summary.json",
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
