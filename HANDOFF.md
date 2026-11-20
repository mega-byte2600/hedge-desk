# HANDOFF — Saturday polish 2026-10-31, rebased 2026-11-20 (toby/sat-polish-2026-10-31)

Base: origin/main `be1a24c` (Ticker feed refresh — 2026-11-20 10:54 ET),
rebased 2026-11-20 from `528a499`. Branch is now 3 ahead / 0 behind main.
Rebase replayed all 3 commits; one conflict in `web/app.js`, resolved by
keeping main's new Desk 5/6/7 `desks()` implementation (landed as `4dbde8a`,
the Desk 5/6 + `market_context.py` content from PR #169's branches) and
keeping this branch's "afternoon research run" fallback copy. `HANDOFF.md` /
`PR_BODY.md` add/add conflicts resolved by keeping this branch's versions
(main carries the Desk 5/6 handoff in the same single-slot files; the
reviewer reads this file for this branch). No PR opened from this
environment (no push path here); push lane = user's other model.
Supersedes: `toby/sat-polish-2026-10-24` (commit `366246a`, same fix, built on
a local-only base and never pushed/merged — main still carried the stale copy).

## What changed (no new features)

### 1. Daily brief copy (2026-10-31, carried through both rebases)

- `web/app.js` — Daily brief subtitle: "research input from the six desks.
  Replaced every morning." → "from the seven desks. Replaced every
  afternoon." Fallback copy: "after the morning research run" → "after the
  afternoon research run." Reason: the daily pipeline runs seven desks and
  publishes from the 13:30 PT run, not the morning. Corroborated on main by
  `web/professional.js` ("seven-desk research architecture… Six evaluated
  workflows").
- `web/index.html` — app.js cache-bust `?v=20261004-sitewide` →
  `?v=20261107-brief-copy`, so the corrected copy is actually served.
- `tests/test_brief_copy.py` (new) — pins the corrected copy and fails on
  any return of "six desks", "every morning", or "morning research run" in
  `web/app.js`.

### 2. /api/market-context no longer blocks on the provider fan-out (2026-11-14)

- `hedge_desk/web_app.py` — the live route (`hedge-desk-web`, per
  `render.yaml` startCommand) ran `base_server._cached("market-context",
  build_market_context)` on the request thread. `build_market_context`
  calls ~27 providers sequentially (15s timeout each, `API_CACHE_SECONDS`
  15s), so every cold-cache hit blocked the request — measured 56.25s on
  the real provider fan-out, past the 30s probe timeout (the Nov 13 probe
  timed out at 30s). The non-blocking snapshot service already existed
  (`hedge_desk/market_context_service.py`) and `server.py` already used it,
  but Render never reaches `server.py`'s route: `web_app.application`
  intercepts `/api/market-context` first. The route now calls
  `get_market_context_snapshot()`: LOADING on cold start, last-good
  snapshot after, refresh in a background daemon thread. Same fix
  `server.py` already carries; this makes the production entry point match
  it. The now-unused `build_market_context` import is removed.
- `tests/test_live_data_plane_web.py` — the endpoint test now patches
  `web_app.get_market_context_snapshot`; new regression test
  `test_market_context_never_blocks_on_provider_fanout` patches the
  synchronous builder to raise and asserts the endpoint still answers 200
  with `LOADING` and `trade_authorized: false`. No behaviour change to the
  payload shape; cold start now honestly reports LOADING instead of hanging.

## What was verified (2026-11-20, after rebase onto be1a24c)

- Rebase: 3 commits replayed, 3 ahead / 0 behind `be1a24c`; all three
  commits author + committer `Toby <toby@muse.ai>`. Diff vs main unchanged
  in shape: `hedge_desk/web_app.py` (9 lines, route only),
  `tests/test_brief_copy.py` (new), `tests/test_live_data_plane_web.py`
  (regression test), `web/app.js` (brief copy only — main's Desk 5/6/7
  `desks()` preserved), `web/index.html` (cache-bust only), plus this
  handoff and `PR_BODY.md`.
- `pytest tests/test_live_data_plane_web.py tests/test_brief_copy.py
  tests/test_market_context.py` — **9 passed**.
- `pytest tests/test_execution_gate.py tests/test_risk_and_decision.py
  tests/test_account_gate.py tests/test_portfolio_gate.py
  tests/test_data_integrations.py` — **129 passed, 7 subtests passed**.
- `node --check` on `web/app.js` (.mjs copy method) — OK.
- Local WSGI timing re-measured on the rebased tree: `/api/market-context`
  answers **0.00s, 200 OK, status LOADING** on a cold start
  (`trade_authorized: false`) — the synchronous builder is never invoked
  (regression test proves it by patching the builder to raise).
- Live probe 2026-11-20 ~11:00 PT: production `/api/market-context` still
  hangs — curl exit 28, 0 bytes in 35s. Control probe
  `/market-ticker.json` answered 200 in 0.99s, so the service is up and
  the hang is specific to the market-context route. The fix is still NOT
  live; it lands only when this branch is pushed, reviewed, and merged.
- PR #169 reconciliation: its Desk 5/6 + `market_context.py` changes are
  on main as `4dbde8a` (Nov 16); the rebase replayed over them with no code
  conflict in `web_app.py` (different regions) and no changes on main to
  the branch's test files. PR #169's own API state was not verifiable from
  this shell (private repo, no authed `gh` here) — not asserted.

## What was verified (2026-11-14, after rebase onto 6fa909b)

- Rebase: clean, 2 ahead / 0 behind `6fa909b`.
- Before/after, same measurement (`/tmp/mc_timing.py`, real provider
  fan-out, WSGI call timed): BEFORE (main) 56.25s, status DEGRADED;
  AFTER (branch) 0.00s, status LOADING. The background thread runs the
  real build; the response does not wait for it.
- `pytest tests/test_live_data_plane_web.py tests/test_market_context_api.py
  tests/test_market_context_service.py tests/test_market_context_storage.py
  tests/test_brief_copy.py tests/test_copy_quality.py` — 15 passed.
- `python3 scripts/lint_copy.py` — copy-quality gate passed.
- `node --test web/*.test.mjs` — 58 passed, 0 failed.
- `cp web/app.js /tmp/syntax-check.mjs && node --check` — OK (the `.mjs`
  method from `docs/ENGINEERING_LESSONS.md` rule 2).
- Dead-code re-check: all 29 first-party `web/*.js` / `web/*.mjs` files
  (excl. `*.test.mjs`, run by node) are referenced by `index.html` or
  imported by a referenced module — nothing to remove. No TODO / FIXME /
  XXX / HACK in first-party web or `hedge_desk/*.py` files.
- Desk 7 teardown hygiene: no remaining references to a rates dashboard in
  `web/`, `docs/`, or `README*` — the Nov 13 teardown left no dangling
  links or copy.
- In-flight check (2026-11-20): main has moved 96 commits past the old
  base. The one main commit touching the branch's files is `4dbde8a`
  (Desk 5/6 + SEC + Carpe DATA, Nov 16 — the PR #169 content); its
  `web_app.py` changes are in different regions from this branch's route
  change and replayed with no code conflict. The `web/app.js` conflict was
  the new `desks()` implementation, kept in full. No other main commit
  touched `hedge_desk/web_app.py`, `tests/test_live_data_plane_web.py`,
  or `tests/test_brief_copy.py` since the old base.
- Served-state check (2026-11-14): pending — browser task dispatched to
  read the served `/api/report` freshness (main `6fa909b` is the Nov 13
  batch); see run log `2026-11-14-sat-polish.md` for the result.

## Deliberately NOT changed

- `README_PUBLIC.md` "Six desks" — the public console's desk list (six
  evaluated workflows); a different, defensible count. Same for the
  Candidates page "six desk methods" copy.
- `web/professional.js` / `web/desk-architecture.js` "Coming soon" for Bonds
  & Rates — that tag describes the public desk card, which still says
  research is in progress; the research pipeline's seventh desk is a separate
  surface. Changing it would assert a product state not verified here.
  Re-checked 2026-11-07: the Nov 6 daily package runs Bonds & Rates as
  desk 7 with real content, but the public console's "six evaluated
  workflows" framing (professional.js, desk-architecture.js subtitle,
  ui-polish.js:29, app.js:63, README_PUBLIC "Six desks") is internally
  consistent and was deliberately left alone for the third week.
- The Nov 13 daily brief's stale NVDA item (board investigation, superseded
  by Huang's resignation effective Nov 12) is published research content,
  not code polish; the republish question stays with the user. Not touched.
- No browser render verification of the copy fix: no live `/api/report`
  backend exists in this environment (same limitation as 2026-10-24).
  Copy verified at source level plus the regression test; visible on next
  deploy.

## Reviewer must check before merge

- The brief subtitle reads "seven desks / every afternoon" on the deployed
  page (cache-bust bump is what makes this visible).
- `/api/market-context` answers in well under a second on a cold start
  (LOADING first, then the snapshot once the background refresh lands);
  confirm no 30s probe timeout recurs after deploy.
- Confirm no other branch in flight re-introduces the old subtitle.

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
