# Hedge-Desk Daily Research Package — Saturday 2026-10-24

**Run:** 13:30 PT (16:30 ET — markets closed; all market closes below are Friday 2026-10-23 closes, not live Saturday quotes).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Standing:** paper-only research. No Risk of Ruin work, no trade authorization, no synthetic data. Every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**Desk status:** all 7 desks delivered. No desk FAILED.

---

## 1. Earnings Event desk — delivered

**Window:** Oct 24 – Nov 7, 2026. SPY/QQQ are ETFs with no earnings (FACT — structure).

| Ticker | Event | Timing | Options-implied expected move | Historical avg earnings-day move |
|---|---|---|---|---|
| MSFT — Q1 FY27 | Wed, Oct 28, 2026 | After close; webcast 2:30 p.m. PT / 5:30 p.m. ET | **~5.3%** (Oct 30 expiry ATM straddle) | UNVERIFIED |
| AAPL — Q4 FY26 | Mon, Nov 2, 2026 | Release 1:30 p.m. PT; call 2:00 p.m. PT / 5:00 p.m. ET | **~4.9%** (Nov 6 expiry ATM straddle, first expiry after the event) | UNVERIFIED |
| TSLA | Already reported — Wed, Oct 21, 2026, after close | — | — | Single datapoint only: −3.1% in the first session after the report (secondary tracker, not independently verified) |
| NVDA | Outside window — expected Wed, Nov 18, 2026 (third-party estimate, not yet announced) | After close (expected) | — | — |

**Method (FACT):** ATM straddle mid (average bid/ask for nearest-strike call + put) ÷ underlying price, from a live Yahoo pull Oct 24 (prices are the Oct 23 close). MSFT: price $524.51, 525 strike, straddle mid $27.68 = 5.28%. AAPL: price $347.73, 350 strike, straddle mid $16.85 = 4.85%. **Caveat (INFERENCE):** a straddle proxy, not a pure earnings-move isolate — the MSFT Oct 30 straddle spans 2 sessions including the event; the AAPL Nov 6 straddle spans 4 sessions after it, so it embeds extra non-event volatility. Neither is a direction forecast.

**Evidence / labels:**
- MSFT date + after-close timing: FACT — Microsoft's own Oct 7, 2026 release.
- AAPL date + times: secondhand-corroborated, not primary-verified — Apple's Investor Relations calendar as reported identically by MacRumors, iClarified, Appleosophy, The Apple Post, and MacObserver (Oct 6–7, 2026); the IR page itself was not opened directly.
- Nasdaq earnings-calendar API returned empty rows for Oct 24 – Nov 7 on this pull (200 response, `rows: null`) — a source gap, not evidence of no earnings; dates above rest on company/press sources, not Nasdaq.
- Historical average earnings-day moves for MSFT/AAPL: UNVERIFIED — no verified series pulled; not estimated or guessed.
- TSLA Oct 21 report and NVDA Nov 18 estimate: INFERENCE-grade (secondary trackers only).

**CFA note:** neither in-window release exists yet, so no statement teardown is possible today. At release time, apply the reading order: guidance vs. consensus first, then GAAP income statement (vs. headline adjusted figure), cash flow (OCF vs. net income, capex, buybacks vs. issuance), segment margins, balance-sheet deltas, call transcript last.

**Sources:** https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; https://www.prnewswire.com/news-releases/microsoft-announces-quarterly-earnings-release-date-302901624.html ; https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/ ; https://www.simianx.ai/stories/magnificent-7-earnings-dates-results-tracker ; Yahoo Finance v7 options chain (cookie+crumb handshake), pulled Oct 24, 2026.

**Decision-relevant:**
1. **[FACT]** MSFT Oct 28 AMC is the week's binary event — first in-window, ~5.3% implied, landing the same evening as Alphabet (outside watchlist). Premium into it is event premium, not mispricing on its own.
2. **[FACT]** AAPL Nov 2 AMC is the second binary event — ~4.9% implied via the Nov 6 straddle; secondary reports say the first call led by CEO John Ternus, a qualitative uncertainty layer beyond the numbers.
3. **[FACT]** No TSLA or NVDA event inside the window — TSLA's Oct 21 print is already priced in; NVDA (Nov 18 est.) is not an in-window catalyst.

**What would change it:** a company-issued date change, a revised implied move from a nearer expiry (if weeklys list after the weekend), or a verified historical earnings-move series replacing the UNVERIFIED marks.

---

## 2. Dividend Opportunity desk — delivered

**Window:** ex-dates Oct 24 – Nov 21, 2026.

