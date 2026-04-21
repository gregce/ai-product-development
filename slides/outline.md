# Slide outline: How product development works in an AI world

**Audience.** Alpine SG portfolio-company product leaders.
**Length.** 11 slides + 3 appendix, ~25 min + live demo + Q&A.
**Tone.** Opinionated. Receipts, not slogans. Use Stoa's own repo as the live case study.
**Thread.** Coding collapsed. Deploy collapsed. Intent didn't. Here's what to do about it, and here are three artifacts you can take home.

---

## Slide 1: Title

> **How product development works in an AI world.**
> Not a prediction. A practice.
> Greg Ceccarelli · Stoa / SpecStory · Alpine SG · April 2026.

Kicker line under the title: *Examples on these slides are drawn from one repo we shipped over the last 7 months.*

Visual: full-bleed dark title, accent orange (Stoa brand `#e35a2c`). Byline with LinkedIn + X.

---

## Slide 2: The question

Product leaders have been asking four things. I'm focusing in on one of them today.

- "How do I jolt my team to accelerate?"
- "How do I go from individual AI usage to a team-wide system?"
- "How should *product development* work in an AI world?" ← **today**
- "How do I measure productivity beyond lines of code?"

Sub-questions inside today's theme:

- Are PRDs the future?
- What does end-to-end AI product development actually look like?
- What bridges product-AI workflows and engineering-AI workflows?
- What happens *after* the prototype: security, handoff, release?

Visual: 2×2 grid of the four questions, one highlighted.

---

## Slide 3: Journey map · before agents

How product shipped, before agents. A specialist at every step. The craft lived in each person's expertise and in the handoffs between them. Coding was the anchor because coding was the skill.

Eight phases, all human: Discover → Ideation → Reqs → Design → Build → Test → Release → Measure.

Two takeaways:
- **Specialists at every step.** Researcher, PM, designer, engineer, QA, ops. Each phase was its own craft; coordinating across them was the job PMs and eng leads were hired for.
- **Coding was the anchor.** Implementation took the most time. Weeks per feature was expected, because careful human coding was the expertise the whole team queued behind.

Visual: horizontal chevron row, eight "Human" cells.

---

## Slide 4: Journey map · with agents

Where AI fits. Where it doesn't. Humans anchor the two endpoints (Discover + Release). Tests stay **human-owned**, always. Agents drive the middles.

- Discover: research with AI · human + agent
- Ideation: problem sensing · human
- Reqs: live intent capture · human + agent
- Design: markdown, in repo · human + agent
- Build: agent in sandbox · agent
- Test: human-owned spec, agent impl ← **sacred boundary**
- Release: agentic PR · human + agent
- Measure: agentic observability · human + agent

Two takeaways:
- **Sacred rule.** *Never let AI specify your tests.* Tests encode shared domain judgment about what "correct" means. Ceding that cedes control.
- **Automate first: the SPEC → BUILD handoff.** That's where activation latency lives. If the spec is picked up by the agent without a human re-routing it, most of your ILT disappears.

Visual: chevron row again, now tagged with Human / Agent / both. The poster version of this slide is the `ai-pdlc-journey-map.md` takeaway.

---

## Slide 5: The bottleneck that didn't collapse

Two collapses happened, on very different clocks:

| Phase | 2015 | 2026 |
|---|---|---|
| Intent capture | weeks | **weeks still** |
| Implementation | days to weeks | **hours** (agents) |
| Deploy | hours to days | **minutes** (CI/CD) |

The bottleneck moved. **DORA can't see it by design.** DORA's clock starts at `git commit`. The expensive thing now happens *before* commit.

> **ILT = t(first commit) − t(product decision captured)**

That gap has a name now: **Intent Lead Time (ILT)**. It's the companion metric to DORA's Lead Time for Changes. Together they measure the full pipeline from agreement to production. ILT ends exactly where DORA's clock starts. No overlap. No gap.

Visual: two-clocks table alongside a striped-orange timeline bar, marked "decision captured → first commit → prod." Left segment is ILT; right is DORA LT.

