#!/usr/bin/env python3
"""Summarize the dev→main agentic release-PR automation.

Reads the four workflow files that orchestrate Stoa's release flow and
emits a machine-readable description of each file's role, trigger
events, agentic surface (engine + tools + instructions), plus — when a
`gh` CLI is authenticated — the list of real release PRs that have run
through the flow. Gracefully degrades when `gh` is missing or
unauthenticated so the payload still ships with everything else.

Also appends a short "talking points" section arguing why the flow is
interesting: the dev→main release PR body is rewritten by an LLM on
every push, which is the actual pitch for the slide.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_STOA_ROOT = Path("/Users/gdc/stoa")

# Relative paths inside the stoa repo. release-pr-body.lock.yml is a
# generated artifact — we record its presence but do not parse it; the
# source of truth is the sibling .md file that gh-aw compiles from.
WORKFLOW_FILES: Dict[str, Dict[str, str]] = {
    "release-pr-sync.yml": {
        "rel": ".github/workflows/release-pr-sync.yml",
        "role": (
            "Push-to-dev hook that finds or opens the single standing "
            "dev→main release PR, delegates the body rewrite to the "
            "agentic workflow, then posts the rewritten summary to "
            "Slack. This is the orchestrator."
        ),
    },
    "release-pr-body.md": {
        "rel": ".github/workflows/release-pr-body.md",
        "role": (
            "gh-aw agentic prompt: instructs Claude to read the "
            "generated main↔dev diff context and rewrite the release "
            "PR body into a structured human-readable summary."
        ),
    },
    "release-pr-body.lock.yml": {
        "rel": ".github/workflows/release-pr-body.lock.yml",
        "role": (
            "Generated lock file produced by `gh aw compile` from "
            "release-pr-body.md. Do not edit by hand — it is the "
            "actual YAML GitHub Actions runs."
        ),
    },
    "main-from-dev-only.yml": {
        "rel": ".github/workflows/main-from-dev-only.yml",
        "role": (
            "Branch-protection workflow: rejects any PR into main "
            "whose head is not `dev`. Guarantees main only ever "
            "receives changes through the standing release PR."
        ),
    },
}

# Triggers we're interested in surfacing in the payload. This is a
# coarse grep — good enough to spot "push on dev" vs "workflow_call",
# which is what the slide cares about.
TRIGGER_KEYWORDS = (
    "workflow_dispatch",
    "workflow_call",
    "push",
    "pull_request",
    "schedule",
)


@dataclass
class WorkflowSummary:
    name: str
    path: str
    exists: bool
    role: str
    lines: int = 0
    triggers: List[str] = field(default_factory=list)
    agentic: Optional[Dict] = None
    references: List[str] = field(default_factory=list)


def extract_triggers(text: str) -> List[str]:
    """Return the subset of TRIGGER_KEYWORDS that appear as YAML keys.

    We look for `^keyword:` at zero or two-space indent (the `on:` block
    typically lives at column 0 with keys at column 2). That's enough
    signal for the summary without writing a full YAML parser.
    """
    found: List[str] = []
    for kw in TRIGGER_KEYWORDS:
        pat = re.compile(rf"^\s{{0,4}}{re.escape(kw)}\s*:", re.MULTILINE)
        if pat.search(text):
            found.append(kw)
    return found


def extract_agentic_prompt(md_text: str) -> Dict:
    """Pull the agent-facing bits out of the gh-aw prompt markdown.

    gh-aw .md files are two-section: a YAML front-matter (engine, tools,
    network, safe-outputs, setup steps) and a markdown body that is the
    prompt passed to the LLM. We split on the first line of dashes
    after the front-matter, coarsely parse engine + toolsets out of
    the YAML, and keep the body as-is (truncated) so the slide can
    show it verbatim.
    """
    parts = md_text.split("\n---\n", 2)
    if len(parts) >= 2:
        front = parts[0].lstrip("-\n")
        body = parts[1]
    else:
        front = ""
        body = md_text

    engine_match = re.search(r"^engine\s*:\s*(\w+)", front, re.MULTILINE)
    engine = engine_match.group(1) if engine_match else None

    # Toolsets appear as a YAML list under `tools:`. Grab the first
    # bracketed list we see after `toolsets:`.
    toolsets_match = re.search(
        r"toolsets\s*:\s*\[([^\]]*)\]", front, re.IGNORECASE
    )
    toolsets = []
    if toolsets_match:
        toolsets = [
            t.strip().strip('"').strip("'")
            for t in toolsets_match.group(1).split(",")
            if t.strip()
        ]

    # Which safe-outputs verbs the agent is allowed to call — that's
    # the "what's it authorized to do" surface area.
    safe_outputs = []
    safe_block = re.search(
        r"safe-outputs\s*:\s*\n((?:\s{2,}.*\n)+)", front
    )
    if safe_block:
        for line in safe_block.group(1).splitlines():
            stripped = line.strip()
            if stripped and stripped.endswith(":"):
                safe_outputs.append(stripped.rstrip(":"))

    instructions = body.strip()
    # Cap the instructions at a reasonable size so the emitted JSON
    # stays legible; the full file is still on disk.
    max_chars = 4000
    if len(instructions) > max_chars:
        instructions = instructions[:max_chars] + "\n…(truncated)"

    return {
        "engine": engine,
        "toolsets": toolsets,
        "safe_outputs": safe_outputs,
        "instruction_char_count": len(body.strip()),
        "instructions": instructions,
    }


def extract_references(text: str) -> List[str]:
    """Find other workflow/file refs mentioned in the workflow.

    Useful for the payload to show that, say, release-pr-sync.yml
    invokes release-pr-body.lock.yml by path. We just regex anything
    that looks like `.github/workflows/...` or `./scripts/...`.
    """
    refs = set()
    for match in re.findall(r"[./]*[.]github/workflows/[\w\-./]+", text):
        refs.add(match.lstrip("./"))
    for match in re.findall(r"scripts/ci/[\w\-./]+", text):
        refs.add(match)
    return sorted(refs)


def summarize_file(name: str, stoa_root: Path) -> WorkflowSummary:
    meta = WORKFLOW_FILES[name]
    abs_path = stoa_root / meta["rel"]
    summary = WorkflowSummary(
        name=name,
        path=str(abs_path),
        exists=abs_path.is_file(),
        role=meta["role"],
    )
    if not summary.exists:
        return summary

    text = abs_path.read_text(encoding="utf-8")
    summary.lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    summary.triggers = extract_triggers(text)
    summary.references = extract_references(text)

    # Only the .md prompt has a meaningful agentic body. The sync
    # workflow has `uses: ./.github/workflows/release-pr-body.lock.yml`
    # which dispatches the agent; we surface that via references but
    # don't try to reach through it here.
    if name == "release-pr-body.md":
        summary.agentic = extract_agentic_prompt(text)

    return summary


def run_git(cmd: List[str], cwd: Path) -> Optional[str]:
    """Run a git command; return stdout or None on any failure."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return proc.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def collect_dev_vs_main_log(stoa_root: Path) -> List[Dict]:
    """Commits currently on origin/dev but not on origin/main.

    Shells out to `git -C … log --oneline -20 origin/main..origin/dev`.
    Returns an empty list if the fetch ever fails; the rest of the
    payload is still useful without it.
    """
    out = run_git(
        [
            "git",
            "-C",
            str(stoa_root),
            "log",
            "--oneline",
            "-20",
            "origin/main..origin/dev",
        ],
        cwd=stoa_root,
    )
    if out is None:
        return []
    commits = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        sha, subject = parts
        commits.append({"sha": sha, "subject": subject})
    return commits