| Symbol | Ex-date | Amount | Pay date | Status |
|---|---|---|---|---|
| MSFT | **2026-11-19** | **$0.98/qtr** | 2026-12-10 | FACT — declared, INCREASE |
| AAPL | ~2026-11-09 (forecast only) | $0.27 expected, unchanged | ~2026-11-12 (forecast) | UNDECLARED — forecast, not FACT |
| SPY | none in window | — | — | Next ex ~2026-12-18, outside window |
| QQQ | none in window | — | — | Next ex ~2026-12-21, outside window |
| NVDA | none in window | — | — | Next ex ~2026-12-04 per one source, outside window; amount UNVERIFIED |
| TSLA | none — pays no dividend | — | — | FACT |

**MSFT — the one declared event in window [FACT].** Nasdaq dividends API (queried 2026-10-24): ex 11/19/2026, $0.98, declared 09/15/2026, record 11/19/2026, pay 12/10/2026. Prior quarter $0.91 (ex 08/20/2026), so the raise is +$0.07, +7.7%, corroborated by the Sep 15 board announcement. Consecutive-increase count: **24 consecutive annual increases (incl. the Sep 2026 raise)**, per the standing standard in `~/workspace/hedge-desk-research/dividend-count-standard.md`. The standard resolves a third-party conflict: MarketBeat still shows "23 years" while FinanceCharts shows 24 — the standard's Sep-15-announcement rule gives 24; do not drift to 23. No cut or special announced.

**AAPL — expected in window, NOT declared [UNVERIFIED as to date/amount].** Nasdaq header still shows last ex 08/10/2026 ($0.27, paid 08/13/2026); Zacks (crawled within 5 days) states Apple has no future dividends declared. DividendMax forecasts declaration 10/29/2026, ex 11/09/2026, pay 11/12/2026, at its own stated 65% forecast accuracy — a forecast, not a declaration. Pattern supports it [INFERENCE]: AAPL's last four Q4 ex-dates fell Nov 4–10 (2022–2025) and raises historically arrive with the May payment, not November, so the expected amount is $0.27 unchanged — but until declared, treat date and amount as SPECULATION/UNVERIFIED, not FACT.

**SPY [FACT on last distribution]:** Yahoo v8 chart (UA-only, prices as of 2026-10-23 close): last ex 2026-09-18, $1.889. Wall Street Horizon / TipRanks put the next ex at 2026-12-18, pay 2027-01-29, amount not yet declared (UNVERIFIED). The Q3 payment date 2026-10-30 falls inside the window but its ex-date was September, so it is not a new opportunity.

**QQQ [FACT on last distribution]:** Nasdaq ETF API: last ex 09/21/2026, $0.75143, paid 10/08/2026. Wall Street Horizon puts next ex 2026-12-21, pay 2027-01-11, amount UNVERIFIED.

**NVDA [FACT on history; next date/amount UNVERIFIED]:** Nasdaq: last ex 09/10/2026, $0.25, paid 10/01/2026 — a jump from $0.01 in Q1 2026 (declared 08/26/2026), confirmed by Yahoo chart events. One calendar source lists next ex 2026-12-04, outside the window; Finbold reports the Q4 payout as not yet officially declared. Do not carry a December amount as FACT.

**TSLA [FACT]:** no dividend — Yahoo chart shows zero dividend events; Nasdaq shows ex N/A; Tesla has never paid a cash dividend.

**Cuts / specials:** none announced for any watchlist name in the sources checked. This is a checked-negative, not an issuer filing review — a cut announced after 2026-10-24 would change it.

**Sources:** https://api.nasdaq.com/api/quote/MSFT/dividends?assetclass=stocks ; https://www.tradingview.com/news/tradingview:5f23beaf59b00:0-microsoft-corp-nasdaq-msft-raises-quarterly-dividend-8-to-0-98/ ; https://api.nasdaq.com/api/quote/AAPL/dividends?assetclass=stocks ; https://www.zacks.com/stock/research/AAPL/dividend-history ; https://www.dividendmax.com/united-states/nasdaq/technology-hardware-and-equipment/apple-inc/dividends ; https://query2.finance.yahoo.com/v8/finance/chart/SPY ; https://api.nasdaq.com/api/quote/QQQ/dividends?assetclass=etf ; https://api.nasdaq.com/api/quote/NVDA/dividends?assetclass=stocks

**Decision-relevant:**
1. **[FACT]** MSFT ex 2026-11-19 at the raised $0.98 is the only declared watchlist ex-date in the next 4 weeks — the ex-date price adjustment of ~$0.98 is the only mechanical event to plan around.
2. **[UNVERIFIED]** AAPL's November dividend is still undeclared — the ~Nov 9 forecast date is pattern-based only; the declaration (expected alongside late-October earnings) is the trigger that converts this from forecast to FACT. Do not price an AAPL ex-date as certain yet.
3. **[FACT]** No dividend-driven ex-date cluster otherwise — SPY, QQQ, and NVDA all next go ex in December, and TSLA pays nothing.

