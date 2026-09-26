# Quant Lab — Wed 2026-09-23 (part file)

Scored read-only via `hedge_desk.research_intelligence` (ResearchSource + assess_source; no code changes). **No new free options datasets or APIs this week — that lane remains empty (negative finding, same as yesterday).** No paper reached TEST this week (yesterday's TEST bar: purged walk-forward harness, 76).

| Paper / source | Date | Verdict (score) | Notes |
|---|---|---|---|
| Cohen, Drake, Guo, Reisinger — "Liquidity Provision and Rebate Design in Option Markets" (arXiv 2609.26606) | 2026-09-22 | ARCHIVE (42) | Nested make/take MM optimization in local-SV market with delta/vega inventory penalties + exchange rebate design. Theory + numerics, no empirical backtest; insufficient current value for the desks. |
| Soleimani — "Target alignment, dilution and forecast selection when cross-sectional forecasts share a common target" (arXiv 2609.26242) | 2026-09-22 | WATCH (45) | Forecast-combination methodology: equal-weighted combos beat no-info benchmarks only when target alignment dominates dispersion. Worth reading before adding signals to any combined ranker. |
| Ye — "Can You Delete a Year of Market Data? Machine Unlearning Against Exact Retraining Oracles" (arXiv, S&P 500 vol panel) | 2026-08-13 | WATCH (57) | Temporal unlearning benchmark: 2020 crisis year dominates memorization; treating stock-level windows as independent inflates t-stats by median 1.9x. Directly supports the purged/embargoed-WF methodology lane (feeds yesterday's TEST harness). |
| Yang et al. — LiMT: "Hierarchical Multi-Task Learning with Liquidity-Aware Signals" (arXiv 2609.25677) | ~2026-09-22 | ARCHIVE (40) | Regime encoder + liquidity-driven MoE jointly forecasting price move/vol/volume; CSI300/CSI500 only, transfer framing unproven on US equity options data. |
| Garcia-Ares, Vasquez, Pearson, Amaya — "The Price Impact of Hedging Expiring Index Options" (SSRN) | 2026-08-25 | ARCHIVE (42) | Proprietary MM-position data: hedge-unwind trades significantly move index futures returns/vol in the 30 min before expiration. Not replicable (proprietary data) — concepts noted for the 0DTE/expiry lane, complements yesterday's 0DTE gamma paper. |
| Brogaard et al. — "Does 0DTE Options Trading Increase Volatility?" (CFMR 2026 WP) | 2026 | ARCHIVE (34) | Finds 0DTE raises intraday/close-to-close variation with weak overnight effect; reconciliation attempt with gamma-dampening literature. Working paper, identification disputed; watch the published version. |
| Subrahmanyam — "Keeping it Simple: How Can PEAD Exist and Not Exist Simultaneously" (SSRN 5930255) | 2025 (flagged via UCLA Anderson Review Jan 2026) | WATCH (50) | PEAD t-stat collapses 2.18 → 1.43 when microcaps excluded — methodological guardrail for any earnings-drift replication (filter sensitivity before anomaly chasing). Slightly older but directly material. |

Sweep sources: https://papers.cool/arxiv/q-fin , https://academ.us/list/q-fin/ , https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/

# Parity Observer — Wed 2026-09-23 (part file)

**Nothing material.** No new parity-violation studies this week; no OESX settlement-methodology changes. Yesterday's standing notes carry over: OESX final settlement is a 10-min average (11:50–12:00 CET), not a closing print — near-expiry parity screens must use the average-based settlement or they manufacture phantom violations; literature expectation is friction-adjusted violations <1% and non-persistent.

Methodology-adjacent (older, FYI only):
- Liu & Zhu, "Can volatility spread fully capture the put–call parity violation?", N. Am. J. Econ. & Fin. vol. 80 (2025): density spread between puts and calls contributes to PCP violations in incomplete markets.
- OCC: SEC approved SR-OCC-2026-003 (May 21, 2026) — STANS methodology amended to accept binary options for clearing (enables Cboe-listed binary options); Cboe EDGX new ORF assessment methodology eff. Jul 1, 2026; OCC Rule 807 memo (Apr 17, 2026) standardized cash-only contract adjustments on corporate events. None parity-relevant.
