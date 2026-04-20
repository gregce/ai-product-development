# AI-PDLC journey map

The poster version of slide 9. Where every AI tool actually fits across the
product development lifecycle, who owns what, and which sub-metric of Intent
Lead Time each phase moves.

```
  ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │          │   │              │   │          │   │          │   │          │   │          │
  │ IDEATION │──▶│    INTENT    │──▶│   SPEC   │──▶│  BUILD   │──▶│   TEST   │──▶│ RELEASE  │
  │          │   │   CAPTURE    │   │          │   │          │   │          │   │          │
  └──────────┘   └──────────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
    human         human + agent      human + agent    agent         human spec /    agent
    owned         co-owned           co-owned         owned         agent impl      owned
                                                                    (sacred rule)
```

Humans own the two endpoints and the test *specification*. Agents own the four
middles and the test *implementation*. The handoff between Spec and Build is
the one to automate first — that's where the ILT wins live.

---

## 1. Ideation

**Who owns it.** Human. This is the "what problem are we even solving" phase.
Agents are spectators.

**Artifact.** A problem doc, a customer-call transcript, a Gong clip, a Slack
thread with enough signal. Messy by design. Not yet structured.

**Representative tools.**

- Product management: Linear, Jira, Productboard, Aha, Shortcut.
- Voice of customer: Gong, Chorus, Grain, customer support transcripts,
  NPS/CSAT dumps.
- Discovery: user interviews, Mixpanel / Amplitude / PostHog event data,
  session-replay tools (FullStory, LogRocket).

**ILT sub-metric moved.** None directly — but the *clarity* of the problem
statement here caps how fast Capture can be in the next phase. Murky
ideation = long Capture latency downstream.

**Watch out for.** Dropping straight from ideation into Build (vibe-coding a
prototype before the problem is named). It looks fast. It isn't — the ILT
clock hasn't started because nothing has been decided yet.

---

## 2. Intent capture

**Who owns it.** Human and agent, co-owned. Human makes the decision; agent
(or transcription tooling) can help capture it in the moment.

**Artifact.** A meeting transcript with the decision highlighted, a timestamped
note, a voice memo transcribed and tagged. Structured enough to answer "who
agreed to what, when?"

**Representative tools.**

- Meeting capture: Stoa (agent-attended meetings), Granola, Read.ai,
  Fireflies, Otter, Fathom.
- Live decision capture: Claude / ChatGPT attending a call, voice-to-text
  dictation, structured Slack templates.
- Decision logs: markdown in-repo, ADR tooling (adr-tools), Linear's
  "decisions" field, Notion decision database.

**ILT sub-metric moved.** **Capture latency** — decision made → decision
recorded. In the old world this was "we'll document it later" (weeks). With
agent-attended capture it drops to seconds.

**Watch out for.** Capturing *conversation* instead of *decisions*. A
transcript isn't intent. The distillation to a single sentence — "we decided
X because Y" — is what an agent downstream can actually pick up.

---

## 3. Spec

**Who owns it.** Human and agent, co-owned. Human owns the outcome, the
constraints, and the out-of-scope list. Agent can help draft, pattern-match
against prior specs, and flag ambiguity.

**Artifact.** A markdown PRD (see `intent-driven-prd-template.md` in this
folder), or a prototype-as-spec, or a Figma Make / Lovable / v0.dev
interactive surface. Versioned in the repo if possible. Timestamped.

**Representative tools.**

- Markdown in-repo: the default. Editor + git + review.
- Prototype-as-spec: Lovable, v0.dev, Bolt, Figma Make, Replit Agent.
- Plan-mode agents: Claude Code in plan mode, Cursor's composer in planning,
  Codex with spec generation.
- Diagram tools when the spec needs architecture: Excalidraw, Mermaid in
  markdown, Miro for collaboration.

**ILT sub-metric moved.** **Sequencing latency** — artifact exists → ticket
created (or in an agent-driven workflow, → agent pickup). When the PRD *is*
the assignment, sequencing collapses to zero.

**Watch out for.** Writing 30-page specs the agent will skim at best. Dense
prose is not precision. The test is: can an agent read this and start work
without a clarifying round-trip? If no, the spec is too long or too vague.

---

## 4. Build

**Who owns it.** Agent, with a human orchestrator. The agent executes the
spec; the human reviews intermediate output, catches off-intent drift, and
decides when to commit.

**Artifact.** A branch (or direct-to-trunk commits in trunk-based flows),
commits referencing the PRD, and the PR itself.

