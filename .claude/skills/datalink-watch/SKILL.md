---
name: datalink-watch
description: One pass of the data-link health monitor — checks every source in the data registry (see `CLAUDE.md` → Data sources) for availability, latency, freshness, rate-limit headroom, and failover state; reports only changes. Designed to run repeatedly via /loop.
argument-hint: "[optional: source IDs to watch, default all critical]"
effort: medium
---

# /datalink-watch — Health monitor (one iteration)

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Run with: `/loop 15m /datalink-watch` (or `/loop /datalink-watch` to let Claude pick the interval).
Watching: **$ARGUMENTS** (empty = every source marked Critical or High in the data registry (see `CLAUDE.md` → Data sources)).

## Each iteration
1. **Check** — use the project health command from `CLAUDE.md` if it exists; otherwise make one cheap, read-only request per source (health/status endpoint or smallest valid GET). Never exceed ~1% of a source's rate limit per hour across iterations.
2. **Measure** — status code, latency, newest data timestamp (→ data age vs. freshness SLA), remaining quota from rate-limit headers, breaker state / served-from if the app exposes it.
3. **Classify** — 🟢 / 🟡 / 🔴 per the legend in the data registry (see `CLAUDE.md` → Data sources).
4. **Compare** with the previous iteration (keep a running note in `.claude/state/datalink-watch.json`, gitignored; create the folder if needed).

## Report — keep it short
- Nothing changed and all 🟢 → a single line: `🟢 All N sources healthy · hh:mm`.
- Something changed → a compact table of only the changed sources (was → now, latency, data age, quota left) plus a one-line likely cause.

## Act — safely
- 🔴 on a Critical source: check the provider's status page, confirm the fallback is serving (secondary or cache with stale flag). Append a row to "Incidents / notes" in the data registry (see `CLAUDE.md` → Data sources). Do not change production config, rotate keys, or deploy — recommend the action and wait for approval.
- Recurring 🟡 (3+ iterations) → suggest `/harden-datalink <source-id>`.
- Quota above 80% → warn with projected exhaustion time.

## Rules
Read-only against providers. Never print secrets, auth headers, or full response bodies. Pass keys only via env-var references inside commands.
If every source has been 🟢 for 12 straight iterations and you are self-pacing, lengthen the interval toward the 1-hour max.
