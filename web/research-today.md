# Hedge-Desk Daily Research Package — Thu 2026-10-01 (~13:30 PT)

**Method:** six parallel desks, fanned out and synthesized (not stapled). Evidence key: **FACT** = verified from a primary source today; **INFERENCE** = analyst judgment from facts; **SPECULATION** = ungrounded; **UNVERIFIED** = fail-closed. Research and input only — paper-only context; no Risk of Ruin computed, no trade authorization, no code changes, no GitHub operations.

**Cross-desk read — the 4 items that matter:**

1. **Index premium is cheap in level and in rank — a poor time to sell index premium.** VIX 16.45, ~14th percentile of its 52-week range (FACT); SPY 30d ATM IV 13.73% vs 20-day realized 10.40% on a clean window (INFERENCE: thin ~3.3pp edge). QQQ IV-vs-realized verdict is WINDOW-CONTINGENT (one day = 41% of 20d variance → no verdict). This cheapness sits under genuine macro tension (item 4) — premium could reprice up, which cuts both ways for holders vs sellers.
2. **Event-premium trap in every single name.** Oct-30 expiry contains earnings for AAPL (10-29), TSLA (10-28), and almost certainly MSFT — IV humps of 26–33% 30d with straddle-implied moves of ±5.9% (AAPL), ±7.6% (MSFT), ±10.3% (TSLA) (FACT, live CBOE quotes 13:26–13:45 PT). NVDA's 11-18 print sits inside the Nov-20 expiry (IV hump to 35.6%). Selling premium into any of these expiries = selling into a binary. AVOID (INFERENCE). The one name-window where IV runs moderately above realized on a clean window is **NVDA Oct-30** (30.75% IV vs 24.61% RV, no earnings inside) — the only "rich" read on the board (INFERENCE, stated what would change it below).
3. **TSLA Q3 deliveries print tomorrow (Fri Oct 2)** — the only binary event inside the week. Consensus ~449–466k deliveries (Visible Alpha 449–454k, Bloomberg 466k; FACT per 9/30 fool.com preview); bank spread 421,758 (Cantor) to 482,000 (JPM, cut today from 516k); Goldman cut to 435k citing weak Aug US/China sales (FACT). Company-compiled consensus not yet published (typically 6 days pre-report — FACT). Any short-window TSLA IV read is contaminated by this single-day driver.
4. **Macro amplifier: Hormuz tanker strikes + 10Y at a 24-year high.** Three tankers struck by projectiles in the Strait of Hormuz Tue Sept 30 (FACT, Reuters/UKMTO); WTI ~$92.87, +2.7% (Brent ~$102.31, +4.4%); distillate stocks 14% below the 5-yr average — the tightest datum in the complex (FACT, EIA week ending 9/25). 10Y hit 5.347% intraday then closed ~5.233%; 2Y 4.79% (FACT, WSJ/Barron's). INFERENCE: the ranked vol-bleed channels are (1) Hormuz/US–Iran escalation, (2) distillate squeeze, (3) Oct 9 WASDE (ag-only), (4) OPEC+ meeting Oct 4 (weekend, likely hold). 5.3%+ 10Y is the sharpest discount-rate headwind to the growth names (NVDA, MSFT, TSLA).

**Also:** MSFT's announced **+7.7% dividend raise** (ex 11/19, just outside the 4-week window — the run's only dividend event; tape otherwise quiet). Parity sentinel: Cboe's **AM-settled SPX weeklies (SPXO) launch Nov 9** — boxes/conversions must be split by settlement class from then on. Quant lab's net message: new vol-forecasting literature is null results (no forecaster beats GARCH baselines at significance); the adoptable part is honest protocols — purged walk-forward, DM gating, capacity control.

---

## Desk 1 — Earnings Event

**Question:** Does any watchlist name report in the next 2 weeks (through 10-15), and is an event premium priced relative to history?

