# Hedge-Desk Daily Research — Fri 2026-11-06

**Run:** 13:30 PT, seven desks fanned out in parallel. Research and input only — no git, no PRs, no code changes.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety. Paper-only.
**Labels:** FACT / INFERENCE / SPECULATION / UNVERIFIED throughout. No Risk of Ruin computed or estimated.

## Decision-relevant items (top 5)

1. **NVDA earnings Tue Nov 17 after close is the only watchlist event in the next 2 weeks.** Implied earnings-day move ±6.2% (desk calc, cross-checked vs ApexVol ±6.1%); 10-yr avg realized move ±8.4%, 2-yr avg ±5.7%. Options price a bigger-than-recent but smaller-than-historical event. Stock is ~23% below its $243.37 high. [Earnings desk]
2. **NVDA 11-20 expiry IV 0.694 vs 0.572 at 11-13 prices the earnings event — premium into this binary event = avoid** (standing rule). NVDA and TSLA front IVs (0.44 / 0.42) run ~2–3× index levels. [Premium desk]
3. **AAPL and MSFT IV-vs-realized verdicts are WINDOW-CONTINGENT** — a single day drives 55.5% (AAPL) and 49.9% (MSFT) of 20-day realized variance. No clean verdict on either until the jump ages out. [Premium desk]
4. **Oil fell ~13% on the week (Brent $98.32, WTI $90.83 Fri settlement) as midterms repriced Iran-war premium lower; Hormuz tanker attacks continued Nov 5–6, putting a floor under the fall. Distillates at a 23-year low (99.3m bbl, 13% below 5-yr avg) — the tightest physical signal — while Brent swaps flipped to contango.** WASDE + STEO both Tue Nov 10. [Futures desk]
5. **Rates: 10Y 4.90%, 2Y 4.58% (FRED, as of Nov 4), 2s10s +32 bp, flattening ~9 bp over 60 days; SOFR−EFFR +4 bp, no funding stress.** 10Y down from Oct 5 peak of 5.31% — discount-rate headwind easing, not gone. [Bonds & Rates desk]

---

## 1. Earnings Event desk

**Window:** 2026-11-06 → 2026-11-20. As-of: Yahoo live pull 2026-11-06 post-close.

| Name | Date / timing | Implied move | Historical avg move |
|---|---|---|---|
| **NVDA** — Q3 FY2027 (qtr ended Oct 25) | **Tue Nov 17, 2026, after close**; call 5:00 PM ET / 2:00 PM PT; first reaction session Wed Nov 18 | **±6.2% earnings-day** (desk calc); raw Nov-20 ATM straddle ±11.2% | **±8.4%** 10-yr avg peak intraday (n=40); median ±6.6%, 95th pct ±20.1%; 2-yr avg ±5.7% |
| AAPL | None in window — reported Mon Nov 2, after close | n/a | n/a |
| MSFT | None in window — reported Wed Oct 28, after close | n/a | n/a |
| TSLA | None in window — reported Wed Oct 21, after close | n/a | n/a |
| SPY / QQQ | No earnings (ETFs) | n/a | n/a |

**NVDA date verification (FACT, triple-sourced):** Yahoo `earningsTimestamp` Nov 17, 2026 21:00 UTC, `isEarningsDateEstimate: false`; Nasdaq earnings calendar API lists NVDA Tue Nov 17 after-hours, fiscal quarter ending Oct/2026, consensus EPS **$2.49** (13 estimates), last year's same-quarter EPS $1.24; multiple outlets citing NVIDIA's own Oct 28 notice. Conflicting aggregator dates (TipRanks Nov 25, MarketBeat Nov 18, one stale Webull page Nov 19) are superseded. A direct fetch of NVIDIA's IR press-release page returned only 241 bytes (blocked/redirect) — the date does not rest on that fetch.

**Implied move — method (INFERENCE):** NVDA closed $186.64 Nov 6 (+2.78%; 52-wk $164.27–$243.37 — Yahoo v8 chart, FACT). First expiry after the print is Fri Nov 20. ATM ($185) straddle mid-price: Nov 13 expiry $12.93 = 6.93% → implied ordinary daily σ ≈ 3.87%; Nov 20 expiry $20.88 = 11.18% of spot — raw straddle covering the event plus 3 post-earnings sessions, NOT the earnings-day move. Variance decomposition (straddle ≈ 0.8σ): earnings-day σ ≈ 7.8% → expected absolute earnings-day move ≈ **±6.2%**. Cross-check: ApexVol independently reports ±6.1%. Flagged discrepancy: EarningsWatcher reports "±10.5% implied move" — consistent with an unadjusted straddle-style reading, not an earnings-day-only move; do not use 10.5% as the earnings-day figure.

**Historical moves (FACT, third-party):** EarningsWatcher, as of Nov 6 — 10-yr avg peak ±8.4% (40 reports), median ±6.6%, 95th pct ±20.1%; 2-yr avg ±5.7%. ApexVol: last 12 reports averaged 5.6% close-to-close; actual exceeded priced move in 3 of 12. Last report (Aug 26, 2026): options priced ±5.9%, stock closed **+8.7%** (peak +9.9%). May 20, 2026 −1.8% vs ±5.9% priced; Feb 25, 2026 −5.5% vs ±6.1% priced. Peak-intraday vs close-to-close bases differ — do not mix them.