def collect_release_prs() -> List[Dict]:
    """Real release PRs via `gh` — any auth/install failure yields []."""
    try:
        proc = subprocess.run(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                "specstoryai/stoa",
                "--base",
                "main",
                "--head",
                "dev",
                "--state",
                "all",
                "--limit",
                "5",
                "--json",
                "number,title,createdAt,mergedAt,state",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return data


def build_payload(stoa_root: Path) -> dict:
    workflows = [
        asdict(summarize_file(name, stoa_root))
        for name in WORKFLOW_FILES
    ]

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "stoa_root": str(stoa_root),
        "workflows": workflows,
        "dev_ahead_of_main": collect_dev_vs_main_log(stoa_root),
        "recent_release_prs": collect_release_prs(),
        "talking_points": [
            "Every push to `dev` triggers a workflow that guarantees a "
            "single standing release PR into `main` is current.",
            "The PR body itself is rewritten by Claude, over a gh-aw "
            "prompt with bounded tool access (repos + pull_requests) "
            "and a one-shot `update-pull-request` safe output.",
            "A sibling workflow enforces that `main` only ever accepts "
            "PRs from `dev`, so the agentic summary is the canonical "
            "release narrative, not a nice-to-have.",
            "The rewritten body is also fanned out to Slack with "
            "`## Header`→`*Header*` conversion and a 2.8KB cap — so "
            "the LLM's release note becomes the channel post.",
            "`release-pr-body.lock.yml` is machine-generated from the "
            "prompt .md by `gh aw compile`; the humans edit the "
            "prompt, the tooling owns the YAML.",
        ],
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
        default=Path(__file__).resolve().parent.parent
        / "data"
        / "release_workflow_summary.json",
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
    wf_count = sum(1 for w in payload["workflows"] if w["exists"])
    print(
        f"Wrote {args.output} — {wf_count}/{len(payload['workflows'])} "
        f"workflows found, {len(payload['dev_ahead_of_main'])} commits "
        f"ahead of main, {len(payload['recent_release_prs'])} recent "
        f"release PRs.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
