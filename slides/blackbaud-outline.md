# Slide outline: Agentic Transformation — Blackbaud Q&A

**Audience.** Blackbaud product / engineering leadership.
**Length.** 12 slides, ~25 min + Q&A.
**Tone.** Field notes voice. Receipts and named anecdotes, no slogans. Drawn from conversations with Abacus, Instacart, Cargurus, Fidelity, Docker, DigitalOcean, GitHub, Archimedes, Variata, Domino, Assignar — plus 7 months running Stoa fully agentic.
**Thread.** Nine questions, nine substantive answers. The story underneath them: tools roll out wide; *the workflow* rolls out narrow. Intent is the new gate. Tests, supply chain, and integration stay human. ILT is the metric nobody is yet tracking.

---

## Slide 1: Title

> **Agentic Transformation.**
> What we're seeing across the portfolio, what we're learning in our own repo.
> Greg Ceccarelli · Stoa / SpecStory · prepared for Blackbaud · April 2026.

Receipt line: *Synthesized from conversations with ~12 named teams, plus 7 months of Stoa shipped fully agentic.*

Visual: dark editorial title, Stoa orange accent, "Q&A" pill in the corner so the audience knows this deck is question-shaped.

---

## Slide 2: The "before" picture

> Where teams started — team size, release cadence, who triggered the change.

**The shape of the field.**
- Larger orgs: scaled-Agile / SAFe + microservices, autonomous-ish teams, but everyone "ends up struggling with… a roadmap planning cadence that tries to cut across all of those teams."
- Startups: traditional startup workflow, monolith, "everybody's building everything." Workflow not as tight or rigorous.
- **Git is a foregone conclusion.** Everyone we talked to is still on feature-branch flow. Larger orgs run long-lived branches (days to weeks); smaller, more agile orgs hold them open for "only a few days."

**What triggered transformation.**
- *In the cases where it happened the fastest, the trigger came from top down — and in a lot of cases from the CEO directly.*
- **Instacart** is the clear example: CEO-championed, pushed top-down across a ~1,000-engineer org.
- Implementation pattern: a dedicated AI-tooling subset of the platform engineering team, owning purchasing, rollout, training, *and* adoption measurement.

**Pull-quote.**
> *"In the cases where it happened the fastest, the trigger decision came from top down. And in a lot of cases from the CEO directly."*

Visual: a four-column "before-state" matrix — Org shape · Git posture · Cadence · Trigger source — with one column highlighting Instacart's CEO-led pattern.

---

## Slide 3: How teams and people reacted

> Two true stories, sized very differently.

**The 5-person greenfield (Assignar).**
- 20–30 engineer org; one 5-person team carved off to build a new construction-finance product.
- CTO sat *on* the team as an active member. Stuck with familiar GitHub flow, but injected agents *as the assignee on tickets* — Copilot picks up the ticket, makes the feature branch, opens the PR. The mechanics matched their old workflow.
- People impact: "*Most of their time writing tickets and then reviewing the output of agents — and very little time on the code itself.*" Code reviews became *structural*. Security reviews ran via a second agent.
- Role shift: engineers pushed *into* product/requirements; PM pushed *into* technical/architectural specs. **Everybody was stretched a little.**
- Hierarchy collapsed: flat. Tickets and specs were taken by whoever had domain expertise. The CTO's role became **"acting as traffic cop"** — sequencing async agent merges to minimize conflicts.
- Mood: excited, "maybe a little trepidatious." Greenfield + new team made it possible.

**The 1,000-engineer org (Instacart).**
- Top-down expectation, but *no project, no kickoff, no cutover point*. Existing teams, existing process — the AI enablement team layered tooling, training, Slack channels, in-person sessions on top.
- Distribution of reactions: early adopters who *loved* it; significant resistance from others ("a whole mix"); a long tail "not actively against, but really dragging their feet."
- The enablement team's own framing: *"they were doing everything they could to drag people along with them."* They literally flew to offices to sit with engineers in person.

