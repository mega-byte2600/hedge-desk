# HANDOFF — Restore Desk 5 Schwab disclosure (toby/schwab-disclosure-2026-11-27)

Base: origin/main `1510b12e` (Ticker feed refresh — 2026-11-27 10:24 ET).
Branch is 1 ahead / 0 behind main. No PR opened from this environment
(Toby's token cannot open PRs); push lane = user's other model, Sol owns
PR → review → merge.

Supersedes: `toby/tuesday-testing-2026-11-17` (local `b518fe7`, remote
`66e4cbd`, "test: fix 3 failing tests — options-seed clock, Schwab
disclosure"). That branch is dead — do not merge it:
- Its options-seed `now=` fix is already on main via PR #171 (`7edd53e`,
  "Independent review rounds 1-3"); the branch's version of the fix is
  byte-equivalent in substance.
- Its `HANDOFF.md` / `PR_BODY.md` are branch-local docs, not shippable.
- Its generated artifacts (`artifacts/am-report-*.json`, `am-demo.html`,
  `web/market-ticker.json`) are stale Nov 17 snapshots; the local-vs-remote
  divergence Monday flagged is artifacts-only (verified: zero diff under
  `tests/`, `hedge_desk/`, `scripts/`).
- The one live item was the `web/app.js` Schwab disclosure panel, which
  this branch carries forward alone, rebased onto current main.

## What changed

- `web/app.js` (1 line, `hydrateDesk5`) — restores the "Broker data
  status" panel at the end of the Desk 5 view, with the locked Schwab
  market-data-only disclosure verbatim: "Schwab / thinkorswim is not
  connected to this research view." / "No Schwab account, positions,
  balances, order history, locate request, or order endpoint is accessed
  here." Desk 5 shows borrow / short-interest data, so the view must say
  plainly that no broker account, locate, or order endpoint is accessed.
  The panel was dropped when PR #169 squash-merged the Desk 5/6 work;
  the Tuesday-testing branch restored it but was never PR'd, so main has
  shipped without it since Nov 17.
- `tests/test_copy_quality.py` (new `SchwabDisclosureTests`) — pins the
  three locked disclosure fragments in `web/app.js` so the panel cannot
  silently disappear in a future squash merge again. Negative control
  verified: the test FAILS on main's `app.js` (panel absent) and PASSES
  with the panel.

## What was verified (2026-11-27, after rebase onto 1510b12e)

- Full suite: `pytest tests/` — **1,416 tests, 0 failures, 0 errors,
  0 skipped** (exit 0; 1,365 collected + 51 subtests, confirmed via
  `--junitxml`; pytest's `-q` summary line is not printed in this
  environment). `node --test web/*.test.mjs` — **60 passed, 0 failed**.
- `python3 scripts/lint_copy.py` — copy-quality gate passed.
- `node --check web/app.js` — OK.
- Patch provenance: the `app.js` hunk is the exact diff from
  `toby/tuesday-testing-2026-11-17` (`66e4cbd` vs its parent `4ea17db`),
  applied cleanly onto current main with no manual edits — the disclosure
  wording is unchanged from the version Tuesday testing reviewed.
- No browser render verification: no live `/api/report` backend exists
  in this environment. Copy verified at source level plus the regression
  test; visible on next deploy.

## Deliberately NOT changed

- No options-seed changes: the `now=` fix is already on main (PR #171).
- No `HANDOFF.md` / `PR_BODY.md` carried over from tuesday-testing:
  those describe a test fix that already landed.
- No generated artifacts touched.

## Reviewer must check before merge

- The "Broker data status" panel renders at the end of the Desk 5 view
  on the deployed page.
- Confirm no other branch in flight re-introduces a Desk 5 view without
  the disclosure.

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
