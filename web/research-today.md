# Hedge-desk daily research — Mon 2026-11-09

**Run:** 13:30 PT, Mon 2026-11-09. Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** seven desks fanned out in parallel; synthesized below, not stapled. Every material claim carries FACT / INFERENCE / SPECULATION / UNVERIFIED. Research and input only — no git, no PRs, no code changes, no GitHub operations. Paper-only; no Risk of Ruin work; no trade authorization.

## Decision-relevant items (the 3–5 that matter)

1. **NVDA earnings Tue Nov 17 after close is the week's binary — and the premium is elevated, not cheap.** Consensus $2.49 (13 estimates, Nasdaq). Options imply a ~9.6% move (Nov 18 ATM straddle $17.18 / $178.67), ~1.7× the 5.8% average absolute reaction of the last three verified prints — and NVDA beat consensus all three times yet fell the next session twice. The stock is −13.6% in four sessions into the print ($206.69 Nov 3 → $178.67 today). Premium desk confirms the IV hump sits exactly on the event expiry (72.2% at 11 DTE vs 60.6% at 4 DTE). Per desk doctrine, premium into a binary event is to be avoided, not chased. [FACT + INFERENCE]
2. **No clean IV-vs-realized verdict exists for any watchlist name today.** All six symbols are WINDOW-CONTINGENT: the Nov 5 crash day still drives 46–63% of each 20-day realized variance (SPY 62.6%, AAPL 55.8%, TSLA 51.3%). Front IV sits below the jump-polluted realized for five of six names; only NVDA is above, and that is earnings-driven. The window cleans up ~Nov 27 when Nov 5 ages out. [FACT]
3. **Rates are a mild tailwind, funding is calm.** Fed funds effective 3.88%, 2Y 4.51%, 10Y 4.86% (all FRED, as of Fri Nov 6) — the 10Y is down ~45 bp from its Oct 5 peak of 5.31%. 2s10s +35 bp, still upward sloping but flattening ~13 bp over the past month. SOFR−EFFR +1 bp: no funding stress. [FACT, repo rates module, REAL_FRED_RATES]
4. **Two futures binaries this week, and oil's Monday drop is diplomacy, not normalization.** USDA WASDE + Crop Production Tue Nov 10, 12:00 ET — soybeans the wildcard (ending-stocks survey spread 280–404 mb, 39% of the prior estimate). Crude fell 3–4% Mon on Trump's "highly unlikely" renewed-attacks remark, but physical Hormuz shipping has NOT normalized: UKMTO-verified tanker fire + projectile strike Nov 7, Houthi hit on Aramco Tower Nov 8, Saudi East–West pipeline attacked Nov 9 (ops unaffected per ministry). **Timing correction:** next EIA Weekly Petroleum Status Report is Thu Nov 12, 12:00 ET (Veterans Day delay), not Wed Nov 11. [FACT + INFERENCE]
5. **Quant lab's most actionable find: Strasmore Research SQL API (#245, scored 61 → WATCH), verified live this run** — the first free, no-key SQL source of options IV/Greeks the lab has tested (demo returned 5 real rows in 320 ms). Free tier is limited to 1 year of history, so it covers recent-window IV/Greeks work but not multi-year IV history; licensing diligence still owed (vendor declines written market-data-rights confirmations). Sandbox cross-check against the desk's Yahoo pull is the next step. [FACT]

---

## 1. Earnings Event desk — COMPLETE

**Question:** Which watchlist names report in the next two weeks (Nov 9–23), and what does the options market price vs history?

| Symbol | Report date | Timing | Consensus EPS | Source |
|---|---|---|---|---|
| **NVDA** | **Tue 2026-11-17** | **After close** (16:00 ET) | **$2.49** (13 estimates) | Nasdaq earnings calendar API; Yahoo v7 quote (earningsTimestamp 1794949200); IV-inputs file `next_earnings: 2026-11-17` |
| AAPL | none in window; next Jan 28, 2027 | — | — | Yahoo v7 quote |
| MSFT | none in window; next Jan 27, 2027 | — | — | Yahoo v7 quote |
| TSLA | none in window; next Jan 27, 2027 | — | — | Yahoo v7 quote |
| SPY / QQQ | ETFs; no earnings | — | — | Structural fact |

- **FACT:** NVDA is the only watchlist name reporting in the next two weeks. Date corroborated three ways (Nasdaq, Yahoo quote timestamp, IV-inputs file).
- **Options-implied expected move — NVDA [FACT, live Yahoo v7 options chain, cookie+crumb, underlying $178.67]:** ~9.6% on the nearest post-earnings expiry (Nov 18 ATM 180 straddle $17.18). 10.5% on the Nov 20 weekly is NOT the earnings read (three extra sessions). ATM IV on Nov 18 expiry ~0.72–0.73 vs 0.774 on the Nov 9 expiry — premium concentrated in the event expiry, as expected.
- **Historical average earnings-day move — NVDA [FACT, Yahoo v8 daily closes; dates vs Nasdaq historical calendar]:** next-session close-to-close after the release: Nov 19, 2025 −3.15% (beat $1.24 vs $1.18); Feb 25, 2026 −5.46% (beat $1.57 vs $1.45); Aug 26, 2026 +8.74% (beat $2.22 vs $2.09). Average signed move +0.04%; average absolute move 5.8% (n=3). **INFERENCE:** options price ~1.7× the recent average absolute reaction — elevated premium. A beat has not meant a rally (3 beats, 2 down-moves); guidance vs consensus is what moves the stock. n=3 is thin; the Aug +8.7% print shows the upside tail is real. Caveat: close-to-close moves include the full next session's drift, not the isolated after-hours reaction. Q1 FY2028 report date could not be verified in Nasdaq's calendar — excluded, **UNVERIFIED**.
- **Context [FACT]:** NVDA $206.69 (Nov 3 close) → $178.67 today, −13.6% in four sessions (Nov 5: 181.60; Nov 6: 186.64; today −4.3% vs prior close). **INFERENCE:** the drawdown raises the bar for a "relief" reaction but lowers the base the Nov 17 guide is judged against.
- **What would change it:** straddle repricing into Nov 17; a date/timing change; the Nov 17 release itself (print + guide).