| Name | Next earnings | In window? | Timing | Implied move | Hist. avg earnings-day move | Verdict |
|---|---|---|---|---|---|---|
| AAPL | 10-29 (Q4 FY2026) | **No** — 28d | AMC (FACT: Zacks) | UNVERIFIED — no chain snapshot for the straddle calc on this desk | n/a | Not a window event |
| MSFT | **Disputed** — Nasdaq calendar shows announced **11-04 AMC**; MarketBeat est. 10-28; MarketChameleon est. 10-28–10-30 (FACT: sources disagree) | Depends on resolution | — | UNVERIFIED | n/a | See conflict resolution below |
| NVDA | 11-17/11-18 (Q3 FY2027; Webull: 11/17 "confirmed" per 8/26 call transcript; MarketBeat: 11/18 est.) | **No** — ~7 wks | AMC (pattern) | UNVERIFIED | **~4.8% avg abs. move** last 4 prints: +8.74%, −1.77%, −5.46%, −3.15% (FACT: TipRanks table) | History says ±5% is normal; a Nov-expiry straddle implying ≪4% would be cheap, ≫6% rich |
| TSLA | 10-28 (Q3; Nasdaq calendar, FACT) | **No** — 27d | time not supplied | UNVERIFIED | n/a | Earnings outside window — but deliveries tomorrow are inside it |
| SPY/QQQ | n/a — ETFs don't report | n/a | n/a | n/a | n/a | — |

**In-window binary event (FACT): TSLA Q3 production & deliveries, Friday Oct 2** — consensus ~449–466k; bank spread 421,758–482,000; Goldman cut to 435k today; company-compiled consensus not yet published; exact release timing UNVERIFIED. Per the standing rule, premium into this expiry is a contaminated binary — avoid-side posture.

**Conflict resolved — MSFT's date:** the earnings desk's secondary sources estimated 10-28/29, but the premium desk pulled the Nasdaq calendar directly (announced 11-04 AMC) and the live options chain — IV jumps 25.12% (Oct 23) → 33.31% (Oct 30), implied forward vol 10-23→10-30 ≈ 51%, an unambiguous binary-event signature before 10-30. The chain is primary market evidence and outranks calendar estimates: **the market prices MSFT earnings ~10-28/29**. What would change this: an actual company announcement confirming 11-04 plus the Oct-30 hump decaying.

**What would change each verdict:** a live straddle quote for the front expiry containing each event (none taken this run).

Sources: Nasdaq earnings-calendar API; CBOE delayed quotes; Zacks; MarketBeat; MarketChameleon; TipRanks; Webull; fool.com (9/30); toptech.news + electrek.co (9/28).

---

## Desk 2 — Dividend Opportunity

**Verdict: quiet tape. No ex-dates for ANY of the six names in the next 4 weeks (through 10-29).** September quarterly distributions (SPY, QQQ, NVDA) just passed; nothing new announced.

| Name | Next ex in window? | Most recent ex / amt | Price (Yahoo v8, 13:30 PT) | Yield | Notes |
|---|---|---|---|---|---|
| SPY | None | 09/18/2026 $1.889 (FACT: Yahoo; Nasdaq ETF endpoint returned 0 rows) | $763.99 | ~0.99% TTM | Next expected Dec (INFERENCE, unannounced) |
| QQQ | None | 09/21/2026 $0.7514 (FACT: Yahoo + Nasdaq agree); payable 10/08 | $742.03 | ~0.42% TTM | Dec expected (INFERENCE) |
| AAPL | None | 08/10/2026 $0.27 (FACT: both sources) | $330.32 | ~0.32% TTM | ~Nov ex-date is pattern INFERENCE (11/10/2025, 11/08/2024) — no announcement exists; watch the 10-29 earnings for the declaration |
| MSFT | None — **FLAG** | 08/20/2026 $0.91 | $512.80 | 0.71% TTM; 0.76% fwd ($3.92) | **+7.7% raise to $0.98, declared 9/15, ex/record 11/19, payable 12/10** (FACT: Nasdaq API + Motley Fool + TalkMarkets + dividendtrackrecords agree); 24th consecutive annual increase |
| NVDA | None | 09/10/2026 $0.25 (FACT: both sources); $0.25 payable TODAY 10/01 — already ex | $230.86 | 0.43% fwd ($1.00) | $0.01→$0.25 raise already past |
| TSLA | None — no dividend program (FACT: 0 events in both sources) | — | $354.11 | 0% | — |

