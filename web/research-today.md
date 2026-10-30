# Hedge-desk daily research — Fri 2026-10-30

**Run:** scheduled 13:30 PT run, all seven desks reported, synthesized ~14:30 PT. No desk dropped.

**Standing labels:** FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it. Paper-only research; no trade authorization; no Risk of Ruin contact.

**Source-reliability flag — Nasdaq earnings calendar API gave inconsistent results across desks this run (read before trusting any calendar claim below).** The Earnings desk's queries for every date Nov 2–13 returned **zero** watchlist rows, including no AAPL row for Nov 2; the Premium desk's pull reported AAPL Nov 2 and MSFT Oct 28 rows from the same API. Resolution: the Nasdaq calendar is treated as **unreliable/incomplete this run**. AAPL's Nov 2 date rests on Apple's own IR announcement (via MacRumors) plus secondary corroboration, and NVDA's Nov 17 date rests on NVIDIA's Oct 28 announcement — neither rests on a clean Nasdaq confirmation. Do not cite "Nasdaq calendar confirms" for either date in downstream briefs until the API is re-checked.

## Market backdrop (indicative post-close marks, NOT settled closes)

Post-close Yahoo v7 options-chain pull, Fri Oct 30 ~13:40 PT / ~16:40 ET [FACT, with the Premium desk's non-synchronicity caveat: the underlying quote drifted between pulls minutes apart while option marks sat post-close, so these levels are indicative, not precise]. Oct 29 closes from the prior session for comparison:

| Symbol | Oct 29 close | Oct 30 post-close mark | Change (recomputed) |
|---|---|---|---|
| SPY | $769.36 | $753.38 | −2.08% |
| QQQ | $715.34 | $690.49 | −3.47% |
| AAPL | $348.91 | $344.63 | −1.23% |
| MSFT | $530.14 | $521.91 | −1.55% |
| NVDA | $213.66 | $204.64 | −4.22% |
| TSLA | $403.30 | $399.81 | −0.87% |

Read: a hard down day concentrated in growth/QQQ beta (NVDA −4.2%, QQQ −3.5%), on top of the Oct 29 AMZN/INTC after-hours damage and today's Hormuz oil spike (see §5) [INFERENCE from the marks + §5 catalysts]. Treat the levels as indicative until settled closes are verified.

## 1. Earnings Event desk

| Symbol | Status | Report date / timing | Consensus | Options-implied move | Historical earnings-day move |
|---|---|---|---|---|---|
| **AAPL** | **Upcoming — the window's only watchlist binary** | **Mon Nov 2, 2026, after close** — release 1:30pm PT, call 2:00pm PT | EPS $1.98, revenue $112.95B (Zacks); Apple guided revenue growth 9–11% YoY, gross margin 47–48% | **~4.3%** (Nov 4 expiry ATM straddle $14.90 / $344.63, Yahoo v7 chain pulled Oct 30; Nov 6 straddle 4.70%) | Fiscal-Q4 reports: up only 6 of 17, median −0.9% (third-party tally — INFERENCE-grade, not primary data); last report (Jul 30, 2026) fell 7.3% next day |
| MSFT | Already reported | Wed Oct 28 AMC (FY27 Q1) | **Beat (FACT, Microsoft release):** revenue $92.3B (+19%), GAAP EPS $4.92 (+32%), non-GAAP EPS $4.89 (+18%), Azure +48%. Do not conflate with the $4.71 Nasdaq forecast figure — that was the forecast, not the print | UNVERIFIED (no citable pre-report implied-move figure found) | Actual: −0.16% Oct 29 ($531.01 → $530.14), then −1.55% Oct 30 |
| TSLA | Already reported | Wed Oct 21 AMC (Q3 2026) | Adj. EPS $0.48 vs ~$0.43–0.46 consensus (beat); revenue $28.05B vs ~$28.06–28.44B (miss on one consensus cut) | UNVERIFIED (one recap says the actual move was "less than options had priced in" but gives no number) | Actual: −3.1% Oct 22 ($386.47 → $374.58) |
| NVDA | Outside window — flag now | **Tue Nov 17, 2026, after close** (FY27 Q3) — company-announced Oct 28; call 2:00pm PT, CFO commentary ~1:20pm PT | EPS ~$2.47, revenue ~$108.8B (MarketBeat); company guided revenue $108.0B ±2%, gross margin 74.0% ±50bp | Not computed (outside window) | — |
| SPY / QQQ | ETFs; no earnings | — | — | — | — |

Sources: Apple IR schedule via MacRumors Oct 6, 2026 (https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/); Zacks AAPL preview Oct 29, 2026 (https://www.zacks.com/stock/news/3018992/apples-q4-earnings-loom-buy-or-sell-aapl-stock-ahead-of-results); MSFT primary release (https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast); NVDA date announcement via https://www.ad-hoc-news.de/boerse/news/corporate-news/nvidia-corporation-stock-november-17-call-sets-next-results-test/70429419; AAPL options: Yahoo v7 chain, cookie+crumb, Oct 30 ~13:45 PT.

- **NVDA date conflict, resolved:** Nov 17 (company-announced Oct 28) vs MarketBeat's Nov 18 estimate vs Nasdaq calendar silence. The company announcement wins; MarketBeat's Nov 18 is the conflicting secondary estimate; Nasdaq's silence is consistent with this run's demonstrated calendar incompleteness, not evidence against Nov 17. The Premium desk's "Nov 18 UNVERIFIED" note is superseded by the Earnings desk's Oct 28 announcement citation — carry Nov 17.
- **INFERENCE:** AAPL's bar is the December-quarter guide and the memory-cost/margin read, not the September quarter, which is largely pre-announced via Apple's own 9–11% guidance. MSFT's flat reaction to a clean beat is consistent with a print already priced in and/or capex ($39.4B in the quarter, per recap of the release) doing the damage — but the pre-earnings implied move is UNVERIFIED, so "vol crush vs priced-in" cannot be separated.
- **Verdict:** AAPL Nov 2 is the only live binary in the window; ~4.3% priced against a negative-leaning fiscal-Q4 history — premium into this binary event = avoid per the standing rule. **What would change this:** the Dec-quarter revenue guide on the Nov 2 call, or a gross-margin guide outside 47–48%.

## 2. Dividend Opportunity desk

Nasdaq dividends calendar API swept for every trading day in the window (Oct 30, Nov 2–6, 9–13, 16–20, 23–27; Nov 11 and Nov 26 returned zero rows — market holidays) plus per-symbol Nasdaq dividend histories. No watchlist ex-date appears on any sampled day except MSFT Nov 19.

| Name | Ex-date | Amount | Pay date | Flag |
|---|---|---|---|---|
| MSFT | Thu Nov 19, 2026 | $0.98 | Dec 10, 2026 | **24th consecutive annual increase** per the desk count standard (Sep 15, 2026 board raise $0.91 → $0.98, Nasdaq-confirmed declaration date) — no new raise since, so no drift from the anchor |
| AAPL | — | — | — | **UNDECLARED** — most recent declaration Jul 30, 2026 ($0.27, ex Aug 10, paid Aug 13); the Nov 10 / $0.27 listing on projection sites is a projection, not a declaration |
| NVDA | — | — | — | Last declared Aug 26, 2026 ($0.25, ex Sep 10, paid Oct 1); next declaration normally accompanies earnings (~Nov 17); any resulting ex-date falls in early December, outside window |
| SPY | None in window | — | — | Last ex Sep 18, 2026; next quarterly ex mid-December, outside window (timing = INFERENCE) |
| QQQ | None in window | — | — | Last ex Sep 21, 2026 ($0.75143); next quarterly ex mid-December, outside window (timing = INFERENCE) |
| TSLA | None — pays no dividend | — | — | No dividend program; Nasdaq returns N/A |

Sources: Nasdaq calendar API (`api.nasdaq.com/api/calendar/dividends?date=…`, pulled Oct 30) and per-symbol histories (`api.nasdaq.com/api/quote/{SYM}/dividends`), cross-checked against ~/workspace/hedge-desk-research/dividend-count-standard.md.

**Flags:** No new increases, cuts, or specials among watchlist names in the window.

**Declaration watches (what would change this section):** AAPL Mon Nov 2 AMC earnings (declaration normally accompanies the print; if declared, a ~Nov 10 ex-date at presumably $0.27 enters the window); NVDA ~Nov 17 earnings (early-December ex-date, outside window but relevant to the next run).

**Verdict:** The only actionable dividend date in the next 4 weeks is MSFT's Nov 19 ex-date ($0.98, 24th consecutive annual increase).

## 3. Overnight Premium desk (IV)

**Baseline file (STALE-labeled, inside the guard):** `~/workspace/hedge-desk-research/nightly/2026-10-29-iv-inputs.json`, **as_of 2026-10-29T13:54:09−07:00** — ~23.5h old at run start, **inside the 26h freshness guard: usable, labeled "as of Oct 29 post-close" throughout, never presented as today's data.** Verified on disk.

**Live supplement (LABELED):** Yahoo v7 options chain pull, cookie+crumb handshake, Fri Oct 30 ~13:40 PT / ~16:40 ET, post-close. Oct 30 expiries are dead (expired 16:00 ET), so the first live expiry per symbol is used. Post-close marks are indicative, not precise (see backdrop caveat).

### Stale-jump screen (Oct 29 post-close file) — FACT
**No symbol is WINDOW-CONTINGENT.** Max single-day variance shares (20-day window, Oct 1–28): SPY 0.186, QQQ **0.288**, AAPL 0.125, MSFT 0.189, NVDA **0.285**, TSLA 0.209. **Flag: QQQ (28.8%) and NVDA (28.5%) sit just under the 30% threshold** — a single large day next week flips either to WINDOW-CONTINGENT, voiding any clean IV-vs-realized verdict on that symbol. IV-vs-realized comparisons below are valid today but fragile for QQQ and NVDA.

### IV snapshot — live levels, Oct 30 post-close (FACT, Yahoo v7 options)
ATM IV = mean of nearest-strike call/put IV on the stated expiry. Realized 20d from the Oct 29 post-close file (annualized std of 19 log returns, Oct 1–28 closes).

| Symbol | Price (live) | Front live expiry (DTE) | Front ATM IV | 2nd expiry (DTE) | 2nd ATM IV | Realized 20d (Oct 29 file) | IV ÷ realized (front) |
|---|---|---|---|---|---|---|---|
| SPY | 753.38 | 2026-11-02 (3) | 13.6% | 2026-11-03 (4) | 15.3% | 10.3% | 1.32× |
| QQQ | 690.49 | 2026-11-02 (3) | 18.0% | 2026-11-03 (4) | 22.5% | 20.1% | 0.90× |
| AAPL | 344.63 | 2026-11-04 (5) | **43.1%** | 2026-11-06 (7) | 40.3% | 13.5% | **3.19×** |
| MSFT | 521.91 | 2026-11-02 (3) | 19.3% | 2026-11-04 (5) | 28.3% | 20.1% | 0.96× |
| NVDA | 204.64 | 2026-11-02 (3) | 27.5% | 2026-11-04 (5) | 37.5% | 31.0% | 0.89× |
| TSLA | 399.81 | 2026-11-02 (3) | 30.1% | 2026-11-04 (5) | 43.4% | 40.0% | 0.75× |

Notes: SPY/QQQ ATM IV was null in the Oct 29 file (failed closed on the expired Oct 29 expiry — solver residuals on dead contracts, correctly rejected); today's live pull fills that gap. AAPL has no Nov 2 weekly in Yahoo's chain; its first live expiry is Nov 4, which captures the Nov 2 earnings event.

### Elevated-IV flags
- **AAPL — ELEVATED, earnings-driven (FACT: 43.1% front IV vs 13.5% realized).** Classic pre-earnings hump; the premium is event pricing, not "rich" vol.
- **Nov 4 leg elevation across MSFT (+9.0 pts vs Nov 2), NVDA (+10.0), TSLA (+13.3), and second-leg rises in SPY/QQQ (INFERENCE):** expiries spanning Nov 3–4 carry event premium consistent with the Nov 3 U.S. midterm election sitting inside those windows. Labeled INFERENCE — the alternative is a weekly-expiry liquidity artifact. What would change it: a Nov 5+ expiry trading back down toward the Nov 2 level after Nov 4, or confirmation that the Nov 4 chains are thin/wide.
- **No other elevated flags.** QQQ, MSFT, NVDA, TSLA front IVs sit at or below trailing realized vol — no complacency signal, no richness signal; roughly fairly priced against the recent regime.

### Earnings inside the window — AVOID premium into binary events
- **AAPL earnings Mon Nov 2, after hours — CONFIRMED on the company announcement (see source-reliability flag above; do not cite Nasdaq as the confirmer).** The Nov 4 expiry (43.1% IV) and Nov 6 expiry (40.3%) both span the event. **Desk rule applies: premium into this binary event = avoid** — long premium pays 3.2× realized vol for a single print; short premium faces gap risk through the print.
- **MSFT earnings already passed (Oct 28).** The Oct 29 file's 28.4% MSFT ATM IV has crushed to 19.3% at 3 DTE, in line with 20.1% realized. No earnings in MSFT's current window.
- **NVDA earnings Nov 17 (company-announced; see §1 resolution).** No earnings hump in NVDA's near-window IV (front 27.5% < 31.0% realized), consistent with earnings ~3 weeks out.
- **SPY, QQQ, TSLA:** no earnings in window.

### Skew and parity sanity checks
- **Skew (FACT, live pull):** SPY Nov 2 put IV 15.6% > call IV 11.6% — normal equity downside skew. TSLA Nov 4 put 46.0% > call 40.8% — same. **QQQ Nov 2 is inverted: call IV 19.6% > put IV 16.4% (INFERENCE: upside-chase positioning or call demand; alternative is a stale call quote — a flag, not a signal).**
- **Put-call parity spot check, SPY Nov 2 ATM (FACT, second pull minutes later):** C−P = −$1.91 vs S−PV(K) = +$0.72, apparent gap −$2.63. **Per the parity rule, the math wins and the inputs are suspect, not the market:** the underlying quote drifted $2.09 (753.38 → 755.47) between the two pulls minutes apart while option marks sat post-close, and SPY call IV moved 11.6% → 8.6% between pulls. This is a non-synchronous post-close data artifact, **not** a tradeable violation — no action. It also means today's live IV levels are indicative, not precise.

### UNVERIFIED (fail-closed)
- **IV rank percentiles: UNVERIFIED for all six names.** No free source supplies IV history; only the IV-vs-realized comparison above is verifiable. No percentile rank is asserted.
- **Cause of the Nov 4 leg elevation: INFERENCE (election premium), not FACT.**

### Verdicts
1. **AAPL front premium is event-priced, not mispriced — avoid binary-event premium.** Would change if: earnings date moves out of the Nov 4 window, or post-print IV crushes below ~20% while realized stays ~13%.
2. **Index and single-name front IV (ex-AAPL) is fairly priced vs trailing realized — no vol edge either way.** Would change if: realized regime breaks (a >2σ day), or QQQ/NVDA flip WINDOW-CONTINGENT, voiding the realized baseline.
3. **Nov 3–4 expiries carry event premium (INFERENCE: midterms).** Would change if: Nov 5+ expiries trade at Nov 2 levels, showing the hump was expiry-specific liquidity, not event pricing.
4. **No parity/alpha signal from the SPY parity gap — post-close data artifact.** Would change if: the gap persists in live, synchronous, tight-market quotes during regular hours.

## 4. Open Quant/AI Model Lab

**Sweep window:** arXiv q-fin submissions Oct 29, 2026 (8 hits; no Oct 30 submissions indexed yet at sweep time ~13:45 PT — Oct 30 submissions announce in the next feed) + GitHub repos created Oct 29–30 (volatility search: 73 hits, pages 1–2 reviewed; "options" search leg too noisy at 394 hits but surfaced one candidate). All scores from the repo's own scorer (`hedge_desk.research_intelligence.assess_source`; bands TEST ≥65, WATCH ≥45, ARCHIVE <45). Ledger checked first — no duplicates of rows #170–#181. **6 new candidates appended to the ledger as rows #182–#187.** No TEST, no INTEGRATE movement this run.

| # | Candidate | Score | Disposition | Why |
|---|---|---|---|---|
| 182 | "Information Flow and Market Risk: Transformer-Based Evidence on Sentiment and Volatility Dynamics" — arXiv:2610.39636v1, 29 Oct 2026 (q-fin.RM) | 48 | **WATCH** | Abstract read at source — ModernFinBERT news sentiment vs conventional predictors for vol forecasting, 11 US stocks, Yang-Zhang target, 1/5/22-day horizons, walk-forward expanding + rolling windows, multiple-testing + HAC-adjusted comparisons. Headline (source-reported, UNVERIFIED — full paper not read): naive persistence achieves the lowest average QLIKE at all horizons; HAR-VIX wins the most individual comparisons but not mean loss; text sentiment improves HAR in only 2 of 33 expanding-window comparisons, neither significant under longer HAC bandwidths. Honest-negative result in the premium desk's vol-forecasting lane — complements #170 (LSTM-vs-HAR negative) and #129. No author code link → reproducibility not established. |
| 183 | "Comparing tail forecasts: the number of exceedances is the sample size" — arXiv:2610.40366v1, 29 Oct 2026 (q-fin.MF/math.ST) | 45 | **WATCH** (band floor) | Abstract read at source — for tail forecasts, the score difference is known in advance except on exceedance days, so exceedance count, not observation count, is the effective sample size; Diebold-Mariano test declares the less conservative forecaster better with at least the no-exceedance probability when exceedances are scarce (small-sample corrections don't remove it; bootstrap-t largely does). Directly relevant to the purged-WF lane (#22/#54): any desk comparison of tail/quantile forecasts on rare events inherits this pitfall. No author code link → reproducibility not established. |
| 184 | "The Generalised Kessler Syndrome and the Persian Gulf" — arXiv:2610.40129v1, 29 Oct 2026 (q-fin.PM) | 28 | **ARCHIVE** | Abstract read at source — supply-chain fragility theory applied to Persian Gulf maritime-supply restrictions from spring 2026, Strait of Hormuz restriction as trigger; Kelly weakest-link allocation conclusion. Context for the futures desk's Hormuz narrative, not a desk procedure: no data, no calibration, no code. Band discipline. |
| 185 | faten20/volatility-forecasting-ml — S&P 500 vol: 7 ML models vs HAR-RV/GARCH, DM tests, VIX ablation (GitHub, created 2026-10-30, MIT, 0 stars) | 43 | **ARCHIVE** | README + tree verified via GitHub API — notebook-only (no tests/, no CI). Claims read at source, code NOT run: 5-day-ahead SPX RV, 504-day OOS test period 2024-10-18→2026-10-22; all 7 ML models beat HAR-RV/GARCH; Ridge ≈ complex models; ablation: HAR+VIX alone delivers most of the gain, Parkinson adds nothing once VIX is in; no model anticipated the April 2025 shock. Method value is real but notebook-only + unrun + 0 stars caps it below WATCH. INFERENCE: the VIX-ablation finding is noted as a method idea for the premium desk's RV-baseline lane despite the archive. |
| 186 | coreyczhang/options-pricing-engine — C++17 European BS + MC Greeks engine, validated vs closed form (GitHub, created 2026-10-30, MIT, 0 stars) | 37 | **ARCHIVE** | README + LICENSE verified via raw fetch (repo metadata endpoint returned nulls this run — content verified directly, not the endpoint). BS closed form + analytic Greeks, MC with standard errors, SE itself tested, variance reduction measured not asserted; tests/ + CI + docs. Honest scope statement (European only, no surface/calibration, no market data, no dividends). Lane is crowded and pinned (#33, #121, #106); no desk differentiator (no IV solver, no live chain, no arb check). Band discipline. |
| 187 | Rubenvalrom/Forecasting-Stock-Volatility-from-Annual-Report-Text — 10-K risk text → vol forecasting (GitHub, created 2026-10-30, MIT, 0 stars) | 28 | **ARCHIVE** | README + tree verified via GitHub API — README states only the research aim; root tree has Makefile + pyproject.toml but no code dirs, no data, no results, no tests/ — a scaffold, not evidence. Adjacent to #182 (text→vol) but with nothing to score beyond the question. Reopen if code + results land. |

**Triage exclusions — no ledger rows (scope misses / unusable code don't get rows):** arXiv 2610.39198 (evolutionary game theory), 2610.39205 (crypto cross-sectional), 2610.39458 (pump.fun/Solana), 2610.39896 (strict local martingale theory), 2610.40404 (Bass/MOT theory); GitHub NOLICENSE items (incl. a Guycomo historical-IV dashboard + live-IV surface, both README-only and IBKR-gated; vishal-chavda-code/options-market-intel, OCC/Cboe free-data angle noted but NOLICENSE); crypto/FX/India/slots/gaming scope misses.

**Standing positions carried forward:** #171 darm-vol remains the run's only TEST (scorer 66) — sandbox still pending; the weekly follow-up job owns it, not this sweep. A re-check of its repo metadata returned nulls from the API endpoint this run (same quirk as #186) — treated as an endpoint quirk, not repo absence; no status change claimed. #170 (WATCH, 64) LSTM-vs-HAR honest negative and #179 (WATCH, 48) Hawkes feed-artifact hygiene lesson stand; #182's sentiment negative now makes three honest negatives in the vol-forecasting lane — the pattern (simple + VIX beats complex) is the lane's story, not any single model. No INTEGRATE movement.

**Ledger:** rows #182–#187 appended to ~/workspace/hedge-desk-research/quant-lab-ledger.md (verified on disk), plus a 2026-10-30 daily note. No candidate lives only in a daily file.

**Verdict:** Quiet sweep — two WATCH adds (one honest-negative vol paper, one forecast-evaluation methodology correction), four ARCHIVEs on band discipline, zero TEST/INTEGRATE. **What would change it:** #182's full paper showing a sentiment edge at some horizon/window, #183's code release, #185 gaining tests + a runnable script, or the Oct 30 arXiv announcements landing in tomorrow's feed.

## 5. Weather/War/Logistics Futures Event desk

### Fresh catalysts triaged

**A. Strait of Hormuz tanker attacks — FRESH, market-moving today [FACT, with one UNVERIFIED element]**
- UK Maritime Trade Operations (UKMTO) reported Fri Oct 30 that a tanker transiting the Strait of Hormuz was attacked by a small boat carrying two explosive devices, causing a fire in the engine room and temporarily disabling the vessel; the vessel later resumed its voyage. Sources: https://www.morningstar.com/news/dow-jones/202610308885/nymex-overview-oil-refined-products-climb-on-middle-east-supply-concerns-opis ; https://investorsking.com/2026/10/30/oil-prices-rise-above-116-as-strait-of-hormuz-attack-raises-supply-concerns/
- A second, related report lists two tankers struck on consecutive days — MT ARZANAH (Liberia-flagged) on Oct 29 and MT LOUISE 1 (Panama-flagged) on Oct 30 — with no crew injuries reported. Source: https://wearemainstreet.org/world/2026/10/30/maritime-security-risks-strait-hormuz
- **UNVERIFIED:** Responsibility for the attack(s) had not been established as of the Oct 30 reports.
- **UNVERIFIED:** Yemen's Houthi militants claimed Thu Oct 29 to have struck Saudi facilities including Ras Tanura and Rabigh refineries and an Aramco facility at Abqaiq. Morningstar/Dow Jones explicitly describes these as "unverified claims," and independent confirmation of damage was limited in the reporting. Do not treat the Saudi-facility strikes as confirmed. Source: https://www.morningstar.com/news/dow-jones/202610305822/the-week-in-oil-crude-stays-elevated-ahead-of-us-midterms
- **INFERENCE:** The market reaction is consistent with a renewed geopolitical risk premium, not with a confirmed physical supply cut — no confirmed Hormuz closure or confirmed Saudi production loss is in the sourced reporting.
- **What would change this read:** A UKMTO/operator confirmation of a Hormuz closure or sustained transit halt, confirmed damage at a named Saudi facility, or a verified attribution — any of which would upgrade this from risk-premium to physical-supply event; conversely, a quiet weekend transit with no further attacks would support premium fade.

**B. Ukraine strike on Russian refining resumes — FRESH [FACT]**
- Ukraine struck the Novokuibyshevsk refinery in Russia's Samara region early Fri Oct 30, ending a two-week pause in attacks on Russian refining infrastructure. Source: https://www.morningstar.com/news/dow-jones/202610308885/nymex-overview-oil-refined-products-climb-on-middle-east-supply-concerns-opis
- Context: Russian oil freight rates remained at record highs in late October amid Black Sea attacks and a tanker shortage: Urals to India ~$30/bbl or more (vs ~$20 in September); a ~100,000-ton Aframax Baltic-to-western-India voyage ~$23m (vs ~$13–16m in September); a Black Sea-to-India Suezmax voyage at a record ~$30m (vs ~$19m in September); Black Sea loadings "largely disrupted since the summer" by drone attacks. Source: https://www.maritimeprofessional.com/news/russian-freight-rates-remain-high-423993 (published 2026-10-30)
- **INFERENCE:** Freight/logistics costs, not just crude price, are a live transmission channel for Russian barrels — elevated freight compresses netbacks even where headline crude is unchanged.
- **What would change this read:** A sustained halt to refinery strikes, or a normalisation in Black Sea loading/freight rates, would weaken the logistics-premium leg.

**C. EIA Weekly Petroleum Status Report, week ended Oct 23 — released Wed Oct 28, 10:30 ET [FACT]**
- Crude inventories **fell 1.9m bbl to 410.6m bbl**, vs a Reuters-poll expectation of a 15,000-bbl build — a bearish-for-supply (bullish-price) surprise. Cushing stocks fell 624,000 bbl; Gulf Coast stocks fell to their lowest since December 2024.
- Gasoline stocks **rose 3.9m bbl to 209.2m bbl**, vs an expected 0.9m-bbl draw — opposite surprise to crude. Distillate stocks **fell 1.5m bbl to 102.8m bbl**, vs an expected 0.9m-bbl draw.
- Refinery runs fell 123,000 bpd; utilisation fell 0.6 pp to 92.8%. Net crude imports fell 796,000 bpd; exports rose 1.4m bpd to 4.85m bpd. Total product supplied fell 1.022m bpd to 20.21m bpd. Source: https://srnnews.com/us-crude-and-distillate-inventories-fall-gasoline-stocks-rise-eia-says/ (Reuters, Oct 28, 2026)
- **INFERENCE:** The crude/distillate draws support prompt tightness; the gasoline build argues against a uniform products squeeze — the tightness is concentrated in crude and distillates, not gasoline.
- **What would change this read:** Next Wednesday's report (Nov 4) — a crude build or distillate rebuild would unwind the tightness leg; a further draw would reinforce it.

**D. EIA Weekly Natural Gas Storage Report, week ended Oct 23 — released Thu Oct 29 [FACT]**
- Working gas **rose 80 Bcf to 3,724 Bcf**, vs a WSJ-survey expectation of ~70 Bcf and a five-year-average weekly build of 77 Bcf. Stocks were 147 Bcf below year-ago but 38 Bcf above the five-year average (3,686 Bcf). South Central injected 43 Bcf to 1,168 Bcf, still ~2.3% below its five-year average; salt storage ~11.6% below seasonal average. Sources: https://www.forexfactory.com/news/1433935-eia-us-gas-inventories-up-by-80-billion/amp ; https://www.fxempire.com/forecasts/article/natural-gas-price-forecast-natural-gas-sees-injection-1641568
- **FACT (price reaction):** Natural gas traded ~$2.96/MMBtu on Oct 30, down ~2.4% on the day, after breaking below $3.04–3.05 support — consistent with the bearish (larger-than-expected build) print plus warmer-than-usual early-November weather forecasts cited by WSJ/FXEmpire. Sources: https://tradersunion.com/news/commodities/show/4034194-natural-gas-slides-below-3-00-as-eia-inventory-surprise-deepens-bearish-pressure/ ; https://www.wsj.com/finance/commodities-futures/european-gas-prices-retreat-after-topping-100-euros-a-megawatt-hour-b9a8807b
- **INFERENCE:** Gas is pricing adequate pre-winter storage and soft early-heating demand — the opposite directional read from crude/distillates. The South Central salt deficit is the one tight pocket to watch into winter.
- **What would change this read:** A cold shift in NOAA guidance, a below-average build in the Nov 5 report, or a QatarEnergy LNG-delivery disruption (see below) tightening Atlantic LNG.

**E. QatarEnergy LNG delivery restrictions extended — reported Oct 29 [FACT as reported, detail UNVERIFIED]**
- QatarEnergy extended restrictions on contractual LNG deliveries until end-December, increasing uncertainty for European and Asian buyers (reported in TradersUnion's Oct 29 pre-report note). Source: https://tradersunion.com/news/commodities/show/4013686-natural-gas-faces-renewed-breakdown-risk-as-3-04-support-comes-under-pressure/
- **UNVERIFIED:** The volume, counterparties, and cause of the restriction were not specified in the sourced reporting — do not quantify it.
- **What would change this read:** A QatarEnergy statement or a European/Asian spot-LNG price spike confirming a physical shortfall.

**F. October WASDE — NOT fresh today, but still the operative grain baseline [FACT]**
- The October WASDE/Crop Production report was released Fri Oct 9 (not this week). No new WASDE was released Oct 30. Next WASDE date: UNVERIFIED from sourced reporting — do not assume a date.
- October WASDE levels: US corn yield 181.1–181.2 bu/ac (sources differ by 0.1 on rounding), production 16.034bn bu (+234m vs September), 2026/27 ending stocks 1.849bn bu (+282m); soybeans record yield 53.1 bu/ac, production 4.562bn bu, ending stocks 315m bu, price held at $12.00/bu; wheat production 1.534bn bu (smallest since 1970), ending stocks 740m bu (+23m), price cut to $6.30/bu. Corn price forecast cut to $4.70/bu. Sources: https://www.iowafarmbureau.com/Article/October-WASDE-Boosts-US-Corn-and-Soybean-Production-Estimates ; https://www.dtnpf.com/agriculture/web/ag/news/article/2026/10/09/october-wasdes-shocking-rise-corn
- **FACT (Oct 30 grain closes):** Dec corn $4.47¾ (four-month low close, week −8¼¢); Jan soybeans $12.34¼ (week −34¼¢); Dec SRW wheat $6.03½ (week −21½¢); Dec HRW wheat $6.44¼ (week −20¼¢). Morning quotes had corn/soybeans lower and wheat higher; the closes reversed wheat. Source: https://www.profarmer.com/news/after-bell/after-bell-corn-closes-multi-month-lows
- **FACT (demand datapoints, Oct 30):** USDA weekly export sales (reported Oct 29): wheat 849,800 MT — a marketing-year high, well above ~350k MT expected; corn 1.3m MT; soybeans 2.58m MT. USDA also announced flash sales of 165.2k MT and 132k MT of soybeans to unknown buyers. YTD wheat commitments still off 29% YoY vs USDA's −17% forecast; corn exports down 34% YoY vs USDA's −4% forecast. Sources: https://www.admis.com/ag-market-view-for-oct-30-2026/ ; https://www.tradingview.com/news/DJN_DN20261029014610:0-wheat-ticks-up-after-export-sales-surprise-daily-grain-highlights/
- **INFERENCE:** Grain futures are still digesting the bearish October WASDE supply build — corn at multi-month lows despite a marketing-year-high wheat sale shows demand headlines are not yet reversing the supply overhang.
- **What would change this read:** The November WASDE (yield/harvest-progress confirmation), a sustained export-sales beat, or confirmed China SRW-wheat buying beyond Thursday's reported inquiry.

### What futures curves appear to be pricing

**Crude — steep backwardation = prompt tightness + risk premium, not a demand boom [FACT on curve shape, INFERENCE on interpretation]**
- **FACT (Fri Oct 30, OPIS via Morningstar):** Dec ICE Brent +$2.76 at $117.61/bbl, Jan Brent +$2.93 at $113.73/bbl (Dec–Jan spread ≈ $3.88 backwardation); Dec WTI +$2.16 at $104.16/bbl, Jan WTI +$2.26 at $102.40/bbl (spread ≈ $1.76 backwardation). Nov ULSD +11.44¢ at $4.8504/gal; Dec ULSD +11.15¢ at $4.699/gal. Source: https://www.morningstar.com/news/dow-jones/202610308885/nymex-overview-oil-refined-products-climb-on-middle-east-supply-concerns-opis
- **FACT (curve context):** Reuters (Oct 30 poll of 32 analysts) reports Brent and WTI "remain higher for contracts for prompt delivery than for crude for delivery later, a price structure known as backwardation that suggests a tight market for oil in the nearer term"; the poll raised the 2026 Brent average view to $92.88 (from $89.05) and WTI to $86.60 (from $83.90), with a forecast Q4 2026 deficit of ~2.7m bpd. A separate curve summary puts Dec 2026 WTI ~$101.93 declining toward the low-$60s by the early 2030s, and Dec 2026 Brent ~$114.34 with Jan 2027 ~$110.68, sliding toward ~$61 by early 2038 — Brent–WTI nearby premium ~$12–13/bbl. Sources: https://www.reuters.com/business/energy/brent-2026-view-tops-90-first-time-since-may-mideast-stability-remains-elusive-2026-10-30/ ; https://commodity-board.com/wti-backwardation-steepens-as-geopolitical-risk-lifts-brent-above-110
- **FACT (month):** Brent headed for ~+13% in October, WTI ~+15% — its fourth consecutive monthly gain. Source: https://investorsking.com/2026/10/30/oil-prices-rise-above-116-as-strait-of-hormuz-attack-raises-supply-concerns/
- **INFERENCE:** The curve is pricing (a) tight prompt physical availability, (b) a large seaborne/geopolitical risk premium concentrated in Brent (the $12–13 Brent–WTI spread is the seaborne-risk gauge), and (c) eventual normalisation — deferred prices in the $60s imply the market does not price today's $104–118 prompt levels as permanent. Diesel/ULSD strength alongside crude supports the distillate-tightness leg from the EIA data.
- **UNVERIFIED:** A full dated curve table (every monthly contract) was not retrieved from a primary exchange source in this run; the curve shape above rests on the two front contracts plus the cited curve summaries, not a complete strip.
- **What would change this read:** A Hormuz de-escalation or OPEC+ supply surprise would compress prompt backwardation and the Brent–WTI spread first; a confirmed supply cut would steepen front-month backwardation further.

**Natural gas — pricing soft prompt demand, not winter scarcity [INFERENCE from FACT prices above]**
- Prompt gas below $3.00 after a larger-than-expected build, with storage 38 Bcf above the five-year average at heating-season start, is consistent with a market pricing adequate supply and warm early-November weather. The South Central salt deficit is the offsetting tightness signal.
- **UNVERIFIED:** The full Henry Hub forward curve shape was not retrieved in this run — do not characterise winter-strip backwardation/contango from these sources alone.
- **What would change this read:** The Nov 5 storage report and any cold-shift in weather guidance.

**Grains — front-month levels only; curve shape UNVERIFIED**
- Front-month levels (Oct 30 closes above) show corn under pressure and wheat stabilising near $6.00–6.45 after the WASDE supply build. No verified deferred-contract curve was retrieved in this run, so no contango/backwardation claim is made for grains.
- **What would change this read:** The November WASDE and deferred-contract quotes from a primary exchange source.

### Forward catalyst calendar (verified dates only)
| Date | Event | Status |
|---|---|---|
| Sun Nov 1 | OPEC+ seven-producer meeting (Saudi Arabia, Russia, Iraq, Kuwait, Algeria, Kazakhstan, Oman) — December targets expected unchanged per three Reuters sources; no final decision made as of Oct 27–29 reporting; ~2m bpd of cuts remain through end-2026; 2027 baselines still pending capacity review | FACT (expectation, not decision) — sources: https://coinpaper.com/38058/opec-expected-to-hold-december-oil-output-steady-despite-brent-trading-above-110 ; https://www.oilandgas360.com/opec-oil-producers-set-to-keep-output-targets-steady-at-sunday-meeting-sources-say/ |
| Wed Nov 4 | Next EIA Weekly Petroleum Status Report | FACT — source: https://el7.ai/en/news/2026-10-29-us-natural-gas-storage-build-exceeds-expectations-pressuring-futures |
| Thu Nov 5 | Next EIA Weekly Natural Gas Storage Report | FACT — source: https://www.fxempire.com/forecasts/article/natural-gas-price-forecast-natural-gas-sees-injection-1641568 |
| Tue Nov 10 | EIA Short-Term Energy Outlook | FACT — source: https://el7.ai/en/news/2026-10-29-us-natural-gas-storage-build-exceeds-expectations-pressuring-futures |
| Sun Nov 29 | Full OPEC+ ministerial meeting (2027 policy) | FACT — source: https://www.tokenpost.com/news/investing/42155 |

### Government-data note
No shutdown/blackout framing applies: the Oct 28 EIA petroleum report and Oct 29 EIA gas report were released on schedule, and the Oct 9 WASDE was released on schedule, consistent with the standing on-schedule rule. No primary-source contradiction was found in this run.

### Desk bottom line
1. **Hormuz attacks on Oct 29–30 are the freshest, highest-impact catalyst** — crude spiked (Brent ~$117.61, WTI ~$104.16 on Oct 30) on risk premium, but Saudi-facility damage remains UNVERIFIED; treat as premium, not confirmed physical loss.
2. **Crude curve is steeply backwardated** (Dec–Jan Brent ~$3.88, WTI ~$1.76) with a ~$12–13 Brent–WTI premium — pricing prompt tightness and seaborne risk, with normalisation deferred to the $60s long-dated.
3. **EIA splits the energy complex:** crude/distillate draws (tight) vs gasoline build and a larger-than-expected gas build (loose) — gas below $3.00 is the counterweight to crude strength.
4. **OPEC+ Sun Nov 1 is the next decision point** — expected hold for December; the real signal is any 2027-baseline guidance.
5. **Grains remain in WASDE-supply-digestion mode** — corn at a four-month low close despite a marketing-year-high wheat export sale; next real grain catalyst is the November WASDE (date UNVERIFIED).

## 6. Box/Parity Observer

**Bottom line: one new index-methodology item to watch, no new parity-violation evidence for SPY/QQQ.**

- **NEW — S&P Dow Jones style-index methodology overhaul, effective before the open Mon Dec 21, 2026** [FACT, as of search 2026-10-30 ~13:30 PT]: S&P Dow Jones Indices will drop 12-month price momentum from growth rankings and rebuild value rankings around intangibles-adjusted book-to-price, trailing + forward earnings-to-price (averaged), sales-to-price, and free cash flow-to-price (excluding real estate, banks, insurers, mortgage REITs and certain financials from the cash-flow factor). Pro-forma files from Fri Dec 4, 2026. Consultation ran Sep 4–25, 2026; announcement reported Oct 23, 2026. Scope covers the S&P U.S. Style indices (S&P 500, Composite 1500, MidCap 400, SmallCap 600, S&P 1000, S&P 900 growth/value and Pure Style series); Bloomberg Intelligence's James Seyffart is cited estimating ≥$375B in passive funds tied to the affected gauges. Sources: https://www.tradingview.com/news/benzinga:b353d12e7094b:0-s-p-changes-the-rules-here-s-new-value-vs-growth/ ; https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing
- **Parity relevance — limited, not a headline-index change** [INFERENCE from the scope above]: this revises growth/value *style* classification, not the headline S&P 500 membership/weighting that SPY tracks, so it does not by itself alter SPY put-call/box parity math. Watch only for constituent-flow effects around the Dec 4 pro-forma and Dec 21 reconstitution dates, not for a parity break.
- **Nasdaq-100 "Fast Entry" — not new** [FACT]: the proposal to admit qualifying large new listings after 15 trading days (top-40 market-cap test, ≥5 trading days' notice, no immediate deletion) dates to Feb 2026; the Oct 22, 2026 item found was a re-report, not a new adoption. No final rule found. Source: https://ts2.tech/en/nasdaqs-fast-entry-plan-could-reshuffle-the-nasdaq-100-faster-and-qqq-holders-are-watching/
- **Published parity-violation analysis — none new found** [FACT, search 2026-10-30]: searches for Oct 2026 box-spread / put-call parity violations returned only educational explainers (e.g., SpotGamma box-spread primer, OptionScout parity explainer), no new empirical violation study for SPY/QQQ/SPX. No measured box or put-call deviation is reported here — any such figure would be UNVERIFIED without a live options-chain check, which is outside this desk's light-touch brief.
- **Standing parity check** [FACT — deterministic math, not a market observation]: a fairly priced box pays exactly the strike width at expiry regardless of the underlying, so Box = (K2 − K1)·e^(−rT); a deviation beyond transaction costs is the arbitrage signal, and the math outranks any model output. No deviation is claimed today.

## 7. Bonds & Rates desk

**Source:** repo module `hedge_desk.rates_desk.rates_environment()` (mode `REAL_FRED_RATES`), run 2026-10-30 13:30 PT from `~/workspace/github/hedge-desk`. Data source reported by the module: `fred-public-csv-http-200`. Module run succeeded; no fallback data used.

### Rates table (FACT — FRED daily series via the module)

| Series | Level | As-of |
|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-29 |
| Treasury 2Y (DGS2) | 4.61% | 2026-10-29 |
| Treasury 10Y (DGS10) | 4.98% | 2026-10-29 |
| 2s10s spread (10Y − 2Y) | +37 bp | 2026-10-29 |
| SOFR | 3.94% | 2026-10-29 |
| EFFR | 3.88% | 2026-10-29 |
| OBFR | 3.88% | 2026-10-29 |

All series are dated 2026-10-29 — the latest FRED daily observation available at run time, i.e. yesterday's close, not stale. (FRED daily series post with a one-day lag; the module's own `as_of` is 2026-10-30.)

### Slope read
- **Curve shape: UPWARD_SLOPING** (FACT, module output; curve_slope 0.04625 on the module's internal scale, spread +37 bp).
- **Direction of change — flattening, modestly:** the 2s10s spread was +41 bp at the start of the module's 60-day window (2026-08-31: 10Y 4.75% − 2Y 4.34%) and is +37 bp now — 4 bp flatter over the window. Day-over-day it narrowed 1 bp (2026-10-28: 5.05% − 4.67% = +38 bp → 2026-10-29: +37 bp). Both legs fell on 2026-10-29 (2Y −6 bp, 10Y −7 bp from 2026-10-28) (FACT, module history series).
- **Fed funds:** effective rate 3.88%, with the module reporting a +0.25 pp change over its 60-day window (FACT, module output). 3.88% sits inside the 3.75–4.00% target range the FOMC held at its October 28 decision (FACT, prior verified run context).
- **Level context:** the 10Y peaked at 5.31% in this window (2026-10-05) and has since eased to 4.98%; the 2Y peaked at 4.92% (2026-09-28) and has eased to 4.61% (FACT, module history). Both legs are off their window highs — a rally, not a selloff, into month-end.

### Funding-stress read
- **SOFR − EFFR = +6 bp** (3.94% − 3.88%) (FACT, computed from module output). OBFR equals EFFR at 3.88%. A 6 bp SOFR premium is a normal, unstressed overnight funding print — no funding-stress signal (INFERENCE from the 6 bp spread; stress would show as a materially wider SOFR–EFFR gap).

### Premium-pricing implication
- **Directional read (INFERENCE):** with the 10Y at 4.98% — near 5% and well above the fed funds rate — discount rates remain elevated, which pressures growth multiples and keeps the margin-of-safety bar high for long-duration names (NVDA, TSLA on the watchlist). The curve is positively sloped, not inverted, so there is no recession-inversion signal in the 2s10s to offset that read. The modest flattening over the window (41 → 37 bp) is too small to change the stance.
- **For premium selling specifically (INFERENCE):** elevated long rates support the rho channel on calls only marginally; the dominant channel is valuation pressure on growth underlyings, which argues for demanding wider premium (more margin of safety) rather than chasing tight premium on richly valued names. No rate-driven reason to favor risk-seeking structures.
- **What would change the read:** a 10Y break back above 5.25% (its late-September window high zone) would strengthen the discount-rate pressure case; a 2s10s inversion (spread < 0) would flip the curve read to recession-warning; a SOFR–EFFR spread widening beyond ~15–20 bp would flag funding stress. None of these conditions holds today.

**Desk status: COMPLETE.** No series missing, no UNVERIFIED items. Note on labeling: all 2Y figures above are FRED DGS2 (the genuine 2Y series), not Yahoo ^FVX (which is the 5Y).

## Synthesis — the 5 most decision-relevant items

1. **Hormuz tanker attacks (Oct 29–30) repriced oil on risk premium, not confirmed supply loss.** Brent ~$117.61, WTI ~$104.16 on Oct 30, curve steeply backwardated with a ~$12–13 Brent–WTI seaborne-risk premium; Saudi-facility damage is UNVERIFIED and no Hormuz closure is confirmed. OPEC+ meets Sun Nov 1 (December targets expected unchanged; 2027 baselines are the real signal). A quiet weekend supports premium fade; a confirmed closure or facility damage upgrades this to a physical-supply event.
2. **AAPL earnings Mon Nov 2 AMC is the window's only watchlist binary — avoid premium into it.** ~4.3% priced (Nov 4 straddle) with front IV 43.1% vs 13.5% trailing realized (3.2×); the fiscal-Q4 history leans negative (median −0.9%, up 6/17). The print's swing factor is the December-quarter guide and the memory-cost/margin read, not the September quarter.
3. **Oct 30 was a hard growth selloff, but front IV ex-AAPL is fairly priced — no vol edge either way.** Indicative post-close marks: QQQ −3.5%, NVDA −4.2%, SPY −2.1%. Front IV sits at or below trailing realized for QQQ/MSFT/NVDA/TSLA. Watch: QQQ (28.8%) and NVDA (28.5%) are one hot day from flipping WINDOW-CONTINGENT, which would void their realized baselines; Nov 3–4 expiries carry event premium (INFERENCE: midterms).
4. **Rates: 10Y 4.98%, 2s10s +37 bp and flattening modestly, SOFR–EFFR +6 bp (no funding stress).** Discount-rate pressure on long-duration growth names persists; no inversion signal, no stress signal. The 10Y is off its 5.31% window high — a rally into month-end, not a selloff.
5. **Dividends: only MSFT's Nov 19 ex-date ($0.98, 24th consecutive annual increase) is actionable in the next 4 weeks.** AAPL's declaration watch resolves at its Nov 2 earnings; NVDA's next declaration comes with its Nov 17 print (early-December ex-date, outside window). Quant lab: quiet sweep — two WATCH adds (#182 honest-negative sentiment-vol paper, #183 tail-forecast evaluation correction), zero TEST/INTEGRATE; parity desk: S&P style-index overhaul effective Dec 21 is a style-classification change, not a SPY parity event.
