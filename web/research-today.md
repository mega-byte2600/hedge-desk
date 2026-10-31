# Hedge-desk daily research — Sat 2026-10-31

**Run:** scheduled 13:30 PT run, all seven desks reported, synthesized ~13:45 PT. No desk dropped, no retry needed. Markets closed for the weekend; all market marks below are Fri Oct 30 closes unless labeled otherwise.

**Standing labels:** FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it. Paper-only research; no trade authorization; no Risk of Ruin contact.

**Source-reliability note — Nasdaq calendar, partial recovery:** yesterday's run found the Nasdaq earnings calendar inconsistent across desks (zero rows for Nov 2–13 on one pull, AAPL Nov 2 present on another). This run's Earnings desk day-by-day sweep (Nov 2–6, 9–13) DID return AAPL Nov 2 (time-after-hours) and NVDA Nov 17, corroborated by company announcements — so those two dates are carried as confirmed, not calendar-only. The calendar is still not treated as sole confirmer for any date.

**Correction to this run's coordinator brief (recorded, not hidden):** the brief told desks the Oct 30 IV-inputs file had an empty symbols dict. The Premium desk read the file and corrected it: `atm_iv` is null for all six symbols (fail-closed on the dead Oct 30 expiry), but the realized-vol block, variance shares, and earnings dates are intact. The package below reflects the file as actually read.

## Market backdrop (Fri Oct 30 closes, per the Oct 31 Yahoo pull)

| Symbol | Oct 29 close | Oct 30 close mark | Change (recomputed) |
|---|---|---|---|
| SPY | $769.36 | $755.72 | −1.77% |
| QQQ | $715.34 | $690.49 | −3.47% |
| AAPL | $348.91 | $344.63 | −1.23% |
| MSFT | $530.14 | $521.91 | −1.55% |
| NVDA | $213.66 | $204.64 | −4.22% |
| TSLA | $403.30 | $399.81 | −0.87% |

Note on SPY: yesterday's package showed an indicative post-close SPY mark of $753.38 that drifted to $755.47 between pulls minutes apart (non-synchronous post-close artifact, documented Oct 30). Today's $755.72 is the settled-close mark from the Oct 31 pull — use it, not the $753.38 indicative mark. The week ends with growth/QQQ beta leading down (NVDA −4.2%, QQQ −3.5% on the day) [INFERENCE from the closes + §5 catalysts].

## 1. Earnings Event Desk

Window: Nov 1–14, 2026. SPY/QQQ are ETFs — no earnings.

| Symbol | Status | Report date / timing | Options-implied move | Historical earnings-day move |
|---|---|---|---|---|
| **AAPL** | **Upcoming — the window's only watchlist binary** | **Mon Nov 2, 2026, after close** — results ~1:30pm PT, call 2:00pm PT | **~4.25%** (live Nov 4 ATM $345 straddle $14.66 / $344.63, Yahoo v7 chain pulled Oct 31) | ~2% typical next-day move over past 8 quarters (Saxo Bank note via FXBrokerTrust, Oct 28 — secondary source, not recomputed) |
| MSFT | Already reported | Wed Oct 28 AMC (FY27 Q1) | — | Context only, secondary-source figures (not release-verified this run): revenue $92.3B, Azure +48%, GAAP EPS $4.92 |
| TSLA | Already reported | Wed Oct 21 AMC (Q3 2026) | — | Context only, secondary-source figures (not release-verified this run): revenue $28.05B, GAAP EPS $0.22, FCF $1.53B |
| NVDA | Outside window — flag now | **Tue Nov 17, 2026, AMC** (FY27 Q3) — company-confirmed | Not computed (outside window) | — |

- **AAPL date (FACT, corroborated):** Nasdaq calendar lists Nov 2 time-after-hours; Apple's own IR schedule (via MacRumors, Oct 6) confirms Nov 2, results 1:30pm PT, call 2:00pm PT. Fiscal Q4 2026 (Jun 28–Sep 26), covering launch-week iPhone 18 Pro sales. Company guide as reported (Zacks, Oct 29): revenue growth 9–11% YoY, gross margin 47–48% incl. ~1pp tariff-refund benefit; consensus revenue $112.95B (+10.2% YoY), EPS $1.98 (+7% YoY).
- **INFERENCE:** implied ~4.3% is roughly double the reported ~2% typical move — the options market prices an outsized reaction (holiday-quarter guide + first Ternus-led call + tariff-refund margin benefit are the plausible drivers). Per the standing rule, premium into this binary event = avoid; the elevated straddle is compensation for event risk, not a mispricing on its own.
- **Verdict:** AAPL Nov 2 is the week's binary-event risk for the watchlist. **What would change this:** the Nov 2 release itself, read in CFA order (guide vs consensus first, then GAAP statement vs headline adjusted figure, then cash flow, segment margins, balance-sheet deltas; call transcript last). A guide miss vs 9–11% revenue growth, or a GAAP-vs-adjusted gap, reframes the reaction more than the print itself.
- Sources: Nasdaq earnings calendar API (queried Oct 31, day-by-day Nov 2–6, 9–13); Yahoo v7 AAPL options chain (Oct 31 pull, cookie+crumb); Apple IR via https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/; Zacks preview Oct 29 https://www.zacks.com/stock/news/3018992/apples-q4-earnings-loom-buy-or-sell-aapl-stock-ahead-of-results; Saxo note via https://www.fxbrokertrust.com/insights/apple-q4-earnings-options-43-implied-move-term-structure.

## 2. Dividend Opportunity Desk

Window: ex-dates Nov 1–28, 2026. As of Sat Oct 31 ~1:45pm PT.

