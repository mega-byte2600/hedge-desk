# Hedge-Desk Daily Research Package — Sunday 2026-10-25

**Run:** 13:30 PT (16:30 ET — markets closed; all market closes below are Friday 2026-10-23 closes, not live Sunday quotes).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Standing:** paper-only research. No Risk of Ruin work, no trade authorization, no synthetic data. Every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**Desk status:** all 7 desks delivered. No desk FAILED. Two cross-desk conflicts are flagged unresolved below (MSFT implied move; Hormuz flow readings) — they are surfaced, not smoothed over.

---

## 1. Earnings Event desk — delivered

**Window:** Oct 25 – Nov 8, 2026. SPY/QQQ are ETFs with no earnings (FACT — structure).

| Ticker | Event | Timing | Options-implied expected move | Historical avg earnings-day move |
|---|---|---|---|---|
| MSFT — Q1 FY27 | Wed, Oct 28, 2026 | After close; webcast 2:30 p.m. PT / 5:30 p.m. ET | **UNRESOLVED RANGE 5.3% – 7.6%** — see conflict note | UNVERIFIED |
| AAPL — Q4 FY26 | Mon, Nov 2, 2026 | Release 1:30 p.m. PT; call 2:00 p.m. PT / 5:00 p.m. ET | **~4.8–5.0%** (convergent secondary reads) | UNVERIFIED |
| TSLA | Already reported — Wed, Oct 21, 2026, after close | — | — | Single datapoint only (see below) |
| NVDA | Outside window — date NOT company-confirmed | After close (expected) | — | — |

