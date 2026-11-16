# Toby handoff — Desk coverage, SEC, Carpe DATA

Branch: `toby/desk6-all-desk-coverage`

## Changes

- Desk 5 now has a read-only, cached SEC EDGAR submissions path for approved watchlist issuers, issuer filing links, honest loading/blocked/unmapped states, and a filing-backed one-cohort depreciation sensitivity using `Decimal`.
- The scenario records the exact SEC filing URL and note, distinguishes reported useful-life from a user-entered shorter-life sensitivity, and explicitly avoids claiming an accounting error, a universal Burry formula, cumulative cohorts, replacement capex, DCF, or a short signal.
- The existing 48-hour Desk 5 task now prioritizes Burry's official Cassandra Unchained posts. Reddit is a lead channel only; claims require authentication and primary-source corroboration.
- Desk 6 Carpe DATA now includes paced GDELT conflict/shipping media leads, labeled uncorroborated, alongside the existing official weather, hazard, commodity, and positioning feeds. Its board shows live provider states and blocks futures rankings until curve, basis, roll, fees, and contract-spec inputs exist.
- The mobile Research Desk view now names and routes Desks 5–7 accurately. Removed false generic “Active” and stale “Coming soon” claims. Desk 7 identifies a dated indicator snapshot and warns after two days that it may be stale.
- Added a seven-desk coverage audit, route/copy/freshness regression checks, and included the new CSS file in the deployment asset allowlist.

## Verification performed

- Passed: `test_burry_sensitivity.py` (3), `test_short_research_board.py` (6), `test_market_context.py` (3), `test_public_signal_feeds.py` (7), `test_data_integrations.py` (103), `test_desk_coverage_copy.py` (3), `test_desk7_indicators.py` (9), `test_copy_quality.py` (1), `test_public_web_surface.py` (24), `test_web_page_guards.py` (24), and `test_iphone_preview_surface.py` (1).
- Passed: browser JavaScript syntax check (`node --check` on an `.mjs` copy), Python compile check, `git diff --check`.
- The complete legacy suite cannot be imported in this environment because `plotly` is not installed (`tests/test_dashboard_build.py`). Do not represent the whole suite as passing.
- SEC handling is implemented and unit-tested, but a live watchlist fetch and the production `/api/short-research` response have not been verified from this branch. The prior Desk 5 handoff recorded a direct EDGAR timeout from this workspace. After merge/deploy, confirm that the per-symbol statuses move from `LOADING` to `LIVE` in Render logs/board; until then, do not tell the GP that production SEC is fixed.
- No live browser visual inspection was completed in this environment. `test_iphone_preview_surface.py` checks the packaged mobile preview contract; the narrow-screen visual check remains for the independent reviewer.

## Independent review checks before merge

1. Confirm current production environment provides `MARKET_DATA_USER_AGENT` with an identifiable contact as expected by SEC access policy; check Render logs and actual SEC per-symbol status after deployment.
2. Review SEC response latency, CIK mapping, and whether all configured symbols receive filings; unsupported mappings must remain explicit.
3. Review the depreciation formula, assumptions, and UI language independently. It is a sensitivity, not Burry's private model and not accounting advice.
4. Verify GDELT pacing and fail-closed behavior under 429s; headlines must remain uncorroborated leads.
5. Inspect Desk 5/6 responsive layouts and the Desk 7 stale snapshot warning on a narrow iPhone viewport.
6. Confirm Desk 6 remains blocked from candidate ranking until all matched futures and cost inputs are supplied.

No production deployment or merge is performed from this branch.
