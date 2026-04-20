<!--
  Intent-driven PRD template.

  This file is empirically distilled from Stoa's own design-doc corpus in
  `docs/design/` (~168 files, 2025-09 to 2026-04). Every section below showed
  up in at least half the sampled docs, and each heading carries a frequency
  tag so you can see how load-bearing it is before you decide whether to
  include it.
-->

# Intent-driven PRD template

## Preface

This template is not invented. It is distilled from `~168` design docs the Stoa team actually shipped with, of which `30` were read closely for this exemplar. The sample spans every month from 2025-09 through 2026-04, every major theme (platform, CRDT, agents, voice, CLI, UI, sync, billing, auth), and every size from 40-line one-page proposals to 2000-line architecture specs. Every section that follows appeared in at least half the docs reviewed; every section is labeled with how often it showed up in the sample so you know which parts are table stakes and which are situational. The one opinionated move the template makes is adding frontmatter: Stoa docs do not currently use it, and this is the single highest-leverage change an author could make for agent readability.

---

## A. Frontmatter (recommended, currently at 0% in corpus; argue for it)

Stoa's design docs today encode status, date, and authorship as a loose block of bold-then-colon lines under the `H1`. That works for humans, is semi-structured, and is invisible to any tool that isn't a person reading top-to-bottom. Switch to YAML frontmatter. It costs nothing, parses everywhere, and a planning agent can load `title`, `status`, and `touches` in one pass without regexing prose.

```yaml
---
title: <one-line declarative title, matches the filename slug>
owner: <email of the single accountable human>
decided_at: <ISO 8601 timestamp with timezone, e.g. 2026-04-19T14:32:00-04:00>
status: draft            # draft | in-review | approved | shipping | shipped | superseded
touches:                 # the systems, packages, or surfaces this feature changes
  - stoa-web/app/api/v1/community
  - stoa-web/supabase/migrations
  - stoa-cli/pkg/remote
intent_lead_time_start: <ISO 8601, usually == decided_at, this starts the ILT clock>
references:              # other design docs, implementation docs, or ADRs this builds on
  - docs/design/2026-04-08-WORKTHREADS-V1-PLAN.md
  - docs/implementation/2026-02-24-SUPPORT-SYSTEM-IMPLEMENTATION.md
---
```

Key-by-key:

- `title`: one declarative phrase. The same wording that belongs in the filename slug and the `H1`. One line, no trailing period.
- `owner`: exactly one human, by email. Stoa docs often list "Greg, with Claude (scribe)" in prose; the frontmatter should collapse that to the accountable party only.
- `decided_at`: the moment product agreed. ISO 8601 with timezone. This is **the timestamp that starts the Intent Lead Time clock**; every other date in the doc is secondary.
- `status`: one of six. Most corpus docs land on `draft`, `in-review`, or mark themselves shipped after the fact via prose. Making this a field lets tools query "what's in flight right now."
- `touches`: the paths, packages, or surfaces this feature changes. Lets an agent pre-grep. `~60%` of the sampled docs list these inline in prose; hoisting them into frontmatter makes them queryable.
- `intent_lead_time_start`: usually identical to `decided_at`, but sometimes earlier (e.g. the decision was made verbally in a meeting before the doc was committed). Be honest here; ILT is a measurement, not a vanity metric.
- `references`: other docs this one depends on or supersedes. `~50%` of the sampled docs include a `Related` section or inline `Builds on:` line; frontmatter makes the graph explicit.

---

## B. Sections (in canonical order)

The heading names below are the ones Stoa authors actually use most often in the corpus. Frequencies are from the sampled docs.

### 1. `## Purpose` or `## Overview` or `## What This Is`  *(in ~85% of docs)*

One to three paragraphs, above the fold. The single most important section in the whole doc. State what this thing is, who it is for, and, if it's easy to say in one sentence, what shipping it looks like. Best corpus examples: `2026-04-06-WORKTHREADS.md` opens with "Workthreads are a new Stoa-owned primitive for durable work context." `2026-04-14-PRELAUNCH-PERFORMANCE-KISS-PLAN.md` opens with "This doc proposes the smallest behavior-preserving performance work to do before the public release."

> Example placeholder: "This doc proposes adding a `--since` filter to `stoa log` so customers running against long-lived repositories can scope output by recency. The change is ~80 lines across one command package and one parsing utility; it is a small, testable surface with no migration risk."

### 2. `## Problem` or `## Context` or `## Current State`  *(in ~75% of docs)*

