<!--
  Intent-driven PRD template.

  Copy this file into your repo (e.g. `docs/design/<short-slug>.md`) whenever
  a product decision is made. Fill in the frontmatter, then the four required
  sections. The appendix is optional but high-leverage.

  The example in this file is a realistic PRD for adding a `--since` filter
  to the `stoa log` CLI command. Replace the content with your own; keep the
  shape.

  Why this shape: it's what an agent can pick up and execute without a
  clarifying round-trip. Humans and agents read the same artifact.
-->

---
title: Add `--since` filter to `stoa log`
owner: greg@specstory.com
decided_at: 2026-04-19T14:32:00-04:00   # ISO 8601 with timezone. Starts the ILT clock.
status: draft                             # draft | approved | shipping | shipped
touched_areas: CLI, stoa log command, time parsing utilities
intent_lead_time_start: 2026-04-19T14:32:00-04:00   # when the decision was captured; often == decided_at
---

# Add `--since` filter to `stoa log`

## Outcome

<!--
  One sentence, phrased "When X, a Y-type user can Z." This is the spec an
  agent can execute. If you can't compress the outcome into one sentence, you
  haven't decided yet -- go back and decide.
-->

When running `stoa log` from the CLI, a Stoa user can pass
`--since <duration|timestamp>` (e.g. `--since 7d`, `--since 2026-04-01`,
`--since 2h`) and see only entries whose timestamp is on or after that cutoff.

## Why now / constraint

<!--
  The non-negotiable motivation. Compliance, incident, customer ask, roadmap
  commitment. One paragraph. If you can't name the constraint, defer this PRD
  -- it's not ready.
-->

Two early-access customers (Alpine SG portfolio) pilot-running Stoa against
a 6-month repo are getting 2000+ line `stoa log` dumps and are bouncing off
the CLI because they can't scope by recency. We promised a fix before their
formal rollouts on 2026-05-05. Building this now also unblocks the
`stoa digest --since` feature already on the roadmap for May.

## Acceptance criteria

<!--
  Testable conditions. For each bullet, flag who owns the specification:
  [human] means a human defined what "correct" looks like (usually because it
  encodes domain judgment); [agent] means the agent can derive or implement
  it from the outcome + codebase context alone.
-->

- [human] `--since 7d`, `--since 2h`, `--since 30m` all work and parse as
  Go `time.Duration` offsets from `time.Now()`. Invalid durations error with
  a message naming the accepted formats. (Domain rule: duration tokens must
  match what `stoa digest` already accepts so users don't relearn syntax.)
- [human] `--since 2026-04-01` and `--since 2026-04-01T12:00:00Z` parse as
  RFC 3339 timestamps in UTC. Timezone-less dates are treated as local time
  at 00:00:00. (Domain rule: matches `stoa session list --since` behavior
  that's already shipping.)
- [agent] Entries with a timestamp strictly before the cutoff are omitted.
  Entries at exactly the cutoff are included.
- [agent] `--since` combines with existing `--limit` and `--json` flags
  without regression.
- [human] The filter is documented in `stoa log --help` output, in
  `stoa-cli/README.md`, and in the man page generator. (Domain rule: our
  CLI docs convention requires all three surfaces.)
- [agent] Table-driven unit tests cover duration parsing, timestamp parsing,
  both-invalid-and-valid inputs, and the cutoff-inclusive boundary.

## Out of scope

<!--
  Explicit. Protects against scope creep on the agent side.
-->

- `--until` (the bounded-range version). Separate PRD if/when we need it.
- Relative tokens beyond Go duration syntax (e.g. "last Tuesday",
  "yesterday"). No natural-language parsing in v1.
- Changing default `stoa log` output when `--since` is not passed.
- Filtering by author, path, or content. Those stay as separate flags.

## Implementation notes for the agent

<!--
  OPTIONAL. Not "tell the agent HOW" -- that's over-specification. This is
  pre-loading context the agent would otherwise burn tokens rebuilding:
  where the code lives, which patterns to match, which traps to avoid.
  Think of it as a README for the PR the agent will open.
-->

- The `stoa log` command lives at `stoa-cli/pkg/cli/log.go`. It composes a
  `cobra.Command` and delegates iteration to
  `stoa-cli/pkg/journal/reader.go`.
- Reuse the duration parser in `stoa-cli/pkg/utils/timefmt.go`
  (`ParseSinceSpec`). It already handles both `Xd/Xh/Xm/Xs` and RFC 3339.
  `stoa digest` calls it.
- The journal reader already streams entries in reverse chronological order,
  so a `--since` filter can short-circuit and stop iterating once it crosses
  the cutoff. This matters for 6-month repos -- don't naively scan all
  entries.
- Existing cutoff-filter pattern to mirror: `stoa session list --since`
  (`stoa-cli/pkg/cli/session_list.go`, function `filterBySince`).
- Known pitfall: table-driven tests in this package use `testify/assert`.
  Our CLAUDE.md says we prefer standard `testing` + `t.Errorf`. Follow the
  repo convention, not the existing package's drift. New tests should use
  the standard library.
- Linter gotchas: run `cd stoa-cli && golangci-lint run` before opening a
  PR. The `revive` and `gocritic` configs flag subtle issues
  (e.g. `time.Now()` in a test body without injection).

## How this differs from a classic PRD

> A classic PRD is a Word/Notion doc written before work starts and forgotten
> by the time code ships. This one is different on four axes:
>
> - **Timestamped decision.** `decided_at` is when product *agreed*, not when
>   a doc was created. That timestamp starts the Intent Lead Time (ILT) clock.
>   ILT runs from `decided_at` to first commit referencing this PRD.
> - **Versioned in the repo alongside code.** Lives in `docs/design/`. Moves
>   through the same PR review as the implementation. Git blame tells you who
>   changed the spec and when, forever.
> - **No ticket required.** The PRD *is* the assignment. An agent (Claude
>   Code, Cursor, Codex) can open this file, read the outcome, and start. The
>   ticketing step -- which used to be how you handed work over -- is dead
>   weight when the picker is an agent.
> - **The format is what agents read.** Plain markdown with predictable
>   headings. The agent doesn't need a ticketing API, a PRD-specific DSL, or
>   custom tooling. It just reads the file.

---

## Template: copy this block for each new PRD

<!--
  Delete the worked example above and use the block below as your starting
  point. Everything inside angle-bracket placeholders gets replaced; the
  section guide comments stay so the next author sees what the section is
  for.
-->

<!--
---
title: <one-line title>
owner: <email>
decided_at: <ISO 8601 timestamp with timezone>
status: draft
touched_areas: <free text -- which systems, packages, or surfaces>
intent_lead_time_start: <usually == decided_at>
---

# <one-line title>

## Outcome

When <context>, a <user type> can <observable behavior>.

## Why now / constraint

<one paragraph: compliance, incident, customer, roadmap commitment>

## Acceptance criteria

- [human] <testable condition that encodes domain judgment>
- [agent] <testable condition the agent can derive or implement>
- ...

## Out of scope

- <explicit non-goal>
- ...

## Implementation notes for the agent

- <file paths and functions the agent should read first>
- <known-good patterns to mirror>
- <pitfalls / lint gotchas / convention drift to avoid>
-->