**What would change it:** an AAPL declaration (expected ~Oct 29) adding a second in-window ex-date, or any issuer announcing a cut/special before Nov 21.

---

## 3. Overnight Premium desk (IV) — delivered

### IV-inputs freshness guard — PASS (within 26h guard, not STALE)
- Latest file: `~/workspace/hedge-desk-research/nightly/2026-10-23-iv-inputs.json`, **as_of 2026-10-23T13:54:05−07:00** (Fri post-close pull; ~23.5h old at this run's 13:26 PT start — inside the 26h guard).
- **Caveat (FACT, from the file's own failures list):** all six symbols' ATM IV in that file are **null** — the pull failed closed because the nearest expiry (2026-10-23) had already expired at 16:00 ET, and Yahoo's post-expiry marks are solver residuals, not tradeable IV. The file's realized-vol data below is still usable; its IV levels are not.
- **Live supplement (labeled):** fresh Yahoo v7 options pull done this run via cookie+crumb handshake. Quotes are **Friday 2026-10-23 close** (quote time 20:00 UTC) — markets are closed Saturday, so these are Friday-close marks, not live executable quotes.

### Snapshot table (FACT — Yahoo chain, Fri close; realized window 2026-09-25 → 10-22)

| Symbol | Fri close | ATM IV, Oct 26 expiry (DTE 2) | ATM IV, Nov 20 expiry (DTE 27) | 20d realized | Window-contingent? | Earnings in window |
|---|---|---|---|---|---|---|
| SPY | 759.97 | 11.1% | 15.8% | 9.9% | No (20.1%) | — |
| QQQ | 704.40 | 19.5% | 25.3% | 19.0% | **YES (30.7%)** | — |
| AAPL | 347.73 | 16.4% | 27.5% | 16.9% | **YES (35.3%)** | 2026-11-02 (in Nov 20 window) |
| MSFT | 524.51 | 18.5% | 33.9% | 20.1% | No (19.1%) | 2026-10-28 (in Nov 20 window) |
| NVDA | 210.96 | 29.6% | 44.3% | 30.3% | No (29.9%, just under 30% line) | 2026-11-18 (in Nov 20 window) |
| TSLA | 372.22 | 29.7% | 40.3% | 37.3% | No (20.9%) | None listed in file |

ATM IV = mean of nearest-strike call/put Yahoo impliedVolatility. **IV rank for all six names: UNVERIFIED** — no IV history available from free sources; no "elevated IV rank" claim is made.

### Findings (labeled)
- **Term structure slopes up everywhere (front < back) — INFERENCE:** no front-month hump at Oct 26, because no watchlist earnings fall inside that expiry. The humps sit in the Nov 20 expiry, which contains MSFT (Oct 28), AAPL (Nov 2), and NVDA (Nov 18) earnings. Elevated back-month IV for those three names is **expected event pricing, not "rich" premium** (CFA sanity check #3).
- **MSFT — premium into a binary event:** front IV 18.5% vs 33.9% in the earnings-bearing Nov 20 expiry. The event premium is in the back expiry, not the Oct 26 weekly — any premium stance spanning Oct 28 must price the crush, not the front IV. Cross-check with the Earnings desk: the Oct 30 straddle implies ~5.3% over the event window, consistent with event premium concentrated in the expiry containing Oct 28. What would change it: earnings date moves or a pre-announcement.
- **Stale-jump screen (standing rule):** QQQ (30.7%) and AAPL (35.3%) are **WINDOW-CONTINGENT** — any IV-vs-realized verdict for them is WINDOW-CONTINGENT, not clean. NVDA at 29.9% sits just under the 30% line; treat its verdict as fragile to one more large day. SPY, MSFT, TSLA windows are not contingent.
- **Window-roll note (FACT, cross-desk):** MSFT's window is no longer contingent on the new Sep 25 – Oct 22 window (19.1%), versus 35.1% on yesterday's Sep 24 – Oct 21 window — the large day rolled out of the window. This is a window change, not a data contradiction; yesterday's verdicts built on the old window do not carry forward mechanically.
- **TSLA — front IV below trailing realized (INFERENCE, clean window):** 29.7% front IV vs 37.3% 20d realized — premium is not pricing the recent realized pace. Backward-looking only; what would change it: a realized-vol regime break or a fresh catalyst. No trade implication is drawn (paper-only; no authorization).
- **SPY/QQQ front IV roughly at trailing realized** (11.1% vs 9.9%; 19.5% vs 19.0%) — no IV-vs-realized edge asserted; QQQ's comparison is window-contingent anyway.
- **Parity check:** not certified — Friday-close marks with wide/closing spreads are not executable quotes, so no put-call/box parity verdict is claimed from this pull. Deterministic parity outranks any model output when live quotes are available; that check awaits Monday's live chain.

**Decision-relevant:**
1. **[FACT]** MSFT Oct 28 earnings sits in the Nov 20 expiry (33.9% IV vs 18.5% front) — premium into the binary event lives in the back expiry; do not read front IV as the event price.
2. **[FACT]** QQQ and AAPL realized windows are WINDOW-CONTINGENT (30.7%, 35.3%) — no clean IV-vs-realized verdict for either; NVDA (29.9%) is one large day from joining them.
3. **[UNVERIFIED]** IV rank is UNVERIFIED for all six names (no free IV history) — no "elevated IV rank" flag is issued this run; the desk reports IV *levels* and term structure only.

---

## 4. Open Quant/AI Model Lab — delivered

**Window status (FACT):** arXiv legs return newest items dated 22 Oct 2026 — Saturday, no new announcements until Monday, so the window is genuinely empty, not a leg failure. GitHub search API leg failed again (empty bodies, 2 strikes — the known proxy transient); switched to the web-search leg per standing rule, which surfaced nothing new since the 2026-10-23 sweep. All 7 candidates below were scored by running the repo scorer (`hedge_desk.research_intelligence.assess_source`) — no hand-scoring. All 7 appended to the ledger as #140–146; verified on disk after append.

| # | Candidate | Score | Disposition | Reason |
|---|---|---|---|---|
| 140 | "Directionally Correct Views in Portfolio Optimization" — arXiv:2610.31074v1, 22 Oct 2026 | 25 | ARCHIVE | Black-Litterman-style views in Markowitz setting (source-reported, UNVERIFIED). Portfolio lane, no vol/options/earnings/dividend/purged-WF transfer; no code link. |
| 141 | "When News Gets Old: Portfolio Allocation with RL and LLMs" — arXiv:2610.30564v1, 22 Oct 2026 | 28 | ARCHIVE | Aging-news treatments in RL/LLM portfolio policies on SEC-disclosure signals (source-reported, UNVERIFIED). Portfolio/LLM-agent lane, no desk procedure; no code link. |
| 142 | "Governed Self-Evolution for Autonomous Investing" (Steward) — arXiv:2610.30557v1, 22 Oct 2026 | 25 | ARCHIVE | Multi-agent LLM investing system (source-reported, UNVERIFIED). Autonomous-investing framing = paper-only boundary mismatch; governance pattern is a note only; no code link. |
| 143 | "Probability-Weighting Functions for Normal Tempered-Stable Laws" — arXiv:2610.26746v1, 19 Oct 2026 | 22 | ARCHIVE | NTS prior/posterior PWF construction (source-reported, UNVERIFIED). Pure distribution theory, no desk procedure; no code link. |
| 144 | "The Control Layer Behind Rule-Following Agents Trading Across Market Conditions" — arXiv:2610.26324v1, 19 Oct 2026 | 28 | ARCHIVE | 2,627 positions, 18% real Hyperliquid orders (source-reported, UNVERIFIED) — live-trading framing mismatch. Rule-adherence-vs-luck toolkit is a process note only; no code link. |
| 145 | "A Pricing and Hedging Framework for Infinite-Dimensional Financial Markets" — arXiv:2610.24169v1, 16 Oct 2026 | 22 | ARCHIVE | Hilbert-space Black-Scholes framework (source-reported). Pure theory, no desk transfer; no code link. |
| 146 | **Keller-Ressel & Nikulski — "Discovering parametrizations of implied volatility with symbolic regression" (PySR)** — arXiv:2603.21892v1, 23 Mar 2026 | 48 | **WATCH** | **Full paper read at source.** PySR conditional symbolic regression on IV slices rediscovers SVI at complexity 15 when the Lee-tail wing-arbitrage penalty is applied (FACT — paper Table 2b, loss 4.06e-11), and finds SVI-plus-one-term extensions fitting W-shaped C6/C8 curves (FACT — eqs. 4.1–4.3). No author code link in the paper text (FACT — "github" search = 0 hits) → reproducibility not established; PySR itself is open-source so the method is re-implementable. |

**Source URLs:** https://arxiv.org/abs/2610.31074, https://arxiv.org/abs/2610.30564, https://arxiv.org/abs/2610.30557, https://arxiv.org/abs/2610.26746, https://arxiv.org/abs/2610.26324, https://arxiv.org/abs/2610.24169, https://arxiv.org/abs/2603.21892. Ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#140–146).

**Most decision-relevant:**
1. **[FACT, with correction]** #146 is the only material new item — and it corrects a secondary claim. The QuantFrame article (22 Oct 2026) that surfaced it claims "the simplest formula that beat SVI scores 10." That is NOT what the paper shows (INFERENCE from the paper's own Table 2): the complexity-10 penalized expression has loss 7.55e-7 versus SVI-at-15's 4.06e-11. The paper's real claim is SVI rediscovery under an arbitrage penalty plus W-shape extensions. Premium-desk follow-up: sandbox PySR conditional regression on a live SPY chain and test whether the SVI-rediscovery + Lee-penalty result reproduces on desk data, against the #18/#128 SVI fits.
2. **[FACT]** Nothing new reached TEST or INTEGRATE (scorer max 48). No re-checks repeated this run — today's earlier kaizen run already covered the license blocks (#1/#20/#32/#86), #21's v3 + ICAIF '26 acceptance, and #23's live Friday data.
3. **[FACT]** Triage exclusions (no ledger rows): Suleyman040/options-analytics (created 1 Oct, not new, plus BTC/Deribit crypto scope); anthonymakarewicz/volatility-trading (already excluded — ORATS paid-data gated); outcometick/polymarket-backtest (prediction-market scope); QuantFrame's PySR/tick/arch/MAPIE roundup (established libraries, not new candidates; the PySR paper itself became #146).

**Bottom line:** quiet Saturday sweep — one WATCH item worth the premium desk's attention (#146, with the secondary-summary correction attached), six ARCHIVEs on band discipline, no TEST/INTEGRATE movement.

---

## 5. Futures Event desk (Weather/War/Logistics) — delivered

**Scope note:** Saturday — latest closes are Friday Oct 23. No new federal release is due this weekend; all federal releases below are on their normal schedule (no shutdown framing — CR funding through Dec 11, per standing rule).

### Fresh catalysts and what futures are pricing

| Catalyst | Facts (labeled) | Read |
|---|---|---|
| **Gulf / Saudi attacks — crude spike** | **FACT:** Brent settled Fri Oct 23 at $116.72/bbl, +$3.55 (+3.14%), highest close since Apr 29; WTI settled at $103.27, +$3.80 (+3.8%). Brent +~6% on the week, WTI +~2.3%. Brent–WTI spread = $13.45 (arithmetic). **FACT:** Houthi strikes hit Saudi targets incl. energy sites/airports during the week; Saudi Aramco evacuated Dhahran HQ staff Thu; a tanker was struck near Oman Wed (UKMTO); State Dept ordered non-essential US personnel out of the kingdom. | Market is pricing a geopolitical risk premium, not a confirmed physical shortfall — see inference below. |
| **Physical flows vs. price** | **FACT:** Middle East crude exports through Hormuz/alternative routes averaged >24M b/d in the week through Oct 18, above the pre-war 23.3M b/d (Kpler, via OPIS/Dow Jones). **FACT:** Saudi said crude production was unaffected, but refined-product shipments were restricted. **INFERENCE:** The price rise alongside recovered headline flows points to a fear/insurance premium (shipping risk, record Persian Gulf freight rates per ING) rather than barrels already lost. **What would change it:** a confirmed large Saudi production outage, a Hormuz closure, or a verified ceasefire/de-escalation — any of which would re-price the premium fast in either direction. | Do not read $116 Brent as evidence of a current supply deficit. |
| **EIA Weekly Petroleum Status Report (week ended Oct 16, released Wed Oct 21)** | **FACT:** Commercial crude −3.1M bbl to 412.5M bbl, ~3% below the 5-yr average, third straight weekly draw. Gasoline −3.0M bbl to 205.3M bbl (~5% below average). Distillates +1.7M bbl to 104.3M bbl (still ~9% below 5-yr average). Refinery utilization 93.4%. US production 13.269M b/d, −410k b/d w/w on lingering Gulf (Hurricane Isaias) effects. SPR −0.3M bbl to 282.7M bbl, lowest since 1982. Cushing +0.9M bbl. | Tight crude/gasoline, but the distillate build undercuts the simplest "everything tight" bull case. |
| **DOE emergency SPR action** | **FACT:** DOE authorized an emergency exchange of up to 400k bbl from the SPR for Phillips 66's Lake Charles refinery (supply disruption). Germany's EBV also tendered strategic diesel/heating-oil/crude volumes — its first such release since the early-October G7 coordinated-release agreement. | Policy response is targeted (refinery-specific), not a broad SPR flood — so far. |
| **EIA Natural Gas Storage (week ended Oct 16, released Thu Oct 22, 10:30 ET)** | **FACT:** +77 Bcf injection to 3,644 Bcf — 152 Bcf (−4%) below year-ago, but +35 Bcf (+1%) above the 2021–2025 average and inside the 5-yr range. South Central +28 Bcf to 1,125 Bcf, still −10% y/y and −3.4% vs average. **FACT (single-source, lower weight):** Henry Hub front-month ~$2.64, −15.28% on the week, testing ~$2.70 support on warm forecasts. | Gas enters withdrawal season near-normal nationally with a South Central deficit — weather, not storage, is the swing factor now. |
| **USDA Oct WASDE (Fri Oct 9, 12:00 ET)** | **FACT:** Corn yield raised to 181.2 bu/acre, production 16.034B bu, ending stocks 1.849B bu (+282M vs Sep, above the 1.677B trade average); soybeans record 53.1 bu/acre, 4.562B bu, stocks 315M bu; wheat production 1.534B bu (smallest since 1970), stocks 740M bu (+23M). **FACT:** Futures fell on the report — corn ~5%, soybeans ~2%, wheat ~3%. | Grain complex is digesting a bearish supply print, opposite sign to energy. |
| **USDA Crop Progress (week ended Oct 18, released Mon Oct 19)** | **FACT:** Corn harvested 44% (5-yr avg 52%); soybeans 64% (avg 65%); cotton 41%; winter wheat planted 60% (avg 69%). Corn 95% mature; 56% good-to-excellent (last corn quality rating of the season). Lag concentrated in MI/OH/IA (MI corn harvest 13%, IA 26%). | Harvest is behind pace but catching up; not a supply shock — a logistics/timing watch item. |
| **Metals (week ended Oct 23)** | **FACT:** COMEX front-month gold settled $3,991.10, −4.05% on the week (largest weekly % drop since week ended Jun 5, 2026); down 2 straight weeks, −24.96% off the Jan 29 52-week high of $5,318.40, ~1% above 52-week lows. Silver fell to its lowest since Nov 2025 (Dow Jones roundup). **INFERENCE:** Metals falling while crude spikes = the market is pricing an oil-specific risk premium, not a broad flight-to-safety. | Divergence argues against treating the crude spike as a general risk-off event. |
| **Futures curve shape** | **UNVERIFIED:** No free-source term-structure (front-vs-deferred spread) data was pulled for crude, gas, or grains in this run, so no contango/backwardation claim is made. Brent's $13.45 premium to WTI is a grade/location spread, not a curve signal. | Do not cite a curve shape from this section. Yesterday's backwardation read is NOT carried forward as today's fact. |

### Releases due in the next week
- **Mon Oct 26:** USDA weekly Crop Progress (weekly Monday release; exact time not re-verified this run).
- **Wed Oct 28, 10:30 ET:** EIA Weekly Petroleum Status Report (standing weekly cadence).
- **Thu Oct 29, 10:30 ET:** EIA Weekly Natural Gas Storage Report (standing weekly cadence; next print per MarketChameleon calendar).
- **Tue Nov 10, 12:00 ET:** Next WASDE (USDA 2026 calendar) — outside this week but the next grain repricing event; October's bearish carryouts are the base it revises.

**Sources:** https://www.morningstar.com/news/dow-jones/202610229168/nymex-overview-crude-climbs-as-saudi-attacks-iran-tensions-heighten-supply-risks-opis ; https://www.mitrade.com/insights/commodity-analysis/oil-news/brent-113-diesel-eia-20261023J1351 ; https://www.engine.online/news/eia-reports-a-draw-in-us-crude-oil-stocks-8306 ; https://m.ajupress.com/view/20261024084739111 ; https://www.southshorepress.com/business/u-s-crude-settles-above-100-as-brent-reaches-its-highest-close-since-april-0d245428 ; https://el7.ai/en/news/2026-10-22-us-natural-gas-inventories-rise-by-77-bcf ; https://www.barchart.com/story/news/8334511/nat-gas-prices-fall-to-2-month-low-on-warm-forecasts-but-recover-modestly-on-eia-report ; https://www.rfdtv.com/wasde-recap-usda-raises-grain-supplies-as-futures-fall-sharply ; https://www.usda.gov/oce/commodity/wasde ; https://www.dtnpf.com/agriculture/web/ag/news/article/2026/10/19/usda-crop-progress-corn-44-harvested ; https://www.farmprogress.com/corn/crop-progress-last-call-for-corn-quality-ratings ; https://www.morningstar.com/news/dow-jones/202610237436/comex-gold-ends-the-week-405-lower-at-399110-data-talk ; https://www.morningstar.com/news/dow-jones/202610239542/materials-down-as-precious-metal-selloff-continues-materials-roundup ; https://businesspost.ng/economy/oil-prices-nears-six-month-high-as-houthis-intensify-attacks-on-saudi/

**Decision-relevant:**
1. **[INFERENCE]** Crude is pricing war premium, not lost barrels. Brent $116.72 / WTI $103.27 at multi-month highs while Hormuz flows exceed pre-war levels. The premium can unwind as fast as it built — the two-sided risk (escalation vs. de-escalation headlines both moved prices this week) is the point, not a directional call.
2. **[FACT]** The EIA report argues against chasing the headline draw. Crude and gasoline drew, but distillates built 1.7M bbl and Cushing built 0.9M bbl; the product market is looser than the crude headline. A crude-long thesis needs the distillate tightness story, and this print weakened it.
3. **[FACT]** Grains and energy are moving in opposite directions on fundamentals. October WASDE delivered the second-largest US corn crop on record and pushed futures down 5%, while energy rallies on geopolitics. Any macro/inflation read that lumps "commodities up" together is wrong this week — and the Nov 10 WASDE is the next grain catalyst.

---

## 6. Box/Parity Observer — delivered (light touch)

**One material item (index methodology):**
- **S&P Dow Jones Indices revises growth/value style methodology — FACT** (corroborated by two independent secondary reports of the S&P DJI release dated Oct 23, 2026; the primary S&P DJI release itself was not directly fetched, so factor-level detail below rests on that corroborated reporting): growth scoring drops 12-month price momentum, keeping 3-yr EPS-change/price and 3-yr sales-per-share growth; value scoring replaces book-to-price with an intangibles-adjusted book-to-price, blends trailing + forward 1-yr earnings-to-price, and adds free-cash-flow-to-price. Applies to S&P 500 Growth/Value and corresponding mid-/small-cap style indices. **Effective before market open Dec 21, 2026, at the annual reconstitution; pro-forma files due Dec 4, 2026.**
- Sources: https://www.tradingview.com/news/cnbctv:efc13bb28094b:0/ and https://bursakl.com/news/s-and-p-changes-rules-for-classifying-growth-and-value-stocks/n751
- **Desk read — INFERENCE:** this is a style-subindex reclassification, not a change to headline S&P 500 membership rules, so direct impact on SPY/QQQ tracking is limited; the actionable flow is style-index fund rebalancing around Dec 21, not a parity signal today. No watchlist-name reclassification is claimed — which names move awaits the Dec 4 pro-forma files (UNVERIFIED until then).

**Parity:** No new published parity-violation or box-spread arbitrage analysis found in the past ~2 weeks — only educational/explainer material (e.g., put-call parity explainer dated Oct 17, 2026). No parity violation to report. Deterministic put-call/box parity stands unchallenged as the pricing constraint; no model output in this desk contradicts it.

**Nasdaq (checked, nothing material):** No new Nasdaq-100 methodology change in the window — only routine items: the Oct 9 Nasdaq-100 constituent change (Moderna in, Warner Bros. Discovery out) and new-index launches effective Oct 16, neither a methodology revision to an existing watchlist benchmark.

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
- **Day-over-day (Oct 21 → Oct 22): both ends fell hard.** 2Y 4.81% → 4.65% (−16 bp); 10Y 5.13% → 4.96% (−17 bp). Slope essentially flat on the day: 32 bp → 31 bp (−1 bp).
- **Over the 60-day window:** 2Y rose 4.17% → 4.65% (+48 bp); 10Y rose 4.64% → 4.96% (+32 bp). Slope compressed 47 bp → 31 bp (−16 bp) — a flattening trend over the window, driven by the front end rising faster than the long end.
- **Fed funds change over window:** +0.25 pp as reported by the module.
- **Funding stress gauge (FACT):** SOFR − EFFR = +2 bp (3.90% vs 3.88%), OBFR = EFFR. No sign of funding stress — overnight markets are calm and aligned with the policy rate.

**Directional read for premium pricing:**
- **[FACT]** Absolute rate levels remain high (10Y near 5%, 2Y at 4.65%): higher long rates mean higher discount rates, which pressures growth-multiple valuations — a headwind for long-duration names on the watchlist (NVDA, TSLA, MSFT) on intrinsic-value grounds, not a trade signal.
- **[INFERENCE]** The day's move cuts the other way at the margin: a ~16–17 bp drop at both ends eases discount-rate pressure slightly versus yesterday. But one day does not reverse a 60-day rise of 32–48 bp — the level story still dominates the daily-move story.
- **[INFERENCE]** Curve still upward-sloping (+31 bp), so no inversion signal; the flattening trend over 60 days bears watching — continued front-end-led flattening would signal the market pricing a higher-for-longer front end relative to long-run growth/inflation expectations.
- **What would change this read:** the next FRED daily prints (Oct 23 data when published) and the Oct 28 FOMC decision — a cut would likely pull the front end down faster than the long end and re-steepen the curve; a hold keeps the flattening pressure in place.

**Decision-relevant:**
1. **[FACT]** Rates dropped sharply on Oct 22 (2Y −16 bp, 10Y −17 bp) but remain historically high — modest discount-rate relief on the day, not a regime change.
2. **[FACT]** 2s10s at +31 bp, still upward-sloping but 16 bp flatter than 60 days ago — front end rising faster than the long end over the window.
3. **[FACT]** Funding markets calm: SOFR−EFFR spread just +2 bp — no stress signal in overnight funding.

---

## Synthesis — 3-5 most decision-relevant items

1. **Earnings-binary week: MSFT Oct 28 AMC is the event, AAPL Nov 2 follows.** [FACT] MSFT ~5.3% implied (Oct 30 straddle) and its Nov 20 IV hump (33.9% vs 18.5% front) both price the Oct 28 report; AAPL ~4.9% implied (Nov 6 straddle) with a Nov 20 IV hump for Nov 2. [INFERENCE] Premium into either binary is event premium, not mispricing on its own — the desk rule is AVOID blind premium stances spanning the event. [UNVERIFIED] Historical earnings-day moves for both names remain unverified; do not anchor on a guessed average.
2. **Crude is pricing war premium, not lost barrels — and it is the live inflation input into the FOMC.** [FACT] Brent settled $116.72 / WTI $103.27 Fri while Hormuz flows exceed pre-war levels; EIA crude/gasoline drew but distillates built. [INFERENCE, cross-desk] The two-sided premium (escalation vs. de-escalation headlines both moved prices this week) is the risk, and it feeds the hawkish-skip read into the Oct 28 FOMC — with rates already at 10Y 4.96% / EFFR 3.88% (Oct 22 FRED prints, Friday data not yet landed). The event stack is FOMC Wed 10/28 → Core PCE Thu 10/29 (post-decision) → EIA Wed 10/28 10:30 ET.
3. **Half the watchlist still carries no clean IV-vs-realized verdict.** [FACT] QQQ (30.7%) and AAPL (35.3%) realized windows are WINDOW-CONTINGENT; NVDA (29.9%) is one large day from joining them. [FACT] MSFT's window rolled clean (19.1%, vs 35.1% yesterday) — a window change, not a contradiction. [UNVERIFIED] IV rank is unverified for all six names (no free IV history); the only clean window reads are SPY/QQQ-front roughly at realized and TSLA front IV (29.7%) below trailing realized (37.3%) — the latter backward-looking only.
4. **The dividend window is MSFT-only.** [FACT] MSFT ex-div Nov 19 at the raised $0.98 (24th consecutive annual increase per the desk standard) is the only declared in-window event; AAPL's ~Nov 9 date is still an undeclared forecast, convertible to FACT only by the declaration expected ~Oct 29. No cuts or specials announced.
5. **Quiet quant sweep, one WATCH item, and a style-index watch item.** [FACT] Quant lab appended #140–146 (six ARCHIVE, one WATCH: #146 PySR/SVI symbolic regression — with the secondary-summary correction that SVI-at-15, not a complexity-10 formula, is what the paper actually shows). [FACT] S&P DJI style methodology changes take effect Dec 21, 2026 (pro-forma files Dec 4) — style-index rebalancing flow to watch, not a parity signal today. No TEST/INTEGRATE movement, no parity violations.

**Cross-desk consistency check:** Rates desk (FRED EFFR 3.88%, 10Y 4.96%, Oct 22 prints) and Futures desk (crude war premium, EIA draws) agree on a hawkish-skip posture into the Oct 28 FOMC; no September PCE print can move that decision (Core PCE lands Oct 29, post-decision, per yesterday's verified BEA schedule). Premium desk term structure (MSFT/AAPL/NVDA Nov 20 humps) is consistent with the Earnings desk calendar (Oct 28 / Nov 2 / Nov 18). Dividend desk (MSFT Nov 19) and Earnings desk (MSFT Oct 28) give two distinct MSFT dates — do not conflate the earnings date with the ex-div date. No contradictions requiring resolution beyond the MSFT window-roll note above, which is explained, not unresolved.

---

## Traceability
- iv-inputs file: `~/workspace/hedge-desk-research/nightly/2026-10-23-iv-inputs.json` (as_of 2026-10-23T13:54:05−07:00, FRESH per 26h guard; IV leg null — failed closed on expired 2026-10-23 expiry)
- live IV supplement: labeled Friday-2026-10-23-close Yahoo v7 options pull by the Premium desk (cookie+crumb handshake); no separate pull file claimed in this package
- quant-lab ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#140–146 appended, verified on disk by the desk)
- rates module: `cd ~/workspace/github/hedge-desk && python3 -c "from hedge_desk import rates_desk; import json; print(json.dumps(rates_desk.rates_environment(), default=str))"` (exit 0; latest FRED observation 2026-10-22)
- EIA weekly (Wed 10/21), USDA export sales / Crop Progress (Mon 10/19), Oct WASDE (Fri 10/9) — published on schedule; no federal-data disruption
- All Yahoo pulls used `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; options pulls used the cookie+crumb handshake
