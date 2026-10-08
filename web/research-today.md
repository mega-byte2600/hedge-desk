# Hedge-Desk Daily Research — Thu 2026-10-08 (PDT)

Paper-only research input. Seven desks fanned out in parallel; synthesized below
(resolved, not stapled). Every material claim carries FACT / INFERENCE /
SPECULATION / UNVERIFIED per the repo `research` profile. Hard boundaries
honored: no Risk of Ruin content, no trade authorization, no invented numbers,
nothing reproduced from licensed material.

**Standing state notes (no change):** no federal shutdown — CR passed 2026-09-01,
funding through Dec 11; BLS September jobs released normally (29K, 4.2%).
Yield convention: ^TNX = 10Y, ^FVX = 5Y (never 2Y); 13W bill = front-end anchor.
Yahoo now 401s v7/v10 JSON endpoints without crumb+cookie even with the correct
UA header — new hard requirement as of this run (earnings desk; curl -c jar
https://fc.yahoo.com → GET /v1/test/getcrumb → API calls with cookie jar +
?crumb=).

**IV-inputs freshness guard:** nightly file
`nightly/2026-10-07-iv-inputs.json` is FRESH (as_of 2026-10-07T22:32 PDT, within
18h) but its `symbols` dict is EMPTY — all six watchlist names failed last
night's ATM IV pull (degenerate quotes, bid/ask 0/0, failed closed). Per the
standing guard the Premium desk marked it EMPTY/MISSING by name and fell back:
L1 live Yahoo v7 chain pull FAILED (persistent 401 bot-gate after backoff);
L2 CBOE delayed-quotes CDN succeeded for all six (as-of 20:33 UTC). Fallback
labeled explicitly below — never presented as nightly inputs.

---

## 1. Earnings Event desk — COMPLETE

Window scanned 2026-10-08 → 2026-10-22 via Nasdaq earnings calendar API, every
weekday fetched individually, filtered for watchlist. Only one watchlist name
reports in-window.

**TSLA — Wed 2026-10-21, after-market close (AMC). FACT (Nasdaq `time-after-hours`).**
- Fiscal quarter ending Sep/2026 (Q3 FY2026); Nasdaq consensus EPS **$0.24**
  (11 estimates); last year's report 10/22/2025 ($0.37). FACT per Nasdaq.
- Options-implied expected move (Yahoo options chain, as-of market close
  2026-10-08, underlying $375.00, mids = (bid+ask)/2):
  - Oct 23, 2026 weekly (nearest expiry containing earnings): ATM $375 call mid
    $15.22 + put mid $14.55 = straddle $29.77 → **7.94%** implied move. FACT
    (computed). INFERENCE caveat: expiry covers 13 days, so the pure binary
    component is slightly smaller than 7.94%.
  - Nov 20, 2026 monthly: $42.67 straddle → 11.38% (includes ~43 days time
    value; context only, not an event read).
  - Oct 16 monthly expires BEFORE the event — carries no earnings premium. FACT.
- Historical earnings-day moves (Yahoo daily closes, AMC convention, report
  dates verified on Nasdaq): 2025-10-22 +2.28% | 2026-01-28 −3.45% |
  2026-04-22 −3.56% | 2026-07-22 −14.52%. Average absolute (last 4 quarters)
  **5.95%**; median 3.51%. FACT (computed). The 7/23/2026 −14.52% move dominates
  the average; its cause is UNVERIFIED (no release read performed).

**Nothing in window (stated explicitly):** SPY — no earnings (ETF). QQQ — no
earnings (ETF). AAPL — next report 2026-10-29 (outside window; BMO/AMC timing
UNVERIFIED). MSFT — next report 2026-11-04 (outside window; timing UNVERIFIED).
NVDA — next report 2026-11-18 (outside window; timing UNVERIFIED).

**Desk verdict:** TSLA Q3 (10/21 AMC) is the only binary event in-window.
Options price ~7.9% vs ~6.0% trailing-average / 3.5% median realized reaction —
moderately above median. What would change it: Nasdaq revising the date, another
name moving into the window, or a fresh chain pull changing the straddle.

Sources: api.nasdaq.com/api/calendar/earnings?date= (fetched ~13:30 PDT);
query2.finance.yahoo.com/v7/finance/options/TSLA (crumb auth, 20:00 UTC quote,
pulled ~13:33 PDT); Yahoo v8 daily chart TSLA 2025-10-01 → 2026-10-08
(pulled ~13:35 PDT).