Source: [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time), companion to the [Beyond Code-Centric whitepaper (2025)](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf).

---

## Slide 6: A metric you can use on Monday

**Intent Lead Time, four sub-components:**

| Sub-metric | Clock | What slows it |
|---|---|---|
| Capture latency | decision made → recorded | "we'll document it later" |
| Sequencing latency | artifact → ticket | triage queue, sprint cadence |
| Pickup latency | ticket → assigned | backlog prioritization |
| Activation latency | assigned → first commit | spec ambiguity |

**Bands** (first-principles estimates, not benchmark data):

| Band | ILT | Description |
|---|---|---|
| Elite | < 1 hour | Intent captured live. Agents in the decision session. |
| High | 1 hour → 1 day | Structured specs. Same-day ticket flow. |
| Median | 1 → 3 weeks | Meeting → doc → ticket → assign → commit. |
| Low | > 4 weeks | Decisions surface in Slack and never get structured. |

Only the first sub-component is load-bearing in an intent-driven workflow. Sequencing / pickup / activation are scaffolding from the assembly-line era. **When the picker is an agent, the spec *is* the assignment.** Tickets-per-engineer goes down; throughput goes up. That's the signal.

Visual: the ILT timeline from slide 5, now exploded into the four latency segments.

---

## Slide 7: The stack

**PRDs aren't going away. The *format* is.** Static Google / Notion docs become a living markdown artifact in the same repo as the code, read by humans and agents on the same line.

Robert C. Martin, *Clean Code*, 2008: *"Specifying requirements so precisely that a machine can execute them is programming. Such a specification is code."* He was early. In the agent era he's load-bearing.

- **Old stack:** Code + Tests. Spec is a PDF nobody re-opens.
- **New stack** (from the whitepaper): **Intent** + Code + Tests. Intent is declared, versioned, live in the repo. The spec *is* the assignment.

Visual: two stacks side by side. Old: 2-layer. New: 3-layer with **Intent** in Stoa orange.

---

## Slide 8: The opinionated cut

Three practices die. One lives.

- **Dies.** Tickets as the unit of work. (Sequencing latency goes to zero when the picker is an agent.)
- **Dies.** Long-lived branches as the unit of collaboration. (GitFlow assumed slow coders.)
- **Dies.** PRs as the unit of review. (Scaffolding from the slow-implementation era; drag, not gate.)
- **Lives.** Trunk-based development. One source of truth. Specs + code + tests versioned together. Near-instant implementation eliminates the need to defer integration.

> "In a truly intent-driven workflow, sequencing, pickup, and activation will collapse to zero."
> — Intent Lead Time guide, April 2026

Your tickets-per-engineer counts drop while throughput climbs. That's the signal. The scaffolding around code was all sized for the old bottleneck. Remove it.

Visual: four kill-cards, three struck through, one (Trunk) alive in orange.

---

## Slide 9: Stoa as receipt

I don't just pitch this. I live it daily. Every number on this slide is mined from the `specstoryai/stoa` monorepo at deck-build time.

- **168 design docs** in `docs/design/` · earliest 2025-01-16, latest 2026-04-18.
- **177 implementation docs** in `docs/implementation/` · earliest 2025-09-15, latest 2026-04-19.
- **10,672 lines** of AS-BUILT architecture across **5 components**, with **65 ASCII diagrams** and **176 code fences**, all last-updated within *8 days* of each other.

Thematic breakdown (design vs. impl):

