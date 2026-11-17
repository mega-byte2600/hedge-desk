# Hedge-Desk Daily Research — Tue 2026-11-17

**Run:** 13:30 PT daily research. **Package written:** 2026-11-17, ~13:55 PT (post-close NVDA print incorporated ~16:35 ET / 13:35 PT). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA. **Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety. **Labels:** FACT = primary source + as-of; INFERENCE = stated logic from FACTs; SPECULATION = ungrounded; UNVERIFIED = looked, could not confirm. Research only — no trades, no Risk of Ruin, no GitHub operations.

## Summary — the 5 most decision-relevant items

1. **NVDA beat after the close — "beat, not a re-rating" (first read).** Revenue $115.84B (+103% y/y) vs ~$108.8B consensus; non-GAAP EPS $2.68 vs $2.47; Q4 guide $130.0B ±3% vs ~$125.3B; +$150B buyback authorized. After-hours +2.20% to $158.88 — well inside the ±8.1% move options priced. The 5:00 p.m. ET call and a full release teardown are still owed. (Desk 1)
2. **Desk 7: 25bp Dec 9 hike call intact, and the market now prices size as 25bp.** Tally unchanged 5 HIKE / 1 CUT / 4 NEUTRAL. Kalshi >25bp tail collapsed $0.12 → $0.04 in four days while 25bp firmed to $0.91. FOMC minutes land tomorrow, Wed Nov 18, 2:00 PM ET — the check on whether 10–2 understates division. (Desk 7)
3. **Live ATM IV recovered after the nine-attempt null streak.** NVDA 1-DTE IV was 136.6% pre-print (implied ~±8–9% move). Every IV-vs-realized comparison remains WINDOW-CONTINGENT: the Nov 5 crash day is 37–54% of every symbol's 20-day realized variance. IV rank UNVERIFIED for all six (no free IV history). (Desk 3)
4. **Hormuz: two confirmed tanker strikes Nov 16, a second strike Nov 17 (one seafarer missing); Kerch Bridge road arch collapsed into the canal today — yet oil fell.** Brent ~$91.6 Tue morning on the IEA Q4 surplus call. The market is pricing surplus over disruption; that discount is fragile. EIA weekly lands tomorrow Wed 10:30 ET. (Desk 5)
5. **MSFT goes ex-dividend Thu Nov 19 at the new $0.98 rate** — the only watchlist ex-date in the next four weeks (24th consecutive annual increase, 0.77% yield). Quant Lab's top item: NoLBERT-Calls (WATCH) — a hindsight-free earnings-call encoder. (Desks 2, 4)

---

## 1. Earnings Event desk

**Headline (FACT):** NVDA — the only watchlist name reporting in the next two weeks — reported Q3 FY2027 after the close today, ~4:22 p.m. ET, and beat on every headline line. The release text itself was not read in full — a statement teardown is still owed (call 5:00 p.m. ET).

### Upcoming earnings — next 2 weeks (Nov 17 – Dec 1)

| Name | Date | Timing | Consensus | Implied move | Hist. avg earnings-day move |
|---|---|---|---|---|---|
| NVDA | Tue Nov 17, 2026 | After close; results ~4:20 p.m. ET, call 5:00 p.m. ET | EPS $2.49 (14 est.); revenue ~$108.8–109.2B | ±8.1% (straddle; see below) | ±7.8% avg peak move, 10-yr (n=39); ±5.7% last 2 yrs |
| SPY / QQQ | — | n/a (ETF) | — | — | — |
| AAPL / MSFT / TSLA | none in window | — | — | — | — |

**FACT (Nasdaq earnings calendar API, pulled 13:30–13:35 PT today):** NVDA is the sole watchlist name on the calendar Nov 17–Dec 1. Every session day checked (Nov 17, 18, 19, 20, 23, 24, 25, 27, 30, Dec 1); no AAPL/MSFT/TSLA rows. NVDA fiscal Q3 ending Oct 2026, consensus EPS $2.49, last-year EPS $1.24 (reported Nov 19, 2025), market cap $3.76T. Timing company-confirmed: date set Oct 28, re-confirmed in the Nov 12 CEO-transition release; CFO Colette Kress (interim CEO) leading the call.

**Pre-print setup (FACT, own computation, CBOE delayed quotes, file timestamp 16:27:31 ET, underlying close $155.46):** Nov 18 expiry ATM 155 straddle mid $12.62 ($6.55 call + $6.08 put) = **±8.12%**. ATM IVs 191.4% call / 194.8% put — no parity red flag (agree within 3.4 pts); straddle-implied vol reconciles with quoted IV (0.8 × 193% × √(1/365) × $155.46 ≈ $12.57 vs $12.62 observed). Nov 20 weekly straddle $15.00 = ±9.65%. IV30 65.26%, +2.15 pts on the day. Skew: Nov 18 140P IV 198.9% vs 175C 199.0% — essentially flat at the wings (strikes not symmetric around $155.46, so read as "no directional skew signal," not a precise skew print). **Corroboration:** EarningsWatcher (Nov 17) prints ±8.4% implied move — consistent with ±8.1% (same full-expiry straddle concept). ApexVol's ±6.4% and optionstrading.org's Nov 12 ±6.8% are a *different* quantity — the reaction-session-only move after stripping ordinary sessions — not a conflict. **INFERENCE:** the market priced roughly an 8% move through Wednesday's close, ~6.5% of it the reaction itself. (Note: the Premium desk's 136.6% 1-DTE ATM IV scaled as 136.6%/√252 ≈ 8.6% is the same move by a second method; the 0.5pt gap is method, not a conflict.)

**History (FACT, EarningsWatcher, Nov 17):** 10-yr average earnings-day peak move ±7.8% (n=39), median ±6.5%, 95th percentile ±18.3%; last 2 years cooler at ±5.7%. Actual beat the priced move in only 5 of the last 17 reports (29%). Last report (Aug 26, 2026): priced ±5.9%, closed +8.7% (peak +9.9%). SentiSense: last 8 reports averaged a 4.0% move (median 3.2%). **INFERENCE:** tonight's ±8.1% priced move sits above the recent-regime average but inside the 10-year ordinary range (80th percentile ±9.8%) — the market is charging a premium for this print relative to the last two years, not relative to NVDA's decade.

**Setup context (FACT):** NVDA closed $155.46, −0.44% vs Monday's $156.14 (Yahoo + CBOE agree). Down ~30% from the Oct 6 high (~$239), on a six-session losing streak, under interim CEO Kress after Jensen Huang's Nov 11 resignation (8-K, Nov 12). Company guide (Aug 26 release): revenue $108.0B ±2%, gross margin 74.0% ±50bp, no China Data Center compute assumed. Consensus sat ~$1B above the guide midpoint, inside the band.

