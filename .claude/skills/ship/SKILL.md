---
name: ship
description: Use before merging to main, releasing, or deploying. Pre-release gate — verifies tests, types, lint, build, secrets, migrations, env-var names, data-link health, and writes release notes plus a rollback plan. Never deploys without explicit approval.
argument-hint: "[optional: version or release name]"
effort: high
---

# /ship — Release readiness gate

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Release: **$ARGUMENTS**

Run every check. Show a ✅ / ❌ / ⚠️ table at the end. **Any ❌ = do not ship.**

1. **Clean tree** — `git status` clean; branch up to date with remote; no stray debug code (`console.log`, `print(`, `debugger`, `.only(`).
2. **Quality** — run test, type-check, lint, and build commands from `CLAUDE.md`. Show summaries.
3. **Secrets** — scan the release diff and full working tree for committed secrets (use `gitleaks detect --no-banner --redact` if installed, otherwise grep for key patterns). Output file:line only, with values redacted. Confirm `.env*` is in `.gitignore`.
4. **Config** — list every env-var *name* the code reads; compare against `.env.example` (names only). Flag any missing from the example or from deploy config docs. Never print values.
5. **Database** — pending migrations? Are they backwards-compatible with the currently running version (expand → migrate → contract)? Is there a down migration or restore plan?
6. **Data links** — run the health command (or `/datalink-watch` logic once). Any 🔴 critical source = ❌. Any 🟡 = ⚠️ with note.
7. **Dependencies** — `npm audit --omit=dev` / `pip-audit` (or equivalent); flag High/Critical.
8. **Release notes** — write `CHANGELOG.md` entry from commits since last tag: Features, Fixes, Performance, Breaking changes.
9. **Rollback plan** — exact steps to revert (previous tag/deploy, migration rollback, feature flags to turn off) and the signals that should trigger it (error rate, data staleness, latency).

## Finish
Show the gate table and verdict. If all green, ask: "Ready to tag and deploy?" — only run tag/push/deploy commands after the user says yes.