**Guidance already on the table (FACT, company, Aug 26 call):** Q3 FY2027 revenue $108.0B ±2%, gross margin 74.0% ±50bp, no Data Center compute revenue from China assumed. **No earnings release exists yet to read** — the release lands Nov 17; per desk standard it must be read directly then, not via summaries.

**Value-lens read (INFERENCE):** Implied (±6.2%) sits below the 10-yr average realized move (±8.4%) but above the cooler 2-yr average (±5.7%) — options price a bigger-than-recent but smaller-than-historical event. The stock is down ~23% from its $243.37 high and ~15% below its 50-day average ($220.64), so the print lands into an already-de-rated tape; a guidance cut on Q4 margins (CFO flagged memory-cost pressure, margins troughing 71–72% in Q4) is the swing factor, not the Q3 print alone.

**Already reported (FACT, third-party calendars; next dates unconfirmed estimates, outside window):**
- AAPL — Mon Nov 2 after close: EPS $2.10 vs $1.99 consensus, revenue $114.48B vs $113.40B (MarketBeat). First reaction Tue Nov 3: −1.9% (SimianX). Next report est. ~Jan 28, 2027 (unconfirmed).
- MSFT — Wed Oct 28 after close: EPS $4.89 vs $4.72 consensus, revenue $92.28B (MarketBeat/CapitalSnitch). Next est. Jan 26, 2027 (TipRanks, not confirmed).
- TSLA — Wed Oct 21 after close: EPS $0.48 vs $0.455 consensus, revenue $28.05B vs $28.06B; stock −3.1% vs ±6.3% priced (EarningsWatcher/MarketBeat). Next est. ~Jan 27, 2027 (not confirmed; Zacks lists Jan 27, 2027 as estimated).

**What would change the verdict:** NVIDIA reschedules or pre-announces; options repricing into Nov 17 (re-pull the Nov 20 straddle nearer the print); the Nov 17 release itself (revenue vs $108B guide, Q4 margin guide, China/Data Center commentary) — read the release + 8-K directly on arrival.

**Sources:** Nasdaq earnings calendar API (api.nasdaq.com); Yahoo Finance v7 options + v8 chart (live pull 2026-11-06, cookie+crumb); earnings-watcher.com; apexvol.com/earnings/nvda; simianx.ai Magnificent 7 tracker (updated Nov 3, 2026); marketbeat.com; tipranks.com; zacks.com.

---

## 2. Dividend Opportunity desk

**Window:** next 4 weeks, through 2026-12-04. As-of: 2026-11-06 close. Sources: Nasdaq dividends calendar API (swept every business day 2026-11-06 → 2026-12-04) + Nasdaq per-symbol dividend history + Yahoo Finance v8 chart (prices are 2026-11-06 closes). All three sources agree on the two in-window events.

| Symbol | Ex-date | Amount | Pay date | Annualized | Yield* | Change vs prior qtr |
|---|---|---|---|---|---|---|
| AAPL | **Thu 2026-11-12** | $0.27 | 2026-11-16 | $1.08 | 0.31% | None — flat at $0.27 (FACT, Nasdaq + Yahoo) |
| MSFT | **Thu 2026-11-19** | $0.98 | 2026-12-10 | $3.92 | 0.74% | **INCREASE — first payment at new rate**; $0.91 → $0.98 (+7.7%), announced 2026-09-15 (FACT, Nasdaq + Yahoo + issuer declaration) |

\*Yields computed by the desk from declared annualized rate ÷ Yahoo 2026-11-06 close (AAPL $342.37, MSFT $530.61). Nasdaq's own yield fields agree for AAPL (0.31%) but are **stale for MSFT** (still shows 0.68% / $3.64 annual from the pre-raise quarter, even though its own history rows list the $0.98 declaration) — use the computed 0.74%.

**No ex-date in window:**
- **SPY** (FACT): last ex-date 2026-09-18 ($1.889, Yahoo). Quarterly pattern (third Friday of Mar/Jun/Sep/Dec) puts the next ex-date ~2026-12-18 — outside the window. TTM yield ~1.03% (TTM $7.583 ÷ $735.36, computed from Yahoo history).
- **QQQ** (FACT): last ex-date 2026-09-21 ($0.75143, Nasdaq + Yahoo). Next ~2026-12-21, outside window. Yield 0.46% (Nasdaq $3.00572 annualized ÷ $656.10 close).
- **NVDA** (FACT): last ex-date 2026-09-10 ($0.25). No December dividend declared yet — declaration expected late Nov on prior pattern (Aug 26 declaration → Sep 10 ex-date). Yield 0.54% ($1.00 ÷ $186.64). Last increase was Jun 2026 ($0.01 → $0.25).
- **TSLA** (FACT): pays no dividend — zero dividend events in Yahoo 5y history; nothing to capture.

