# Hedge-Desk Daily Research — Fri 2026-10-02 (13:30 PT run)

**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA. **Lens:** value investor — mispricings, margin of safety.
**Standing labels:** FACT / INFERENCE / SPECULATION / UNVERIFIED. Research-only: no git, no pushes, no code changes.
**Note on sources:** Yahoo Finance options/futures APIs 401/429 from this VM (standing block) — agents worked around via CBOE delayed-quotes API and press-reported levels; where a number could not be verified it is marked UNVERIFIED.

---

## 1. Earnings Event desk

No watchlist name reports earnings in the Oct 2–16 window (FACT).

| Ticker | Report date | BMO/AMC | Implied move % | Historical avg move | Source |
|---|---|---|---|---|---|
| SPY | — (ETF) | n/a | n/a | n/a | — |
| QQQ | — (ETF) | n/a | n/a | n/a | — |
| TSLA | **Oct 21, 2026 — confirmed by Tesla IR** | AMC | n/a (outside window) | UNVERIFIED | https://ir.tesla.com/press-release/tesla-third-quarter-2026-production-deliveries-and-deployments |
| MSFT | ~Oct 27–28 (est., UNCONFIRMED) | AMC (est.) | n/a (outside window) | UNVERIFIED | https://www.wallstreethorizon.com/microsoft-earnings-calendar |
| AAPL | Oct 29 (est.; one source cites Oct 28) | AMC (est.) | n/a (outside window) | UNVERIFIED | https://www.zacks.com/stock/research/AAPL/earnings-calendar?tab=dividends |
| NVDA | **Nov 17, 2026 — confirmed on 8/26 earnings call** | AMC (est.) | n/a (outside window) | UNVERIFIED | https://www.MarketBeat.com/earnings/reports/2026-8-26-nvidia-co-stock/ |

- **FACT:** Nasdaq earnings-calendar API returned zero records for watchlist names in Oct 2–16.
- **FACT:** TSLA Q3 deliveries were 486,532 vs ~461,100–461,974 consensus (a beat, per Tesla IR press release) — worth flagging ahead of Oct 21 since the deliveries beat is already in price.
- **Desk verdict:** Quiet window; the action is the Oct 21–29 cluster just beyond it (TSLA confirmed 10/21, MSFT/AAPL estimated). Premium-selling into expiries covering Oct 21–29 is premium into binary events — avoid (INFERENCE). Earnings-reading protocol on any report: guidance-vs-consensus first, then GAAP-vs-adjusted gap, cash flow, segments, balance-sheet deltas, call transcript last (CFA standard).
- **What would change it:** an unscheduled/early report date announced inside Oct 2–16, or company-confirmed IR dates shifting AAPL/MSFT into the window.

---

## 2. Dividend Opportunity desk

No watchlist name has an ex-dividend date inside the Oct 2–30 window (FACT). Clean calendar.

| Ticker | Ex-div in window? | Most recent / next dividend | Amount | Change flag |
|---|---|---|---|---|
| SPY | None | Ex-div 09/18 (passed); payable 10/30 | quarterly dist. | — |
| QQQ | None | Ex-div 09/21 (passed); payable 10/08 | $0.7514 qtr | **CUT** ~7.6% (from $0.8135; already ex, priced in) |
| AAPL | None | Ex-div 08/10 (passed) | $0.27 qtr | — |
| MSFT | None | Next ex-div **11/19** (outside window); announced 09/14, $0.98 qtr | $0.98 | Increase vs prior — UNVERIFIED (sources conflict) |
| NVDA | None | Ex-div 09/10 (passed); paid 10/01 | $0.25 qtr | — |
| TSLA | None | Pays no dividend | — | — |

