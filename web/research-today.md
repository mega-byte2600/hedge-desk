# Hedge-Desk Daily Research Package — Friday 2026-10-23

**Run:** 13:30 PT (16:30 ET — US equities closed; 2026-10-23 weekly options expired at 16:00 ET).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Standing:** paper-only research. No Risk of Ruin work, no trade authorization, no synthetic data. Every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**Desk status:** 6 of 7 desks delivered substantive findings. The **Earnings Event desk FAILED** (see §1) after two attempts returned pointer-only handoffs with no findings; its section is marked FAILED by name, not dropped.

---

## 1. Earnings Event desk — FAILED

**Desk status: FAILED.** Two attempts were made (initial + one Rung-1 retry after a 2–5 min backoff). Both returned pointer-only handoffs ("my report is above") with no substantive findings delivered. Per the self-recovery rule the desk is marked FAILED BY NAME, and no earnings section is invented.

**What was NOT delivered:** 2-week earnings calendar for the watchlist (report dates, BMO/AMC timing, options-implied expected moves, historical average earnings-day moves), and any statement-analysis teardown of this-week reports.

**Cross-desk corroborated dates (from the Premium desk's iv-inputs file read, sourced to its Nasdaq calendar sweep — not a substitute for the desk's own verification):**
| Symbol | Next earnings (per file) | Position vs 2-week window |
|---|---|---|
| MSFT | 2026-10-28 | INSIDE window (5 days out) — timing UNVERIFIED (BMO/AMC not confirmed) |
| AAPL | 2026-11-02 | Just outside window — date UNVERIFIED |
| NVDA | 2026-11-18 | Outside window — date UNVERIFIED |
| TSLA | none in file | Possibly already reported this week — UNVERIFIED |

**Action:** the earnings calendar must be rebuilt on the next run (or via a follow-up) — implied moves and report timing are UNVERIFIED as of this package.

---

## 2. Dividend Opportunity desk — delivered

**Method:** Nasdaq dividends calendar API scanned day-by-day 2026-10-24 → 2026-11-20 (only MSFT appeared for the watchlist); Yahoo v8 chart `events=div` (UA-only) for the watchlist; 2010–2026 histories checked against the desk streak standard (~/workspace/hedge-desk-research/dividend-count-standard.md), MSFT anchored at 24.

### 4-week ex-div calendar (through Nov 20, 2026)

| Name | Ex-div | $/share | Declared | Payable | Flag |
|---|---|---|---|---|---|
| MSFT | **Nov 19, 2026** | **$0.98** | Sep 15, 2026 | Dec 10, 2026 | INCREASE (+$0.07, +7.7%; 24th consecutive year) |
| AAPL | not yet declared | est. $0.27 (forecast only) | expected ~Oct 29, 2026 (FY Q4 earnings) | est. ~Nov 12 (forecast) | none — raise cycle comes with May payment |
| NVDA | not yet declared | est. $0.25 (unconfirmed) | not announced | est. ~Dec 25, 2026 (forecast) | none pending; outside window |
| SPY | ~Dec 18–20 (est.) | ~$1.9 | n/a | n/a | outside window (seasonal INFERENCE) |
| QQQ | ~Dec 22 (est.) | ~$0.8 | n/a | n/a | outside window (seasonal INFERENCE) |
| TSLA | — | — | — | — | no dividend |

**Sources:** Nasdaq dividends calendar API scan (2026-10-23); Microsoft board announcement https://news.microsoft.com/source/2026/09/15/microsoft-announces-quarterly-dividend-increase-7/; AAPL "no future dividends declared" per https://www.zacks.com/stock/research/AAPL/dividend-history and https://stockinvest.us/dividends/AAPL?page=2.

**This week (Oct 19–23):** no increases/cuts/specials announced for watchlist names. Two material 2026 events predate this week: NVDA's 25x raise ($0.01 → $0.25, announced May 2026, first payout ex Jun 4, 2026; plus $80B buyback authorization) and MSFT's +8% raise (Sep 15, 2026).

