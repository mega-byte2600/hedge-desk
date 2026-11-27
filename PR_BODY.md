[polish] Daily brief copy + /api/market-context no longer blocks on provider fan-out

Saturday good/better/best — no new features.

1. Daily brief copy: the page told readers its research input came from "the
six desks" and was "Replaced every morning". Both were false: the daily
pipeline runs seven desks and publishes from the afternoon (13:30 PT) run.
This fixes the subtitle and the unpublished-brief fallback, bumps the app.js
cache-bust so the fix is actually served, and adds `tests/test_brief_copy.py`
so the drift cannot silently return. Supersedes `toby/sat-polish-2026-10-24`
(same fix, stale local-only base, never merged).

2. /api/market-context: the live route ran the synchronous
`build_market_context` (~27 providers, sequential, 15s timeout each) on the
request thread, so a cold-cache hit blocked 56s — past the 30s probe timeout
(Nov 13 probe timed out). The route now serves the snapshot
(`get_market_context_snapshot`, same as server.py already does): LOADING on
cold start, last-good after, refresh in a background thread. Measured
before/after on the real provider fan-out: 56.25s → 0.00s. Regression test
added proving the synchronous builder is never invoked on the request path.

3. About page source copy now matches the served copy (2026-11-21):
`web/ui-polish.js` rewrites the About card's first paragraph on every
render, so the paragraph in `web/app.js` was dead copy at runtime — and
stale, still calling Bonds & Rates "in development" after the Desk 7
indicator board shipped. Aligned to the served wording ("six specialized
research workflows…"); no user-visible change. `tests/test_copy_quality.py`
pins it so source and served copy cannot drift again.

Verified (2026-11-27, after rebase onto main 1510b12e): full suite pytest
1,419 tests, 0 failures/errors/skipped; node test set 60 passed, 0 failed;
`scripts/lint_copy.py` passed; `node --check` on web/app.js OK; local WSGI
timing re-measured 0.001s cold / 0.000s warm (LOADING, sync builder never
invoked). Live probe 2026-11-27: production /api/market-context still hangs
(http 000, 45s timeout) — the fix is still not live.
Verified (2026-11-21, after rebase onto main 1743c27): full suite pytest
1,368 passed, 0 failed; node test set 60 passed, 0 failed;
`scripts/lint_copy.py` passed; `node --check` on web/app.js OK; local WSGI
timing re-measured 0.00s (LOADING, cold start). Live probe 2026-11-20:
production /api/market-context still hangs (curl timeout, 0 bytes in 35s)
while /market-ticker.json answers in 0.99s — the fix is still not live.
Earlier verification (2026-11-20, after rebase onto main be1a24c): pytest
market-context + brief-copy 9 passed; gate + data-integration suites 129
passed, 7 subtests passed; node --check on web/app.js OK; local WSGI timing
re-measured 0.00s (LOADING, cold start). Earlier verification (2026-11-14,
after rebase onto main 6fa909b): pytest market-context + brief-copy +
copy-quality 15 passed; `scripts/lint_copy.py` passed; node test set 58
passed, 0 failed; dead-code scan clean (all first-party web files
referenced); no Desk 7 dashboard references left after the Nov 13 teardown.
Deliberately untouched: README_PUBLIC "Six desks" (public console's six
evaluated workflows — a different count; Desk 7 is an indicator board, not
an evaluated engine) and the Candidates "six desk methods" copy. Note: the
Bonds & Rates "Coming soon" tag cited in earlier versions of this body no
longer exists — main's PR #169 shipped the Desk 7 board; the About
"in development" line fixed here was the stale remnant.

Reviewer check: confirm the deployed brief subtitle reads "seven desks /
every afternoon", and that /api/market-context answers in well under a second
on a cold start.
