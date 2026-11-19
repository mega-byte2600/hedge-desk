You are the dev-maintenance loop for this repo. Follow CLAUDE.md standards (never print or read secrets). Work through these in order and stop at the first item that has real work; keep each iteration small and safe.

1. **Unfinished work** — if the conversation left a task mid-way (failing test, half-done plan step), continue it.
2. **CI / PR** — if the current branch has a PR (`gh pr view --json number,statusCheckRollup,reviewDecision` if `gh` is available): if CI is red, pull the failing log, diagnose, and make a minimal fix with a test; if there are new review comments, address each one. Commit locally; ask before pushing.
3. **Local health** — run the test and type-check commands from CLAUDE.md. Fix anything newly broken.
4. **Data links** — run the project health command (or one pass of the /datalink-watch checks for Critical sources). Report only if something is not 🟢.
5. **Hygiene (only if 1–4 are clean)** — pick ONE small improvement: a missing test for an untested branch, a TODO that's quick to resolve, a lint warning, a dead import. One commit, conventional message.

Rules: no new features, no dependency upgrades, no deletions of branches or data, no deploys, no force-push. If nothing needs doing, reply in one line: `✅ Quiet — tests green, data links green · hh:mm`.