- **FACT:** The three nearest ex-dates (SPY 09/18, QQQ 09/21, NVDA 09/10) all fell *before* the window; payment dates (NVDA 10/01, QQQ 10/08, SPY 10/30) carry no option early-exercise implication — ex-div is what prices into calls (INFERENCE).
- **FACT (corroborated, 2 sources):** QQQ's ~7.6% distribution cut is now ex and reflected in option pricing.
- **Desk verdict:** Nothing here changes option valuation or assignment risk. QQQ's cut is stale; MSFT's $0.98 declaration is a November-horizon item, not this window (INFERENCE).
- **What would change it:** a new special dividend, accelerated declaration, or TSLA reinstatement placing an ex-date inside Oct 2–30.
- **Source note:** Nasdaq dividends calendar API 500'd; Finnhub dividend calendar returned empty (endpoint appears unavailable on this plan — INFERENCE). Data from MarketBeat compare tables + financecharts.com, corroborated across pages crawled today.

---

## 3. Overnight Premium desk (IV)

Data as-of 13:26 PT via CBOE 15-min-delayed quotes; realized vol from Yahoo v8 daily. All IV sanity checks pass (parity-consistent call/put IVs, executable quotes, no stale-quote flags) (FACT).

**ATM IV % (mean call/put IV, strikes nearest spot) and term shape:**

| Ticker | Spot | ~14d (10-16) | ~28d (10-30) | ~49d (11-20) | Term shape | IV rank | Earnings in expiry |
|---|---|---|---|---|---|---|---|
| SPY | 770.01 (+0.79%) | 11 | 13 | 14 | gentle contango | UNVERIFIED | None |
| QQQ | 749.79 (+1.05%) | 17 | 19 | 20 | gentle contango | UNVERIFIED | None |
| AAPL | 333.42 (+0.94%) | 21 | **25** | 25 | hump at Oct 30 | UNVERIFIED | YES — ~10-29 (in Oct-30 expiry) |
| MSFT | 517.40 (+0.90%) | 23 | **32** | 31→29 | big hump, decays post-event | UNVERIFIED | YES — ~10-28/29 (in Oct-30 expiry) |
| NVDA | 233.93 (+1.33%) | 28 | 29 | **34** | hump at Nov 20 | UNVERIFIED | YES — ~11-18/19 (in Nov-20 expiry) |
| TSLA | 370.36 (+4.58%) | 37 | 43 | 41 | spike at Oct 23 | UNVERIFIED | YES — ~10-21/22 (in Oct-23 expiry) |

**Implied earnings moves from term humps (arithmetic FACT, event attribution INFERENCE):** AAPL ~4.5%, MSFT ~6.7%, TSLA ~8.0%, NVDA ~7.2%.

**IV vs 20-day realized:** SPY RV 10.07% vs IV30 12.45 (+2.4 pts, max-day share 29.4% — *just under* the 30% window-contingency line); QQQ 15.00 vs 18.67 (+3.7, **WINDOW-CONTINGENT** — 9/21 +2.74% = 41.9% of variance); AAPL 22.50 vs 25.40 (+2.9, **WINDOW-CONTINGENT** — 9/10 = 30.5%); MSFT 21.71 vs 32.03 (gap is event pricing, **WINDOW-CONTINGENT** — 9/25 = 34.6%); NVDA 24.25 vs 28.85 (+4.6, not contingent); TSLA 38.03 vs 43.01 (+5.0, **WINDOW-CONTINGENT** — 9/4 = 32.5%).

- **FACT:** TSLA spot +4.58% today with IV roughly flat day-over-day — vol didn't chase the rally.
- **Desk verdict:** IV exceeds realized on all six, but four names' gaps are binary-event pricing (humps land exactly on the earnings windows) — not clean mispricings (INFERENCE). The only un-conflicted premium is SPY/QQQ: SPY 30-day IV 12.45% vs RV 10.07% is a modest +2.4 pt margin cushion for premium sellers (INFERENCE), nearly clean of single-day contamination. Premium into any of the four earnings windows = avoid per the binary-event rule (INFERENCE). IV rank UNVERIFIED for all — 52-week IV history unavailable from free sources, so nothing is labeled "cheap" or "rich."
- **What would change it:** realized vol overtaking IV (regime break); real IV-rank history becoming available; an earnings-date shift collapsing a hump; SPY's 9/21 day rolling out of the 20-day window.

