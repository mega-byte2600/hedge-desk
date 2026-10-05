# PR: About DOM ownership regression test

**Title:** Add About-page DOM ownership regression test (#146/#149/#150 never-again)

**Body:**
Locks in the root-cause fixes for the 2026-10-04 About incidents as CI-enforced invariants.

**Root causes guarded:**
- #146/#149: two modules owned the same About branding → duplicate logo on prod.
- #150: zero-arg MutationObserver re-rendered on its own mutations → render loop, About page disappeared on prod.

**The test** (`tests/test_about_dom_ownership.py`, static analysis over `web/*.js`):
1. Only `professional.js` may contain `.emporion-about-logo`.
2. Only `professional.js` may define `aboutCapitalBlock`.
3. No other module may reference About-brand selectors.
4. `professional.js` must not contain a zero-arg `MutationObserver` callback; its observer must inspect mutation records (`addedNodes`).

**Evidence:**
- All 4 tests pass on this branch (based on #150 head).
- The observer-guard test fails against pre-#150 code — proven to catch the bug.
- No frontend changes in this PR; visual checks remain separate.

**Merge note:** branched from #150 head. Merge #150 first then this, or merge this directly (contains both).