---

## 2. Dividend Opportunity desk — COMPLETE

Window 2026-10-08 → 2026-11-05, daily sweep of Nasdaq dividends calendar API.
**No watchlist name has a confirmed ex-dividend date inside the 4-week window.
FACT (zero hits across all six names).**

| Symbol | Ex-div in window | Amount | Yield @ 1pm PT price | Increase / Cut / Special | Consecutive increases (per standard) |
|---|---|---|---|---|---|
| SPY | None — paid 9/18/26 ($1.889); next ~12/18 | $7.583 TTM | 0.98% (÷ $773.93) | None | N/A (ETF) |
| QQQ | None — paid 9/21/26 ($0.751); next ~12/21 | $3.091 TTM | 0.41% (÷ $747.58) | None | N/A (ETF) |
| AAPL | None declared — Nov dividend undeclared | est. $0.27/qtr ($1.08 ann.) | 0.32% (÷ $340.42) | Raised May 2026 → $0.27 | **15** (incl. May 2026 raise; initiation 2012 = yr 1) |
| MSFT | None — next ex **11/19/2026** | $0.98/qtr fwd ($3.92 ann.) | 0.70% trailing / 0.75% fwd (÷ $522.61) | **INCREASE** — Sep 15, 2026 raise $0.91 → $0.98 | **24** (standard anchor) |
| NVDA | None — paid 9/10/26 ($0.25); next ~Dec | $1.00 ann. | 0.43% (÷ $230.48) | **INCREASE** — May 2026 $0.01 → $0.25/qtr (+2,400%) | **1** (2025 had no increase → reset per standard) |
| TSLA | None — pays no dividend | $0 | 0% | None | N/A |

Evidence: AAPL Nov undeclared FACT (Zacks, crawled 2 days ago); Nov 13 payment
estimate UNVERIFIED (stockevents, third-party). AAPL declaration-with-Q4-earnings
pattern FACT (documented corporate practice); implied ex-date ~Nov 6–9 if pattern
holds INFERENCE. NVDA raise FACT (Morningstar, announced with fiscal Q1 2027;
Yahoo events confirm $0.25 paid 9/10/26). MSFT ex 11/19/2026 FACT (Nasdaq
calendar: ex 11/19, pay 12/10, rate 0.98, announced 9/15/26). AAPL 15-year count:
raises 2017–2026 verified year-by-year from Yahoo events; initiation Aug 2012 and
2013–2016 raises are documented corporate history, issuer IR cross-check blocked
by Cloudflare (caveat noted, not silently dropped).

**Covered-premium watch item (INFERENCE, not a declared date):** no ex-div lands
on Oct 16 / Oct 23 / Oct 30 / Nov 6 expirations, so no dividend-capture timing
risk in-window. Forward flag: if AAPL declares with Q4 earnings (expected late
Oct), the ex-date would likely fall within a day of the Nov 6 monthly expiry —
early-assignment trigger for deep-ITM short calls. Recheck AAPL dividend status
after AAPL earnings.

Sources: api.nasdaq.com/api/calendar/dividends?date= (daily sweep 10/08–11/06);
Yahoo v8 chart API (dividend events + prices, 20:00 UTC); zacks.com AAPL
dividend history; stockevents.app; global.morningstar.com NVDA hike piece.

---

## 3. Overnight Premium (IV) desk — COMPLETE (via labeled L2 fallback)

**Sourcing status:** nightly iv-inputs EMPTY/MISSING (fresh but empty —
labeled, not silently replaced). L1 Yahoo v7 live chain pull FAILED all six
symbols (crumb bootstrap 401 → 401 on options bootstrap, then crumb endpoint
itself 401 after 150s backoff — classified persistent bot-gate on this egress
IP, not transient). L2 **CBOE delayed-quotes public CDN succeeded for all six**:
cdn.cboe.com/api/global/delayed_quotes/options/{SYM}.json, quotes timestamped
**2026-10-08 20:33 UTC (1:33 PM PDT)**, ~33 min after session close; all ATM
pairs had real, tight bid/ask. Raw data archived under
`~/workspace/goals/hedge-desk-daily-research/hidden_files/premium-desk/`.