---

## 4. Open Quant/AI Model Lab

Scorer: repo's own `hedge_desk.research_intelligence.assess_source` (100-pt; ≥80 INTEGRATE / ≥65 TEST / ≥45 WATCH / else ARCHIVE). Deduplicated vs the 9/25 deep sweep. Coverage: arXiv q-fin (mid-Sep onward), SSRN, GitHub, Kaggle.

| # | Candidate | Score | Disposition | One-line reason |
|---|---|---|---|---|
| 1 | purgedcv (eslazarev) — sklearn-native purged CV, 354 tests, pyOpenSci presubmission | 80 | **INTEGRATE** | First test-pinned, maintained purged walk-forward implementation found; replaces ad-hoc desk code (gated: LICENSE must confirm MIT) |
| 5 | Hindsight (zwc-11) — leakage-audited point-in-time backtest harness | 55 | WATCH | Methodology patterns (leakage tripwires, run manifests) transferable; crypto domain blocks direct adoption |
| 2 | "The Year-End Toll" (arXiv 2609.20224) — 2–3 bp Dec-31 funding-basis wedge in SPX/RUT option-implied rates | 51 | WATCH | Direct caution for the Box/Parity desk's rate-extraction method; no code/data |
| 6 | 0DTE research platform (m-man2591) — yfinance ingestion, bid-ask engine, purged K-fold, GEX | 46 | WATCH | Pattern library only; single-author, no test evidence seen; synthetic chains never touch our real data |
| 3 | Asymptotically-informed NNs for BS IV (arXiv 2609.05491) | 45 | WATCH | Potential faster IV solver; no code — fail closed |
| 4 | Fast IV expansions (Hekimoglu & Gokgoz, arXiv 2606.10245) | 45 | WATCH | Claims 1.73–1.78× throughput, O(1e-14); code link unverified |
| 7 | Fukasawa IV asymptotics (arXiv 2609.13961) | 44 | ARCHIVE | Theory only, no implementation path |
| 8 | Latent no-arb IVS geometry (arXiv 2609.00332) | 42 | ARCHIVE | No code; extends an already-WATCHed cluster |
| 9 | alt-data vol literature notes (aroesler1) | 40 | ARCHIVE | Curated notes, no primary research to adopt |
| 10 | Prediction-markets-as-options (arXiv 2609.14267) | 25 | ARCHIVE | Crypto-only, wrong domain |

- **Gaps:** No new free API endpoints surfaced; the 9/25 HF Data Library INTEGRATE candidate remains the active data-source candidate. Two independent groups claiming Householder-seeded near-machine-precision IV inversion (items 3, 4) — the technique is converging; verify one code release and the desk likely gets a free solver upgrade (INFERENCE).
- **Headline:** one new INTEGRATE (purgedcv, license-gated), five WATCHes, four ARCHIVEs.

---

## 5. Futures Event desk (weather/war/logistics, last ~72h)

