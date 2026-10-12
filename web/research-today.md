# Hedge-desk daily research — 2026-10-12

**Run:** Monday 2026-10-12, 13:30 PDT (coordinator). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** 7 parallel desks, synthesized — contradictions resolved, top items kept. Standing rules: Yahoo Finance first (UA header `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`), Nasdaq second; ^TNX = 10Y, ^FVX = 5Y (never 2Y), 13W bill = front-end anchor; no shutdown framing (CR passed 2026-09-01, funding through Dec 11). Technique: CFA skill; every material claim tagged FACT/INFERENCE/SPECULATION/UNVERIFIED.

---

## 1. Earnings Event desk

**One in-window event (Oct 12–26).**

| Symbol | Quarter | Date | Timing | Options-implied expected move | Historical avg earnings move |
|---|---|---|---|---|---|
| **TSLA** | Q3 2026 | **Wed 2026-10-21** | **After close** (webcast 5:30 PM ET) | **±3.97%** | −4.81% signed avg / **5.95% avg-absolute, last 4** |
| MSFT | FQ1 2027 | Wed 2026-10-28 | After close | n/a (outside window) | — |
| AAPL | FQ4 2026 | Mon 2026-11-02 | After close | n/a (outside window) | — |
| NVDA | FQ3 2027 | Wed 2026-11-18 | Not supplied (Nasdaq) | n/a (outside window) | — |

