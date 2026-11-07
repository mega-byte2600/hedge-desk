# Hedge-Desk Daily Research — Sat 2026-11-07 (~13:30 PT)

Research-only input package. Paper-only context. No trade authorization, no Risk of Ruin estimate.
Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED.
All prices/closes as of Fri 2026-11-06 unless stated. Market closed Sat; no live Saturday prints exist.

## Top 5 decision-relevant items (synthesis)

1. **NVDA earnings Tue Nov 17 (after close) is the only watchlist earnings in the next two weeks — and the options market prices a move roughly double history.** FACT: consensus EPS $2.47, revenue ~$108.98B vs $108.0B ±2% guidance. Nov-20 ATM straddle implies ~11.2% (~8.9% event-isolated); historical average earnings-day move ~5% over the last 10 reports (6 down / 4 up). Nov-20 ATM IV 71.8% vs 49.8% at the 2-DTE expiry. Premium into the Nov 17 binary event = avoid. (Earnings desk + Premium desk, corroborated.)
2. **Oil's war premium collapsed, then Hormuz escalated again after the close.** FACT: Brent −16.4% on the week ($117.64 → $98.32 Fri) on US–Iran de-escalation pricing after Democrats won both chambers Tue Nov 3; WTI $90.83. FACT: three more tankers attacked in the Strait Thu Nov 5; Hormuz flows below 60% of normal; explosions heard on Qeshm Island Sat Nov 7 (cause UNVERIFIED). INFERENCE: the −16% week is a sentiment repricing of a possible deal, not a supply glut clearing — distillates at a 23-year low (99.3 Mbbl, −3.6 Mbbl w/e Oct 30), five straight crude draws. Watch: the Sunday-evening oil reopen. (Futures desk.)
3. **December Fed hike odds repriced to ~77–80% on the hot jobs print — and Tuesday Nov 10 is the week's hinge.** FACT: BLS Oct payrolls +165K vs ~65K expected, unemployment 4.1% (from 4.2%), Fri Nov 6. Invezz (Nov 6, citing CME FedWatch): Dec hike odds ~77%, up ~10pp; traders raised to ~80% from 75%. FACT: Oct CPI lands Tue Nov 10, 8:30 ET — the last CPI the FOMC sees before its Dec 8–9 meeting — alongside USDA WASDE 12:00 ET and the EIA STEO. Resolution of an apparent conflict: the Rates desk's Nov 5 front-end rally (2Y −12bp) predates the Nov 6 jobs print, so the easing read and the hike-odds jump are sequential, not contradictory. (Futures desk + coordinator verification via Invezz/CME FedWatch, 2026-11-07.)
4. **Every IV-vs-realized verdict is WINDOW-CONTINGENT — no clean "premium cheap/rich" call on any name.** FACT: the Thu Nov 5 selloff (SPY −4.51%, QQQ −6.71%, NVDA −9.72%, TSLA −11.40%) drives 46–63% of each 20-day realized-variance window; the Wed Nov 4 rally (AAPL +5.17%, MSFT +6.47%) drives the other two. Ex-driver realized vols: SPY 13.4%, QQQ 25.0%, AAPL 17.2%, MSFT 26.0%, NVDA 37.0%, TSLA 42.4% — every headline 20d realized is inflated by that single day. IV rank is UNVERIFIED for all six names (no free IV-history source). Verdicts become clean only when Nov 4–5 roll out of the window (~Dec 3–4). (Premium desk.)
5. **Rates: no funding stress; curve steepened a touch on the front-end rally, pre-jobs-print.** FACT (FRED via repo rates module, REAL_FRED_RATES, obs through Thu Nov 5 — Fri Nov 6 FRED data not yet in the pull): EFFR 3.88%, 10Y 4.84% (−6bp), 2Y 4.46% (−12bp), 2s10s +38bp (32bp → 38bp in a day), SOFR 3.92% vs EFFR 3.88% (+4bp spread — narrow, no stress signal). INFERENCE: long rates elevated = continued pressure on growth multiples via discount rates; one day of steepening is not a regime call. What would change it: Fri Nov 6 FRED observations, or a hot Tue CPI repricing the front end up. (Bonds & Rates desk.)

---

## 1. Earnings Event desk — COMPLETE

| Ticker | Date | Timing | Consensus EPS | Options-implied move | Historical avg earnings-day move |
|---|---|---|---|---|---|
| NVDA | Tue 2026-11-17 | After close (call 5:00 PM ET / 2:00 PM PT) | $2.47 (Yahoo avg; Zacks $2.49) | ~11.2% via Nov-20 ATM straddle; ~8.9% event-isolated | ~5% avg absolute move, last 10 reports (May 2024–Aug 2026); 6 down / 4 up |
| AAPL | — none in window — | — | — | — | Last reported 2026-11-02 ($2.10 vs $1.99 est.); next ~2027-01-28 (estimate) |
| MSFT | — none in window — | — | — | — | Last reported 2026-10-28 ($4.89 vs $4.72 est.); next ~2027-01-27 (estimate) |
| TSLA | — none in window — | — | — | — | Last reported 2026-10-21 ($0.48 vs $0.45 est.); next ~2027-01-27 (estimate) |
| SPY / QQQ | — none — | — | — | — | ETFs; no earnings |

