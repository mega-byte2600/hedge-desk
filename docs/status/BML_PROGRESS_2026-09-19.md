# Emporion BML Progress Dashboard — 2026-09-19

Build-Measure-Learn loop status. Each row is a committed, verified slice. VERIFIED =
measured by a command; VALIDATED = matches the GP's stated expectations. Full suite:
**738/738 tests green** (7s, offline/deterministic).

## Commits (newest first)

| Commit | Type | What it did | Verified by |
|---|---|---|---|
| fc14b1b | fix(data) | DATA peer-review: macro mode→BLOCKED when all blocked; CPI YoY from one fetch; retry-sleep fix; `_safe` broadened to any Exception | macro 3/3, suite 738 |
| 8abdf95 | docs(vv) | RESEARCH peer-review: don't present blocked FRED snapshot as current reality | doc review |
| 906ac46 | docs(vv) | ENGINEER peer-review: scope the "bounded batch" claim honestly | doc review |
| 8058165 | test(nightly) | ENGINEER peer-review: green must mean the desk worked (asserts candidates, csp fit, vix, macro, freshness) | nightly 2/2 |
| b5903c3 | fix(risk) | QUANT+RISK peer-review: equity-path units bug fixed; VIX regime risk filter (HIGH→block, ELEVATED→warn) | position_sizing + vix suites |
| e6a5e7d | feat(demo) | Rank GP-fit candidates best-trade-first + top-pick callout | am_demo 3/3 |
| dac12ea | feat(demo) | Show data as-of + freshness in AM report header | live page |
| 5607f1a | perf(pipeline) | Bound FRED fetch time (25s→8s) so a down source can't stall the batch | rates 3/3, macro 2/2 |
| 00a7cb6 | docs(vv) | Record VIX + FRED macro data surface and pipeline engineering | doc review |
| e264449 | perf(pipeline) | Run independent data fetches concurrently + offline nightly test | nightly 2/2 (0.1s) |
| e141909 | feat(pipeline) | Data-freshness gate + 4:30pm EST scheduled batch (launchd) | freshness 4/4, launchctl loaded |
| 000d89f | feat(data) | Wire real VIX regime + FRED macro desk into the nightly report | vix 5/5, macro 2/2 |
| 2cddddf | fix(demo) | Render return-on-capital as a clean percent on the AM page | am_demo 2/2 |
| 06cbfc3 | docs(demo) | MVP demo README + AM report V&V record | doc review |
| d23e3c6 | chore(demo) | Regenerate the real AM report in demo.sh before serving | live page |
| 847813f | feat(web) | Serve true-MVP AM report routes from artifacts/ | server 15/15 |
| 5a53ca1 | feat(paper) | Decision recorder CLI closes the Learn loop | paper_log 6/6 |
| b6fe110 | fix(csp) | return_on_capital basis (credit/strike) + sub-$55 GP-fit universe | csp 4/4, real Cboe |

## BML loop state

- **BUILD**: real-data pipeline (Yahoo EOD, Cboe chains, FRED rates+macro, SEC EDGAR,
  VIX), 4:30pm EST scheduled batch, concurrent fetches, freshness gate, ranked demo,
  decision recorder. 18 commits.
- **MEASURE**: the actionable metric is "GP acts on a premium candidate." Current:
  **0 recorded decisions** (paper journal empty). The report surfaces 7 GP-fit
  cash-secured-put candidates (real Cboe, <$5k, 0.55–1.39% RoC).
- **LEARN**: peer review (6 SOUL profiles, 6 model families) caught 5 real defects —
  all fixed. The loop's Learn side (paper outcomes) is armed but empty until the GP
  records a decision.

## Next increments (dependency order)

1. GP records one decision (closes the Learn loop) — the actionable measure.
2. Real account-equity input → survivability evaluates instead of INDETERMINATE.
3. Forward-earnings calendar (free sources currently 401/404-gated; retry).
4. Risk-gated Schwab execution (the gated release behind the risk engine + kill switch).