**Representative tools.**

- IDE-embedded agents: Cursor, Claude Code, GitHub Copilot (agent mode),
  Windsurf, Zed with AI.
- Terminal-native agents: Claude Code in a tmux pane, Codex CLI, aider.
- Sandboxed remote agents: E2B, Daytona, Modal, GitHub Codespaces with
  agent extensions, Replit Agent.
- Pair-agent review: a second model reviewing the first's output before
  commit (e.g. GPT-5 checking Claude-generated code, or vice versa).

**ILT sub-metric moved.** **Pickup latency** — work available → work started.
Agents don't queue, don't triage, don't wait for the next sprint. Pickup
collapses to roughly the cost of dispatching a prompt.

**Watch out for.** Agents ship on the wrong intent *faster* if the intent
isn't structured. The speed boost is real only when Spec is tight. Murky
spec + fast agent = high-velocity wrong turn. This is the biggest regret
you can have in the new stack.

---

## 5. Test

**Who owns it.** **Split ownership by design.** Humans own the *specification*
of what to test (the sacred rule). Agents own the *implementation* of that
specification.

**Artifact.** A test suite — unit, integration, end-to-end — co-versioned
with the spec and code. Plus manual/exploratory test notes where the domain
demands it.

**Representative tools.**

- Unit / integration: Vitest, Jest, pytest, Go `testing`, JUnit, RSpec.
- End-to-end: Playwright, Cypress, WebdriverIO, Detox (mobile).
- Visual regression: Percy, Chromatic, Playwright screenshots.
- Contract / API: Pact, Dredd, Postman / Insomnia suites.
- Human-owned spec tooling: Gherkin / Cucumber feature files, plain-english
  acceptance criteria (like the `[human]` lines in the PRD template).
- Load / chaos: k6, Locust, Gremlin, Chaos Mesh.

**ILT sub-metric moved.** **Activation latency** — assigned → first
executable. When tests are co-versioned with the spec, "done" is
unambiguous. No back-and-forth on what "works" means.

**Watch out for.** Letting the agent write the *specification* of the tests
as well as the code. Tests encode shared domain judgment; they are the
place AI must not substitute its inferred intent for yours. Quote Diwank
Singh: "Never. Let. AI. Write. Your. Tests." The nuance (per the whitepaper):
it's the *specification* of tests that must stay human-owned. Implementation
can be agent-assisted.

---

## 6. Release

**Who owns it.** Agent, with humans approving the gate. The agent assembles
the release summary, posts the fanout, and orchestrates the merge. Humans
confirm go/no-go.

**Artifact.** A pull request with an agent-authored body, a Slack / Teams
announcement, the merged release, and the deploy trace that follows.

**Representative tools.**

- Agentic release PRs: gh-aw (GitHub Agentic Workflows), the
  `release-pr-automation/` kit in this folder.
- CI / CD: GitHub Actions, GitLab CI, CircleCI, Buildkite, Argo, Spinnaker.
- Fanout: Slack webhooks (see the TODO block in the automation kit),
  Discord, Teams, status-page automation (Statuspage, Instatus).
- Post-release: feature flags (LaunchDarkly, Unleash, Flagsmith),
  observability (Datadog, Honeycomb, Sentry) feeding back into Ideation
  for the next cycle.

**ILT sub-metric moved.** **Activation latency**, continued — the last mile
from "code merged" to "users experiencing the change." Agentic release PRs
collapse the handoff between engineering and the rest of the org.

**Watch out for.** Releasing the agent's summary as canonical without
actually reading it. The agent is good; it isn't infallible. A 30-second
human skim of the release body is the cheap insurance against shipping a
mischaracterized change.

---

## How to read this poster

Run one finger along the chevron at the top. Each phase has an owner, an
artifact, a cluster of tools, and exactly one ILT sub-metric it moves.
Your job as a leader is to figure out *which phase your team is slowest at*
and instrument that one first. All four ILT sub-metrics can go to roughly
zero in an intent-driven workflow — but only if you measure them.

For the metric definitions: see slide 8 of the deck and the
[Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time).

For the whitepaper that defines the Intent + Code + Tests stack: see
`docs/beyond-code-centric-whitepaper.txt` in this repo.

---

> **"Never let AI specify your tests."**
> — *Beyond Code-Centric* (SpecStory, 2025), paraphrasing Diwank Singh.
> Tests encode shared domain judgment. That's the sacred boundary, and it's
> what keeps the agent era honest.