- NVDA date/timing FACT: confirmed by Nvidia's Oct 28 press release and the Nasdaq earnings calendar API (day-by-day sweep Nov 9–21 — NVDA the only watchlist hit); Yahoo calendarEvents agrees, `isEarningsDateEstimate: false`. Fiscal Q3 2027, quarter ended Oct 25, 2026. First full reaction session: Wed Nov 18.
- Expectations FACT: consensus revenue ~$108.98B (range $104.94–$116.25B); company guidance (Aug 26 call) revenue $108.0B ±2%, gross margin 74.0%, no Data Center compute revenue from China assumed.
- Implied move: Yahoo v7 options chain (cookie+crumb, prices as of Fri Nov 6 close, NVDA $186.64): Nov-20 expiry ATM (185 strike) straddle mid $20.88 = 11.18% of spot (call IV ~73%, put IV ~71%). Pre-earnings Nov-13 expiry straddle $12.65 = 6.78%. Variance-subtracting the baseline gives ~8.9% event-isolated — INFERENCE, the desk's calculation, not a market quote.
- Historical move FACT (secondary source, Motley Fool Nov 2, 2026): last 10 reports moved "about 5% up or down on average"; revenue beat the top of management's guided range in all 10; EPS beat in 8 of the last 8. Direction UNVERIFIED — no directional pattern in the last 10 reports.
- What would change the verdict: a revised guidance print (especially Q4 gross-margin outlook — memory costs flagged as a margin headwind), a Data Center revenue miss vs the $108B guide, or a pre-report options repricing by Nov 16.
- Technique note: no earnings release exists yet inside the window, so the CFA "read the release itself" step has nothing to read this run; the Nov-17 release should be read directly when it drops, not via summaries.
- Sources: Nasdaq earnings calendar API `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`; Yahoo v10 quoteSummary; Yahoo v7 options `query2.finance.yahoo.com/v7/finance/options/NVDA`; Motley Fool 2026-11-02; Zacks NVDA earnings calendar; Gekko NVDA page. All accessed Sat 2026-11-07.

## 2. Dividend Opportunity desk — COMPLETE

Window: next 4 weeks, through ~2026-12-05.

| Ticker | Ex-date | Amount | Record | Pay date | Yield | Flag |
|---|---|---|---|---|---|---|
| AAPL | Thu 2026-11-12 | $0.27/qtr | 2026-11-12 | 2026-11-16 | 0.31% (Nasdaq) | No change — flat vs Aug/May 2026 |
| MSFT | Thu 2026-11-19 | $0.98/qtr | 2026-11-19 | 2026-12-10 | 0.68% (Nasdaq — see caveat) | **INCREASE — $0.91 → $0.98 (+7.7%), declared 2026-09-15** |

- AAPL FACT (Nasdaq dividends API, pulled 2026-11-07): declared 2026-11-02, $0.27, ex 11/12, pay 11/16. Unchanged from May and August 2026 payments; the 2026 raise was $0.26 → $0.27, declared 2026-04-30. Capture window closes at the Nov 11 close.
- MSFT FACT: 24 consecutive annual increases per the standing count standard (`~/workspace/hedge-desk-research/dividend-count-standard.md`), including the Sep 15, 2026 raise to $0.98/qtr; initiated 2003, no skipped year. Caveat FACT: Nasdaq's header "annualized dividend $3.64 / yield 0.68%" is stale — $3.64 = $0.91 × 4, the pre-raise rate. Forward annual at the declared rate is $3.92 ($0.98 × 4). Do not use Nasdaq's 0.68% as the forward yield.
- NVDA FACT: no dividend declared for the December quarter as of 2026-11-07. Last ex 2026-09-10, $0.25, paid 2026-10-01. INFERENCE: next ex likely early December on cadence (Dec 5, 2024 and Dec 4, 2025) — UNDECLARED and UNVERIFIED until the board acts, typically declared with Q3 FY2027 results in late Nov. FACT (issuer-confirmed): the May 18, 2026 board action raised the quarterly dividend 25×, $0.01 → $0.25, first paid Jun 26, 2026 (NVIDIA May 20, 2026 results release; Form 10-Q for the quarter ended Apr 26, 2026).
- TSLA FACT: pays no dividend; Nasdaq dividends API returns an empty history.
- SPY FACT: last ex 2026-09-18, $1.8888, paid 2026-10-30. Next ex Dec 18, 2026 — OUTSIDE the window (projected/estimated, not yet declared). Amount UNVERIFIED. Wall Street Horizon also lists a 2026-12-31 "XOTH" entry — a possible year-end extra distribution, amount unknown, UNVERIFIED.
- QQQ FACT: last ex 2026-09-21, $0.75143, paid 2026-10-08. Next ex Dec 21, 2026 — OUTSIDE the window (projected, not yet announced). Amount UNVERIFIED: third-party estimates conflict ($0.790 vs $0.794).
- Cuts: none announced. Specials: none announced.
- Method gaps (flagged, not dropped): Nasdaq `api/calendar/dividends?date=2026-11` and `?date=2026-12` returned 0 rows — endpoint unusable this run. Yahoo v8 chart `events=div` returned empty events for all six tickers — not usable as a cross-check. Nasdaq per-symbol endpoints worked for AAPL/MSFT/NVDA/TSLA and QQQ (ETF); SPY returns "Symbol not exists" (NYSE Arca listing) — SPY figures from Wall Street Horizon/TipRanks instead.
- What would change the verdicts: NVDA declaring its December dividend; SPY/QQQ December amounts when State Street/Invesco declare; any new AAPL/MSFT declaration (next raises not expected until spring / September on cadence).
- Sources: `https://api.nasdaq.com/api/quote/{AAPL,MSFT}/dividends?assetclass=stocks`; https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx; https://wallstreethorizon.com/spy-dividend-calendar; https://wallstreethorizon.com/qqq-dividend-calendar; https://www.tipranks.com/etf/spy/dividends; https://www.tipranks.com/etf/qqq/dividends.

