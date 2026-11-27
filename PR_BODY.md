[fix] Restore Desk 5 "Broker data status" Schwab disclosure

The Desk 5 view shows borrow / short-interest data but has shipped without
any broker-data disclosure since PR #169 squash-merged the Desk 5/6 work:
nothing tells the reader Schwab / thinkorswim is not connected and no
account, locate, or order endpoint is accessed here. Restores the panel at
the end of the Desk 5 view with the locked market-data-only disclosure
verbatim, and pins it in tests/test_copy_quality.py so a future squash
merge cannot silently drop it again.

Supersedes toby/tuesday-testing-2026-11-17, whose only unlanded item this
was: its options-seed now= fix already landed via PR #171, its generated
artifacts are stale, and its branch docs are not shippable. The app.js hunk
is the exact Tuesday-testing diff, applied cleanly onto current main.

Verified (2026-11-27): full suite pytest 1,416 tests, 0 failures; node
test set 60 passed, 0 failed; scripts/lint_copy.py passed; node --check
on web/app.js OK; negative control — the new disclosure test FAILS on
main's app.js and PASSES with the panel. No browser render check (no live
backend in this environment); copy verified at source level plus test.

Reviewer check: confirm the "Broker data status" panel renders at the end
of the Desk 5 view on the deployed page.