| Symbol | Ex-date | Amount | Declared | Payable | Flag |
|---|---|---|---|---|---|
| **MSFT** | **Thu Nov 19, 2026** | **$0.98/qtr** | Sep 15, 2026 | Dec 10, 2026 | **Increase** — up from $0.91 (+7.7%); **24th consecutive annual increase** per the desk count standard (count increments on announcement date, not payment date) |
| AAPL | — none declared — | — | — | — | Last ex Aug 10, 2026 ($0.27, declared Jul 30); Nov ex-date pattern-plausible (Monday cadence: Feb 9, May 11, Aug 10 → Mon Nov 9) but **UNVERIFIED** until declared; third-party "Nov 10, $0.27" listings are projections, not declarations |
| SPY | — none — | — | — | — | Last ex Sep 18, 2026 ($1.889); next quarterly ex mid-December, outside window (timing = INFERENCE) |
| QQQ | — none — | — | — | — | Last ex Sep 21, 2026 ($0.751); next quarterly ex mid-December, outside window (timing = INFERENCE) |
| NVDA | — none — | — | — | — | Last ex Sep 10, 2026 ($0.25, declared Aug 26); next declaration normally with earnings (~Nov 17), early-December ex-date, outside window |
| TSLA | — none; pays no dividend — | — | — | — | No dividend program |

