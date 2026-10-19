# Hedge-Desk Daily Research — Mon 2026-10-19

**Run:** daily research, 1:30pm PT slot (post-close: quotes are Monday Oct 19 regular-session closes). Research + input only — no git, no PRs, no code changes.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; never risk-seeking framing.
**Evidence standard:** every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it.
**Market-data rule:** Yahoo first, Nasdaq second, fallbacks after. Yahoo calls sent with `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`.
**FRED:** module observations dated Oct 16 (normal one-business-day publication lag — not stale).
**Government-data rule:** no federal shutdown (CR through Dec 11, per standing rule); EIA weekly and Oct WASDE released on schedule. The stale `brief-correction-2026-10-05.md` shutdown framing is not applied.
**Synthesis note:** no desk failed; no desk was dropped. All desks returned output. Two cross-desk discrepancies resolved below (CPI headline conflict; Oct-FOMC odds conflict).

## Top 5 decision-relevant items (synthesized)

1. **TSLA Wed Oct 21 AMC is the dominant near-term event — premium into it is a binary, not an edge.** Front-expiry (Oct 23) ATM IV is 0.687 vs 0.443 thirty days out — the single steepest event hump on the board (FACT, Premium desk live pull 13:27 PT). The straddle implies ±6.41% while TSLA's last 8 realized reactions averaged 7.77% — the only watchlist name where the market prices *less* than history delivered (FACT, Earnings desk; both desks corroborate the hump). Direction is a coin flip (4 up / 4 down, last two both negative). Desk rule: premium into this binary = avoid.
2. **AAPL's event premium looks rich vs its own history — the clearest mispricing signal on the board.** Options imply ±5.31% (Nov 6 expiry straddle, first after the Nov 2 print) against an 8-quarter realized average of 2.46% — ~2.2× historical reaction, and 6 of 8 prints were down-but-small (FACT, Earnings desk). INFERENCE: premium overpriced on realized history — *unless* the Jul-26 print (−7.35%, largest in the sample) marks a genuine volatility-regime shift in AAPL prints (AI/iPhone narrative sensitivity) rather than an outlier. Only subsequent prints tell.
3. **SPY is the only clean event-free rich-premium read.** 30d ATM IV 14.25% vs trailing 20-day realized 9.0% (+5.3pp), NOT window-contingent, no earnings anywhere near (FACT). QQQ/AAPL/MSFT/TSLA verdicts are all WINDOW-CONTINGENT (single day >30% of 20-day realized variance), and NVDA's +15.6pp spread is event-justified (11-18 earnings inside the Nov-20 expiry) — arithmetic stands, no mispricing implied.
4. **Rates: discount-rate headwind persists but is no longer intensifying; Oct 27–28 FOMC is live and unpriced.** EFFR 3.88% (mid-range of 3.75–4.00%), 10Y 5.09% (−22bp from the Oct 5 local high of 5.31%), 2s10s +35bp flattened from 50bp over 60 days, SOFR−EFFR 0bp = funding plumbing normal (all FACT, FRED module). Chair Warsh refused to signal the October decision (Oct 16, IMF Bangkok); Sept minutes show most participants see another hike likely by year-end. Hot CPI supports the hike case — but see the conflict below.
5. **Hormuz escalation is the dominant macro catalyst; crude front-loaded tight, diesel squeeze worsening.** WTI $98.49 / Brent $108.43 (front-month, −2.9%/−1.3% Monday on Trump Russia-sanction-waiver news, not on flow normalization); the ~$10 WTI–Brent spread signals tight *seaborne* supply vs looser US domestic (FACT/INFERENCE, Futures desk). EIA Thursday draw −8.6M bbl to 415.6M (partly Hurricane Isaias, transient); distillates 12% below 5-yr avg; IEA emergency diesel release covers <4 days of the Hormuz shortfall (press-reported). Spot above EIA's $105 Q4-average Brent forecast = market pricing front-loaded tightness.

## Cross-desk discrepancies — resolved