What is broken today, in concrete terms. Link to real filenames, real tables, real behaviors. The corpus convention is to be ruthlessly specific: cite file paths with line numbers, name specific tables and columns, point at the exact buttons that don't work. `2026-04-17-RESTORE-VERSION-UX.md` spends its opening section listing a table of five UI surfaces and exactly where Restore is/isn't reachable in each; that specificity is what makes the rest of the doc implementable.

**When to skip:** pure research docs or vision docs (e.g. `2025-09-17-INTENT-VS-GIT.md`) skip this because they're comparative, not corrective. Everything else includes it.

> Example placeholder: "`stoa log` has no recency filter. Customers running against 6-month repos hit 2000+ line dumps and bounce off the CLI. The blocker is that `stoa-cli/pkg/journal/reader.go:114` streams everything and trusts `--limit` as the only bound; there is no short-circuit for time-based cutoffs."

### 3. `## Goals` and `## Non-Goals`  *(goals in ~70%; non-goals in ~35%)*

Numbered or bulleted list of what shipping this means. Non-goals is the single best weapon against scope creep on the agent side; about a third of the sampled docs include one, and those are the docs that hand off cleanest. `2026-04-16-COMMUNITY-FORUM-DESIGN.md` makes an art of it: eight explicit non-goals including "typing indicators (wrong modality for async long-form)." Name what you are not building and why.

> Example placeholder:
> **Goals**
> 1. Let users pass `--since 7d`, `--since 2h`, `--since 2026-04-01` to `stoa log`.
> 2. Short-circuit iteration once the cutoff is crossed (matters for big repos).
> 3. Match the duration syntax already accepted by `stoa digest --since`.
>
> **Non-Goals**
> - `--until` (bounded range). Separate PRD when needed.
> - Natural-language relative time ("yesterday", "last Tuesday").
> - Changing default `stoa log` output when `--since` is absent.

### 4. `## Proposal` or `## Design` or `## Chosen Approach` or `## What We're Building`  *(in ~90% of docs; this is the core)*

The meat. How the thing works. Every corpus doc earns its keep here, but the best ones do three things the weaker ones don't:

1. **Name the options you considered and explicitly picked one.** `2026-04-13-LIVE-CLI-AGENT-PRESENCE-IN-MEETINGS.md` lists four candidate architectures ("A. Snapshot polling. B. Intent-server broadcasts... C. CLI self-publishes... D. Activity-derived presence"), then writes "Greg picked **Option D** for its minimal footprint." Cheap to write, enormously valuable to the agent and to the next engineer.
2. **Use ASCII diagrams or small tables liberally.** `~60%` of sampled docs include at least one ASCII box diagram for data flow or component layout. They render in any terminal, survive copy-paste into Slack, and agents parse them fine.
3. **Cite specific code paths in the existing tree.** The best docs read like "`stoa-web/app/api/v2/spaces/[spaceSlug]/agent/events/route.ts` opens a long-lived `ReadableStream` for SSE" rather than "the agent route handles streaming." The former tells an agent where to start reading.

> Example placeholder: the proposal section of a typical corpus doc runs 100-400 lines and mixes prose, ASCII diagrams, code snippets, decision tables, and inline file references. Don't try to fit everything in a sub-template; let the shape follow the feature.

### 5. `## Acceptance criteria` or `## Success` or `## What 'done' looks like`  *(explicit section in ~30%; inline in proposal in another ~40%)*

Testable conditions. Corpus practice is split: about a third of docs have a dedicated section, and another big chunk inline the criteria into phase descriptions or requirement numbering (`R1`, `R2`... as in `2026-03-13-TOPICS-REDESIGN.md` and `2026-03-23-MEETING-NARRATIVE-AND-SEARCH-RESULTS.md`). Either is fine; **having nothing is not**. This is the section most commonly missing from docs that failed to hand off.

