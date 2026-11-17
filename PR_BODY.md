test: fix 3 failing tests — options-seed clock, Schwab disclosure

Tuesday testing run. Full suite was 1296 passed / 3 failed; after these
fixes it is 1299 passed / 0 failed.

- `options_seed_refresh.refresh()` gains an optional `now` parameter so
  the refresh tests can pin the fixed 2026-09-30 clock instead of the
  wall clock, which had aged past the fixture expirations and failed
  closed with "no put expiration within 30 days". Production calls are
  unchanged (workflow calls `refresh()` with no arguments).
- Restored the locked Schwab market-data-only disclosure panel on the
  Desk 5 view, dropped by the Nov 16 polish. Sentence restored verbatim.

Test evidence: full suite 1299 passed, 0 failed; named Tuesday areas
(data integrations, Graham, real-estate, Yahoo failover paths,
workbench, options lab) 173 passed; `node --check` on a `.mjs` copy of
`web/app.js` passed.