**Consecutive-increase counts (desk standard — consecutive calendar years counting back in which an increase was ANNOUNCED):** MSFT 24 (anchored; Yahoo-history check shows annual raises 2010–2026, no break); AAPL 14 (verified raises every year 2013–2026); NVDA 1 (2026 raise starts new run; skipped 2025 breaks the prior run — finbold's "three consecutive years" is screener drift against the desk's skipped-year-break rule); SPY/QQQ n/a (ETFs); TSLA n/a.

**Decision-relevant (labeled):**
- **[FACT]** MSFT ex-div Nov 19 is the only in-window watchlist event; payout security very high (AAA; ~39.5% cash payout ratio). **[INFERENCE]** This year's 8% raise trails the last three years' 10%+ pace — consistent with the ~$175B FY2027 capex guide, mild not alarming. Dividend-capture into Nov 19 earns ~0.19%/quarter — not a value play.
- **[FACT]** NVDA's 25x raise + $80B buyback is a capital-return inflection (fiscal Q2 2027 returned ~$26B; FY2026 FCF ~$96.5B). **[INFERENCE]** It validates the cash machine but at ~6.3% forward payout ratio and ~0.44% yield adds no margin of safety — NVDA remains a growth-multiple stock; the dividend is a rounding error.
- **Net desk verdict:** clean calendar — one in-window ex-div, no cuts or specials, no new margin-of-safety information.

---

## 3. Overnight Premium desk (IV) — delivered

### IV-inputs freshness guard
File: `~/workspace/hedge-desk-research/nightly/2026-10-22-iv-inputs.json`, **as_of 2026-10-22T13:54:04-07:00** — ~23.6h at run time → **FRESH** (inside the 26h guard). Failures logged in file: SPY/QQQ atm_iv = None (failed closed — the 10-22 expiry died before the pull). AAPL/MSFT/NVDA/TSLA marks carried 2026-10-23 expiry at DTE=1 — those contracts **died 16:00 ET today (~13:00 PT), ~30 min before this run** → labeled EXPIRED/solver-residuals, not presented as live IV.

### Realized-vol table (file; FACT; window 2026-09-24 → 2026-10-21)

| Symbol | RV 20d | max single-day var share | Window-contingent? |
|---|---|---|---|
| SPY | 9.08% | 0.209 | no |
| QQQ | 16.29% | 0.334 | **YES** |
| AAPL | 17.19% | 0.340 | **YES** |
| MSFT | 21.97% | 0.351 | **YES** |
| NVDA | 25.75% | 0.217 | no |
| TSLA | 35.81% | 0.225 | no |

### LIVE ATM-IV pull (LIVE; Yahoo v7 options, cookie+crumb; pulled 2026-10-23T20:31:56Z = 13:31 PT; post-close settlement marks)

| Symbol | Oct-30 ATM IV (DTE 7) | Nov-20 ATM IV (DTE 28) | Spot | Term-structure read |
|---|---|---|---|---|
| SPY | **15.46%** | 15.48% | 759.97 | flat; no event in window |
| QQQ | **26.27%** | 24.92% | 704.40 | flat, slightly inverted |
| AAPL | **21.31%** | 26.99% | 347.73 | Nov hump = earnings 11-02 in monthly |
| MSFT | **45.66%** | 33.31% | 524.51 | front hump = earnings 10-28 in Oct-30 |
| NVDA | **36.27%** | 43.52% | 210.96 | Nov hump = earnings 11-18 in monthly |
| TSLA | **37.40%** | 39.56% | 372.22 | flat; no event in window |

Raw pull: `~/workspace/goals/hedge-desk-daily-research/hidden_files/live_iv_pull_2026-10-23.json`. Skew note (FACT from pull): on SPY at the ATM point, call IV (17.15%) > put IV (13.81%) — upside-demand skew. Sanity check: front IV exceeds back IV only where an event sits in front (MSFT) — consistent term structure, no parity contradiction observed.

