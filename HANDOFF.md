# HANDOFF — Saturday polish 2026-10-31 (toby/sat-polish-2026-10-31)

Base: origin/main `d8a987f` (Daily research brief — 2026-10-30).
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
  `?v=20261031-brief-copy`, so the corrected copy is actually served.
- `tests/test_brief_copy.py` (new) — pins the corrected copy and fails on
  any return of "six desks", "every morning", or "morning research run" in
  `web/app.js`.

## What was verified

- Syntax: `cp web/app.js /tmp/syntax-check.mjs && node --check` — OK
  (the `.mjs` method from `docs/ENGINEERING_LESSONS.md` rule 2; plain
  `node --check` silently passes ESM files).
- `pytest tests/test_brief_copy.py tests/test_copy_quality.py` — 3 passed.
- `python3 scripts/lint_copy.py` — copy-quality gate passed.
- `node --test web/*.test.mjs` — 33 passed, 0 failed.
- Dead-code re-check: every `web/*.js` file is referenced by `index.html`,
  `real-estate.html`, `iphone-preview.html`, or imported by a referenced
  module — nothing to remove.
- AI-slop scan of `web/*.js` + `web/*.html`: no hits.
- In-flight check: last main change to `web/app.js` / `web/index.html` was
  2026-10-05 (merged); recent main commits are brief-only. No collision.

## Deliberately NOT changed

- `README_PUBLIC.md` "Six desks" — the public console's desk list (six
  evaluated workflows); a different, defensible count. Same for the
  Candidates page "six desk methods" copy.
- `web/professional.js` / `web/desk-architecture.js` "Coming soon" for Bonds
  & Rates — that tag describes the public desk card, which still says
  research is in progress; the research pipeline's seventh desk is a separate
  surface. Changing it would assert a product state not verified here.
- No browser render verification: no live `/api/report` backend exists in
  this environment (same limitation as 2026-10-24). Copy verified at source
  level plus the regression test; visible on next deploy.

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