- **CPI headline conflict (reported, not smoothed):** Sept CPI released Oct 14. Core CPI +2.6% y/y vs 2.5% est. = FACT per Reuters reporting of Labor Department data (broad-based: software +28% y/y, record toy-price rise — corroborated across outlets). The **headline y/y number is UNVERIFIED at the single-number level**: Reuters/Investopedia print 3.7% vs 3.6% est; OppHub prints 3.4% citing the same release. Both secondaries, no BLS primary check yet this run — follow-up scheduled for the next run.
- **Oct-FOMC odds conflict:** one secondary (invezz) prints Oct hold odds ~84% / Dec hike odds 85–92%; economists Sharif (Inflation Insights) and Aleman (Raymond James) via Reuters say the broad-based hot CPI raises the *October* hike probability — near coin-flip. Basis for market-odds numbers UNVERIFIED; economist read FACT-per-Reuters. No desk verdict rests on either.
- **AAPL declaration timing:** Dividend desk's "~Oct 29–30 declaration" was a 2025-calendar pattern expectation, superseded by the Earnings desk's package-standard resolution (Oct 17): AAPL prints Mon Nov 2 AMC per the Nasdaq calendar. INFERENCE: the dividend declaration (unannounced; $0.27 last declared 07/30, ex 08/10) is expected with that release, not on a standalone Oct 29–30 date. What would change it: a declaration announcement this week.
- **NVDA earnings date:** Nov 18 per Nasdaq calendar (Earnings desk, FACT for the date; timing still UNVERIFIED — secondaries disagree Nov 17/25).

---

## 1. Earnings Event desk

**In-window (through ~Nov 2):** TSLA Wed Oct 21 AMC; MSFT Wed Oct 28 AMC; AAPL Mon Nov 2 AMC. NVDA Nov 18 — out of window. SPY/QQQ: indices, no earnings.

| Name | Date | Timing | Options-implied move | Method (FACT — real chains) | Hist. avg reaction-day move (n=8) |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21 | AMC (Nasdaq `time-after-hours`) | **±6.41%** | ATM 367.5 straddle, Oct 23 expiry; mids 12.20+11.38=23.58 ÷ 368.06 (Oct 19 close) | 7.77% abs avg (4 up / 4 down) |
| MSFT | Wed Oct 28 | AMC (Nasdaq) | **±5.61%** | ATM 532.5 straddle, Oct 30 expiry; 15.90+14.02=29.92 ÷ 533.52 | 7.02% abs avg (3 up / 5 down) |
| AAPL | Mon Nov 2 | AMC (Nasdaq) | **±5.31%** | ATM 345 straddle, Nov 6 expiry; 8.48+9.75=18.23 ÷ 342.94 | 2.46% abs avg (2 up / 6 down) |

Historical detail (FACT — Yahoo daily closes, reaction-day = report-day close → next trading-day close, each report date verified on the Nasdaq calendar):
- **TSLA:** −14.52 (Jul-26), −3.56 (Apr-26), −3.45 (Jan-26), +2.28 (Oct-25), −8.20 (Jul-25), +5.37 (Apr-25), +2.87 (Jan-25), +21.92 (Oct-24). Range −14.5% to +21.9%.
- **MSFT:** +15.51 (Jul-26), −3.93 (Apr-26), −9.99 (Jan-26), −2.92 (Oct-25), +3.95 (Jul-25), +7.63 (Apr-25), −6.18 (Jan-25), −6.05 (Oct-24). Range −10.0% to +15.5%.
- **AAPL:** −7.35 (Jul-26), +3.24 (Apr-26), +0.46 (Jan-26), −0.38 (Oct-25), −2.50 (Jul-25), −3.74 (May-25), −0.67 (Jan-25), −1.33 (Oct-24). Range −7.4% to +3.2%.

**Desk reads (value-investor lens):** (1) AAPL ±5.31% implied vs 2.46% realized avg — premium-rich on history; would change if Jul-26 marks a regime shift (INFERENCE). (2) TSLA implied *below* its 8-qtr realized avg — only name so priced; tail widest (INFERENCE). (3) MSFT reactions skew negative (5/8 down) but magnitude is event-driven, not direction-driven; implied ±5.61% vs 7.02% realized avg. (4) Method caveat: each expiry is 2 sessions post-print, so implied slightly overstates the pure event move — same method all three names, cross-comparison valid. (5) No release yet to tear down under the CFA reading order; TSLA's Oct 21 print is the first eligible teardown (Oct 21/22 run).