### IV-vs-realized verdicts (labeled)
- **SPY: IV RICH vs realized — clean verdict.** Oct-30 IV 15.46% vs trailing RV 9.08% (+6.4pp) on a non-contingent window. Implied 7-day move ≈ 2.1%. (INFERENCE from FACT)
- **QQQ: WINDOW-CONTINGENT** — 33.4% of 20-day variance from one day; no clean verdict.
- **AAPL: WINDOW-CONTINGENT** — 34.0% single-day share; Nov hump is earnings, not richness.
- **MSFT: WINDOW-CONTINGENT + binary event** — front IV 45.66% ≈ 6.3% expected 7-day move driven by 10-28 earnings; premium into a binary event = **AVOID** per desk rule.
- **NVDA: elevated but event-adjacent** — Oct-30 IV 36.27% vs RV 25.75% (clean window, +10.5pp); Nov hump 43.52% reflects 11-18 earnings in that expiry. (INFERENCE)
- **TSLA: roughly FAIR** — IV 37.40%/39.56% vs RV 35.81%, clean window.
- **IV rank: UNVERIFIED** — no free IV-history source; no rank claim made.

**Decision-relevant:**
1. **[FACT]** MSFT Oct-30 front IV 45.66% prices the 10-28 earnings — textbook hump. **[INFERENCE]** Premium into this binary = AVOID per desk rule. **[UNVERIFIED]** Whether 45.7% is "rich" is unverifiable without a clean realized window.
2. **[FACT]** Three of six realized windows are CONTINGENT — no clean mispricing verdict exists for half the watchlist today.
3. **[FACT]** Only clean "IV rich" read: SPY (+6.4pp vs realized). **[INFERENCE]** On a value lens that's a seller-side richness read, an observation not a position (paper-only). TSLA is the only clean fair-pricing read.

---

## 4. Open Quant/AI Model Lab — delivered