**Pull-quotes.**
> *"The CTO was acting as traffic cop in terms of letting all of these asynchronous agent requests get merged in, in the right way, in the right order."*

> *"They felt like they were doing everything they could to drag people along with them."*

Visual: two-column case-study comparison — flat 5-person greenfield vs. 1,000-eng top-down — same shape, very different physics.

---

## Slide 4: Where it failed — and what surprised us

> Failure modes we (and the teams we talk to) actually hit.

**Failure 1 — Prompt-based instead of spec-based.**
- Early attempts threw prompts at the model and watched the output drift. Most teams are past this now.
- *"Agents will perform much better if they're fed with context intentionally — if you do separate turns of the crank in terms of planning versus executing."*
- Specdocs loaded upfront → much better results. Plan / execute is a *boundary*, not a flourish.

**Failure 2 — One teammate runs ahead; shared mental model collapses.**
- The fast person has the model in their head. The system grows. Others can't keep up. *"The context is not there and fully self-contained… even if you check in a bunch of spec documents."*
- The fix is counterintuitive: **intentionally slow down.** Build shared mental models *back* into the team — through intent reviews, documentation, paired sessions on architecture.

**Hardest stages to hand to AI.**
- Unit testing: agents are *good* at this — except when they hallucinate stub-only tests that always pass.
- **Integration testing, smoke testing, manual testing.** This is where the human hand still shows up the most.

**What surprised us positively.**
- The unit of hand-off keeps growing. Two years ago: 30-second nudges. Now: **10–30-minute, sometimes hour-long tasks** are routinely delegated.

**Pull-quote.**
> *"What we've seen is a need to intentionally slow down in order to try and increase shared understanding and shared mental models."*

Visual: two failure cards (Prompt-vs-spec · Fast-teammate drift) + a "hardest to delegate" panel (integration / smoke / manual highlighted in red, unit tests in amber for the stub-hallucination caveat).

---

## Slide 5: Decision gates — what we kept human

> Code review broke. Two new gates moved in.

**The old gate that no longer carries weight.**
- Pull-request line-by-line code review *as the primary gate.*
- **"You can no longer review code line by line the way you would when the code was produced by humans."** Two reasons: quantity, and a mismatch around *intent vs. output.*
- Larger orgs still do line-by-line reviews. Faster-moving teams (Stoa, Assignar) let that go.

**The two gates that replaced it.**

| Gate | Where it sits | What it's for | Hard or soft? |
|---|---|---|---|
| **Intent review** | *Before* implementation | Shared mental model. Course-correct if intent is wrong. | **Soft / non-gating** — agents start implementing in parallel; worst case, scrap. |
| **Integration / smoke / manual testing** | *Between staging and production* | This is where humans exert "heavy influence." | **Hard gate.** |

**What stays human, what moved to agents.**
- Stayed human (mostly): integration test design, smoke test, manual exploratory test, intent.
- Moved to agents: unit test authoring, structural code review, security scans (run via a second agent), commit + PR mechanics, release-note writing.
- Trust shifts: the gates *that exist* haven't moved much in 7 months. What's moved is **how much code we let through** between gates — because we trust the intent-review gate to catch the wrong things early.

**Pull-quote.**
> *"You can no longer review code line by line the way you would when the code was produced by humans. There's a quantity issue — but also a mismatch around intention and expectation."*

Visual: a flow diagram — Intent → Build → Code review (faded) → Staging → **Integration / smoke / manual** → Prod. The two gates we keep are highlighted in Stoa orange; the old one is dimmed.

---

## Slide 6: Metrics — what actually changed

> Heavy adoption, fuzzy gains, moving bottlenecks.

**The productivity paradox is real.**
- 2025 developer survey: **only 16.3% of 30,000 developers** say AI agents significantly improve productivity.
- Faros studies: **75% of engineers use AI tools**, yet most organizations see no measurable performance gains.

