---
name: datalink-audit
description: Use when asked about data health, API reliability, outages, or redundancy, and before adding a new data provider. Full health and redundancy audit of every external API, feed, and database the project depends on. Builds/refreshes the data registry (see `CLAUDE.md` → Data sources) and produces a prioritized resilience fix plan.
argument-hint: "[optional: one source ID or folder to limit scope]"
effort: high
---

# /datalink-audit — Data link health & redundancy audit

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Scope: **$ARGUMENTS** (empty = whole repo).
Tip: for repos with many integrations, say `use a workflow` so one agent audits each source in parallel and a final agent cross-checks findings.

## 1. Discover every data link
Search the codebase for: HTTP clients (`fetch`, `axios`, `requests`, `httpx`, `got`), SDK clients, WebSockets/SSE, DB/Redis/queue connections, cron/ETL jobs, webhooks in and out, scrapers. For each, record the provider, endpoint (no keys), auth env-var **name**, call sites, and what features depend on it.

## 2. Score each link (0–2 each, max 20)
| # | Control | 0 = missing · 1 = partial · 2 = solid |
|---|---|---|
| 1 | Explicit timeout (connect + read) |
| 2 | Retries: bounded, exponential backoff + jitter, idempotent only, respects `Retry-After` |
| 3 | Circuit breaker / failure budget |
| 4 | Response schema validation (zod / pydantic / etc.) |
| 5 | Redundancy: secondary provider or mirror |
| 6 | Cache / last-known-good with TTL + stale flag |
| 7 | Rate-limit awareness (quota tracking, throttling, 429 handling) |
| 8 | Freshness tracking (timestamp shown, staleness alert) |
| 9 | Observability: structured logs, latency/error metrics, health endpoint |
| 10 | Secrets hygiene: env-var only, never logged, least-privilege key, rotation path |

## 3. Probe live health (read-only, safe)
- Prefer the project's health command from `CLAUDE.md`. Otherwise call only documented health/status or cheap GET endpoints, a few times max, respecting rate limits.
- Pass credentials by env-var reference inside the command; never print them, never print full response bodies (status code, latency, record count, newest timestamp only).
- Check the provider's public status page if one exists.

## 4. Single points of failure
List every user-facing feature that breaks if ONE provider fails. These are the top priority.

## 5. Write results
- Create or update the data registry (see `CLAUDE.md` → Data sources) (registry columns + 🟢🟡🔴 status). Env-var names only.
- Write `docs/audits/<yyyy-mm-dd>-datalinks.md`: scorecard table, live probe results, SPOFs, and a ranked fix plan (Critical → Low), each item with effort (S/M/L) and the exact `/harden-datalink <source-id>` command to fix it.

## 6. Reply
Overall grade, the 3 biggest risks in plain English, and the first command to run.