**Catalysts (FACT, dated):**
1. **G-7 emergency fuel release plan (Oct 2):** 100M bbl crude + fuels from stocks within 4 months, frontloaded diesel release in first 20 days (Macron statement); EU separately weighing 50M bbl diesel (~17% of EU emergency diesel stocks) after Trump threatened a diesel export ban. Sources: WSJ, OilPrice.com.
2. **U.S./Iran escalation (this week):** Pentagon sending third carrier strike group + ~9–10K troops to the Middle East by end-Nov; UKMTO tanker attacks reported "in recent weeks." Counter-note (Kpler): ex-Iran Gulf exports 16.5M b/d in Sept — back to prewar average, ~40% now bypassing Hormuz (vs 17% pre-war). Source: Morningstar/Dow Jones.
3. **China reinstated refined-product export ban for October** (Reuters, Oct 1); diesel stocks ~20M bbl below pre-war levels — Asian crack rally.
4. **EIA weekly petroleum (rel. Sept 30, week ended Sept 25):** crude +0.922M bbl to 427.3M (vs expected 0.264M draw); Cushing +0.553M to 24.3M. Gasoline −1.7M to 204.4M, distillates −2.3M to 105.2M — both well below 5-yr seasonal averages (distillates ~14% below). Refinery utilization 92.5%.
5. **EIA natural gas storage (rel. Oct 1):** +64 Bcf to 3.415 Tcf — in line with consensus, below the 80-Bcf 5-yr avg build; ~4% below year-ago, ~2% above 5-yr avg. Henry Hub prompt ~$2.90–3.01; record Sept Lower-48 production 113.3 Bcf/d.
6. **USDA Grain Stocks + Small Grains (rel. Sept 30):** corn Sept 1 stocks 2.095B bu (+35% y/y, above all expectations — bearish); soybeans 315M bu (−3% y/y); wheat 1.846B bu (−14% y/y). Immaterial to the watchlist (no ag names).
7. **OPEC+ meets Sunday Oct 4:** expected to hold November targets steady; core producers ~5M b/d below pre-war output.
8. **Fed repriced dovish:** October hike probability cut to ~21% from ~70% after soft prints.

**Curve read (INFERENCE):** WTI Nov-26 $90 → Dec-26 $88.13 → Jan-27 $86.52 — **backwardated** (reported, not quote-tape: Yahoo futures blocked from this VM). Physical vs paper divergence: Dated Brent (physical) >$120 while ICE Brent sits ~$101 — the physical market is pricing a genuine squeeze the paper market isn't; this is the sharpest margin-risk signal in the complex this week (INFERENCE). G-7 release news is masking underlying diesel tightness (distillates 14% below avg + China export ban) that can re-widen cracks fast (INFERENCE). U.S. gas is insulated — no margin-pressure signal for the watchlist (INFERENCE).

**Desk verdict:** Oil ~$90 WTI / ~$101 Brent with a war-driven physical premium keeps energy-cost pressure moderate-to-elevated — a mild headwind for watchlist margins, well below levels that threaten the margin-of-safety on AAPL/MSFT (INFERENCE). TSLA is the most two-sided: high oil supports the EV thesis, freight/logistics tightness squeezes its cost side; net direction UNVERIFIED. Corn's bearish print is immaterial to the watchlist.

**What would change it:** (1) Hormuz closure or U.S. strike on Iran pushing front-month above ~$110 → material margin risk; (2) OPEC+ raising November targets Sunday → relieves the physical premium; (3) the G-7 diesel release failing to reach the market within 20 days → re-tightened cracks; (4) colder-than-normal November in the Oct 6 EIA STEO → winter demand lift.

---

## 6. Box/Parity Observer

Nothing material. No new CBOE index-methodology documents (only existing VIX1D / SPX target-term governance PDFs, no updates); no fresh published parity-violation studies (only old academic papers). **FACT:** the Oct 1 Summa Money options brief computes put-call-parity-implied VIX-futures forwards (Oct 17.89 / Nov 18.49) within 0.16 of quoted feeds — parity is holding, no violation flagged.

**Parity note for the lab:** the Quant Lab's WATCH item #2 ("Year-End Toll," 2–3 bp Dec-31 wedge in option-implied rates) is the one live caution for rate extraction via put-call parity — logged there, not a violation.

---

## 7. Macro driver check (oil + bonds)

