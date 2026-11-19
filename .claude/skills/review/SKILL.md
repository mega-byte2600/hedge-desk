---
name: review
description: Use proactively before any commit is pushed or PR is opened, and whenever asked to check code. Senior-level code review of the current branch or a PR — correctness, security, secrets leaks, data-link resilience, performance, and tests — with prioritized, verified findings.
argument-hint: "[optional: PR number, branch, or path]"
effort: high
---

# /review — Ruthless, fair code review

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Scope: **$ARGUMENTS** (if empty, review the current branch vs. the default branch: `git diff $(git merge-base HEAD origin/HEAD)...HEAD`).

For large diffs (20+ files), say `use a workflow` to fan out one reviewer per file and then merge findings.

## Checklist
1. **Correctness** — logic errors, off-by-one, null/undefined paths, race conditions, timezone/date bugs, float math on money or odds (use decimals/ints).
2. **Secrets** — scan the diff and new files for keys, tokens, passwords, connection strings, private URLs with credentials, `.env` contents, or secrets in logs/tests/fixtures. Report by file:line only — never echo the secret itself. If found: severity **Critical**, recommend rotating.
3. **Security** — injection (SQL, command, XSS), authz on every endpoint, input validation, SSRF on user-supplied URLs, unsafe deserialization, CORS, dependency risks.
4. **Data-link resilience** — every external call has timeout, bounded retry w/ jitter, breaker, schema validation, fallback, and no secret in logs. Is the data registry (see `CLAUDE.md` → Data sources) updated?
5. **Performance** — N+1 queries, missing indexes, unbounded loops/pagination, large client bundles, missing caching, blocking I/O on hot paths.
6. **Tests** — do tests cover the acceptance criteria and failure paths (provider down, slow, bad data)? Any flaky patterns (real network, sleeps, time-dependence)?
7. **Maintainability** — naming, duplication, dead code, consistency with repo patterns.

## Verify before reporting
For each candidate finding, re-read the code and try to disprove it. Drop anything you can't back with a concrete failure scenario.

## Output
A table sorted by severity — **Critical / High / Medium / Nit** — with `file:line`, the problem, a concrete failure scenario, and the fix. Then a one-line verdict: **Ship**, **Ship after fixes**, or **Rework**. Offer to apply the fixes.