### NVDA actuals — just released (4:22 p.m. ET)

**FACT (corroborated across Seeking Alpha, CoinDesk, GamesBeat, Longbridge, all citing the company release/8-K):**
- Revenue **$115.84B, +103% y/y** — beat consensus ~$108.8B by ~$7.1B and beat the top of the company's own guide band ($110.16B).
- Non-GAAP EPS **$2.68** vs $2.47 consensus (+$0.21); GAAP EPS $2.70.
- Data Center revenue **$107.6B, +110% y/y** vs ~$101.9B estimated — 93% of total revenue.
- Gross margin 74.8% GAAP / 74.9% non-GAAP vs 74.0% guided.
- **Q4 FY2027 guidance: revenue $130.0B ±3%** vs ~$125.3B consensus; gross margin 71–72%.
- **+$150B share-repurchase authorization** added.
- After-hours (Finnhub, as of 16:24 ET): **$158.88, +2.20%** vs the close — a positive but modest reaction, well inside the ±8.1% priced move. **INFERENCE:** the beat was large in dollars but substantially pre-sold by a guide/consensus structure the market had already discounted; the first read is "beat, not a re-rating" — the 5:00 p.m. call decides whether that holds.

### Other watchlist names — next reports (outside the window)

**FACT:** AAPL, MSFT and TSLA all reported in the Oct–Nov season and have no confirmed date inside the next two weeks (Nasdaq calendar, above). **INFERENCE (estimated, unconfirmed — sources conflict by a day, so exact dates are UNVERIFIED):** next reports cluster in late Jan 2027 — MSFT ~Jan 26–27, TSLA ~Jan 26–27, AAPL ~Jan 28, all after close, all estimated from reporting cadence, none company-confirmed. MSFT's last print was Oct 28, 2026 (Q1 FY27: EPS $4.89 vs $4.72 consensus, revenue $92.28B — MarketBeat).

**What would change the verdict:** the 5:00 p.m. ET call (Q4 guide color beyond the $130B headline, Blackwell/Rubin delivery, memory-cost pressure on the 71–72% margin guide, China, CEO search); a full release teardown (owed) — AInvest flagged receivables, the $279B supply-commitment book, and equity-security gains inside other income ($23.7B in H1 FY27) as the lines that matter more than the headline; Wednesday's session closing outside ±8.1% from $155.46 would mean the market moved more than options priced — the first such overshoot since August.

**Sources:** Nasdaq earnings calendar API (api.nasdaq.com/api/calendar/earnings, Nov 17, 13:30–13:35 PT); CBOE delayed quotes (cdn.cboe.com, 16:27:31 ET); Yahoo Finance quoteSummary/quote (cookie+crumb; close $155.46); NVDA Oct 28 call-setting release + Nov 12 8-K; EarningsWatcher NVDA pages (Nov 17); SentiSense big-tech earnings brief (Nov 14 data); Seeking Alpha (Nov 17, 4:22 p.m. ET), CoinDesk, GamesBeat, Longbridge for the print; Finnhub after-hours (16:24 ET).

---

## 2. Dividend Opportunity desk

**Window:** ex-dates Nov 17 – Dec 15, 2026 (4 weeks). Checked: Nasdaq dividends calendar day-by-day sweep Nov 17 – Dec 21, Nasdaq per-symbol dividend histories, Yahoo Finance v8 chart (prices), web corroboration for NVDA/SPY.

### Upcoming ex-dividend dates in the window — only one

| Symbol | Ex-date | Amount | Record | Payable | Indicated annual / yield* | Note |
|---|---|---|---|---|---|---|
| **MSFT** | **Thu Nov 19, 2026** | **$0.98/qtr** | Nov 19, 2026 | Dec 10, 2026 | $3.92 / **0.77%** | First ex-date at the raised rate; raise announced Sep 15, 2026 |

\* Yields computed from Yahoo Finance intraday prices ~midday PT Nov 17, 2026 (MSFT $506.24).

**MSFT — FACT** (Nasdaq calendar + Nasdaq dividend history, both pulled this session): ex-date Nov 19, 2026, $0.98, record Nov 19, payable Dec 10, 2026, declared Sep 15, 2026. Prior quarterly rate $0.91 — the raise is +7.7%. **Consecutive increases: 24** (per the desk standard `~/workspace/hedge-desk-research/dividend-count-standard.md`, incl. the Sep 2026 raise; initiated 2003, no skipped year). No further MSFT raise is expected before the next annual cycle (typically September) — **INFERENCE** from the annual cadence.

**Increases / cuts / specials: none newly announced in the window — FACT** (Nasdaq calendar sweep found no other watchlist entries Nov 17 – Dec 21; no specials listed). The MSFT raise and the NVDA step-up below were both announced earlier and already carried in prior packages.

### Rest of watchlist — no ex-date in the window

- **AAPL — FACT** (Nasdaq history): last ex-date **Nov 12, 2026, $0.27**, payable **Nov 16, 2026** (paid yesterday). Rate raised $0.26 → $0.27, announced Apr 30, 2026. Next ex-date ~Feb 2027 — **INFERENCE** from the quarterly cadence; not yet declared. Indicated yield $1.08 / $351.91 = **0.31%**. Consecutive-increase count **UNVERIFIED** this run (not pulled from issuer history; the desk standard resolves MSFT only).
- **NVDA — FACT** (Nasdaq history, corroborated by NVIDIA Form 10-Q for the quarter ended Jul 26, 2026): last ex-date **Sep 10, 2026, $0.25**, paid Oct 1, 2026. The board raised the quarterly dividend **25-fold, $0.01 → $0.25, on May 18, 2026**; first payment at the new rate Jun 26, 2026. December dividend **not yet declared** as of Nov 17 — **FACT** (absent from the Nasdaq calendar sweep through Dec 15; StockAnalysis also lists it undeclared; prior two Decembers went ex Dec 5, 2024 and Dec 4, 2025, history not a forecast). Indicated yield at the new rate $1.00 / $155.46 = **0.64%**; trailing-12-month paid is $0.52, i.e. 0.33% — do not annualize the $0.25 rate as if it applied all year. **Watch item:** declaration expected late Nov; if declared at $0.25, the ex-date would fall ~early Dec, inside or just past the window edge — timing **UNVERIFIED** until declared.
- **SPY — FACT** (TipRanks / Wall Street Horizon / StockAnalysis, corroborated across sources): last ex-date **Sep 18, 2026, $1.88883**, paid Oct 30, 2026; TTM $7.58, yield **~1.04%** at $732.44. Next ex-date **expected Dec 18, 2026** (TipRanks estimate; Wall Street Horizon lists Dec 18 with pay Jan 29, 2027) — **just outside the 4-week window** and amount **UNVERIFIED** (SPY distributions vary each quarter; Nasdaq calendar has no SPY listing for Dec 18 as of Nov 17). SPY's Sep payment was −0.8% vs June's $1.90 — a variable-distribution fluctuation, not a cut; **INFERENCE** that it carries no signal, since SPY's payout tracks index dividends.
- **QQQ — FACT** (Nasdaq history): last ex-date **Sep 21, 2026, $0.75143**, paid Oct 8, 2026. Next ex-date ~Dec 21, 2026 — **INFERENCE** from the quarterly cadence, outside the window, timing and amount **UNVERIFIED**. Yield **UNVERIFIED** this run (Q4 2025 amount not pulled; Nasdaq SPY/QQQ quote endpoints returned errors/empty for this pull).
- **TSLA — FACT** (Nasdaq history endpoint returns no dividend rows): pays no dividend; nothing to report.