**Why it looks fuzzy in aggregate.**
- *"There are multiple bottlenecks. If you're looking at lead time — how quickly a change makes it to production — yes there are improvements, but the bottlenecks move around."*
- Code review is now the choke point. The sheer **volume of code to review** is a new pinch.

**The metric the field isn't measuring yet.**
- DORA's clock starts at `git commit`. The expensive thing now happens *before* commit.
- That gap has a name: **Intent Lead Time (ILT).** Decision captured → first commit. The companion metric to DORA Lead Time for Changes.
- Stoa is tracking it. It is the metric we'd argue *every* AI transformation should baseline this quarter.

**Pull-quote.**
> *"Yes, there are improvements [in lead time]. But the bottlenecks move around."*

Visual: two stat tiles (16.3% · 75%) over a horizontal bottleneck-shifts diagram — code-gen collapses, code-review balloons, intent stays flat. Then a callout: *the part nobody's measuring yet.*

---

## Slide 7: Security, compliance, and IP

> Data exfiltration was the early fear. Supply chain is the live one.

**Solved (mostly).**
- Early posture at advanced orgs like **DigitalOcean**: blanket policy *blocking cloud AI models entirely*. Confusion about training data and exfiltration risk.
- Resolution: cloud-provider partnerships, Bedrock availability, contractual data terms — a "well-established sense of trusted computing for AI usage." Security teams got comfortable.

**Live concerns that are growing, not shrinking.**
1. **Secrets leak more easily.** Subtle, but trending. Agents touch more files, faster, with less ceremony.
2. **Supply chain hygiene is degrading.** NPM and other open-source packages have been compromised; agents incorporate them; *human review on those things has been dropping down*. When humans wrote code by hand, they read package docs, checked versions, audited compromises. With agentic workflows, that doesn't happen — *"and often you see outdated packages or versions being used."*

**Guardrails to put in place.**
- A **decision gate around third-party package inclusion** — currently left to individual developers, "doesn't happen as often as it should."
- **Continuous review with software-supply-chain security scanners.** "Those become absolutely critical, if not more so than in the past."
- Treat secrets-scanning as a first-class CI step, not an afterthought.

**Pull-quote.**
> *"NPM packages and other open-source packages have been compromised, and agents use them and incorporate them — and human review on those things has been dropping down."*

Visual: split panel — left: "early fear (resolved)" with the DigitalOcean blanket-block story; right: two glowing risk cards (secrets · supply chain) above a checklist of three guardrails.

---

## Slide 8: Idea → delivery → maintenance

> The new shape of the loop.

**Process methodology in the field.**
- Most teams: a blend of traditional Agile, scaled Agile, plus a homegrown roadmap planning process layered on top.
- We aren't making the case for ripping that out. We *are* making the case that the artifacts inside it have changed weight.

**Stakeholder communication is the silent loser — *and* a hidden win.**
- The loss: things move so fast that *team members who used to be intimately involved start to lose context.* Stakeholders, customers, internal partners — "it's hard for people to keep up."
- The hidden win: the same AI that produces the code can now produce, and *maintain*, **the secondary artifacts** — change logs, release notes, documentation, internal playbooks, support books. The best teams already do this.

**Artifact promotion: tertiary → first-class.**
- *"Before, we would write them and toss them and say the code is the source of truth."*
- Now, **specs and AS-BUILT architecture become absolutely critical** — agents need them as context; humans need them as the shared mental model. The ranking is flipped.

**Org structure.**
- Most haven't restructured. The pattern that's working: a small, named *AI enablement* function inside platform engineering — owning tools, training, *and adoption measurement.*

**Pull-quote.**
> *"Secondary artifacts — non-code artifacts — end up taking on a higher weight than they ever had before."*

