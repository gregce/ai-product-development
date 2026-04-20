#!/usr/bin/env python3
"""Mine the AS-BUILT-ARCHITECTURE.md files across the Stoa monorepo.

For every shipping component (stoa-cli, stoa-web, stoa-web/supabase,
stoa-desktop-mac, stoa-desktop-windows), walk the component's
AS-BUILT-ARCHITECTURE.md and extract a structural fingerprint: total
line count, the "Last Updated" date stamped at the top (or bottom) of
the file, the list of H2 section headings (for a table-of-contents
view), and counts of code fences, ASCII system-diagram blocks, and
top-level bullets.

The payload is consumed by the slide deck in Phase 4 to argue "each
shipping surface has a living, hand-maintained AS-BUILT doc" without
having to re-parse the source files in JS.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

# Default stoa checkout. Override with --stoa-root if the caller put the
# monorepo somewhere else, but for this presentation we target the exact
# checkout that Phase 1 scaffolded against.
DEFAULT_STOA_ROOT = Path("/Users/gdc/stoa")

# Relative AS-BUILT paths to mine. Order matters for readability in the
# emitted JSON; keep canonical code → backend → desktop.
AS_BUILT_RELATIVE_PATHS = (
    ("stoa-cli", "stoa-cli/AS-BUILT-ARCHITECTURE.md"),
    ("stoa-web", "stoa-web/AS-BUILT-ARCHITECTURE.md"),
    ("stoa-web-supabase", "stoa-web/supabase/AS-BUILT-ARCHITECTURE.md"),
    ("stoa-desktop-mac", "stoa-desktop-mac/AS-BUILT-ARCHITECTURE.md"),
    ("stoa-desktop-windows", "stoa-desktop-windows/AS-BUILT-ARCHITECTURE.md"),
)

# Each component's AS-BUILT uses slightly different markdown for the date
# line (italic `*Last Updated: YYYY-MM-DD*`, bold `**Last Updated**:`,
# lowercase "updated", etc.). One permissive regex catches them all.
LAST_UPDATED_RE = re.compile(
    r"""
    [*_]{1,2}              # opening italic/bold markers
    \s*last\s+updated\s*   # the literal, case-insensitive
    [*_]{0,2}              # optional closing markers before the colon
    :?\s*                  # optional colon + whitespace
    [*_]*                  # stray italic markers after the colon
    \s*
    (\d{4}-\d{2}-\d{2})    # the ISO date itself
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass
class ComponentFingerprint:
    """Structural fingerprint of one AS-BUILT-ARCHITECTURE.md file."""

    name: str
    path: str
    lines: int
    last_updated: Optional[str]
    h2_sections: List[str] = field(default_factory=list)
    code_fences: int = 0
    ascii_diagrams: int = 0
    top_level_bullets: int = 0


def parse_last_updated(text: str) -> Optional[str]:
    """Pull the first ISO date from any "Last Updated" marker in the doc."""
    match = LAST_UPDATED_RE.search(text)
    if match is None:
        return None
    return match.group(1)


def count_structure(text: str) -> dict:
    """Walk the markdown once and collect counts the slide wants.

    ASCII diagrams are fenced code blocks whose body contains at least one
    box-drawing char (│ or ─). Top-level bullets are lines starting with
    "- " at column 0 (sub-bullets are ignored). H2 is any `## ` heading
    not inside a fenced block.
    """
    h2_sections: List[str] = []
    code_fences = 0
    ascii_diagrams = 0
    top_level_bullets = 0

    in_fence = False
    fence_has_box_chars = False

    for raw in text.splitlines():
        stripped = raw.lstrip()
        # Fence open/close toggles regardless of nesting depth.
        if stripped.startswith("```"):
            if in_fence:
                # Fence is closing — finalize the current block.
                if fence_has_box_chars:
                    ascii_diagrams += 1
                in_fence = False
                fence_has_box_chars = False
            else:
                in_fence = True
                fence_has_box_chars = False
                code_fences += 1
            continue

        if in_fence:
            # Cheap short-circuit — only scan chars when we haven't already
            # flagged this block.
            if not fence_has_box_chars and ("│" in raw or "─" in raw):
                fence_has_box_chars = True
            continue

        # H2 headings outside fences.
        if raw.startswith("## ") and not raw.startswith("### "):
            h2_sections.append(raw[3:].strip())
            continue

        # Top-level bullets — either "- " or "* " at column 0, no indent.
        if raw.startswith("- ") or raw.startswith("* "):
            top_level_bullets += 1

    return {
        "h2_sections": h2_sections,
        "code_fences": code_fences,
        "ascii_diagrams": ascii_diagrams,
        "top_level_bullets": top_level_bullets,
    }


def fingerprint(name: str, path: Path) -> ComponentFingerprint:
    text = path.read_text(encoding="utf-8")
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    structure = count_structure(text)
    return ComponentFingerprint(
        name=name,
        path=str(path),
        lines=lines,
        last_updated=parse_last_updated(text),
        **structure,
    )


def build_payload(stoa_root: Path) -> dict:
    components: List[ComponentFingerprint] = []
    for name, rel in AS_BUILT_RELATIVE_PATHS:
        abs_path = stoa_root / rel
        if not abs_path.is_file():
            # Don't silently skip — downstream code trusts the list shape.
            raise FileNotFoundError(f"AS-BUILT file missing: {abs_path}")
        components.append(fingerprint(name, abs_path))

    totals = {
        "lines": sum(c.lines for c in components),
        "components": len(components),
        "ascii_diagrams": sum(c.ascii_diagrams for c in components),
        "code_fences": sum(c.code_fences for c in components),
        "top_level_bullets": sum(c.top_level_bullets for c in components),
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "stoa_root": str(stoa_root),
        "components": [asdict(c) for c in components],
        "totals": totals,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stoa-root",
        type=Path,
        default=DEFAULT_STOA_ROOT,
        help="Path to the stoa monorepo checkout.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "as_built_summary.json",
        help="Where to write the JSON payload.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args.stoa_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    totals = payload["totals"]
    print(
        f"Wrote {args.output} — {totals['components']} components, "
        f"{totals['lines']} total lines, {totals['ascii_diagrams']} ASCII diagrams, "
        f"{totals['code_fences']} code fences.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