**Evidence / labels:**
- MSFT date + after-close timing: FACT — Microsoft's own Oct 7, 2026 release, independently confirmed this run by a direct Nasdaq earnings-calendar API pull (consensus EPS $4.71, 14 estimates, vs $4.13 last year). Revenue ~$90.62B is secondary-source consensus, not company guidance.
- AAPL date + times: FACT-grade via corroboration — Apple's Investor Relations calendar as reported identically by MacRumors, iClarified, Appleosophy, and MacObserver (Oct 6–7, 2026), confirmed this run by Nasdaq API (consensus EPS $2.00, 8 estimates, vs $1.85 last year; MarketBeat shows $1.99 — a $0.01 estimate-count difference, not an error to resolve by guessing). Secondary reports say the call is the first led by CEO John Ternus — a qualitative uncertainty layer beyond the numbers. Prior guide cited: +9–11% revenue growth.
- **MSFT implied-move conflict (UNRESOLVED — read before using either number):** yesterday's package recomputed an Oct 30-expiry ATM straddle from the Oct 23 close chain at **5.28%** ($27.68 straddle ÷ $524.51). Today's desk did not recompute a straddle; its sourced reads are **±7.57%** (MetisTrades, Oct 18 chain, ATM-straddle method) and a TipRanks/Cboe "50% probability of a move greater than 7.52%" — a probability-threshold metric, NOT a straddle, which must not be conflated with the 7.57%. The two straddle reads differ by date (Oct 18 vs Oct 23 chain) and possibly by strike/expiry selection; neither desk reconciled them. The fresher own-calculation (5.3%) is the more recent market read, but it is yesterday's, not today's. **No single MSFT implied-move figure is asserted this run.** What settles it: a fresh ATM-straddle recomputation from Monday's live chain.
- AAPL implied move: convergent — Investor's Business Daily (Oct 23–24) 4.8% either direction (Nov 4 expiry ATM put+call); TipRanks ±5.02% ($17.05). Today's desk did not independently recompute; these are sourced reads, not an own calculation. Consistent with yesterday's own 4.85% recomputation.
- Historical average earnings-day moves for MSFT/AAPL: UNVERIFIED — the only figures found are single-secondary-source claims (MSFT last-8 avg ~7.0% absolute; AAPL last-8 avg ~2.5% absolute), read only as search-result descriptions, not verified price history. Do not publish them as verified history.
- NVDA: FACT that the date is unconfirmed — CMEG (data current Oct 21): "Nvidia has not yet confirmed" its fiscal Q3 2027 date; trackers list Nov 17, 18, and 25. **The IV-inputs file's "NVDA 2026-11-18" is an estimate only — do not copy it as confirmed.** Company guidance cited secondhand: revenue $108.0B ±2%, gross margin 74.0% ±50bp.
- TSLA: FACT — Q3 2026 reported Wed Oct 21, 2026, after close (Tesla IR table); public reports actual EPS $0.48 vs $0.40 estimate. Next date disputed (Jan 27 vs Feb 3, 2027) — UNVERIFIED and outside this window. (Correction: the Premium desk's "last reported Oct 22" is a one-day slip; Oct 21 is the reported date.)

**CFA note:** neither in-window release exists yet, so no statement teardown is possible today. At release time, apply the reading order: guidance vs. consensus first, then GAAP income statement (vs. headline adjusted figure), cash flow (OCF vs. net income, capex, buybacks vs. issuance), segment margins, balance-sheet deltas, call transcript last.

**Sources:** https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; https://www.macrumors.com/guide/earnings/ ; https://www.mactrast.com/2026/10/apple-to-announce-fiscal-q4-2026-earnings-on-november-2/ ; https://www.metistrades.com/blog/options-analysis/msft-18oct2026 ; https://www.tipranks.com/news/the-fly/cboe-data-shows-mixed-options-sentiment-in-microsoft-with-shares-up-0-84-thefly-news ; https://www.investors.com/research/options/apple-stock-aapl-tech-options-income-trading-markets-investing/ ; https://www.cmelitegroup.com/knowledge-hub/nvidia-earnings-date/ ; Nasdaq earnings-calendar API (api.nasdaq.com/api/calendar/earnings?date=2026-10-28 and ?date=2026-11-02, pulled this run).

**Decision-relevant:**
1. **[FACT]** MSFT Oct 28 AMC is the week's binary event — and it lands on FOMC decision day (INFERENCE from calendar overlap: do not attribute the Oct 28–30 move to earnings alone; macro + earnings vol share the session).
2. **[FACT]** AAPL Nov 2 AMC is the second binary event — ~4.8–5.0% implied, the convergent read.
3. **[UNRESOLVED]** MSFT's implied move is 5.3% on the fresher own-calculation vs 7.6% on the sourced Oct 18 read — do not anchor on either until Monday's chain is recomputed.

**What would change it:** a company-issued date change, a fresh Monday straddle recomputation settling the MSFT range, or a verified historical earnings-move series replacing the UNVERIFIED marks.

---

## 2. Dividend Opportunity desk — delivered

**Window:** ex-dates Oct 25 – Nov 22, 2026.

| Symbol | Ex-date | Amount | Pay date | Status |
|---|---|---|---|---|
| MSFT | **2026-11-19** | **$0.98/qtr** | 2026-12-10 | FACT — declared, INCREASE |
| AAPL | Early–mid Nov (projection only; TalkMarkets lists Nov 10) | $0.27 expected, unchanged | — | UNDECLARED — projection, not FACT |
| SPY | none in window | — | — | Next ex ~2026-12-18, outside window |
| QQQ | none in window | — | — | Next ex ~2026-12-21, outside window |
| NVDA | none in window | — | — | Next ex ~2026-12-04 (projected), outside window |
| TSLA | none — pays no dividend | — | — | FACT |

**MSFT — the one declared event in window [FACT].** Board declared $0.98/qtr on Sep 15, 2026 (+$0.07, +8% over $0.91); ex Nov 19, 2026, pay Dec 10, 2026. Consecutive-increase count: **24 consecutive annual increases (incl. the Sep 2026 raise)**, per the standing standard in `~/workspace/hedge-desk-research/dividend-count-standard.md`. (Zacks shows the announcement as Sep 14 — a one-day press-timing difference, immaterial.) No cut or special announced.

**AAPL — expected in window, NOT declared [UNVERIFIED as to date/amount].** Zacks' AAPL page states Apple "does not have any future dividends declared," and a dividend calendar updated Oct 22, 2026 likewise shows no upcoming Apple dividend. The most recent declared dividend is the Jul 30, 2026 declaration of $0.27, ex Aug 10, paid Aug 13, 2026. TalkMarkets (Oct 25) lists AAPL Nov 10 at $0.27 — treated as a projection, not a declaration. Pattern supports it [INFERENCE]: November ex-dates ran Nov 10, 2023, Nov 8, 2024, and Nov 10, 2025, and raises historically arrive with the May payment, so the expected amount is $0.27 unchanged — but until declared, treat date and amount as UNVERIFIED, not FACT. Yesterday's DividendMax-based ~Nov 9 forecast and today's Nov 10 listing bracket the same early–mid-November projection window; neither is a declaration.
**AAPL consecutive-increase count — deliberately UNVERIFIED:** third-party streak labels conflict (Light Horse: "4 years"; StockAnalysis: "14 growth years"), and the standard forbids copying a count without issuer-history verification. The 2026 increase itself is FACT (announced Apr 30, 2026, $0.26 → $0.27).

**SPY [FACT on last distribution]:** last ex 2026-09-18, $1.888834, paid Oct 30, 2026. Next ex ~2026-12-18, amount undeclared (Wall Street Horizon / TipRanks estimates). One flag: Wall Street Horizon also lists a SPY 12/31/2026 "XOTH" entry — type and amount undeclared, UNVERIFIED.
**QQQ [FACT on last distribution]:** last ex 09/21/2026, $0.7514, paid 10/08/2026. Next ex ~2026-12-21, amount undeclared.
**NVDA [FACT on history; next date/amount UNVERIFIED]:** last ex 09/10/2026, $0.25, paid 10/01/2026 — the May 18, 2026 increase ($0.01 → $0.25) is FACT. Next dividend not yet declared (Finbold/TokenPost explicit); Dec 4, 2026 ex-date is a Nasdaq-listing projection, outside the window either way.
**TSLA [FACT]:** no dividend — never paid a cash dividend on common stock.

**Cuts / specials:** none announced for any watchlist name in the sources checked. This is a checked-negative, not an issuer filing review.

**Sources:** https://www.zacks.com/stock/research/MSFT/dividend-history ; https://www.ad-hoc-news.de/boerse/news/corporate-news/microsoft-stock-carries-a-higher-98-cent-dividend/70224760 ; https://www.zacks.com/stock/research/AAPL/dividend-history ; https://talkmarkets.com/article/stocks-going-ex-dividend-in-november-2026 ; https://www.wallstreethorizon.com/spy-dividend-calendar ; https://wallstreethorizon.com/qqq-dividend-calendar ; https://www.lighthorse.io/tickers/nvda/dividends ; https://finbold.com/heres-how-much-100-nvda-shares-will-earn-from-nvidias-q4-2026-dividend-payout/

**Decision-relevant:**
1. **[FACT]** MSFT ex-div Nov 19 at the raised $0.98 is the only declared watchlist ex-date in the next 4 weeks — the ~$0.98 mechanical ex-date adjustment is the only dividend event to plan around.
2. **[UNVERIFIED]** AAPL's November dividend is still undeclared — the early–mid-November projection converts to FACT only on the declaration expected alongside earnings (Nov 2). Do not price an AAPL ex-date as certain yet.
3. **[FACT]** No dividend-driven ex-date cluster otherwise — SPY, QQQ, and NVDA all next go ex in December, and TSLA pays nothing.

**What would change it:** an AAPL declaration (expected ~Nov 2) adding a second in-window ex-date, or any issuer announcing a cut/special before Nov 22.

---

## 3. Overnight Premium desk (IV) — delivered

### IV-inputs freshness guard — PASS (within 26h guard, not STALE)
- Latest file: `~/workspace/hedge-desk-research/nightly/2026-10-24-iv-inputs.json`, **as_of 2026-10-24T13:54:04−07:00** (~23.5h old at this run's 13:26 PT start — inside the 26h guard).
- **Caveat: this is YESTERDAY'S post-close data, not today's.** Realized-20d and window-contingent figures below come from this file; IV levels are reported per-source, never blended.
- **Live supplement (labeled):** fresh Yahoo v7 options pull this run via cookie+crumb handshake. Quotes are **Friday 2026-10-23 close** — markets are closed Sunday, so these are Friday-close marks, not live executable quotes.
- **Cross-source level discrepancy (flagged, unresolved):** today's live pull gives higher front-expiry ATM IVs than both the file and yesterday's live pull for every symbol (e.g. SPY 13.6% today vs 11.1% in the file and in yesterday's live pull; NVDA 36.2% vs 29.6%). Same Oct 26 expiry, markets closed in between — this is a methodology/extraction difference between pulls, not a vol move. Levels below are reported per-source; **do not blend them and do not compare today's live levels against yesterday's live levels as if they were one series.** Term-structure shape (upward slope, Nov 20 humps) agrees across pulls and is the robust read.

### Snapshot table (realized window 2026-09-28 → 10-23, from the file; IV levels per source)

| Symbol | Fri close | ATM IV, Oct 26 expiry — file | ATM IV, Oct 26 / Nov 20 — live Yahoo today | 20d realized | Window-contingent? | Earnings in window |
|---|---|---|---|---|---|---|
| SPY | 759.97 | 11.1% | 13.6% / 16.0% | 9.7% | No (20.9%) | — |
| QQQ | 704.40 | 19.5% | 23.9% / 25.8% | 18.8% | **YES (32.0%)** | — |
| AAPL | 347.73 | 16.4% | 20.1% / 28.4% | 16.6% | **YES (36.4%)** | 2026-11-02 (in Nov 20 window) |
| MSFT | 524.51 | 18.5% | 22.7% / 34.5% | 19.5% | No (20.1%) | 2026-10-28 (in Nov 20 window) |
| NVDA | 210.96 | 29.6% | 36.2% / 45.1% | 29.4% | **YES (31.0%)** | 2026-11-18 est. (in Nov 20 window; date unconfirmed) |
| TSLA | 372.22 | 29.7% | 36.4% / 40.8% | 34.0% | No (24.8%) | None upcoming |

**IV rank for all six names: UNVERIFIED** — no IV history available from free sources; no "elevated IV rank" claim is made.

### Findings (labeled)
- **Term structure slopes up everywhere (front < back) — INFERENCE from both pulls:** no front-month hump at Oct 26, because no watchlist earnings fall inside that expiry. The humps sit in the Nov 20 expiry, which contains MSFT (Oct 28), AAPL (Nov 2), and NVDA (Nov 18 est.). Elevated back-month IV for those three names is **expected event pricing, not "rich" premium** (CFA sanity check).
- **MSFT — premium into a binary event:** Nov 20 IV 34.5% vs 22.7% front (live pull). The event premium is in the back expiry, not the Oct 26 weekly — any premium stance spanning Oct 28 must price the crush, not the front IV. The front Oct 26 expiry is the only earnings-free MSFT point, and it expires before the event.
- **Stale-jump screen (standing rule):** QQQ (32.0%), AAPL (36.4%), and NVDA (31.0%) are **WINDOW-CONTINGENT** — any IV-vs-realized verdict for them is WINDOW-CONTINGENT, not clean. NVDA crossed the 30% line since yesterday's 29.9% reading on the rolled window — a window change, not a data contradiction. SPY, MSFT, TSLA windows are not contingent.
- **Clean-window reads (INFERENCE, per-source levels — direction only, given the level discrepancy):** SPY front IV above trailing realized (mild richness); MSFT front IV below realized (mild cheapness); TSLA front IV below trailing realized (−4.3pp on file levels; the cheapest vs recent realized on the board, backward-looking only). QQQ/AAPL/NVDA near-parity readings carry no clean verdict.
- **Parity check:** Yahoo's quoted same-strike call vs put IVs diverge materially at ATM (e.g. SPY Oct 26: call 15.0% vs put 12.1%). Under deterministic put-call parity with common rate/dividend inputs these should match, so the gap reflects Yahoo's IV-calculation assumptions (or stale legs), **not** an arbitrage signal — the math wins over the quoted field. No parity violation is claimed from Friday-close marks with closing spreads.

**Decision-relevant:**
1. **[FACT]** MSFT Oct 28 earnings sits in the Nov 20 expiry (34.5% vs 22.7% front, live pull) — premium into the binary event lives in the back expiry; do not read front IV as the event price.
2. **[FACT]** QQQ, AAPL, and NVDA realized windows are WINDOW-CONTINGENT (32.0%, 36.4%, 31.0%) — no clean IV-vs-realized verdict for any of the three; NVDA newly crossed the line on the window roll.
3. **[UNVERIFIED]** IV rank is UNVERIFIED for all six names (no free IV history) — no "elevated IV rank" flag is issued this run; the desk reports IV *levels* and term structure only. **[UNRESOLVED]** Today's live IV levels run systematically above yesterday's live levels for the same expiry and closes — treat cross-day level comparisons as unreliable until the extraction difference is identified.

---

## 4. Open Quant/AI Model Lab — delivered

**Window status (FACT):** arXiv legs return newest items dated 22 Oct 2026 — Sunday, no new announcements until Monday, so the window is genuinely empty, not a leg failure (per the 2026-10-17 weekend rule). GitHub search + direct `/repos/` endpoints healthy all run (no 403s). All 4 candidates below were scored by running the repo scorer (`hedge_desk.research_intelligence.assess_source`) — no hand-scoring. All 4 appended to the ledger as #148–151; verified on disk after append.

| # | Candidate | Score | Disposition | Reason |
|---|---|---|---|---|
| 148 | Onger/Foscari — "Equilibria and Learning in Competitive Market Making" — arXiv:2610.30891v1, 22 Oct 2026 | 28 | ARCHIVE | Pure-strategy Nash equilibria for N strategic market makers; equilibrium spread widens with asset-value volatility (source-reported, simulations only). Game theory, no desk procedure; no code link. Catch-up: missed by the 2026-10-24 sweep. |
| 149 | Mohl et al. — "Understanding the Inner Workings of a State-Space Foundation Model for LOBs" (Oxford) — arXiv:2610.28753v1, 20 Oct 2026 | 39 | ARCHIVE | 8.2M-param Mamba-3 model on LOB message streams of 8 large-cap US equities; order-flow imbalance decodable at R² ≈ 0.59, generalizes to unseen stocks (source-reported, UNVERIFIED). Accepted at ICAIF '26 per the paper's own comment line — peer-review signal noted, but no code link → still ARCHIVE (even credibility 4 scores 44, below the 45 WATCH band). Catch-up: missed by the 2026-10-24 sweep. |
| 150 | **Yajrzyna/spy-atm-iv-forecasting** — GitHub, created 2026-10-24, MIT, 0 stars | 46 | **WATCH** | MSc thesis code forecasting short-horizon SPY ATM IV (OptionsDX 30-min chains 2017–2023, 54.8k ATM rows, 1–7 DTE; chronological train/val/test). Test-2023 OOS R² (source-reported, code NOT run): OLS 0.192, stacking 0.177, LSTM 0.172, MLP 0.060 — all beat random walk, simple OLS best; skill strongest 1–2 DTE, weakest when VIX low. **BLOCKER: OptionsDX data licensed and NOT included — headline results not reproducible from the repo alone** (tests/figures run data-free). Honest framing helps: documented vega-unit 100× correction, and the vega-only Sharpe explicitly disclaimed as ignoring theta/hedging/exit costs. |
| 151 | **h-a-forster/surfbench** — GitHub, created 2026-10-24, MIT, 2 stars | 54 | **WATCH** | Benchmark of arbitrage-free IV surface fits (raw SVI, SSVI, eSSVI, SABR + quadratic baseline) under one shared objective and pre-registered quote filter, scored on held-out accuracy (5-fold CV IV error, in-spread share, outermost-quote holdout), next-snapshot error vs quote persistence, and static arbitrage (Durrleman g(k), monotonicity/convexity, calendar variance), with bootstrap CIs and Holm-adjusted sign-flip tests. Pipeline complete and tested, 24-month synthetic validation run end-to-end — **but the Deribit market-data study is PENDING on Tardis.dev free quota, so no real-market results exist yet.** Crypto-data scope, but the scorecard methodology transfers directly to the premium desk's surface-fit choice (#18 vs #128 vs #146). |

**Source URLs:** https://arxiv.org/abs/2610.30891, https://arxiv.org/abs/2610.28753, https://github.com/Yajrzyna/spy-atm-iv-forecasting, https://github.com/h-a-forster/surfbench. Ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#148–151).

**Triage exclusions (no ledger rows):** Belotti03/svi-volatility-surface-digital-pricing (NOLICENSE, README-only stub, no code); scenario7/volatility-forecasting (NOLICENSE, no README); SOUP0821/options-desk (NOLICENSE, textbook BS pricer, crowded lane); sophiezxh/volatility-signals (NOLICENSE, CMU vol-selling framing — VIX/VIX3M > 1 stress filter noted as a method idea only); themiya2003/financial-time-series-comb-volatility (empty repo); FX/forensics/crypto scope hits.

**Most decision-relevant:**
1. **[FACT]** Two new WATCH items, both premium-desk-relevant: #151's held-out + next-snapshot + arbitrage-violation scorecard is directly portable to the desk's SPY surface-fit choice (#18/#128/#146); #150's OLS-beats-LSTM SPY ATM-IV result is interesting but blocked on licensed data.
2. **[FACT]** Nothing new reached TEST or INTEGRATE (scorer max 54). No re-checks repeated this run.
3. **[FACT]** The 2026-10-24 sweep missed two in-window arXiv items (#148, #149) — caught this run. A sweep-coverage gap worth noting for the next weekend run, not a data error.

---

## 5. Futures Event desk (Weather/War/Logistics) — delivered

**Scope note:** Sunday — latest closes are Friday Oct 23. No new federal release is due this weekend; all federal releases below are on their normal schedule (no shutdown framing — CR funding through Dec 11, per standing rule). Nothing found contradicts the on-schedule state.

### Fresh catalysts and what futures are pricing

| Catalyst | Facts (labeled) | Read |
|---|---|---|
| **Gulf / Saudi attacks — crude spike** | **FACT:** Brent settled Fri Oct 23 at $116.72/bbl, +$3.55 (+3.14%), highest close since Apr 29; WTI settled at $103.27, +$3.80 (+3.8%). Brent +~6% on the week (4th straight weekly gain), WTI +~2.3%. Brent–WTI spread = $13.45 (arithmetic). **FACT:** Houthi strikes hit Saudi targets incl. energy sites/airports Thu–Fri Oct 22–23; Saudi Aramco evacuated Dhahran HQ staff Thu; a tanker was struck near Oman Wed (UKMTO); State Dept ordered non-essential US personnel out of the kingdom. An Iranian claim of seven tankers hit is circulating — **UNVERIFIED, do not rely on it.** | Market is pricing a geopolitical risk premium, not a confirmed physical shortfall — see inference below. |
| **Physical flows vs. price — UNRESOLVED CONFLICT** | **CONFLICT (see below):** yesterday's package reported Middle East crude exports through Hormuz/alternative routes averaged >24M b/d in the week through Oct 18, above the pre-war 23.3M b/d (Kpler, via OPIS/Dow Jones), with Saudi saying production was unaffected. Today's desk reports Hormuz "effectively closed to normal traffic," ~13 tankers/day transiting vs ~100/day pre-crisis (Kpler via GlobalOilShock, Sep data), and 27 merchant-fleet attacks in October as of Oct 22. These readings cannot both describe the same flow measure — they differ in metric (barrels via alternative routes vs tanker counts), date (week through Oct 18 vs September/October counts), and sourcing chain. **No resolution is asserted: do not cite either flow figure as settled until a primary Kpler/OPIS read reconciles them.** What is agreed: futures surged while at least some physical measures did not collapse — consistent with a fear/insurance premium (record Persian Gulf freight rates per ING; US Gulf→Asia supertanker ~$60M now vs ~$6M pre-war, ~10×). | Do not read $116 Brent as evidence of a current supply deficit. The premium can unwind as fast as it built. |
| **EIA Weekly Petroleum Status Report (week ended Oct 16, released Wed Oct 21)** | **FACT:** Commercial crude −3.06–3.1M bbl to 412.5M bbl, ~3% below the 5-yr average, third straight weekly draw. Gasoline −3.0M bbl to 205.3M bbl (~5% below average). Distillates +1.7M bbl to 104.3M bbl (build vs expected draw — the bearish wrinkle). Cushing +0.99M bbl to 27.6M bbl. Refinery utilization 93.4%. US production 13.269M b/d, −410k b/d w/w on lingering Gulf (Hurricane Isaias) effects. SPR −0.3M bbl to 282.7M bbl, lowest since 1982 (yesterday's package). | Tight crude/gasoline, but the distillate build undercuts the simplest "everything tight" bull case. |
| **DOE emergency SPR action** | **FACT (from yesterday's package, not re-verified this run):** DOE authorized an emergency exchange of up to 400k bbl from the SPR for Phillips 66's Lake Charles refinery; Germany's EBV also tendered strategic volumes — its first such release since the early-October G7 coordinated-release agreement. Policy response is targeted (refinery-specific), not a broad SPR flood — so far. | — |
| **EIA Natural Gas Storage (week ended Oct 16, released Thu Oct 22, 10:30 ET)** | **FACT:** +77 Bcf injection to 3,644 Bcf — below the 83 Bcf consensus, 152 Bcf (−4%) below year-ago, but +35 Bcf (+1%) above the 2021–2025 average. The 5-yr-average surplus has shrunk from ~148 Bcf (early Sep) to ~1%. EIA's October STEO path (3,850 Bcf end-Oct) now looks hard to reach — recent builds imply ~3,780 Bcf instead. **FACT:** Henry Hub front-month ~$2.64/MMBtu (−16¢ Fri, ~−50¢ on the week); Winter 2026-27 strip at a fresh 5-yr low of $2.97; Summer 2027 at 5-yr low $2.78. Curve shape: **contango**. Europe TTF ~€88–93.85, highest since Dec 2022 — a ~$23+/MMBtu transatlantic gap US prices cannot capture because LNG feedgas is maxed out (record ~18.9–20.7 Bcf/d). | Gas enters withdrawal season near-normal nationally with a South Central deficit — weather, not storage or war, is the swing factor now. US gas is a weather trade, not a war trade, until forecasts turn cold. |
| **USDA Oct WASDE (Fri Oct 9, 12:00 ET)** | **FACT:** Corn yield raised to 181.2 bu/acre, production 16.034B bu, ending stocks 1.849B bu (+282M vs Sep, above the 1.677B trade average); soybeans record 53.1 bu/acre, 4.562B bu, stocks 315M bu; wheat production 1.534B bu (smallest since 1970), stocks 740M bu (+23M). Futures fell on the report — corn ~5%, soybeans ~2%, wheat ~3%. | Grain complex is digesting a bearish supply print, opposite sign to energy. |
| **USDA Crop Progress (week ended Oct 18, released Mon Oct 19)** | **FACT:** Corn harvested 44% (5-yr avg 52%); soybeans 64% (avg 65%); winter wheat planted 63% (vs 69% avg; yesterday's package reported 60% planted — a small source difference, not material to the read). Corn 95% mature; 56% good-to-excellent (last corn quality rating of the season). | Harvest is behind pace but catching up; not a supply shock — a logistics/timing watch item. |
| **Grains — Friday closes** | **FACT:** Dec corn $4.56/bu (−3.85% w/w, 4th straight weekly decline); Nov soybeans $12.56½ (+0.3% Fri, −0.45% w/w) on strong China export sales (2.84M tons w/e Oct 15, 2.18M to China); Dec Chicago wheat $6.25 (−5.27% w/w, 8th straight weekly loss, lowest weekly settlement since June); KC wheat $6.64½. Bloomberg Grain Subindex 30.8240 (−3.21% w/w). | Grains pricing a big-crop harvest with fund liquidation, partially offset by genuine Chinese soybean demand. |
| **Metals (week ended Oct 23, from yesterday's package, not re-verified this run)** | **FACT:** COMEX front-month gold settled $3,991.10, −4.05% on the week (largest weekly % drop since week ended Jun 5, 2026); silver fell to its lowest since Nov 2025. **INFERENCE (carried):** metals falling while crude spikes = the market pricing an oil-specific risk premium, not a broad flight-to-safety. | Divergence argues against treating the crude spike as a general risk-off event. |
| **Futures curve shape — crude** | **FACT:** WTI backwardation and Brent backwardation at Friday's close (Morgan Downey weekend table). Weekend indicative: WTI $103.60 vs Fri close $103.27. | Backwardation says "pay up for a barrel today" — classic disruption pricing, encouraging draws over storage. |
| **Other dated catalysts** | **FACT:** Brazil presidential election Sun Oct 25 — outcome moves BRL and hence Brazilian export competitiveness vs US grains; result not yet known at run time — **UNVERIFIED outcome**. Fed decision Wed Oct 28. OPEC+ meeting Nov 1. US midterms ~10 days out — cited by FinanceFeeds as a political incentive for Washington to want oil lower. | — |

### Releases due in the next week
- **Mon Oct 26, 4:00 PM ET:** USDA weekly Crop Progress.
- **Wed Oct 28, 10:30 ET:** EIA Weekly Petroleum Status Report.
- **Thu Oct 29, 10:30 ET:** EIA Weekly Natural Gas Storage Report.
- **Tue Nov 10, 12:00 ET (per yesterday's package):** next WASDE — outside this week but the next grain repricing event; October's bearish carryouts are the base it revises. (Today's desk confirms only "next WASDE is November"; the Nov 10 date is carried from yesterday's verified USDA calendar read, not re-verified this run.)

**Sources:** https://www.morningstar.com/news/dow-jones/202610229168/nymex-overview-crude-climbs-as-saudi-attacks-iran-tensions-heighten-supply-risks-opis ; https://www.morningstar.com/news/dow-jones/202610237436/comex-gold-ends-the-week-405-lower-at-399110-data-talk ; https://www.nass.usda.gov ; https://commoditynews.morgandowney.com ; https://www.naturalgasintel.com ; https://www.tradingnews.com ; https://www.dtnpf.com ; https://www.bakkenwire.com ; https://wrightonthemarket.com ; https://www.thehindubusinessline.com ; https://financefeeds.com ; https://globaloilshock.com

**Decision-relevant:**
1. **[INFERENCE]** Crude is pricing war premium, not lost barrels. Brent $116.72 / WTI $103.27 at multi-month highs in steep backwardation while the physical-flow picture is itself contested (see conflict note). The premium can unwind as fast as it built — the two-sided risk (escalation vs. de-escalation headlines both moved prices this week) is the point, not a directional call.
2. **[FACT]** The EIA report argues against chasing the headline draw. Crude and gasoline drew, but distillates built 1.7M bbl and Cushing built ~1M bbl; the product market is looser than the crude headline.
3. **[FACT]** Grains and energy are moving in opposite directions on fundamentals. October WASDE delivered the second-largest US corn crop on record and pushed futures down ~5%, while energy rallies on geopolitics. Any macro/inflation read that lumps "commodities up" together is wrong this week — and the Nov 10 WASDE is the next grain catalyst.

---

## 6. Box/Parity Observer — delivered (light touch)

**One material item (index methodology) — carried from yesterday, one new secondhand detail:**
- **S&P Dow Jones Indices revises growth/value style methodology — FACT** (corroborated by multiple secondary reports of the S&P DJI release dated Oct 23, 2026; the primary S&P DJI release itself was not directly fetched): growth scoring drops 12-month price momentum, keeping 3-yr EPS-change/price and 3-yr sales-per-share growth; value scoring replaces book-to-price with an intangibles-adjusted book-to-price, blends trailing + forward 1-yr earnings-to-price, and adds free-cash-flow-to-price. Applies to S&P 500 Growth/Value and corresponding mid-/small-cap style indices. **Effective before market open Dec 21, 2026, at the annual reconstitution; pro-forma files due Dec 4, 2026.**
- **New detail this run (secondhand, UNVERIFIED against a primary source):** Bloomberg Intelligence estimate of ≥$375B in passive funds tied to affected gauges.
- Sources: https://www.tradingview.com/news/cnbctv:efc13bb28094b:0/ ; https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/
- **Desk read — INFERENCE:** this is a style-subindex reclassification, not a change to headline S&P 500 membership rules, so direct impact on SPY/QQQ tracking is limited; the actionable flow is style-index fund rebalancing around Dec 21, not a parity signal today. No watchlist-name reclassification is claimed — which names move awaits the Dec 4 pro-forma files (UNVERIFIED until then).

**Parity:** No new published parity-violation or box-spread arbitrage analysis found in the past ~7 days — only educational/explainer material. No parity violation to report. Deterministic put-call/box parity stands unchallenged as the pricing constraint; no model output in this desk contradicts it.

**Nasdaq (checked, nothing material):** recent Nasdaq-100 methodology explainers describe rules that took effect May 1, 2026 (fast-entry / float-weighting), not a new rule in the last 7 days.

**Net:** no new put-call/box parity violations or methodology changes affecting executable parity. Nothing actionable today beyond the Dec 21 style-rebalance watch item.

---

## 7. Bonds & Rates desk — delivered

**Module output (FRED daily series via `rates_desk.rates_environment()`, `mode: REAL_FRED_RATES`; all numbers are module output — none retyped from memory). Note: latest FRED observations are dated 2026-10-22 (Thu); Friday 2026-10-23 data had not landed in the daily series at pull time — so today's levels are identical to yesterday's package, which reported the same Oct 22 prints. This is a data-lag repeat, not a new observation.**

| Item | Value | As-of |
|---|---|---|
| Fed funds effective (DFF) | 3.88% | 2026-10-22 |
| Treasury 2Y (DGS2) | 4.65% | 2026-10-22 |
| Treasury 10Y (DGS10) | 4.96% | 2026-10-22 |
| 2s10s spread | 31 bp | 2026-10-22 |
| Curve shape (module) | UPWARD_SLOPING | — |
| SOFR | 3.90% | 2026-10-22 |
| EFFR | 3.88% | 2026-10-22 |
| OBFR | 3.88% | 2026-10-22 |

**Direction of change (FACT, computed from module's 60-day histories):**
- **Day-over-day (Oct 21 → Oct 22): both ends fell hard, slope flat.** 2Y 4.81% → 4.65% (−16 bp); 10Y 5.13% → 4.96% (−17 bp). Slope 32 bp → 31 bp (−1 bp) — a parallel yield drop, not a curve-shape shift.
- **Over the 60-day window:** 2Y rose 4.17% → 4.65% (+48 bp per yesterday's read; +46 bp on the module's Aug 26 base in today's desk read — a base-date difference, immaterial to the direction); 10Y rose 4.64% → 4.96% (+32 bp; +30 bp on today's base). Slope compressed 47 bp → 31 bp (−16 bp) — a flattening trend over the window, driven by the front end rising faster than the long end.
- **Fed funds change over window:** +0.25 pp as reported by the module.
- **Funding stress gauge (FACT):** SOFR − EFFR = +2 bp (3.90% vs 3.88%), OBFR = EFFR. No sign of funding stress — overnight markets are calm and aligned with the policy rate.

**Directional read for premium pricing:**
- **[FACT]** Absolute rate levels remain high (10Y near 5%, 2Y at 4.65%): higher long rates mean higher discount rates, which pressures growth-multiple valuations — a headwind for long-duration names on the watchlist (NVDA, TSLA, MSFT) on intrinsic-value grounds, not a trade signal.
- **[INFERENCE]** The Oct 22 drop eases discount-rate pressure slightly versus the prior day, but one day does not reverse a 60-day rise of 30–48 bp — the level story still dominates the daily-move story.
- **[INFERENCE]** Curve still upward-sloping (+31 bp), so no inversion signal; the flattening trend over 60 days bears watching — continued front-end-led flattening would signal the market pricing a higher-for-longer front end relative to long-run growth/inflation expectations.
- **What would change this read:** the next FRED daily prints (Oct 23 data when published) and the Oct 28 FOMC decision — a cut would likely pull the front end down faster than the long end and re-steepen the curve; a hold keeps the flattening pressure in place.

**Decision-relevant:**
1. **[FACT]** Rates dropped sharply on Oct 22 (2Y −16 bp, 10Y −17 bp) but remain historically high — modest discount-rate relief on the day, not a regime change.
2. **[FACT]** 2s10s at +31 bp, still upward-sloping but 16 bp flatter than 60 days ago — front end rising faster than the long end over the window.
3. **[FACT]** Funding markets calm: SOFR−EFFR spread just +2 bp — no stress signal in overnight funding.

---

## Synthesis — 3-5 most decision-relevant items

1. **Earnings-binary week, with a macro collision: MSFT Oct 28 AMC lands on FOMC day.** [FACT] MSFT (Nasdaq consensus $4.71, 14 ests) and AAPL Nov 2 (Nasdaq $2.00, 8 ests) are the two in-window binaries; AAPL's implied move is convergent at ~4.8–5.0%. [UNRESOLVED] MSFT's implied move is 5.3% on the fresher own-calculation vs 7.6% on the sourced Oct 18 read — do not anchor on either until Monday's chain is recomputed. [INFERENCE] Premium into either binary is event premium, not mispricing on its own — the desk rule is AVOID blind premium stances spanning the event, and Oct 28's move cannot be attributed to earnings alone. [UNVERIFIED] Historical earnings-day moves for both names remain unverified.
2. **Crude is pricing war premium, not lost barrels — and the physical-flow evidence itself is now contested.** [FACT] Brent settled $116.72 / WTI $103.27 Fri in steep backwardation; EIA crude/gasoline drew but distillates built. [UNRESOLVED] Yesterday's >24M b/d Hormuz-flow read conflicts with today's effectively-closed / ~13-tankers-per-day read — neither flow figure should be cited as settled until reconciled against a primary source. [INFERENCE, cross-desk] The two-sided premium feeds the hawkish-skip read into the Oct 28 FOMC — with rates already at 10Y 4.96% / EFFR 3.88% (Oct 22 FRED prints, Friday data not yet landed). The event stack is FOMC Wed 10/28 → EIA Wed 10/28 10:30 ET → Core PCE Thu 10/29 (post-decision) → USDA Crop Progress Mon 10/26 4pm ET.
3. **Half the watchlist still carries no clean IV-vs-realized verdict — now three names, not two.** [FACT] QQQ (32.0%), AAPL (36.4%), and NVDA (31.0%) realized windows are WINDOW-CONTINGENT; NVDA newly crossed the line on the window roll. [FACT] Term structure slopes up everywhere with Nov 20 humps for MSFT/AAPL/NVDA — event pricing, not dislocation. [UNVERIFIED] IV rank is unverified for all six names (no free IV history). [UNRESOLVED] Today's live IV levels run systematically above yesterday's live levels for the same expiry and closes — cross-day level comparisons are unreliable until the extraction difference is identified; use term-structure shape, not level deltas, for cross-day reads.
4. **The dividend window is MSFT-only, and the AAPL watch item rolls to earnings week.** [FACT] MSFT ex-div Nov 19 at the raised $0.98 (24th consecutive annual increase per the desk standard) is the only declared in-window event; AAPL's early–mid-November date is still an undeclared projection, convertible to FACT only by the declaration expected alongside its Nov 2 earnings. No cuts or specials announced.
5. **Quiet quant sweep, two new WATCH items, and a style-index watch item.** [FACT] Quant lab appended #148–151 (two ARCHIVE catch-ups the Oct 24 sweep missed, two WATCH: #150 SPY ATM-IV forecasting, blocked on licensed OptionsDX data; #151 surfbench IV-surface benchmark, whose scorecard ports directly to the desk's SPY surface-fit choice). [FACT] S&P DJI style methodology changes take effect Dec 21, 2026 (pro-forma files Dec 4) — style-index rebalancing flow to watch, not a parity signal today; a secondhand ≥$375B passive-exposure estimate is attached, unverified. No TEST/INTEGRATE movement, no parity violations.

**Cross-desk consistency check:** Rates desk (FRED EFFR 3.88%, 10Y 4.96%, Oct 22 prints) and Futures desk (crude war premium, EIA draws) agree on a hawkish-skip posture into the Oct 28 FOMC. Premium desk term structure (MSFT/AAPL/NVDA Nov 20 humps) is consistent with the Earnings desk calendar (Oct 28 / Nov 2 / Nov 18 est.). Dividend desk (MSFT Nov 19) and Earnings desk (MSFT Oct 28) give two distinct MSFT dates — do not conflate the earnings date with the ex-div date. Two conflicts remain genuinely unresolved and are flagged in place rather than resolved by fiat: (a) MSFT implied move 5.3% vs 7.6% (different chain dates/methods; Monday recomputation settles it); (b) Hormuz flow readings (different metrics/dates/sourcing chains; a primary Kpler/OPIS read settles it). The TSLA report date (Oct 21, not Oct 22) and NVDA's unconfirmed status (not Nov 18 as FACT) were corrected in synthesis from the Earnings desk's primary-source reads.

---

## Traceability
- iv-inputs file: `~/workspace/hedge-desk-research/nightly/2026-10-24-iv-inputs.json` (as_of 2026-10-24T13:54:04−07:00, FRESH per 26h guard; YESTERDAY'S post-close data — labeled as such throughout)
- live IV supplement: labeled Sunday-2026-10-25 Yahoo v7 options pull by the Premium desk (cookie+crumb handshake); Friday-2026-10-23 closes as served; levels run systematically above yesterday's live pull — flagged, not blended
- quant-lab ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#148–151 appended, verified on disk by grep after the run)
- rates module: `cd ~/workspace/github/hedge-desk && python3 -c "from hedge_desk import rates_desk; import json; print(json.dumps(rates_desk.rates_environment(), default=str))"` (exit 0; latest FRED observation 2026-10-22)
- EIA weekly (Wed 10/21), USDA Crop Progress (Mon 10/19), Oct WASDE (Fri 10/9) — published on schedule; no federal-data disruption
- All Yahoo pulls used `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; options pulls used the cookie+crumb handshake
