# Hedge-Desk Daily Research — Wed 2026-10-14

**Run:** 1:30pm PT, Wed 2026-10-14. Research + input only. Paper-only context.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Standing rules applied:** Yahoo-first (UA header required); ^TNX = 10Y, ^FVX = 5Y (never 2Y), 13W = front-end anchor; NO federal shutdown (CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11); MSFT dividend count per ~/workspace/hedge-desk-research/dividend-count-standard.md; window-contingent rule (>30% single-day share of 20-day realized variance); IV-inputs 26h freshness guard.

**Synthesis — the 5 most decision-relevant items:**
1. **Earnings-loaded premium is the trap to avoid; NVDA is the clean read.** MSFT (Oct 28), TSLA (Oct 21), AAPL (Nov 2) all report before Nov-13 expiry, so their elevated IVs partly reflect the pending print, not harvestable vol premium. NVDA (Nov 18, past expiry) is the only single name whose Nov-13 IV is earnings-free — IV 33.9% vs 20-day realized 22.7%, NOT window-contingent — the desk's single highest-conviction premium observation. (Premium desk)
2. **Rates are a headwind for growth multiples.** FRED via the repo's own rates module (as-of 2026-10-13): EFFR 3.88%, 2Y 4.79%, 10Y 5.21%, 2s10s +42bp — bear-flattening (2Y +60bp vs 10Y +49bp over 60 days). SOFR–EFFR +1bp = no funding stress. (Bonds & Rates desk)
3. **Diesel is the energy story; EIA is tomorrow, not today.** IEA: diesel/gasoil "tight well into 2027," record ~$95/bbl Sep diesel margins; heating oil +4.2% over 4 sessions vs RBOB −4.7%. EIA weekly was NOT due today — Columbus Day shift moves it to Thu Oct 15, 12:00pm ET (primary source: eia.gov schedule). Oil is backwardated on Houthi/Aramco headlines (Dec→Jan Brent −$2.55). (Futures desk)
4. **TSLA's consensus is disputed — don't trust a beat/miss call.** Nasdaq EPS consensus $0.21 (10 ests) vs Yahoo avg $0.45 (range $0.30–$0.70). MSFT consensus is clean ($4.71 vs $4.72). TSLA implied move 7.33% vs 3.10% ex-outlier historical mean; MSFT implied 6.17% vs 5.61% ex-outlier. (Earnings desk)
5. **No dividend capture in the window.** No watchlist name goes ex-dividend by Nov 11. MSFT ex Nov 19 (just outside window), $0.98 (+7.7%), 24 consecutive annual increases per standard. AAPL Q4 not yet declared. (Dividend desk)

**Cross-desk reconciliation:** Dividend desk's inference that AAPL declares "with earnings ~Oct 30" is superseded by the Earnings desk's dual-source-verified AAPL date of Mon Nov 2 AMC — declaration timing, if it follows earnings, tracks Nov 2, not Oct 30. Premium desk's earnings dates (MSFT 10-28, TSLA 10-21, AAPL 11-02, NVDA 11-18) agree with the Earnings desk except NVDA, which the Earnings desk flags as single-source/provisional (Nasdaq calendar does not yet list it). Futures desk corrected the brief's EIA premise (due today → actually Thu Oct 15 noon ET) against the primary eia.gov schedule; the correction stands.

---

## 1. Earnings Event Desk

**Question:** Which watchlist names report in the next 2 weeks, and what does the options market price?

| Symbol | Earnings date | Timing | Implied move % (ATM straddle) | Historical avg earnings-day move |
|---|---|---|---|---|
| TSLA | Wed 2026-10-21 | AMC | **7.33%** — Oct-23 expiry straddle $26.92 / spot $367.16 (ATM strike 367.5; call mid $13.58 + put mid $13.35) | Mean \|move\| **5.95%**, n=4 (+2.28%, −3.45%, −3.56%, −14.52%); **3.10%** ex-outlier |
| MSFT | Wed 2026-10-28 | AMC | **6.17%** — Oct-30 expiry straddle $32.95 / spot $533.69 (ATM strike 535; call mid $16.58 + put mid $16.38) | Mean \|move\| **8.09%**, n=4 (−2.92%, −9.99%, −3.93%, +15.51%); **5.61%** ex-outlier |
| AAPL | Mon 2026-11-02 | AMC — **outside window** | n/a | n/a |
| NVDA | ~Tue 2026-11-17 | timing UNVERIFIED — **outside window** | n/a | n/a |
| SPY / QQQ | — | — | n/a | ETFs; no earnings (FACT) |