| Indicator | Level | Move | Source |
|---|---|---|---|
| WTI front-month | ~$89.50–92.02 intraday Fri (tick-timing variance) | −2% to −4% Fri; ~−3% on week | Economies.com, Convextrade, Investopedia 5 Things (Oct 2) |
| 10Y yield (^TNX) | ~5.18–5.26% Fri | Off Thursday's 24-year high (~5.34–5.35%); −~6bp Fri | IndexBox, Morningstar/DJ |
| 2Y yield (^FVX) | ~4.73–4.80% Fri | −~6bp Fri | IndexBox, Reuters |

- **FACT (drivers):** Oil's drop followed EU discussion of a French proposal to release 50M bbl diesel + 50M bbl crude from IEA members, on top of recovering Middle East flows; partly offset by a third U.S. carrier to the Gulf and China's refined-export ban. The yield retreat followed a soft September jobs report (29K nonfarm vs ~84–90K expected; unemployment 4.1%→4.2%), which removed October Fed-hike pricing (now ~84% no-change); Fed policy rate 3.75–4% after the Sept 16 hike.
- **Macro verdict:** The oil pullback modestly eases energy-cost pressure on watchlist margins and inflation prints, but $90+ WTI / $100+ Brent remain well above long-run averages — the drag is smaller, not gone (INFERENCE). Long yields at 24-year highs keep discount-rate pressure on equity valuations — a headwind for high-multiple watchlist names (AAPL, MSFT, NVDA) (INFERENCE) — and mechanically richen call premium via cost-of-carry, which benefits premium sellers (FACT on the rate→premium direction via the Black-Scholes carry term).
- **What would change it:** Iran/Hormuz escalation restoring the oil premium (WTI back above ~$95–100); a hawkish Fed surprise re-accelerating long yields; or executed reserve releases + a confirmed Fed pause normalizing both drivers.

---

## Synthesis — the 4 decision-relevant items

1. **Binary-event premium dominates the watchlist's front end.** AAPL, MSFT, TSLA, and NVDA term structures hump exactly over their earnings dates (implied moves: AAPL ~4.5%, MSFT ~6.7%, TSLA ~8.0%, NVDA ~7.2%); those gaps are event pricing, not mispricings. Premium into any of the four = avoid. The only un-conflicted premium is SPY/QQQ (SPY IV30 12.45% vs 20d RV 10.07%, nearly window-clean) — a modest margin-of-safety cushion for premium sellers. (INFERENCE)
2. **Energy is a mild-but-persistent margin headwind with a diesel tail.** WTI's ~3% pullback on G-7 release news is overshadowed by the physical squeeze (Dated Brent >$120 vs ICE ~$101) and distillate stocks 14% below seasonal average + China's export ban. OPEC+ Sunday and the 20-day release timeline are the two near-term swing factors. (FACT + INFERENCE)
3. **Rates at 24-year highs are the valuation headwind.** 10Y ~5.2% after the soft jobs report killed October hike odds; discount-rate pressure persists on high-multiple names even as the pause repricing is mildly supportive. Call premium mechanically richer via carry — favors the premium-selling side of the ledger. (FACT + INFERENCE)
4. **One new implementable research candidate; quiet calendars otherwise.** purgedcv (sklearn-native, test-pinned purged walk-forward CV, score 80 → INTEGRATE, license confirmation pending) is the first such open implementation found — closes the methodology gap the 9/25 sweep flagged. Earnings and dividend calendars are clean in-window; QQQ's ~7.6% distribution cut is already ex and priced. (FACT + INFERENCE)

**Cross-desk consistency check:** Earnings desk confirms the four earnings dates (TSLA 10/21 confirmed; MSFT/AAPL estimated; NVDA 11/17) that the Premium desk's term-structure humps are pricing — the two desks agree on where the binary premium sits. Futures and Macro desks agree on the oil read (Futures: physical squeeze; Macro: $90+ drag smaller but not gone). Quant Lab's Year-End Toll WATCH is filed as a parity-desk caution, not a violation — consistent with Parity's "nothing material."

*No new contradictions to resolve. No Risk of Ruin generated; no trade authorizations proposed; no licensed material reproduced.*
