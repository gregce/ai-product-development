# Slide outline — How product development works in an AI world

**Audience.** Alpine SG product leaders.
**Length.** 10 slides, ~25 min + live demo + Q&A.
**Tone.** Opinionated. Receipts, not slogans. Use Stoa's own repo as the live case study.
**Thread.** Coding collapsed. Deploy collapsed. Intent didn't. Here's what to do about it, and here are three artifacts you can take home.

---

## Slide 1 — Title

> **How product development works in an AI world.**
> Not a prediction. A practice.
> Greg Ceccarelli · Stoa / SpecStory · Alpine SG · April 2026.

Kicker line under the title: *Examples on these slides are drawn from one repo we shipped over the last 7 months.*

Visual: full-bleed dark title, accent orange (Stoa brand `#e35a2c`) on the word **Intent**. Subtle grid.

---

## Slide 2 — The question

Product leaders have been asking four things. We're answering one of them today.

- "How do I jolt my team to accelerate faster?"
- "How do I go from individual AI usage to a team-wide system?"
- "How should *product development* work in an AI world?" ← **today**
- "How do I measure this?"

Sub-questions inside today's theme:

- Are PRDs the future?
- What does end-to-end AI product development actually look like?
- What bridges product-AI workflows and engineering-AI workflows?
- What happens *after* the prototype — security, handoff, release?

Visual: 2×2 grid of the four questions, one highlighted.

---

## Slide 3 — The shift nobody priced in

Two collapses happened, on very different clocks:

| Phase | 2015 | 2026 |
|---|---|---|
| Intent capture | weeks | **weeks still** |
| Implementation | days to weeks | **hours** (agents) |
| Deploy | hours to days | **minutes** (CI/CD) |

The bottleneck moved. DORA can't see it by design — DORA's clock starts at `git commit`. The expensive thing now happens *before* commit.

> **ILT = t(first commit) − t(product decision captured)**

That gap has a name now: **Intent Lead Time (ILT)**. It's the companion metric to DORA's Lead Time for Changes. Together they measure the full pipeline from agreement to production.

Visual: timeline bar. "Decision — *ILT* — first commit — *DORA LT* — prod running." Two clocks, one gap.

Source: [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time), companion to the [Beyond Code-Centric whitepaper (2025)](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf).

---

## Slide 4 — From code-centric to intent-centric

Robert C. Martin, *Clean Code*, 2008:

> "Specifying requirements so precisely that a machine can execute them is programming. Such a specification is code."

He was early. In the agent era he's load-bearing.

**Old stack:** Code + Tests. Spec is a PDF nobody re-opens.

**New stack (from the whitepaper):** **Intent** + Code + Tests. Intent is declared, versioned, timestamped — the spec *is* the assignment.

This is what kills "are PRDs the future?" as a question. PRDs aren't going away. The *format* is. Static Word doc → living markdown artifact in the same repo, read by humans and agents on the same line.

Visual: two stacks side by side. Old: 2-layer. New: 3-layer with **Intent** in Stoa orange.

---

## Slide 5 — The opinionated cut

Three things die. One thing lives.

**Dies.** Tickets as the unit of work. (Sequencing latency is ~0 when the picker is an agent.)
**Dies.** Long-lived branches as the unit of collaboration. (GitFlow assumed slow coders.)
**Dies.** PRs as the unit of review. (They're scaffolding from the slow-implementation era — they're now drag, not gate.)

**Lives.** Trunk. One source of truth. Specs + Code + Tests versioned together in one repo.

> "In a truly intent-driven workflow, sequencing, pickup, and activation will collapse to zero."

This is the workflow shape. The scaffolding *around* code was all sized for the old bottleneck.

Visual: four icons with strike-throughs on three; fourth (trunk) in orange and upright.

---

## Slide 6 — Stoa as receipt

I don't just pitch this. I live it daily. Here's our repo over 7 months, entirely mined by the scripts that produced this talk.

- **168 design docs** in `docs/design/` · earliest 2025-01-16, latest 2026-04-18.
- **177 implementation docs** in `docs/implementation/` · earliest 2025-09-15, latest 2026-04-19.
- **5 AS-BUILT architecture docs** across the monorepo — **10,672 lines**, **65 ASCII system diagrams**, **176 code fences**, all last-updated within *8 days* of each other.

Thematic breakdown (design vs. impl):

