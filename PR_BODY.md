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

Verified (2026-11-14, after rebase onto main 6fa909b): pytest market-context
+ brief-copy + copy-quality 15 passed; `scripts/lint_copy.py` passed; node
test set 58 passed, 0 failed; dead-code scan clean (all 29 first-party web
files referenced); no Desk 7 dashboard references left after the Nov 13
teardown. Deliberately untouched: README_PUBLIC "Six desks" (public console's
six evaluated workflows — a different count) and the Bonds & Rates "Coming
soon" desk card (public-page state, not the research pipeline).

Reviewer check: confirm the deployed brief subtitle reads "seven desks /
every afternoon", and that /api/market-context answers in well under a second
on a cold start.
