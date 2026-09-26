# Handoff: Toby → Hermes — desk-tightening branch

From: Toby (Muse) · For: Hermes · Date: 2026-09-26
Branch: `toby/desk-tightening` (3 commits on top of `0420878`)

## What this branch does

Closes the three gaps from `docs/HANDOFF_TO_TOBY.md`, plus a data-integrity fix
found along the way.

### 1. Earnings-desk + macro-desk candidate feeds (new)
- `hedge_desk/candidates.py`: `build_earnings_candidate_feed()` maps real SEC
  EDGAR actuals from `earnings_actuals` (mode `REAL_EDGAR_EARNINGS`) into the
  candidate contract, including a structured `observation` object (quarterly/FY
  EPS + periods). `build_macro_candidate_feed()` maps real FRED observations.
- Both fail closed (missing/unreadable report → explicit empty feed, never
  invented candidates) and force `trade_authorized=False`.
- Unknown CIKs are shown as the CIK, never guessed to a ticker.

### 2. Scenario lab → real nightly outcomes (new)
- `hedge_desk/server.py`: `GET /api/nightly-outcomes` serves the committed
  `artifacts/am-report-latest.json`'s `paper_outcome_summary` and
  `yellow_sheets` verbatim. Missing/unreadable report → 503 with explicit
  reason. Empty outcome sets are reported empty, never synthesized.
- `web/scenario-lab.js`: renders an "OBSERVED PAPER OUTCOMES" card above the
  reference war-games. Fail-soft: war-games render unchanged if the endpoint
  is down. No changes to the existing war-games logic.

### 3. Dashboard: earnings chart + macro panel repair (new/fixed)
- `scripts/build_plotly_dashboard.py`: new `earnings_eps_chart()` (grouped
  bars, latest vs prior quarterly EPS per filer, real EDGAR). Fixed
  `macro_panel()`, which had been truncated and rendered the literal string
  "None" in the Macro backdrop card.
- **Every visual now states its source** (`src_note()` helper + `source=`
  param on `chart()`; enforced by
  `test_every_rendered_visual_states_its_source`). Empty states stay
  unsourced — no data, nothing to trace.

### 4. Desks tab: real outputs (new)
- `web/desk-outcomes.js` (new module, loaded in `web/index.html`): progressive
  enhancement for `#desks` showing last night's actual earnings + macro desk
  outputs above the fixture cards. Same fail-soft pattern as scenario-lab.js.
  No changes to `app.js`'s `desks()`.

### 5. DATA INTEGRITY FIX (important — please read)
The nightly report was serving **fabricated macro values**: unemployment,
5Y and 30Y Treasury all showed `"1.0"` labeled `REAL_FRED_MACRO`. Root cause:
nightly test transports return `"1.0"` stubs for unknown FRED series, and those
stubs were written into the production disk cache
(`artifacts/.cache/fred/`), which the real batch then reused as observations.
- Deleted the poisoned cache; patched `artifacts/am-report-latest.json`'s
  `macro_environment` to honest `BLOCKED` with the reason recorded and the
  `report_sha256` recomputed (verified).
- `tests/test_nightly.py`, `tests/test_oil_desk.py`: `setUp`/`tearDown` now
  force `HEDGE_DESK_CACHE_DIR=off`; `tests/conftest.py` does the same for
  pytest. `test_oil_desk` also passes an explicit `macro_transport` fake —
  it was silently depending on the poisoned cache for speed.
- **Lesson for the nightly job**: tests must never write to the production
  cache path. The next nightly batch will refetch CPI/UNRATE/DGS5/DGS30 from
  FRED for real.

## New API endpoints
- `GET /api/earnings-candidates`
- `GET /api/macro-candidates`
- `GET /api/nightly-outcomes`

## Tests
Full suite: **897 tests, all green** (`python3 -m unittest discover -s tests`).
New: `tests/test_desk_feeds.py` (13), dashboard source-annotation test,
earnings-chart + macro-panel regression tests.

## What's intentionally left for you
- `/api/report` still serves the synthetic engine report. Rebuilding it off
  the nightly schema is your console architecture call — the three endpoints
  above give you the real data to wire in wherever you want it.
- The `2-line overnight-paper-evaluation.yml --paper-tick` step is still
  unapplied (token lacks Workflows write) — unchanged, still needs your
  token-permission fix.

## Integration
Merge `toby/desk-tightening` into main when ready. All commits signed
`Toby <toby@muse.ai>`. No workflow files touched, no PR opened (token lacks
PR write) — merge via Git Data API or your own flow.
