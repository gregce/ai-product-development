# How product development works in an AI world

A 10-slide deck, four analysis scripts, and three copy-me takeaway artifacts.
Built for a live talk to Alpine SG portfolio-company product leaders in April 2026.

**Live deck.** Open [`index.html`](./index.html) in any browser — or view it on GitHub Pages once the repo is pushed public. Arrow keys to navigate. Single self-contained file; no build step.

## The thesis in one paragraph

Coding agents collapsed implementation from days to hours. CI/CD had already collapsed deploys to minutes. The *intent-capture* phase — meetings, decisions, PRDs, tickets — didn't collapse at all. DORA can't see it: DORA's clock starts at `git commit`. That gap has a name now: **Intent Lead Time**. This repo is the argument, with receipts from one repo we shipped over the last 13 months.

## Deck

- [`slides/outline.md`](./slides/outline.md) — the written narrative per slide, with the raw quotes bank at the bottom.
- [`index.html`](./index.html) — the actual slideshow, dark editorial, Stoa orange accent, real data embedded. 10 slides, keyboard navigable.

Slides at a glance:

1. Title
2. The question — four things leaders ask; we answer one today
3. The shift nobody priced in — Intent Lead Time
4. From code-centric to intent-centric (the Intent + Code + Tests stack)
5. The opinionated cut — three die, one lives
6. Stoa as receipt — 168 design docs, 177 impl docs, 5 AS-BUILT architectures
7. Live demo · the agentic release — a `dev → main` PR that writes itself
8. A metric you can use on Monday — ILT sub-components and bands
9. Journey map — AI across the PDLC
10. Take it home — three artifacts, three moves

## Data behind the charts

Every number on the deck (168 design docs, 177 implementation docs, 10,672 lines of AS-BUILT architecture, 65 ASCII system diagrams, the last five `dev → main` release PRs, theme and monthly breakdowns) was mined from [`specstoryai/stoa`](https://github.com/specstoryai/stoa) at deck-build time and inlined into `index.html`. The deck is a self-contained snapshot.

## Take-home artifacts

Three things leaders can grab from [`takeaways/`](./takeaways/):

1. [`takeaways/release-pr-automation/`](./takeaways/release-pr-automation/) — a drop-in GitHub Actions kit: `release-pr-sync.yml` + gh-aw `release-pr-body.md` + `main-from-dev-only.yml` + README. Your release notes write themselves tonight.
2. [`takeaways/intent-driven-prd-template.md`](./takeaways/intent-driven-prd-template.md) — an opinionated PRD template shaped for agent handoff. Worked example included.
3. [`takeaways/ai-pdlc-journey-map.md`](./takeaways/ai-pdlc-journey-map.md) — poster version of slide 9. Which tool, which phase, who owns what, at each step.

## Reading order

If you're here to skim: read the [slide outline](./slides/outline.md), then open [`index.html`](./index.html) to see it rendered, then grab whichever takeaway is most relevant.

If you're here to reuse: steal the [release-pr-automation kit](./takeaways/release-pr-automation/) first — it's the biggest single lift per hour of your time.

If you're here to argue with it: go straight to the [Beyond Code-Centric whitepaper](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf) and the [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time).

## Repo layout

```
ai-product-development/
├── index.html          # the deck — single self-contained file
├── slides/outline.md   # written narrative, one section per slide
├── takeaways/          # copy-me artifacts (workflow kit, PRD template, PDLC map)
└── README.md
```

## Built with

Stoa (`specstoryai/stoa`), Claude Code (`opus-4-7`), hand-rolled SVG, and a lot of opinion. No JS framework, no build step, no npm, no tracker.

## Credits & contact

Greg Ceccarelli — co-founder of [Stoa / SpecStory](https://withstoa.com). [LinkedIn](https://www.linkedin.com/in/gregceccarelli/) · [Beyond Code-Centric whitepaper](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf) · [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time).

License: talk contents are CC-BY 4.0; the release-pr-automation kit is MIT.