Visual: a left-to-right loop: Idea → Spec → Build → Stage → Release → Maintain. Above the loop: which artifacts the agent is now writing (release notes, changelog, playbooks, AS-BUILT). Below: the human role at each step.

---

## Slide 9: Sequencing — what we'd do again, what we wouldn't

> Roll the tools out wide. Roll the *workflow* out narrow.

**Two sizes of rollout, not one.**

| Rollout | Speed | Why |
|---|---|---|
| **Agentic coding *tools*** | Wide. Org-wide. Now. | **Force multiplier.** *"Even if nothing else about your process changes, there is a difference in productivity."* |
| **Fully agentic *workflow*** (agents writing large chunks of code, not just autocompleting) | Narrow. Controlled experiment. | A team that's bought in. Greenfield if you can get it. Establish a working approach before you scale. |

**The pattern that worked.**
- Stoa's own experience is greenfield + small-team — not fair to extrapolate to enterprises.
- The pattern *across* the field: start with **one team or a small number of teams in ideal circumstances** — new product, new surface — let them *establish an approach* that works inside your org's culture, *then expand.*

**The pattern that didn't.**
- *"Force AI adoption top-down across the set of engineers in your entire organization seems like it was more effort and missteps than [the small-team approach]."*
- Top-down without a controlled team to establish the workflow → AI enablement teams burn cycles "dragging people along."

**Pull-quote.**
> *"Having access to agentic coding tools is a force multiplier. Even if nothing else about your process changes — using versus not using these tools is night and day."*

Visual: a two-lane diagram — *Tool rollout* (wide arrow, full org) · *Workflow rollout* (narrow arrow, one team → expand) — with a quiet footnote about the cost of getting these confused.

---

## Slide 10: If we were starting over — the two extremes to watch

> Both ends of the spectrum will burn you.

**Extreme 1 — Underestimating what agents can do.**
- Capabilities have changed *dramatically* every six months. If your assumptions are based on the experience you had even six months ago, they're stale.
- The countermove: designate a **special team (or small set of teams) pushing agents past what you'd assume they can do.** Give them the latitude to break your old mental model.

**Extreme 2 — Letting go of the things you shouldn't.**
- *"There are some things you should not let go of."*
- **Retain control over intent.** Be explicit about what you want from agents. The intent is yours; the output isn't trustworthy without it.
- **Be rigorous and ruthless in assessing output quality** — *not* in terms of code style, but in terms of **functionality and architectural impact.** That is the human's last and most important job.

**Pull-quote.**
> *"Be rigorous and ruthless in assessing the quality of the output — not in terms of the code, but in terms of the functionality and the architectural impact."*

Visual: a barbell — left weight: "Push agents harder than you assume" · right weight: "Hold the line on intent + functional/architectural review." Both ends labeled; the middle (the comfortable default) is what to avoid.

---

## Slide 11: The thesis underneath all nine answers

> The shift, in one sentence per layer.

- **Bottleneck:** moved from coding to *intent*. Code-gen and deploy collapsed. Decision-to-commit didn't.
- **Gate:** moved from line-by-line code review to **intent review (soft) + integration / smoke / manual (hard).**
- **Artifact:** specs and AS-BUILT architecture went from tertiary to first-class. Agents need them; humans need them.
- **Measurement:** DORA still works post-commit. **Intent Lead Time** (ILT = `t(first commit) − t(decision captured)`) covers the part DORA can't see.
- **Org pattern:** wide tool rollout + narrow workflow rollout + a named AI-enablement function. Don't force the workflow change top-down before a controlled team has shaped it.

The point of building Stoa is to make this loop *routine*: capture intent live, version it next to the code, let agents pick the spec up directly, keep tests and integration sacred, and watch ILT fall.

Visual: a stacked summary card — five rows, one per layer (Bottleneck · Gate · Artifact · Metric · Org). The "before agents → with agents" delta on each row.

---

## Slide 12: Take it home + Q&A

