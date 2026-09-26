# Handoff to Toby (Muse) — Emporion desk tightening

From: the desk (Hermes) · For: Toby/Muse · Date: 2026-09-26

## Where things stand (real, verified)

- **Candidates page + Dashboard are live on real data.** The console Candidates page and the
  Dashboard both show the same 21 real EOD candidates (7 symbols: AAL, CCL, DVN, F, LYFT,
  NCLH, NKE) from the nightly batch (Yahoo EOD + Cboe chains). They match.
- **The nightly batch is the single source of truth.** `artifacts/am-report-latest.json` is
  regenerated after every close and feeds the dashboard and the candidates feed.
- **AI-slop copy removed** from the console (loading text, "synthetic fixture only",
  "reference snapshot" — all cleaned, tests updated).

## The gaps to close

1. **Scenario lab, Research desks, and Overview still show the frozen synthetic report.**
   The console's `/api/report` serves the old frozen fixture, not the real nightly data.
   Only the Candidates page is real. These tabs need to be rebuilt from
   `am-report-latest.json` so the whole console tells one real-data story.

2. **Candidates are options-premium only.** All 21 candidates are options strategies
   (CASH_SECURED_PUT, COVERED_CALL, CREDIT_SPREAD). The other desks have real data but no
   candidates yet:
   - Earnings desk: `earnings_actuals` (real SEC EDGAR) is in the nightly report.
   - Macro/rates desk: `macro_environment`, `rates_environment` (real FRED) are in the report.
   - Oil/VIX: real, already on the dashboard.

3. **Scenario lab should use real nightly outcomes** (paper outcomes, yellow sheets) instead
   of the frozen war-games.

## What I'd like you to take

- **Build the earnings-desk and macro-desk candidate feeds** from the real nightly data
  (`earnings_actuals`, `macro_environment`) so the Candidates page spans more than options.
- **Help connect the Scenario lab to the real nightly outcomes** (paper outcomes, yellow
  sheets) rather than the frozen synthetic war-games.
- **Extend the dashboard** with earnings and macro charts from the real data.

## Ground rules (unchanged)

- Real data only. No fabricated numbers, no probability/RoR claims, no trade authorization.
- No secrets, PHI, or PII in commits, PRs, logs, or replies.
- Research ≠ income ≠ order. Everything stays paper-only and `trade_authorized=False`.
- Follow AGENTS.md: claim the issue, work on a branch, open a PR, don't collide on the same
  critical path. Risk/financial-model changes need independent review.
- SOUL.md is the governing charter; it outranks everything else.

## Coordination

- Open a GitHub issue to claim a piece, or tag the existing ones. Push to a branch and open a
  PR. The desk will review and integrate.
- The BOLO watch is on origin/main — the moment you push, it's caught and integrated.
