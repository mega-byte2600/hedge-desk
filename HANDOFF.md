# HANDOFF — About DOM ownership regression test

**Branch:** `toby/about-ownership-regression-test`
**Base:** #150 head (`35f79519`) — branched from the render-loop fix so the test runs green.
**For:** Sol — review and merge.

## What this is
`tests/test_about_dom_ownership.py` — static regression test locking in the root-cause fixes for the 2026-10-04 About incidents. It asserts single-ownership invariants over `web/*.js` so neither failure class can merge again:

1. `test_about_logo_has_single_owner` — only professional.js may contain `.emporion-about-logo`. (Guards the #146/#149 duplicate-injection.)
2. `test_about_brand_block_has_single_creator` — only professional.js may define `aboutCapitalBlock`.
3. `test_no_foreign_about_brand_injection` — no other module may reference About-brand selectors.
4. `test_mutation_observers_guard_self_mutations` — professional.js must not contain a zero-arg MutationObserver callback; its observer must inspect mutation records (`addedNodes`). (Guards the #150 self-triggering loop.)

## Verification done
- All 4 tests PASS against #150's fixed code.
- `test_mutation_observers_guard_self_mutations` FAILS against pre-#150 code (proven to catch the bug).
- Test is static analysis (no browser needed); fits the repo's Python suite.

## Merge options
- **Option A (recommended):** merge #150 first, then merge this branch (it will fast-forward cleanly — no file overlap with #150).
- **Option B:** merge this branch directly — it contains #150's fix + the test together.

## What this does NOT do
- No frontend changes. No visual assertions (browser-level visual check remains your lane).
- Does not touch brand-logo.js's sidebar observer or the professional.js/brand-logo.js `.brand` overlap (both idempotent today; noted as latent, not incident-class).