- **Flags:** Announced increases: MSFT only. Cuts: none. Specials: none. (FACT, Nasdaq + Yahoo cross-check.)
- **Data quirk (FACT):** Nasdaq's MSFT header still shows annualized $3.64 (4 × old $0.91); forward annualized at $0.98 is $3.92 by arithmetic — do not quote $3.64 as the forward rate.
- **Options-relevant mechanic (FACT):** MSFT's ex-date falls Thu Nov 19, so the last purchase day for entitlement is Wed Nov 18, 2026.
- **INFERENCE (capture note):** MSFT Nov 19 is the only actionable capture date in the window, but the $0.98 has been public since Sep 15 — no information edge attaches to the ex-date itself.
- **What would change this section:** an AAPL board declaration (typically accompanies the earnings cycle — re-check Nasdaq AAPL history before Monday's open); an NVDA early declaration pulling its ex-date into late November (cadence does not suggest it).
- Sources: Nasdaq dividends API (per-symbol histories + calendar Nov 10/13/19); Yahoo v8 chart dividend events; Zacks AAPL dividend history (updated Oct 29–30, "does not have any future dividends declared"); count standard ~/workspace/hedge-desk-research/dividend-count-standard.md.
- **Verdict:** One declared ex-date in the window: MSFT Nov 19, $0.98, raised rate, 24th consecutive annual increase.

## 3. Overnight Premium Desk (IV)

**Market state:** Saturday Oct 31 — all option quotes are Fri Oct 30 close marks pulled live from Yahoo on Oct 31 at 13:30 PT, NOT live Saturday prints. Paper-only research.

### Input-file status (read, not assumed)

- `~/workspace/hedge-desk-research/nightly/2026-10-30-iv-inputs.json`, **as_of 2026-10-30T13:54:06−07:00** (~23.5h old at run start, inside the 26h freshness guard) — **ATM IV effectively MISSING by name**: `atm_iv` is null for all six symbols (13:54 PT pull ran after the Oct 30 expiry died at 16:00 ET; Yahoo's post-expiry marks were solver residuals on dead contracts and the pull correctly failed closed). The file's realized-vol block is intact and is used for comparison only, labeled Oct 30 vintage.
- **Fallback used (labeled):** live Yahoo v7 options-chain pull, Oct 31 13:30 PT, cookie+crumb handshake. Only **tradeable expiries (Nov 2, 2026 and later)** used; expired Oct 30 contracts excluded. ATM IV = mean of same-strike call/put IV at the strike nearest Friday's close. Friday-close bid/ask spreads were tight (cents to ~$0.55), passing the stale-quote sanity check — with the weekend-staleness caveat below.

### Snapshot — front tradeable expiry (fallback pull, Friday-close marks)

| Symbol | Spot (Fri close) | Front expiry | DTE* | ATM IV (mean) | 2nd expiry ATM IV | Realized 20d (fresh window Oct 5–30) | IV vs realized |
|---|---|---|---|---|---|---|---|
| SPY | 755.72 | 2026-11-02 | 2 | 12.6% | 2026-11-03: 14.4% | 11.6% | ~in line — **WINDOW-CONTINGENT** |
| QQQ | 690.49 | 2026-11-02 | 2 | 20.8% | 2026-11-03: 24.6% | 22.9% | Slightly below realized |
| **AAPL** | 344.63 | 2026-11-04 | 4 | **47.2%** | 2026-11-06: 43.8% | 14.9% | **3.2× realized — earnings hump, AVOID** |
| MSFT | 521.91 | 2026-11-02 | 2 | 23.3% | 2026-11-04: 31.1% | 20.1% | Modestly above realized |
| NVDA | 204.64 | 2026-11-02 | 2 | 31.7% | 2026-11-04: 41.0% | 31.6% | At realized (front); hump further out |
| TSLA | 399.81 | 2026-11-02 | 2 | 33.4% | 2026-11-04: 47.8% | 36.9% | Below realized (front) |

\* DTE in calendar days from Sat Oct 31; Nov 2 expiry is one session (Monday) away. Approximate expected move to front expiry, IV × √(DTE/365) — arithmetic approximation, not a forecast: SPY ~0.9%, QQQ ~1.5%, AAPL ~4.9%, MSFT ~1.7%, NVDA ~2.3%, TSLA ~2.5%.

### Stale-jump screen (single day >30% of 20-day realized variance ⇒ WINDOW-CONTINGENT)

- **SPY — WINDOW-CONTINGENT (fresh window).** Fri Oct 30 itself (−1.79% log return) drives **32.2%** of the fresh Oct 5–30 window's variance, over the 30% line. The Oct 30 file's window (Oct 2–29, excluding Oct 30) showed 19.7% and was NOT contingent — the verdict flips entirely on whether Friday's selloff is in the window. **Any IV-vs-realized verdict for SPY built on this window is WINDOW-CONTINGENT, not clean.** What would change it: one more session's return diluting Friday's share below 30%, or a window excluding Oct 30.
- **QQQ — not contingent but near the line:** max-day share 29.8% (just under 30%). Treat its IV-vs-realized read as provisional; a small revision could flip it.
- **AAPL 13.1%, MSFT 19.2%, NVDA 24.1%, TSLA 26.1% — not contingent.** Their IV-vs-realized comparisons stand as ordinary reads (subject to the Friday-close caveat).
- Vintage gap: the Oct 30 file's realized vols (window Oct 2–29) were SPY 10.0%, QQQ 20.2%, AAPL 14.0%, MSFT 19.9%, NVDA 30.3%, TSLA 37.3% — close to fresh-window figures except SPY, where Friday's move matters most.

### Term structure and earnings inside the window

- **AAPL — earnings hump, premium into a binary event = AVOID.** Nov 2 earnings sits inside the Nov 4 expiry; front IV 47.2% is 3.2× trailing realized, falling to 43.8% at Nov 6 — the classic front-month hump. Elevated IV with an event inside the window is expected, not "rich": it is event premium, and buying it means paying for a binary outcome.
- **NVDA — earnings hump further out, not in the front expiry.** Nov 17 earnings sits outside Nov 2/Nov 4 but inside Nov 20, where ATM IV is **48.7%** (Nov 13: 40.6%) vs 31.6% realized. Front-expiry premium is not event-inflated; Nov 20 premium is. Same binary-event rule applies to Nov 20.
- **SPY / QQQ / MSFT / TSLA — no earnings inside the front windows.** Term structure rises from 2-DTE to the next expiry for all four, but the cause is **UNVERIFIED** — very short-dated (2-DTE) IV annualizes a single session and is not directly comparable to a 4-DTE print, so no event attribution is made. Yesterday's Nov 3–4 midterm-election event-premium read remains INFERENCE only (see §5 calendar: midterms Tue Nov 3); today's desk declined to attribute the rise without a named catalyst.
- **IV rank: UNVERIFIED for all six symbols.** No free source of IV history was available; no percentile rank is claimed and no symbol is labeled "elevated IV rank." The flags above are IV-vs-realized comparisons only — do not let any downstream summary upgrade them into IV-rank claims.

### Sanity flags (CFA derivatives standard)

- **SPY call/put IV spread 4.2pp (14.7% vs 10.5%) is the widest on the board** (QQQ 3.4pp; MSFT 2.1pp; NVDA 2.0pp; AAPL 1.7pp; TSLA 0.3pp). Same-strike call/put IVs should be close; the 12.6% SPY mean blends two disagreeing legs — treat as approximate, not precise. This alone is NOT a put-call parity violation (parity is a price relation needing rates and dividends, not an IV equality), and no parity violation is asserted.
- **Parity rule applied:** no model output used; every number is a published Yahoo mark or arithmetic on one. Where Yahoo's solver and the desk's rule disagreed (dead-expiry residuals), the fail-closed treatment stands.
- **Weekend staleness:** Friday-close spreads were tight, but Monday's open can gap the underlying away from these strikes. Re-pull Monday premarket before acting on any level here.
- Sources: Yahoo v7 options chains (cookie+crumb, Oct 31 13:30 PT); Yahoo v8 chart closes (realized vol, fully-closed bars only); nightly file above; technique standard ~/workspace/custom-skills/local-cfa-financial-analysis/references/derivatives_options.md.

### Desk verdicts

1. **AAPL: AVOID long premium into Nov 2 earnings** — 47.2% front IV is event premium, not mispricing. Changes if: earnings date moves out of the Nov 4 window or Monday quotes crush the hump.
2. **NVDA Nov 20: AVOID as event premium** (48.7% into Nov 17 earnings); front expiries ordinary. Changes if: earnings date moves or Monday quotes reprice Nov 20.
3. **SPY: no clean IV-vs-realized verdict — WINDOW-CONTINGENT** on Friday's −1.79% driving 32.2% of fresh-window variance. Changes if: the window rolls past Oct 30 or Monday's return dilutes its share below 30%.
4. **TSLA front IV (33.4%) sits below trailing realized (36.9%)** — the only name where front premium prices below what the last 20 days delivered. A fact about the two prints, not a "cheap" call: realized is backward-looking and the window is not contingent (26.1%).
5. **IV rank for every name is UNVERIFIED.**

## 4. Open Quant/AI Model Lab

**Sweep window:** arXiv q-fin through Oct 29 (Oct 30 submittedDate filter returned 0 hits — not yet announced/indexed; the no-filter control is the evidence, not a leg failure) and GitHub repos created Oct 30–31. All scores from the repo's own scorer (`hedge_desk.research_intelligence.assess_source`, run this sweep — no hand-scoring). No candidate reached TEST or INTEGRATE. All 9 new candidates appended to the ledger as #188–#196 (verified present after prior row #187).

**Evidence labels (per evidence_standards.md):** README/tree contents verified via GitHub API are FACT; every headline result below is source-reported and UNVERIFIED (code NOT run in this sweep — sandbox runs are the follow-up, not this sweep).

| # | Candidate | Source | Score | Disposition | Reason |
|---|---|---|---|---|---|
| 188 | siddhardhad17/option-pricing-lib — C++17 BSM + barrier pricers, Greeks, MC variance reduction, SVI calibration + no-arb checks, zero deps | https://github.com/siddhardhad17/option-pricing-lib | 52 | WATCH | MIT, tests/ + CMake, closed-form-benchmark claims (benchmarks UNVERIFIED, code not run). SVI + arb-check differentiators vs #186, but pricing lane is crowded and pinned (#33/#121/#106), no live chain shown. |
| 189 | rabeeka-m/financial-volatility-regime-detection — CUSUM, audited PELT, Markov-switching regime comparison | https://github.com/rabeeka-m/financial-volatility-regime-detection | 55 | WATCH | MIT, tests/ + synthetic benchmarks + configs (FACT). CAVEAT (README-stated): historical manuscript and financial data remain private — real-data findings NOT reproducible from the repo; only synthetic benchmarks are. Private-data cap blocks TEST. |
| 190 | NaiL00ng/stock-volatility-midas-epu — MIDAS EPU correction to HAR/GARCH/XGB vol forecasts, three markets | https://github.com/NaiL00ng/stock-volatility-midas-epu | 58 | WATCH | Apache-2.0, code + data + results + revision doc (FACT). Honest mixed result, source-reported/UNVERIFIED: DEC lowers QLIKE vs XGB controls on all three markets but RAISES MSE, and does not improve CSI300 interval quality; EPU real-release vintage + fresh holdout still missing. Top of this run's band; value is the ablation discipline, not the headline. |
| 191 | abhishektotre/dl-lstm-recurrent-stock-trend-forecaster-v2 — LSTM trend forecaster, synthetic telemetry | https://github.com/abhishektotre/dl-lstm-recurrent-stock-trend-forecaster-v2 | 25 | ARCHIVE | MIT but 'Day 28' series installment, synthetic-data demo, no tests/ dir. No desk procedure, no verifiable claim. Band discipline. |
| 192 | VineedMindForge/RiskForge — Streamlit market-risk platform (VaR/ES, portfolio construction, vol modelling) | https://github.com/VineedMindForge/RiskForge | 31 | ARCHIVE | MIT, yfinance ingestion with a no-auto-interpolation note (FACT), but no tests/ dir and no desk procedure — generic risk dashboard, not a vol forecast, surface, purged-WF input, or futures catalyst. Band discipline. |
| 193 | AndrewFSee/market-compass — Streamlit hub: regime gauges, breadth, credit, macro, vol/tail dashboards | https://github.com/AndrewFSee/market-compass | 52 | WATCH | MIT, tests/ + modules + nightly jobs (FACT). Value is vol-regime/market-context dashboards from public data. CAVEAT: Claude-powered analyst brief pipeline is LLM-generated text with no stated verification discipline — brief text is never desk evidence. |
| 194 | ilyaeis/monte-carlo-finance — MC study project: GBM paths, option pricing vs BS, variance reduction, GARCH, VaR | https://github.com/ilyaeis/monte-carlo-finance | 34 | ARCHIVE | MIT, tests/ + run_all script (FACT), but explicitly RTU coursework; crowded lane (#33/#121/#106/#186) with no desk differentiator (no IV solver, no live chain, no arb check). Band discipline. |
| 195 | tommasozeri/Time-Series-Foundation-Models-for-Commodity-Futures — zero-shot TSFMs (Timestral, TimesFM-3, Chronos-2) vs econometric benchmarks, 15 commodity futures | https://github.com/tommasozeri/Time-Series-Foundation-Models-for-Commodity-Futures | 55 | WATCH | MIT, code + downloaded data + result files (FACT); no tests/ dir. First zero-shot-TSFM benchmark in the futures desk's lane (RV + 1-day VaR tasks, daily forecasts Jan 2024–Oct 2026, source-reported/UNVERIFIED). Sandbox question: does zero-shot TSFM beat the desk's HAR baseline on one desk future before any wider read. |
| 196 | SachiK0thari/options-scout-ai — LangGraph screener: cash-secured puts / LEAPS, sized to buying power | https://github.com/SachiK0thari/options-scout-ai | 49 | WATCH | MIT, tests/ + evals/ + PRD + PRIVACY (FACT); never trades, never connects to a brokerage (README-stated). BOUNDARY: a candidate-selection screener is NOT a desk signal — the desk never proposes trade authorization. Transferable item is the tested-computation + explicit-risk-limit pattern only. |

Numbering follows the ledger exactly (rows #188–#196).

**Triage exclusions (no ledger rows):** arXiv Oct 26–29 scope misses (agentic wealth-management liquidation fragility, MBS negative convexity, queue-sensitive market-impact calibration, LLM evaluation on underspecified queries, mean-field-games LOB trading, healthcare-equity LLM rankings); GitHub NOLICENSE hits; crypto scope; India scope; noisy options-leg non-quant hits.
**Re-checks:** none this sweep — the Oct 31 kaizen run already re-checked the WATCH/TEST board today (#171 sandbox-verified, moved TEST→WATCH; #173 pushed today; #183 Zenodo code link noted). No TEST/INTEGRATE candidate this run; the run's only TEST remains #171 (sandbox follow-up owned by the weekly job).
**Decision-relevant takeaway:** strongest new item is the MIDAS-EPU vol-forecast study (58) for its honest QLIKE-vs-MSE tradeoff documentation — a cautionary data point for any desk vol-forecast comparison, not an adoption. The zero-shot-TSFM commodity-futures benchmark is the futures desk's first foundation-model benchmark and the only candidate opening a new method family rather than crowding an existing lane.

## 5. Futures Event Desk (Catalysts)

*As of Sat Oct 31 ~1:25pm PT. US futures closed for the weekend — prices are Fri Oct 30 settlements unless labeled otherwise. No new EIA/USDA data was released Oct 31 (weekend). Prior run: 2026-10-30 package; this section covers what is NEW since that run plus the coming week's calendar.*

### Fresh catalysts triaged

**A. Hormuz: new tanker incident Sat Oct 31 AND a live Doha mediation track — FRESH Oct 31 [FACT as reported, several elements UNVERIFIED]**
- UKMTO reported a further attack on an oil tanker in the Strait of Hormuz on Sat Oct 31, near the Iranian island of Lavan; Iran's Revolutionary Guards said the tanker struck a mine after sailing an "unauthorized route." Source: https://themedialine.org/headlines/us-delegation-expected-in-doha-as-iran-qatar-discuss-nuclear-program-strait-of-hormuz/
- Oman's navy rescued 25 crew from a vessel targeted ~122 miles off Musandam Governorate (reported Oct 31). Source: https://en.sababu.mv/world/74480
- **UNVERIFIED:** Attribution for the Oct 30–31 incidents remains unestablished in sourced reporting; IRGC Navy claims (supertanker mine strike, tankers stopped south of the strait) are Iranian state-media claims, not independently confirmed. The US CENTCOM commander said the main recognised shipping lanes had been cleared of Iranian mines and vessels were moving freely — in tension with the new incident reports, so lane status is genuinely contested, not settled.
- **FACT (transit collapse, week ending Oct 28):** UKMTO recorded 122 outbound and 155 inbound Hormuz transits that week, roughly a 70% decline from pre-war levels. Source: https://news.tulsian.ai/news/macro/oil-prices-hit-six-month-highs-amid-hormuz-attacks.html
- **INFERENCE:** The transit count is the hardest physical datapoint in this story: even without a confirmed closure, a ~70% transit decline is a real logistics constriction, not just a risk premium on paper. It supports the prompt-backwardation read better than any single attack headline.
- **What would change this read:** A UKMTO-confirmed halt or reopening of transits, or next week's transit count moving materially in either direction.

**B. US–Iran Doha talks: mediation is live, no deal confirmed — FRESH Oct 31 [FACT as reported / SPECULATION on outcome]**
- Iranian negotiators met Qatari mediators in Doha on Sat Oct 31 after 12+ hours of talks in Tehran on Fri Oct 30; talks coordinated with Washington. US Secretary of State Marco Rubio said Sat that President Trump has not yet decided whether to launch new strikes against Iran. Source: https://www.devdiscourse.com/article/international/4000174-iranian-envoys-meet-qatari-mediators-as-threat-looms-of-us-strikes-after-midterms?amp
- Iranian FM Abbas Araghchi told Al Jazeera on Sat that a US letter (from VP JD Vance) is "a positive step," that Iran sees "no need to meet with the Americans" at this stage, and that a proposal now cuts the implementation period of Iran's Hormuz-reopening plan to two days (from a Qatari-proposed five). Iran's stated conditions: lifting sanctions imposed after the Islamabad memorandum, reduced US forces in the region, restoration of oil waivers, release of frozen funds including funds held in Qatar.
- **UNVERIFIED / SPECULATION:** Qatari newspaper Al-Araby Al-Jadeed's report of preliminary understandings (nuclear steps, Hormuz navigation, financial incentives, China/Russia as guarantors) and of a US delegation joining in Doha is single-newspaper sourcing, explicitly unconfirmed by US or Iranian officials, and contradicted in part by Araghchi's "no plans to meet" statement. Do not treat a deal as done.
- President Trump said Fri Oct 30 the Iran war will end "very soon, one way or the other," with no date or terms given.
- **INFERENCE:** A genuine two-way weekend catalyst: a Hormuz-reopening deal would be the fastest route to premium compression, while a post-midterm (Tue Nov 3) US strike decision would extend it. Monday's open will price whichever signal hardens first.
- **What would change this read:** A joint US–Iran statement, a confirmed direct meeting, or a US strike decision after Nov 3.

**C. Ukraine refinery strikes resume for a second straight day — FRESH Oct 31 [FACT as reported, damage extent UNVERIFIED]**
- Overnight into Sat Oct 31, drones struck the Bashneft-Novoil refinery in Ufa (Bashkortostan, >1,500 km from the front), igniting a fire; geolocation analysis cited by Interfax-Ukraine indicated the catalytic reforming (L-35) unit was likely burning. Follows the Oct 30 Novokuibyshevsk strike that ended the two-week pause.
- **UNVERIFIED:** Extent of production damage at Novoil, and whether a second Ufa facility was also hit, are unconfirmed; Russia's Defense Ministry said it shot down 433 Ukrainian drones overnight but did not detail Ufa. Context (IEA, as cited): Russian refinery processing fell in June to 3.8m bpd, ~30% below a year earlier, with a refinery attacked roughly once every three days on average in Jan–Aug 2026.
- Separately, Zelenskyy and Erdoğan agreed in Istanbul to work on a grain corridor / Black Sea ceasefire discussion, and Rubio spoke of growing interest in a Black Sea ceasefire — but no agreement was confirmed at the reporting cutoff.
- **INFERENCE:** Two refinery strikes in two days confirms the Oct 30 strike was a resumption, not a one-off — the Russian-products tightness leg (distillates, ULSD) has a live supply-side driver again. The Black Sea ceasefire talk is the offsetting upside risk for grain/logistics flows, but prospective only.
- **What would change this read:** Confirmed Novoil outage duration, or a confirmed Black Sea shipping agreement.

**D. Libya pipeline valve shut — small, single-sourced [FACT as reported]**
- Libya's National Oil Corporation reported a disruption after an armed group shut a valve on the main Hamada oil pipeline, halting ~15,000 bpd. **INFERENCE:** 15,000 bpd is immaterial against global supply; a reminder Libyan flows remain fragile, not a price driver. Do not weight it alongside Hormuz.

**E. Natural gas: Dec futures near $2.90, strips at five-year lows — FRESH Oct 30 close [FACT]**
- Dec 2026 Henry Hub fell ~3% on Fri Oct 30 to $2.858/MMBtu (Finimize/LSEG) / near $2.90 (Energy Buyers Guide); balance-of-winter 2026-27 strip $2.93 and Summer 2027 ~$2.71 — both at new five-year lows. Lower 48 output recently bounced to ~113.5 Bcf/d (Oct average 112.1).
- **FACT (weather driver):** NOAA's Oct 28 outlook favors above-normal temperatures across most of the CONUS for Nov 5–11, especially the northern Plains/Upper Midwest; NOAA's Oct 15 seasonal outlook favors a warmer-than-normal northern tier through Feb 2027 (strong El Niño influence). AGA notes the week ending Oct 24 ran 17.5% warmer than the 30-year normal on a gas-weighted heating-degree-day basis.
- European contrast: Dutch TTF traded above €100/MWh on Oct 30 (highest since Dec 2022) on colder near-term European forecasts — the US/Europe gas gap is widening, not narrowing.
- **INFERENCE:** Gas prices a warm start to heating season plus rising output — the mirror image of crude. The five-year-low winter strip says the market is not paying for winter scarcity even with the Hormuz/LNG backdrop; a cold shift is the only fast repricing trigger.
- **What would change this read:** The Nov 5 storage report (week ending Oct 30; five-year-average injection for that week is 61 Bcf) or a cold revision to NOAA guidance.

**F. Grains: no new weekend data; harvest pace is the operative baseline [FACT, Oct 26 report — NOT fresh Oct 31]**
- USDA Crop Progress (week ending Oct 25, released Mon Oct 26): corn harvest 60% complete (vs 66% five-year average), soybeans 79% (vs 77% average), winter wheat 76% planted / 53% emerged.
- **INFERENCE:** Harvest is far enough advanced that the supply picture is largely locked in ahead of the Nov 10 WASDE; the remaining grain catalyst is export demand, not harvest progress. Next Crop Progress: Mon Nov 2.
- Oct 30 grain closes (carried from the Oct 30 package, unchanged over the weekend): Dec corn $4.47¾ (four-month low), Jan soybeans $12.34¼, Dec SRW wheat $6.03½, Dec HRW wheat $6.44¼.

### What futures curves appear to be pricing

**Crude — backwardation persists, but mind the contract roll [FACT on prices, INFERENCE on interpretation]**
- **FACT (Fri Oct 30 settlements, Reuters consensus across multiple outlets):** Dec Brent expired at $117.64 (+$2.76, +2.4%, intraday high $118); new front-month Jan Brent settled at $113.43 (+$2.63); WTI settled at $104.12 (+$2.12, +2.08%). October: Brent +13.6%, WTI +15.2% — fourth consecutive monthly gain for both, highest closes since late April.
- **Roll warning [FACT]:** Because Dec Brent expired Friday, Brent's "front month" drops ~$4.21 on paper (from $117.64 to $113.43) without any price fall — it is the Dec→Jan spread, not a selloff. Any source showing Brent "down" on the week is measuring the rolled contract, not a decline. Genuine Dec–Jan backwardation is $117.64 − $113.43 = $4.21.
- **FACT (curve context):** Dec 2028 WTI $74.30 and Dec 2028 Brent $78.96, vs front-month $104.12 / $113.43 — a steep multi-year decline embedded in the strip.
- **UNVERIFIED:** A full dated strip from a primary exchange source was not retrieved in this run; curve shape rests on front contracts plus the cited summary, not a complete strip.
- **INFERENCE:** Unchanged from Oct 30, strengthened by the transit data: the curve prices prompt physical/logistics tightness plus a large seaborne risk premium, with normalisation deferred years out — not a demand boom. The weekend's two-way Doha setup means Monday's open is a binary repricing risk in either direction, not a trend continuation to assume.
- **What would change this read:** A Hormuz deal (compresses backwardation and the Brent–WTI spread first) or a confirmed supply cut / post-midterm escalation (steepens front backwardation further).

**Natural gas — soft prompt, no winter premium [INFERENCE from FACT prices above]**
- Dec Henry Hub near $2.90 with winter and summer-2027 strips at five-year lows prices adequate storage (3,724 Bcf, 38 Bcf above the five-year average) and warm early-November weather — not winter scarcity. The South Central salt deficit (~11.6% below seasonal average, per the Oct 30 package) remains the one tight pocket.

**Grains — front-month levels only; curve shape UNVERIFIED.** No verified deferred-contract curve was retrieved in this run; no contango/backwardation claim is made for grains.

### Forward catalyst calendar (verified dates only)

| Date | Event | Status |
|---|---|---|
| Sun Nov 1 | OPEC+ seven-producer meeting (Saudi Arabia, Russia, Iraq, Kuwait, Algeria, Kazakhstan, Oman) — December targets expected unchanged per three Reuters sources; no final decision as of Oct 27–29 reporting; ~2m bpd of cuts remain through end-2026; 2027 baselines still pending capacity review | FACT (expectation, not decision) |
| Mon Nov 2 | USDA Crop Progress (week ending Nov 1); AAPL earnings AMC (§1) | FACT (weekly Monday schedule) |
| Tue Nov 3 | US midterm elections — flagged as a decision point for post-election US–Iran strike risk | FACT (election date) / SPECULATION (strike timing) |
| Wed Nov 4 | EIA Weekly Petroleum Status Report (week ending Oct 30), 10:30 ET; OKTA joins S&P 500 (§6) | FACT (standard Wednesday schedule) |
| Thu Nov 5 | EIA Weekly Natural Gas Storage Report (week ending Oct 30); five-year-average injection for that week is 61 Bcf | FACT |
| Fri Nov 6 | US jobs report (per week-ahead previews) | FACT (scheduled release, as cited in week-ahead previews) |
| Tue Nov 10 | November WASDE + Crop Production, 12:00 ET, AND EIA Short-Term Energy Outlook | FACT (USDA calendar) |
| Sun Nov 29 | Full OPEC+ ministerial meeting (2027 policy) | FACT |

**Calendar correction note:** EIA's petroleum schedule lists the week ending Nov 6 as releasing Thu Nov 12 (Veterans Day exception) — that does NOT move the Nov 4 report (week ending Oct 30), which remains a standard Wednesday release.

### Government-data note

No shutdown/blackout framing applies. The Oct 28 EIA petroleum report, Oct 29 EIA gas report, Oct 26 Crop Progress, and Oct 9 WASDE were all released on schedule, consistent with the standing on-schedule rule. **Flagged and disregarded:** low-credibility AI-generated items found in this run's search results claim the November WASDE was "rescheduled to November 14 due to a government shutdown" — these contradict USDA's own published calendar (Nov 10, 12:00 ET) and the standing user-verified rule, and they describe a different crop-year context. They are NOT treated as a reschedule; if a primary source (usda.gov) ever contradicts the Nov 10 date, that would override.

### Desk bottom line

1. **Hormuz is now a two-way weekend binary, not just a risk premium** (new Oct 31 incident + live Doha mediation + post-midterm strike decision pending — Monday's crude open reprices on whichever hardens first).
2. **Transit data is the hardest physical signal** (~70% below pre-war Hormuz transits, week ending Oct 28) underpinning crude backwardation (Dec–Jan Brent $4.21).
3. **Don't be fooled by the Brent roll** (Jan Brent $113.43 is not a $4 fall from $117.64 — Dec expired Friday).
4. **Gas is the counterweight** (Dec Henry Hub near $2.90, strips at five-year lows, warm NOAA outlook into mid-November).
5. **Next decision points in order:** OPEC+ Sun Nov 1 → midterms Tue Nov 3 → EIA petroleum Wed Nov 4 → EIA gas Thu Nov 5 → WASDE + STEO Tue Nov 10.

## 6. Box/Parity Observer

**Bottom line: one NEW headline-index membership change (Okta into the S&P 500, effective Nov 4); no new published parity-violation analysis for SPY/QQQ. No parity deviation is claimed today.**

- **NEW — S&P 500 membership change, effective before the open Wed Nov 4, 2026** [FACT, S&P Dow Jones Indices release dated Oct 30, 2026, corroborated via PR Newswire + Morningstar republication; sweep as of Oct 31 ~13:35 PT]: Okta Inc. (NASDAQ: OKTA, Information Technology, promoted from the S&P MidCap 400) will replace Kenvue Inc. (NYSE: KVUE, Consumer Staples) in the S&P 500. Kenvue is being removed because S&P 500 constituent Kimberly-Clark (NASDAQ: KMB) is acquiring it, with the deal expected to close soon pending final conditions. Cascade: Glaukos Corp. (NYSE: GKOS) replaces Okta in the MidCap 400; McGrath RentCorp (NASDAQ: MGRC) replaces Glaukos in the SmallCap 600. Source: https://www.prnewswire.com/news-releases/okta-set-to-join-sp-500-others-to-join-sp-midcap-400-and-sp-smallcap-600-302925405.html
- **Parity relevance — watch for flow, not for a parity break** [INFERENCE]: a single-name, acquisition-driven swap in the headline index SPY tracks does not by itself alter put-call/box parity math for SPY options. Watch only for index-fund rebalancing flow in OKTA/KVUE around the Nov 4 effective open, not for a SPY parity deviation. No OKTA/KVUE weight was stated in the release [FACT].
- **Carried forward — S&P style-index methodology overhaul, effective before the open Mon Dec 21, 2026** [FACT, reported Oct 23/28, 2026 — see 2026-10-30 package for detail]: momentum dropped from growth rankings; value rebuilt around intangibles-adjusted book-to-price, averaged trailing + forward earnings-to-price, sales-to-price, and free-cash-flow-to-price (excl. real estate, banks, insurers, mortgage REITs, certain financials). Pro-forma files from Fri Dec 4, 2026. No update since yesterday's run. Parity relevance remains limited [INFERENCE]: style reclassification, not headline S&P 500 membership/weighting.
- **Nasdaq-100 "Fast Entry" — no change** [FACT]: no new adoption found since yesterday's run; the Feb 2026 proposal remains unadopted as far as this sweep found.
- **Published parity-violation analysis — none new found** [FACT, search Oct 31 ~13:35 PT]: searches for Oct 2026 box-spread / put-call parity violations returned only explainers and flow commentary (e.g., a $125.27M multi-leg SPY structure from Oct 23, 2026 — a directional spread, not a parity violation) and unrelated crypto/prediction-market arbitrage papers; no new empirical box or put-call deviation study for SPY/QQQ/SPX. No measured box or put-call deviation is reported here — any such figure would be UNVERIFIED without a live, synchronous, regular-hours options-chain check, which is outside this desk's light-touch brief.
- **Standing parity check** [FACT — deterministic math, not a market observation]: a fairly priced box pays exactly the strike width at expiry regardless of the underlying, so Box = (K2 − K1)·e^(−rT); a deviation beyond transaction costs is the arbitrage signal, and the math outranks any model output. No deviation is claimed today. Yesterday's apparent SPY Nov 2 parity gap (−$2.63) stands as a post-close non-synchronous data artifact, not a tradeable violation [FACT, 2026-10-30 package].

## 7. Bonds & Rates Desk

**Source:** repo module `hedge_desk.rates_desk.rates_environment()` (REAL_FRED_RATES mode, FRED public CSV, HTTP 200), run Sat Oct 31, 2026. **FRED-lag note:** latest observation in the pull is **Thu Oct 29, 2026** for every series — the Fri Oct 30 observation had not yet landed in the FRED daily pull at run time. All figures below are as of Oct 29, not Oct 31. No Yahoo yields substituted; no numbers retyped from memory.

| Series (FRED) | Level | As of | Label |
|---|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-29 | FACT |
| Treasury 2Y (DGS2) | 4.61% | 2026-10-29 | FACT |
| Treasury 10Y (DGS10) | 4.98% | 2026-10-29 | FACT |
| 2s10s slope (10Y − 2Y) | +37 bp | 2026-10-29 | FACT (computed: 4.98 − 4.61) |
| Curve shape (module) | UPWARD_SLOPING | 2026-10-29 | FACT |
| SOFR | 3.94% | 2026-10-29 | FACT |
| EFFR | 3.88% | 2026-10-29 | FACT |
| OBFR | 3.88% | 2026-10-29 | FACT |
| SOFR − EFFR spread | +6 bp | 2026-10-29 | FACT (computed: 3.94 − 3.88) |
| Module-reported fed funds change over 60-day window | +0.25 pp | 2026-10-29 | FACT (module output; window = 60 days) |

**Direction of change (FACT, from module 60-day histories):**
- Day-over-day (Oct 28 → Oct 29): 10Y fell 7 bp (5.05% → 4.98%), 2Y fell 6 bp (4.67% → 4.61%); 2s10s narrowed 1 bp (38 bp → 37 bp) — marginal flattening on the day.
- Week-over-week (Oct 23 → Oct 29): 2s10s widened 6 bp (31 bp → 37 bp) — modest steepening on the week, driven by the 2Y falling 8 bp while the 10Y fell only 2 bp.
- 60-day (Sep 1 → Oct 29): 2s10s essentially flat, 40 bp → 37 bp (−3 bp); both legs rose over the window (2Y 4.39% → 4.61%, 10Y 4.79% → 4.98%), with the 10Y peaking at 5.31% on Oct 5 before retracing.

**FOMC cross-check (FACT, module-consistent):** EFFR 3.88% sits inside the 3.75–4.00% target range set by the Oct 28 hold (10–2 vote, per desk context). The module output is consistent with the hold — it does not show a post-meeting funds-rate break.

**Funding stress gauge (INFERENCE):** SOFR − EFFR at +6 bp is a small, unremarkable gap — no sign of acute overnight funding stress. OBFR equals EFFR (3.88%), reinforcing a calm front end. What would change this read: SOFR − EFFR widening persistently above ~15–20 bp, or a jump in EFFR itself toward the top of the target range.

**Directional read for premium pricing (INFERENCE, not a trade call):**
- Long rates remain elevated in absolute terms (10Y just under 5.00%) even after the late-October retrace from the 5.31% Oct 5 peak — higher discount rates continue to pressure growth-multiple valuations, the margin-of-safety headwind for long-duration watchlist names.
- The curve is upward-sloping but not steep (+37 bp): no recession-style inversion signal, and no steepening surge arguing for a sharp re-rating either way.
- The week-over-week steepening came from the front end falling faster than the long end — consistent with the market holding the post-hold policy path steady while trimming near-term rate expectations slightly, not with a growth scare.
- For premium pricing: nothing in this snapshot argues for a rates-driven IV regime change; the rates backdrop is a steady headwind, not a catalyst. What would change this read: a 10Y break back above 5.31% (the Oct 5 high) or below ~4.90% with a simultaneous slope move, or a SOFR − EFFR blowout.

**UNVERIFIED / gaps:** Fri Oct 30 FRED observations (not yet published in the pull at run time) — the desk read above is explicitly as of Oct 29. No 13W-bill or ^TNX/^FVX Yahoo cross-check was substituted, per desk rules; the FRED DGS2 series is the 2Y here, so the ^FVX-labeling rule does not apply to any number in this section.

**Desk status:** COMPLETE — module succeeded, no fallback used.

## Synthesis — the 5 decision-relevant items

1. **AAPL Mon Nov 2 AMC is the week's binary event — premium into it = avoid.** ~4.25% implied (live Nov 4 straddle) vs ~2% typical; front IV 47.2% is 3.2× trailing realized. The Dec-quarter guide, not the September print, is the bar. NVDA Nov 17 (Nov 20 chain IV 48.7%) is the next binary, outside this window.
2. **Hormuz is a two-way weekend binary into Monday's open.** New Oct 31 tanker incident + live Doha mediation (two-day reopening proposal, unconfirmed) + a post-midterm US strike decision pending. Hardest physical signal: Hormuz transits ~70% below pre-war (week ending Oct 28). Crude: Dec Brent expired $117.64, Jan Brent $113.43, WTI $104.12 — do not misread the $4.21 Brent drop as a selloff; it is the Dec→Jan roll/spread.
3. **SPY has no clean IV-vs-realized verdict — WINDOW-CONTINGENT.** Friday's −1.79% drives 32.2% of the fresh 20-day window's variance; QQQ sits just under the line at 29.8%. IV rank is UNVERIFIED for all six names — no downstream summary may upgrade an IV-vs-realized comparison into an IV-rank claim.
4. **Rates are a steady headwind, not a catalyst.** 10Y 4.98%, 2Y 4.61%, 2s10s +37 bp (upward-sloping, +6 bp steeper on the week), EFFR 3.88% inside the post-hold range, SOFR−EFFR +6 bp (no funding stress) — all as of Thu Oct 29 (FRED lag; Oct 30 not yet published).
5. **Calendar stack for the coming week:** OPEC+ Sun Nov 1 (expected hold) → AAPL earnings Mon Nov 2 AMC → US midterms Tue Nov 3 → EIA petroleum Wed Nov 4 (plus OKTA joins the S&P 500, replacing Kenvue) → EIA gas Thu Nov 5 → jobs Fri Nov 6 → WASDE + STEO Tue Nov 10. Only declared dividend in the window: MSFT ex-div Thu Nov 19, $0.98, 24th consecutive annual increase. Quant lab: 9 new candidates logged (#188–#196), none TEST/INTEGRATE; strongest is the MIDAS-EPU vol-forecast study (58, WATCH) for its honest QLIKE-vs-MSE tradeoff — a caution, not an adoption.

**No desk dropped.** Research only — no git operations, no pushes, no PRs, no code changes.