**Sources:** Nasdaq calendar API `api.nasdaq.com/api/calendar/earnings?date=2026-10-21|10-28|11-02|11-18`; Yahoo options chains (crumb-authenticated, UA header) exp 2026-10-23 / 10-30 / 11-06; Yahoo daily bars for history.

## 2. Dividend Opportunity desk

**Bottom line: nothing goes ex-dividend in the next 4 weeks.** The only hard upcoming ex-date is MSFT 11/19 ($0.98), 3 days outside the window. No cuts, no specials anywhere on the watchlist.

| Name | Next ex-date in window? | Declared | Yield (FACT, computed from 10-19 closes) | Consecutive increases (per 2026-10-05 standard) | Flags |
|---|---|---|---|---|---|
| AAPL | Not declared — expected with Nov 2 release (see cross-desk resolution) | $0.27/qtr (ex 08/10) | 0.31% ($1.08/$342.94) | **15** consecutive years (initiation 2012; raised every year 2013–2026) | Increase $0.26→$0.27 (+3.8%), 04/30/2026 — FACT |
| MSFT | 11/19/2026 (outside window) | $0.98/qtr (declared 09/15, pay 12/10) | 0.73% ($3.92/$533.52) | **24** consecutive years per standard anchors (raised 09/15/2026) | Increase $0.91→$0.98 (+7.7%), 09/15/2026 — FACT |
| NVDA | None in window (next ~early Dec, pattern INFERENCE) | $0.25/qtr (ex 09/10) | 0.46% ($1.00/$217.09) | **1** (May 2026 raise; flat 2025 broke the prior streak) | **Material increase:** $0.01→$0.25 (25×), 05/20/2026 — FACT (issuer press release); +$80B buyback authorized same day |
| SPY | None (~Dec 18, pattern INFERENCE) | Last $1.88901 (ex 09/18) | 0.99% TTM ($7.583/$766.48) | N/A (ETF) | None |
| QQQ | None (~Dec 21, pattern INFERENCE) | Last $0.75143 (ex 09/21) | 0.43% TTM ($3.091/$718.36) | N/A (ETF) | None |
| TSLA | Never pays — no rows in Nasdaq API, none in Yahoo history | — | — | N/A | FACT: no dividend events ever declared |

**Cross-desk flag (→ Premium desk):** MSFT's 11/19 ex-div sits inside the November monthly options cycle (expiry Fri 11/20); AAPL's expected early-Nov ex-div lands in the same cycle. Dividend-driven early-exercise risk on short in-the-money calls that week — do not treat those cycles as clean.

**Notes:** payout ratios UNVERIFIED (EPS not pulled from primary today); disconfirming check for cuts/specials across all six names found none; Yahoo v7 quote endpoint returned no data — recovered via v8 chart endpoint, no data gap.

**Sources:** Nasdaq quote dividends APIs (AAPL/MSFT/NVDA stocks, QQQ ETF); Yahoo chart API div events + 10-19 closes; NVIDIA Q1 FY27 press release (investor.nvidia.com); ~/workspace/hedge-desk-research/dividend-count-standard.md.

## 3. Overnight Premium desk (IV)

**IV-inputs freshness: file exists and is inside the 26h guard — USABLE (not stale).** `~/workspace/hedge-desk-research/nightly/2026-10-18-iv-inputs.json`, `as_of` = 2026-10-18T13:59:19-07:00 (~23.5h old at this run). **Live supplement (labeled):** Yahoo options API, as-of 2026-10-19T13:27:55-07:00 (post-close Monday quotes), 6/6 symbols succeeded. Baseline expiry (Oct 19, 1 DTE) ≠ live front expiry (Oct 21 / Oct 23 TSLA) — do not read baseline→live as a time series (FACT, method note). IV rank: **UNVERIFIED for all six names** — no free IV-history source; richness judged on the IV-minus-realized proxy only.