**What would change this:** NVDA declaring its December dividend (watch late Nov): a declaration at $0.25 confirms the new rate as the run-rate; a declaration below $0.25 or a skip would reopen whether the May step-up was one-off. SPY's Dec 18 distribution amount (announced days before): a large deviation from the ~$1.89–1.99 range would reflect index-level dividend shifts, not a single-name call.

**Sources:** Nasdaq dividends calendar API (`api.nasdaq.com/api/calendar/dividends`, day-by-day sweep Nov 17–Dec 21, 2026, pulled Nov 17); Nasdaq quote dividends history (`api.nasdaq.com/api/quote/{MSFT,AAPL,NVDA,QQQ}/dividends`); Yahoo Finance v8 chart (intraday prices ~midday PT Nov 17, 2026); NVIDIA Form 10-Q quarter ended Jul 26, 2026 (SEC EDGAR, via search result); TipRanks / Wall Street Horizon / StockAnalysis SPY dividend pages.

---

## 3. Overnight Premium desk (IV)

### Headline
**Live ATM IV recovered for all six symbols — first non-null pull in nine attempts** (the null streak was expiry-calendar-driven: yesterday's nearest expiry was Monday Nov 16, already dead at pull time; today's nearest expiry, Nov 18, is live). **NVDA front-end IV was 136.6% at 1 DTE into earnings tonight after close — textbook binary-event premium: avoid.** Every IV-vs-realized comparison below is **WINDOW-CONTINGENT**, never a clean verdict: the Nov 5 crash day drives 37–54% of every symbol's 20-day realized variance.

