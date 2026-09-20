# Emporion BML Progress Dashboard — 2026-09-19

Build-Measure-Learn loop status. Each row is a committed, verified slice. VERIFIED =
measured by a command; VALIDATED = matches the GP's stated expectations. Full suite:
**753/753 tests green** (7s, offline/deterministic).

## Commits (newest first)

| Commit | Type | What it did | Verified by |
|---|---|---|---|
| 2c41b4a | fix(data) | Don't present the demo $100k as the GP's real account balance (DATA peer-review) | full 753 |
| 0d2cee2 | fix(decision) | CLI validates input semantically BEFORE any vault write (ENGINEER peer-review) | manual reject tests |
| ab8a070 | fix(quant) | csp_scan collateral now credit-offset, consistent with evaluate_premium (QUANT+RISK) | csp 4/4, full 753 |
| 04c4952 | docs(morning) | one-page overnight build review for the GP | doc review |
| c8e77ed | docs(demo) | document VIX + FRED macro + 4:30pm EST scheduled batch | doc review |
| f667c96 | feat(decision) | Yellow Sheet — the GP's decision document (thesis/evidence/invalidation/exit + auto risk), not a paper-log line | yellow_sheet 6/6, full 753 |
| 665027f | feat(demo) | Compounding scale wired into AM report + demo (AAL: 1 contract @$100k, 4 @$250k, 8 @$500k, 17 @$1M) — proven on served page | full 747 |
| 7a8d9fb | feat(risk) | scale_position_to_equity — size contracts up as the account compounds (holds 2%-of-equity, scales to get big) | position_sizing suite, full 747 |
| 3d518a6 | feat(risk) | wheel-fit-for-equity — states how the wheel sizes to the GP's account (2%-of-equity → max position) | position_sizing suite, full 745 |
| 9b71a46 | feat(demo) | Surface survivability per candidate in the CSP panel (PASS/FAIL/INDETERMINATE) | am_demo 3/3 |
| fe249a9 | docs(status) | Dashboard + survivability LEARN (2%-of-equity rule needs ~$160k for a $3.2k CSP) | doc review |
| 5799682 | feat(risk) | Real account-equity input → survivability evaluates (PASS/FAIL) instead of INDETERMINATE; privacy-safe (raw equity never committed/shown) | account 5/5, nightly 2/2 |
| 46dc180 | docs(status) | BML progress dashboard — 18 commits, loop state, next increments | doc review |
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
2. Forward-earnings calendar (free sources currently 401/404-gated; retry).
3. Risk-gated Schwab execution (the gated release behind the risk engine + kill switch).

## LEARN this cycle

Wiring real account equity surfaced an honest truth: the 2%-of-equity max-loss rule
means a $3,200 cash-secured-put needs ~$160k equity to pass survivability. At a small
account, every candidate fails survivability even though it fits the wheel's capital
and return rules. That is the GP's conservative rule working as intended — the desk
now surfaces it instead of hiding behind INDETERMINATE.

**Design decision (GP): keep that scale, design to get big.** The 2%-of-equity
discipline is the immutable safety rail; the sizing is designed to compound — as the
account grows (premium collection + capital), `scale_position_to_equity` scales
contracts up automatically (a $3,200 CSP: 0 contracts at $25k, 1 at $250k, 6 at
$1M). No performance is projected or claimed; the scale path is purely conditional
on real equity.
