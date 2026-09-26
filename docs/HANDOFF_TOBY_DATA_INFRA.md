# Handoff to Toby (Muse) — data engineering infra + platform hardening

From: the desk (Hermes) · For: Toby/Muse · Date: 2026-09-26

## Context: we don't have live data always

The desk runs on delayed/EOD data (Yahoo EOD, Cboe delayed chains, FRED, SEC EDGAR,
VIX, WTI). That's fine for an overnight research desk — but it means the platform must
be built to be **reliable, redundant, and honest** when a source is down, rate-limited,
or stale. Live data arrives only when Schwab connects. Until then, the desk must be
fully usable on delayed data.

## What's already good (verified)

- **Real sources only**: Yahoo EOD, Cboe delayed, FRED, SEC EDGAR, VIX, WTI. No fabricated
  numbers; BLOCKED is honest when a source fails.
- **Freshness checks**: `freshness_summary` reports `is_current` + a human note.
- **Cache management**: FRED cache with `HEDGE_DESK_CACHE_DIR` (off in tests — the
  fabricated-macro bug is fixed and isolated).
- **Historical reports**: dated `artifacts/am-report-*.json` are kept.
- **Market-cycle schedule**: 4:30pm close ingest + 8am pre-open report (fresh for the 9am open).

## What's needed to make the infra solid (the gaps)

1. **Data-source redundancy.** If Yahoo or Cboe is down/rate-limited, the batch should
   fall back to a secondary source (Alpha Vantage, Tiingo, Stooq) rather than BLOCKED.
   There are already Alpha Vantage references — wire a real fallback path.
2. **Structured historical store.** The dated reports exist but there's no queryable
   history. Add a lightweight store (SQLite or JSONL) of daily closes / candidates so we
   can show trends and backtest the wheel over time.
3. **Data-quality monitoring.** A freshness/staleness alert: if a source is stale or a
   series is missing, flag it loudly (not silently). The FRED "1.0" bug showed this matters.
4. **Rate-limit handling.** Retry with backoff, cache aggressively, and degrade gracefully
   when a free-tier API is throttled.
5. **Live-data path (future).** Design the ingestion so a live feed (Schwab) can drop in
   without rearchitecting — same schema, just a new transport.

## Other open-data APIs worth connecting

- **Alpha Vantage** — EOD + some intraday + fundamentals (free tier). Already referenced.
- **Tiingo** — EOD + fundamentals + news (free tier, generous).
- **Stooq** — free EOD CSV, no key needed (good fallback).
- **Finnhub** — free real-time quotes + news + economic calendar.
- **Polygon.io** — free market data + aggregates.
- **Twelve Data** — free EOD + forex/crypto.
- **Nasdaq Data Link (Quandl)** — free datasets.
- **OpenBB** — open-source financial data platform (aggregates many sources).
- **Economic calendar** (e.g., FRED release calendar, or a free calendar API) — for the
  event-driven desks (earnings, Fed, macro).
- **News API** — for catalyst/event research (Muse's lane).

## What I'd like you to take

1. **Wire a real fallback data source** (Alpha Vantage or Tiingo) for EOD closes so the
   batch survives a Yahoo outage — fail over, don't just BLOCK.
2. **Add a structured historical store** (SQLite or JSONL) of daily closes + candidates,
   and surface a trend/backtest view on the dashboard.
3. **Add a data-quality monitor** — staleness/freshness alert that flags a stale or
   missing series loudly.
4. **Rate-limit + retry hardening** on the free-tier fetches.
5. **Design the live-data seam** so Schwab can drop in later without rearchitecting.

## Ground rules (unchanged)

- **SOUL.md is the governing charter — it outranks everything.** Read it first. The desk is a
  compass, not a hand on the wheel: real data only, no fabricated numbers, no probability/RoR
  claims, no trade authorization, no secrets/PHI/PII, research ≠ income ≠ order, paper-only,
  `trade_authorized=False`. Every change must serve the GP's standing orders.
- **Build value, not output.** The measure of this work is whether the GP can act on it — a
  usable desk that turns real data into a decision-ready briefing. Don't add breadth for its
  own sake; each increment must make the desk more usable, more honest, or more reliable.
  Kill waste. Prefer the smallest useful vertical slice that the GP can actually use.
- Real data only. No fabricated numbers, no probability/RoR claims, no trade authorization.
- No secrets, PHI, or PII in commits, PRs, logs, or replies.
- Follow AGENTS.md: claim the issue, branch, PR, no critical-path collision.
- Tests must be deterministic and never write to the production cache.

## Coordination

Open a GitHub issue to claim a piece. Push to a branch, open a PR. The BOLO watch is on
origin/main — the moment you push, it's caught and integrated.
