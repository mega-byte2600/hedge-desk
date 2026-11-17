# Toby handoff — Tuesday testing: fix 3 failing tests

Branch: `toby/tuesday-testing-2026-11-17`

## Changes

- `hedge_desk/options_seed_refresh.py`: `refresh()` now accepts an optional
  `now` parameter (default: wall clock via `_now()`), threaded through to
  `_mark_failed`. Production behavior is unchanged — the weekly workflow
  calls `refresh()` with no arguments.
- `tests/test_options_seed.py`: the two refresh tests pin `now=AS_OF`
  (2026-09-30), matching the fixed clock the `select_seed_put` tests
  already use.
- `web/app.js`: restored the "Broker data status" panel at the end of the
  Desk 5 view, with the locked Schwab market-data-only disclosure verbatim:
  "No Schwab account, positions, balances, order history, locate request,
  or order endpoint is accessed here."

## Why

- The options-seed fixture expirations (Oct 12 / Oct 29 / Nov 10, 2026)
  are all in the past relative to the wall clock on Nov 17, so the
  refresh tests failed closed with "cboe chain has no put expiration
  within 30 days". That is the refresh logic working correctly; the
  defect was the tests using a wall clock against fixed-date fixtures —
  a determinism gap (AGENTS.md: tests must use fixed clocks). The
  injectable `now` closes it without touching production behavior.
- The Nov 16 Desk 5 polish (49db3ba, then 8fd1833) dropped the Schwab
  market-data-only disclosure from the Desk 5 view. The lock test
  `test_schwab_surface_is_market_data_only_and_exposes_no_account_data`
  caught it. The sentence is restored verbatim, not reworded
  (ENGINEERING_LESSONS rule 1: locked copy).

## Verification performed

- Full suite before fixes: 1296 passed, 3 failed.
- Full suite after fixes: **1299 passed, 0 failed** (1299 dots, no F/E).
- Named Tuesday areas re-run explicitly, all passing (173 tests):
  `test_data_integrations`, `test_graham_candidate_surface`,
  `test_real_estate_lazy_route`, `test_options_workbench`,
  `test_options_seed`, `test_cboe_chain`, `test_quantdesk_ml_options`,
  `test_eod_stooq_fallback`, `test_fred_api_fallback`,
  `test_data_providers`.
- Browser JavaScript syntax check passed (`node --check` on a `.mjs`
  copy of `web/app.js`, per ENGINEERING_LESSONS rule 2).
- Coverage check: every module shipped Nov 10–16 (Desk 5/6 evidence
  paths, SEC/FINRA services, Burry sensitivity, institutional feeds)
  has a corresponding test file and passes. No untested shipped code
  found. The stale `test_yahoo_failover` pycache is a leftover from a
  deleted file; Yahoo failover is covered by `test_schwab_core_data`
  (4 tests patching `_fetch_yahoo`) and `test_eod_stooq_fallback`.

## Independent review checks before merge

1. Confirm the restored "Broker data status" panel renders on the Desk 5
   view at phone width.
2. Confirm the weekly options-seed workflow (`.github/workflows/
   options-seed.yml`) still calls `refresh()` with no arguments, so the
   `now` parameter is test-only.
3. Note: GitHub Actions is blacked out until 2026-12-01 per the GP's
   directive; CI status on this branch was verified locally only.

No production deployment or merge is performed from this branch.