**IV-rank: UNVERIFIED for all six** — no IV history from free sources; never
guessed.

| Sym | Spot | 1-DTE ATM IV (Oct-09) | ~8-DTE IV (Oct-16) | 20d realized (Yahoo v8 closes) | Window-contingent? |
|---|---|---|---|---|---|
| SPY | 774.38 | 10.9% | 11.2% | 44.9% | No (max share 0.26, Sep-21 +1.5%) |
| QQQ | 748.05 | 17.7% | 17.3% | 65.9% | **YES (0.34, Sep-21 +2.7%)** |
| AAPL | 340.34 | 23.1% | 22.9% | 88.4% | **YES (0.40, Sep-29 −2.7%)** |
| MSFT | 523.41 | 27.1% | 25.2% | 89.2% | **YES (0.32, Sep-25 +3.6%)** |
| NVDA | 230.95 | 35.8% | 31.7% | 105.5% | **Borderline (0.29–0.31, Sep-14 −3.4%)** |
| TSLA | 374.88 | 35.6% | 38.9%; 15-DTE Oct-23 **49.1%** | 130.4% | No (0.29, Oct-02 +4.6%) |

Term structure: gentle upward slope into Oct-16 weeklies for all six (normal, no
inversion). **TSLA has a clear earnings hump: 38.9% (8-DTE) → 49.1% (15-DTE,
Oct-23 expiry, first to capture earnings)** — expected event premium, not
"rich." No comparable binary hump on any other name.

Parity sanity: ATM call IV ≈ put IV within ≤0.4 pts on all six → no
parity-violation signal; math and screen agree. Bid/ask tight except MSFT (~7–8%
wide: call 3.05/3.30, put 2.71/2.91) — mild liquidity note, not a flag.

**Earnings-in-window:** TSLA Q3 2026 confirmed Wed Oct 21, 2026 after market
close (Tesla IR via Morningstar press release). **Premium into this binary =
avoid** (desk playbook application — INFERENCE, not a pricing verdict). No
pronounced event hump on SPY/QQQ/AAPL/MSFT/NVDA inside the visible 15-DTE window.

**Stale-jump screen (standing rule 2026-09-28, computed live from Yahoo v8
closes since the nightly file was empty):** WINDOW-CONTINGENT — QQQ, AAPL, MSFT
(single day drives 32–40% of 20-day variance). NVDA borderline → treated as
contingent until the spike day rolls off. **No clean "IV cheap/rich" verdict may
be issued on these four.** SPY/TSLA not contingent, but trailing realized
(44.9% / 130.4%) still reflects a genuinely volatile Sep/early-Oct tape —
IV<realized here is a regime question (recent calm), not a proven mispricing.
INFERENCE; what would change it: spike days (Sep-14/21/25/29, Oct-02) rolling
off in ~1–3 weeks, mechanically deflating realized.

**Desk verdicts:**
1. **No elevated-IV (premium-rich) signal anywhere today.** Evidence: 8-DTE ATM
   IVs 11–39%, no rankable history (UNVERIFIED), no binary humps except TSLA.
2. **Premium optically cheap vs trailing realized — not actionable.** 1-DTE IVs
   11–36% vs 20d realized 45–130% is a striking gap, but the window is
   contaminated (see stale-jump screen).
3. **TSLA Oct-23 chain: avoid premium into the 10/21 AMC binary.** Thesis: the
   49.1% hump is event premium. What would change it: an earnings-date move.
4. **Pipeline degraded:** Yahoo v7 remains 401-gated after backoff. If it stays
   down, future runs should treat CBOE delayed quotes as primary and note the
   ~15-min delay explicitly. Kaizen note logged in the quant-lab ledger.

---

## 4. Open Quant/AI Model Lab — COMPLETE

**Result: 4 new candidates, all WATCH (scores 48–64), none TEST/INTEGRATE-ready.**
Nothing material missed for other desks. All four appended to
`~/workspace/hedge-desk-research/quant-lab-ledger.md` as #35–#38 in existing
format (row 34 verified intact); standard work honored — no candidate lives
only in this file.