| Theme | Design | Impl | Read |
|---|---:|---:|---|
| Platform / arch | 52 | 28 | architecture is intentionally over-specified vs. over-built |
| Agents | 40 | 32 | biggest product surface, proportionate implementation |
| CRDT / automerge | 26 | 32 | foundational, docs drive the code |
| Meetings / voice | 21 | 23 | parity — new product surface |
| CLI / terminal | 18 | 26 | implementation-heavy (as you'd expect) |
| P2P / sync | 18 | 11 | design-heavy (as you'd expect — sync is the hard part) |
| Billing / auth | 3 | 26 | the "security and handoff" gap — design-light, impl-heavy |

Top term across 345 combined docs: **"intent"** (7,589 occurrences). The word itself carries the team.

Visual: two-column bar chart of themes (design vs impl), or a monthly density stacked bar. Data is captured at deck-build time from `specstoryai/stoa` and inlined into `index.html`.

---

## Slide 7 — The agentic release, live

This is the concrete example leaders can copy. A `dev → main` release PR that writes itself.

**What's wired up** (4 files in `.github/workflows/`):

1. `release-pr-sync.yml` — on push to dev, find-or-create a single standing "Release dev to main" PR.
2. `release-pr-body.md` — a gh-aw prompt invoking Claude with `{repos, pull_requests}` toolsets. It reads the accumulated diff, looks at the touched `docs/design/` and `docs/implementation/` files, and rewrites the PR body with Highlights / Major Change Areas / Operational Notes / Commits.
3. `release-pr-body.lock.yml` — generated YAML (`gh aw compile`). Humans edit the prompt; tooling owns the YAML.
4. `main-from-dev-only.yml` — rejects any PR into main whose head isn't `dev`. The agent's summary isn't nice-to-have; it's canonical.

**Proof it runs.** 5 real "Release dev to main" PRs in the last 4 days: #11, #12, #13, #14 merged; #16 currently open. Median time from open to merge: under an hour.

Why it's interesting:
- The PR body is written by the LLM. It reads the actual diff and the matching design/impl markdown. That's intent-aware review — *because* intent is in the repo.
- Bounded tools. One `update-pull-request` safe output. No shell.
- Output is reused: same body is posted to Slack with `## H`→`*bold*` rewriting.

This is in your takeaways folder. Adapt, ship, brag.

Visual: vertical pipeline diagram. dev push → sync workflow → gh-aw agentic rewrite → updated PR body → Slack fanout → merge.

---

## Slide 8 — A metric you can use on Monday

Leaders have been asking for "objective metrics beyond lines of code." Here's one.

**Intent Lead Time — four sub-components:**

| Sub-metric | Clock | What slows it |
|---|---|---|
| Capture latency | decision made → decision recorded | "we'll document it later" |
| Sequencing latency | artifact exists → ticket created | triage queue |
| Pickup latency | ticket created → assigned | prioritization backlog |
| Activation latency | assigned → first commit | spec ambiguity |

**Bands** (first-principles, not benchmark data — yet):

| Band | ILT |
|---|---|
| Elite | < 1 hour |
| High | 1 hour → 1 day |
| Median | 1 → 3 weeks |
| Low | > 4 weeks |

**The provocation:** in a truly intent-driven workflow three of the four sub-components collapse to zero. Your tickets-per-engineer goes down while throughput goes up. That's the signal.

Visual: four stacked bars showing the 4 sub-components, with the bottom three fading to zero in the "agentic" column.

---

## Slide 9 — Journey map: AI across the PDLC

Where every AI tool actually fits, with a human-judgment floor underneath.

```
IDEATION → INTENT CAPTURE → SPEC → BUILD → TEST → RELEASE
                                                       
   (humans)   (live meeting,    (markdown,  (agent    (humans   (agentic
              agent-attended,   versioned)  in sandbox specify,  release
              decisions         or CLI)     agent      PR)
              extracted)                    implements)
```

Opinions baked in:
- **Never let AI specify your tests.** Tests encode shared domain judgment. That's the sacred boundary (per the whitepaper).
- Humans own the two endpoints and the test *spec*. Agents own the four middles.
- The handoff between SPEC and BUILD is the one to automate first — that's where the ILT wins live.

Visual: horizontal chevrons, each with the human/AI role stacked vertically, and a single red line under TEST saying "human-owned spec."

---

## Slide 10 — Take it home

Three things to steal. All in this repo.

1. **Agentic release-PR workflow** · `takeaways/release-pr-automation/` — drop-in GitHub Actions + gh-aw prompt. Your release notes will write themselves tonight.
2. **Intent-driven PRD template** · `takeaways/intent-driven-prd-template.md` — the shape of a PRD an agent can actually pick up.
3. **AI-PDLC journey map** · `takeaways/ai-pdlc-journey-map.md` — the poster version of slide 9, with tools called out by phase.

Three moves to make this week:

- **Measure ILT** for one feature. Anything is a baseline.
- **Put one canonical workflow under the agent** — release notes, incident summaries, RFC intake. The body writes itself.
- **Version your intent.** One markdown doc, in the repo, with the decision timestamp in the commit.

The clock starts the moment your team agrees.

Visual: three cards, each linking to its takeaway file. Bold CTA. Contact / deck URL.

---

## Raw quotes bank (for callouts & pull-quotes)

**Whitepaper — Beyond Code-Centric (SpecStory, 2025):**
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
