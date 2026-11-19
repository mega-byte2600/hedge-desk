# Scoring rubric — what a 9 means for the desk

Independent reviews drifted ±1 between rounds with no code change. Each
dimension now has explicit criteria. `python scripts/scorecard.py` checks the
**VERIFIED** items (measured by a command) in seconds, and `--full` adds the
whole test suite. A reviewer judges the **VALIDATED** items against the
GP's stated expectations. A 9 requires every item to hold.

## Code quality
- VERIFIED: the ruff gating set (E9, F, B, FA102) is clean across
  `hedge_desk`, `tests` and `scripts`.
- VERIFIED: CI runs pytest (so pytest-style tests are actually collected),
  ruff, and the 3.9/3.11/3.13 matrix with the coverage gate.
- VERIFIED: the full suite passes. Tests are deterministic, with fixed
  clocks and no calendar literals.
- VALIDATED: new logic lives in small pure modules (`premium_score`,
  `desk_call`) with reference tests.

## API & data health
- VERIFIED: Cboe and EOD fetches go through `feed_base.with_retries`
  (jittered backoff on 0/429/5xx only).
- VERIFIED: `/api/report` degrades to the last real report, labelled STALE
  with its age, and never serves synthetic data. With no last-good report it
  still returns 503.
- VERIFIED: `/api/options-seed` reports freshness against the weekly SLA.
- VERIFIED: vendor float noise is quantized at ingest.

## UI/UX
- VERIFIED: am-demo loads Plotly from the vendored copy first and renders
  offline.
- VERIFIED: the Desk call header sits above the source-health strip.
- VERIFIED: the premium-selling trader panel shows the ranked candidates,
  each component's contribution and the management plan.
- VALIDATED: a trader can read the decision and the top candidates without
  scrolling past boilerplate.

## Insight
- VERIFIED: premium score with four sourced components (variance risk
  premium, time value, 30–45 DTE window, 16–30 delta).
- VALIDATED: matches the GP's wheel (30–45 DTE; return on collateral, not a
  misleading return on risk).

## Rigor
- VERIFIED: win probability is exact BSM N(d2) with r and q (model 2.0.0),
  with Hull reference cases 15.6 and 17.1 and put-call parity.
- VERIFIED: the premium-score delta uses the same r and q.
- VERIFIED: missing inputs earn no score (`RV_UNAVAILABLE` gives vol edge 0).
- VALIDATED: the weights are a disclosed design choice until there is
  enough paper-outcome history to backtest them.

## Actionability
- VERIFIED: the Desk call gives an action (NO_TRADE unless gate APPROVED),
  a shortlist, an invalidation level, exits and the premium score.
- VERIFIED: every candidate carries its 21-DTE time exit and its 50%-of-credit
  take-profit.