| Sym | Live front ATM IV (labeled) | Live 30d ATM IV (Nov-20, labeled) | Live 60d (Dec-18, labeled) | Realized 20d (9/21–10/16) | IV−RV (30d) | Verdict |
|---|---|---|---|---|---|---|
| SPY | 0.116 (Oct-21, 2dte) | 0.1425 | 0.1473 | 0.0900 | **+0.053** | **RICH — clean** (share 0.2104, not contingent); no binary near |
| QQQ | 0.193 (Oct-21, 2dte) | 0.2154 | 0.2154 | 0.1543 | +0.061 | **WINDOW-CONTINGENT** (0.3559) |
| AAPL | 0.220 (Oct-21, 2dte) | 0.2647 | 0.2497 | 0.1646 | +0.100 | **WINDOW-CONTINGENT** (0.3737); Nov-2 earnings inside Nov-20 expiry |
| MSFT | 0.230 (Oct-21, 2dte) | 0.3156 | 0.2948 | 0.2234 | +0.092 | **WINDOW-CONTINGENT** (0.3485); Oct-28 earnings inside Nov-20 expiry |
| NVDA | 0.298 (Oct-21, 2dte) | 0.3925 | 0.3704 | 0.2368 | **+0.156** | **RICH — clean arithmetically, event-explained** (share 0.2458); Nov-18 earnings inside Nov-20 expiry |
| TSLA | **0.687** (Oct-23, 4dte) | 0.4427 | 0.4178 | 0.3001 | +0.143 | **WINDOW-CONTINGENT** (0.3136) **+ binary event 10-21 inside front expiry → AVOID** |

**Term-structure reads (FACT):** SPY normal upward slope 0.116→0.143→0.147, no event hump. QQQ flat back end 0.193→0.215→0.215. AAPL 0.220→0.265→0.250, MSFT 0.230→0.316→0.295 (sharpest, +8.6pp front→30d), NVDA 0.298→0.393→0.370 — Nov humps each containing the name's earnings; elevation event-expected, not "rich" (INFERENCE). TSLA 0.687→0.443→0.418 — extreme front hump collapsing down the curve; prices the Wed earnings event (INFERENCE from event-in-window + hump shape). No parity violations observed; skew unreadable (single-strike call/put IV differences are strike-placement artifacts, not skew reads).

**Spot context Fri→Mon (FACT):** SPY 763.25→766.48 (+0.4%), QQQ 709.80→718.36 (+1.2%), AAPL 343.46→342.94 (−0.2%), MSFT 529.05→533.52 (+0.8%), NVDA 214.13→217.09 (+1.4%), TSLA 354.72→368.06 (+3.8% into earnings).

## 4. Open Quant/AI Model Lab