### Sources & freshness
- **Live IV levels: Yahoo Finance v7 options chain, cookie+crumb handshake, pulled this session at 2026-11-17T13:27:33-08:00** (recipe per `~/workspace/hedge-desk-research/nightly/pull_iv_inputs.py`). Spot prices cross-checked against Yahoo v8 chart at the same time — identical (SPY 732.44, NVDA 155.46, MSFT 506.24). **FACT.**
- **Realized 20d + window screen: STALE — `~/workspace/hedge-desk-research/nightly/2026-11-16-iv-inputs.json`, as_of 2026-11-16T14:54:31-07:00 (~22.5h old, within the 26h guard, but yesterday's post-close data).** All six ATM IVs in that file are null (eighth straight null pull). **FACT.**
- **IV rank: UNVERIFIED for all six symbols** — no IV history is available from free sources (Yahoo publishes no historical IV series); never guessed. **UNVERIFIED.**

### IV snapshot — live ATM IV (today, 13:27 PT) vs realized 20d (STALE, window 2026-10-19 to 2026-11-13)

| Symbol | Spot | ATM IV 1 DTE (exp 2026-11-18) | ATM IV 31 DTE (exp 2026-12-18) | Realized 20d (STALE) | Max 1-day var share | Window |
|---|---|---|---|---|---|---|
| SPY | 732.44 | 21.7% (call 21.6 / put 21.8) | 20.6% | 22.83% | 54.4% | **CONTINGENT** |
| QQQ | 656.95 | 33.6% (34.9 / 32.3) | 30.5% | 36.50% | 46.5% | **CONTINGENT** |
| AAPL | 351.91 | 22.9% (22.4 / 23.4) | 26.2% | 28.24% | 46.3% | **CONTINGENT** |
| MSFT | 506.24 | 45.9% (46.6 / 45.2) | 34.8% | 37.35% | 41.9% | **CONTINGENT** |
| NVDA | 155.46 | **136.6%** (135.7 / 137.6) | 64.0% | 54.48% | 36.9% | **CONTINGENT** |
| TSLA | 380.11 | 47.9% (47.2 / 48.6) | 51.2% | 61.48% | 47.8% | **CONTINGENT** |

All figures **FACT** from the pulls cited above. ATM IV = mean of ATM call/put `impliedVolatility` at the strike nearest spot; call/put IVs sit within ~1–3 pts of each other on every symbol — no put-call parity anomaly evident in the ATM straddles (**FACT**; deterministic parity outranks any model read, and nothing here contradicts it).

### Per-symbol reads (all IV-vs-realized verdicts WINDOW-CONTINGENT)
- **SPY — no edge visible.** Near IV 21.7% vs STALE realized 22.8%: roughly at par; 31 DTE 20.6% slightly below the front end. **INFERENCE:** term structure mildly downward-sloping, consistent with no near-term event premium in the index. No verdict on cheap/rich premium is possible while the realized window is dominated by one day.
- **QQQ — no edge visible.** Near 33.6% vs realized 36.5% (below), 31 DTE 30.5%. Same caveat as SPY: the "below realized" gap is an artifact candidate, not a signal, while Nov 5 is 46.5% of the window.
- **AAPL — no edge visible.** Near 22.9% vs realized 28.2%; upward-sloping curve (near < 31 DTE 26.2%). **INFERENCE:** the market prices more vol a month out than tomorrow — the opposite of an event spike; nothing to chase.
- **MSFT — near-term IV elevated, treat with suspicion.** 1 DTE 45.9% vs realized 37.3% and vs 31 DTE 34.8% — a steep front-end spike with no earnings in window (no MSFT earnings in the next 45 days per the Nov 16 Nasdaq sweep). **INFERENCE:** a 1-DTE print is the noisiest tenor (theta decay + wide spreads compress into the solver); do not read 45.9% as a durable vol regime. The 31 DTE 34.8% sits below STALE realized — again WINDOW-CONTINGENT, not a cheap-premium call.
- **NVDA — EARNINGS TONIGHT AFTER CLOSE (2026-11-17). AVOID premium into the event.** 1 DTE ATM IV 136.6% vs 31 DTE 64.0% vs STALE realized 54.5%: the front end priced a ~2× vol event. Implied 1-day move at 136.6% ≈ 136.6% / √252 ≈ 8.6% (**INFERENCE**, standard 1-day scaling — the options market priced roughly an ±8–9% earnings move; the Earnings desk's straddle computation gives ±8.1% — same move by a second method). Selling premium into this binary is exactly what the desk rule forbids; buying it pays the spike. The 31 DTE 64.0% vs realized 54.5% gap is also WINDOW-CONTINGENT. (Post-print: NVDA beat; see §1. The 136.6% front end collapses on the result — re-pull tomorrow's nearest expiry before any NVDA premium read.)
- **TSLA — no edge visible.** Near 47.9% and 31 DTE 51.2% both below STALE realized 61.5%, upward-sloping curve. **INFERENCE:** the market is pricing *less* vol than the crash-inflated trailing window — but that window is 47.8% one day, so "IV cheap vs realized" is not a usable verdict.

### Earnings inside the window
- **NVDA reported today, Tue 2026-11-17, after close — FACT** (Nasdaq earnings calendar via the Nov 16 iv-inputs file; corroborated by the 136.6% 1-DTE IV print, which is itself the market's earnings signature). No other watchlist name has earnings in the next 45-day sweep window. **FACT** per the same file.

### What would change the verdicts
1. **Nov 5 crash day aging out of the 20-day window** (after Dec 3) — realized vols will fall sharply and the window-contingent flag lifts; only then do IV-vs-realized comparisons become clean.
2. **NVDA's print tonight** — done (see §1); re-pull tomorrow's nearest expiry before any NVDA premium read.
3. **A working IV-history source** — would convert IV rank from UNVERIFIED to a scored read; none exists from free sources today.
4. **MSFT 1-DTE spike persisting into the Nov 19–20 expiries** — would turn a noisy 1-DTE print into a real near-term vol event worth investigating.

**Desk status:** delivered, with two standing limitations named: IV rank UNVERIFIED for all six (no free history), and every IV-vs-realized comparison WINDOW-CONTINGENT (Nov 5 = 37–54% of 20-day variance). No desk failure: the live Yahoo pull succeeded on all six symbols with zero failures, and spots were independently corroborated via v8 chart.

---

## 4. Open Quant/AI Model Lab

**Sweep coverage (FACT, arXiv API, as of 2026-11-17 ~13:30 PT):** q-fin window submitted Nov 14–16, announced Tue Nov 17 — 16 new v1 items. Date-range query and no-filter control agree (newest 2611.21326, 2026-11-16T16:17:57Z). GitHub leg SKIPPED per the run brief's ban on GitHub operations — no new-repo discovery, no repo re-checks, no code/license verification. All scores run through the repo scorer (`hedge_desk.research_intelligence.assess_source`, module — never hand-scored). No TEST/INTEGRATE movement this run (max score 60).

### New candidates (ledger #292–#297, appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md`, now 296 rows)

| # | Candidate | Score | Disp. | Why |
|---|---|---|---|---|
| 294 | Foley et al — **NoLBERT-Calls: Reading Earnings Calls Without Hindsight** (arXiv:2611.19849v1) | 60 | **WATCH** | Run's top score. NoLBERT encoder (pretrained only on 1976–1995 text) adapted to earnings calls with a hard 31 Dec 2023 cutoff; tested on every US call Jan 2025–Oct 2026 (20,323 calls, 254,575 questions): true answer ranked first 78.0% (95% CI 77.8–78.2; chance 8.0%), +1.0pp vs call-adapted ChronoBERT, +3.4pp vs FinBERT; year-by-year 2013–2026 test finds no look-ahead premium (source-reported, **UNVERIFIED** — abstract only). Directly the desk's purged/look-ahead doctrine applied to earnings-call text. No code link in record; staged adaptation ~13 GPU-hours. Scorer inputs: signal 4 / data 4 / impl 3 / risk 4 / cred 3, reproducible False. Follow-up: re-check code/model release; idea transfer only for now. |
| 292 | Bansal/Iyer/Jain — **PIRanNN: Random-Feature Pricing and Calibration under Jump-Diffusion and SV** (arXiv:2611.19792v1) | 57 | **WATCH** | Single least-squares solve prices European options + Greeks + parameter derivatives under Merton/Kou/Heston/SABR; Black–Scholes subtraction cuts jump-model error ~100×. Honest limits (source-reported, **UNVERIFIED** — abstract only): FD with the same subtraction is still ~100× more accurate; Heston/SABR errors ~1%, calibrated params within ~15%. Code linked in arXiv comment (github.com/RiskLabIISc/PiRANN) but **NOT verified** — GitHub leg banned; license **UNVERIFIED**. Scorer: 4/3/4/3/3, reproducible False. Follow-up: verify repo + license via a permitted leg; sandbox vs FD on a live SPY chain if licensed. |
| 293 | Servais/Hainaut — **European derivatives pricing via constrained Gaussian process regressions** (arXiv:2611.20746v1) | 51 | **WATCH** | GP prior conditioned on the Feynman–Kac PIDE; closed-form differentiable price, Greeks without simulation/finite differences; Weissinger fixed-point convergence proof for the jump iteration. Illustrated on a 5-D Heston + Kou-jump problem, benchmarked vs Monte Carlo (source-reported, **UNVERIFIED** — abstract only). No code link in record. Scorer: 4/2/3/3/3, reproducible False. Follow-up: re-check code release; sandbox vs #292 if code appears. |
| 297 | Kim/Zhou — **EWMA Principal Eigenportfolios** (arXiv:2611.20363v1) | 42 | ARCHIVE | Beta-hedging vs SPY/RSP; 50-stock Dirichlet portfolios: mean variance reduction 92.17% (PC1) vs 79.03% (SPY) vs 91.93% (RSP); advantage over RSP mixed, costs excluded (source-reported, **UNVERIFIED**). Portfolio lane, not options/vol/earnings/dividend — archived on band discipline. |
| 295 | Zhang — **BSDE Mollification Regularization, Part I: Theory** (arXiv:2611.20550v1) | 36 | ARCHIVE | Theory only; numerical evidence + implementation deferred to companion Part II. No code, no data, no desk-ready method. Reopen when Part II appears. |
| 296 | Adachi/Hara — **Toward an Admissibility Theory of Aharonov–Bohm Arbitrage** (arXiv:2611.19870v1) | 25 | ARCHIVE | Provisional categorical framework; finite FX toy model; identifying parameters from market primitives is the stated remaining problem. No code, no data, no options transfer. |

**Triage exclusions (no ledger rows):** 2611.21326 health-insurance claims, 2611.21262 bank-liquidity networks, 2611.20911 portfolio-subspace transport, 2611.20839 HF crypto LOB Hawkes, 2611.20589 ESG fragility, 2611.20242 markets for compute, 2611.20163 log-optimal regime-switching portfolios, 2611.19937 AllocFlow portfolio trading, 2611.19903 graph-attention multi-asset portfolios, 2611.19068 corporate societal stances — all out of scope.

**Re-checks (FACT, arXiv API id_list):** core version-triggered set #4 (2510.20699 v1), #9 (2608.22478 v2, 2026-10-19), #13 (2609.00332 v1), #14 (2509.11928 v3), #15 (2509.05911 v1), #20 (2609.22893 v2), #21 (2608.00616 v3), #30 (2607.08500 v3), #31 (2511.07571 v3), plus #25 (2609.13402 still v4, 2026-11-10) and #257 (2611.13616 still v2, 2026-11-12) — **no version movement on any item; all stay WATCH.**

**Decision-relevant takeaway:** the run's one item with real desk transfer is #294 NoLBERT-Calls — a hindsight-free earnings-call encoder that operationalizes the desk's own look-ahead discipline (78.0% top-1 vs 8% chance, no look-ahead premium over 2013–2026). It is WATCH, not TEST: v1 preprint, no code/model release in the record. Nothing reached TEST or INTEGRATE.

---

## 5. Weather / War / Logistics Futures Events

**Bottom line:** Fresh and material today: **two tankers confirmed struck in/near the Strait of Hormuz on Mon Nov 16** (a second strike on one vessel Nov 17 left a seafarer missing), **Ukraine collapsed the Kerch Bridge road arch into the shipping canal today**, and **oil fell a second straight session on the IEA's Q4 surplus call** — yet the market is pricing surplus, not disruption: Brent ~$91.6 Tue morning, down from $92.44 Mon settle and a $118 high on Oct 30. EIA weekly lands tomorrow; USDA had no new WASDE this week (last one Nov 10).

### Catalyst triage

| Event | Date | What it is | Market relevance |
|---|---|---|---|
| **EIA Weekly Petroleum Status Report** | **Wed Nov 18, 10:30 ET** (week ending Nov 13) | Weekly crude/products stocks, refinery runs, imports/exports | Direct crude-products catalyst. Last print (Nov 12, week ending Nov 6) was a big bearish surprise: crude **+4.7m bbl to 414.4m** vs Reuters poll expecting a ~1.1m draw; gasoline +1.8m, distillate +4.1m, total commercial petroleum +11.4m. [FACT — EIA Table 1 via eia.gov; Reuters via Kilambi/B OE Report] |
| **API Weekly Statistical Bulletin** | **Today ~4:30pm ET** (Tue) | Private survey, ~18h ahead of EIA | Preview of tomorrow's EIA print; last week API showed +8.97m crude vs EIA's +4.66m — direction agreed, magnitude did not. [FACT — api.org; Gate.com] |
| **EIA Weekly Natural Gas Storage** | **Thu Nov 19, 10:30 ET** | Working gas in storage | Last print: 3,862 Bcf on Nov 6, up from 3,801 Bcf Oct 30. [FACT — EIA via SageNoodle/ReadGeo] |
| **USDA Weekly Export Sales** | **Thu Nov 19, 8:30 ET** | Weekly grain/oilseed export sales | Tests the higher US export forecasts in the Nov 10 WASDE. [FACT — Morningstar/Dow Jones grain highlights] |
| **USDA Crop Progress** (released) | **Mon Nov 16** | Corn 88% harvested (vs 92% 5-yr avg; Iowa 84%, 11 pts behind avg); soybeans 96% (vs 95% avg); winter wheat 92% planted, 82% emerged, **53% good-to-excellent, +4 pts w/w** | Harvest nearly done; corn lag is the only soft spot. No major surprise — Archer: "held no major surprises." [FACT — USDA NASS via DTN/Farm Progress] |
| **Nov WASDE** (released) | **Tue Nov 10** | Corn yield cut 1.6 bu to 179.6 bu/acre; production 15.893bn bu; ending stocks 1.758bn bu (below trade avg 1.846bn). Soy yield 53.3, production 4.574bn bu, ending stocks 300m bu (vs 332m expected). Cotton cut to 13.18m bales. | Already digested; grains mostly higher last week after it. Next WASDE is December (routine demand adjustments expected per Allendale); next yield final is the Jan 12 annual summary. [FACT — USDA WASDE-677 via Oklahoma Farm Report/Allendale] |
| **OPEC+ ministerial meeting** | **Sun Nov 29** | Full 21-member meeting to set 2027 quotas, using the independent capacity assessment **completed today, Nov 17** (DeGolyer & MacNaughton / Shri Chandra) | The big supply-policy date. Dec targets were held at September levels (~31m b/d) on Nov 1; ~2m b/d of cuts still run to end-2026. Individual capacity figures/baselines not yet published. [FACT — OPEC/Reuters via Global Banking & Finance; WiseVoter Nov 17] |
| **NOPA crush** (released) | **Mon Nov 16** | October soybean crush **234.2m bu — new all-time high**, above avg trade estimate 225m bu | Bullish soybean demand signal; supports crush margins. [FACT — NOPA via Archer Financials, Nov 17] |

### Fresh disruptions — last 24–48h

**1. Strait of Hormuz — two confirmed tanker strikes, Nov 16 (FACT, UKMTO).**
- **05:58 UTC Nov 16, UKMTO Warning 207-26:** Panama-flagged tanker *On Phoenix*, outbound through Hormuz ~3nm off Oman, "struck by an unidentified projectile"; engine-room fire; all crew accounted for, no casualties. [FACT — UKMTO via Riviera/Seatrade]
- **~19:00 UTC Nov 16, UKMTO Warning 208-26:** second tanker attacked ~7nm north of Khasab, Oman — identified as Panama-flagged LPG carrier *Tara Gas* (25 crew, 24 Indian nationals); disabled, engine-room fire. **Nov 17 update: a second strike hit the same vessel, another fire; 24 crew evacuated ashore at Khasab, one seafarer missing, search ongoing.** [FACT — UKMTO via Safety4Sea, Nov 17]
- **Nov 15 (prior day):** VLCC *Al Dhannah* (ADNOC-managed) attacked in the Arabian Gulf approaching Hormuz, struck in steering-gear room, returned toward Dubai; crew safe. [FACT — UKMTO via Indian shipping authorities, Seatrade]
- **UNVERIFIED / do not use:** IRGC claims that two tankers struck mines Nov 16 and that a VLCC sank — no vessel named, no independent verification; Reuters could not verify; UKMTO used "projectile"/"attack," never "mine." [UNVERIFIED — Iranian state media via Reuters/Seatrade]
- **Context (FACT):** EIA Global Energy Security Data, released Mon Nov 16, put Hormuz oil flows at **9.1m b/d in Q3 2026** (vs ~20.9m b/d H1 2025 per EIA chokepoint data, and ~10.5m b/d tanker transits since early Oct per Kpler via Reuters). JMIC Advisory Update 114 (Nov 15) rated Hormuz threat **severe** but recorded continuing passages (~28 US-facilitated transits/day Nov 12–14). IMO: 131 confirmed incidents near Hormuz Feb 28–Nov 9; October (35) the worst month. War-risk insurance quoted 3–10% of hull value vs ~0.25% pre-war. [FACT — EIA; JMIC via Asymmetric Analytics; IMO via Logistics Material]
- **Bab el-Mandeb (FACT):** Yemen's Southern Armed Forces announced Nov 15 redeployment away from Dhubab airfield / Bab el-Mandeb to defend Aden — assessed as increasing Houthi opportunity to threaten the southern Red Sea entrance. JMIC recorded only 67 commercial passages Nov 12–14 (~22/day vs ~61/day 2023 reference). **Counter-trend:** Suez container transits passed 50% of pre-disruption levels in Oct; Evergreen resumed Suez voyages Nov 7; Maersk/Hapag-Lloyd restoring selected services. [FACT — JMIC/Asymmetric Analytics; BIMCO via Logistics Material, Nov 13]

**2. Kerch Bridge — road arch collapsed into the shipping canal, Tue Nov 17 (FACT).**
- Ukraine struck the bridge a second straight day; the main road arch and a road span collapsed into the Kerch-Yenikale Canal — the only deepwater channel between the Sea of Azov and the Black Sea — blocking navigation. Rail section still standing (damaged arch); rail traffic resumed Tue after a brief pause. No official Russian confirmation of damage extent; Kremlin says it will be restored. [FACT — Reuters via BusinessDay/WNCY, Nov 17; Ukraine General Staff]
- **Grain relevance:** SovEcon's Andrey Sizov: the collapse could "substantially delay any eventual resumption of shipping from the Sea of Azov," as debris must be cleared. Caveat: shipping there has been suspended since July 2026 over drone strikes, so this delays a *resumption*, not current flows. [FACT — SovEcon via Reuters/Military.com]
- **Market response (FACT):** Dec CBOT wheat **+1.4% Tue to $5.95¼**; March Chicago SRW $6.1025 (+9.25¢), KC HRW $6.4450 (+15.25¢). Dec corn −0.4% to $4.46¾; Jan soybeans −0.3% to $12.25½. [FACT — Morningstar/Dow Jones, Nov 17 15:43 ET]

**3. IEA surplus call — the dominant price driver (FACT).**
- IEA (Fri Nov 13): global oil market returns to **surplus in Q4 2026** as Middle East exports recover faster than demand; Oct supply +2.3m b/d to 105.4m b/d; Q4 surplus ~1.7m b/d. [FACT — IEA via Reuters/TalkMarkets]
- Goldman Sachs: Brent to average **$88 in 2027, falling to $78 by Dec 2027** as the market returns to surplus. [FACT — Goldman via CNBC/FinanceFeeds, Nov 17]

### Futures-curve read (what is verifiable)
- **Crude (front month, FACT):** Brent **$91.62–91.66 Tue ~04:30–07:20 GMT, −0.8/−0.9%**, after Mon's −3.6% slump to a $92.44 settle; WTI **$84.89–84.99, −0.9%**. Prices later recovered intraday — Brent ~$93.33 / WTI ~$86.45 by Tue evening per a Yahoo-sourced aggregator — so the morning print is a snapshot, not the close. [FACT — Reuters via multiple outlets; late-day levels: nabdmal/Yahoo Finance, timestamped Tue 20:44 — secondary source, treat as indicative]
- **Net read (INFERENCE):** the curve is pricing recovering Gulf supply and a Q4 surplus over the Hormuz attack premium — two confirmed tanker strikes in 24h did not hold prices up. That is a market judgment, not a fact about supply; a strait closure would reprice it instantly.
- **Term structure (contango/backwardation): UNVERIFIED** — no verified deferred-contract spread obtained in this sweep; do not infer curve shape from front-month levels alone.
- **Natural gas (FACT):** NYMEX front month **~$3.06/MMBtu Tue morning, −2%, third straight down session** as the weekend cold spell eases; later ~$3.18 (+1.8% on the day per Yahoo-sourced live quote). [FACT — Dow Jones/Morningstar 09:23 ET; NowPrice/Yahoo]
- **Grains (FACT, Tue settlements):** Dec corn $4.4675 (−2¢); Jan soybeans $12.2550 (−3.5¢); March wheat sharply higher (see above). CFTC (week through Nov 11): money managers extended corn net short to **62,311 contracts** (largest in 5 months, +39,411 w/w); CBOT wheat net short cut to 88,729. [FACT — Feedstuffs, Nov 17]
- **EIA STEO (Nov 10, FACT):** US crude output averaging **13.99m b/d in Q4 2026** (weekly prints already hit 14.01m b/d w/e Nov 6 and 14.00m b/d w/e Oct 30); forecast **14.3m b/d in 2027**; US crude inventories forecast to rise in 2027 (416m bbl end-Jan to 444m bbl end-Dec). [FACT — EIA STEO via Rigzone, Nov 17]

### What would change this read
- EIA Wed 10:30 ET: a second consecutive all-products build would reinforce the surplus narrative; a draw (esp. distillates, still 8% below 5-yr avg) would cut against it.
- Any Hormuz closure, additional confirmed strikes, or a US/Iran escalation headline — the market is currently discounting the attacks; that discount is fragile.
- OPEC+ Nov 29: 2027 quotas + handling of the ~2m b/d of cuts expiring end-2026.
- USDA Export Sales Thu 8:30 ET for grain demand confirmation.

**Sources:** eia.gov (WPSR Table 1, week ending Nov 6; STEO Nov 10); api.org (WSB schedule); USDA NASS Crop Progress Nov 16 via DTN/Farm Progress; USDA WASDE-677 Nov 10 via Oklahoma Farm Report; IEA via Reuters Nov 17; UKMTO Warnings 207-26/208-26 via Riviera, Seatrade, Safety4Sea; JMIC Advisory 114 via Asymmetric Analytics; Reuters via BusinessDay/WNCY (Kerch); OPEC/Reuters via Global Banking & Finance; NOPA via Archer Financials; CFTC via Feedstuffs. All as-of Tue Nov 17, 2026.

---

## 6. Box / Parity Observer

**Nothing material found today.**

Checked: web sweep for new put-call parity / box-spread violation analysis and for S&P Dow Jones index-methodology news (as of ~13:30 PT, Nov 17). What surfaced was either generic educational material (put-call parity primers, undated or months old), a crypto-venue arbitrage scanner (Optionly, Deribit/Derive — best break SOL Mar 2027 reversal, $2.22/contract; not watchlist-relevant), or routine items — no new published parity-violation analysis on SPY/QQQ or watchlist names, and no new index-methodology document issued today.

Standing watch item, no new development (FACT, sources below): S&P Dow Jones Indices' growth/value methodology revamp, announced Oct 23, 2026 — removes 12-month price momentum from growth ranking, adds free-cash-flow-to-price and intangible-adjusted book value to value screens — takes effect at the annual reconstitution before the open Dec 21, 2026, with preliminary files Dec 4; Bloomberg Intelligence estimated ≥$375B in passive funds tied to the affected gauges. Sources: https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/ and https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing. Relevance is index-composition, not parity: no change to the deterministic parity math (C − P = S − Ke^(−rT)) or to box-spread pricing on watchlist names. No action; next check is the Dec 4 preliminary files.

No desk-relevant parity violation to report; no numbers unverified beyond the above.

---

## 7. Bonds & Rates desk (Desk 7 — consolidated deliverable)

**Method note (FACT):** the repo's `rates_desk.rates_environment()` ran clean this session (mode `REAL_FRED_RATES`, FRED public CSV, HTTP 200, as-of 2026-11-17) but returns the rates environment only — it contains no core-indicator function, so the 10 indicator series were pulled this session through the same module's `fred_series_rows` FRED transport (script `/tmp/desk7_pull.py`, output `/tmp/desk7_pull.json`). No numbers below are retyped from memory or from the Nov 13 snapshot; unchanged reads are verified unchanged by today's pull, not carried forward blindly.

### Rates table (FRED daily, as of Mon 2026-11-16)

| Series | Read | vs Fri 2026-11-13 |
|---|---|---|
| Effective fed funds (DFF) | 3.88% | 0.00 over the 60-day window (FACT) |
| 2Y Treasury (DGS2) | 4.83% | 4.88% → −5bp |
| 10Y Treasury (DGS10) | 5.12% | 5.15% → −3bp |
| 2s10s slope | +29bp, UPWARD_SLOPING | +27bp → widened +2bp (both legs fell; the front end fell faster) |
| SOFR | 3.93% | — |
| EFFR / OBFR | 3.88% / 3.88% | — |
| **SOFR − EFFR funding spread** | **+5bp** | No funding stress: a 5bp term-premium gap is normal, not a dislocation (INFERENCE) |

Target range 3.75–4.00% after the Oct 10–2 hold (FACT, federalreserve.gov via consolidated doc). Yields eased off Friday's highs but remain ~14bp above the Nov 10 anchor (10Y 4.98%) — the hiking repricing has not reversed (INFERENCE).

### Core-indicator table (all pulled this session, FRED unless noted)

| Indicator | Trigger rule | Today's read | Score | Broker POV — discount rate / margin of safety |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA) | HIKE if y/y > 2.5% or m/m > +0.25% | y/y +3.121%, m/m +0.317% (130.902, Sep 2026) — **no new print since Nov 13**; Oct print due Nov 25 (provisional) | HIKE | Anchor the discount rate to the higher regime. The decision variable is PCE, not CPI; nothing re-anchors before Nov 25. |
| Breakevens (T5YIE / T10YIE) | HIKE if > 2.75%; NEUTRAL 2.0–2.5% | 2.25% / 2.20% (Nov 16) — down from 2.31% / 2.24% (Nov 12) | NEUTRAL | Anchored expectations = no credibility crisis; room for 25bp, not a forced 50bp. Tripwire remains a break above 2.75%. |
| Michigan expectations (MICH, U-M) | HIKE if yr-ahead > 3.5% | **4.3% yr-ahead, Nov prelim (rel. Nov 6)** — FRED MICH still lags at Sep 4.6%; the 4.3% is the manual U-M marker, unchanged since Nov 13 | HIKE | Do not average with breakevens: 4.3% vs 2.20% is a credibility gap the Fed reads as pressure to act. The fall from 4.7% narrows it; the level still fires. |
| Payrolls, 3-mo avg (PAYEMS, BLS) | HIKE if > +150k; CUT if < +50k | 3-mo avg **+137k** (Jul→Aug +186k, Aug→Sep +60k, Sep→Oct +165k; Oct level 159,293k) — unchanged from Nov 13 | NEUTRAL | Rule as written: NEUTRAL. The +165k October print alone does not override the average — one print is noise, the average is the signal. |
| Initial claims, 4-wk avg (ICSA, DOL) | CUT if > 300k; NEUTRAL < 250k | 200k w/e Nov 7; 4-wk avg **195,250** — unchanged; next print (w/e Nov 14) due Thu Nov 19 | NEUTRAL | No action. Check every Thursday: a 4-wk avg above 300k flips the labor read to CUT before payrolls confirm. |
| Job openings (JTSJOL, BLS) | HIKE if 3-mo change positive | 7,523k, Sep 2026 (Jul 7,335k, Aug 7,190k) — no new print | HIKE | Demand has not rolled over: rules out the "labor is cracking" case for a hold. Corroborates payrolls rather than replacing them. |
| Real GDP (GDPC1, BEA) | HIKE if > 2.5% ann.; CUT if < 1.0% | Q3 **+3.37% annualized** (Q2 +2.22%) — no new print | HIKE | Above-trend growth removes the "restraint is biting" objection to a hike. Growth is backdrop, not trigger. |
| Housing starts (HOUST, Census) | CUT if −5% over 3 mo | 1,221k; **−10.8% Jul→Sep** (Sep 2026) — no new print; Oct starts due ~Nov 19 | CUT | Report it, don't bury it: the evidence a hold argument would cite, and why the call is 25bp, not 50bp. |
| High-yield OAS (BAMLH0A0HYM2) | CUT if > 5.00%; NEUTRAL < 4.00% | **3.34% (Nov 16)** — up from 3.20% (Nov 12), still well inside NEUTRAL | NEUTRAL | No credit stress; the market is neither doing the Fed's tightening work nor forcing easing. Watch a break above 5.00%. |
| FOMC vote & guidance | HIKE if dissents favor tightening | Oct 28: held 3.75–4.00%, **10–2, Cook + Hammack dissenting for +25bp**; statement: "Inflation remains elevated." | HIKE | Weight the vote above any single print. **Minutes land tomorrow, Wed Nov 18, 2:00 PM ET — pending catalyst; the check on whether 10–2 understates division.** |

**Tally: 5 HIKE / 1 CUT / 4 NEUTRAL — unchanged from Nov 13.** No kept indicator printed new data this session except breakevens, HY OAS, and the yield curve (all small moves, no trigger flips).

### Market pricing vs the indicator read

**Kalshi, direct API pull this session (~13:30 PT Nov 17, Dec-2026 meeting `KXFEDDECISION-26DEC-*`):**
- 25bp hike: **$0.91** (bid/ask 0.90/0.91, prev 0.90; 24h vol 80,563) — up from $0.88 on Nov 13.
- More than 25bp: **$0.04** (0.04/0.05, prev 0.06; 24h vol 137,792) — **collapsed from $0.12 on Nov 13**.
- Hold: $0.05 (prev 0.05) — up from $0.03. 25bp cut / >25bp cut: $0.01 each.
- Total hike $0.95 (was $1.00); the five lasts sum to $1.02 (2-cent over-round, was 5 cents).
- (FACT) **The 50bp tail repriced down two-thirds in four days while the 25bp price firmed — the market now prices size as 25bp, not 50bp.**

**CME FedWatch — secondhand only (FACT: CME's tool could not be read directly; no public text API):** reads converging Nov 16–17 at **92.7–97.5% for 25bp** (growbeansprout.com, citing CME as of Nov 17: 97.5%; bitcoinsistemi citing CME FedWatch Nov 17: 92.7% 25bp / 7.3% 50bp; TheStreet ~93%; Binance/Jin10 Nov 16: 95.7% / 4.3%). **Disagreement named:** Kalshi's >25bp tail ($0.04) now sits *below* the FedWatch 50bp range (4.3–7.3%) — the two venues agree on direction and on 25bp as the base case, and disagree only on how much tail to leave on 50bp. The remaining indicator-vs-market gap is unchanged: the indicator set votes direction (hike), not size.

**Fed speak (FACT, press-reported, single-basis):** St. Louis Fed President Musalem said Nov 17 in Buenos Aires that multiple hikes may be needed before spring 2027 and the real policy rate should reach 2–2.5% by spring 2027; Governor Waller has said a 50bp hike should be considered in December if inflation stays hot (TheStreet, Nov 16). Speakers today Nov 17: Waller 9:10 AM ET, Hammack 9:30 AM ET (Brookings), Williams 2:25 PM ET (Kalkine). These are hawkish-leaning statements consistent with the HIKE tally, not new data (INFERENCE).

### Verdict

- **Thesis:** 25bp hike on Dec 9, to 4.00–4.25%. Core PCE (3.12% y/y) is above target with no labor deterioration, above-trend growth, and a 10–2 vote with two hike dissents. (INFERENCE from the FACTs above.)
- **Evidence:** tally 5/1/4 unchanged; Kalshi total hike $0.95 with 25bp at $0.91; FedWatch secondhand 92.7–97.5% for 25bp; 2s10s +29bp upward-sloping; SOFR−EFFR +5bp (no funding stress).
- **What changed since Nov 13:** only the size tail — Kalshi >25bp $0.12 → $0.04 — which *strengthens* the 25bp call and weakens the 50bp tail. Direction confidence is higher; size confidence is now higher too, on the market side. The indicator set still cannot distinguish 25bp from 50bp on its own.
- **What would change it:** Oct core PCE Nov 25 (m/m ≤ +0.15% with a downward Sep revision); claims 4-wk avg above 300k; **Nov 18 minutes** or a named speaker arguing for a hold, showing the Committee more worried about overtightening than 10–2 suggested. November CPI lands Dec 10, after the decision, and cannot change December (FACT, date single-basis).

### Graham lens (arithmetic, not opinion)

- 10Y 5.12% (Nov 16) vs 5.15% (Nov 13) vs 4.98% (Nov 10 anchor). At assumed perpetual growth g = 3.00%, Gordon multiple 1 ÷ (r − g): **47.17x** now, vs 46.51x Nov 13 (+1.4% as yields eased 3bp), vs 50.51x at the Nov 10 anchor (−6.6% since Nov 10). Duration ≈ 8 puts the 3bp yield decline at ≈ +0.24% on a 10-year position (approximation; ignores convexity).
- Margin of safety is still ~6–7% thinner than at the Nov 10 anchor on this sensitivity: any intrinsic-value estimate carried at 4.98% overstates value. Re-anchor to 5.12%.
- Earnings-yield vs bond-yield spread: UNVERIFIED (bond side verified at 5.12%; no primary-source earnings yield pulled this session). No live spread asserted.
- Defensive read: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price — a wider required discount, not a chase for yield.

**Desk status:** COMPLETE. No failures. One method note: `rates_environment()` does not compute the 10 core indicators (no such function exists in the module) — they were pulled this session via the module's own FRED transport; the task brief's description of the module is inaccurate on that point. Nothing UNVERIFIED except the earnings-yield spread and the direct CME FedWatch read (secondhand range given instead).

---

## Run notes

- **Desk status:** all seven desks delivered. No desk FAILED. Earnings desk recorded two failed exec calls during its pull (subprocess nonzero exits) but recovered and delivered a complete section; the NVDA print was incorporated from corroborated secondary sources citing the company release/8-K — the release text itself was not read in full, so a statement teardown is still owed.
- **IV-inputs freshness:** `~/workspace/hedge-desk-research/nightly/2026-11-16-iv-inputs.json`, as_of 2026-11-16T14:54:31-07:00 (~22.5h old at run start — within the 26h guard, STALE-labeled). ATM IVs in the file all null (eighth straight null pull); live Yahoo pull this session recovered ATM IV for all six symbols.
- **Quant Lab ledger:** rows #292–#297 appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (now 296 rows).
- **Cross-desk reconciliation:** NVDA implied move — Earnings desk straddle ±8.1% vs Premium desk IV-scaling ±8.6%; same move by two methods, 0.5pt gap is method, not a conflict. NVDA after-hours +2.20% sits well inside both. Desk 7's 25bp call and the Premium desk's "avoid NVDA premium into the binary" are consistent (the binary has now resolved). Hormuz disruption (Desk 5) vs Desk 7's no-funding-stress read: different markets (oil vs USD funding), no contradiction.
- **Standing items carried:** Nov 5 crash day still 37–54% of 20-day realized variance — all IV-vs-realized verdicts WINDOW-CONTINGENT until it ages out after Dec 3. ATM IVs null a seventh straight pull in the nightly file (eighth counting this file) — the live pull this session broke the streak, expiry-calendar-driven. IV rank UNVERIFIED (no free IV history). FOMC minutes Nov 18, 2:00 PM ET. EIA weekly Nov 18, 10:30 ET. MSFT ex-div Nov 19. Oct core PCE Nov 25 (provisional).