| # | Title | Authors | Date | Venue | Score/Disp. | Reason |
|---|---|---|---|---|---|---|
| 35 | Finance-Aware Spatiotemporal Reconstruction of Incomplete IV Surfaces ("VolPaint") | Texas Tech Math/Stats + JHU Carey | 30 Sep 2026 | MDPI Risks 19(10):746 (peer-reviewed) | 59 / WATCH | SPX-surface study (OptionMetrics 2010–2025); paper's own honesty note: completions violate no-arb more often; removing violations kills most of the gain → not pricing-ready. Data proprietary, code UNVERIFIED |
| 36 | Pricing American Options under Stochastic Local Volatility & Stochastic Correlation via RBSDE | Long Teng | 1 Oct 2026 | arXiv:2610.01187 | 48 / WATCH | New this week; single author, no code → reproducibility not established. Methodological relevance only |
| 37 | holdout — backtest overfitting toolkit (PSR/DSR, PBO, purged CV) | DaniyalMlk | 22 Sep 2026, upd. 5 Oct | GitHub, MIT | 64 / WATCH | CI+tests verified in repo; each statistic validated against worked examples; PyPI release pending. Complements #22 (purgedcv), #5 (snowjug). 64 = one point under TEST band — band respected, TEST requires a sandbox run |
| 38 | implied-volatility-conditioning-lab — quote-aware IV inversion, boundary diagnostics | lcx0731 | 8 Oct 2026 | GitHub, MIT | 58 / WATCH | Synthetic quotes only ("all generating volatilities equal 25%"), "educational research software" — honest fail-closed framing. Thesis (excellent price fit can coexist with unreliable IV) aligns with the desk's stale-jump screen. Test claims UNVERIFIED; 0 stars → credibility bounded |

**Sweep coverage & explicit gaps:** arXiv q-fin, GitHub topic/created-after,
Hugging Face datasets, free-API news. Dead legs classified: Semantic Scholar
API → HTTP 429, retried 3× (8–20s backoffs), transient-exhausted (may recover
next run). Hugging Face → only crypto/spam, nothing US-equities relevant.
Dividend forecasting → no in-window results. Earnings-drift → nothing newer than
June 2026. No purged-walkforward datasets or free market-data API launches this
run. Numerical claims above are source-reported (FACT that the paper reports
them, UNVERIFIED as independent truth).

**Cross-desk note (industry news, not scored):** Cboe + Robinhood announced 30
Sep 2026 planned launch of **KPI binary contracts** (23 companies, October 2026,
SEC-regulated, zero fees through year-end, subject to regulatory approval).
Sources: marketsmedia.com, morningstar.com, prnewswire.com. Relevant to the
Futures Event desk's prediction-market/event-catalyst monitoring.

---

## 5. Weather/War/Logistics Futures Event desk — COMPLETE

All four coverage areas produced output. Government-data rule honored: no
shutdown/blackout framing; both federal releases on schedule per primary
calendar.