**Ledger:** 12 new candidates appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` as #128–#139 (scorer-run via `research_intelligence`, no hand-scoring); #114 row updated (repo deleted); run logged to `~/memory/2026-10-23.md`. Re-checks: #1/#20/#32/#86 license blocks unchanged; #56 volrec pushed today — iv_history.csv now 3,625 rows covering 34 trading days 2026-09-04→2026-10-23 (today's row included; Yahoo cross-check pending).

**New candidates:**
- **TEST:** #128 ParBproject/options-vol-surface (73) — SPY IV surface from a real 2026-10-22 chain snapshot (1,077 OTM quotes, 11 expiries 7–603d), SVI fit + butterfly/calendar arb audit, MIT, CI green ×3, honest fail-closed framing on SVI calendar violations. #129 Alexden28/equity-vol-forecasting (73) — walk-forward GARCH vs HAR vs LSTM with Diebold-Mariano tests; clean-MIT alternative to #125's NOLICENSE-blocked lane. #130 coldcityjin-arch/backtest-guardian (67) — auditable toolkit with next-bar execution invariant + anchored walk-forward. #133 buildering-dev/sample-backtest-audit (67) — 8-page forensic audit template with DSR.
- **WATCH:** #131 algomaschine/algomaschine-kit (46, AFML stack, no CI); #132 talalmalikllc-debug/volatility-forecasting-study (61, "index CFDs" provenance UNVERIFIED); #134 nathanaelhub/rust-backtester (64); #135 alimohamad2005/leakage-aware-volatility-forecasting (46, headline claims UNVERIFIED); #136 Fukasawa Lean-4 IV-asymptotics proof (57, process reference not a desk tool).
- **ARCHIVE:** #137 arXiv:2610.31141 (flow Sharpe 16–63 → likely selection/lookahead artifacts; scorer 28); #138 arXiv:2610.30637 (American-put theory; 28); #139 arXiv:2610.25822 (37).

**Most decision-relevant:** (1) #128 — first premium-desk-ready SVI arb-audit on a current SPY chain with CI-green evidence; strongest IV-surface candidate since #18. (2) #129 — HAR-X(VIX) + DM tests as the premium desk's best RV-baseline template, clean substitute for blocked #125. (3) #130 + #133 — two-piece validation-lane upgrade (next-bar timing guard + backtest-review template). Gap noted: four TEST candidates opened but no sandbox runs this cycle (next-cycle work per standard).

---

## 5. Futures Event desk (Weather/War/Logistics) — delivered

**ENERGY — FACT (EIA weekly, released Wed Oct 21, week ended Oct 16; via OilPrice/TradingView/Reuters):** commercial crude drew **3.1 mb to 412.5 mb** — deeper than ~0.8 mb consensus, third straight weekly draw, 3% below 5-yr avg. Gasoline drew 3.0 mb (5% below avg). Distillates built an unexpected 1.7 mb (vs expected draw), still 9% below avg. Refinery runs 16.6 mb/d at 93.4% utilization; Gulf Coast stocks at lowest since Jan 2025. Products supplied 21.1 mb/d (4-wk avg), +3.2% y/y.
**Curve (FACT, Yahoo ~4:30pm ET Fri):** Brent prompt (Dec 26) $111.53, +2.4% since the Wednesday report; WTI prompt $103.21; Brent–WTI $8.32. WTI Dec 26 $103.21 → Mar 27 $95.65 → Jul 27 $87.41 — **deep backwardation, −15.3% Dec-to-Jul**. Nat gas prompt $3.05 (backwardated vs Mar). Gold Dec ~$4,011 (safe-haven contango).
**INFERENCE:** curve prices acute prompt tightness + war-risk premium, not demand collapse. **What would change it:** Hormuz de-escalation or a ceasefire restoring ~5 mb/d of Gulf output.
Sources: https://oilprice.com/Energy/Crude-Oil/EIA-Says-US-Crude-Inventories-Sink-Further.html; https://www.tradingview.com/news/reuters.com,2026:newsml_L6N467119:0-us-gulf-coast-crude-oil-stocks-fell-to-lowest-since-january-2025-eia-says/; https://www.reuters.com/business/energy/opec-agrees-principle-keep-november-oil-output-targets-steady-sources-say-2026-10-04/

**AGRICULTURE — FACT (USDA weekly export sales, week ended Oct 15, released Thu Oct 22; via Dow Jones/Morningstar):** soy sales 2.84 MMT (vs 574.9K prior; survey 1.1–3.0), China 2.18 MMT — largest weekly print since Nov 2023; cumulative 2026/27 sales highest since 2022; corn 1.53 MMT (+36% w/w, topped expectations); wheat 239.6K tons (−25% w/w, below expectations). Thursday closes: Nov soy +0.6% to $12.53/bu (snapped 8-session losing streak); Dec corn −0.6% $4.605; Dec wheat −0.6% $6.2475.
**INFERENCE:** corn/soy/wheat curves all in contango (ample forward supply) — the China soybean demand shows in the nearby, not deferred; no verified South American planting disruption this week.
Sources: https://www.morningstar.com/news/dow-jones/202610227236/us-soybean-export-sales-see-big-weekly-rise; https://www.morningstar.com/news/dow-jones/2026102210024/soybean-futures-gain-amid-strong-export-sales-daily-grain-highlights

**GEOPOLITICS/LOGISTICS — FACT:** Iran's FM offered a conditional 7-day plan to reopen Hormuz (Oct 21); Trump rejected it. Kpler via Reuters (Oct 22): Hormuz crude flows recovered to ~11.7 mb/d in October (~82% of pre-war) on US-escorted convoys; UKMTO logged a record 12 attacks last week. Houthi strikes hit Shaybah/Dammam and the Yanbu pipeline link (restored).
**UNVERIFIED/single-source (not relied on):** Iranian state TV claim of 7 tankers damaged; a blog's 35 Qatari LNG cargoes force majeure; a LinkedIn digest's "Brent $117."
**INFERENCE:** market prices a contested-but-functioning strait with a ~$38/bbl war premium over pre-war Brent (~$73). **SPECULATION:** post-Nov-3 strike risk (NYT-reported US-Israeli plans, secondhand) vs war-fatigue diplomacy — treat oil volatility as the operative risk, not direction.
Sources: https://www.reuters.com/commentary/reuters-open-interest/dont-mistake-mideast-oil-rebound-normality-2026-10-22/

**MACRO → index futures — FACT (secondhand reads, labeled):** CME FedWatch via PANews (Oct 22): Oct 28 FOMC **83.9% hold / 16.1% +25bp**; December 76% cumulative +25bp, 14.2% +50bp. Kalshi (Oct 23): 91% hold. Target 3.75–4.00%, EFFR 3.88%. **Core PCE Thu Oct 29, 8:30am ET** — the day AFTER the FOMC decision (BEA release schedule, primary source verified 2026-10-23). No PCE print can move the Oct 28 outcome; September CPI (3.7%, core +0.3%) is the last inflation read the Fed sees. White House: Section 338 Canada tariffs modified (effective Oct 30); Oct 16 EO waived Graham Act Russia-oil tariffs pending monitoring; Oct 22 EO directed wind-turbine-import negotiations (no new tariffs).
**INFERENCE:** hawkish-skip, not dovish-pivot — December is the live meeting (76% for +25bp). With energy-driven inflation, the spillover to SPY/QQQ is higher discount rates and multiple compression on long-duration growth; ES Dec closed −0.5% on the day.
Sources: https://www.panews.io/articles/01a160ed-1cc2-7188-9486-977756e5bf12; https://www.whitehouse.gov/fact-sheets/2026/10/fact-sheet-president-donald-j-trump-further-modifies-canadian-products-subject-to-tariffs-under-section-338/

**Decision-relevant:** (1) **[INFERENCE, high conviction]** Third straight EIA draw + deep backwardation keep energy as persistent headline-inflation driver → rate-path surprise risk is hawkish; December (76% priced) is the live meeting. (2) **[FACT of tension / SPECULATION on resolution]** Hormuz binary: escalation vs ceasefire restoring ~5 mb/d. Brent $111+ holds ~$38/bbl war premium. (3) **[FACT]** Next week's event stack: FOMC Wed 10/28 (hold ~84–91% priced) → Core PCE Thu 10/29 (8:30am ET, the day after the decision — no PCE print can move the Oct 28 outcome). No federal-data disruption — EIA (Wed) and USDA (Thu) published on schedule.

---

## 6. Box/Parity Observer — delivered (light touch)

No parity-violation analysis published in the last ~2 weeks (put-call parity on SPX/SPY/NDX/QQQ, box-spread dislocations, dividend-arbitrage anomalies). Two adjacent CBOE items:
1. **[FACT]** New **SPX Box Rate index (BOX20X26)** began disseminating 07-OCT-2026 (Cboe Global Indices notice C2026100604): box-spread-implied risk-free rate from SPX boxes over the Global Indices Feed. **[INFERENCE]** Infrastructure, not a signal — but the cleanest public feed for monitoring whether SPX box-implied rates detach from SOFR/funding; worth a glance in future runs for funding-stress reads.
2. **[FACT]** Cboe BuyWrite indices methodology change effective Oct 15, 2026 (announced Sep 3, C2026090301): BXTB/BXHB/BXLB/BXVBW/BXWBW now use last traded option price across OPRA exchanges in the 3:45–4:00 ET window (Cboe Hanweck theoretical fallback) instead of the proposed VWAP. **[INFERENCE]** Index values only, not executable parity — noted so a mid-October step in any BuyWrite index series isn't misread as a market move.

**Net:** no new put-call/box parity violations or methodology changes affecting executable parity. Deterministic parity remains binding; nothing actionable.

---

## 7. Bonds & Rates desk — delivered

**Module output (verbatim, FRED daily series via `rates_desk.rates_environment()`, `mode: REAL_FRED_RATES`; all prints as-of 2026-10-22 — normal one-day weekend-adjacent lag):**

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

**Direction of change (FACT, recomputed from module history arrays):** prior day (10-21): 10Y 5.13%, 2Y 4.81% → 2s10s 32 bp. Now: 10Y 4.96%, 2Y 4.65% → 31 bp. **Bull flattening −1 bp:** both legs fell nearly in parallel (10Y −17 bp, 2Y −16 bp). 60-day context: 10Y peaked 5.29% on 09-30 (−33 bp since); 2Y peaked 4.92% on 09-28 (−27 bp since).
**Funding stress (FACT):** SOFR − EFFR = +2 bp; OBFR = EFFR. No funding-stress signal.
**Directional read for premium pricing:**
- **[FACT]** 10Y at 4.96% is in the top quartile of the 60-day range (4.64–5.29%).
- **[INFERENCE]** Elevated long rates = elevated discount rates = continued pressure on long-duration growth multiples. Value-investor read: ~5% risk-free competition compresses the equity risk premium; NVDA/TSLA (highest duration on the watchlist) most exposed; AAPL/MSFT carry less rate sensitivity.
- **[INFERENCE]** Stable upward-sloping 31 bp curve gives no curve-driven reason to expect a vol-regime shift on rates alone heading into the Oct 28 FOMC. Parallel rally reads as benign drift toward the meeting, not flight-to-quality.
- **[FACT]** Policy stance is hiking-phase (+25 bp over the module's 60-day window), not easing. The money-market-leg vs 2Y inversion (4.65 − 3.88 = 77 bp) prices further tightening pressure, not cuts. **[SPECULATION]** The Oct 28 decision itself is unverifiable from this data.

---

## Synthesis — 3-5 most decision-relevant items

1. **Earnings-binary week into MSFT's 10-28 report.** [FACT] MSFT Oct-30 front IV 45.66% prices ~6.3% over 7 days with earnings inside the expiry — premium into a binary event = AVOID per desk rule. [FACT] QQQ/AAPL/MSFT realized windows are WINDOW-CONTINGENT, so half the watchlist carries no clean IV-vs-realized verdict today. The Earnings desk FAILED (dates/timing/implied moves UNVERIFIED) — do not build around an earnings calendar until it is rebuilt.
2. **Rate path is the year's decisive macro variable, and it is hawkish.** [FACT] EFFR 3.88%, 10Y 4.96% (bull-flattened −1 bp on the day), SOFR−EFFR +2 bp (no stress). [INFERENCE, corroborated by Futures desk] The market prices the *December* meeting (76% for +25bp), not a pivot; energy-driven inflation (third straight EIA draw, Brent $111.53, −15.3% backwardation) keeps headline-CPI pressure on. [INFERENCE] ~5% long rates compress the ERP and punish duration — NVDA/TSLA most exposed, cash-flow names least.
3. **Next week's event stack: FOMC Wed 10/28 (~84–91% hold priced) → Core PCE Thu 10/29 (8:30am ET, post-decision).** [INFERENCE] With no September PCE before the decision, the Oct 28 vol event is the statement itself; the plausible vol path into month-end is December-repricing, not a PCE print. Position-reads should treat Wednesday as near-certain-hold-with-live-December-repricing.
4. **The only clean paper-desk observations.** [FACT→INFERENCE] SPY IV rich vs realized (+6.4pp, clean window) — seller-side richness read, an observation not a position. TSLA implied ≈ realized — fair-priced on a clean window. NVDA Oct-30 IV 36.27% vs RV 25.75% (+10.5pp, clean window) but event-adjacent (11-18 earnings in the Nov hump).
5. **Quant lab hands the desks two upgrades.** #128 (current SPY IV-surface SVI arb-audit, CI-green) is the strongest premium-desk surface candidate since #18; #129 (HAR-X(VIX) walk-forward with DM tests) is the best RV-baseline template and cleanly substitutes for the NOLICENSE-blocked #125.

**Cross-desk consistency check:** Rates desk (FRED EFFR 3.88%, 10Y 4.96%) and Futures desk (FedWatch 83.9% hold / Kalshi 91% hold, December 76% +25bp) agree on a hawkish-skip posture. Premium desk term structure (MSFT front hump, AAPL/NVDA Nov humps) is consistent with reported earnings windows. No contradictions requiring resolution.

---

## Traceability
- iv-inputs file: `~/workspace/hedge-desk-research/nightly/2026-10-22-iv-inputs.json` (as_of 2026-10-22T13:54:04-07:00, FRESH per 26h guard)
- live IV pull (LIVE, 2026-10-23T20:31:56Z): `~/workspace/goals/hedge-desk-daily-research/hidden_files/live_iv_pull_2026-10-23.json`
- quant-lab ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (#128–#139 appended; #114 updated)
- rates module: `cd ~/workspace/github/hedge-desk && python3 -c "from hedge_desk import rates_desk; import json; print(json.dumps(rates_desk.rates_environment(), default=str))"` (exit 0, first attempt)
- EIA weekly (Wed 10/21), USDA export sales (Thu 10/22) — published on schedule; no federal-data disruption
- All Yahoo pulls used `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; options pulls used the cookie+crumb handshake