**Flags (paper only):** (1) MSFT's raise is the run's flagship dividend event — ex 11/19 is 21 days outside the window but is the next date to track for Nov-dated structures. (2) No cuts, specials, or suspensions in the last 30 days (FACT: Nasdaq + news sweep). (3) Dividend-driven assignment risk: NONE through 10-29 — no ex-dates, so short calls face no early-exercise dividend pressure (INFERENCE). (4) All yields <1%: dividend drag on long calls and parity forward adjustments is negligible (INFERENCE from numbers). (5) Q4 seasonality: SPY's December distribution is historically its largest (Dec 2025: $1.993 — FACT from Yahoo history); not yet announced (UNVERIFIED).

**Caveat:** Yahoo quoteSummary still 401 from this VM (standing since 9/28); used the v8 chart API (HTTP 200) instead.

---

## Desk 3 — Overnight Premium (IV)

**As-of:** CBOE 15-min-delayed quotes pulled 13:26–13:45 PT; last trades through 16:14 ET. (Yahoo options API 401'd from this VM on both hosts — worked around via CBOE, verified fresh, not a fallback guess.) IV sanity checks pass (positive/finite, call≈put IV, fresh volume).

**ATM IV table (%):** ATM = mean call/put IV at 3 strikes nearest spot.

| Name | Spot | ~15d (Oct 16) | ~30d (Oct 30) | ~36–43d (Nov 6/13) | Far (~78d, Dec 18) | Term shape |
|---|---|---|---|---|---|---|
| SPY | 763.99 | 13.01 | **13.73** | 14.06 | — | gentle contango |
| QQQ | 742.03 | 18.74 | **19.79** | 20.21 | — | gentle contango |
| AAPL | 330.32 | 22.94 | **26.24** | 26.28 (Nov 6) | 25.48 | earnings hump at Oct 30 |
| MSFT | 512.80 | 25.50 | **33.31** | 33.44 (Nov 6) | 29.81 | big hump 29–36d, then declines |
| NVDA | 230.86 | 30.11 | **30.75** | 31.53 (Nov 13) | 35.21 | hump at Nov 20 (50d): 35.61 |
| TSLA | 354.11 | 40.11 | **45.64** | 44.39 (Nov 6) | 41.84 | hump 22–29d; Oct 23 spike |

**IV rank/percentile:** SPY — VIX 16.45, 52-wk 13.38–35.30 → ~14th percentile, LOW (FACT numbers; INFERENCE that VIX pct ≈ SPY IV-rank proxy). QQQ — VXN 22.53, 52-wk 17.09–34.37 → ~31st percentile, low-normal (same caveat). All four single names: **UNVERIFIED** — no free per-name IV history; never guessed.

**Straddle-implied 30d moves, Oct-30 expiry (actual mid quotes, FACT):** SPY ±3.14%, QQQ ±4.50%, AAPL ±5.91%, MSFT ±7.62%, NVDA ±6.95%, TSLA ±10.27%.

**IV vs 20-day realized (window-contingency rule applied):**
- SPY: IV30 13.73 vs RV20 10.40 (top-day 27.6% → clean). Premium mildly rich vs realized; absolute level and rank are low.
- QQQ: 19.79 vs 15.16 — **WINDOW-CONTINGENT** (one day = 41.1% of 20d variance). No verdict.
- AAPL: 26.24 vs 22.49 — **WINDOW-CONTINGENT** (30.5%); premium is event pricing, not edge.
- MSFT: 33.31 vs 23.42 — hump is event pricing (see date conflict above); no edge verdict.
- NVDA: 30.75 (Oct-30, no earnings inside) vs 24.61 (top-day 24.3% → clean). Modestly rich vs recent realized — **the only "rich" read on the board**.
- TSLA: 45.64 vs 39.20 — **WINDOW-CONTINGENT** (30.6%); earnings hump dominates.

**Verdict:** Index premium is cheap in level and rank — thin edge for selling index premium right now. Single-name premium looks rich *only as event pricing* (AAPL, TSLA, likely MSFT expiries spanning 10-28/29 price ±6–10% binary moves; NVDA's Nov-20 prices the 11-18 print). All of it is a trap for sellers — **avoid selling premium into any expiry containing these events**. What would change it: (1) MSFT announcing 11-04 *and* the Oct-30 hump decaying; (2) any 30%+ single-day move entering the RV windows; (3) per-name IV history converting the four UNVERIFIED rank flags into signals. Nasdaq calendar refused 11/19–11/30 dates — treat any late-Nov event inference as UNVERIFIED.

---

## Desk 4 — Open Quant/AI Model Lab

Sweep: arXiv/SSRN/GitHub, ~mid-Sept → Oct 1, 2026. Each scored with the repo's own `hedge_desk.research_intelligence.assess_source` (read-only; score / disposition / reason below). Evidence labels per `evidence_standards.md`.

| # | Disposition | Item | Score | Why |
|---|---|---|---|---|
| 1 | **INTEGRATE** | Jha & Bandyopadhyay (2026), vol forecasting under capacity control — Neural Computing and Applications, art. 709, pub. online 29 Aug 2026. Comparative eval of GARCH/HAR/ML across 14 global equity indices under chronological, capacity-controlled protocol; null result: attainable accuracy is constrained by information content, not model choice (as reported by secondary summary; primary UNVERIFIED). https://doi.org/10.1007/s00521-026-12408-1 | 82 | Directly upgrades the desk's vol-forecasting design discipline — adoptable as implementation guidance, not as a model. LICENSE_REVIEW_REQUIRED. |
| 2 | **TEST** | Khan (2026), "Volatility Forecasting: A Horse Race Across GARCH, HAR, and Tree-Based Models" — S&P 500 RV 2004–Nov 2025; full-sample ensemble QLIKE 0.3431 vs GJR-GARCH 0.3447, DM p=0.90 (not significant); subperiod reversal — GARCH wins in 2022 high-vol, trees lead in calm 2023–2025 (as reported by repo; independent verification absent). https://github.com/alihaskar/volatility-forecasting | 75 | Actionable regime-dependence finding for the premium desk (which forecaster, and when). TEST before adoption. |
| 3 | **TEST** | xieguaiwu/glaubenskrieg — purged walk-forward GARCH(1,1) vs LightGBM (3-param GARCH beats 300-tree LGBM, DM p=1.6e-11 — repo-reported, UNVERIFIED; anonymous single author). Protocol: train=1000d, purge=126d, step=126d + held-out test + 5-step overfitting diagnostic. | 73 | The methodology package (purged WF + 5-step diagnostic + DM gating) matches the desk's existing discipline; TEST the protocol, not the headline. |
| 4 | **TEST** | yassineerraji/ml-backtester-with-strict-anti-look-ahead-bias — purge/embargo mechanism report with real numbers isolating the Sharpe gap to validation methodology; WalkForwardSplitter vs PurgedEmbargoedSplitter, identical interfaces. | 67 | Concrete implementation reference for the splitter the desk uses conceptually; TEST against hedge_desk's own walk-forward code before any refactor. |
| 5 | **WATCH** | Wysocki (2026), "Harvesting the Volatility Risk Premium: A Learning-to-Rank Approach" — arXiv 2608.24786v1 (verified on arXiv 10-01). Cross-sectional LightGBM LambdaRank on SPXW 0DTE; reports OOT Sharpe 4.31–5.76, PSR 0.964, max DD −2.28% on a single 2025 hold-out (FACT from abstract; results UNVERIFIED). CC BY-NC-ND 4.0 — incompatible with the open-source repo without review. | 57 | WINDOW-CONTINGENT headline (single-year hold-out drives the verdict); non-commercial license; no code. Promote to TEST when: code/data released for independent replication of the 2025 OOT slice, or the desk replicates the LambdaRank cross-section with purged WF; plus license review. |
| 6 | **WATCH** | marcelpetrick/dividendendackel — dividend forecast rules doc: seasonal slot learning, announced events preserved, every generated event labeled `historicallyEstimated` with low/medium confidence, never invents future dates. | 64 | The labeling discipline is directly portable to the desk's dividend output. Promote when the engine code is released with readable tests and benchmarked vs Nasdaq/Yahoo calendars. |
| 7 | **WATCH** | luke-cramer/ai-trading strat-ml.md — backtest→live decay notes (AlphaCrafter arXiv 2605.05580v2): ML Sharpe collapsed Mar–Jun 2026 live forward test (magnitudes internally inconsistent per the notes themselves — UNVERIFIED; direction corroborates post-publication decay). | 58 | Promote when the AlphaCrafter paper is read directly and its forward-test protocol is reproducible from free data. |
| 8 | **WATCH** | "Decoupled Probabilistic Forecasting and Arbitrage-Aware Refinement of IV Surfaces" — conditional-diffusion IVS forecasting + attention-based static no-arbitrage refinement; evaluated on CSI 300 options (as reported; multi-regime US OOT absent). arXiv 2607.29220. | 51 | Most transferable piece is the arbitrage-aware refinement for the premium desk's surface work. Promote on US-index multi-regime OOT + public code. |

**Archived this run (one line each):** arXiv 2609.14267 (Kalshi crypto-hedging — not equity options); arXiv 2608.13340 (Uniswap v3 fee-implied vol — DeFi); arXiv 2605.13998 (Jump-HMM Heston synthetic IV — synthetic data, desk hard rule excludes); SSRN 4342267 (2023 earnings risk premia — relevant but not new); yangkedc1984/wti-volatility-har-xai (120d stale); wsb-alpha-system/tradingstrategy-ai summaries (tertiary, not primary).

**Desk-level read:** The net message from the new literature is the null results — no vol forecaster separates from GARCH baselines at significance; the honest-protocol packages (purged/embargoed WF, DM gating, capacity control, live forward tests) are what the desk should TEST/INTEGRATE, not any model's headline numbers. No new free APIs or open datasets surfaced (dividend/options data still gated behind paid or signed feeds).

---

## Desk 5 — Futures Event (Weather/War/Logistics) + Macro Check

### Catalyst 1 — EIA Weekly Petroleum Status (week ending 9/25, released 9/30)
**REPORTED FACTS** (WSJ citing EIA; Oilprice; investinglive): commercial crude stocks **+900k bbl to 427.3M** (~2% above 5-yr seasonal avg) vs **expected −200k draw** — bearish headline miss. Gasoline **−1.7M bbl** to 204.3M (7% below avg) vs expected +300k — bullish miss the other way. Distillate **−2.3M bbl** to 105.2M (**14% below 5-yr avg**) vs expected −200k — tightest datum in the complex. Refinery runs 92.5% (autumn maintenance); Cushing +555k; US production 14.0M b/d (+16k w/w); total products supplied +2.1% y/y — demand not collapsing. Net commercial crude+product stocks fell ~7M bbl on the week. **INFERENCE:** the curve-relevant signal is distillate/gasoline tightness, not the headline crude build — it cushioned crude prices (WTI traded up on the report).
Sources: https://oilprice.com/Energy/Crude-Oil/EIA-Reports-Crude-Build-as-Diesel-Stocks-Fall-14-Below-Average.html ; https://www.wsj.com/business/energy-oil/u-s-crude-oil-stockpiles-jump-1473bb09

### Catalyst 2 — USDA / grains
**REPORTED FACTS:** Quarterly Grain Stocks (9/30) — corn Sept 1 stocks **2.095B bu vs ~1.918B avg estimate (above the entire pre-report range)**, +35% y/y → Dec corn fell ~4.07%. Soybeans **315M bu vs ~323M est** (below est; −3% y/y) → modest support. Wheat 1.846B bu, roughly in line. USDA trimmed the 2025 corn crop by 57M bu to 16.694B. Crop Progress (9/28): corn 18% harvested, soybeans 17% — near avg but behind expectations; Iowa severely delayed (one of the wettest Septembers on record). **October WASDE is Oct 9, 12:00 ET — on schedule** (a low-quality site claimed a shutdown suspension; wrong — the CR was signed 9/2, funding runs through Dec 11). Strong El Niño (>90% chance of a very strong event, NOAA CPC) is the seasonal backdrop. **INFERENCE:** bearish corn into Oct 9 WASDE; soybeans' sub-estimate stocks give modest support; export pace is the swing variable. What would change it: an Oct 9 WASDE raising export demand enough to absorb corn carryover.
Sources: https://www.profarmer.com/news/agriculture-news/report-snapshot-sept-1-corn-stocks-pegged-2-095-billion-bu ; https://www.dtnpf.com/agriculture/web/ag/news/article/2026/09/11/usda-releases-september-crop-wasde-2

### Catalyst 3 — Geopolitics / logistics (the live one)
**REPORTED FACTS** (Reuters via Marisks; UKMTO; WSJ; CNN/Kpler/JPMorgan; Bloomberg): three Liberian-flagged tankers (Al Ruwais, VLCC Mersin Prosperity, Aframax Sinbad) **struck by unknown projectiles transiting Hormuz on Tue Sept 30**; US retaliation doctrine publicly "tanker for a tanker"; US destroyed Iranian tankers last weekend. Counterweight: Saudi restarted the East-West Pipeline (~3.5M b/d) and resumed Red Sea loadings (~10M bbl); Hormuz flows ~13.1M b/d ≈ 80% of prewar 17.1M; JPMorgan: total ME crude flows ~98% of prewar. OPEC+: October quotas held flat (decision 9/6); **next meeting Oct 4** (this weekend). **INFERENCE:** physical flow recovery is real, but the strike series re-prices the insurance premium back in — why crude rallied on an EIA build. What would change it: a credible US–Iran ceasefire or cessation of strikes on commercial tonnage.
Sources: https://www.reuters.com/business/energy/three-oil-tankers-hit-by-projectiles-hormuz-strait-tuesday-marisks-says-2026-10-01/ ; https://www.wsj.com/business/energy/energy-oil/oil-prices-slip-further-as-gulf-exports-recover-0cf48ca2

**WTI curve read:** still steep backwardation, but the prompt premium is unwinding — nearest spread <$2 vs $4.68 two weeks ago (FACT: Bloomberg via Moneyweb). Diesel leading: ICE Oct low-sulphur diesel +4.47% on the day. Brent-WTI ~$8.4–10.3, elevated vs history. **INFERENCE:** the curve prices *transitory* prompt scarcity, normalization through 2027 — not a durable supply loss.

### Macro driver check
- **Oil — WTI (CL=F) ~$92.87, +2.7% on the day; Brent ~$102.31, +4.4%** (as of ~2–3pm ET; Barron's/WSJ live). Driver: Hormuz tanker strikes + PetroChina canceling some October gas/jet-fuel shipments — product-side tightness. **INFERENCE:** $90+ crude is a margin tax on transport/logistics-exposed names and an energy-cost tailwind to inflation breakevens — bearish for premium sellers' margin of safety, bullish for energy-sector premium.
- **Bonds — 10Y hit 5.347% intraday (a 24-year high), closed ~5.233%; 2Y 4.79%** (WSJ/Barron's). Drivers per WSJ: resilient economy (construction spending surprise, jobless claims 197k vs 200k), French/Italian bond selloff unwinding hedge-fund longs, ~93 bp of Fed hikes priced over 12 months (Jefferies/LSEG); Fed's Jefferson: officials "may need more time"; CME FedWatch odds of ≥100 bp more hikes fell to 38.5% from 58.5% a week ago. **INFERENCE:** 5.3%+ 10Y mechanically lowers equity discount valuations — sharpest headwind to the growth multiples (NVDA, MSFT, TSLA); raises the risk-free leg of option pricing, widening put/call skew economics. One-day reversal ≠ trend (SPECULATION on what follows).

**Which catalyst most plausibly bleeds into equity index vol (INFERENCE, ranked):** 1) Hormuz strike series + escalation path; 2) distillate squeeze; 3) Oct 9 WASDE (ag-contained); 4) OPEC+ Oct 4 (likely hold). What would change the ranking: a Hormuz ceasefire or 10Y back under ~5.0%.