**Increases / cuts / specials:** No cuts, no specials anywhere on the watchlist (FACT — nothing in Nasdaq calendar sweep or Yahoo histories). One increase in effect: MSFT's Sep 15, 2026 raise to $0.98/qtr. Per the desk standard (~/workspace/hedge-desk-research/dividend-count-standard.md), MSFT stands at **24 consecutive annual increases** (incl. the Sep 2026 raise; initiated 2003; count increments on announcement date). No 2026 raise remains to be announced; next expected Sep 2027. AAPL: last raise May 2026 ($0.26 → $0.27, +3.8%, declared 2026-04-30); the Nov 2, 2026 declaration held $0.27 flat. Consecutive-year streak count for AAPL: **UNVERIFIED** — not in the desk standard and not verified against issuer history this run; do not carry a number forward. NVDA: no new declaration in window; June 2026's 25x raise ($0.01 → $0.25) remains the latest increase.

**Value-lens read (INFERENCE):** Neither in-window event is a mispricing signal: both are routine quarterly payments at well-covered payout ratios (AAPL ~38% per Nasdaq; MSFT ~28%). The only decision-relevant item is mechanical — **MSFT goes ex-dividend Nov 19 at the new $0.98 rate**, so any premium-selling or assignment analysis spanning that date should use $0.98, not the stale $0.91 (and not Nasdaq's stale $3.64 annualized figure). AAPL's Nov 12 ex-date is a $0.27 non-event. No dividend-capture opportunity of substance: sub-1% yields across the board.

**What would change this:** NVDA declares its December dividend in late Nov (expected ~$0.25, flat) — would add a ~Dec 3–4 ex-date at the window's edge; watch the declaration, not the calendar pattern. SPY/QQQ December declarations (mid-Dec) fall outside this window but land in the next run's window.

---

## 3. Overnight Premium desk (IV)

**Inputs & freshness:** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-05-iv-inputs.json`, `as_of` **2026-11-05T14:54:05-07:00** — **22.5h old at pull time, inside the 26h guard → FRESH per guard, but STALE (yesterday's post-close) for levels.** All file-sourced levels below carry that label. Live Yahoo pull (cookie+crumb handshake, UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`), **2026-11-06 13:27 PT / 16:27 ET, post-close** — FACT. Underlyings: SPY 735.36, QQQ 656.10, AAPL 342.37, MSFT 530.61, NVDA 186.64, TSLA 358.22 (v8 chart regularMarketPrice).

**Dead-expiry discard (FACT, fail-closed):** 2026-11-06 expiry contracts expired 16:00 ET; their Yahoo ATM IVs are solver residuals (e.g. SPY call 0.067 vs put 0.012; AAPL 0.013 vs 0.025) — **discarded, not reported as IV**, same logic as the file's SPY/QQQ nulls yesterday.

### Per-symbol IV snapshot (ATM IV = mean of ATM call/put Yahoo impliedVolatility)

| Symbol | Live IV 11-09 (1 trad. day) | Live IV 11-13 | Live IV 11-20 | STALE file IV 11-06 exp. (as_of 11-05 14:54 PT) | Realized 20d (file, 10-08–11-04) | Max 1-day var share | Window-contingent? |
|---|---|---|---|---|---|---|---|
| SPY | 0.157 | 0.220 | 0.215 | null (failover unavailable) | 0.131 | 0.258 | No |
| QQQ | 0.231 | 0.330 | 0.328 | null (failover unavailable) | 0.236 | 0.290 | No |
| AAPL | 0.201 | 0.276 | 0.274 | 0.321 | 0.259 | **0.555** | **YES** |
| MSFT | 0.235 | 0.312 | 0.323 | 0.372 | 0.338 | **0.499** | **YES** |
| NVDA | 0.436 | 0.572 | 0.694 | 0.701 | 0.337 | 0.220 | No |
| TSLA | 0.424 | 0.559 | 0.547 | 0.661 | 0.395 | 0.231 | No |

Term-structure shape (INFERENCE from live pulls): front end compressed at 11-09 (1 trading day), rising to 11-13, flat to 11-20 — except NVDA, which keeps climbing into 11-20. Call/put ATM IVs agree within ~1–3 pts at every live expiry — no parity-violation signal at ATM (limited check only; not a full synthetic-forward parity audit).

### IV-vs-realized verdicts (live 11-09 IV vs trailing 20d realized)
- **SPY — IV modestly above realized** (0.157 vs 0.131, +2.6 pts). Clean verdict (not window-contingent). FACT levels; verdict INFERENCE.
- **QQQ — IV ≈ realized** (0.231 vs 0.236, −0.5 pts). Clean verdict.
- **AAPL — WINDOW-CONTINGENT, no clean verdict.** Nominally IV below realized (0.201 vs 0.259), but a single day drives 55.5% of the 20-day variance — the realized leg is dominated by one jump, so the comparison is not meaningful.
- **MSFT — WINDOW-CONTINGENT, no clean verdict.** Nominally IV well below realized (0.235 vs 0.338), but a single day drives 49.9% of the variance — same disqualification.
- **NVDA — IV elevated vs realized** (0.436 vs 0.337, +10 pts). Clean verdict. The 11-20 expiry IV of 0.694 vs 0.572 at 11-13 is consistent with the market pricing the 11-17 earnings event into that expiry (INFERENCE).
- **TSLA — IV modestly above realized** (0.424 vs 0.395, +2.9 pts). Clean verdict.

