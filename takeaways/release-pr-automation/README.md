# Agentic release-PR automation

A drop-in GitHub Actions kit that turns your `dev -> main` release PR into a
standing, self-writing artifact. Copy the three workflow files into your repo's
`.github/workflows/` directory and wire the one-time setup below.

## What's in the kit

- **`release-pr-sync.yml`**: on every push to `dev`, finds or creates the
  standing "Release dev to main" PR. One PR per release cycle, not one per
  push. Delegates the body rewrite to the agentic workflow.
- **`release-pr-body.md`**: a [gh-aw](https://github.github.com/gh-aw/) prompt.
  The agent reads the accumulated diff plus any referenced spec / design /
  implementation markdown and rewrites the PR body with Highlights, Major
  Change Areas, Operational Notes, and Commits.
- **`main-from-dev-only.yml`**: rejects any PR into `main` whose head isn't
  `dev`. The agent's summary isn't nice-to-have; it's canonical.

## One-time setup

1. **Compile the agentic workflow.** After each edit to `release-pr-body.md`,
   run `gh aw compile release-pr-body.md`. That produces
   `release-pr-body.lock.yml` next to it. Commit both. Humans own the prompt,
   tooling owns the YAML.
2. **(Optional) Slack fanout.** Uncomment the `notify-slack` job in
   `release-pr-sync.yml` and add a `SLACK_WEBHOOK_URL` repo secret.
3. **Branch protection.** In GitHub repo settings, protect `main` and require
   the `main-from-dev-only` check to pass. Without this, the guardrail only
   flags violations rather than blocking them.

## What to expect on your next push to `dev`

The standing PR appears within seconds. Its body is blank ("Generating release
summary...") for ~30 seconds, then the agent rewrites it. If you enabled Slack,
a formatted preview posts to your channel. Merge the PR and the cycle resets.

## References

- Live production version: [specstoryai/stoa `.github/workflows/`](https://github.com/specstoryai/stoa/tree/main/.github/workflows)
- The talk this kit is from: [How product development works in an AI world](../../index.html)