Label each criterion by owner. `[human]` means a human defined what correct looks like (usually because it encodes domain judgment the agent can't derive). `[agent]` means the agent can implement or verify it from the outcome + codebase context alone. This labeling is original to this template; the corpus does not do it, but the frequent hand-off friction Greg sees suggests it would help.

> Example placeholder:
> - `[human]` Invalid `--since` input errors with a message listing accepted formats. Match `stoa digest` error wording.
> - `[agent]` Entries strictly before the cutoff are omitted; entries at exactly the cutoff are included.
> - `[agent]` `--since` composes cleanly with existing `--limit` and `--json`.
> - `[human]` Documented in `--help` output, `stoa-cli/README.md`, and the man-page generator.

### 6. `## Phases` or `## Implementation Plan` or `## Rollout`  *(in ~55% of docs)*

Numbered milestones, each with its own deliverable and, ideally, an acceptance bar. The corpus convention is Phase 1 / Phase 2 / Phase 3 with optional "Phase N: Defer until measurement justifies it" at the end. `2026-04-14-PRELAUNCH-PERFORMANCE-KISS-PLAN.md` uses this structure rigorously: Changes 1-6 ordered by implementation priority, plus an explicit "Defer these until production data exists" list.

**When to skip:** single-atomic-change docs (e.g. `2025-09-16-AUTOMATIC_FILE_MOVE_SOLUTION.md`, `2026-01-21-TOOLBAR-AND-KEYBOARD-SHORTCUTS.md`). If the whole feature lands in one PR, don't manufacture phases.

> Example placeholder:
> - **Phase 1, duration + timestamp parsing.** Extend `ParseSinceSpec` in `stoa-cli/pkg/utils/timefmt.go`. Ship with table-driven unit tests.
> - **Phase 2, wire into `stoa log`.** Add `--since` flag in `stoa-cli/pkg/cli/log.go`; short-circuit the journal reader once the cutoff is crossed.
> - **Phase 3, docs pass.** Update `--help`, `stoa-cli/README.md`, man-page generator. Confirm changelog entry.

### 7. `## Open Questions` or `## Unresolved`  *(in ~17% of docs, but strongly predictive of clean hand-off)*

A short bulleted list of things that aren't decided yet, each with a tag for who has to decide and a deadline if it blocks implementation. The corpus is sparse here (only about one in six sampled docs uses an explicit section), but the docs that *do* include one are disproportionately the ones that got matching implementation docs in `docs/implementation/`. Writing open questions down is a leading indicator of successful hand-off.

> Example placeholder:
> - `[product]` Do we accept `--since "-7d"` (with leading minus) in addition to `--since 7d`? Default: no, but flag the decision. Needed by 2026-05-01.
> - `[agent-discoverable]` Should `--since` interact with `--limit` by applying `--since` first, then truncating? Probably yes; agent can choose if acceptance tests pass.

### 8. `## References` or `## Related` or `## Related Documents`  *(in ~35% of docs; should be higher)*

Other docs, issues, external links. Paired with the `references` key in frontmatter above. The corpus often mixes this into the opening metadata block (`Related: docs/implementation/2026-02-24-SUPPORT-SYSTEM-IMPLEMENTATION.md`) or an `H2` at the bottom. Either placement works; what matters is the graph of causality. An agent reading this PRD should be able to follow the references back to ancestor decisions.

> Example placeholder:
> - Precedent: `docs/design/2026-03-23-CLI-TOPICS-AND-MEETING-SEARCH.md` (shipped `--since` on `stoa web meetings search`; same grammar).
> - Parser source: `stoa-cli/pkg/utils/timefmt.go` (existing `ParseSinceSpec`).
> - Customer ask: internal issue TEAM-INVITES-01.

---

## C. Worked example

Below is a filled-in PRD using the template. The feature is fictional, a
per-team invite-link system, and the example is deliberately short. Its
purpose is not to demonstrate a production-grade spec; it is to show what
every section looks like when an author fills it in without cruft.

```markdown
---
title: Per-team invite links
owner: priya@example.com
decided_at: 2026-04-19T10:00:00-04:00
status: draft
touches:
  - app/api/v1/invites
  - components/settings/TeamInvites.tsx
  - supabase/migrations
intent_lead_time_start: 2026-04-19T10:00:00-04:00
references:
  - docs/design/2026-03-18-ORG-MEMBERSHIP-REFACTOR.md
---

# Per-team invite links

## Purpose

Workspace admins need a self-service way to invite teammates. Today, the
only path is a one-off email from the admin panel. There is no URL an
admin can paste into Slack or embed in onboarding docs. This PRD proposes
a per-team invite-link primitive: revocable, optionally time-limited,
optionally seat-capped.

## Problem

The current invite flow at `app/api/v1/invites/email-only/route.ts:34`
requires an exact email, so admins pasting lists from HR hit validation
errors. There is no shareable URL, so teams default to passing around
stale onboarding instructions in Slack. And there is no cap on link
usage, so a single leaked URL is unbounded exposure.

## Goals

1. An admin can generate an invite URL for a specific team in two clicks.
2. Links can be revoked, and are revoked automatically on team deletion.
3. Optional expiry (1d / 7d / 30d / never) and max-uses (1 / 5 / 25 /
   unlimited).

## Non-Goals

- Personalized invite emails; the email-only path already covers that.
- Per-role links (admin vs member). One link grants `member`.
- Cross-team links. One link, one team.

## Design

### Data model

Add `team_invite_links`:

| column      | type          | notes                    |
|-------------|---------------|--------------------------|
| id          | uuid pk       |                          |
| team_id     | uuid fk teams | cascades on team delete  |
| token       | text unique   | opaque, unguessable      |
| expires_at  | timestamptz   | null = never expires     |
| max_uses    | int           | null = unlimited         |
| use_count   | int           | default 0                |
| revoked_at  | timestamptz   | null until revoked       |

### API

- `POST /api/v1/teams/:teamId/invite-links`: create; admin-only.
- `DELETE /api/v1/invite-links/:id`: revoke; idempotent.
- `POST /api/v1/invites/accept`: body `{ token }`; joins the current
  user to the team. Rejects expired, revoked, or over-cap tokens.

### UI

One new section in `settings/TeamInvites.tsx`: a list of active links
with per-row "copy URL" and "revoke" actions. A single "Create link"
button opens a modal with expiry and seat-cap pickers.

## Acceptance criteria

- `[human]` Revoked or expired links surface a branded error page, not a
  raw 401.
- `[human]` "Copy URL" yields a full, absolute URL using the app's
  canonical host.
- `[agent]` Unit tests cover token generation, acceptance, revocation,
  expiry, and use-count enforcement.
- `[agent]` E2E: create link → accept as a different user → user appears
  in the team membership list.

## Phases

1. Schema + API routes. Land behind feature flag `team_invite_links`.
2. Admin UI; flag stays off.
3. Flag on for 10% of orgs; monitor error rate for one week.
4. Flag on for all orgs; retire the legacy email-only path.

## Open Questions

- `[product]` Email the creator when a link hits 80% of its seat cap?
  Default no for v1; revisit after launch.
- `[agent-discoverable]` Should revoked links respond 410 or 404? Either
  is fine if consistent with existing `/api/v1` conventions.

## References

- `docs/design/2026-03-18-ORG-MEMBERSHIP-REFACTOR.md`: the membership
  primitives this builds on.
```

*(end of worked example)*

---

## D. Patterns we observed (appendix)

### Section presence in the sample

The following table reports how often each heading appeared in the 30 design docs sampled. Weighted toward `H2` headings; synonyms are collapsed.

| Section                               | Appeared in  | Notes                                                         |
|---------------------------------------|--------------|---------------------------------------------------------------|
| `Purpose` / `Overview` / `What This Is` | ~85%       | Always at the top. One paragraph, occasionally two.           |
| `Problem` / `Context` / `Current State` | ~75%       | The best examples cite file paths and line numbers.           |
| `Goals`                                 | ~70%       | Bulleted or numbered; 3-8 items typical.                      |
| `Proposal` / `Design` / `Chosen Approach` | ~90%     | The longest section, by far. ASCII diagrams common.           |
| `Non-Goals` / `Out of scope`            | ~35%       | Predictor of clean hand-off. Write them.                      |
| `Acceptance criteria` (explicit)        | ~30%       | Another ~40% inline the criteria into phases or numbered `R#`. |
| `Phases` / `Implementation Plan` / `Rollout` | ~55% | Skip for atomic changes.                                      |
| `Open Questions`                        | ~17%       | Rare but strongly predictive of shipping.                     |
| `References` / `Related`                | ~35%       | Often in the header block, sometimes an `H2` at the bottom.   |
| `Status` / `Date` metadata              | ~95%       | As bold-then-colon lines under `H1`. Should be frontmatter.   |
| YAML frontmatter                        | 0%         | Universal opportunity. Zero current adoption.                 |

### What the sibling implementation docs had that the design docs often didn't

A subset of the sampled design docs had a matching `docs/implementation/*.md` sibling (e.g. `2025-10-25-STAGING-AND-BRANCHING-ANALYSIS.md` → `2025-10-25-EPISODE-IMPLEMENTATION-PLAN.md`). The implementation docs consistently added three things the design docs tended to lack:

1. **A phased roadmap with status checkboxes.** `[x] Phase 1 done`, `[▶] Phase 2 in flight`, `[ ] Phase 3`. Implementation docs are living trackers; design docs are decision captures. The template above lets you pre-seed Phase bullets so the sibling plan inherits the shape.
2. **Explicit pointers to the existing-code starting position.** Not just "the journal lives at `pkg/journal/`" but "`pkg/journal/journal.go:114`, function `StreamReverse`". Design docs are usually one level less specific. Getting more specific in the design doc saves the agent's first exploratory round.
3. **A testing section.** An explicit `## Testing Strategy` or `## Test Criteria` appeared in most implementation docs but only a handful of design docs. Most design docs inline testable conditions into acceptance criteria; a few omit testability altogether. The template pushes testability into `Acceptance criteria` by requiring each bullet to be verifiable.

### The one thing the best docs did

They committed to an option. Every strong doc in the corpus has a moment where it stops surveying and says "Greg picked Option D" or "We are going with the schema-isolated `community` Postgres schema" or "Do NOT implement Git-style staging." Docs that read like comparative research but never land on a verdict are the docs that stall. If your PRD has not picked a path by the end of the `Design` section, it is not ready for an agent to execute; it is still a brainstorm. This is the single most important editorial discipline, and the template enforces it via the `Proposal / Design / Chosen Approach` heading: the word "Chosen" is not decorative.

### Anti-patterns from weaker docs

- **"Future vision" prose with no commitment.** `2025-10-11-FUTURE-VISION-AND-ROADMAP.md` and `2025-10-12-TUI-SEARCH-ROADMAP.md` list dozens of ranked ideas but never commit to a Phase 1. Useful as strategy artifacts; unusable as PRDs.
- **Missing acceptance criteria.** Several of the sampled docs describe a design in detail but leave "how will we know this shipped" implicit. The agent picks up, builds something that matches the prose, and the reviewer rejects the PR for reasons not listed anywhere.
- **Bold-then-colon header blocks instead of frontmatter.** `**Status:** Draft` / `**Date:** 2026-04-14` is universal in the corpus. It's unparseable by tools, and Stoa is now shipping enough docs that the tooling gap matters.
- **Implementation notes buried in prose.** Specific file paths, function names, and lint gotchas tend to be scattered across the `Design` section. Collect them in a `Notes for the agent` subsection (or a trailing bullet list in `Design`) so the agent's first read loads them in one pass.
- **No reference to prior docs.** When a PRD supersedes or extends an earlier decision, say so in `references`. About two-thirds of the corpus does; one-third leaves the graph implicit, and those docs are the hardest to navigate six months later.

---

## E. How to hand this to an agent

Once the PRD is written:

1. **Commit it to `docs/design/<YYYY-MM-DD>-<SLUG>.md`.** The filename carries the date. The filename slug matches the `title` field. The commit itself, not the file's mtime, is when `decided_at` gets the Intent Lead Time clock running, so be honest about the timestamp: if product decided on Tuesday but the doc didn't land until Friday, `decided_at` is Tuesday.
2. **Open the coding agent in plan mode** (Claude Code's `/plan`, Cursor's plan mode, Codex's review mode, whichever tool this agent uses). Point it at the PRD path. Ask it to draft an implementation plan as a sibling doc in `docs/implementation/`.
3. **The sibling implementation doc** should inherit the phases from the PRD, add the file-level specifics (function names, test file layout, migration numbers), and track status with checkboxes as work lands. The PRD stays frozen; the implementation doc is the living artifact.
4. **When the implementation lands**, the commit message should reference the PRD path (`Ref: docs/design/2026-04-19-TEAM-INVITE-LINKS.md`). Every ILT dashboard or report pulls from this reference. A commit that references a PRD-with-a-`decided_at` is a commit that can be measured. A commit that doesn't, can't.
5. **When the feature ships**, update the PRD's `status` to `shipped` in a small commit. This is the last touch the PRD gets. Future readers open the file, see `status: shipped`, and trust the contents were what was actually built.

The PRD is the contract. The agent is the vendor. The sibling implementation doc is the work order. Git is the audit trail.

---

## F. Closing

From Greg's whitepaper *"A practical AI product development lifecycle"*:

> "The throughput of a modern product team is no longer bounded by how fast engineers can type. It is bounded by how fast the team can agree: on a goal, on a constraint, on what 'done' means. Every minute between decision and execution is a minute of inventory."

From the *"Intent Lead Time"* field guide:

> "You cannot manage what you do not measure. ILT is the stopwatch that starts when product commits to an outcome and stops when code referencing that outcome lands. Every PRD that doesn't capture `decided_at` is a stopwatch that never started."

A PRD that honors both of these is a PRD that an agent can pick up, execute, and close the loop on, without the hand-off friction that used to sit between "we decided" and "we shipped."