### Flags
- **Elevated IV (absolute): NVDA and TSLA** — front IVs 0.44 / 0.42 and 11-13 IVs 0.57 / 0.56, roughly 2–3× index levels. FACT from live pull. Whether that is "elevated" vs their own history is **UNVERIFIED — IV rank / percentile cannot be computed; no free IV-history source available. Never guessed.**
- **Earnings in window — NVDA 2026-11-17** (FACT per iv-inputs file; confirmed by Earnings desk). It sits inside the 11-20 expiry, which is why that expiry's IV (0.694) jumps. **Premium into this binary event = avoid** (standing rule). No other watchlist name shows an earnings date in the file (all null) — confirmed by Earnings desk.
- **Stale-file note:** yesterday's 1-DTE IVs (NVDA 0.701, TSLA 0.661, AAPL 0.321, MSFT 0.372) were live at pull time 11-05 but are now expired-tenor marks; the lower live 11-09 IVs are a tenor roll, not evidence of a vol collapse (INFERENCE).
- **SPY/QQQ gap closed:** yesterday's file had null ATM IV for both (expired-expiry failover); today's live pull supplies tradeable 11-09 levels (0.157 / 0.231).

**What would change each verdict:** AAPL/MSFT — a fresh realized window in which the single-day jump share falls below 30% (jump ages out or is swamped by new variance). SPY/QQQ/TSLA — Monday's open quotes and a realized window extended through 11-05/11-06 closes; a >5-pt move in front IV would flip the "modestly above / at parity" reads. NVDA — confirmation (or change) of the 11-17 earnings date; post-earnings, the 11-20 IV should collapse toward the 11-13 level if the event premium was the driver. IV rank for all names: any verified IV-history source (currently UNVERIFIED).

**Desk status: complete, no failures.** Live Yahoo pull succeeded for all six names on all three expiries; no retry needed.

---

## 4. Open Quant/AI Model Lab

**Coverage (FACT):** arXiv q-fin API leg (https) covered submissions Oct 29–Nov 5; date-filtered [20261105 TO 20261106] returned exactly 3 items, all read — no Nov 6 submissions indexed at sweep time. GitHub leg skipped per the run brief's ban on GitHub operations — no new-repo discovery, no repo re-checks, no contents/license verification (leg gap, same as Nov 1–4). All 19 candidates scored with the repo scorer (`hedge_desk.research_intelligence.assess_source`, run not hand-computed). All claims below are abstract-level, source-reported and UNVERIFIED unless marked FACT.

**New candidates — WATCH (7):**