## 3. Overnight Premium desk (IV) — COMPLETE

IV inputs file: `~/workspace/hedge-desk-research/nightly/2026-11-07-iv-inputs.json`, as_of **2026-11-07T06:55:17-08:00** — within the 26h freshness guard (file ~6.5h old at run start), no failures. STALE label applies to levels (morning file, market now closed); supplemented with a labeled live pull below.

### IV table (nearest expiry Mon 2026-11-09, DTE 2)

| Symbol | ATM IV (morning file) | Realized 20d | Realized ex-driver day | Max-day share | IV-vs-realized verdict |
|---|---|---|---|---|---|
| SPY | 18.0% | 20.8% | 13.4% | 62.6% | **WINDOW-CONTINGENT** — IV below headline realized, above ex-driver realized |
| QQQ | 26.3% | 33.6% | 25.0% | 50.4% | **WINDOW-CONTINGENT** — IV ≈ ex-driver realized |
| AAPL | 22.8% | 25.9% | 17.2% | 55.8% | **WINDOW-CONTINGENT** — IV above ex-driver realized |
| MSFT | 27.1% | 35.7% | 26.0% | 45.8% | **WINDOW-CONTINGENT** — plus cross-source gap (below) |
| NVDA | 49.8% | 49.1% | 37.0% | 49.3% | **WINDOW-CONTINGENT** — IV ≈ headline realized, well above ex-driver |
| TSLA | 49.4% | 59.4% | 42.4% | 51.3% | **WINDOW-CONTINGENT** — IV below headline, above ex-driver |

Realized window 2026-10-12 to 2026-11-06 (20 closes, 19 log returns). All six symbols WINDOW-CONTINGENT.

### Stale-jump screen — driver days (FACT, Yahoo v8 chart)

- Thu 2026-11-05 selloff drives four windows: SPY −4.51%, QQQ −6.71%, NVDA −9.72%, TSLA −11.40% (log returns).
- Wed 2026-11-04 rally drives two: AAPL +5.17%, MSFT +6.47%.
- INFERENCE: the "IV < realized" read on SPY/QQQ/TSLA is an artifact of the Nov 5 print, not evidence premium is cheap.

### Live supplement (labeled)

- Yahoo v7 options: EMPTY on Saturday. Cookie+crumb handshake worked (crumb fetched), but the default response and the `?date=` re-fetch for 2026-11-09 both returned 0 calls / 0 puts for all six symbols (attempted 13:27 PT). Genuine dead end on Yahoo today — not an auth failure. FACT, source: `https://query1.finance.yahoo.com/v7/finance/options/{SYM}`.
- Fallback — CBOE delayed quotes, fetched live Sat 13:28–13:29 PT (`https://cdn.cboe.com/api/global/delayed_quotes/options/{SYM}.json`): full chains, Friday-2026-11-06-close marks. ATM IV (mean call/put IV, 2026-11-09 expiry): SPY 17.8%, QQQ 26.7%, AAPL 22.8%, MSFT 25.3%, NVDA 49.8%, TSLA 48.9%. Corroborates the morning Yahoo prints within ~0.5pp for five names. FACT — but these are Friday-close marks, not Saturday prints; the market is closed, so no live Saturday IV exists.
- MSFT discrepancy — UNVERIFIED: CBOE 25.3% vs morning Yahoo 27.1% (−1.8pp), the only material cross-source gap. Both are Friday-close marks from different solvers; do not treat either as the truer print. No clean MSFT IV level until Monday's live chain.