- **FACT:** Only TSLA Oct 21 AMC and MSFT Oct 28 AMC fall in the window; each confirmed on two independent sources (Nasdaq calendar API + Yahoo calendarEvents, `isEarningsDateEstimate: false`). AAPL Nov 2 AMC is the first one after the window. *What would change it:* an issuer reschedule or calendar revision.
- **FACT:** Implied move = nearest-ATM straddle mid ÷ spot, first weekly expiry *after* earnings (TSLA Oct 23, MSFT Oct 30). Both expiries sit 2 sessions after the report, so each straddle carries ~2 extra days of time value and **slightly overstates** the pure single-session earnings move. Neighboring-strike straddles bracket TSLA at 7.33–7.57% and MSFT at 6.17–6.45%.
- **FACT:** Historical moves = Yahoo daily-bar closes, earnings-date close → next-session close, last 4 reported quarters, verified individually against the Nasdaq calendar. Raw (unadjusted) closes; no splits in window. n=4 means are small-sample, each dominated by one big quarter — context, not forecast.
- **FACT + INFERENCE:** TSLA consensus EPS: **Nasdaq $0.21 (10 ests) vs Yahoo avg $0.45 (range $0.30–$0.70), revenue avg $28.11B** — the two sources disagree; do not average them. Implied 7.33% exceeds the trailing mean |move| 5.95% and far exceeds the 3.10% ex-outlier average (INFERENCE). Any "beat/miss" call against either consensus number is unreliable until the release lands. *What would change it:* the Oct 21 release + 10-Q; a reconciled consensus.
- **FACT + INFERENCE:** MSFT consensus is consistent: **Nasdaq $4.71 (13 ests) vs Yahoo $4.72, revenue ~$90.7B**. Implied 6.17% sits below the 8.09% trailing mean (inflated by Jul-26's +15.51%) and just above the 5.61% ex-outlier average (INFERENCE). *What would change it:* the Oct 28 release; a guidance surprise.
- **UNVERIFIED:** NVDA Nov 17 is single-source and tentative (Yahoo lists 2026-11-17; Nasdaq's 2026-11-17 calendar, checked directly, does not yet list NVDA — likely too far out). Treat as provisional until Nasdaq or the issuer confirms.
- No earnings release exists yet for TSLA or MSFT, so there is nothing to teardown under the CFA read-the-release standard; EDGAR was not queried because no 8-K/10-Q for these quarters can exist yet.
- AAPL consensus: Nasdaq $1.99 vs Yahoo $1.98 (consistent) (FACT).

**Sources:** Nasdaq earnings calendar API `https://api.nasdaq.com/api/calendar/earnings?date=2026-10-21` (same pattern for the 2026-10-15…2026-10-28 sweep, plus 2026-11-02, 2026-11-17, and 8 historical dates); Yahoo options `https://query1.finance.yahoo.com/v7/finance/options/TSLA`, `…/options/MSFT` (cookie+crumb session; UA header); Yahoo calendarEvents `https://query1.finance.yahoo.com/v10/finance/quoteSummary/TSLA?modules=calendarEvents` (same for MSFT, AAPL, NVDA); Yahoo daily bars `https://query1.finance.yahoo.com/v8/finance/chart/TSLA?range=2y&interval=1d` (same for MSFT). As-of ~13:28 PT Oct 14.

---

## 2. Dividend Opportunity Desk

**Window:** 2026-10-14 → 2026-11-11 (4 weeks). **Headline: NO ex-dividend dates on the watchlist fall inside the window.** (FACT — verified by per-date Nasdaq calendar API scan.)

| Symbol | Ex-date | Pay date | Amount | Change vs prior | Consecutive-increase count (per standard) | Status |
|---|---|---|---|---|---|---|
| SPY | None in window | — | — | — | N/A (variable ETF distribution) | Next ex Dec 18, 2026 (FACT, SSGA schedule) |
| QQQ | None in window | — | — | — | N/A (variable ETF distribution) | Next ex ~Dec 21–22, 2026 (INFERENCE from prior-year pattern; amount UNVERIFIED) |
| AAPL | None in window — **Q4 dividend NOT YET DECLARED** | — | — | — | UNVERIFIED this run (not checked against issuer history; do not carry a count) | Next declaration expected with earnings (INFERENCE); ex-date UNVERIFIED until declared |
| MSFT | None in window — ex **Nov 19, 2026** (8 days past window end) | Dec 10, 2026 | **$0.98** | **+$0.07 vs $0.91 (+7.7%)** — announced Sep 15, 2026 | **24 consecutive annual increases (incl. the Sep 2026 raise to $0.98/qtr)** per the standing standard | Declared; outside window |
| NVDA | None in window — Q4 NOT YET DECLARED | — | — | — | UNVERIFIED this run | Next payment estimated late Dec (INFERENCE); ex-date UNVERIFIED |
| TSLA | — | — | — | — | — | Pays no dividend (FACT) |

- **FACT:** No dividend-capture opportunity in the window — nothing to act on.
- **FACT:** MSFT is the only announced change on the watchlist, and it sits just outside the window: ex Nov 19, pay Dec 10, $0.98 (+7.7% vs $0.91). Count = 24 consecutive annual increases per the standing standard — some third-party screens still show 23; the standard explicitly resolves this to 24 (the Sep 15, 2026 raise); this desk does not drift from it. No new increase/cut/special announced since Sep 15.
- **FACT:** AAPL Q4 is the one to watch, not to assume: last ex Aug 10, 2026 ($0.27, raised from $0.26 on Apr 30, 2026). The Q4 declaration has not been made as of this run, so its ex-date and amount are UNVERIFIED — no projected date or amount is carried as fact. (Note: the desk's "~Oct 30" earnings-timing inference is superseded by the Earnings desk's verified AAPL date of Nov 2 — see reconciliation above.)
- **FACT + labeled estimates:** ETF/NVDA variability is not a "cut": SPY (last ex Sep 18, $1.889) and QQQ (last ex Sep 21, $0.75143) pay variable quarterly distributions; NVDA's next quarter is undeclared with only third-party estimates (~$0.25, late Dec). None is an announced cut, increase, or special.

**Sources (as-of ~13:30–14:00 PT Oct 14):** Nasdaq dividends calendar API per-date queries — `https://api.nasdaq.com/api/calendar/dividends?date=2026-11-19` → MSFT row (ex 11/19/2026, pay 12/10/2026, record 11/19/2026, $0.98, announced 9/15/2026); per-date scans of 2026-10-15, 10-16, 11-02 through 11-12, 12-10, 12-11, 12-18 returned zero watchlist rows inside the window. Consecutive-increase definition: `~/workspace/hedge-desk-research/dividend-count-standard.md`. SPY Dec 18, 2026 ex-date: SSGA SPDR Dividend Distribution Schedule (https://dooprimechn.co/__line/www.ssga.com/library-content/products/fund-data/etfs/us/distribution/SPDR_Dividend_Distribution_Schedule.pdf). AAPL last dividend: https://www.marketbeat.com/stocks/NASDAQ/AAPL/dividend/. MSFT raise corroboration: https://alphabetastock.com/microsoft-msft-stock-8-percent-dividend-increase/. NVDA last dividend ($0.25, ex 9/10/2026, pay 10/1/2026; next undeclared): https://www.marketbeat.com/stocks/NASDAQ/NVDA/dividend/ and https://www.zacks.com/stock/research/NVDA/dividend-history. Yahoo Finance quoteSummary dividend modules returned empty for all six symbols this run — Yahoo NOT relied on for this desk's numbers; Nasdaq API is the source of record here.

---

## 3. Overnight Premium Desk (IV)

**Data lineage:** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-10-13-iv-inputs.json`, `as_of` **2026-10-13T13:54:24−07:00** — within the 26h guard, USED, but it is yesterday's post-close snapshot. **Live Yahoo pull FAILED** (query1/query2 → HTTP 401; finance.yahoo.com → connection reset, despite the required UA header). Fallback per standing rule: **live Nasdaq option-chain pull** 2026-10-14 ~13:45 PT, ATM IV inverted from bid/ask midpoints via Black–Scholes (r = 4.26% = FRED DGS3MO 2026-10-13; q = 0 simplification, labeled). **IV-rank is UNVERIFIED for all six** — no free IV-history source available; never guessed.

**⚠️ Do not use the file's own `atm_iv` for SPY/QQQ:** SPY 1.20% / QQQ 1.14% are 0-DTE same-day-expiry artifacts (expiry 2026-10-13, DTE 0), not comparable to 20-day realized. Single-name file values are 1-DTE. All comparisons below use the live ~30-DTE IV.

| Symbol | Live ATM IV (~30 DTE, Nov 13 expiry) | Realized 20d (file, window 9-15→10-12) | Window-contingent | IV-vs-realized verdict | Earnings in Nov-13 window | As-of |
|---|---|---|---|---|---|---|
| SPY | 15.9% (K=752, 2.2% below spot — nearest strike in truncated Nasdaq page, not true ATM) | 9.7% | YES (0.327) | IV > realized by ~6.2 pts — **WINDOW-CONTINGENT** | n/a (index) | Live 10-14; realized 10-13 |
| QQQ | 20.3% (K=728 ≈ spot) | 15.5% | YES (0.426) | IV > realized by ~4.8 pts — **WINDOW-CONTINGENT** | n/a (index) | Live 10-14; realized 10-13 |
| AAPL | 26.5% (K=345) | 17.3% | YES (0.335) | IV > realized by ~9.2 pts — **WINDOW-CONTINGENT** | **YES — 11-02 inside window** | Live 10-14; realized 10-13 |
| MSFT | 31.7% (K=535) | 21.2% | YES (0.359) | IV > realized by ~10.5 pts — **WINDOW-CONTINGENT** | **YES — 10-28 inside window** | Live 10-14; realized 10-13 |
| NVDA | 33.9% (K=220) | 22.7% | NO (0.228) | IV > realized by ~11.1 pts — **cleanest rich-premium read** | NO — 11-18 is 5 days past expiry | Live 10-14; realized 10-13 |
| TSLA | 44.5% (K=365) | 30.6% | YES (0.301, barely over 0.30) | IV > realized by ~13.9 pts — **WINDOW-CONTINGENT** | **YES — 10-21 inside window** | Live 10-14; realized 10-13 |

- **INFERENCE:** Premium is rich vs trailing realized across the whole watchlist. Every name's live ~30-DTE ATM IV sits 5–14 pts above its 20-day realized vol. Only NVDA's verdict is clean — its window is NOT contingent (max single-day share 0.228), so the IV > realized gap is the desk's single highest-conviction premium observation.
- **FACT:** Five of six verdicts are WINDOW-CONTINGENT, not clean. SPY (0.327), QQQ (0.426), AAPL (0.335), MSFT (0.359), TSLA (0.301) each have one day driving >30% of 20-day realized variance. The realized leg of every one of those comparisons is dominated by a single session — treat the gaps as suggestive, not settled. *What would change it:* the dominant day rolling out of the 20-day window, or a realized series recomputed ex-that-day.
- **INFERENCE:** AAPL, MSFT, TSLA Nov-13 premium is earnings-loaded — premium into a binary event = avoid. MSFT reports 10-28, TSLA 10-21, AAPL 11-02, all before Nov-13 expiry, so their elevated IVs partly reflect the pending print, not a harvestable vol premium. NVDA (11-18) is the only single name whose Nov-13 IV is earnings-free — which is precisely why its rich-premium read is the cleanest.
- **INFERENCE (noisy):** Term structure: QQQ front-end elevated, SPY flat. From the same live Nasdaq pull, 1-DTE ATM IV was SPY ~15.0% (vs 15.9% at 30 DTE — flat) and QQQ ~25.2% (vs 20.3% at 30 DTE — downward-sloping, front elevated). Caveat: 1-DTE quotes are noisy (pin risk, wide spreads, q=0 assumption) — read as direction only. Put-call parity residuals on the 30-DTE ATM pairs were small (QQQ −0.03, NVDA +0.01, SPY +0.14, AAPL +0.24, MSFT +0.28, TSLA +0.64), consistent with the q=0 simplification plus quote noise — no parity violation claimed (FACT).

*What would change the desk's verdicts:* (1) a free IV-history source enabling true IV-rank; (2) the dominant realized-variance day exiting the window; (3) earnings passing for MSFT (10-28), TSLA (10-21), AAPL (11-02), after which their IVs should be re-read ex-event.

**Sources:** IV inputs `~/workspace/hedge-desk-research/nightly/2026-10-13-iv-inputs.json` (as_of 2026-10-13T13:54:24−07:00); live chains `https://api.nasdaq.com/api/quote/{SYM}/option-chain?assetclass=etf|stocks&limit=250&fromdate=2026-11-06&todate=2026-11-20`; live underlyings `https://api.nasdaq.com/api/quote/{SYM}/info?assetclass=etf|stocks`; risk-free proxy `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO` (2026-10-13: 4.26%). Yahoo Finance quote/options endpoints: attempted 2026-10-14, blocked (HTTP 401 / connection reset) — Nasdaq fallback used and labeled.

---

## 4. Open Quant/AI Model Lab

**Sweep:** arXiv API (q-fin PR/ST/MF/RM, 60 hits sorted by submittedDate + title-matched searches for implied volatility / option / volatility forecasting / earnings drift / dividend), GitHub repo search API (4 queries, created>2026-10-12), Semantic Scholar bulk API (429 twice → transient-exhausted; arXiv + GitHub covered the sweep, per 2026-10-08 precedent). Window Oct 13–14. Deduped vs all 66 existing ledger entries and the 2026-10-13 package. All scores from the repo's own `hedge_desk.research_intelligence.assess_source` on own evidence; bands TEST ≥ 65 / WATCH ≥ 45 / ARCHIVE < 45. **4 new candidates appended to the ledger as #67–70**, plus one pending promotion closed (#38). No INTEGRATE-ready candidates.

| # | Candidate | Type | Source URL | Score | Disposition | Reason |
|---|---|---|---|---|---|---|
| 67 | Yao/Chi/Gao — Structured SDEs for Realized GARCH: realized-measure feedback, 1-day-ahead integrated-variance forecasting | Preprint | https://arxiv.org/abs/2610.17732 | 60 | **WATCH** | Beats HAR/Realized GARCH OOS on 17 equity indices (source-reported, UNVERIFIED); no author code link → reproducibility not established |
| 68 | Wiese/Buehler/Horvath — GROMM: statically + dynamically arb-free European option market model (SANOS-based) | Preprint | https://arxiv.org/abs/2610.16732 | 60 | **WATCH** | SPX 2022–2025: fits within bid/ask for >95% of prices (source-reported, UNVERIFIED); no code → TEST stays closed despite strong author pedigree — band discipline, not name discipline |
| 69 | Bonacorsi — Certified Alpha Capacity: Statistical Arbitrage When Learning Takes Time | Preprint | https://arxiv.org/abs/2610.01115 | 48 | **WATCH** | Certification-frontier theory; validation time as a cost (complements #34 frozen-referee theme). No desk procedure to adopt; WATCH band floor |
| 70 | Itkin — GLE-LSV model with state-dependent leverage and colored noise | Preprint | https://arxiv.org/abs/2610.18706 | 39 | **ARCHIVE** | Pure LSV existence/uniqueness theory, no empirical results, no code. Below the 45 band; no desk transfer |
| 38 | lcx0731/implied-volatility-conditioning-lab — **promoted WATCH→TEST** | Repo | https://github.com/lcx0731/implied-volatility-conditioning-lab | 58→**73** | **TEST** | Pending scorer re-run closed on the 2026-10-10 sandbox evidence (59/59 pytest pass); repo unchanged since 2026-10-08, MIT verified. Caveat: synthetic-only by design — market-data validation still absent; TEST is sandbox, not integrate |

- No new TEST/INTEGRATE candidates this run. The day's two strongest papers (#67, #68) both sit at 60 WATCH — top of band, held there by missing code, not by lack of interest.
- Triage exclusions (no ledger rows): all GitHub hits NOLICENSE except imharshitrai/Option-Repository (MIT but NIFTY-50 scope); Nitmore/ML-Volatility-forecasting-options-research still NOLICENSE (repeat exclusion from 10-13); JoBi246/earnings-drift NOLICENSE + empty description; polytutor-ai Polymarket BTC bot (crypto + NOLICENSE); arXiv 2610.17231 (Buffett Effect — disclosure-premium event study, no desk transfer).
- No re-check status changes on standing WATCH items; #1/#20/#32 license line-stops untouched (re-verifying unchanged blockers adds nothing).
- Tool note (for future runs): arXiv/GitHub query strings must NOT go through `urlencode` — it escapes `+`/`OR` into literals and returns 0 hits. Use raw `+` with `%3A`/`%3E` for `:`/`>` in GitHub qualifiers.
- All material claims above labeled per evidence standards; paper findings are source-reported (abstracts read at source, full papers not read) → UNVERIFIED until replicated.

**Ledger:** ~/workspace/hedge-desk-research/quant-lab-ledger.md — rows #67–70 appended, #38 updated to 73/TEST, 2026-10-14 Jidoka entry added.

---

## 5. Weather/War/Logistics Futures Event Desk

**As-of ~1:27pm PT (16:27 ET) Oct 14. All prices Yahoo Finance front-month continuous contracts unless noted.**

| Event | Date/time | Headline fact | Futures-market read | Source |
|---|---|---|---|---|
| EIA Weekly Petroleum Status Report — **CORRECTION: NOT today** | **Thu Oct 15, 12:00pm ET** (Columbus Day shift) | EIA's own schedule moves the week-ending-Oct-9 report from the standard Wed 10:30am ET slot to Thu Oct 15, 12:00pm ET. **FACT** (primary source). The desk brief's "due today" premise is wrong; no fresh EIA inventory numbers exist yet this week. | No EIA-driven repricing today. Tomorrow's print is the next inventory catalyst — distillate stocks are the number to watch given the IEA diesel call below. | https://www.eia.gov/petroleum/supply/weekly/schedule.php |
| USDA Oct WASDE | Fri Oct 9, 12:00pm ET | **FACT** (corroborated across 4+ independent secondaries; USDA PDF not pulled directly): Corn yield raised +2.7 bu/ac to **181.2 bu/ac**; production **16.034B bu** (+234M vs Sep); 2026/27 ending stocks **1.849B bu** (+282M, vs ~1.677B trade avg); stocks-to-use 9.7% → 11.3%; season-avg farm price cut $0.10 to **$4.70/bu**. Soy: production **4.562B bu**, yield 53.1 bu/ac, ending stocks **315M bu** (+5M). Wheat: ending stocks **740M bu** (+23M), production 1.534B bu. World corn ending stocks 280.44 MMT. | Bearish corn: Dec corn fell ~20¢ on release day to ~$4.80 (8-week low per secondary). By today, front corn **$4.81** (ZC=F 481.0¢) is essentially flat vs the post-WASDE level — the selloff has stalled, not extended. Soy drifting lower: **$12.775** (ZS=F), down from $12.92 four sessions ago. Wheat **$6.735** (ZW=F), flat. **INFERENCE:** grain curve is digesting, not re-pricing further, pending harvest progress. | https://www.iowafarmbureau.com/Article/October-WASDE-Boosts-US-Corn-and-Soybean-Production-Estimates ; https://www.global-agriculture.com/global-agriculture/usdas-surprise-yield-hike-sends-corn-futures-to-an-eight-week-low/ |
| IEA Oil Market Report — diesel | Released Wed Oct 14 (today) | **FACT** (Reuters/AFP via secondaries): IEA says global diesel/gasoil balance "will remain tight well into 2027," dependent on Middle East product-supply recovery. Combined Middle East + Russia diesel-export losses **1.3M bpd in Sep** (~4.5% of global gasoil demand). Diesel refining margins hit record ~**$95/bbl** in Sep. IEA expects refinery recovery to produce a diesel surplus in Q1 2027 but says it will not offset the accumulated deficit; without Gulf supply normalization, "further demand reductions" may be needed. IEA members coordinating ~100M bbl emergency oil/diesel release (per Reuters). Global oil demand forecast **−2.6M bpd in 2026**, 25% from diesel. | Heating oil (diesel proxy) **$4.9382/gal** (HO=F), up from $4.738 four sessions ago (+4.2%) — market is pricing the diesel squeeze. Gasoline is diverging: RBOB **$3.1407/gal**, down from $3.295 four sessions ago (−4.7%). **INFERENCE:** the distillate/gasoline crack split corroborates a diesel-specific, not general-petroleum, tightness story. | https://www.tbsnews.net/world/global-economy/diesel-supplies-remain-tight-2027-iea-1572726 ; https://wixx.com/2026/10/14/diesel-shortages-could-persist-well-into-2027-iea-says/ |
| Houthi attacks on Saudi targets / Saudi Aramco building hit | Ongoing; attack reported Wed Oct 14 | **FACT** (OPIS via Morningstar, ~12:41pm ET today; corroborated by SP Angel, BusinessLine): Saudi Energy Ministry said a building belonging to Saudi Aramco was attacked; continuing Houthi missile/drone attacks on Saudi Arabia keeping Middle East tensions at forefront. | WTI Nov **~$95.40** at noon ET (+$1.25), Dec WTI **~$94.20** (+$1.00); Brent Dec **~$106.20** (+$0.50), Jan Brent **~$103.65** (+$0.75). Yahoo front-month at 1:27pm PT: WTI **$95.14**, Brent **$106.03**. **INFERENCE:** Dec→Jan Brent −$2.55 and Nov→Dec WTI −$1.20 = backwardation, consistent with near-term physical tightness / war-risk premium rather than a demand-boom curve. Fourth straight up session for both benchmarks per OPIS. | https://www.morningstar.com/news/dow-jones/202610146401/nymex-overview-oil-rises-on-saudi-aramco-attack-iea-report-opis ; https://www.thehindubusinessline.com/markets/commodities/brent-crude-rises-above-106-as-houthis-intensify-attacks-on-saudi-targets/article71582244.ece |
| Shipping / chokepoints (Hormuz, Red Sea, Black Sea) | Ongoing, background | **FACT** (TI Insight Oct risk monitor; Maersk Oct update): Strait of Hormuz closed to shippers since war broke out Feb 28; East-West pipeline attack removed a Hormuz-bypass route (repairs est. 3–5 weeks); Black Sea commercial-vessel attacks escalated Sep–Oct (incl. sinkings off Romania/Bulgaria). Maersk (Oct 13) says Middle East disruption continues to shape IMEA routing/transit times. Container spot rates softening despite this: Drewry WCI $4,434/40ft (−0.8%), Asia–Europe rates down >60% since July (SAAFF/BUSA via Africa Ports). | No direct futures read today. **INFERENCE:** freight is a two-track market — tanker/war-risk costs elevated while container rates fall on overcapacity. For grain, Black Sea risk is a latent wheat upside tail, not a current price driver (wheat flat post-WASDE). | https://ti-insight.com/briefs/global-supply-chain-risk-monitor-october-2026/ ; https://www.maersk.com/news/articles/2026/10/13/india-middle-east-and-africa-market-update-october |
| US Sep CPI energy pass-through (context, not a futures catalyst) | Released Wed Oct 14 | **FACT** (USA Today/BLS via secondary): Gasoline +9.1% MoM in Sep, +34.2% YoY; national avg regular $4.33/gal (AAA); diesel ~$6.30/gal. | Context for the diesel squeeze's macro bite; not a curve signal. | https://www.usatoday.com/story/money/economy/inflation-cost-of-living/2026/10/14/september-2026-cpi-report-inflation-prices/92214458007/ |

**Futures snapshot (Yahoo, ~1:27pm PT Oct 14):** WTI CL=F **$95.14** (4 sessions ago $91.85, +3.6%) · Brent BZ=F **$106.03** ($104.72 → +1.3%) · NatGas NG=F **$3.259** (flat) · Heating oil HO=F **$4.9382** (+4.2% over 4 sessions) · RBOB RB=F **$3.1407** (−4.7%) · Corn ZC=F **$4.81** · Soy ZS=F **$12.775** · Wheat ZW=F **$6.735**. Attempted individual-expiry Yahoo pulls (CLX26, CLZ26, ZCZ26, etc.) returned no data — curve shape above uses OPIS noon-ET Nov/Dec/Jan points instead. Brent–WTI front spread ~**$10.89**.

- **INFERENCE:** Diesel is the energy story; crude is the passenger. IEA's "tight well into 2027" diesel call + record $95/bbl Sep diesel margins + HO outperforming RBOB by ~9pp over four sessions all point one way. *What would change it:* a Thu EIA print showing a large distillate build, or a confirmed Gulf refinery/export restart.
- **FACT:** No EIA catalyst today — tomorrow at noon ET is the next inventory event. Any "EIA reaction" framing for today's tape is wrong; today's oil move is geopolitics + IEA. *What would change it:* nothing — the schedule is primary-source.
- **INFERENCE:** WASDE's corn shock is absorbed, not accelerating. Corn sits at its post-report level five days later; the 11.3% stocks-to-use reset is priced. *What would change it:* November WASDE revising the 181.2 bu/ac yield against actual harvest results, or harvest delays tightening basis.
- **INFERENCE:** Geopolitical risk premium is live and front-loaded. Backwardation (near > far) plus a 4-session WTI rally on Aramco/Houthi headlines = market paying for prompt barrels. *What would change it:* a ceasefire/de-escalation signal or restored Gulf exports — either would likely collapse the near premium faster than the far curve.

**Gaps / UNVERIFIED:** USDA WASDE figures from usda.gov directly (secondary corroboration is strong and mutually consistent, but the primary PDF was not pulled) — do not treat as primary-verified. Proposed US port fees on Chinese-built ships reportedly effective Oct 14 — single stale-dated source, not corroborated; excluded from verdicts. Government-data rule holds: no shutdown framing used; EIA delay is a published Columbus Day holiday shift, not a funding disruption.

---

## 6. Box/Parity Observer

**Verdict: Nothing material — no new parity-violation analysis or index-methodology change relevant to the watchlist found today.**

- **FACT (secondary source):** A recent option-implied-distribution check (MQL5, updated ~7 days ago) reported SPY with no monotonicity, convexity, or bound violations and the tightest parity agreement of the four underlyings tested — i.e., no SPY parity violation evidenced there. No new published parity-violation analysis specific to QQQ, AAPL, MSFT, NVDA, or TSLA surfaced. Source: https://www.mql5.com/en/articles/24246
- **FACT:** No new S&P 500 methodology change found. The S&P DJI MegaCap consultation concluded with no changes to S&P 500 eligibility criteria or methodology. Source: https://www.morningstar.com/news/pr-newswire/20260604ny76716/sp-dow-jones-indices-consultation-on-treatment-of-megacap-companies-results
- **FACT (not watchlist-relevant):** S&P announced Sept 11, 2026 that foreign-domiciled companies may join S&P/TSX indexes effective at the Dec 21, 2026 rebalance. This affects Canadian indexes only, not SPY/QQQ or the watchlist. Source: https://www.ainvest.com/news/index-rule-change-matters-2609/
- **FACT (not new):** The most recent Nasdaq-100 methodology overhaul took effect May 1, 2026 (Fast Entry, low-float weighting cap at 3× float, quarterly membership reviews). No newer October 2026 methodology doc found. Source: https://indexes.nasdaq.com/docs/Nasdaq-100_Index_Consultation_February_2026_Summary_of_Responses_and_Conclusion.pdf
- **FACT:** No new watchlist-specific dividend-arbitrage or early-exercise anomaly published. Recent items found were general education (early-exercise rule: ITM short call with extrinsic value below the coming dividend invites assignment) and non-watchlist examples (UNP, TPG). Source (general rule): https://www.theoptionpremium.com/p/dividend-aristocrats-portfolio-poor-mans-covered-call-strategy

**INFERENCE:** No parity-based edge or methodology-driven distortion to price into the watchlist today. Deterministic put-call/box parity stands as the check on any model output; nothing found today contradicts it. *What would change this verdict:* a new S&P DJI or Nasdaq index notice affecting SPY/QQQ constituents, or a published parity/box-spread violation study on a watchlist name.

---

## 7. Bonds & Rates Desk

**Source:** repo's own `rates_desk.rates_environment()` module, mode `REAL_FRED_RATES`, run 2026-10-14 ~1:30pm PT. All numbers below are from that module output — none retyped from memory. Series latest date is 2026-10-13 (FRED daily series post with a one-day lag) — FACT.

| Metric | Value | As-of |
|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-13 |
| Fed funds change over 60-day window | +0.25 pp (per module) | 2026-08-17 → 2026-10-13 |
| Treasury 2Y (DGS2) | 4.79% | 2026-10-13 |
| Treasury 10Y (DGS10) | 5.21% | 2026-10-13 |
| 2s10s spread | +42 bp | 2026-10-13 |
| Curve shape | UPWARD_SLOPING | 2026-10-13 |
| SOFR | 3.89% | 2026-10-13 |
| EFFR | 3.88% | 2026-10-13 |
| OBFR | 3.88% | 2026-10-13 |
| SOFR − EFFR spread | +1 bp | 2026-10-13 |

- **FACT (from module histories):** Curve is upward-sloping but has flattened over the window. 2s10s was +53 bp at the window start (2026-08-17: 10Y 4.72% − 2Y 4.19%) and is +42 bp now; the latest session also narrowed (44 bp on 10-09 → 42 bp on 10-13). This is a bear-flattening pattern: over 60 days the 2Y rose ~60 bp (4.19% → 4.79%) while the 10Y rose ~49 bp (4.72% → 5.21%) — the front end led. *What would change it:* 2s10s turning negative (inversion) or widening back above ~55 bp.
- **FACT:** No funding stress. SOFR (3.89%) sits 1 bp above EFFR (3.88%), with OBFR also at 3.88%. *What would change it:* SOFR−EFFR widening to >10 bp sustained across several sessions. Direction of the SOFR−EFFR spread change is UNVERIFIED — the module reports no SOFR/EFFR history.
- **INFERENCE:** Rates backdrop is a headwind for long-duration/growth multiples. The 10Y at 5.21%, up ~49 bp in 60 days, means higher discount rates applied to distant cash flows, pressuring growth-multiple valuations. *What would change it:* a sustained 10Y retracement toward ~4.7% (window-start level) or evidence the rise is driven by real-growth expectations rather than term premium (not distinguishable from this module's output alone).
- **INFERENCE:** Premium-pricing read. Higher long rates raise call premiums modestly via rho, but the dominant channel for premium sellers/buyers is the equity-multiple pressure above plus the flattening curve (less steepening tailwind for financials' carry). No curve-inversion recession signal is present in this data. *What would change it:* curve inversion, or a sharp 10Y reversal that re-rates growth multiples upward.

**Desk status: SUCCEEDED.** No fallback used; no Yahoo yields substituted.

---

## Desk status

| Desk | Status |
|---|---|
| 1. Earnings Event | SUCCEEDED |
| 2. Dividend Opportunity | SUCCEEDED |
| 3. Overnight Premium (IV) | SUCCEEDED (Nasdaq fallback for live chains; Yahoo blocked 401/reset; IV-rank UNVERIFIED) |
| 4. Open Quant/AI Model Lab | SUCCEEDED (4 new candidates #67–70 appended to ledger; #38 promoted to TEST) |
| 5. Futures Event | SUCCEEDED |
| 6. Box/Parity Observer | SUCCEEDED (nothing material) |
| 7. Bonds & Rates | SUCCEEDED (module output) |

No desk FAILED. No retry needed.
