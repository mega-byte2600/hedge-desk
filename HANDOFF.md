# HANDOFF — Saturday polish 2026-10-31, rebased 2026-11-07 (toby/sat-polish-2026-10-31)

Base: origin/main `442e1a0` (Batch refresh — 2026-11-07), rebased 2026-11-07
from `d8a987f`. Rebase was clean: no main commit since Oct 30 touched
`web/app.js` or `web/index.html` (brief + batch commits only).
Supersedes: `toby/sat-polish-2026-10-24` (commit `366246a`, same fix, built on
a local-only base and never pushed/merged — main still carried the stale copy).
Push this branch; the Oct 24 branch can be dropped by the push lane once this
one is up. No PR opened from this environment (no push path here).

## What changed (no new features)

- `web/app.js` — Daily brief subtitle: "research input from the six desks.
  Replaced every morning." → "from the seven desks. Replaced every
  afternoon." Fallback copy: "after the morning research run" → "after the
  afternoon research run." Reason: the daily pipeline runs seven desks and
  publishes from the 13:30 PT run, not the morning. Corroborated on main by
  `web/professional.js` ("seven-desk research architecture… Six evaluated
  workflows").
- `web/index.html` — app.js cache-bust `?v=20261004-sitewide` →
  `?v=20261107-brief-copy`, so the corrected copy is actually served.
  (Re-dated from `20261031` on the 2026-11-07 rebase; the fix ships today.)
- `tests/test_brief_copy.py` (new) — pins the corrected copy and fails on
  any return of "six desks", "every morning", or "morning research run" in
  `web/app.js`.

## What was verified (2026-11-07, after rebase onto 442e1a0)

- Syntax: `cp web/app.js /tmp/syntax-check.mjs && node --check` — OK
  (the `.mjs` method from `docs/ENGINEERING_LESSONS.md` rule 2; plain
  `node --check` silently passes ESM files).
- `pytest tests/test_brief_copy.py tests/test_copy_quality.py` — 3 passed.
- `python3 scripts/lint_copy.py` — copy-quality gate passed.
- `node --test web/*.test.mjs` — 33 passed, 0 failed.
- Dead-code re-check: every `web/*.js` / `web/*.mjs` first-party file is
  referenced by `index.html`, `real-estate.html`, `iphone-preview.html`,
  or imported by a referenced module — nothing to remove. No TODO / FIXME /
  XXX / HACK in first-party web files.
- AI-slop scan of `web/*.js` + `web/*.html`: no hits (`lint_copy.py` passed).
- In-flight check: no main commit since Oct 30 touched `web/app.js` /
  `web/index.html`; recent main commits are brief-only plus the Nov 7 batch
  refresh. No collision.
- Served-state check (2026-11-07): the landed batch commit `442e1a0`
  carries `data_freshness` `as_of` 2026-11-06, `is_current: true`, all
  sources OK, 0 alerts — the dashboard data is current through the Nov 6
  close. The live site still serves the stale brief subtitle until this
  branch lands (main's app.js is unchanged).

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
- No browser render verification of the copy fix: no live `/api/report`
  backend exists in this environment (same limitation as 2026-10-24).
  Copy verified at source level plus the regression test; visible on next
  deploy. Served-state spot check (Render shell responds; SPA renders
  client-side) could not read the subtitle from fetched text.

## Reviewer must check before merge

- The brief subtitle reads "seven desks / every afternoon" on the deployed
  page (cache-bust bump is what makes this visible).
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