Sources: Nasdaq earnings calendar API (`https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`, pulled 2026-11-09 ~13:30–13:45 PT); Yahoo Finance v7 quote + v7 options chains (`query2.finance.yahoo.com`, cookie+crumb); Yahoo v8 chart daily closes; `~/workspace/hedge-desk-research/nightly/2026-11-09-iv-inputs.json` (as_of 2026-11-09T07:56:28-07:00).

## 2. Dividend Opportunity desk — COMPLETE

**Question:** Which watchlist names go ex-dividend in the next four weeks (through 2026-12-07), and has anything changed?

| Symbol | Ex-div date | Amount | Payment date | Change vs prior quarter |
|---|---|---|---|---|
| AAPL | Thu 2026-11-12 | $0.27 | Mon 2026-11-16 | None — same as Aug 10, 2026 |
| MSFT | Thu 2026-11-19 | $0.98 | Wed 2026-12-10 | None — first payment at the Sep 15, 2026 raised rate |

No other watchlist name has a declared ex-dividend date in the window.

- **AAPL — $0.27 declared, no change [FACT].** Board declared $0.27/share in the Nov 2, 2026 Q4 results release, payable Nov 16 to holders of record Nov 12; ex-div Nov 12. Source: [apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results](https://www.apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results/), corroborated by Nasdaq calendar (announcement 11/02/2026, $0.27, $1.08 indicated annual). **INFERENCE:** no increase/cut/special; $0.27 matches the May 11 and Aug 10, 2026 payments. Last day to buy for the dividend is the close of Wed Nov 11. Apple raises annually in spring; the $0.27 rate was set with the May 2026 payment (+3.8% vs $0.26 a year earlier).
- **MSFT — $0.98 ex-div Nov 19, first payment at the raised rate [FACT].** Nasdaq calendar: ex-div Thu Nov 19, 2026, record Nov 19, payment Dec 10, 2026, $0.98/share, announced Sep 15, 2026. Per the desk's standing count standard, this is the first payment at the raised rate in **24 consecutive years of annual increases (incl. the Sep 15, 2026 raise to $0.98/qtr)**. Yahoo history confirms the prior rate was $0.91 (last paid Aug 20, 2026). **Data-quality note [FACT]:** Nasdaq's `indicated_Annual_Dividend` field for MSFT still shows $3.64 (= $0.91 × 4, stale); the correct annualized rate at $0.98/qtr is $3.92.
- **NVDA — next dividend not yet declared [FACT]; December ex-date expected but unconfirmed [INFERENCE].** Last payment $0.25, ex-div Sep 10, 2026, paid Oct 1. The $0.25 rate was a 25-fold raise from $0.01 announced May 18/20, 2026 (first payment Jun 26, 2026) — a 2026 event, not a new one. Prior two Decembers went ex Dec 5, 2024 and Dec 4, 2025, so a late-November declaration with an early-December ex-date is the historical pattern. **What would change it:** NVIDIA's Q3 FY27 earnings release / board declaration, expected late November.
- **SPY / QQQ — no December distribution declared yet [FACT].** Last quarterly distributions: SPY $1.889 ex Sep 18, 2026; QQQ $0.751 ex Sep 21, 2026 (Yahoo). Q4 distributions historically go ex mid-to-late December (SPY Dec 19, 2025; QQQ Dec 22, 2025), outside this window.
- **TSLA — pays no dividend [FACT].** Yahoo 5-year chart data shows zero dividend events.
- **Increases / cuts / specials in window:** none newly announced. Cuts: none. Specials: none.
- **Verdict:** no dividend-capture opportunity of note this week — both in-window ex-dates are routine quarterly payments at already-known rates. AAPL ~0.32% / MSFT ~0.7% yields are **UNVERIFIED** against a live price pull, not computed here. **Watch item:** NVDA December declaration — holding $0.25 confirms the new rate as run-rate.
- **AAPL consecutive-increase count:** third-party sources cite 14 consecutive years since the 2012 reinstatement — **UNVERIFIED** against issuer history under the desk standard (the standard anchors only MSFT); not used as a desk claim.

Sources: Nasdaq dividends calendar API (`api.nasdaq.com/api/calendar/dividends`, swept every weekday 2026-11-09 → 2026-12-07); Yahoo Finance v8 chart dividend events (5y history, pulled 2026-11-09); Apple Q4 FY2026 results release (2026-11-02); NVIDIA Q1 FY27 release / Form 10-Q (May 2026).

## 3. Overnight Premium desk (IV) — COMPLETE

**Question:** Is front-month implied vol pricing in more or less movement than the market just delivered, and is any of it an earnings event rather than genuine premium?

**IV-inputs file:** `~/workspace/hedge-desk-research/nightly/2026-11-09-iv-inputs.json`, `as_of` **2026-11-09T07:56:28-07:00** (premarket pull, ~5.5h old at run start — **FRESH** under the 26h guard). **Data-quality caveat [FACT]:** file carries a `_failover` note — repo `hedge_desk.data.options_failover` unavailable (clone on a branch without it); legacy Yahoo-only options pull used. No failover redundancy behind these numbers.
**Live supplement:** Yahoo Finance v7 options chain, pulled ~13:35 PT / 16:35 ET (post-close; underlyings are Nov 9 closing prices), cookie+crumb handshake. Source: `query1.finance.yahoo.com/v7/finance/options/`.

### Stale-jump screen — ALL SIX SYMBOLS WINDOW-CONTINGENT
**[FACT]** 20-day realized window 2026-10-12 to 2026-11-06; max single-day variance share: SPY 62.6%, QQQ 50.4%, AAPL 55.8%, MSFT 45.8%, NVDA 49.3%, TSLA 51.3%. The Nov 5 crash day still drives >30% of every symbol's 20-day realized variance. **Every IV-vs-realized verdict below is WINDOW-CONTINGENT, never clean.** What changes it: the Nov 5 day aging out of the 20-day window (~Nov 27), or a realized-vol measure that excludes the jump day.

### IV table (ATM, call/put average; live = post-close Nov 9)

| Symbol | Close | IV file (0 DTE, premarket) | Live front IV | Live ~30–39 DTE IV | 20d realized | IV vs realized |
|---|---|---|---|---|---|---|
| SPY | 752.69 | 16.4% | 13.6% (1 DTE) / 14.8% (2 DTE) | 16.1% (39 DTE) | 20.8% | IV below realized — WINDOW-CONTINGENT |
| QQQ | 679.35 | 25.1% | 21.4% (1 DTE) / 24.4% (2 DTE) | 24.6% (39 DTE) | 33.6% | IV below realized — WINDOW-CONTINGENT |
| AAPL | 350.69 | 27.4% | 22.6% (2 DTE) / 24.5% (4 DTE) | 23.6% (39 DTE) | 25.9% | IV ≈ realized — WINDOW-CONTINGENT |
| MSFT | 545.18 | 33.1% | 25.1% (2 DTE) / 27.9% (4 DTE) | 26.5% (39 DTE) | 35.7% | IV below realized — WINDOW-CONTINGENT |
| NVDA | 178.67 | 77.4% | 60.9% (2 DTE) / 60.6% (4 DTE) | 72.2% (11 DTE, Nov 20) | 49.1% | IV above realized — WINDOW-CONTINGENT |
| TSLA | 378.05 | 51.6% | 43.9% (2 DTE) / 46.9% (4 DTE) | 46.7% (11 DTE, Nov 20) | 59.4% | IV below realized — WINDOW-CONTINGENT |

### Findings
1. **NVDA earnings hump confirmed — premium into a binary event = avoid [FACT + INFERENCE].** NVDA next earnings 2026-11-17 (per IV-inputs file). Term structure: 60.6% at 4 DTE → 72.2% at 11 DTE (Nov 20 expiry, which contains the Nov 17 print). The hump is exactly where the event sits, so the elevation is expected, not "rich." IV crush on the print is the base case. What changes it: earnings date moves, or the Nov 20 IV collapsing toward the 4-DTE level before the print.
2. **No other watchlist name has earnings inside the window [FACT, per file].** SPY, QQQ, AAPL, MSFT, TSLA all `next_earnings: null`. Term structures for SPY/QQQ/AAPL/MSFT slope gently upward (front < back, normal contango, no event hump). TSLA is flat ~44–47% across 2–11 DTE — no event priced, just a high-vol name.
3. **IV rank: UNVERIFIED for all six [UNVERIFIED].** No IV history is available from free sources, so no rank/percentile can be computed. Do not infer "elevated" or "cheap" from single-day levels. What changes it: a history source (paid IV database or a locally accumulated series).
4. **0 DTE IVs are degenerate — do not use [FACT].** Live 0-DTE ATM IVs printed 1–11% (e.g., SPY put IV 0.00001%) because the market was closed and the contracts expire today; they are expiry-day artifacts, not vol readings. The file's premarket 0-DTE numbers (16–77%) are likewise not comparable to the live front expiries. Front IV is read from 1–4 DTE above.
5. **Parity sanity check: no violation evident [INFERENCE].** ATM call/put IVs are tight at every non-0DTE expiry (e.g., NVDA 60.4%/61.5% at 2 DTE; QQQ 21.1%/21.7% at 1 DTE), consistent with put-call parity holding. The SPY 1-DTE call/put gap (15.0% vs 12.3%) is within normal skew/bid-ask noise, not a parity break. The 0-DTE put IV of ~0% is a stale/degenerate quote, not a parity violation.
6. **Directional read [INFERENCE, WINDOW-CONTINGENT].** Front IV sits below the (jump-polluted) 20-day realized for five of six names; the only name with IV above realized is NVDA, and that is earnings-driven. On the raw numbers this looks like post-crash IV compression rather than complacency — but the realized leg is dominated by one day, so no clean "premium is cheap/rich" verdict is supportable today. What changes it: a clean realized window, or front IV moving materially against the 39-DTE level.

**Desk status: COMPLETE.** No desk failure. All six symbols covered; IV rank the only UNVERIFIED item, by design (no free IV history).

## 4. Open Quant/AI Model Lab — COMPLETE

**Question:** What new papers, preprints, datasets, or free APIs relevant to the desks surfaced since the last sweep (2026-11-08)?

**Sweep result: 8 new candidates, all scored with the repo's `assess_source` and appended to the ledger as #238–245.** No TEST/INTEGRATE movement; 4 WATCH, 4 ARCHIVE. Note: the ledger's latest entry was actually #237 (QuanterLab PEAD, 2026-11-08), not #236 as briefed — numbering continues from #237. The Nov 6–8 sweeps' "empty arXiv window" was announcement lag, not an empty window: the Nov 5–6 submissions below only became visible in the API feed today. GitHub leg skipped per the run brief (no GitHub operations).

| # | Candidate | Score | Disposition | Why |
|---|---|---|---|---|
| 238 | Vidovich/Zerjal — "The End-of-Day Reversal After 2019" (arXiv:2611.09286v1, 6 Nov 2026) | 59 | **WATCH** | Pre-registered replication of the Baltussen/Da/Soebhag end-of-day reversal on point-in-time S&P 500 ex ~80 heavily traded names. Claims (source-reported, UNVERIFIED — abstract only): reversal 3.13 bps/day (t=7.5) 2016–19 and 3.05 bps (t=3.0) 2023–26, but indistinguishable from zero 2020–22; full-index reversal falls 3.40 → 0.74 bps, weakness concentrated in the largest stocks; no pre-registered mechanism test passes. No code link → reproducibility not established. Transferable item is the pre-registration + honest-null-windows discipline for the purged-WF lane, not a desk signal. |
| 239 | Tran/Yu — "Does a Trading Policy Need to Know What It Trades?" (arXiv:2611.08701v1, 5 Nov 2026) | 59 | **WATCH** | RL execution policies trained once on 954 stocks (2019 Nasdaq replay) evaluated unchanged on 1,964 unseen stocks 2020–21, 2,629 stocks 2025–26, crypto, second exchange. Claims (source-reported, UNVERIFIED — abstract only): invariant-units policy within 0.015 spreads/share of stock-specific training, own history doesn't help; but invariant units beat raw units by <1 bp and nothing extrapolates to unseen spread regimes; a near-zero transfer gap vs a pooled comparator is weak evidence a representation is right. No code link → reproducibility not established. Execution-lane read: invariance is a normalization prior, not a free lunch. |
| 240 | Nand/Guney — "Towards Robust RL Market Making" (arXiv:2611.09012v1, 6 Nov 2026) | 34 | **ARCHIVE** | Abstract carries no market, data, sample, metric, or number — inventory/cash penalties "foster resilience" is the whole claim (source-reported, UNVERIFIED). No code link. Band discipline. |
| 241 | Wang/Rachev/Fabozzi — "The Logic of Factor Portfolios" (arXiv:2611.09834v1, 6 Nov 2026) | 56 | **WATCH** | Walsh decomposition of Boolean threshold rules; US stocks 1973–2024. Claims (source-reported, UNVERIFIED — abstract only): predicted vs realized persistence correlations ≥0.999, turnover slope 1.02; 58% of single-signal portfolios beat quoted-spread costs vs 24% two-signal and 6% three-signal; interactions raise OOS Sharpe of single-signal tangency. No code link. Screen-methodology note: multi-signal interaction screens need a turnover/cost budget, not just a backtested premium. |
| 242 | Celary et al. — "Drift-invariant kernels for discount curve models" (arXiv:2611.09751v1, 6 Nov 2026) | 41 | **ARCHIVE** | Pure theory (RKHS kernel iff-form for arbitrage-free discount curves). No empirical evaluation; no code. Rates-desk-adjacent only. |
| 243 | Olkhov — "Price-Volume Correlations Are Always Zero" (arXiv:2611.08528v1, 4 Nov 2026) | 31 | **ARCHIVE** | Single-author methodological critique claiming standard price–volume correlation is definitionally zero; proposes correlating prices with squared volumes instead. No empirical validation shown; no code. Measurement-hygiene claim only. |
| 244 | Liu/Vanduffel/Bernard — "Robust distortion riskmetrics over Bregman–Wasserstein balls" (arXiv:2611.04021v1, 2 Nov 2026) | 35 | **ARCHIVE** | Risk-capital theory, same family as #205. Desk never touches the risk engine; no desk transfer. |
| 245 | Strasmore Research — SQL API over US equities + options | 61 | **WATCH** | New vendor (not in ledger). One SQL endpoint: equities since 2003, options since 2014, plus filings/macro/news; MCP; no key for the demo surface. **Verified live this run (FACT — demo endpoint queried 2026-11-09 ~13:45 PT):** test query returned 5 real rows in 320 ms; response states its own limits — no-key window is 1 year of history (from 2025-01-01), 500 rows/query, 5-day quote tape, no tick data; Developer $79/mo = 3 years, Pro $249/mo = full history. Free tier covers recent-window IV/Greeks work only, not multi-year IV history. Vendor declines written confirmations on market-data rights → licensing diligence before any desk reliance. Sandbox first: cross-check its watchlist IV against the desk's Yahoo pull. |

- **Re-check:** #236 (Fan/Wang/Ye HAR-RV-RHeston) still v3 (2026-04-10) — no new version, stays WATCH. No broad WATCH re-check this run (full re-check done 2026-11-07).
- **Triage exclusions (no ledger rows):** Buchegger #9 / Bastola #157 / Jin-Agarwal #31 re-surfaced by search — already ledgered; cvforge options-snapshot API (thin wrapper over Massive's feed; FMV is a proprietary estimate, not an executable quote; pricing/terms unverified); insurance/pension/ruin-theory, crypto/on-chain, AIDA outage registry; SSRN 2005 PEAD paper + experimental dividend-shock study (old/secondary); Emerson/Devon/ARKO/Genco dividend announcements (news, non-watchlist names — dividend desk's lane).
- **Most decision-relevant item:** #245 Strasmore — the first free, no-key SQL source of options IV/Greeks the lab has verified live; worth a sandbox cross-check against the Yahoo pull, with the 1-year free window as the hard limit. Second: #238/#239 — both are honest-negative, pre-registered or out-of-sample designs whose discipline transfers to the desk's own validation practice.

All 8 rows appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#238–245, lines 301–308) plus a 2026-11-09 kaizen-log entry (verified by orchestrator).

## 5. Weather / War / Logistics Futures Event desk — COMPLETE

**As of:** Mon 2026-11-09, 13:30 PT / 16:30 ET. Sources checked 2026-11-09.

### Imminent scheduled catalysts — CORRECTION to brief timing
- **USDA WASDE + Crop Production — Tue Nov 10, 12:00 ET (11:00 CT) — FACT.** USDA's own 2026 schedule lists Nov 10, 12:00pm ET, with Crop Production released at the same time. Multiple previews (DTN, Pro Farmer, Morningstar) confirm noon ET Tuesday. Sources: https://www.usda.gov/oce/commodity/wasde ; https://www.dtnpf.com/agriculture/web/ag/news/article/2026/11/06/grain-prices-melt-can-usda-provide ; https://www.profarmer.com/news/agriculture-news/november-wasde-why-soybeans-are-biggest-wildcard
  - **What markets expect (Dow Jones / Bloomberg surveys, via DTN & Pro Farmer, 2026-11-06):** Corn yield ~180.6 bpa, down ~0.6–0.7 bpa from Oct 181.2; production ~15.97–15.98 bb vs Oct 16.034 bb; ending stocks ~1,846 mb vs Oct 1,849 mb — essentially unchanged. Soybean yield ~53.6 bpa, up ~0.5 bpa from Oct 53.1, a new record; production ~4.60 bb vs Oct 4.562 bb; ending stocks ~332–336 mb vs Oct 315 mb. Wheat ending stocks ~744–747 mb vs Oct 740 mb.
  - **Soybeans are the wildcard — FACT (survey dispersion):** Pro Farmer: soybean ending-stocks estimates range 280–404 mb, a 124 mb spread = 39.4% of the prior USDA estimate, vs 14.7% for corn and 7.3% for wheat. Yield guesses span 53–55 bpa.
  - **What would change it:** USDA print vs survey avg at noon ET Tue; a soybean yield/stocks print outside the 280–404 mb range, or a corn yield cut materially larger than ~1 bpa.
  - **Contradicted claim flagged — do NOT use:** one aggregator (trends.glance.com) claimed WASDE was rescheduled to Nov 14 amid a shutdown. That contradicts USDA's primary schedule and all Nov 6–9 previews. Labelled **UNVERIFIED / contradicted by primary source**; no shutdown framing applies (standing rule).
- **EIA Weekly Petroleum Status Report — NOT Wed Nov 11 — Thu Nov 12, 12:00 ET — FACT (correction).** EIA's official schedule: data for week ending Nov 6, 2026 → alternate release **Thu Nov 12, 2026, 12:00 p.m. ET, Veterans Day** (holiday delay, not a shutdown). Source: https://www.eia.gov/petroleum/supply/weekly/schedule.php ; corroborated by YCharts next-release Nov 12, 12:00 EST.
  - **Last print (week ending Oct 30, released Nov 4) — FACT:** crude −865k bbl to 409.8 mmbbl vs Reuters poll +877k expected (a 1.74 mmbbl surprise draw); gasoline −222k to 209.0 mmbbl vs +153k expected; distillates −3.565 mmbbl to 99.3 mmbbl vs −100k expected — lowest since May 2003, 13% below 5-yr avg; refinery runs 94.5%, crude 4% below 5-yr avg. Sources: https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_11_04/wpsr_2026_11_04.php ; https://www.rigzone.com/news/usa_oil_stocks_drop_by_almost_1mm_bpd_week_on_week-06-nov-2026-185033-article/
  - No Reuters poll for the Nov 12 print was found in search as of this run — **UNVERIFIED**; do not invent an expectation.
  - **EIA Natural Gas Storage — next Thu Nov 13 (delayed from usual Thu by Veterans Day) — FACT** via FX Empire 2026-11-09. Last print Nov 5: +77 Bcf injection.

### Energy futures — what the curve appears to be pricing
- **Crude — sharp de-escalation sell-off Mon Nov 9 — FACT.** Dec WTI $87.43 at 09:47 ET Mon, −$3.40 / −3.74% vs Fri settlement $90.83; Jan Brent $93.96, −$4.36 / −4.43% vs $98.32. Later Mon prints ~$87.83 WTI / $93.90 Brent (−3.3% / −4.5% on the day). Sources: https://www.quantisnow.com/insight/seven-opec-producers-keep-december-output-unchanged-while-crude-opens-6780775 ; https://price-chart.com/ ; https://www.morningstar.com/news/dow-jones/202611098354/the-worlds-oil-safety-net-is-fraying-now-comes-the-rush-to-remake-it-commodities-roundup
  - **INFERENCE:** the market is pricing *reduced* near-term war-risk premium on diplomacy headlines (see below), not a resolution of physical supply disruption. The drop follows a ~16–17% Brent fall last week (per RegionAlert summary, corroboration weak — treat weekly % as **UNVERIFIED** in detail, direction confirmed by Mon levels).
  - **OPEC+ — FACT:** seven producers agreed Nov 1 to hold December output at September required levels; next meeting Nov 29. Reuters survey Mon: OPEC output +1.38 mmbpd in Oct to 22.87 mmbpd, ~90% of pre-war rate, led by Saudi/Kuwait/Iraq; Iran output −120k to 1.9 mmbpd, lowest in Bloomberg survey data back to 1989; no tankers seen at Kharg Island since late Aug. Source: https://oilprice.com/Latest-Energy-News/World-News/Saudi-Pipeline-Attacked-as-OPEC-Output-Climbs-to-90-of-Pre-War-Levels.html
  - **What would change it:** any breakdown in US–Iran talks, a verified Hormuz closure/escalation, or OPEC+ Nov 29 change.
- **Natural gas — FACT.** Dec NYMEX nat gas ~$3.03–$3.15/MMBtu Mon (FX Empire ~$3.032; Morningstar market talk +5% to $3.148 on a coming-weekend cold spell, described as short-lived). Ample storage (+77 Bcf last injection) caps upside. **INFERENCE:** curve pricing a transient weather lift, not a structural tightening. Sources: https://www.fxempire.com/forecasts/article/natural-gas-and-oil-forecast-can-wti-reclaim-93-as-hormuz-talks-continue-1643230 ; https://www.morningstar.com/news/dow-jones/202611098354/the-worlds-oil-safety-net-is-fraying-now-comes-the-rush-to-remake-it-commodities-roundup

### Geopolitics / logistics — Hormuz & Red Sea, last 48h — MATERIAL, still live
- **Diplomacy headline driving oil lower — FACT.** Pres. Trump told CNN Sun Nov 8 renewed US attacks on Iran are "highly unlikely" if Tehran makes progress toward a nuclear agreement and reopening Hormuz (repeated 5× in a 20-min phone interview); also told CBS "60 Minutes" he was "not looking to" escalate. Sec. of State Rubio Sun: "wouldn't say we're on the verge of a breakthrough." Military option remains on the table; US–Iran talks are quietly ongoing via Qatar mediation; Iran publicly demands 7 preconditions incl. ending the war on "all fronts" and lifting the maritime blockade. Sources: https://www.cnn.com/2026/11/08/politics/trump-interview-on-iran ; https://www.cnn.com/2026/11/09/middleeast/iran-us-talks-explainer-intl
  - **INFERENCE:** this headline, not any verified change in shipping, is the proximate driver of Mon's −3–4% crude move.
- **Physical shipping threat has NOT normalised — FACT (UKMTO-verified) vs IRGC claims (UNVERIFIED).** UKMTO Warnings 199-26 / 200-26, Nov 7 evening: vessel fire 8 NM NW of Khasab, Oman ~19:20 UTC, then an unknown-projectile strike on an outbound tanker ~20:20 UTC. Source: ISW Iran Update Nov 8, https://understandingwar.org/research/middle-east/iran-update-november-8-2026/ ; corroborated in LinkedIn Gulf brief citing UKMTO. Sun Nov 8: debris from an intercepted Houthi attack damaged several floors of the Aramco Tower in Riyadh (geolocated footage, ISW). Drones struck Khor Mor gas field, Iraqi Kurdistan, Nov 8. Mon Nov 9: Saudi East–West pipeline (main Hormuz-bypass route to Yanbu) attacked in Medina region — limited fire, no casualties, Saudi Energy Ministry says **no disruption to operations** (physical damage not explicitly ruled out). Source: https://oilprice.com/Latest-Energy-News/World-News/Saudi-Pipeline-Attacked-as-OPEC-Output-Climbs-to-90-of-Pre-War-Levels.html
  - IRGC Navy claims (Iranian state media, **UNVERIFIED / not independently confirmed**): southern Hormuz navigation aids destroyed overnight Nov 8–9; three (later five tankers + tug) hit mines / caught fire; southern lanes declared unauthorised/mined; night transits halted. Reuters / Times of Israel could not independently verify who/how. AIS/PortWatch traffic cited by secondary sources at ~7.1 ships/day vs 84.8 pre-crisis (~8% of normal), 54 vessels holding — **treat as INFERENCE/UNVERIFIED in detail**: sourced to secondary aggregators, not to a primary UKMTO/PortWatch release read in this run; direction (traffic severely depressed) is consistent with EIA's published Q2 Hormuz flows falling to 4.9 mmbpd from 21.6 mmbpd in Q4 2025 and with ISW's assessment that IRGC attacks continue.
  - US enforcement continues: US forces disabled the St. Kitts-flagged tanker M/V *Huda* Nov 7 after it tried to violate the US blockade of Iranian ports (ISW).
  - **What would change it:** verified resumption of sustained commercial Hormuz transits (UKMTO/PortWatch), a signed US–Iran agreement, or conversely a verified mine strike / closure declaration by a non-Iranian authority.
- **Ukraine — fresh talks Tue Nov 11, Abu Dhabi — FACT.** US–Ukraine–Russia trilateral talks restart Tue Nov 11 in Abu Dhabi, first since February; fourth round, all prior rounds ended without breakthrough; Russia still demands Donbas control, smaller Ukrainian military, no NATO. Source: https://www.cnn.com/2026/11/09/europe/russia-ukraine-us-peace-talks-preview-intl
  - **INFERENCE:** low prior probability of breakthrough; limited near-term futures impact unless an energy ceasefire emerges. What would change it: a signed ceasefire / energy-infrastructure truce.

### Ag futures — curve pricing ample supply into WASDE
- **Mon Nov 9 closes — FACT (Brownfield / Morningstar / Barchart, 2026-11-09).** Dec corn $4.39¼, −2¼¢ (−0.5%); Jan soybeans $11.82–11.88 (small source discrepancy — Brownfield $11.82¼, Morningstar $11.88¼; use the range), −~6¢ (−0.5%); Dec Chicago wheat $5.88, −3¼¢ (−0.5%).
- **Curve shape — FACT from Barchart/FarmProgress quotes Nov 9:** corn Dec $4.39 → Mar '27 $4.52 (+~13¢ contango); soy Nov '26 $11.82 → Jan '27 $11.88; wheat Dec $5.88 → Mar '27 $6.00 (+~12¢). **INFERENCE:** contango + falling prices = market pricing ample nearby supply / comfortable balances, awaiting WASDE — not scarcity.
- **Positioning — FACT (CFTC via ADM, Nov 9):** money managers sold ~79k corn contracts, flipping net short for first time in 4 months; sold 127k across soybean complex, combined long down to 285k (smallest in 2 months); Chicago wheat managed-money short up to 93k, largest in 10 months. Source: https://www.admis.com/ag-market-view-for-nov-9-2026/
- Dec corn carved a fresh 4-month low Mon, next support contract low $4.25¾ (ADM). **INFERENCE:** bearish positioning + contango leaves grains vulnerable to a *bullish* WASDE surprise (esp. soybeans, widest survey range) and cushioned against a mildly bearish one.
- Sources: https://brownfieldagnews.com/news/closing-grain-and-livestock-futures-november-9-2026/ ; https://www.morningstar.com/news/dow-jones/202611099219/grain-futures-lose-ground-ahead-of-wasde-report-daily-grain-highlights

### Watchlist relevance
No direct futures catalyst for SPY/QQQ/AAPL/MSFT/NVDA/TSLA from this desk today. Indirect channel only: **INFERENCE** — lower crude (−3–4% Mon on diplomacy headlines) eases energy-cost / inflation pressure, supportive at the margin for equities; a Hormuz re-escalation would reverse it abruptly. No position or trade implication offered (paper-only desk).

## 6. Box / Parity Observer — COMPLETE

**As of:** Mon 2026-11-09, 13:30 PT. Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA.

**Bottom line:** No new index-methodology change and no published parity-violation analysis in the last few days. Nothing material for SPY/QQQ box or put-call parity today — one pending methodology item and one rule filing to watch, and no reported parity dislocation from the Nov 5 crash.

1. **No new SPX/SPY/QQQ methodology change — FACT.** No CBOE or S&P DJI methodology update for the S&P 500, SPX, SPY, or Nasdaq-100/QQQ dated in the last few days was found in search (checked 2026-11-09). The only CBOE methodology note surfaced is a Feb 2026 consultation on the S&P 500 15% Buffer IC Index series (Tel Aviv trading-hours change) — unrelated to SPX/SPY/QQQ. Source: https://cdn.cboe.com/resources/release_notes/2026/Consultation-Results-Regarding-Methodology-Update-for-the-Cboe-S-P-500-15-Buffer-IC-Index-Series.pdf
2. **S&P DJI style-methodology revision — pending, not new — FACT (WATCH).** S&P Dow Jones Indices announced Oct 23, 2026 that U.S. style-index methodology changes take effect before the open on Dec 21, 2026: growth scoring drops 12-month price momentum; value scoring replaces book-to-price with an intangibles-adjusted measure, averages trailing + forward earnings-to-price, and adds free cash flow-to-price (excluded for real estate, banks, insurers, and certain financials). Pro-forma files reach clients Dec 4. At least ~$375B in passive funds track the affected gauges (Bloomberg Intelligence estimate via TradingView/Benzinga). This changes S&P 500 Growth/Value sub-index composition, not the S&P 500 itself or SPY/QQQ holdings — no direct parity implication. No new development since the Oct 23 announcement. Sources: https://www.tradingview.com/news/benzinga:b353d12e7094b:0-s-p-changes-the-rules-here-s-new-value-vs-growth/ ; https://www.tokenpost.com/news/investing/40132
3. **CBOE complex-order rule filing SR-CBOE-2026-081 — FACT (WATCH, minor).** Filed Oct 9, 2026; published in the Federal Register Oct 22, 2026. Amends Rules 5.33(g) and 5.34 to let a complex order with legs in different series groups leg into the Simple Book (in addition to the Complex Order Book) where Cboe designates the groups as related, and to set risk controls on a related-group basis. Context in the filing notes SPX (A.M.-settled) and SPXW (P.M.-settled) sit on separate matching engines, with Weekly A.M.-settled SPX ("SPXO") planned. This is execution plumbing for multi-leg (including box) orders, not a parity or methodology change; no evidence it has moved box-spread pricing. Source: https://www.govinfo.gov/content/pkg/FR-2026-10-22/html/2026-21576.htm
4. **Nov 5 crash — no reported parity dislocation — UNVERIFIED (no published analysis found).** Nov 5, 2026: S&P 500 −4.36%, Nasdaq-100 −6.36% (worst since Mar 2020), VIX closed 28.18 (+~70% on the day). Saxo (Nov 6) reports 0DTE SPX options had priced a ~0.55% move vs the actual 4.36% (~8× priced move), put volume outnumbered calls ~4:1 in index funds, and dealer hedging "may have added to Thursday's fall" — but Saxo attributes amplification to hedging, not to a parity break, and reports no put-call parity or box-spread violation. CrossVol (Nov 6) reports 1-month QQQ skew jumping from 5.2 pts (28th percentile) to 12.4 (99th) — a skew repricing, not a parity violation. Nov 5 flow data (SquawkFlow) shows extreme same-day SPY/QQQ put volume (SPY Nov-5 puts $4.1B estimated premium, 6.65M contracts) — heavy hedging flow, not evidence of arbitrage failure. **No source found reports a box-spread or put-call parity dislocation on Nov 5; equally, no source has published a parity check of that session — absence of a report is not proof parity held.** Deterministic parity (C − P = D·(F − K)) cannot be verified for Nov 5 from free sources. Sources: https://www.home.saxo/en-mena/content/articles/options/eight-times-the-priced-move---options-brief---6-november-2026-06112026 ; https://newsletter.crossvolresearch.com/p/stock-market-crash-what-happens-next-nasdaq ; https://squawkflow.com/options-flow/2026-11-05?utm_source=rss
5. **Background (not new): SPX parity holds in price space; a systematic carry wedge exists — FACT (published analysis, Aug 2026).** Shin (arXiv, Aug 24, 2026, "The Cost of a Free Lunch"), using minute-level NBBO SPX/RUT data Jan 2016–Oct 2025: quoted put-call parity residuals vs traded-futures forwards are "tightly compressed around zero," but the option-implied discount factor leaves a systematic carry gap vs OIS (sample median ≈37 bp, >98% positive) — an implementation wedge from finite arbitrage capital and path/margin risk, not a tradeable price-space violation. A companion paper (May 19, 2026, v3) reaches the same conclusion. An independent SPX surface fit on Oct 16, 2026 quotes (Deyirviel, "The Derivatives Lab") likewise found parity "essentially exact," with only one small calendar violation (4.9×10⁻⁴ in total variance) between the 2M and 3M slices. Neither is new in the last few days; both reinforce that parity is enforced in price space while box-implied rates run above risk-free — the standing reason box spreads price as synthetic loans, not free money. Sources: https://arxiv.org/html/2604.19604 ; https://arxiv.org/pdf/2605.12250v3.pdf ; https://www.deyirviel.com/portfolio/derivatives-lab/

**What would change this verdict:** a published parity check of the Nov 5 session showing box-implied rates or C−P residuals materially off fair value; a CBOE/S&P DJI methodology notice dated after Oct 23 affecting SPX, SPY, or QQQ; or the Dec 4 S&P pro-forma files revealing watchlist-name style reclassifications large enough to move index-tracking flows.
**Disposition:** No action. Watch items only: S&P DJI pro-forma files (Dec 4) and Dec 21 style reconstitution; SR-CBOE-2026-081 complex-order legging.

## 7. Bonds & Rates desk — COMPLETE (PASS)

**Source:** repo module `hedge_desk.rates_desk.rates_environment()` — mode `REAL_FRED_RATES`, FRED public CSV (HTTP 200). Module run succeeded; all numbers below are from its output. Latest observations are **Fri 2026-11-06** (FRED daily series lag one business day; today's Nov 9 data not yet published at run time).

| Series | Level | As of | Note |
|---|---|---|---|
| Fed funds effective (DFF/EFFR) | **3.88%** | 2026-11-06 | Module reports change-over-window: +0.25 (as returned; sign/convention per module) |
| Treasury 2Y (DGS2) | **4.51%** | 2026-11-06 | Down from 4.80% on Oct 9 |
| Treasury 10Y (DGS10) | **4.86%** | 2026-11-06 | Down from 5.24% on Oct 9; peak 5.31% on Oct 5 |
| 2s10s slope | **+35 bp** | 2026-11-06 | Upward sloping; 48 bp on Oct 6, 44 bp on Oct 9 → **flattening ~13 bp over the past month** |
| SOFR | **3.89%** | 2026-11-06 | |
| EFFR | **3.88%** | 2026-11-06 | |
| OBFR | **3.88%** | 2026-11-06 | |
| **SOFR − EFFR spread** | **+1 bp** | 2026-11-06 | No funding stress |

- **FACT:** Fed funds effective 3.88%, 2Y 4.51%, 10Y 4.86%, all as of 2026-11-06 (FRED via repo module). 2s10s +35 bp, upward sloping.
- **FACT:** The curve flattened over the past month — 2s10s narrowed from 48 bp (Oct 6) / 44 bp (Oct 9) to 35 bp (Nov 6), computed from the module's 60-day history. The 10Y fell ~45 bp from its Oct 5 peak (5.31% → 4.86%).
- **FACT:** SOFR−EFFR is +1 bp and OBFR equals EFFR at 3.88% — overnight funding markets are calm, no stress signal.
- **INFERENCE:** Long rates easing from early-October highs reduces discount-rate pressure on growth multiples — modestly supportive for the growth-heavy watchlist names (NVDA, MSFT, QQQ, and SPY via its growth weight). This is a directional read, not a valuation call: the 10Y at 4.86% remains elevated in absolute terms, so the pressure is lessened, not gone.
- **INFERENCE:** The flattening (2Y stickier than 10Y) is consistent with the market pricing the front end as anchored near the current policy rate while the long end drifts lower — no inversion, no recession signal from this curve segment.
- **UNVERIFIED:** Today's (Mon Nov 9) rates — FRED daily series not yet published at run time; nothing here reflects Monday's session.

**What would change the verdicts:** a 10Y move back above ~5.25% would restore the early-October discount-rate pressure read; a 2s10s inversion (below 0 bp) would flip the curve read to a recession-warning signal; a SOFR−EFFR widening beyond ~10 bp would change the funding-stress read from calm to stressed. Monday's FRED release (tomorrow's run) supersedes the Nov 6 levels.

**Desk status: PASS** — module ran clean, real FRED data, no substitution. Nothing material for the premium desk beyond the directional read above: rates are a mild tailwind to growth multiples this week, funding is calm, and the curve is flattening but still upward sloping.

---

## Cross-desk reconciliation (orchestrator)

- **NVDA earnings is the single cross-desk event:** Earnings desk (Nov 17 after close, $2.49 consensus, ~9.6% implied move) and Premium desk (IV hump at Nov 20 expiry, 72.2% vs 60.6% at 4 DTE) agree; Dividend desk adds that NVIDIA's December dividend declaration is expected around the same window (late November). No contradiction.
- **Window-contingency is the week's governing caveat:** Premium desk's all-symbols WINDOW-CONTINGENT verdict and Parity desk's "no parity check of Nov 5 exists" both trace to the same Nov 5 crash day. No desk issued a clean cheap/rich or parity-held verdict today.
- **EIA timing correction (Futures desk, verified against eia.gov):** next Weekly Petroleum Status Report is Thu Nov 12, 12:00 ET (Veterans Day delay), NOT Wed Nov 11 as the run brief stated. WASDE Tue Nov 10, 12:00 ET confirmed against USDA's schedule. A third-party claim of a WASDE reschedule to Nov 14 amid a shutdown is contradicted by USDA's primary schedule — do not use; no shutdown framing applies.
- **No contradictions between desks on levels:** NVDA close $178.67 (Earnings and Premium desks agree); SPY 752.69 / QQQ 679.35 post-close (Premium desk). Rates desk's FRED levels are as of Fri Nov 6 (series lag), not Monday's session — no conflict with any desk.
- **Desk status:** all seven desks COMPLETE; no desk FAILED; no retry needed. Quant lab ledger append verified by orchestrator (#238–245, lines 301–308, plus kaizen-log entry).

## Run notes
- IV-inputs freshness guard: PASS — `2026-11-09-iv-inputs.json`, as_of 2026-11-09T07:56:28-07:00, ~5.5h old at run start, within the 26h guard. Caveat: `_failover` note — legacy Yahoo-only pull, no failover redundancy.
- Yield labeling: ^FVX is the 5Y (never 2Y); 13W is the front-end anchor, labeled as 13W.
- Government-data rule applied: no shutdown framing; EIA/WASDE on schedule per primary sources (eia.gov / usda.gov).

---

## Addendum — NVDA governance event (added 13:44 PT, post-run correction)

The 13:30 run's NVDA sections carry the price move (−13.6% in four sessions, $206.69 → $178.67) and the premium caution but do not name the cause. The cause was corroborated Mon morning before the run and belongs in the record:

- **FACT (corroborated across Morningstar, CoinDesk, BusinessWire, Hindu BusinessLine, Zacks):** Nvidia's board announced Sun Nov 8 an independent investigation by a committee of independent directors, supported by outside legal counsel, into reports CEO Jensen Huang was targeted by a foreign intelligence effort. Underlying reports: NYT Nov 8 and FT/WSJ — US intelligence identified Alice Huang, a former executive at Singapore-based Megaspeed, as a Chinese spy; Huang admitted an affair/intimate relationship with her, apologised to staff/family, and supports the review.
- **FACT (company position, repeated across outlets):** Nvidia states no reason to believe US national security or company secrets/confidential information were compromised.
- **UNVERIFIED:** the foreign-intelligence allegations themselves; investigation outcome and timeline unknown. Zacks notes an expectation of US Congress hearings.
- **FACT (price move, corroborated):** NVDA −5.76% to $175.89 at 07:33 ET Mon Nov 9 vs Fri close $186.64; Morningstar puts the implied market-value loss at ~$232B. The move is NVDA-specific — broad futures were up at the same time.
- **UNVERIFIED (unchanged):** the +27% 0DTE IV rise itself remains Yahoo-only (CBOE delayed quotes came back empty in the Nov 8 nightly). The driver and the price move are corroborated, not the IV level.
- **Implication (carried from the morning delivery):** NVDA is a governance-event name, not a cheap/rich premium signal. Do not sell NVDA premium into the spike. Do NOT treat Nov 17 earnings as a clean earnings binary — it now carries a governance overhang. The ~9.6% implied move in §1 is the market's earnings read; the governance overhang is a separate, unpriced-in-full risk on top of it.