| Theme | Design | Impl | Read |
|---|---:|---:|---|
| Platform / arch | 52 | 28 | architecture is intentionally over-specified vs. over-built |
| Agents | 40 | 32 | biggest product surface, proportionate implementation |
| CRDT / automerge | 26 | 32 | foundational, docs drive the code |
| Meetings / voice | 21 | 23 | parity; new product surface |
| CLI / terminal | 18 | 26 | implementation-heavy (as you'd expect) |
| P2P / sync | 18 | 11 | design-heavy (sync is the hard part) |
| Billing / auth | 3 | 26 | the "security and handoff" gap; design-light, impl-heavy |

Top term across 345 combined docs: **"intent"** (7,589 occurrences). The word itself carries the team.

**March 2026** (38 design / 46 impl) was our push into native Windows, the Intent→Stoa rebrand, and the meeting-document surface. Docs track surges; they don't lag them.

Visual: theme bar chart (design vs. impl) alongside a monthly density chart.

---

## Slide 10: Live demo · the agentic release

A `dev → main` release PR that writes itself. Humans don't read release diffs. Our fix: **the PR writes itself.** Four files in `.github/workflows/`, running on every push to `dev`.

**The pipeline:**

1. **Orchestrator** · `release-pr-sync.yml` — on every push to `dev`, find-or-create the single standing "Release dev to main" PR. One PR per release cycle, not one per push.
2. **Agent** · `release-pr-body.md` (gh-aw prompt, Claude) — reads the full `main…dev` diff plus every touched `docs/design/` and `docs/implementation/` file. Synthesizes a structured release body: Highlights, Major Change Areas, Operational Notes, Commits. Bounded tools: `repos` + `pull_requests`. Safe output: `update-pull-request × 1`. No shell.
3. **Outputs** — PR body is the canonical release narrative. Same content reshaped to Slack mrkdwn and posted to `#release-stream`. Humans review the summary, click merge.

**Proof it runs.** Last five "Release dev to main" PRs in `specstoryai/stoa`: #11, #12, #13, #14 merged; #16 currently open. 4 of 5 merged; two merged in under 10 minutes, because the agent had already written the summary humans would have put off.

**Guardrails.** One standing PR. `main-from-dev-only.yml` rejects any PR into main whose head ≠ `dev`. The *prompt* is a markdown file humans edit; `release-pr-body.lock.yml` is generated by `gh aw compile`. Slack gets the same canonical body — no duplicate writing.

This is in `takeaways/release-pr-automation/`. Adapt, ship, brag.

Visual: three-stage pipeline (Orchestrator → Agent → Outputs), plus a PR table showing the last five release PRs with lifespans.

---

## Slide 11: Take it home

Three assets to steal. Three moves to make this week.

**Assets:**

1. **Agentic release-PR workflow** · `takeaways/release-pr-automation/`: drop-in GitHub Actions + gh-aw prompt. Your release notes will write themselves tonight.
2. **Intent-driven PRD template** · `takeaways/intent-driven-prd-template.md`: the shape of a PRD an agent can actually pick up. Four sections. No ticket required.
3. **AI-PDLC journey map** · `takeaways/ai-pdlc-journey-map.md`: poster version of slide 4, with tools called out by phase.

**Moves:**

- **Move 01 — Put one canonical workflow under the agent.** Release notes, incident summaries, RFC intake. Let it write the body.
- **Move 02 — Version your intent.** One markdown doc, in the repo, with the decision timestamp in the commit.
- **Move 03 — Measure ILT for one feature.** Anything is a baseline. `t(first commit) − t(decision)`.

> The clock starts the moment your team agrees.

Visual: three take-cards linking to each artifact, three moves paired below, end-card with byline + deck URL.

---

## Appendix A (Slide 12): On agents.md, claude.md, and skills

A minority report on agent conventions. Everyone is curating `AGENTS.md`, `CLAUDE.md`, and custom skills. I don't think most of it earns its keep. Three things do.

**What I don't buy:**
- `AGENTS.md` / `CLAUDE.md` churn — different format per tool, bloats toward a wiki nobody audits.
- Custom skill gardens — too narrow, age poorly, maintenance cost exceeds per-use value.
- Slash-command metadata — a tax you pay forever for a speedup you forget about in a week.

**What actually compounds:**
1. **One doc per surface: `AS-BUILT-ARCHITECTURE.md`.** One living doc per product surface (CLI, web, desktop, backend). Kept current. Agents `@`-reference it as their first pass. Receipt: Stoa ships 5 of these, 10,672 lines, all last-updated within 8 days of each other.
2. **Prose-thick commits.** Not `fix bug`. Paragraphs — the why, the constraint, the follow-up. Co-authored with the agent that did the work. Your `git log` becomes the search index nobody else's repo has.
3. **Two skills that earn it.** `impeccable.style` for design/style review; `last30days` for real-time research past the training cutoff. Both narrow enough to age well, general enough to use weekly.

> A new markdown-file convention is not architecture. **Your AS-BUILT doc is.**

---

## Appendix B (Slide 13): What an AS-BUILT.md looks like

Structural exemplar pulled from `stoa-cli/AS-BUILT-ARCHITECTURE.md` (3,250 lines · 48 code fences · 21 ASCII diagrams · last updated 2026-04-13).

Table of contents, verbatim: Overview → System Architecture → Package Structure → Data Flow Diagrams (Real-Time Change / Offline Sync / Episode Switching / LLM-Powered Merge / Remote Sync) → Core Components (23 of them: Service Manager, File Watcher, Correlation Engine, CRDT Manager, Outbox, Journal, Timeline, Ask Service, Shell, Git Integration, Episode Manager, Explorer TUI, Snapshot, Digest, Exchange Watcher, Git Watcher, Provenance, Git Status Filter, Agent Observer, Path Utilities, Actor Identity, Space Daemon, Provenance Marks, TUI, Remote Sync) → Storage Architecture → Network & Collaboration → Technology Stack → Performance & Scale → Security & Privacy → Future Architecture.

Why show this: most AI-era "architecture docs" are one page of bullets. An AS-BUILT is the receipt that the architecture is actually *there*, in the repo, in enough detail that an agent can `@`-reference it as its first pass and make a correct plan.

Visual: a rendered markdown mockup of the actual TOC, with section line numbers.

---

## Appendix C (Slide 14): Harness & workflow

Two harnesses, many terminals, saved sessions. How I actually run this day-to-day. Opinionated, not a review. These are the four practices that compound.

1. **Tandem harnesses — Claude Code + Codex.** Not one or the other. Claude Code for orchestration and parallel agent teams; Codex with `gpt-5.4-xhigh` for complex implementations and second-opinion audits. Claude drafts → Codex checks. Or Codex implements the hard part while Claude reviews. The two compound.
2. **Plan before you touch — violent plan mode + agent teams.** Start with `/plan`. Let the agent enumerate before it edits. Fan out via agent teams (Claude) or sub-agents (Codex). The coordinator coordinates; it doesn't do the mechanical work. Plans are often the entire value. Edits are mechanical once the plan is right.
3. **Context lives in terminals — many named terminals, in Cursor.** Six to ten open at once, each one named. One per repo, one per long-running agent. Stop holding context in your head; the names do it. Modern compaction means each session's context is cheap to carry.
4. **History as context — SpecStory CLI for session memory.** Every session saves to `.specstory/history/`. When a new session needs context from an old one, pipe the relevant markdown into the prompt. Zero re-priming. The history *is* the context.

> **Plan more. Type less.**

---

## Raw quotes bank (for callouts & pull-quotes)

**Whitepaper, Beyond Code-Centric (SpecStory, 2025):**
- "Software's bottleneck has moved: it's no longer about how fast we type but how clearly we think."
- "In this model, humans focus on understanding user needs, making architectural tradeoffs, and precisely articulating intent."
- "Never. Let. AI. Write. Your. Tests." (Diwank Singh, quoted)
- "The specification is still code, just a different kind."
- "Teams that master the art of iterative specification to orchestrate agents will own the future."

**Intent Lead Time guide (April 2026):**
- "DORA gave us the metrics for the DevOps era. Intent Lead Time is the metric for the agentic era."
- "The clock starts the moment your team agrees."
- "Software has always had what I've called the intent gap."
- "In a truly intent-driven workflow, sequencing, pickup, and activation will collapse to zero."

**Robert C. Martin (*Clean Code*, 2008):**
- "Specifying requirements so precisely that a machine can execute them is programming. Such a specification is code."