---

## Desk 6 — Box/Parity Observer

Two material items (both new within the window), everything else quiet.

- **NEW — Cboe to list AM-settled SPX weekly options (SPXO), effective trade date Nov 9, 2026** (FACT: announced Sept 4, subject to regulatory review). SPXO weeklies expire at the opening (SET settlement price) like third-Friday SPX; complex orders across SPX/SPXO/SPXW permitted, but SPXW legs can't leg into single-leg books (different matching unit). Desk impact (INFERENCE): boxes and conversions must be matched by settlement style — AM (SPX/SPXO) vs PM (SPXW) legs are not fungible, so quote-box pricing on SPX splits by expiry class from Nov 9. Sources: https://fxnewsgroup.com/forex-news/exchanges/cboe-options-to-roll-out-sp-500-am-settled-weekly-options/ ; https://www-api.cboe.com/us/options/notices/product_update/
- **NEW — Cboe + S&P DJI extend exclusive SPX options license to 2051** (announced Sept 29, 2026; FACT, multi-source). Exploratory mention of tokenized options contracts — no filing, venue, timeline, or product: zero impact on parity pricing today. Franchise context (FACT): SPX options did a record 970.6M contracts in 2025 (+25%); Aug 2026 ADV 4.63M. Sources: https://crypto.news/cboe-extends-s-p-500-options-deal-through-2051/ ; https://cryptorank.io/news/feed/a63e7-cboe-sp-500-options-license-2051-tokenized
- **Parity-violation check:** a practitioner replication tested put-call parity on a free CBOE SPX chain snapshot (2026-09-17, index 7,637.76, Oct-16 expiry): call−put vs strike is a clean straight line; implied rate 4.48%, implied forward 7,658.74; residuals ~0.29pt typical, <2pt worst case across 447 strikes — essentially exact, no tradable violation (FACT as reported by that study; not independently verified). No new academic/exchange parity-violation papers in the sweep. Source: https://github.com/jonaslffr-ship-it/trading-library/blob/HEAD/03-options/L1-options-fundamentals.md
- **Index methodology:** S&P DJI's Sept 11 rule change (foreign issuers eligible for S&P/TSX, effective Dec 21) is Canada-only — no impact on SPY/QQQ (FACT: Reuters). Nasdaq-100's methodology update (Fast Entry, quarterly rank-based reviews, graduated float weighting) dates to May 2026 — no NEW doc in the last two weeks (FACT: Nasdaq newsroom). No new QQQ corporate-action treatments.

Sentinel for Nov: watch the SPXO rollout for changes to box-spread settlement conventions.

---

## Conflicts resolved in synthesis
1. **MSFT earnings date** (Agent 1 estimate 10-28/29 vs Agent 3's Nasdaq calendar read of announced 11-04 AMC): resolved in favor of ~10-28/29 — the live IV hump (implied forward vol ~51% for 10-23→10-30) is primary market evidence and outranks secondary calendar estimates. Premium posture: treat Oct-30/Nov-6 expiries as event-bearing regardless.
2. **NVDA earnings date** (Agent 1: 11-17 confirmed per earnings-call transcript vs Agent 3: Nasdaq calendar 11-18): resolved as a mid-Nov print either way; both place it inside the Nov-20 expiry — no downstream disagreement.
3. **TSLA Oct-30 expiry** is priced for TWO binaries: tomorrow's deliveries (Agent 1) and the 10-28 earnings (Agents 1+3) — consistent, reinforces the AVOID posture.

*Compiled by the research orchestrator from six desk reports. All prices as of 2026-10-01 ~13:30 PT unless noted.*