**Quiet sweep — no TEST, no INTEGRATE this run.** Two new candidates, both scored with `hedge_desk.research_intelligence.assess_source`, both appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (rows #110, #111; table integrity verified at 111 rows):

- **#110 — Burés & Vives, "On the skew-curvature power law relationship in a stochastic vol model with infinite-variation Lévy jumps"** (arXiv:2610.23488v1, 16 Oct, q-fin.MF; https://arxiv.org/abs/2610.23488). Claims: short-time ATM-IV skew/curvature expansions under mixed rough-vol + infinite-variation Lévy dynamics (numerical evidence, source-reported **UNVERIFIED**, no code repo). Score 39 → **ARCHIVE** (below the 45 WATCH band; band discipline, same as #97). Would change: code repo + peer review → rescore.
- **#111 — Kulkarni & Nayar, "From Alpha to Execution: Trading Horizons, Regimes, and Schedules under Concave Impact and Hurst Scaling"** (arXiv:2610.23749v1, 16 Oct, q-fin.MF; https://arxiv.org/abs/2610.23749). Execution-layer theory; outside the seven research lanes (paper-only desk has no execution lane). Score 33 → **ARCHIVE**.

**Material finding (user-visible): PyPI `finlab` is a NAME COLLISION.** The pip name `finlab` (now 2.2.14) is FinLab Taiwan (finlab.finance, a stock-strategy platform), **not** ledger #54 landtml/finlab-ml (the AFML toolkit). The ledger's #54 adoption note said "pin finlab==0.1.5" — a bare `pip install finlab` would pull the wrong package. Poka-yoke logged in the ledger kaizen: install #54 only from GitHub URL (`pip install git+https://github.com/landtml/finlab-ml`), never the bare PyPI name.

**Re-checks:** #33 ArturSepp/VanillaOptionPricers pushed today; v2.2.1 tag, PyPI 2.2.1 live (matches pinned adoption), no drift. #22 purged-cross-validation PyPI 0.1.11 = pinned, no drift. #54 landtml/finlab-ml unchanged. #87 conformalForecast live on CRAN. License blocks #1/#5 unchanged. **Infra note:** GitHub search API returned proxy-level connection-empty twice → classified transient-exhausted per the 2026-10-10 rule; direct `/repos/` endpoints stayed healthy; new-repo discovery leg limited to arXiv + re-checks; search leg retries tomorrow.

## 5. Weather/War/Logistics Futures Event desk

**Dominant catalyst — Strait of Hormuz escalation (FACT, multi-source press Oct 16–19):** IRGC-linked attacks on commercial shipping continue — a Singapore-flagged container ship sunk by an Iranian projectile (10/16); three tankers damaged (10/19); Iran responding to the US port blockade; a missile aimed at Yanbu, Saudi Arabia's main Red Sea export port; Hormuz flows ~a third below normal (~8.5 Mb/d vs 20+ Mb/d baseline, Kpler via press — single-source, INFERENCE-adjacent). IEA released 20M+ barrels of emergency diesel; press-cited Kpler estimate says it covers <4 days of the shortfall and barely moved crude.

- **Monday counter-move (FACT):** Trump waived certain Russian energy sanctions/tariffs (60-day review conditional) → WTI −2.9% to $98.49, Brent −1.3–1.8% to ~$108.4, after Friday's $110 touch (invezz; equentis). Selloff is on waiver-hope, not flow normalization (INFERENCE).
- **INFERENCE (curve):** market pricing a multi-week, not days, disruption; ~$10 WTI–Brent spread = tight *seaborne* barrel vs relatively looser US domestic supply; spot above EIA's $105 Q4-average forecast = front-loaded tightness. Would change: ceasefire/deal restoring flows or contradicting Kpler data. **Full curve shape UNVERIFIED** (stooq timed out; Yahoo single-month futures tickers not resolving) — reads rest on front-month + spot-vs-STEO-average only.
- **Gold (FACT):** GC=F $4,158, spot $4,165–4,182 Fri–Mon, Dec ~$4,196 (invezz). Two-headed bid: Hormuz safe-haven + 10Y falling ~13bp to 5.06% on AI-funding credit stress (capitalstreetfx). January-2026 record-high figure conflicts across sources ($5,318 vs $5,602) — reported as range only.
- **Nat gas (FACT):** NG=F $3.04, −2.6% — well-supplied, mild weather, 113.9 Bcf/d output; +67 Bcf storage build vs 74 expected.
- **EIA WPSR (Thu Oct 15, one day late for Columbus Day — on schedule per standing rule):** commercial crude −8.6M bbl to 415.6M vs ~−0.3M expected (Reuters poll); distillates −2.5M bbl, 12% below 5-yr avg; gasoline +3.5M; Cushing +1.9M; refinery runs 93.5%; SPR unchanged 283M. Part of the draw attributed to Hurricane Isaias shutting Gulf production/imports — transient supply shock, not demand (Mizuho via BOE Report). **CONFLICT reported, not hidden:** oilprice.com says crude 3% *above* 5-yr avg; RTT says 3% *below* — both agree on the 415.6M level; neither relative claim labeled FACT. Oct 6 STEO: Brent to average $105 Q4 (+$14 from Sept forecast) assuming 4.5 Mb/d average Middle East shut-ins. Next: WPSR Wed Oct 21, gas storage Thu Oct 22.
- **USDA (FACT, on schedule):** Oct WASDE released Oct 9 — corn yield 181.2 bpa (16.034B bu, second-largest on record), ending stocks 1.849B bu (+282M); soy 53.1 bpa / 4.56B bu / 315M stocks; wheat stocks 740M bu (+23M). Corn futures fell ~5% on the report; front-month reads (Yahoo 16:37 ET): corn $4.6675, wheat $6.56, soybeans $12.53 — soft on record/second-record supply. Next WASDE Nov 10. No shutdown framing (standing rule; a stale 2025-vintage shutdown crawl was ignored).
- **REJECTED:** capitalsnitch.com "WTI $101.91 / Brent $126.55 Oct 14" — conflicts with Yahoo, oilprice, financefeeds, BOE Report; excluded as unreliable.
- **Watchlist spillover (value-investor lens, INFERENCE):** energy + gold at these levels is an input-cost and discount-rate story — Brent $105–110 plus the diesel squeeze is an inflation tax on consumers and margin pressure on transport/logistics/chemicals; 10Y at 5.06% keeps pressure on growth multiples (QQQ/NVDA/MSFT premium pricing). China's Q3 GDP beat (+4.5% vs 4.4%, retail sales +1.1% vs 0.5–0.6% expected) is a modest demand-side offset. No buy framing — cost-of-capital watch item.

**Sources:** eia.gov-linked reporting via oilprice.com, BOE Report, TradingView/RTT; usda.gov-linked via RFD-TV, Farm Futures; financefeeds, capitalstreetfx 10/19, invezz 10/19, equentis 10/19, nextmsc; Yahoo futures pulls 16:37 ET.

## 6. Box/Parity Observer

Two items, nothing actionable for the watchlist:

1. **SPXO (A.M.-settled weekly SPX options) launch prep — T-3 weeks (FACT, status).** Cboe SPXO remains scheduled for effective trade date **Nov 9, 2026** (C1). New operational detail since the prior flags (Sep 28/29, Oct 1 packages): SR-CBOE-2026-081 (updated ~Oct 9) adds group-level trading parameters — active launch prep (INFERENCE: on-track; disconfirming delay/cancellation search found nothing — weak evidence, noted). Parity relevance: different settlement methodology (A.M. opening vs P.M. close) — box/conversion parity is exact only within one settlement style; SPXO legs cannot mix with SPX/SPXW legs in a deterministic box without a settlement-basis adjustment; matching-unit split restricts cross-symbol complex execution (FACT, parity math per derivatives_options.md). Sources: https://fxnewsgroup.com/forex-news/exchanges/cboe-options-to-roll-out-sp-500-am-settled-weekly-options/ , https://cdn.cboe.com/resources/regulation/rule_filings/approved/2026/SR-CBOE-2026-044.pdf , https://cdn.cboe.com/resources/regulation/rule_filings/approved/2026/SR-CBOE-2026-081.pdf
2. **New parity-related paper pair — WATCH.** Shin (2026), "The P behind Q: Empirical Evidence from Physical Drift in Put-Call Parity" (arXiv 2605.12250v5, recent revision) and "The Cost of a Free Lunch: Evidence from U.S. Derivatives Markets" (arXiv 2604.19604): quoted put-call residuals vs traded futures on SPX/RUT tightly compressed (no visible violation), but the OIS-discounted synthetic-forward channel leaves a systematic "carry gap" (annualized difference between option-implied and OIS discount factors) explained by funding costs, margin/capital burden, frictions, physical-measure drift. NOT an arbitrage claim — limits-to-arbitrage interpretation. Disposition WATCH: consistent with the desk's standing doctrine (deterministic parity math wins; apparent violations resolve to implementation costs). Overlap-checked against Quant Lab #110/#111 — different papers, no dedupe needed.
3. Marginal: "Option-Implied Zero-Coupon Yields" (arXiv 2512.10823) constructs implied yield curves from SPX put-call parity — WATCH, no violation claim.

**Otherwise quiet:** no new index-methodology docs affecting watchlist parity bounds (DJX P.M.-settlement change is March-2026 vintage); no dividend-forecasting changes affecting parity bounds; no published reports of capturable put-call/box violations in liquid names — consistent with standing expectation that genuine violations are rare post-cost in actively traded names. CBOE–S&P DJI license extension through 2051 (Sept 29) is licensing news, no methodology impact.

## 7. Bonds & Rates desk

**Module status: SUCCESS — REAL_FRED_RATES mode (FRED public CSV, HTTP 200), `as_of` 2026-10-19; latest observations Oct 16. All numbers below come from the module output (FACT).**

| Series | Level | Date |
|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 2026-10-16 |
| 10Y Treasury (DGS10) | **5.09%** | 2026-10-16 |
| 2Y Treasury (DGS2) | **4.74%** | 2026-10-16 |
| SOFR / EFFR / OBFR | **3.88% / 3.88% / 3.88%** | 2026-10-16 |

**Curve (FACT + INFERENCE on direction):** 2s10s = **+35bp** (5.09−4.74), shape UPWARD_SLOPING. Mild flattening: 50bp at window start (2026-08-20: 4.69−4.19) → 35bp now (~15bp over 60 days); Oct 13→16: 42bp→35bp, 10Y −12bp while 2Y −5bp. 10Y off its 5.31% local high (Oct 5) — ~22bp of relief, still firmly above 5%.

**Funding stress (FACT):** SOFR−EFFR = **0bp**; OBFR also 3.88 — secured and unsecured overnight markets aligned. **No funding stress** (INFERENCE: plumbing normal).

**Fed funds (FACT + INFERENCE):** EFFR 3.88% sits mid-range of the 3.75–4.00% target; 25bp window change consistent with the September 25bp hike taking effect Sept 17 (12–0 vote, first hike since 2023).

**Directional read for premium pricing (INFERENCE):** higher-for-longer pressure intact — 10Y above 5% keeps discount rates elevated, valuation pressure concentrates on long-duration growth names (NVDA, MSFT, AAPL, QQQ basket). A flattening-but-positive curve at elevated levels = tight policy with resilient economy — equity risk premium compression is the bigger drag on growth multiples than credit stress (would change with rapid re-steepening, e.g. 2s10s back through 60bp). Funding normal = no forced-selling/financing tail for put premium; implied vol on this desk's read is macro-driven (policy), not plumbing-driven.

**Fed news context (supplemental scan):** Next FOMC **Oct 27–28** — decision Wed Oct 28, 2:00pm ET; presser 2:30pm ET. Sept meeting minutes (released Oct 7): most participants judged another hike likely by year-end. Chair Warsh (Oct 16, IMF Bangkok) refused to signal the October decision — "not in that business anymore" — read as reducing near-term hike odds. Hot Sept CPI (core +2.6% y/y vs 2.5% est, broad-based; headline y/y UNVERIFIED — see cross-desk resolution) raises the October-hike case (Sharif/Aleman via Reuters). Reuters (Oct 19): Fed officials debating how higher borrowing costs filter through an AI-investment-driven economy (~$1T AI investment next year ≈ 3% of GDP). **INFERENCE:** Oct-28 is a volatility event for rate-sensitive premium — Warsh's silence + broad CPI acceleration = no priced-in certainty, so 0–1 week tenor around Oct 27–28 carries policy-event risk. Would change with pre-meeting speaker coalescence or soft data next week.

---

## Desk status register

| Desk | Status |
|---|---|
| 1. Earnings Event | COMPLETE |
| 2. Dividend Opportunity | COMPLETE |
| 3. Overnight Premium (IV) | COMPLETE (IV inputs file USABLE, ~23.5h old, inside 26h guard) |
| 4. Open Quant/AI Model Lab | COMPLETE (ledger rows #110, #111 appended; 111 rows, integrity verified) |
| 5. Futures Event | COMPLETE |
| 6. Box/Parity Observer | COMPLETE |
| 7. Bonds & Rates | COMPLETE (module SUCCESS) |

No desk FAILED. No desk dropped. No numbers guessed; where a single source existed it is named; conflicts are shown, not smoothed.