| # | Event | Date/time | Print vs expectation | Futures curve read |
|---|---|---|---|---|
| 1 | **EIA Weekly Petroleum Status Report** (wk ended Oct 2) | Wed Oct 7, 10:30 ET | Crude **−3.186M bbl** vs +1.7–1.9M bbl build expected (5th surprise draw); gasoline +0.382M vs −1.611M exp.; distillate −0.042M vs −1.52M exp.; Cushing +0.444M; refinery util 92.7% (+0.2pp); exports 4.77M b/d. SPR ~283.8M bbl, lowest since Oct 1982 | WTI Nov $90.79 / Dec $90.06 / Jan $89.32 → **$0.73/bbl prompt backwardation**; Brent Dec $103.46 / Jan $100.33 → **$3.13/bbl Dec–Jan backwardation**. Strong backwardation = market pricing nearby tightness despite improved Middle East flows. FACT (EIA WPSR via WSJ/oilprice.com; curve Yahoo ~1:20pm ET Oct 8). SPR level per tradingnews.com — FACT per that source, not primary-verified |
| 2 | **EIA Weekly NatGas Storage** (wk ended Oct 2) | Thu Oct 8, 10:30 ET | +85 Bcf vs 79 Bcf WSJ survey; 5-yr avg +96 → **8th consecutive below-average build**; stocks 3,500 Bcf, +68 Bcf (+1.9%) over 5-yr avg | Henry Hub Nov $3.133 / Dec $3.465 / Jan $3.883 → steep front contango into winter; Feb quote $3.498 anomalous below January → UNVERIFIED, not a strip signal. EIA end-Oct projection ~3,985 Bcf (10-yr high); 111 Bcf/wk arithmetic makes it unlikely (INFERENCE). FACT (EIA via WSJ 14:59 ET) |
| 3 | **Tropical Storm Isaias**, Gulf of Mexico | Formed Wed Oct 7; expected hurricane landfall late Fri Oct 9, Mississippi–Alabama | 8 platforms + 2 rigs evacuated; 511,619 b/d oil (25% of Gulf) and 350 MMcf/d gas shut in (BSEE via Morningstar/DJ) | WTI +2.8% → $90.79; Brent +3.3% → $103.48. INFERENCE: short-term factor — storm also kills Gulf Coast cooling/power demand and could interrupt LNG exports, offsetting shut-ins. Clean pass = support leg disappears; structural damage = extends. **Freshest marginal catalyst on crude.** FACT (NHC track, BSEE; price moves Yahoo/WSJ) |
| 4 | **USDA Oct WASDE** — ON SCHEDULE | **Fri Oct 9, 12:00 ET** (verified against usda.gov release calendar) | DTN pre-report: corn production 15,716M bu, yield 177.6 (Sep 178.5); soybeans 4,541M bu, yield 52.9 (Sep 52.8); corn ending 1,677M bu (Sep 1,567); soy 311M; wheat 722M. WSJ survey: corn yield cut 0.9 bu/ac. US harvest delayed. 2010-style October yield cut = tail risk | Dec corn $4.9975 / Mar $5.145 (+$0.1475 ~3-mo carry); Dec wheat $6.835 / Mar $6.975 (+$0.14); Nov soy $12.865 / Jan $13.03 (+$0.165) — modest contango everywhere = market pricing adequate harvest supply; Black Sea risk premium sits on top, not in carry. Corn "gave back part of Tuesday's rally" pre-report. FACT (schedule usda.gov; expectations DTN/WSJ; quotes Yahoo ~1:20pm ET) |
| 5 | **EIA STEO (Oct, monthly)** | Released this week | EIA raised Q4 Brent forecast to avg **$105/bbl (+$14)**; global inventories −1.9M b/d Q3, −0.7M b/d Q4; Middle East export shut-ins 4.8M b/d Sep | Brent ~$103 Dec ≈ in line with revised STEO path, not ahead of it. FACT (Morningstar/DJ citing EIA) |
| 6 | **Black Sea grain corridor escalation** | Oct 5–6 | Bulk carrier *Royad Mammadov* (Ukrainian corn) struck by drones Oct 5, sank in Romania's EEZ, 2 fatalities; further vessels attacked off Bulgaria Oct 6 | Matif wheat ~€247.50/t, **+4.8% w/w on war-risk repricing, not crop news**; Rabobank: Jul–Sep Black Sea wheat exports ~7Mt below normal (~50% of typical, ~4% of global trade) — "risk premium, not shortage." Premium in EU basis/insurance, not yet in CBOT wheat (flat −0.44% today). FACT (commodity-board, graincentral, agriinsite, Rabobank) |
| 7 | **Iran war / Hormuz / Red Sea** | Ongoing; US blockade enforcement codified Oct 5; Saudi coalition struck Sana'a/Saada Oct 7; MT *On Peace* attacked near Hormuz Oct 7, 12 mariners wounded | EIA: Middle East exports rose in Sept despite attacks; Pentagon deployed third carrier (WSJ, early Oct) | Crude settled lower yesterday (WTI $88.28 −1.3%, Brent $100.20 −0.4%) — market weighting supply recovery over escalation. Prompt backwardation = price of near-term cover/optionality on disruption. No Suez closure. FACT (Morningstar/DJ, wires); weighing INFERENCE |
| 8 | **Panama Canal** | Oct 4 update | Restrictions EASING: draft 49 ft (from Sep 28); daily slots rise to 33 from Oct 15; Gatun Lake ~84.7 ft, projected stable | Not a disruption — logistics friction easing. Neutral-to-positive for freight/energy shipping. FACT (vesselhunter.io, FreightWaves) |

