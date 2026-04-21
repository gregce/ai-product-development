<div align="center">

# How product development works in an AI world

<p>
  <a href="https://gregce.github.io/ai-product-development/">
    <img alt="Open the live deck" src="https://img.shields.io/badge/%E2%96%B6%20OPEN%20THE%20DECK-e35a2c?style=for-the-badge&labelColor=0b0f14" />
  </a>
</p>

<p><strong><a href="https://gregce.github.io/ai-product-development/">gregce.github.io/ai-product-development</a></strong></p>

<p><em>A talk for Alpine SG portfolio-company product leaders · April 2026</em></p>

</div>

---

A 13-slide deck (10 + 3 appendix), four analysis scripts, and three copy-me takeaway artifacts.

## The thesis in one paragraph

Coding agents collapsed implementation from days to hours. CI/CD had already collapsed deploys to minutes. The *intent-capture* phase (meetings, decisions, PRDs, tickets) didn't collapse at all. DORA can't see it: DORA's clock starts at `git commit`. That gap has a name now: **Intent Lead Time**. This repo is the argument, with receipts from one repo we shipped over the last 7 months.

## Deck

- [`index.html`](./index.html): the actual slideshow, dark editorial, Stoa orange accent, real data embedded. 13 slides, keyboard navigable.
- [`slides/outline.md`](./slides/outline.md): the written narrative per slide, with the raw quotes bank at the bottom.

Slides at a glance:

1. Title
2. The question: four things leaders ask; I'm focusing in on one today
3. Journey map: where AI fits across the PDLC (and where it doesn't)
4. The bottleneck that didn't collapse: Intent Lead Time
5. A metric you can use on Monday: ILT sub-components and bands
6. The stack: from code-centric to intent-centric
7. The opinionated cut: three practices die, one lives
8. Stoa as receipt: 168 design docs, 177 impl docs, 5 AS-BUILT architectures
9. Live demo · the agentic release: a `dev → main` PR that writes itself
10. Take it home: three artifacts, three moves
11. **Appendix A**: a minority report on AGENTS.md, CLAUDE.md, and agent skills
12. **Appendix B**: what an AS-BUILT-ARCHITECTURE.md looks like (structural exemplar from `stoa-cli`)
13. **Appendix C**: harness & workflow (two harnesses, many terminals, saved sessions)

## Data behind the charts

Every number on the deck (168 design docs, 177 implementation docs, 10,672 lines of AS-BUILT architecture, 65 ASCII system diagrams, the last five `dev → main` release PRs, theme and monthly breakdowns) was mined from [`specstoryai/stoa`](https://github.com/specstoryai/stoa) at deck-build time and inlined into `index.html`. The deck is a self-contained snapshot.

## Take-home artifacts

Three things leaders can grab from [`takeaways/`](./takeaways/):

1. [`takeaways/release-pr-automation/`](./takeaways/release-pr-automation/): a drop-in GitHub Actions kit: `release-pr-sync.yml` + gh-aw `release-pr-body.md` + `main-from-dev-only.yml` + README. Your release notes write themselves tonight.
2. [`takeaways/intent-driven-prd-template.md`](./takeaways/intent-driven-prd-template.md): an opinionated PRD template shaped for agent handoff. Worked example included.
3. [`takeaways/ai-pdlc-journey-map.md`](./takeaways/ai-pdlc-journey-map.md): poster version of slide 3. Which tool, which phase, who owns what, at each step.

## Reading order

If you're here to skim: read the [slide outline](./slides/outline.md), then open [`index.html`](./index.html) to see it rendered, then grab whichever takeaway is most relevant.

If you're here to reuse: steal the [release-pr-automation kit](./takeaways/release-pr-automation/) first. It's the biggest single lift per hour of your time.

If you're here to argue with it: go straight to the [Beyond Code-Centric whitepaper](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf) and the [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time).

## Repo layout

```
ai-product-development/
├── index.html          # the deck, single self-contained file
├── slides/outline.md   # written narrative, one section per slide
├── takeaways/          # copy-me artifacts (workflow kit, PRD template, PDLC map)
└── README.md
```

## Built with

Stoa (`specstoryai/stoa`), Claude Code (`opus-4-7`), hand-rolled SVG, and a lot of opinion. No JS framework, no build step, no npm, no tracker.

## Credits & contact

Greg Ceccarelli, co-founder & CPO at [Stoa / SpecStory](https://withstoa.com). [LinkedIn](https://www.linkedin.com/in/gregceccarelli/) · [X](https://x.com/gregce10) · [Beyond Code-Centric whitepaper](https://specstory.com/whitepapers/beyond-code-centric-specstory-2025.pdf) · [Intent Lead Time guide](https://withstoa.com/guides/intent-lead-time).

License: talk contents are CC-BY 4.0; the release-pr-automation kit is MIT.
