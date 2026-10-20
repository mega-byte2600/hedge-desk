# Hedge-desk daily research package — Tue 2026-10-20

**Run:** scheduled 13:30 PT 2026-10-20 · **Mode:** research/input only, no git ops · **Profile:** research (trace claims to evidence; FACT/INFERENCE/SPECULATION/UNVERIFIED) · **Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety.

**IV-inputs freshness:** consumed `~/workspace/hedge-desk-research/nightly/2026-10-19-iv-inputs.json`, `as_of` **2026-10-19T14:01:17-07:00** (~23.5h before run start — **within the 26h guard**, labeled throughout as yesterday's post-close data). All six 10-19 `atm_iv` fields are null (failed closed: Monday 10-19 expiry contracts were dead at the post-expiry pull). Supplemented with a **live Yahoo pull** (`as_of` 2026-10-20T13:30:09-07:00, closing marks) via cookie+crumb handshake — labeled LIVE below.

---

## 1. Earnings Event desk

**In-window (through ~Nov 3):** TSLA Wed Oct 21 AMC; MSFT Wed Oct 28 AMC; AAPL Mon Nov 2 AMC. **Out of window:** NVDA Nov 18. SPY/QQQ: indices, no earnings.

| Name | Date | Timing | Implied move (live, mid-session) | Method | Hist. avg reaction-day move (n=8) |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21 | AMC (Nasdaq `time-after-hours`) | **±6.48%** | ATM 372.5 straddle, Oct-23 expiry; mids 12.78+11.45=24.23 ÷ 373.71 spot; DTE 2 | 7.77% abs avg (4 up / 4 down) |
| MSFT | Wed Oct 28 | AMC (Nasdaq `time-after-hours`) | **±5.47%** | ATM 532.5 straddle, Oct-30 expiry; mids 14.65+14.43=29.08 ÷ 531.87 spot; DTE 9 | 7.02% abs avg (3 up / 5 down) |
| AAPL | Mon Nov 2 | AMC (Nasdaq `time-after-hours`) | **±5.22%** | ATM 340 straddle, Nov-6 expiry; mids 8.98+8.75=17.73 ÷ 339.50 spot; DTE 16 | 2.46% abs avg (2 up / 6 down) |

- Dates/timing FACT from Nasdaq earnings calendar API (all 11 dates 2026-10-20→2026-11-03 queried today; no watchlist rows elsewhere). Implied quotes FACT from live Yahoo v7 chains pulled 13:35–13:40 PT Oct 20 (market open), non-degenerate. Consensus EPS (same source): TSLA $0.22, MSFT $4.71, AAPL $2.00.
- Historical series (FACT — Yahoo daily closes, reaction-day = report-day close → next trading-day close; Jul-26 print for each name re-verified today against fresh v8 closes with exact recompute match):
  - TSLA: −14.52 (Jul-26), −3.56 (Apr-26), −3.45 (Jan-26), +2.28 (Oct-25), −8.20 (Jul-25), +5.37 (Apr-25), +2.87 (Jan-25), +21.92 (Oct-24). Range −14.5% to +21.9%.
  - MSFT: +15.51 (Jul-26), −3.93 (Apr-26), −9.99 (Jan-26), −2.92 (Oct-25), +3.95 (Jul-25), +7.63 (Apr-25), −6.18 (Jan-25), −6.05 (Oct-24). Range −10.0% to +15.5%.
  - AAPL: −7.35 (Jul-26), +3.24 (Apr-26), +0.46 (Jan-26), −0.38 (Oct-25), −2.50 (Jul-25), −3.74 (May-25), −0.67 (Jan-25), −1.33 (Oct-24). Range −7.4% to +3.2%.
- **Desk reads:** (1) TSLA is the only watchlist binary within 48h — implied ±6.48% vs 7.77% realized avg; market prices *below* history (FACT). Direction coin-flip historically (4/4; last two prints both negative). Desk rule: premium into this binary = avoid. (2) AAPL's event premium is rich vs its own history: ±5.22% vs 2.46% avg (~2.1×; 6 of 8 down-but-small). INFERENCE: overpriced on realized history *unless* the Jul-26 −7.35% marks a genuine regime shift rather than an outlier. What would change it: tomorrow's TSLA reaction and the Nov-2 AAPL print. (3) MSFT between the two: ±5.47% vs 7.02%, modestly below history; not enough to call a mispricing.
- Off-watchlist mega-cap note (FACT, Nasdaq calendar): META Wed Oct 21 AMC, GOOGL Wed Oct 28 AMC, AMZN Thu Oct 29 AMC — same-session QQQ companions for the TSLA/MSFT events.
- **Sources:** Nasdaq earnings calendar API; Yahoo v7 options chains (query1, cookie+crumb); Yahoo v8 chart daily closes.

---

## 2. Dividend Opportunity desk

| Name | In-window ex-date (through ~Nov 17)? | Detail |
|---|---|---|
| AAPL | None declared | Expected ~Mon Nov 9, $0.27 — **UNVERIFIED** (not yet declared; Zacks reports no future dividends declared as of 2 days ago). INFERENCE from 2025 pattern (declared Oct 30, 2025; ex Nov 10, 2025). Declaration typically arrives with the FQ4 earnings call. |
| MSFT | **Just outside window** — Thu Nov 19 | $0.98 quarterly, first payment of the **Sep 15, 2026 raise**, payable Dec 10. FACT (Nasdaq calendar API + PRNewswire issuer release). Consecutive-increase count **24** per the desk standard (`dividend-count-standard.md`), incl. the Sep 2026 raise — no drift. |
| NVDA | None | Current quarterly $0.25; next ex-date early Dec (~Dec 3) — exact date UNVERIFIED. FACT (Yahoo chart events). |
| SPY | None | Next ex-date ~Dec 18 (pattern). |
| QQQ | None | Next ex-date ~Dec 21 (pattern). |
| TSLA | N/A | Pays no dividend. |

- **Increases/cuts/specials in window:** none announced. MSFT's raise was Sep 15 (outside window, previously reported). No cuts or specials on watchlist in the last week.
- **Coverage note:** Nasdaq dividends calendar API returned near-empty calendars this run (transient/unreliable) — desk fell back to web verification with issuer releases; labeled accordingly.
- **Sources:** Nasdaq dividends calendar API (partial), Yahoo v8 chart events=divs, PRNewswire issuer release, Zacks dividend pages.

---

## 3. Overnight Premium (IV) desk

**Data vintages:** (a) yesterday's IV-inputs file (as_of 2026-10-19T14:01:17-07:00, within 26h guard — realized-20d + stale-jump fields consumed, labeled yesterday's post-close; all six `atm_iv` null); (b) **LIVE** Yahoo v7 options pull as_of 2026-10-20T13:30:09-07:00 (closing marks), nearest-weekly **Oct-23 (DTE=3)** and **Oct-30 (DTE=10)** ATM IV, cookie+crumb handshake; first curl seed attempt failed (exit 52 empty reply, transient), retry succeeded; zero chain failures.

