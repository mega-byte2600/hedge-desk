[polish] Daily brief copy: seven desks, afternoon refresh (fresh base)

Saturday good/better/best — no new features.

The Daily brief page told readers its research input came from "the six
desks" and was "Replaced every morning". Both were false: the daily pipeline
runs seven desks and publishes from the afternoon (13:30 PT) run. This fixes
the subtitle and the unpublished-brief fallback, bumps the app.js cache-bust
so the fix is actually served, and adds `tests/test_brief_copy.py` so the
drift cannot silently return.

Supersedes `toby/sat-polish-2026-10-24` (same fix, stale local-only base,
never merged).

Verified (2026-11-07, after rebase onto main 442e1a0): app.js syntax via the
`.mjs` check from ENGINEERING_LESSONS; pytest brief-copy + copy-quality
3 passed; `scripts/lint_copy.py` passed; node test set 33 passed, 0 failed.
Deliberately untouched: README_PUBLIC "Six desks" (public console's six
evaluated workflows — a different count) and the Bonds & Rates "Coming soon"
desk card (public-page state, not the research pipeline).

Reviewer check: confirm the deployed brief subtitle reads "seven desks /
every afternoon".
