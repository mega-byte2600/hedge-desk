# Emporion True-MVP Re-scope (GP order, 2026-09)

Status: governing. Drives the next build increment. Supersedes the "six paper
desks" framing for what we ship first.

## The product (in the GP's words, corrected)

Making money selling premiums is a simple, formulaic way to make money roughly
every 30 days with options basics — it cannot be overlooked. The Overnight
Premium Desk is the centerpiece. The equities EOD screen is NOT the product: it
is the universe feeder that picks the underlyings at batch end-of-day. Then the
premium desk runs overnight and hands the GP a risk-vetted candidate list by the
open.

Equities = screen. Premiums = the money-maker.

## Core architecture: batch, not live

- We do NOT ingest all data live/real-time. It is not possible or needed.
- EOD batch in: a real end-of-day equities feed (verified reachable from the
  dev box: stooq.com 200, query1.finance.yahoo.com 200) for a watchlist universe.
- Overnight run: the existing deterministic overnight pipeline evaluates the
  premium desk on that universe.
- AM out: ranked, risk-vetted candidates for defined-risk premium sells
  (cash-secured put / covered call / vertical credit spread).
- Schwab: risk-gated AUTO execution (GP's explicit choice). The deterministic
  risk gate plus aggregate max-loss / drawdown veto plus a kill switch stay
  authoritative. His order overrides AGENTS.md's paper-only default; the risk
  gate does NOT get skipped.

## What the repo already ships (verified)

- `hedge_desk/options/requirements.py` — versioned collateral/margin for
  CASH_SECURED_PUT, COVERED_CALL, CREDIT_SPREAD; defined risk, Decimal money.
- `hedge_desk/options/cadence.py` — monthly new-entry cadence gate, min 21 days.
- `hedge_desk/options/scanner.py` — deterministic enumeration of every admissible
  vertical credit spread from a validated snapshot (no probability, no RoR).
- `hedge_desk/options/universe.py` — cross-underlying ranking by executable
  credit-to-max-loss.
- Batch spine: `hedge_desk/overnight.py`, `scheduler.py` (idempotent,
  fail-closed), `data/batch.py` manifest, `data/intake.py` BYO-data envelope.
- Schwab: `brokers/schwab_oauth.py`, `brokers/schwab_readonly.py` (READ-ONLY),
  `broker_link.py` store.
- 653 unit tests pass (measured 2026-09-19).

## The gaps that define the build

1. The overnight engine runs on synthetic fixtures; no REAL EOD batch intake is
   wired. This is the first, biggest gap.
2. The Schwab adapter is strictly read-only; a test asserts no order-placement
   code path exists. Building risk-gated auto execution means introducing that
   path behind the risk gate + kill switch (per the GP's order and the existing
   RISK mandate).
3. The equities EOD screen (universe selection) has no real feed — it is seeded
   with static candidates today.

## Verified status of this record

- VERIFIED: 653/653 unit tests green (`python3 -m unittest discover -s tests`).
- VERIFIED: overnight -> morning pipeline, premium requirements, cadence,
  scanner all exist and are imported by the tested pipeline.
- VERIFIED: stooq + Yahoo query1 EOD endpoints return HTTP 200 from this host.
- VALIDATED: matches the GP's stated expectations for the product shape
  (premium selling centerpiece; EOD batch -> overnight -> AM candidates;
  risk-gated Schwab auto execution).
- NOT YET: real EOD intake, Schwab execution path, real universe screen.

## Build order (incremental, each proven before the next)

1. Real EOD equities intake adapter -> validated DataArtifact + batch manifest,
   proven with a live batch + unit test.
2. Universe screen on real EOD data -> premium-desk table of underlyings.
3. Nightly orchestrator run -> AM candidate list rendered for web + iOS.
4. Schwab execution adapter (risk-gated auto) behind the risk engine + kill
   switch, with `LIVE_RELEASE` still conditioned on the existing release gate.