### IV snapshot — LIVE (today's closing marks)

| Symbol | Spot | Oct-23 ATM IV (DTE 3) | Oct-30 ATM IV (DTE 10) | Term shape | 3-day implied move* |
|---|---|---|---|---|---|
| SPY | 769.05 | **11.97%** | 13.34% | upward | ±1.09% |
| QQQ | 717.63 | **21.16%** | 22.86% | upward | ±1.92% |
| AAPL | 339.50 | **23.39%** | 23.36% | flat | ±2.12% |
| MSFT | 531.87 | **24.27%** | **41.04%** | **earnings hump** | ±2.20% / ±6.79% (10d) |
| NVDA | 216.47 | **36.19%** | 36.17% | flat | ±3.28% |
| TSLA | 373.71 | **77.69%** | 56.54% | **inverted — earnings in front** | ±7.04% / ±9.36% (10d) |

\* Straddle ≈ IV × √(DTE/365). FACT (Yahoo v7 options, as_of above). ATM IV = mean(call, put) of Yahoo's published `impliedVolatility` at strike nearest spot, overlapping-strike set, non-degenerate quotes verified.

### IV vs 20-day realized (realized from YESTERDAY's post-close file)

| Symbol | Live front IV | 20d realized (yesterday's close) | Read |
|---|---|---|---|
| SPY | 11.97% | 9.00% (window 9/21–10/16, not contingent) | INFERENCE: sellers modestly paid (~3 pts premium); cleanest read on the board. Changes if: realized expands above ~12% over next 3 sessions. |
| QQQ | 21.16% | 15.43% | **WINDOW-CONTINGENT** (0.356) — no clean verdict. Changes if: dominant day ages out of the 20d window or realized re-accelerates. |
| AAPL | 23.39% | 16.46% | **WINDOW-CONTINGENT** (0.374) — no clean verdict. |
| MSFT | 24.27% | 22.34% | **WINDOW-CONTINGENT** (0.349) — no clean verdict on front; the 41% back-month is the earnings hump (expected, not "rich"). |
| NVDA | 36.19% | 23.68% (not contingent) | INFERENCE: front IV ~12.5 pts (≈+53%) above trailing 20d realized with **no event in the window** — sellers being well paid for near-term vol; complacency-free read. Changes if: realized-vol regime break (news) or confirmation of a genuine forward risk premium (e.g., supply-chain/AI headline risk). |
| TSLA | 77.69% | 30.01% | Earnings tomorrow inside the window — elevation is the event premium; also **WINDOW-CONTINGENT** (0.314). No clean verdict. |

Term-mismatch caveat: 3-DTE IV vs 20-day trailing realized — directional reads, not arbitrage signals.

### Earnings inside the window (binary flags)
- **TSLA — Wed 2026-10-21 after-hours** (FACT, verified live via Nasdaq earnings calendar API). Inside the Oct-23 front window. Desk rule: premium into a binary event = avoid.
- **MSFT — Wed 2026-10-28 after-hours** (FACT, same Nasdaq API). Inside the Oct-30 window only, not Oct-23. The 41.04% back-month hump is the textbook earnings term-structure signature.
- AAPL (11-02) and NVDA (11-18) outside both windows (dates carried from the 10-19 file; UNVERIFIED against a live source today).

### IV rank — **UNVERIFIED**
No free source exposes single-name IV history; no 52-week IV-rank percentile can be computed. Per fail-closed protocol it is marked, not estimated. Relative-to-trailing-realized reads above are the labeled substitute.

### Parity spot-check (deterministic math over Yahoo marks, Oct-23 chain)
- NVDA: holds (deviation 0.03 on combined spread 0.34). TSLA: holds (0.115 on 0.45). AAPL (0.275) / MSFT (0.455) within their wider spread sums.
- **SPY/QQQ: FAIL the naive check — structural, not a bad quote.** C−P deviates from S−K by a **constant parallel shift across five strikes** (SPY ~+1.07, QQQ ~+1.44–1.54) on 3–16-cent spreads. Dividends ruled out: SPY last ex-div 2026-09-18 ($1.889), QQQ 2026-09-21 ($0.751) — next quarterly ex-divs ~December, nothing inside DTE=3 (FACT, Yahoo v8 chart events=divs). Signature: option-implied forward ~0.14% (SPY) / ~0.21% (QQQ) above spot — INFERENCE: implied borrow/carry or post-close mark convention; exact cause **UNVERIFIED**. Consequence (CFA technique — parity outranks models): the front-week SPY/QQQ **call-IV-rich appearance** (SPY call 13.65% vs put 10.29%; QQQ 23.63% vs 18.69%) is the forward showing up in the marks, not genuine upside-chase positioning — do not read event skew into it, and treat Greeks off these marks with caution.

**Desk verdicts:** (1) TSLA earnings tomorrow sit inside the Oct-23 window — front IV 77.7%, ±7% 3-day implied move, inverted term structure. Binary-event zone: avoid per desk rule. (2) MSFT's Oct-30 IV (41.0%) is an earnings hump, not richness. (3) NVDA front IV (36.2%) runs ~53% above its non-contingent 20-day realized (23.7%) with no event in the window — the cleanest seller-paid read on the board; SPY the milder version (+33%).
**Sources:** Yahoo v7 options (cookie+crumb, UA Mozilla/5.0 Mac), Yahoo v8 chart, Nasdaq earnings calendar API, 2026-10-19-iv-inputs.json (realized/stale-jump only).

---

## 4. Open Quant/AI Model Lab

Sweep: arXiv (date-filtered leg 500'd server-side again; no-filter control leg ran healthy — 40 newest items Oct 15–19 as coverage evidence; 6 abstracts read at source) + GitHub new-repo discovery (`options volatility created:>2026-10-18`, 12 repos, first try). All candidates scored with repo `assess_source`. Both promising arXiv candidates (#112, #113) have **no author code link** on their arXiv abs pages — reproducibility not established for any. Re-checks: #80 StochLOB/Penny unchanged (MIT, pushed 2026-10-06; sandbox pending next cycle); #87 conformalForecast still live on CRAN (200); #71 unchanged. Semantic Scholar leg explicitly skipped per the 10-15 kaizen (no date filter → stale papers).

| # | Candidate | Score | Disposition |
|---|---|---|---|
| 114 | **louisbelot/vol-lab** — MIT pricing library + live CBOE SPY smiles (Jaeckel IV solver, parity forwards, T-bill discounting; honest American/European caveat) | 46 | **WATCH** — premium-desk market-data pattern value; crowded lane |
| 112 | AddMart — arb-free IV surface via additive martingales | 31 | ARCHIVE (no code/data; architectural idea noted) |
| 113 | Reddit-embeddings vol diagnostics (ICAIF '26 accepted; honest negative result: WSB OOS R² 0.13 collapses under identity controls; HAR gain +1.22% MSE, zero post-2019) | 39 | ARCHIVE — but **process note adopted**: nest firm controls + day-text shuffling before any narrative-vol feature (complements #4 M2VN, #85) |
| 115 | remikwisniewski/options-lab — browser JS pricing simulator, MIT | 31 | ARCHIVE (scope mismatch: educational, not desk utility) |
| 116 | SHADE alpha-stable probabilistic forecasting | 31 | ARCHIVE (crypto/FX only, no code) |
| 117 | NoLBERT hindsight-free news topics | 28 | ARCHIVE (cross-section, no desk transfer) |
| 118 | Smerlak optimal trading filters | 25 | ARCHIVE (execution theory, no execution lane) |

**Triage exclusions (no ledger rows):** 10 NOLICENSE GitHub repos + 19 arXiv scope misses (crypto, prediction markets, execution, portfolio, LOB-level).
**Net:** no TEST/INTEGRATE movement (scorer max 46). All candidates appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#112–#118 rows + jidoka/kaizen entries) — none lives only in this file.

---

## 5. Weather/War/Logistics Futures Event desk

**The 3 that matter most:**
1. **Hormuz escalation is the live vol catalyst.** Mine strikes on Oct 19 (two supertankers afire, IRGC claims); Gulf crude flows collapsed to a ~8.5M bpd 7-day average from >20M the week before (Kpler); LNG transits through the strait largely halted (~20% of global LNG normally transits); European gas +10% over two days. Brent $110–111 (5-month high), WTI ~$100–109. Live war-risk premium, not a drill — bleeds into diesel/inflation expectations (rates-adjacent vol).
2. **Diesel, not crude, is the pressure point.** Distillates 12% below 5Y average; IEA governing board accelerated the remaining ~100M bbl of the March 400M-bbl collective release (incl. >20M bbl diesel ASAP) on Oct 15; Shell Q3 refining margin doubled to $42/bbl. Curve pricing refined-product scarcity.
3. **Grains digesting the Oct 9 WASDE shock** — corn ending stocks raised 282M bu to 1.849B; Dec corn tested multi-week lows near $4.80; dry warm harvest window this week is near-term bearish; **next WASDE Nov 10** is the next binary.

**Detail (FACT unless labeled):**
- At least two supertankers struck naval mines south of the Strait of Hormuz on **Oct 19**; JMIC threat level SEVERE; 16–18 ships struck since hostilities began. Houthis struck Saudi energy infrastructure/airports; Egypt offered Saudi Arabia security support. (oilprice.com, assafinaonline.com, i3investor)
- US retaliated with airstrikes and scrapped the waiver that had allowed Iranian crude sales; administration separately weighing easing sanctions on some "shadow fleet" tankers to free tanker capacity — analysts call impact "virtually nil" given insurance/certification constraints.
- **INFERENCE:** market pricing a sustained risk premium (ING: recovering flows "decimated" again). **SPECULATION:** SEB warns Iran likely escalates further into the **Nov 3 US midterms** — calendar risk for premium into early November.
- **EIA weekly (due Wed Oct 21, 10:30 ET; last report week ended Oct 9, released Oct 15, holiday-delayed):** commercial crude **−8.6M bbl to 415.6M bbl** (3% below 5Y avg; largest draw since February); gasoline +3.5M to 208.3M (4% below 5Y avg); distillates **−2.5M to 102.6M** (12% below 5Y avg); refinery utilization 93.5%; Cushing +1.9M bbl; production estimate −300k bpd to **13.689M bpd** (Hurricane Isaias Gulf shut-ins); net imports −596k bpd. US retail diesel eased 3rd straight week to **$6.179/gal** (week ended Oct 12), down from the $6.529 Sep-21 record peak — still extreme. Nov'26 heating oil ~$4.997/gal (+1.56% midday Oct 20), RBOB ~$3.207/gal (+0.50%); NYMEX Nov'26 gas ~$3.028/MMBtu (−0.98%). INFERENCE: the crude draw was largely supply-side (Isaias shut-ins, low imports), not demand strength — a big Wednesday draw ≠ bullish demand read. **UNVERIFIED:** precise futures-curve snapshot (backwardation depth) — no verified exchange-source curve snapshot; expiry-day WTI spike anecdotal, not a curve read.
- **Oct 9 WASDE (FACT):** corn yield 181.1–181.2 bpa (+2.7 from Sept), production **16.034B bu** (2nd-largest US), 2026/27 ending stocks **+282M to 1.849B bu**, farm price cut to $4.70; Dec corn −5% post-report. Soybeans: record yield 53.1 bpa, record production 4.562B bu, stocks 315M bu, price held $12.00. Wheat: production **1.534B bu** (smallest since 1970), exports cut 25M to 750M bu, stocks 740M bu, price cut to $6.30. **Next WASDE Nov 10.** Oct 19 Crop Progress: corn 44% harvested (8pp behind 5Y avg), soybeans ~64% (1pp behind); corn good-to-excellent 56%. Overnight Oct 20 bounce (wheat +0.88%, soybeans +0.44%, corn +0.16%) after multi-day declines. US corn export inspections 74M bu (highest in ~2 years), YTD +27% vs USDA's +12% forecast — demand bright spot. Brazil soybean planting 26% (ahead of last year's pace).
- **Metals:** gold ~$4,144/oz (−0.39% midday); per Discovery Alert gold sits ~27% below its January ~$5,608/oz high — major drawdown in a war year (contrarian datum; INFERENCE: safe-haven bid absent; do not front-run a bottom on this evidence alone). Silver $57.3; copper LME ~$14,340/t holding off the August record near $14,500; BHP Q3 copper output −19% YoY (grade, maintenance, severe weather), guidance unchanged.
- **Rates/macro link:** Fed tightened last month (first since 2023), meets next week ahead of the midterms; diesel near records and Brent ~$110 are direct inflation inputs. IEA expects global oil demand to fall 2.6M bpd this year as disruptions raise fuel prices.
- **Not covered by name:** precise futures-curve structure (no verified exchange-source snapshot); CPC/NOAA long-range weather for winter gas demand (omitted for time).
- **Sources:** oilprice.com, assafinaonline.com, i3investor/klse, edgeconsultancykw.com, political.org, sourcefirstnews.com, informistmedia.com, boereport.com, morningstar.com, global-agriculture.com, rfdtv.com, dtnpf.com, moneyweb.co.za, discoveryalert.com, tradingview/seekingalpha. Federal releases on schedule (no shutdown framing — CR 2026-09-01, signed 2026-09-02, funding through Dec 11).

---

## 6. Box/Parity Observer

**Quiet.** No parity violations found; no new published parity-violation analysis in the last ~2 weeks. One methodology event: **Cboe Global Indices methodology change for its Fixed Income ETF BuyWrite and ETF BuyWrite indices** (BXTB, BXHB, BXLB, BXVBW, BXWBW; Ref C2026090301) — option-pricing input changed from a 3:45–4:00 p.m. ET VWAP to the last traded option price across OPRA-reporting exchanges in that window, with Cboe Hanweck theoretical values as fallback. Took effect at the Oct 15, 2026 close (announced Sep 3, so the document is not new — the effective date is). INFERENCE: relevance is thin — a covered-call index-valuation change, not a parity-arb input; it shifts how buywrite premium levels are measured (last-trade vs VWAP), not how conversions/reversals are enforced. Deterministic parity still assumed binding; **UNVERIFIED** as a measured claim (no live per-leg conversion/reversal premium screen was run — the clean-parity claim rests on absence of published violation evidence, not direct measurement). Box-spread financing flow context (Cboe-reported ~$1.7B daily notional per TokenPost; implied premium ~32bp avg, recently ~69bp over SOFR) is background, not a violation signal — the SOFR-overcharge figure is secondhand via a crypto news outlet, treat with caution.
**Source:** https://cdn.cboe.com/resources/release_notes/2026/Announcement-Regarding-Effective-Date-of-Methodology-Changes-to-Select-Cboe-Fixed-Income-and-ETF-BuyWrite-Indices.pdf

---

## 7. Bonds & Rates desk

**Status: LIVE** — repo's own rates module (`rates_desk.rates_environment()`), mode `REAL_FRED_RATES`, source `fred-public-csv-http-200`. All figures below are FACT from that output, latest FRED observations **2026-10-19**.

| Item | Value |
|---|---|
| Fed funds effective rate (DFF) | **3.88%** (+25 bps over the 60-day window) |
| 2Y Treasury (DGS2) | **4.77%** |
| 10Y Treasury (DGS10) | **5.15%** |
| 2s10s spread | **38 bps**, curve shape **UPWARD_SLOPING** |
| SOFR / EFFR / OBFR | 3.87 / 3.88 / 3.88 — SOFR–EFFR ≈ −1 bp |
| Front-end anchor | module does not expose 13W; FRED EFFR (3.88%) is the clean front-end anchor here |

**Direction of change (INFERENCE from the 60-day histories in the module output):** 2s10s was 50 bps on 2026-08-21 → now 38 bps: **flattened ~12 bps in two months** — bear-flattening off rising front rates (2Y 4.24→4.77, +53 bps; 10Y 4.74→5.15, +41 bps). The 10Y traced 4.74 → 5.31 peak (Oct 5) → 5.15 now: long rates eased ~16 bps from the early-October high. SOFR 1 bp *below* EFFR: **no funding stress** (calm; widening would signal dealer-balance-sheet tightness).
**Directional read for premium pricing:** 10Y at ~5.15% keeps discount rates elevated → sustained pressure on growth multiples (NVDA, TSLA) — the same mechanical headwind capping premium-rich tech rallies all month. The flattening front-end (rising 2Y) is the more option-relevant move: higher near-term carry supports put-side premium but compresses levered carry-style premium selling. What would change the read: 2s10s breaking below ~30 bps (inversion risk → recession-odds repricing → vol bid) or a 10Y re-test of the 5.31% Oct-5 high (growth-multiple compression, call-premium erosion on duration-long names). FACT: the module output currently forces neither.
**Sources:** FRED via repo `hedge_desk.rates_desk` (DFF, DGS10, DGS2, SOFR/EFFR/OBFR daily series).

---

## Synthesis: the 5 most decision-relevant items

1. **TSLA earnings tomorrow (Wed Oct 21 AMC) is the only watchlist binary within 48h.** Front IV 77.7%, ±7% 3-day implied move vs ±6.48% straddle-derived expected move (live mid-session quote), inverted term structure (56.5% behind the event). Implied prices *below* the 8-quarter realized avg (7.77%); direction a coin flip historically (4 up / 4 down; last two both negative). Desk rule: premium either side of this binary = avoid. Watchlist-vol channel: META reports the same evening (same-session QQQ companion).
2. **NVDA is the cleanest seller-paid premium read on the board.** Front IV 36.2% vs a *non-window-contingent* 20-day realized 23.7% (~+53%) with no event inside the window — sellers being well paid for near-term vol. SPY is the milder version (+33%: 12.0% vs 9.0%). Verdict changes if realized vol breaks upward (news regime) rather than mean-reverting. Rates read leans the same way: 10Y at 5.15% keeps discount pressure on growth multiples — NVDA is the name that pressure hits hardest.
3. **AAPL's event premium is rich vs its own history.** Implied ±5.22% vs 2.46% realized avg (~2.1×; 6 of 8 prints down-but-small). INFERENCE: overpriced *unless* the Jul-26 −7.35% print marks a genuine regime shift in AAPL reactions. The Nov-2 print decides. (IV-vs-realized for AAPL is WINDOW-CONTINGENT — no clean verdict from that angle.)
4. **Hormuz escalation is the live macro-vol catalyst, with the Nov 3 midterms as calendar risk.** Mine strikes Oct 19, Gulf flows ~8.5M bpd vs >20M, LNG halted, Brent $110+, European gas +10%/2d. Diesel (12% below 5Y avg) is the tightest barrel and the direct inflation channel; EIA Wed 10:30 ET (supply-side draw expected, not demand strength — don't read a big draw as bullish demand). SEB: Iran likely escalates further into the midterms. Watchlist linkage: energy → inflation → rates into the Fed's pre-midterm meeting.
5. **Rates: bear-flattening with no funding stress.** 2s10s at 38 bps (down from 50 bps 60 days ago), 10Y 5.15% off the 5.31% Oct-5 peak, DFF 3.88%, SOFR–EFFR −1 bp (calm). Long-rate pressure on growth multiples persists; what changes it: 2s10s below ~30 bps or a 10Y re-test of 5.31%. On the rates axis, the desk's directional call has not changed since yesterday's read.

**Desks with nothing material:** Dividend (no in-window ex-dates; MSFT's $0.98 ex-div lands Nov 19, 2 days outside the window), Box/Parity (quiet; one valuation-methodology change to Cboe BuyWrite indices effective Oct 15, not parity mechanics), Quant Lab (no INTEGRATE/TEST movement; one WATCH candidate — louisbelot/vol-lab, scorer 46).

---

*Hard-boundary compliance: paper-only research; no Risk of Ruin estimated; no trade recommendations or authorizations; no licensed material reproduced; unverifiable numbers marked UNVERIFIED, never guessed. No git operations performed. IV-rank percentiles UNVERIFIED (no free IV history). AAPL/NVDA earnings dates carried from 10-19 file re-verified live for AAPL (Mon Nov 2 AMC via Nasdaq calendar 11-date sweep); NVDA Nov 18 stands from the 10-19 package (no row in this run's 11-date in-window scan). SPY/QQQ naive parity-check failure is an implied-forward/data-quality caution (cause UNVERIFIED), not an arbitrage claim.*