### Term structure (CBOE, Friday-close marks; FACT)

ATM IV by expiry — 11-09 (DTE 2) / 11-13 (DTE 6) / 11-20 (DTE 13): SPY 17.8 / 23.2 / 22.0 — QQQ 26.7 / 34.8 / 33.3 — AAPL 22.8 / 28.7 / 27.8 — MSFT 25.3 / 32.0 / 32.4 — NVDA 49.8 / 61.0 / **71.8** — TSLA 48.9 / 59.1 / 56.5.
INFERENCE: every name slopes up sharply from the 2-DTE Monday expiry into the following week — near-term premium is depressed relative to next-week premium, consistent with the market having just absorbed the Nov 4–5 two-day swing and the Monday expiry carrying only weekend theta. NVDA's 11-20 print (71.8%) is the stand-out: it straddles the Nov 17 earnings event.

### IV rank and earnings warnings

- IV rank: UNVERIFIED for all six names. No free source (Yahoo/CBOE) supplies IV history or a 52-week IV range, so no rank can be computed. No name is flagged as "elevated IV rank" on a rank basis. Cross-sectional observation only (INFERENCE): single-name near-term IV (NVDA/TSLA ~49–50%) runs ~2.7× SPY's 18%, normal single-name vs index dispersion, not by itself an elevation signal.
- NVDA earnings Tue 2026-11-17 (FACT, Nasdaq calendar via iv-inputs file). The 11-20 expiry (71.8% IV) prices the event; the 11-13 expiry (61.0%) does not. Premium into the Nov 17 binary event = avoid. No other watchlist name has earnings within 45 days (FACT, same Nasdaq sweep).
- DTE-2 Monday expiry (2026-11-09): no binary event inside the window for any name (FACT). Weekend/overnight premium into Monday is a pure two-calendar-day theta carry, not an event trade.
- Skew note: morning Yahoo file shows SPY call IV 19.4% > put IV 16.6%; CBOE shows SPY call 17.77% ≈ put 17.80% (flat). The SPY call-put gap is not corroborated across sources — treat as UNVERIFIED.
- What would change the verdicts: Nov 5 (SPY/QQQ/NVDA/TSLA) and Nov 4 (AAPL/MSFT) rolling out of the 20d window (~Dec 3–4); a live Monday chain after the 11-09 expiry (resolves the MSFT gap); NVDA earnings Nov 17 resolving (collapses the 11-20 premium); an IV-history source (required before any IV-rank flag).

## 4. Open Quant/AI Model Lab — COMPLETE

