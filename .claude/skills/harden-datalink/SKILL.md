---
name: harden-datalink
description: Use whenever code that calls an external API or feed is added or changed, or a source is flaky. Makes one external data source production-grade — resilient client wrapper, failover to a secondary provider, last-known-good cache, schema validation, health check, and failure-injection tests.
argument-hint: "[source ID from the data registry (see `CLAUDE.md` → Data sources), or provider name]"
effort: high
---

# /harden-datalink — Best-in-class resilience for one data link

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Target: **$ARGUMENTS**

## 0. Context
Read `CLAUDE.md`, the target's row in the data registry (see `CLAUDE.md` → Data sources), and the latest `docs/audits/*-datalinks.md` if present. Find every call site.
If no secondary provider exists and choosing one is a business decision (cost, licensing, data parity), propose 2–3 options with trade-offs and ask before integrating one. Never sign up for services or create keys yourself.

## 1. One gateway per source
Route ALL calls through a single client module (e.g. `src/lib/datasources/<source>.ts` or `app/datasources/<source>.py`) exposing typed functions. Call sites never hit the raw API.

## 2. Resilience layers (in this order)
1. **Timeouts** — connect + total, sized to the latency budget.
2. **Retries** — max 3, exponential backoff with full jitter, only on idempotent requests and retryable errors (network, 5xx, 429 honoring `Retry-After`).
3. **Circuit breaker** — open after N consecutive failures / error-rate threshold; half-open probe; expose state.
4. **Validation** — parse every response against a schema; treat schema failure as a provider failure (don't pass bad data downstream).
5. **Failover chain** — primary → secondary provider (normalized to the same internal type) → last-known-good cache → explicit degraded state the UI can show ("Data delayed, last updated hh:mm").
6. **Rate limiting** — client-side throttle + quota counter; warn at 80%.
7. **Caching** — TTL matched to the freshness SLA; request coalescing so concurrent callers share one in-flight request.
8. **Observability** — structured log per call: source, endpoint name, status, latency, attempt, breaker state, served-from (primary/secondary/cache). NO keys, NO full payloads, NO user PII.
9. **Health check** — a cheap `health()` function/endpoint returning status, latency, breaker state, data age.

## 3. Tests (required)
Mock the provider and prove: success path · timeout → retry → success · persistent 5xx → breaker opens → failover · secondary down → cache served with stale flag · schema-invalid response rejected · 429 with `Retry-After` respected · no secret appears in any log line.

## 4. Finish
- Run tests + type-check; show results.
- Update the source's row in the data registry (see `CLAUDE.md` → Data sources) (fallback chain, timeouts, health check, status).
- Commit as `feat(datasource): harden <source>`.
- Reply with before/after scorecard (from the audit rubric) and remaining risks.
