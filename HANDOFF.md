# HANDOFF — Close the RoR-substitution escape in scripts/ (toby/ror-boundary-scripts-2026-11-27)

Base: origin/main `1510b12e` (Ticker feed refresh — 2026-11-27 10:24 ET).
Branch is 1 ahead / 0 behind main. No PR opened from this environment
(Toby's token cannot open PRs); push lane = user's other model, Sol owns
PR → review → merge.

Risk-control change: per repo AGENTS.md, an agent may implement and test a
risk-control change but may NOT approve its own risk-control change for
release. This branch needs independent authorized review before merge.
No Risk of Ruin was calculated, estimated, inferred, modified, or
substituted by this run: the fix REMOVES the only RoR calculation outside
the conventional boundary.

## The gap (Thursday risk audit, 2026-11-26, GAP 1)

`tests/test_architecture_boundaries.py` scanned only `hedge_desk/` for
`estimate_risk_of_ruin` calls. `scripts/real_nke_paper_trade.py:103` and
`scripts/real_ccl_paper_trade.py:96` called it, wrapped the result in
`build_validated_risk_inputs` (model "0.1.0-unvalidated", validator
"classic-vv-fixture-validator"), and approved a paper-trade plan from it —
the forbidden pattern end to end, untested because `scripts/` was outside
the scan. Both scripts' docstrings claimed "RoR from the deterministic
engine". Not on any schedule (demo scripts only), but the escape was real:
any future script could do the same and the boundary test would stay green.

## What changed

- `hedge_desk/demo.py` — new `build_demo_risk_inputs(...)` helper: the
  single demo-only construction path for validated risk inputs. It does
  NOT estimate RoR; both RoR slots carry an explicit `Decimal("0")`
  placeholder standing in for a separately validated engine output, with
  the unvalidated model/validator labels. `build_reference_plan` now uses
  it (identical args, no behavior change to the frozen fixture).
- `scripts/real_nke_paper_trade.py`, `scripts/real_ccl_paper_trade.py` —
  removed the `estimate_risk_of_ruin` import + call and the direct
  `build_validated_risk_inputs` construction; both now use
  `build_demo_risk_inputs`. Docstrings corrected ("RoR from the
  deterministic engine" removed); the printed RoR line now reads
  "demo placeholder 0 (not computed)".
- `tests/test_architecture_boundaries.py` — `python_sources()` now scans
  `hedge_desk/` AND `scripts/`; new `test_boundary_scan_covers_scripts`
  pins that coverage (both real_* scripts in the scanned set) so the scan
  cannot silently narrow again.

## Behavior change to state plainly

The scripts' decisions no longer depend on a computed RoR. With the
placeholder 0, `risk_gate`'s `RISK_OF_RUIN_LIMIT` check passes and the
decision reflects only the other gates (quote age, liquidity, loss
limit) — the same posture as the frozen reference demo. The scripts
demonstrate the paper lifecycle with real Cboe quotes; their decisions
are mechanics demos, not risk approvals. No production path changes:
no scheduled job runs these scripts.

## What was verified (2026-11-27, after rebase onto 1510b12e)

- Full suite: `pytest tests/` — **1,416 tests, 0 failures, 0 errors,
  0 skipped** (exit 0; 1,365 collected + 51 subtests, confirmed via
  `--junitxml`). Focused risk suites (`test_architecture_boundaries`,
  `test_risk_and_decision`, `test_ror_vv_vectors`, `test_execution_gate`,
  paper workflow/settler/runner, `test_account_gate`,
  `test_compliance_traceability`) — **102 passed**.
- Negative control: with the old scripts temporarily restored, the two
  extended boundary tests FAIL (RoR calculation confined +
  validated-inputs construction); with the fix, all 6 boundary tests
  pass. The guard is real, not vacuous.
- `node --test web/*.test.mjs` — **60 passed, 0 failed**.
- `python3 -m py_compile` on both scripts + `demo.py` + the test file —
  OK. `grep estimate_risk_of_ruin scripts/` — zero hits.
- Not run end-to-end: the scripts fetch live Cboe data at import and
  their contracts expired Oct 23, 2026, so a live run is not meaningful
  in this environment; verification is static (boundary tests + compile)
  plus the full suite.

## Deliberately NOT changed

- `hedge_desk/risk/ruin.py` (the estimator) and `hedge_desk/risk/inputs.py`
  untouched — the conventional boundary itself is unchanged, only its
  enforcement scope widened.
- `rates_desk.py` Sentry W48 F1–F9: still open, not this branch (separate
  fix, separate review).
- No Risk of Ruin value touched anywhere. No schedule changes.

## Reviewer must check before merge

- Confirm the demo-only RoR posture is acceptable: scripts pass an
  explicit 0 placeholder, labeled unvalidated, and print it as such.
- Confirm no other script in `scripts/` constructs validated risk inputs
  outside `demo.py` (the extended test now enforces this).
- Independent authorized approval required (risk-control change).

---
## Carried forward from main (2026-11-20)

From PR #178 on, the nightly writes `artifacts/premium-ledger.jsonl`, the
append-only paper track record of the premium score. It is **not** ignored by
git. `scripts/run_nightly_batch.sh` stages it after each run.

**Batch committers (Toby lane):** add it to every "Batch refresh" commit
alongside `am-demo.html`, `am-report-latest.json` and the dated report:

    git add artifacts/premium-ledger.jsonl

Safety net: each dated `am-report-YYYY-MM-DD.json` also carries that night's
appended ledger rows (`premium_ledger.appended_rows`), so
`hedge_desk.premium_ledger.rebuild_from_reports` can rebuild the full ledger
from committed reports if the `.jsonl` is ever lost.