| # | Candidate | Score | Reason |
|---|---|---|---|
| 214 | Neural Realized Measures — forecast-supervised intraday aggregation for vol forecasting | 51 | arXiv:2611.07287. Uniform weights nest the raw realized measure (FACT — abstract); QLIKE improves in all 54 paired OOS comparisons — but on six cryptos only, equities transfer UNVERIFIED; no code link. Sandbox: reimplement on SPY 5-min vs HAR-RV. |
| 215 | RISVIX — rough instantaneous squared VIX, term structure + option pricing | 51 | arXiv:2611.07120. OOS VIX-option MSE −13.06% / MAE −6.33% vs Markovian benchmark, Jan 2018–Jun 2025 (source-reported); no code link. |
| 216 | OLIVIA — point-in-time protocol for LLM news readings | 57 | arXiv:2611.03985. **Run's best, 4 pts under TEST.** Fine-tuned model IC 0.055/0.065 validation → 0.020 (t=1.7) blinded Jan–Jul 2026; commercial models' signal lives only in the overnight move. Directly relevant to #85 (availability contract) + #34 frozen-referee lane; no code link. |
| 217 | Honest Small Decision Models for Finance | 48 | arXiv:2611.03755. Every rung 0.8B–32B lands at the prior baseline (acc. 0.37–0.38, no conditional edge); ECE 0.026 at 2B. Honest negative for the validation lane; no code link. |
| 218 | Fast Regime Switches pricing (Cotton) | 45 | arXiv:2611.00466. Abstract states "implementation is public" but the abs page shows NO author code link (FACT, read at source) → reproducibility not established. Band floor. |
| 219 | Lorig — Intro to Financial Derivatives lecture notes | 57 | arXiv:2611.01355. Open notes + Python code; LaTeX source at github.com/mattlorig/intro-financial-derivatives (FACT — stated in abstract; repo/license NOT verified, banned leg). Reference resource for parity/Greeks discipline, not an adoption candidate. |
| 220 | Repair Risk in Crypto Option Surfaces | 45 | arXiv:2611.00958. Multiple admissible no-arb repairs → Greeks dispersion (~20× control gap). Crypto scope, but the idea transfers: an arb-free SVI fit is one repair among many (#18/#128 gap). No code link. Band floor. |

**New candidates — ARCHIVE (12, band discipline, scores 28–43):** #221 FINCOSMOS (43), #222 Growth Optimal Portfolio (31), #223 Rank Reversals (40), #224 PanelGP (39), #225 CGMY certification (31), #226 Spec LASSO (34), #227 Asym-Sticky-NCO sector rotation (34), #228 Marketron (31), #229 RiskReason (31), #230 AMM learning agents (28), #231 2BSDE NN (31), #232 TSFM uncertainty calibration (39 — closes the Nov-4 leg gap on 2611.03592).

**No TEST, no INTEGRATE this run.** Scorer max 57 (#216).

**Re-checks:** #21 still v3 (2026-10-16), ICAIF '26 accepted, no code link — WATCH stands. #31 still v3 (2026-10-22), no journal ref, no code link — WATCH stands. **#183 movement:** Zenodo code+data link now confirmed present in the arXiv record comment (DOI 10.5281/zenodo.23770670) — record-claimed, Zenodo page not opened, stays WATCH.

**Ledger-append confirmation:** all 19 rows (#214–#232) appended once to the latest table in `~/workspace/hedge-desk-research/quant-lab-ledger.md`, verified present on disk (spot-checked #214, #216, #219, #232); #183 row updated with the 2026-11-06 re-check; 2026-11-06 kaizen entry appended (notes: use https for the arXiv API leg — plain http returned an empty body; check the year in date-filter ranges, 2611 = Nov 2026).

**Caveat:** one exec tool call inside the Quant Lab subagent run returned a nonzero exit (details not available to the parent run); the desk's report and ledger appends were verified complete on disk regardless.

---

## 5. Weather/War/Logistics Futures Event desk

As of ~13:30 PT / 16:30 ET, Fri 2026-11-06. **Bottom line:** The week's dominant catalyst is political, not physical: the U.S. midterm result repriced Iran-war risk sharply lower in oil, then fresh Hormuz tanker attacks on Nov 5–6 put a floor under the fall. Physical data underneath is tighter than the price fall suggests — notably distillates at a 23-year low — while the prompt Brent swaps curve has flipped to contango, signalling ample immediate supply. Grains are quiet into Tuesday's WASDE. No federal shutdown framing applies — EIA and USDA releases are on schedule.

### U.S. midterms repriced the war premium — FACT, with outcome SPECULATION
- **FACT:** Democrats regained the House and Senate in the Nov 3 midterms — at least 40 House seats and at least 7 Senate seats, above expectations (Reuters, Nov 6). https://www.reuters.com/commentary/reuters-open-interest/global-markets-view-usa-2026-11-06/
- **FACT:** Brent settled −8.7% Wed Nov 4 to $94.62/bbl; WTI −8.3% to $88.12 — both lowest since Aug 31 (Reuters via BusinessWorld, Nov 5). https://bworldonline.com/world/2026/11/05/791628/oil-slumps-after-midterm-election-rebuke-to-trump-raises-bets-on-iran-war-exit/
- **FACT:** Trump acknowledged the Iran war played a role in the defeat; VP Vance blamed the war squarely for the losses; Trump also said the U.S. had no immediate plans to strike Iran and would end $4bn/yr military aid to Israel at year-end (Reuters, Nov 6).
- **INFERENCE:** The market is pricing a higher probability of a negotiated de-escalation / constrained escalation, i.e. an unwinding of war premium — not a change in physical supply that day.
- **SPECULATION / UNVERIFIED outcome:** Whether de-escalation actually happens. Counter-evidence: Iran's Supreme Leader said U.S. hostility would persist regardless of party; a senior Iranian official said Washington and Tehran remain far from agreement; Qatar mediation is stepped up but no deal is reported (Reuters/BusinessWorld, Nov 5). Do not treat de-escalation as priced fact.

### Hormuz tanker attacks renewed — FACT, scale UNVERIFIED (conflicting measures)
- **FACT:** Iran reported three more tankers damaged in the Strait on Thu Nov 5; at least five vessels reported incidents since Sunday, per UKMTO — close to the record pace of 35 vessels hit in October (Reuters, Nov 5). IRGC said two tankers struck naval mines and another caught fire. https://www.reuters.com/world/middle-east/tankers-hit-hormuz-iran-keeps-up-pressure-after-us-vote-2026-11-05/
- **FACT:** One seafarer was killed Thu in a believed missile attack on the products tanker MT Velos, sailing unladen toward Bahrain (Reuters, Nov 6). https://www.reuters.com/world/one-seafarer-killed-missile-attack-tanker-gulf-2026-11-06/
- **FACT:** Reuters (Nov 6) puts overall Hormuz flows at under 60% of capacity. https://www.reuters.com/business/energy/oil-set-sharp-weekly-drop-middle-east-supply-concerns-provide-floor-2026-11-06/
- **UNVERIFIED — conflicting transit measures, do not collapse to one number:** PortWatch-based trackers cited in secondary sources put daily transits in single figures vs ~85/day pre-war (~7–10% of normal); Vortexa ship-tracking cited by Reuters puts Gulf crude/condensate exports at ~14m b/d in Oct, ~86% of pre-war, and total Gulf exports (ex-LPG) at 17.1m b/d in Oct vs 18.9m in Sep. The gap reflects pipeline diversion (Saudi East-West pipeline to the Red Sea) vs strait transits. Treat "Hormuz closed" as a transit statement, not an export statement.
- **UNVERIFIED (single low-quality source):** Sudan drone strikes Nov 4 damaging the Haya pipeline junction carrying South Sudanese crude to Bashair terminal — reported only by RegionAlert in this sweep, not corroborated by Reuters. https://regionalert.com/blog/hormuz-strait-oil-shipping-intelligence-2026.html
- **FACT (logistics):** Ocean freight: November demand moderating, but ~12% of global fleet capacity still absorbed by network bottlenecks; Hormuz security driving surcharges/diversions to Jeddah, King Abdullah Port, Khor Fakkan and Fujairah, even as more loops return to Suez (C.H. Robinson Edge, via LogisticsNews, Nov 6). https://logisticsnews.ph/2026/11/06/global-ocean-freight-markets-see-moderating-november-demand-amid-divergent-regional-capacity-and-geopolitical-shifts/

### Oil prices and curve — FACT (settlement) + INFERENCE (curve signal)
- **FACT (Fri settlement, Bloomberg via Rigzone, 16:05 ET Nov 6):** Jan Brent $98.32/bbl (+0.03%); Dec WTI $90.83 (+0.3%). Front-month fell ~13.2% on the week — biggest weekly percentage loss since 2022. https://www.rigzone.com/news/wire/oil_posts_biggest_weekly_drop_since_2022-06-nov-2026-185035-article/
- Note: intraday reports earlier Fri quoted ~12% and ~16% weekly declines — those were developing intraday estimates; the 13.2% settlement figure supersedes them.
- **FACT:** Brent swaps (CFDs) have moved into contango — prompt-week contract below next-week at the steepest discount since July (LSEG data, via Reuters Nov 6); 2nd- and 3rd-week contracts also at a discount. Brent futures from Jan 2027 delivery remain in backwardation. https://www.globalbankingandfinance.com/high-oil-prices-curb-demand-fresh-signs-glut-appear/
- **FACT:** JPMorgan (cited Reuters, Nov 6): global market surplus ~1.1m b/d in Sep, widening to ~1.4m in Oct; Goldman: global inventories stopped falling in Sep–Oct after declining early in the conflict. https://stockbiz.vn/en/news/market-on-november-6-oil-rebounds-nearly-4-gold-tops-usd-4100ounce-agricultural-commodities-diverge/42674935
- **INFERENCE:** Prompt physical market is pricing ample immediate supply / demand destruction from high prices, while the futures strip still prices near-term tightness and war premium. Divergence is the watch item: veteran trader Adi Imsirovic notes futures could follow swaps into contango if swaps stay there. This is a curve signal, not a supply forecast.
- **FACT (context, stale):** EIA's Oct 6 STEO (cutoff Oct 1) estimated global draws of 1.9m b/d in Q3 slowing to 0.7m in Q4 — now in tension with the JPMorgan surplus figures above. Next STEO Tue Nov 10 (EIA). https://www.eia.gov/outlooks/steo/release_schedule.php

### EIA petroleum — Wed Nov 4, 10:30 ET, week ended Oct 30 — FACT (EIA via Reuters/Morningstar)
- Crude −0.865m bbl to 409.8m, 4% below 5-yr avg, **5th straight weekly draw**, vs Reuters poll +0.877m build. Gasoline −0.222m to 209.0m, 2% below avg, vs +0.153m expected. **Distillate −3.6m to 99.3m — lowest since May 2003, 13% below 5-yr avg**, vs −0.1m expected. Total commercial petroleum −8.2m bbl. https://www.morningstar.com/news/dow-jones/2026110410540/us-crude-oil-stockpiles-post-fifth-straight-weekly-drop
- Refinery runs +199k b/d to 16.725m b/d, utilization 94.5% (+1.7pp); production 14.003m b/d; Cushing +0.28m; SPR −0.399m to 282.2m.
- **FACT:** Next Weekly Petroleum Status Report is **Thu Nov 12, noon ET** (Veterans Day shift), not Wed. https://www.fxempire.com/forecasts/article/crude-oil-forecast-why-falling-inventories-keep-supply-risks-in-focus-1643000
- **INFERENCE:** The distillate draw (36× the polled expectation) is the tightest physical signal in the report; the market fell anyway — price action this week was driven by the political repricing, not the inventory print.

### EIA natural gas — Thu Nov 5, 10:30 ET, week ended Oct 30 — FACT
- Injection +77 Bcf to 3,801 Bcf, vs WSJ survey +81 Bcf and 5-yr avg +61 Bcf; +54 Bcf (+1.4%) vs 5-yr avg (3,747 Bcf), −109 Bcf (−2.8%) y/y. South Central (1,208 Bcf) below its 5-yr avg; East/Midwest/Mountain/Pacific above. Dec Nymex ~$2.956/mmBtu Thu, −0.1%. https://www.morningstar.com/news/dow-jones/2026110516493/oil-prices-stay-below-100-as-traders-weigh-iran-diplomacy-supply-outlook-commodities-roundup
- **INFERENCE:** Adequate storage cushion into winter; no shortage signal. Next gas report Fri Nov 13.
- **FACT:** European gas storage 74% full as of Nov 3 vs 5-yr seasonal avg 90% (Barchart, Nov 5) — a secondary tightness note, not a U.S. pricing driver. https://www.barchart.com/story/news/8682147/above-average-inventories-knock-nat-gas-prices-lower

### USDA / grains — no new USDA report today; WASDE Tue Nov 10 — FACT + INFERENCE
- **FACT:** Next WASDE + Crop Production: **Tue Nov 10, 12:00 ET (11:00 CT)**, per USDA schedule. https://www.usda.gov/oce/commodity/wasde
- **FACT (Fri Nov 6 closes, ProFarmer/Brownfield):** Dec corn $4.41½ (+1½¢), week −6½¢, 6th straight weekly decline. Jan soybeans $11.93¾ (+5½¢), week −40½¢, after 9 straight daily drops and an 11-week low early Fri. Dec SRW wheat $5.91¼ (−8¢), week −12¼¢, 4-month low, 10th straight weekly loss. https://www.profarmer.com/news/after-bell/after-bell-soybeans-snap-losing-streak
- **FACT:** Weekly export sales: wheat 538k t beat expectations; soybeans 1.46 Mt, down 44% w/w; corn 1.29 Mt, down 1% w/w (Grain Central, Nov 6). https://www.graincentral.com/markets/daily-market-wire-6-november-2026/
- **INFERENCE / UNVERIFIED until print:** Trade expects USDA to cut corn yield (additional harvest data) and raise soybean yield — StoneX raised soy yield to 55.0 bpa from 54.1 and production to 4.725bn bu from 4.648bn; corn 183.1 bpa per StoneX snippet. ProFarmer flags soybeans as the biggest wildcard given wide carryout estimates. https://www.profarmer.com/news/agriculture-news/november-wasde-why-soybeans-are-biggest-wildcard

**Watchlist relevance:** No direct watchlist-name catalyst from this desk today; the cross-desk read is macro only — the ~13% weekly oil fall eased inflation pressure and helped Treasuries (10Y as low as 4.82% Thu, Reuters), while the Thu tech rout (~$3tn S&P 500 cap, Reuters) was driven by post-midterm AI/data-center backlash, not by futures — rates/equity desks own those verdicts.

**What would change the verdict:** A ceasefire / de-escalation announcement, or a renewed U.S./Israeli strike on Iran — either reprices the war premium in the opposite direction within a session. UKMTO incident count / Hormuz transit data for the coming week; a sustained return of transits vs continued attacks. WASDE + STEO, both Tue Nov 10; EIA petroleum Thu Nov 12 — distillate stocks and any revision to the surplus/draw picture. Brent swaps flipping back to backwardation (would kill the contango/surplus signal) or futures following swaps into contango (would confirm it).

---

## 6. Box/Parity Observer

**Verdict: nothing material on parity violations this week. One index-constituent note and one upcoming reconstitution date worth tracking.**

- **No new published parity-violation analysis found for SPY/QQQ in the past week** (search as of 2026-11-06 13:26 PT). [FACT — absence of findings in web sweep; not proof none exists]
- The only recent academic item surfaced is Shin, "The P behind Q: Empirical Evidence from Physical Drift in Put-Call Parity" (arXiv 2605.12250, dated May 19, 2026) — **not new this week**; it finds quoted put-call parity tightly compressed in SPX/RUT price space, with a systematic wedge only in the synthetic-forward vs traded-futures channel under finite arbitrage capital. [FACT — arxiv.org/pdf/2605.12250v3.pdf] No action: confirms the desk's standing rule that deterministic parity outranks model output; the wedge is a funding/capital friction, not an exploitable box-spread mispricing for a paper-only desk.
- Nov 5 flow data (SquawkFlow) shows heavy 0DTE SPY/QQQ put volume (SPY Nov 5 puts ~$4.1B estimated premium; QQQ Nov 5 puts ~$2.4B) — [FACT, squawkflow.com, as of Nov 5, 2026 16:14 ET] — but volume/flow is not a parity violation, and no box-spread dislocation was reported. [INFERENCE — no parity signal inferred from flow alone]
- **S&P 500: Okta replaced Kenvue before trading opened Nov 4, 2026.** [FACT — akka.app, updated 2026-11-05] Constituent swap only; no methodology change, no parity implication for SPY options.
- **Nasdaq-100 annual reconstitution calendar (2026 methodology, live since May 1, 2026): ranking Mon Nov 30, announcement after close Fri Dec 11, effective open Mon Dec 21.** [FACT — pacifictape.com, published Oct 24, 2026] Watch item only: reconstitution flows can briefly widen index-arbitrage basis around the effective date, but no violation is expected or reported. [SPECULATION — flagged as watch item, not a prediction]
- No new S&P or Nasdaq methodology document published this week; the May 2026 Nasdaq-100 update (quarterly reviews, fast-entry rule, 3× float cap) is already on record. [FACT — nasdaq.com]

**Bottom line:** No parity-violation signal, no box-spread mispricing, no methodology change affecting SPY/QQQ options this week. Nothing actionable for the value lens.

---

## 7. Bonds & Rates desk

**Source:** repo module `hedge_desk.rates_desk.rates_environment()`, mode `REAL_FRED_RATES`, schema `hedge-desk-rates-desk-1.0.0`, data source `fred-public-csv-http-200`. Module ran clean (exit 0). All numbers below are verbatim from module output — no Yahoo substitution, no retyping from memory.

### Levels (FACT)

| Series | Level | As-of |
|---|---|---|
| Fed funds effective rate (DFF) | **3.88%** | 2026-11-04 |
| Treasury 2Y (DGS2) | **4.58%** | 2026-11-04 |
| Treasury 10Y (DGS10) | **4.90%** | 2026-11-04 |
| SOFR | **3.92%** | 2026-11-05 |
| EFFR | **3.88%** | 2026-11-05 |
| OBFR | **3.88%** | 2026-11-05 |

- Fed funds change over 60-day window: **+0.25** (module figure, verbatim).
- 2s10s slope: **+32 bp** (4.90 − 4.58); shape **UPWARD_SLOPING**.

### Slope / direction of change (FACT, computed from the module's own 60-day histories)
- Slope at window start (2026-09-08): 4.80 − 4.39 = **41 bp** → now **32 bp**: curve **flattened ~9 bp** over 60 days.
- Near-term slope is steady: Nov 2 = 32 bp, Nov 3 = 34 bp, Nov 4 = 32 bp — no fresh steepening/flattening move this week.
- Both ends down from their autumn peaks: 2Y 4.92% (Sep 28) → 4.58%; 10Y 5.31% (Oct 5) → 4.90%. The 10Y has spent the last two weeks below 5.00% after sitting above 5% for most of September–October.

### Funding stress (FACT + INFERENCE)
- SOFR − EFFR = 3.92 − 3.88 = **+4 bp**; OBFR = EFFR exactly (3.88%). **INFERENCE:** no funding stress — overnight funding is trading essentially at the policy rate, with no SOFR/EFFR dislocation. A spread widening past ~10–15 bp would change this read.

### Premium-pricing read (INFERENCE)
- 10Y at 4.90% keeps discount rates elevated: **pressure on long-duration growth multiples** — the watchlist's growth-heavy names (NVDA, TSLA, QQQ) carry the most rate sensitivity; premium sellers should not assume multiple expansion is doing the work.
- But the direction is mildly favorable: yields have drifted *down* from the Oct 5 peak (10Y −41 bp), and the curve flattening is driven by the long end falling faster than the front end — a modest easing of the discount-rate headwind, not a regime change.
- Upward-sloping curve (+32 bp) with no inversion: no recession signal from 2s10s; no curve-driven reason to expect a volatility regime shift from rates alone.

### What would change these verdicts
- 10Y reclaiming 5.25%+ or 2s10s inverting (slope < 0) → flip to a harsher discount-rate / recession-risk read.
- SOFR − EFFR widening beyond ~10–15 bp, or OBFR diverging from EFFR → funding-stress flag.
- A Fed funds move (next FOMC decision) would reset the front-end anchor; the module's +0.25 window change is a measured fact, not a forecast.

**Desk status: OK — no failures.** Module note (verbatim): "Observations of official FRED daily series. Fed funds/src curve change is a measured fact, not a forecast and not advice. No order placed."

---

## Cross-desk reconciliation

- **NVDA Nov 17 earnings is confirmed by two desks independently** (Earnings desk via Nasdaq API + Yahoo; Premium desk via iv-inputs file). Implied move ±6.2% and the 11-20 IV jump to 0.694 are consistent — the event premium is real and priced.
- **AAPL/MSFT:** both reported in the last week (Nov 2 / Oct 28) and both have window-contingent realized-vol windows — the same earnings jumps that drove their reports are the single-day variance drivers. No clean IV-vs-realized verdict on either.
- **Rates vs futures:** the ~13% weekly oil fall eased inflation pressure and helped Treasuries (10Y as low as 4.82% Thu per Reuters) — consistent with the rates desk's read of yields drifting down from the Oct 5 peak. No contradiction.
- **Dividends vs premium:** MSFT's Nov 19 ex-date at the new $0.98 rate sits inside the 11-20 expiry window — premium/assignment analysis spanning Nov 19 must use $0.98, not $0.91.
- **No contradictions between desks required resolution.** One open item: IV rank remains UNVERIFIED for all names (no free IV-history source) — the Premium desk's "elevated" label for NVDA/TSLA is absolute, not relative to history.

## Desk status
All seven desks reported. No desk FAILED. No retries needed. Quant Lab: one internal exec tool call returned nonzero (details unavailable to parent run); report and ledger appends verified complete on disk.