**Desk read (INFERENCE, flagged):** the marginal-risk board for the next 48h is
(a) **Isaias landfall damage report Friday** — asymmetric crude upside only with
structural damage; (b) **Oct WASDE tomorrow 12:00 ET** — risk is a 2010-style
corn yield cut against priced-in "adequate carry" (contango everywhere in
grains); positioning light ahead of it; (c) **Black Sea vessel attacks into NATO
waters** — war-risk repricing in Matif/EU basis, not yet CBOT wheat; a ceasefire
or export agreement unwinds it quickly (Rabobank's own warning). Curve
structure agrees: **energy backwardated (near-term tightness), grains contangoed
(adequate harvest supply), natgas front-contangoed into winter with a shrinking
storage surplus**.

Nothing fresh: Suez/Rotterdam freight, strikes — no verified new strike or port
closure in the last 72h beyond the Black Sea attacks and Isaias.

Sources: Yahoo Finance futures quotes (UA header) ~1:20–1:25pm ET Oct 8; WSJ
Market Talk (EIA prints); oilprice.com; Morningstar/Dow Jones wires; DTN
pre-report survey; usda.gov/oce/commodity/wasde (schedule verified);
graincentral.com, commodity-board.com, agriinsite.com; vesselhunter.io.

---

## 6. Box/Parity Observer — COMPLETE

**Nothing material.** The last ~2 weeks produced no new index-methodology changes
affecting SPY/QQQ/AAPL/MSFT/NVDA/TSLA and no fresh published parity-violation
analysis. Closest items were outside the window or irrelevant: SEC approval of
P.M.-settled DJX options (SR-CBOE-2026-005, Apr 10, 2026 — not a watchlist
underlying); Cboe binary-index-options rule consolidation (SR-CBOE-2026-032)
and C2 obvious-error fee change (SR-C2-2026-025, Sep 9); expanded
cash-settlement eligibility for FLEX ETF options (SR-CBOE-2026-035, ~2 months
ago); S&P DJI loosening S&P/TSX Canadian inclusion criteria (Sep 13, Canada-only).
Box-spread write-ups found were stale educational pieces (Nasdaq 2010, an
academic paper from 2005). Deterministic parity state unchanged: no new
settlement-rule or index-construction change in the window that would alter
put-call or box-spread parity math for the watchlist names. FACT (negative
result from the sweep).

---

## 7. Bonds & Rates desk — COMPLETE

Module `rates_desk.rates_environment()` ran clean (exit 0, REAL_FRED_RATES mode,
schema hedge-desk-rates-desk-1.0.0, data_source fred-public-csv-http-200,
as_of 2026-10-08). **No Yahoo fallback used** — no yield-labeling risk arose.
All numbers FACT from module output; FRED daily series lag one trading day.

| Item | Value | As-of |
|---|---|---|
| Fed funds effective rate | **3.88%** | 2026-10-07 |
| Fed funds change, 60-day window | +0.25pp | vs ~2026-08-10 |
| 10Y (DGS10) | **5.28%** | 2026-10-07 |
| 2Y (DGS2) | **4.77%** | 2026-10-07 |
| 2s10s slope | **+51bp**, UPWARD_SLOPING | 2026-10-07 |
| SOFR / EFFR / OBFR | 3.88% / 3.88% / 3.88% | 2026-10-07 |
| SOFR − EFFR spread | **0.00bp** | 2026-10-07 |

**Curve read:** prior day (10/06) 2s10s = 5.27 − 4.79 = 48bp; today 5.28 − 4.77
= 51bp → steepened **+3bp day-over-day** (10Y +1bp, 2Y −2bp). Curve upward
sloping across the 60-day window (2s10s ranged ~31–51bp); early-Aug ~47bp,
late-Sept tightened to ~31bp, then re-widened. Both legs rose over the window
(2Y 4.25→4.77, 10Y 4.72→5.28). **The 2Y at 4.77% sits 89bp above the 3.88% fed
funds rate — the front end prices rate cuts ahead of the current policy level.**
Funding stress: none — SOFR − EFFR = 0bp, all three overnight benchmarks at the
policy rate. FACT (computed from module history).

**Premium-pricing implications:**
- INFERENCE: 10Y at 5.28% (vs 4.6–4.7% August range) = higher discount rates
  compressing growth multiples — classic headwind for premium-selling on
  high-multiple growth names (NVDA/TSLA/MSFT); margin of safety thinner than
  August levels.
- INFERENCE: a steepening 2s10s with rising long rates typically compresses vol
  spreads on rate-sensitive tech while widening them on value/financials. With
  the 10Y up +56bp over 60 days, selling premium into growth names means being
  paid for a duration-driven multiple-compression risk that has already been
  partially repricing.
- INFERENCE: the 2Y-above-FFR inversion (+89bp) implies the market prices easier
  policy ahead — if the cut path materializes, long rates could re-anchor lower
  (premium-selling-positive for growth) — market expectation, not a realized
  rate.
- SPECULATION: 10Y direction from here depends on fiscal/supply and growth
  prints, which the rates desk does not observe. What would change the verdict:
  a sustained 10Y back under ~5.00% restores the August backdrop; a break above
  ~5.50% shifts the edge toward shorter-duration/value underlyings.
- Paper-only; module itself returns `trade_authorized: false`.

---

## Synthesized read — 3 to 5 decision-relevant items

1. **TSLA earnings (Wed 10/21 AMC) is the only binary event on the board, and
   it's priced as one.** The Oct-23 weekly straddle implies 7.9% vs a 3.5% median
   trailing reaction (avg 6.0% skewed by one −14.5% outlier) — options moderately
   above median, with a visible IV hump (38.9% → 49.1%) on the first chain
   capturing earnings. Per the playbook, premium into that binary is an avoid,
   not an opportunity. AAPL (10/29), MSFT (11/4), NVDA (11/18) report after the
   window — no implied-move work needed this run.
2. **The IV-vs-realized screen is compromised by the tape itself: QQQ, AAPL,
   MSFT are WINDOW-CONTINGENT, NVDA borderline.** A single September day drives
   32–40% of each 20-day realized window, so the optically cheap implied vol
   (11–36% 1-DTE vs 45–130% trailing realized) is not a tradeable verdict — the
   spike days must roll off in ~1–3 weeks before any clean call exists. The
   desk issued no elevated-IV flag and no clean "cheap" verdict today.
3. **Rates are the structural headwind for growth-name premium.** 10Y at 5.28%
   (+56bp over 60 days), 2s10s at 51bp steepening, no funding stress — discount
   rates are compressing growth multiples, which thins the margin of safety on
   selling premium into NVDA/TSLA/MSFT relative to August. The 2Y sits 89bp
   above fed funds: the market prices easier policy ahead, which would reverse
   this if it materializes.
4. **Commodity catalysts stack into Friday:** EIA crude printed a 5th surprise
   draw (−3.186M bbl vs +1.7–1.9M build expected), curves backwardated (nearby
   tightness); Tropical Storm Isaias threatens Gulf infrastructure with
   expected hurricane landfall late Friday (freshest marginal catalyst on
   crude); and the Oct WASDE hits tomorrow 12:00 ET with a 2010-style corn yield
   cut as tail risk against priced-in adequate supply. Black Sea vessel attacks
   are repricing war risk in European wheat basis, not yet CBOT — watch whether
   it spreads into Chicago pricing.
5. **No dividend-capture timing risk in-window; one forward flag.** No
   confirmed ex-divs for any watchlist name through Nov 5. If AAPL declares its
   November dividend with Q4 earnings (late Oct, pattern-based INFERENCE), the
   ex-date would likely land within a day of the Nov 6 monthly expiry —
   early-assignment trigger for deep-ITM short calls. Recheck after AAPL
   earnings.

**Desks with nothing material:** Parity — no new methodology docs or
parity-violation analysis (one line, per playbook). Quant lab — 4 new WATCH
candidates (#35–38, none TEST/INTEGRATE), ledger appended; Semantic Scholar 429
transient-exhausted.

**Desk failures this run:** none that were dropped. Nightly iv-inputs were
fresh-but-empty (labeled EMPTY/MISSING); Yahoo v7 chain pull 401-gated after
backoff (labeled, classified persistent bot-gate on this egress IP); L2 CBOE
fallback succeeded. Self-recovery not exhausted — nothing to alert.

---
*Run metadata: job_id hedge-desk-daily-research, Thu 2026-10-08 13:30 PDT,
seven desks fanned out in parallel, package written by synthesizer, all desks
reporting. Evidence labels per CFA standards. Paper-only: research and input
only — no trades, no positions, no Risk of Ruin content.*