**Three artifacts you can copy tonight (linked in the repo):**
1. **Agentic release-PR workflow** · `takeaways/release-pr-automation/` — drop-in GitHub Actions + gh-aw prompt. Release notes write themselves.
2. **Intent-driven PRD template** · `takeaways/intent-driven-prd-template.md` — the shape of a spec an agent can pick up.
3. **AI-PDLC journey map** · `takeaways/ai-pdlc-journey-map.md` — which tool, which phase, who owns what.

**Three moves for this week.**
- Stand up an **intent review** as a *non-gating* checkpoint upstream of any agent-driven implementation.
- Add a **third-party package gate** + a software-supply-chain scanner on every push.
- Baseline **ILT** for one feature this sprint. Anything is a baseline.

**Open questions I'd love to push on with you.**
- Which Blackbaud surface is *most ready* for a fully-agentic-workflow pilot? (Greenfield > brownfield, by a lot.)
- What's your current AS-BUILT-doc posture? (If the answer is "we don't have one," that's the first artifact to commission.)
- Where would you rather pay the coordination cost of the change — at the tool layer (wide), or the workflow layer (narrow)?

**Closing line.**
> *The clock starts the moment your team agrees.*

Visual: three take-cards (the artifacts) + three move-rows + an end-card with byline & deck URL.

---

## Quote bank (pull-ready)

**Triggers & adoption**
- "Git is a foregone conclusion. Most of the teams we talk to are traditionally still using a feature-branch-based approach." (00:03:00)
- "In the cases where it happened the fastest, the trigger decision came from top down. And in a lot of cases from the CEO directly." (00:03:30)

**Roles**
- "Most of their time writing tickets and then reviewing the output of agents — and very little time on the code itself." (00:06:40)
- "The CTO was acting as traffic cop in terms of letting all of these asynchronous agent requests get merged in." (00:08:47)
- "They were doing everything they could to drag people along with them." (00:09:32)

**Failure / surprise**
- "Agents will perform much better if they're fed with context intentionally — if you do separate turns of the crank in terms of planning versus executing." (00:11:30)
- "A need to intentionally slow down in order to try and increase shared understanding and shared mental models." (00:14:15)
- "Hallucinate and end up writing tests that always pass because they're fully stubbed out." (00:17:14)

**Gates**
- "You can no longer review code line by line the way you would when the code was produced by humans." (00:15:20)
- "It's actually not a gate — it's a non-gating intent review." (00:16:00)
- "The place that continues to be both challenging and also a place for humans to exert heavy influence is on integration, smoke, and manual testing." (00:17:30)

**Metrics**
- "Only 16.3% of 30,000 developers say AI agents significantly improve productivity." (2025 dev survey · 00:18:30)
- "75% of engineers use AI tools — most organizations see no measurable performance gains." (Faros studies · 00:18:45)
- "The bottlenecks move around." (00:19:10)

**Security**
- "Even advanced technical organizations like DigitalOcean had a policy to completely block use of cloud AI models." (00:20:00)
- "Human review on those things has been dropping down." (00:21:30)
- "Software supply chain security scanners and tooling… become absolutely critical, if not more so than in the past." (00:22:25)

**Process**
- "Secondary or non-code artifacts end up taking on a higher weight than they ever had before." (00:24:30)
- "Specs and the as-built architecture become absolutely critical." (00:25:00)

**Sequencing**
- "Force AI adoption top down across the set of engineers in your entire organization seems like it was more effort and missteps." (00:25:50)
- "Having access to agentic coding tools is a force multiplier." (00:26:50)
- "Code-generation piece being fully agentic… has benefited from being done in a more controlled environment." (00:27:50)

**If starting over**
- "Things have changed dramatically [in just six months]." (00:28:50)
- "Be rigorous and ruthless in assessing the quality of the output — not in terms of the code, but in terms of the functionality and the architectural impact." (00:29:30)