- **Date FACT:** Nasdaq earnings calendar API (all in-window trading days queried 2026-10-12 ~13:35 PDT) + Tesla IR Oct 2 company announcement (after-close results Oct 21, webcast 5:30 PM ET). TSLA market cap shown $1.51T.
- **Implied move FACT:** Yahoo options chain (crumb-authenticated, UA header), TSLA Oct-23-2026 expiry (first expiry after the event) — ATM 377.5 straddle mid 15.00 on underlying 378.03 (chain timestamp 2026-10-12 20:00 UTC = 13:00 PDT): call bid/ask 7.80/8.05 (IV 34.9%), put 7.00/7.15 (IV 33.2%). 15.00 / 378.03 = **3.97%**. Tight call/put IV spread — no visible skew blowout (INFERENCE: market pricing symmetric risk around the print, not downside hedging).
- **Historical FACT (Yahoo daily bars):** last four TSLA earnings sessions: +2.28% (2025-10-22), −3.45% (2026-01-28), −3.56% (2026-04-22), **−14.52% (2026-07-22)**. Signed avg −4.81%; ex-outlier signed avg −1.58%; avg-absolute 5.95%. (INFERENCE caveat: AMC timing for the four past quarters is inferred from TSLA's consistent AMC practice, not confirmed from IR per quarter.)
- **Context (statement_analysis reading order — guide > print):** FACT — Q3 deliveries 486,532 reported Oct 2 (stock +4.7% at $370.59; ~5.3% beat vs 461,974 consensus); Street EPS $0.23 expected, down ~38% y/y from $0.37; Tesla missed consensus in each of the last four quarters; trailing P/E ~354, forward ~197. INFERENCE: July's −14.5% drop followed a prior record delivery quarter — the print does not drive the move; the Oct 21 teardown starts at automotive gross margin by segment, GAAP vs adjusted, OCF vs net income, Q4 guidance.
- **Verdict:** market-implied ±3.97% vs 5.95% historical average-absolute — options pricing *below* historical realization on a binary event with a −14.5% July tail. Premium into this event = avoid (premium-desk rule). What would change it: an announced time change (verify ir.tesla.com), material straddle repricing into the event, or AMC-timing verification for the four historical quarters.
- Sources: Nasdaq earnings calendar API `https://api.nasdaq.com/api/calendar/earnings?date=`; https://www.barchart.com/story/news/5381644/earnings-preview-what-to-expect-from-tesla-s-report; https://jorgai.com/blog/tesla-q3-2026-deliveries-earnings-october-21; Yahoo Finance options chain + v8 chart.

## 2. Dividend Opportunity desk

**One material item: AAPL's November dividend lands at the end of the window.**

| Symbol | Next ex-div | Amount | Declared? | Increase / cut / special | In window? |
|---|---|---|---|---|---|
| AAPL | **~Nov 6 or Nov 9 (expected, not yet declared)** | **$0.27 expected** | No — expected ~Nov 2 with earnings | None expected (raised May 2026: $0.26→$0.27) | **YES — likely** |
| MSFT | Nov 19, 2026 | $0.98 | Yes (declared Sep 15, 2026; payable Dec 10) | **INCREASE — 24th consecutive year** (per count standard; Sep 2026 raise $0.91→$0.98) | No |
| NVDA | ~Dec 3–4 (pattern) | $0.25 expected | No | None | No |
| SPY | ~Dec 18 (cadence) | varies | No | None | No |
| QQQ | ~Dec 18 (cadence) | varies | No | None | No |
| TSLA | None — pays no dividend | — | — | None | — |

- **AAPL timing — INFERENCE.** FACTs: FYQ4 2026 earnings set for Mon Nov 2, 2026 (MacRumors Oct 6 citing Apple's IR page — secondary source; Apple IR page not independently opened this run). November-dividend pattern (Nasdaq data): declared 10/30/2025 → ex 11/10/2025 ($0.26); declared 10/31/2024 → ex 11/08/2024 ($0.25). $0.27 expectation is INFERENCE from the May 2026 raise ($0.26→$0.27, verified in Nasdaq dividend history) and AAPL's once-a-year May cadence. **Value-lens note:** the expected ex-date sits right after the Nov 2 earnings release — a dividend-capture position would cross a binary earnings event, so this is not a clean standalone catalyst. What would change it: the actual declaration (~Nov 2).
- **MSFT $0.98 raise — FACT** (Nasdaq symbol-dividends API, 2026-10-12 ~13:32 PDT): ex 11/19/2026, cash $0.98, declared 09/15/2026, record 11/19/2026, payable 12/10/2026. Consecutive-increase count **24**, per `~/workspace/hedge-desk-research/dividend-count-standard.md` (counts calendar years with an announced increase, increments on announcement date; MSFT resolved from issuer history — no drift). Just outside this run's window — flag for the next run.
- **NVDA/SPY/QQQ nothing in window — FACT** on last-paid dates (Yahoo chart `events=div`, 1y, 2026-10-12 ~13:30 PDT): NVDA last ex 09/10/2026 ($0.25); SPY last ex 09/18/2026 ($1.889); QQQ last ex 09/21/2026 ($0.751). Next ex-dates are INFERENCE from quarterly cadence (Dec for all three) — not declared. Nasdaq's ETF dividend endpoint returned 0 rows for SPY/QQQ (endpoint quirk, not evidence of absence); the Nasdaq calendar API returned degraded results (1988–2104 timeframe, near-zero rows) and is **UNVERIFIED as a forward source this run** — transient/degraded, retried with different parsing, still unusable; Yahoo/Nasdaq-symbol history substituted.
- **TSLA — FACT:** zero dividend events in the 1-year Yahoo pull; pays no dividend.
- **AAPL consecutive-increase count — UNVERIFIED this run** (streak not verified against issuer IR history; standing rule forbids copying screener counts — no count stated). No cuts or specials announced for any watchlist name.
- Sources: Yahoo chart API `https://query1.finance.yahoo.com/v8/finance/chart/<SYM>?events=div&range=1y&interval=1d`; Nasdaq `https://api.nasdaq.com/api/quote/<SYM>/dividends?assetclass=stocks`; https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/; `~/workspace/hedge-desk-research/dividend-count-standard.md`.

## 3. Overnight Premium desk (IV)

**Freshness guard tripped — live fallback used and labeled.**

- **IV-inputs file: STALE.** `2026-10-11-iv-inputs.json` as_of 2026-10-11T13:54 PDT = ~23.6h old (> 18h guard). **Fallback:** live Yahoo options-chain pull (crumb-authenticated, post-close quotes as of 4:00pm ET) — labeled explicitly as fallback, never presented as file data. FACT.
- **Findings (labeled):**
  - MSFT 31D IV 31.1% and TSLA 31D 41.7% — earnings-inflated (MSFT Oct 28 / TSLA Oct 21, both confirmed) → binary-event premium, **avoid**. FACT on dates; INFERENCE on "inflated."
  - NVDA 31D 30.5% vs stale 20D realized 21.8% — looks rich, no earnings inside; **PROVISIONAL, needs tonight's pull to confirm.**
  - All other IV-vs-realized verdicts **WINDOW-CONTINGENT** (stale-jump screen: single-day variance share over the 30% threshold in the stale file).
  - IV rank **UNVERIFIED** — no free IV-history source available; never guessed.
- **What would change it:** tonight's iv-inputs pull (fresh `as_of` within 18h) — the NVDA provisional read and all WINDOW-CONTINGENT verdicts reset on fresh realized-variance data.

## 4. Open Quant/AI Model Lab

**5 new candidates scored with the repo's `research_intelligence.assess_source` (read-only import), appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` as #59–#63 (deduped against existing 58 rows — no repeats). No WATCH item moved this run (all re-checked within the two-cycle window).**

| # | Candidate | Source | Score / Disp. | Reason |
|---|---|---|---|---|
| 59 | iftekhar-mobin/**quant-market-regime-research** — purged walk-forward + embargo study, deflated Sharpe, 95% CIs, "built to return 'no'" | GitHub (created 2026-08-26), MIT (verified via API + LICENSE) | 52 / WATCH | Study-scope (FX), not a package — methodology reference for the purged-WF lane; complements #22/#54/#60 |
| 60 | vkovshov/**ml4t-diagnostic** — DSR/PBO/CPCV/RAS backtest-diagnostic package | GitHub + PyPI v0.1.8 (2026-09-24), MIT (badge + README verified) | 63 / WATCH | One point under TEST band — TEST opens only on sandbox evidence. **Caveat:** README links issue tracker at github.com/ml4t/diagnostic — org-vs-author provenance UNVERIFIED |
| 61 | khalid-naami/**earnings-intelligence-actor** — Apify actor: ATM-straddle implied move, gap-fill %, 5-day drift bias, analyst targets | GitHub (pushed 2026-10-01), Apache-2.0 (verified) | 61 / WATCH | Method transparent (implied move = (call ask+put ask)/price); serves the earnings desk's implied-move lane. **Blocked** on Apify token + pay-per-run (user/platform decision); earnings-date/quote provenance UNVERIFIED |
| 62 | Christensen/Timmermann/Veliyev — **"Warp speed price moves: Jumps after earnings announcements"** | arXiv:2601.08962v2; peer-reviewed J. Financial Econometrics (DOI verified on arXiv record) | 52 / WATCH | Tick-by-tick jump tests: earnings "almost always induce jumps"; post-announcement strategies consistent with efficient price formation after 2016 (source-reported, full paper not read). No code → reproducibility not established. Lens note: if PEAD is dead post-2016, the desk hunts the event move, not drift |
| 63 | Brogaard et al — **"Does 0DTE Options Trading Increase Volatility?"** | CFMR 2026 conference paper (abstract read only) | 36 / ARCHIVE | Below the 45 WATCH band; conference (not journal) paper; reproducibility not established. Reconciliation vs dampening literature (incl. #7) noted as context only |

- **Triage exclusions (no ledger rows):** aroyston14/time-series-momentum-trading-pipeline — NOLICENSE (all-rights-reserved; line stop); sentisenseapp/skills options-payoff-calculator — key-gated vendor API, proprietary IV models, single-vendor skill; lse-data forks — commercial vendor SDK, signup-gated; yakupmrt7 quant-research-harness — crypto scope (Deribit/Binance), zero watchlist transfer; MDPI dividend LSTM (price-direction, stale); Cheng & Cheng short-term IV asymptotics (2024 theory, marginal desk fit).
- **Labels:** FACT — license statuses, PyPI dates, #62's JFE DOI, all scores (scorer-run, not inherited). SOURCE-REPORTED — every performance claim in #59–#62 READMEs/abstracts (nothing executed this run). UNVERIFIED — #60's ml4t-org provenance, #61's earnings-date/quote provenance, #62's empirical claims (full paper unread). Band discipline held: 63 ≠ TEST.

## 5. Weather/War/Logistics Futures Event desk

**(a) USDA October WASDE — Fri Oct 9, 12:00 ET. Bearish corn surprise.**
- **Corn FACT:** yield raised 2.7 bu/acre to **181.2** (Sept 178.5; trade avg estimate 177.6 — trade expected a *cut*). Production **16,034 million bushels** (Sept 15,800; est. 15,716) — second-largest U.S. corn crop on record. Ending stocks **1,849 mb** (Sept 1,567; est. 1,677), +282 mb m/m. Farm price lowered to **$4.70** (Sept $4.80).
- **Soybeans FACT:** near-neutral, slightly bearish — yield 53.1 bu/ac (record); production 4,562 mb; ending stocks 315 mb (Sept 310; est. 311); exports raised 10 mb on Chinese buying; farm price $12.00 unchanged.
- **Wheat FACT:** carryover up despite smallest U.S. crop since 1970 — production 1.534 bb; exports cut 25 mb to 750 mb (commitments down 32% y/y); ending stocks 740 mb (Sept 717; est. 722); farm price cut to $6.30. World: EU −0.8 mmt; Russia wheat exports cut 3 mmt to 40 mmt (lowest in five years); Argentina and Canada +0.5 mmt each; global ending stocks ~276 mmt, little changed.
- **Market reaction FACT (Oct 9):** Dec corn briefly hit limit down; KC wheat −17¢ at $7.19¼; Chicago wheat −12¢; Nov soybeans +4.5¢ at $12.94 (rallied >22¢ off the morning low on Chinese demand). Next WASDE: Nov 10.
- Sources: https://www.dtnpf.com/agriculture/web/ag/news/article/2026/10/09/usda-raises-corn-yield-2-7-bpa-181-2; https://www.dtnpf.com/agriculture/web/ag/news/article/2026/10/09/october-wasdes-shocking-rise-corn; https://www.brownfieldagnews.com/news/u-s-corn-soybean-wheat-ending-stocks-all-up-on-month/; https://teucrium.substack.com/p/october-wasde-recap

**(b) EIA weekly petroleum — last report Wed Oct 7 (week ended Oct 2); next Wed Oct 14, 10:30 ET.**
- FACT: crude −3.19 mb to 424.1 mb vs Reuters poll expecting a **+1.72 mb build** (bullish headline). Cushing +0.444 mb. Gasoline **+0.38 mb** to 204.7 mb vs expected **−1.66 mb draw** (bearish). Distillates ~flat (−0.042 mb) to 105.1 mb vs expected **−2.11 mb draw** (bearish vs expectations; distillate still structurally tight). Refinery runs +223 kb/d, utilization 92.7%. U.S. crude production **record 13.979 mb/d**. Brent closed ~$101.49, WTI ~$89.57–$89.89.
- **Preview for Oct 14: no published Reuters consensus poll located as of deadline — UNVERIFIED.** Key question: whether draws persisted against record domestic production.
- Sources: https://www.reuters.com/business/energy/us-crude-stocks-distillate-inventories-fall-gasoline-inventories-rise-eia-says-2026-10-07/; https://investinglive.com/commodities/eia-weekly-us-crude-oil-inventories-3186k-vs-1722k-expected/

**(c) Geopolitical / logistics — last ~72h.**
- **Hormuz FACT:** IRGC Navy reports **three tankers struck naval mines Sat Oct 10–Mon Oct 12** while attempting unauthorized exits with AIS switched off (a 750,000-bbl cargo cited in one incident); IRGC warns vessels disabling navigation systems will be treated as hostile. UKMTO confirmed damage reports over the weekend. Kpler: flows ~13.1 mb/d late September (~80% of pre-war 17.1 mb/d); transit counts slowed this month. Iranian claims are one-sided — no independent vessel identification as of deadline. Sources: https://www.cnn.com/2026/10/11/middleeast/iran-hormuz-oil-analysis-intl?cid=external-feeds_iluminar_meta
- **Houthi/Saudi FACT:** Houthis claimed a missile strike on Riyadh's King Khalid International Airport Sat Oct 11 (13 killed, 300+ wounded) and a second strike Sunday (1 killed, ~11 injured); Dammam airport also struck. Lufthansa and Air India suspended Riyadh flights. Oct 4 Aramco/Khurais pumping-station attack briefly halted the East-West bypass pipeline; Saudi energy minister said flows restored by Oct 6 (5.8 mb/d that morning). Weekend attacks targeted aviation, not energy infrastructure. Sources: https://www.reuters.com/commentary/breakingviews/riyadh-attacks-hit-core-saudis-economic-pivot-2026-10-12/; https://www.barrons.com/livecoverage/stock-market-news-today-101226/card/oil-prices-rise-as-saudi-attacks-u-s-russia-diesel-pact-add-market-uncertainty-9iMFpm7GM0QTs5nQBafk; https://www.reuters.com/business/energy/oil-climbs-mideast-conflict-tanker-attacks-persist-2026-10-11/
- **Trump announcements (Sunday) FACT:** claimed Russia-Ukraine "energy ceasefire" (Zelenskyy pushed back, citing Russian strikes on Ukrainian energy targets hours later); Russia diesel deal — 300 kt+ immediately, another ~500 kt in November (reported tonnages conflict across outlets — treat as rough); lifted sanctions on Russian diesel. Goldman Sachs raised its Dec Brent forecast to $90 (from $85), estimating >$20/bbl geopolitical risk premium, base case no quick end to the U.S.-Iran war. Sources: https://www.wsj.com/business/energy-oil/oil-prices-fall-as-traders-weigh-russian-diesel-deal-middle-east-supply-risks-bc9fabcf; https://oilprice.com/Latest-Energy-News/World-News/Oil-Stuck-Between-Middle-East-Escalation-and-Russia-Ukraine-Energy-Truce.html
- **Oil prices FACT (Mon Oct 12):** Dec Brent settled $106.65 (+1.8%); Nov WTI $93.74 (+2.1%). Yahoo pull (v8 chart, 4:30pm ET): WTI front-month $93.21, Brent $106.07.
- **Tanker/logistics FACT:** VLCC Persian Gulf→East Asia rates at record ~$1.4M/day (Bloomberg-cited); ship-to-ship shuttle transfers around Hormuz tying up VLCCs, draining fleet availability. Container CTS Global Price Index at 117 in August (+44% y/y, +50% since Jan 2026); transpacific Asia–USWC near peak on pre-holiday volumes; Asia–Europe down 10–15% from July highs but still ~$1,000/FEU above May baselines. German port labor disputes and Rhine draft restrictions adding friction. Sources: https://www.wsj.com/logistics-report/tanker-shortage-sends-oil-shipping-rates-soaring-d526cdb7; https://www.analystmarkets.xyz/news/187466/tanker-rates-soar-to-record-as-oil-crisis-becomes-shipping-crisis/; https://cross-border-magazine.com/global-container-shipping-record-freight-prices-2026/; https://commodity-board.com/global-logistics-bottlenecks-keep-freight-costs-elevated-squeezing-agri-food-margins
- **Natural gas FACT:** Nov Nymex $3.174 (Yahoo, 4:30pm ET). EIA storage (Oct 8, week ended Oct 2): +85 bcf to 3,500 bcf vs ~79 bcf survey; 68 bcf above the 5-yr average. EIA Oct 6 outlook revised end-October forecast to 3,850 bcf (+2% above seasonal avg). Hurricane Isaias (Gulf landfall) shut in ~1.1 bcf/d (57% of Gulf output) — but Gulf offshore is only ~2% of U.S. marketed production, so the storm's bigger lever is demand/LNG interruption. Europe storage 73% full vs 88% seasonal average. Sources: https://www.wsj.com/finance/commodities-futures/u-s-natural-gas-futures-gain-ahead-of-inventory-data-9a9d067d; https://www.tradingview.com/news/barchart:60b0897eb094b:0-nat-gas-prices-erase-early-gains-on-weekly-storage-builds/

**Futures-curve observations (INFERENCE, labeled):**
- **Crude in steep backwardation — market paying for prompt barrels.** Oct 1 strip data (https://commodity-board.com/crude-oil-rally-steepens-backwardation-as-brent-wti-spread-widens): WTI Nov 2026 settled $92.87 declining to ~$51 by Dec 2035; Brent Dec 2026 $102.63 declining to low-$60s late-2030s.
- **Brent-WTI front spread widened to $12.86** (106.07 − 93.21, Yahoo, today) vs ~$10 on Oct 1. INFERENCE: the war/geopolitical premium is concentrating in seaborne Brent, not inland WTI — consistent with Hormuz/Houthi headlines pricing into barrels exposed to the shipping corridor. Backwardation + record refinery runs + wide Brent-WTI = the curve is pricing near-term physical tightness, not structural shortage (long end anchored in the $50s–$60s).
- **Grains curve shape UNVERIFIED** — Yahoo month-contract symbols returned no data this run; no curve-shape claim made. Directionally, the WASDE bearish surprise (limit-down Friday in Dec corn) puts pressure on the front; confirmation awaits a working strip source.
- **Diesel/gasoil is the bullish anchor of the complex** (commodity-board, Oct 1): distillate cracks firm into heating season; the U.S.-Russia diesel deal is a headline supply loosener but INFERENCE — a one-off sanction carve-out does not clear the structural distillate deficit (U.S. distillate still well below 5-yr average), so gasoil backwardation should persist; watch gasoil cracks as the lead indicator.

## 6. Box/Parity Observer

**NOTHING MATERIAL.** No new CBOE or SPDJI index-methodology changes and no published put-call/box parity-violation analysis surfaced in the past week. The only box-spread item is IRS Notice 2026-62 (late Sep/early Oct) targeting the tax treatment of box-spread ETFs like BOXX — a tax/regulatory matter, not a parity-arbitrage signal. Nothing actionable for parity or mispricing work on the watchlist.

## 7. Bonds & Rates desk

**Source:** repo's own `hedge_desk.rates_desk.rates_environment()` — real FRED daily series (mode `REAL_FRED_RATES`, FRED pull HTTP 200). No shutdown/data-blackout framing — FRED live. Numbers are FACT = module fields.

| Metric | Value | As-of |
|---|---|---|
| Fed funds effective rate | **3.88%** | 2026-10-08 |
| Change over 60-day window | **+25 bps** | 2026-08-13 → 2026-10-08 |
| 2Y Treasury (DGS2) | **4.75%** | 2026-10-08 |
| 10Y Treasury (DGS10) | **5.22%** | 2026-10-08 |
| 2s10s slope | **+47 bps** | 2026-10-08 |
| Curve shape | **Upward sloping** (module classification) | — |
| SOFR / EFFR / OBFR | 3.87% / 3.88% / 3.88% | 2026-10-08 |
| SOFR vs EFFR spread | **−1 bp** | 2026-10-08 |

- **Direction of change (INFERENCE from history arrays):** curve slope essentially flat over the window (started ~48 bps, ends 47 bps — a hair flatter), with an intra-window steepening arc. Both ends sold off roughly in parallel (2Y +60 bps, 10Y +59 bps) — a **parallel bear shift**, not a slope regime change. Near-term: both 2Y and 10Y peaked early October (2Y 4.84 / 10Y 5.31 on Oct 5) and eased into Oct 8 (4.75 / 5.22) — short-term pullback off the peak. **Funding stress:** none — unsecured (EFFR) and secured (SOFR) funding rates essentially identical.
- **Directional read for premium pricing:** 10Y at 5.22% = elevated discount rates → pressure on growth multiples (QQQ, NVDA, TSLA most exposed; AAPL, MSFT less so). Shallow +47bp upward slope = positive term premium but no strong growth-acceleration pricing — mixed signal for equity risk premium. The near-term easing off the Oct 5 peak is a modest tailwind into earnings season; if 10Y re-tests 5.30%+ it becomes a headwind — that is what would change this read. No credit-friction angle (SOFR ≈ EFFR): premiums are moving on rate level and event vol, not funding strain.
- Note: all series as of 2026-10-08 — the expected weekend lag (today is Monday), not a data failure. No Yahoo substitution used; module ran exactly as required.

---

## Synthesis — the 3–5 most decision-relevant items

1. **TSLA Oct-21 AMC is the only in-window binary event — and options are pricing it below history.** Implied ±3.97% vs 5.95% historical average-absolute move, with a −14.5% July tail. The Earnings and Premium desks agree: premium into this event = avoid. The desk's real work on Oct 21 starts at automotive gross margin, OCF vs net income, and Q4 guidance — the print does not drive the move.
2. **Weekend escalation is the live oil catalyst.** Three Hormuz mine strikes, Houthi airport attacks, record VLCC rates — Brent $106.65 (+1.8%) in steep backwardation, $12.86 Brent-WTI spread concentrating the premium in seaborne barrels. The curve's long end ($50s–$60s) prices this as a contained disruption, not a structural re-rating — any credible de-escalation headline is the asymmetric move lower.
3. **Oct WASDE was a bearish corn event.** USDA raised the corn yield when the trade expected a cut; Dec corn hit limit-down Friday. Soybeans were saved by Chinese buying. Next scheduled reads: EIA Wed Oct 14 (10:30 ET; consensus poll not yet published — UNVERIFIED) and Nov WASDE Nov 10.
4. **Rates backdrop: EFFR 3.88%, 10Y 5.22%, 2s10s +47bp, zero funding stress (SOFR−EFFR −1bp).** Elevated long rates keep pressure on growth multiples; the easing off the Oct 5 peak is a modest tailwind into earnings season — re-test of 5.30%+ flips it back to headwind.
5. **Calendar notes:** AAPL dividend likely ex Nov 6/9 (right after Nov 2 earnings — not a clean dividend-capture); MSFT's raised $0.98 dividend ex Nov 19 (24th consecutive increase). Quant Lab ledgered 5 new candidates (#59–#63); none promoted past WATCH. Box/Parity: nothing material.

---

## Desk status

| Desk | Status |
|---|---|
| 1. Earnings Event | Complete |
| 2. Dividend Opportunity | Complete |
| 3. Overnight Premium (IV) | Complete — live Yahoo fallback used and labeled (iv-inputs STALE per 18h guard) |
| 4. Open Quant/AI Model Lab | Complete — 5 candidates appended to quant-lab-ledger.md (#59–63) |
| 5. Futures Event | Complete |
| 6. Box/Parity Observer | Complete — nothing material |
| 7. Bonds & Rates | Complete — repo module, live FRED |

No FAILED desks. No shutdown-framing used. All numbers carry sources and as-of timestamps; unverifiable items marked UNVERIFIED.