Sweep coverage: arXiv q-fin window Nov 6–7 is genuinely empty — filtered leg returned 0, and the no-filter control confirms the newest q-fin item is still 2026-11-05 (2611.07464, already #221). Saturday window; arXiv announces weekdays. GitHub leg skipped per the run's no-GitHub-operations rule. Web-search legs covered vol/earnings/dividend/purged-walk-forward angles. No TEST/INTEGRATE movement.

### New candidates (scored with the repo scorer, not hand-computed)

**#233 — Gene Yu, "How Much Evidence Does a Backtest Really Have?" — score 49 → WATCH**
- Source: https://zecrilox.com/paper.pdf — self-hosted PDF, Sep 2026, full paper read at source (1,144 lines). No arXiv/SSRN ID, no peer review, no code link in the paper.
- What it is (FACT — paper read): measured case study of one RF+XGBoost system on 162 ETFs/stocks/indices in 8 factor categories, shared calendar split with 126-session embargoes, evaluation protocol fixed in code before the final test.
- Findings (source-reported, UNVERIFIED — not independently reproduced): per-ticker splits leak up to 52% of test rows; naive standard errors 2–3× too small for small-cap ETFs; peak label yields 2.3–3.1× more positives than the median label; whole price history holds only 53–99 independent outcomes per category at 3–6 month holds (26–49 at 6–12 months); effective series per category 1.04–2.35 via Kish design-effect counting. Honest negative: OOS ROC-AUC up to 0.90, yet only 2/8 categories produce a rule and neither beats ignoring the model. One result crossed the bar only because a probability floor was rounded to 6 decimals.
- Reproducibility NOT established: data frozen 2026-09-04 with SHA-256 manifest but not distributed; re-download does not reproduce (adjusted-price revisions); one screen applied by hand-edit, "cannot be reproduced from the repository" (paper's own words — a repository is implied but not linked).
- Scorer inputs: signal 4 / data 3 / impl 2 / risk 4 / cred 2, reproducible False. Reasons: MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED, LICENSE_REVIEW_REQUIRED.
- Follow-up: re-check for a code repo / arXiv deposit; apply the effective-series count + shared-calendar-split check to any desk backtest pooling correlated names.

**#234 — QuantJourney Backtester point-in-time observation layer — score 43 → ARCHIVE**
- Source: https://quantjourney.substack.com/p/beyond-price-data-sentiment-ml-predictions — maintainer announcement (Substack), published 2026-11-05, read at source. Repo contents + license NOT verified (GitHub leg banned).
- What it is (article-reported, UNVERIFIED): ObservationData / ObservationBacktester layer — data_date / observed_at / decision_at triple, latest observation strictly before the cutoff, freshness checks, missing stays missing, provenance + input hashes in run_metadata.json; Adanos sentiment adapter; synthetic 2-year AAPL example; single instrument in weight mode only. Apache 2.0 claimed in the article, NOT verified at source.
- Scorer inputs: signal 3 / data 2 / impl 3 / risk 3 / cred 2, reproducible False. Reasons: INSUFFICIENT_CURRENT_VALUE, REPRODUCIBILITY_NOT_ESTABLISHED, LICENSE_REVIEW_REQUIRED. ARCHIVE on band discipline (secondary-source evidence only, no verified code, no multi-instrument support).
- Method idea noted for the purged-walk-forward lane: the triple-timestamp + provenance-hash pattern complements #204 (QBX availability effects) and #85. Reopen if the repo verifies (Apache 2.0 + tests) and multi-instrument support lands.

### Ledger

Both rows appended to the latest table in `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#233, #234) and a run note added to the kaizen log. Verified on disk by re-reading. No duplicates: AddMart #112, Jin/Agarwal #31, Bastola #157, Buchegger #9 re-surfaced by search and confirmed already ledgered.

### Triage exclusions (no ledger rows)

Crypto scope: Bitcoin paper-trading agent (Medium), Suleyman040/options-analytics (Deribit BTC), Grok-bot crypto stack. Secondary explainers with no new release: backtest-overfitting pieces. Portfolio-allocation lane: Medium walk-forward HMM/HRP/Black-Litterman engine. No distributable artifact yet: Jonas Löffler Volatility Lab (pre-registered SPX vol forecast still planned). Already excluded 2026-10-17: anthonymakarewicz/volatility-trading (ORATS paid-data gated). #207 author's Substack is commentary on an already-ledgered item.

## 5. Weather/War/Logistics Futures Event desk — COMPLETE

All prices Yahoo Finance v8 chart (front-month), Friday Nov 6 closes unless stated. Sources checked 13:26–13:45 PT.

| # | Event | Date | What happened / expected | Futures-curve read | Watchlist relevance |
|---|---|---|---|---|---|
| 1 | US midterms → Iran de-escalation pricing | Tue Nov 3–Wed Nov 4 | Democrats won both chambers of Congress. Brent fell ~8% on Wed Nov 4 alone to two-month lows; Iran reportedly sent a nuclear proposal to Washington via Qatar (Reuters, via CNBC). FACT | Brent Jan settled $98.32 Fri Nov 6, WTI Dec $90.83; full week Brent −16.4% ($117.64 → $98.32), WTI ~−13% — steepest weekly Brent drop since Covid, largest absolute weekly fall in LSEG data back to 1988 (Reuters). Mon→Fri: Brent −6.2%, WTI −5.8%. Curve is pricing a peace-deal supply return, not a shortage. | Indirect, high. Lower oil removes an inflation headwind for SPY/QQQ, but the move is a binary geopolitical repricing, not a fundamentals trend — it can reverse in one headline (see #2). |
| 2 | Hormuz escalation — tanker attacks + Saturday explosions | Thu Nov 5 – Sat Nov 7 | Iran reported three more tankers attacked in the Strait of Hormuz on Thu Nov 5 (Reuters). Hormuz shipping flows below 60% of normal capacity (Reuters). Sat Nov 7 (today, after market close): explosions heard on Qeshm Island and at Jask; Tasnim says two missiles struck Qeshm; cause unclear; US had carried out limited strikes on the island days earlier (Reuters, 1h ago). FACT for the attacks/explosions; UNVERIFIED whether Saturday's blasts were a new US strike — no official confirmation of source. | Thu–Fri rebound (+~$4 Brent off the $93.65 Thu low) put a floor under the selloff; war premium is being cut, not eliminated. Sunday-evening reopen is the test: a gap-up would confirm the market still prices Hormuz disruption risk. | Indirect, high. A Hormuz closure scenario is the single largest tail for SPY/QQQ energy-cost and inflation pricing. No watchlist name is directly exposed; the channel is macro (oil → CPI → rates). |
| 3 | EIA Weekly Petroleum Status Report | Wed Nov 4, 10:30 ET (w/e Oct 30) | Crude −0.9 Mbbl to 409.8 Mbbl (5th straight draw; ~4% below 5-yr avg; Reuters poll had expected a build). Gasoline −0.2 Mbbl. Distillate −3.6 Mbbl to 99.3 Mbbl — lowest since May 2003, 13% below 5-yr avg. Refinery utilization 94.5%. Total commercial petroleum −8.2 Mbbl. SPR 282.2 Mbbl. FACT (EIA via Morningstar/Rigzone/OilPrice). | Bullish inventory print was completely overwhelmed by the de-escalation repricing. Distillate tightness is the real physical story: diesel/heating-oil buffer at a 23-year low heading into winter, while crude itself is only modestly below average. | Low direct; distillate tightness is a winter heating/logistics cost input, not a watchlist driver. |
| 4 | EIA Weekly Natural Gas Storage | Thu Nov 5 (w/e Oct 30) | Injection +77 Bcf vs +81 Bcf expected (WSJ survey) and +61 Bcf 5-yr avg. Storage 3,801 Bcf: +1.4% vs 5-yr avg, −2.8% y/y. FACT (EIA via Morningstar/FXEmpire). | Front-month Dec nat gas $2.998 Fri (Yahoo), +5.0% Mon→Fri on cooler forecasts, but still soft: Dec contract below its 20-day MA; deferred Apr testing multi-month lows — curve pricing ample winter supply, not scarcity. | Negligible direct. |
| 5 | BLS October Employment Situation | Fri Nov 6, 8:30 ET | Payrolls +165K vs ~65K expected (Reuters poll); unemployment 4.1% (from 4.2%); AHE +0.4% m/m, +3.1% y/y; Aug/Sep revised up +84K combined. FACT (BLS USDL-26-1632). Dec Fed hike odds rose to ~78–80% (CME FedWatch/LSEG) — corroborated by coordinator check of Invezz, Nov 6 (see synthesis item 3). | Gold sold off on the print (Kitco) but front-month gold still closed the week $4,074.90, +2.65% Mon→Fri (Yahoo) — haven bid from Hormuz outweighed the hawkish jobs read. | Indirect, material. A December hike repricing is a headwind for long-duration growth (NVDA, TSLA, AAPL, MSFT) via the discount-rate channel. |
| 6 | USDA Nov WASDE + Crop Production | Tue Nov 10, 12:00 ET (11:00 CT) — ahead | Analyst averages (Pro Farmer): corn yield 180.6 bu/ac (vs 181.2 Oct), production 15.979B bu; ending stocks corn 1,846.2M bu, soy 332.2M bu (range 280–404M — widest spread, biggest wildcard), wheat 744.1M bu. USDA is adding AI pre-release data checks after earlier corn-estimate errors (USDA Under Secretary Hutchins). FACT that the report is scheduled and these are the consensus figures; the outcome itself is SPECULATION until release. | Corn front-month 441.5¢, −1.5% Mon→Fri; soybeans 1,193.75¢, −0.9% (Yahoo) — quiet ahead of the report; no pre-positioning visible in front-month prices. | Negligible direct. |
| 7 | EIA STEO + OPEC Monthly Oil Market Report | Tue Nov 10 (STEO) / Wed Nov 11 (OPEC) — ahead | EIA Oct 6 STEO: global inventory draws 1.9 Mb/d Q3, forecast 0.7 Mb/d Q4. JPMorgan (Nov 4): supply exceeded demand by 1.1 Mb/d in Sep, widening to 1.4 Mb/d in Oct. FACT as reported. | If STEO/OPEC confirm a widening surplus, it supports the lower-price regime; if either flags Hormuz-related supply loss, expect a sharp reversal. What would change the read: a Hormuz transit halt or a formal US–Iran deal announcement. | Indirect (see #1). |

### Week-ahead calendar (all ET)

- Mon Nov 9: USDA Crop Progress (weekly).
- Tue Nov 10, 8:30: US October CPI (BLS). Tue Nov 10, 12:00: USDA WASDE + Crop Production. Tue Nov 10: EIA Short-Term Energy Outlook.
- Wed Nov 11: Veterans Day — OPEC Monthly Oil Market Report due; EIA weekly petroleum report shifted to Thu Nov 12, 12:00 ET (FXEmpire/EIA notice).
- Thu Nov 12, 12:00: EIA Weekly Petroleum Status Report (w/e Nov 6). Fri Nov 13: next EIA natural gas storage report (date conflict between sources — FXEmpire's storage page says Fri Nov 13, Natural Gas Brief says Thu Nov 12; UNVERIFIED which day).

### Futures snapshot (Yahoo v8 chart, Fri Nov 6 closes)

| Contract | Close | Mon→Fri |
|---|---|---|
| WTI crude CL=F | $90.83 | −5.8% |
| Brent BZ=F | $98.32 | −6.2% |
| Nat gas NG=F | $2.998 | +5.0% |
| Gold GC=F | $4,074.90 | +2.65% |
| Corn ZC=F | 441.5¢ | −1.5% |
| Soybeans ZS=F | 1,193.75¢ | −0.9% |

Term structure: UNVERIFIED. Deferred-contract Yahoo symbols (CLF27, CLM27, BZF27, NGZ26, etc.) returned no data in this run, so curve shape (backwardation/contango) cannot be verified from a primary source. Not inferred from front-month moves alone.

### Verdicts (with what would change them)

1. The oil market is pricing de-escalation, but the physical facts point the other way. Distillates at a 23-year low, five straight crude draws, Hormuz flows <60% of normal, and fresh Saturday explosions — the −16% week is a sentiment repricing of a possible deal, not a supply glut clearing. INFERENCE. What would change it: a signed US–Iran agreement (would confirm the lower-price regime) or a Hormuz transit halt (would reverse it violently).
2. No direct watchlist catalyst this week. No watchlist name is an energy or ag producer; the transmission is macro only (oil → CPI Tue → Fed hike odds → growth multiples). FACT (watchlist composition) + INFERENCE (transmission channel).
3. Tuesday Nov 10 is the week's hinge: CPI 8:30 ET + WASDE 12:00 ET + STEO same day. FACT (schedules confirmed on BLS/USDA/EIA calendars via sources below).

### Notes / gaps

- No federal data blackout: EIA and BLS released on schedule this week (Nov 4, 5, 6), consistent with the standing verified fact that the CR funds the government through Dec 11. No shutdown framing applies.
- Abu Dhabi Nov 10–11 trilateral peace talks and overnight Russian strikes on Kyiv's grid appear only in low-credibility single sources (Substack newsletters) — UNVERIFIED, excluded from verdicts.
- No material weather/logistics disruption beyond Hormuz identified in the last 48h; no USDA report was released in-window (last was Oct 9 WASDE).

Sources: EIA Weekly Petroleum Status Report (w/e Oct 30, released Nov 4): https://www.morningstar.com/news/dow-jones/2026110410540/us-crude-oil-stockpiles-post-fifth-straight-weekly-drop ; https://www.rigzone.com/news/usa_oil_stocks_drop_by_almost_1mm_bpd_week_on_week-06-nov-2026-185033-article/ ; EIA Weekly Natural Gas Storage (w/e Oct 30, released Nov 5): https://www.morningstar.com/news/dow-jones/2026110516493/oil-prices-stay-below-100-as-traders-weigh-iran-diplomacy-supply-outlook-commodities-roundup ; Oil price action / Hormuz: https://985theriver.com/2026/11/05/oil-set-for-sharp-weekly-drop-but-middle-east-supply-concerns-provide-floor/ ; https://financefeeds.com/brent-crude-oil-price-98-32-saturday-week-ahead-us-iran-deal-bets-cpi-10-november-bull-105-bear-93/ ; Saturday Qeshm explosions: https://www.reuters.com/world/middle-east/explosions-heard-irans-qeshm-island-iranian-media-reports-2026-11-07/ ; USDA Nov WASDE preview: https://www.profarmer.com/news/agriculture-news/november-wasde-why-soybeans-are-biggest-wildcard ; BLS Oct Employment Situation (Nov 6): https://www.kitco.com/news/article/2026-11-06/gold-prices-see-some-selling-pressure-us-economy-created-165k-october ; Futures closes: Yahoo Finance v8 chart, pulled directly 2026-11-07 ~13:40 PT (CL=F, BZ=F, NG=F, GC=F, ZC=F, ZS=F).

## 6. Box/Parity Observer — COMPLETE

Bottom line: no new parity violation; one new index-methodology item worth a line.

- S&P DJI style-index methodology change (FACT, announced 2026-10-28; effective before open Mon 2026-12-21; pro forma files from Fri 2026-12-04): S&P Dow Jones Indices is revising its U.S. growth/value classification — growth drops 12-month price momentum (ranks on 3-yr EPS change vs price and 3-yr sales-per-share growth only); value adds free-cash-flow-to-price and an intangibles-adjusted book-to-price, and averages trailing with 1-yr forward earnings-to-price. Applies to S&P 500 / Composite 1500 / MidCap 400 / SmallCap 600 / S&P 900 / S&P 1000 style indices. Source: S&P DJI announcement via Benzinga/TradingView, 2026-10-28. Relevance (INFERENCE): style-index reconstitution only — no change to S&P 500 membership, weighting, or SPX option mechanics, so no parity implication; watchlist impact is limited to possible IVW/IVE-style ETF rebalancing flows around Dec 4–21. Note: announced Oct 28, so not new this week — flagged here because it is the only new methodology doc in the sweep window.
- Put-call parity holding (FACT, Saxo Options Brief, 2026-11-04): put-call parity on the 18 Nov SPX options at Tuesday's close returned 19.96, in line with the 19.90 settlement — no violation indicated. Source: home.saxo, 2026-11-04.
- No new published parity-violation analysis found (FACT, as of this sweep): no new box-spread or index-parity violation study surfaced in the Nov 2026 window. Background only, not new: arXiv preprint "The Cost of a Free Lunch" (Shin, 2026-08-24) finds SPX/RUT quoted parity residuals tightly clustered near zero vs traded futures, with a systematic ~37 bp median carry gap vs OIS — i.e., no exploitable price-space violation, only a carry-space enforcement wedge.
- Box-spread context (FACT, CBOE, 2026-03-12): CBOE's SPX box-spread explainer stands unchanged; no update since March. SPX boxes remain the clean European-style, cash-settled parity vehicle; American-style SPY/QQQ boxes still carry early-assignment risk (INFERENCE: no change to desk guidance — use SPX only for box/parity reads).
- Verdict: nothing actionable. No parity violation to exploit; parity math holds on the latest check. No desk action.
- Sources checked (2026-11-07 ~13:30 PT): S&P DJI growth/value announcement (2026-10-28, via TradingView/Benzinga); Saxo Options Brief 2026-11-02 and 2026-11-04; CBOE SPX box-spread post (2026-03-12); arXiv 2604.19604 (2026-08-24); Optionly arb scanner snapshot 2026-11-07 (crypto venues only, no equity-index signal).

## 7. Bonds & Rates desk — COMPLETE

Module run: SUCCEEDED. `rates_desk.rates_environment()` returned mode `REAL_FRED_RATES`, schema `hedge-desk-rates-desk-1.0.0`, source `fred-public-csv-http-200`. As-of 2026-11-07; latest observations **2026-11-05** (Thursday) — Friday Nov 6 FRED data was not yet in the pull. No Yahoo substitution was needed or used.

1. Fed funds effective rate — 3.88% [FACT — FRED DFF via module, obs 2026-11-05]. Module's `fed_funds_change_over_window` field reads +0.25 over the 60-day window; reported verbatim but not independently endorsed as to sign convention — the level (3.88%) is the verified number.
2. 10Y / 2Y levels — 10Y 4.84%, 2Y 4.46% [FACT — FRED DGS10/DGS2 via module, obs 2026-11-05]. Both fell on the day: 10Y −6bp (4.90 → 4.84), 2Y −12bp (4.58 → 4.46).
3. 2s10s slope — +38bp, UPWARD_SLOPING, steepening at the margin [FACT — arithmetic on module history arrays]. Spread was 32bp on Nov 4 → 38bp on Nov 5 (+6bp in a day, driven by the front end rallying twice as fast as the long end). Context: ~37bp a week ago (Oct 29), ~41bp at the 60-day window start (Sep 8) — so the curve is essentially flat-to-slightly-flatter over the window, with the latest move a one-day steepening, not a trend break.
4. SOFR vs EFFR spread — +4bp (SOFR 3.92% vs EFFR 3.88%, OBFR 3.88%, all obs 2026-11-05) [FACT on levels; INFERENCE on the read]. A 4bp SOFR–EFFR gap is narrow — no funding-stress signal. The three overnight benchmarks are effectively pinned together at the policy rate.
5. Directional read for premium pricing [INFERENCE — follows from the verified levels, not a forecast]: long rates remain elevated (10Y 4.84%): higher discount rates continue to pressure growth multiples — a headwind for long-duration premium selling on growth names, and no relief in the cost of carry. The front-end rally (2Y −12bp in a day, −26bp since Oct 29's 4.61%) with the long end holding firmer is consistent with the market pricing further policy easing at the front while term premium stays sticky at the long end. If that steepening persists, it favors shorter-dated premium structures over long-dated ones, all else equal — but one day of steepening is not a regime call.

Yield labeling: ^TNX is the 10Y, ^FVX is the 5Y — never labeled ^FVX as 2Y. 13W bill is the front-end anchor, labeled explicitly as 13W, not 2Y.

What would change these verdicts: Friday Nov 6 FRED observations (absent from this pull) — could narrow or reverse the +6bp steepening; a hot CPI/jobs print or a hawkish Fed speaker repricing the front end upward would flatten the curve and lift the 2Y back toward the 10Y; a SOFR–EFFR spread widening beyond ~10–15bp would flip the funding read from "no stress" to "watch."

Note (coordinator): the Nov 6 jobs print (+165K) postdates this pull and repriced December hike odds to ~77–80% (see synthesis item 3) — the front-end easing read above is a Nov 5 snapshot, superseded in part by the Nov 6 print. Tuesday's CPI is the next repricing event.

---

## Run notes

- All seven desks delivered. No desk FAILED; no desk retried. No git operations of any kind.
- IV inputs file as_of 2026-11-07T06:55:17-08:00, within the 26h guard; live Yahoo options chains were empty on Saturday (dead end, not auth failure) with CBOE delayed quotes as the labeled fallback.
- Cross-desk conflict resolved: Futures desk's Dec hike-odds claim (~78–80%) vs Rates desk's front-end easing read — resolved by dating: the 2Y rally was Nov 5, the hike repricing followed the Nov 6 jobs print; corroborated by Invezz (Nov 6, citing CME FedWatch, ~77%, up ~10pp).
- Government data on schedule: EIA (Nov 4, 5) and BLS (Nov 6) released normally; CR funds the government through Dec 11. No shutdown framing applies.
- Quant lab ledger updated with #233 (WATCH, 49) and #234 (ARCHIVE, 43).
