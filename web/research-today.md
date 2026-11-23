# Hedge-Desk Daily Research — Mon 2026-11-23 (as of ~13:30 PT)

Run: `hedge-desk-daily-research`, scheduled 13:30 PT. Seven desks fanned out in parallel; all seven reported. Research and input only — no git operations, no code changes.

Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Lens: value investor — mispricings, intrinsic-value gaps, margin of safety. Every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED. A number without a source and as-of is a rumor.

## The 5 most decision-relevant items

1. **The tape is the day: NVDA +31.5% on the Huang reinstatement, SPY +4.7%, QQQ +7.0%.** [FACT — Yahoo options-chain quote and v8 chart agree on levels; NVDA $125.53 Fri close → $165.05 intraday, TSLA $345.82 → $385.46, QQQ $608.45 → $651.03, SPY $689.81 → $722.29] The board voted unanimously to reinstate Jensen Huang as President/CEO and board director, effective immediately (NVIDIA Newsroom, Nov 23 — corroborates the Nov 23 governance record). Every IV read, every vol verdict, and the yield move below must be read against this tape, not as a quiet-day snapshot. **What would change it:** tomorrow's chain and close — whether the move holds or retraces.
2. **Desk 7: 5 HIKE / 0 CUT / 5 NEUTRAL — Dec 9 25bp hike call holds; the 50bp tail is dead.** [FACT — FRED via repo module + FRED API-key route, Kalshi direct API ~13:35 PT] Kalshi 25bp $0.93 (was $0.91 Nov 18); >25bp collapsed $0.08 → $0.03; hold halved $0.08 → $0.04. FedWatch secondhand 93–97% for 25bp. Housing starts flipped CUT → NEUTRAL. **Watch:** HY OAS widening fast — 3.76%, +56bp in 8 days toward the 4.00% tripwire. Next re-anchor: Oct core PCE, Wed Nov 25.
3. **No clean IV verdict anywhere — all six windows WINDOW-CONTINGENT.** [FACT — live Yahoo pull + IV-inputs file] Max single-day variance shares: SPY 35.5%, QQQ 33.8%, AAPL 46.2%, MSFT 38.2%, NVDA 46.6%, TSLA 43.4% — all >30%. The Nov 5 crash day still drives SPY/QQQ/TSLA windows; NVDA's window is now dominated by its Nov 20 −15.1% day. IV rank UNVERIFIED for all six (no IV history from free sources). No premium-selling thesis is supportable until the windows clean up (~Dec 3 for Nov 5, ~Dec 18 for NVDA Nov 20).
4. **Oil is pricing surplus, not war.** [FACT — EIA/Reuters, IEA, Yahoo] WTI ~$80.27, −4% Monday, after a weekend of Hormuz tanker strikes; EIA build +3.38M bbl vs +0.058M expected; IEA flipped to a +1.7 mb/d Q4 surplus. OPEC+ ministerial Sun Nov 29 is the next oil binary. Brent level UNVERIFIED to ±$1 (sources $86.70–$88.70); direction (−3 to −4%) corroborated.
5. **No earnings binary and no dividend event in the window — the calendar is empty.** [FACT — Nasdaq calendar API + Yahoo] Zero watchlist earnings Nov 23–Dec 7; next cluster late Jan 2027 (MSFT/TSLA Jan 27, AAPL Jan 28). Only confirmed ex-div in the next 4 weeks: NVDA Dec 2, $0.25, ~0.61%. SPY Dec 18 / QQQ Dec 21 distributions are scheduled but amounts undeclared.

## 1. Earnings Event desk

**Headline: NO watchlist name reports earnings in the next 2 weeks (Nov 23 – Dec 7, 2026).** [FACT — verified twice: Nasdaq earnings-calendar API queried for every date Nov 23–Dec 7 returned live rows with no watchlist symbol (filter verified working — e.g. Nov 24 shows DELL, ADI, MDT, ADSK); Yahoo v7 quote independently shows next earnings Jan 27–28, 2027 for MSFT/TSLA/AAPL. As-of 2026-11-23 ~13:30 PT]

| Symbol | Report date | Timing | Implied move % | Historical avg move % | Source / as-of |
|---|---|---|---|---|---|
| AAPL | None in window — next Jan 28, 2027 | — | — (no event) | — (no event) | Yahoo v7 quote (cookie+crumb), 2026-11-23 13:30 PT |
| MSFT | None in window — next Jan 27, 2027 | — | — (no event) | — (no event) | Yahoo v7 quote, 2026-11-23 13:30 PT |
| NVDA | None in window — last reported Nov 17, 2026; next date not yet set | — | — (no event) | — (no event) | Yahoo v7 quote; NVIDIA IR / SEC 8-K, 2026-11-23 |
| TSLA | None in window — next Jan 27, 2027 | — | — (no event) | — (no event) | Yahoo v7 quote, 2026-11-23 13:30 PT |
| SPY / QQQ | N/A — ETFs, no earnings | — | — | — | Yahoo v7 quote, 2026-11-23 |

- **FACT — NVDA Q3 FY27 print re-verified at the primary source.** Reported Tue Nov 17 after close: revenue $115.8B (+103% YoY, +20% QoQ), GAAP EPS $2.70, non-GAAP EPS $2.68 (+111% YoY); Data Center $107.6B (+110% YoY); Q4 FY27 guide ~$130B. Source: NVIDIA press release (investor.nvidia.com, Nov 17) corroborated by SEC 8-K exhibit. Note: $2.68 is non-GAAP; GAAP is $2.70 — do not cite $2.68 as GAAP EPS. No new NVDA release exists to read in-window, so no statement teardown applies this run.
- **FACT — Next earnings cluster is late January 2027.** Yahoo next-earnings timestamps (ET): MSFT Wed Jan 27, 2027; TSLA Wed Jan 27, 2027; AAPL Thu Jan 28, 2027 (all 16:00 ET, after close, per Yahoo timestamp convention). NVDA's next date is not yet published in Yahoo — **UNVERIFIED**; do not assume a February date. January dates are Yahoo-indicated and should be re-verified against company IR calendars as they approach.
- **INFERENCE — No earnings-driven binary-event premium in the window for the watchlist.** With zero watchlist earnings Nov 23–Dec 7, there is no earnings-avoid flag for the Premium desk from this desk's names. What would change it: a company announcing/rescheduling a report into the window, or a calendar update — re-check at the next daily run.

## 2. Dividend Opportunity desk

Window: ex-dividend dates Nov 23 – Dec 21, 2026. Prices as of Yahoo v8 chart, Nov 23, 2026 (SPY $722.51, QQQ $651.03, NVDA $165.05, AAPL $349.08, MSFT $492.50).

| Symbol | Ex-div date | Dividend | Yield | Increase / cut / special | Consecutive increases (per standard) | Source / as-of |
|---|---|---|---|---|---|---|
| NVDA | **Dec 2, 2026** | $0.25/qtr ($1.00/yr indicated) | ~0.61% | None — flat vs Sep 2026 $0.25 | UNVERIFIED (streak not re-verified against issuer history this run) | Nasdaq dividends calendar API + Yahoo quoteSummary, 2026-11-23 |
| SPY | **Dec 18, 2026** (issuer-scheduled, NOT yet declared) | Amount not yet declared — last paid $1.8888 (Sep 18) | ~1.05% trailing | None — amount undeclared, do not project | n/a (ETF) | State Street 2026 distribution schedule via Dividend Vision; Yahoo v8 chart, 2026-11-23 |
| QQQ | **Dec 21, 2026** (window boundary) | **UNVERIFIED — conflicting:** $0.7941 (dripcalc, "declared") vs ~$0.75 (FI Handbook est. / DivTrkr) | ~0.46% | None — amount disputed, no increase/cut claim | n/a (ETF) | TipRanks / dripcalc / dividendmax / FI Handbook, 2026-11-23 |
| AAPL | None in window — last ex-div Nov 12, 2026 ($0.27); next ~Feb 2027 | $0.27/qtr ($1.08/yr) | ~0.31% | None; last raise May 2026 ($0.26 → $0.27) | UNVERIFIED (streak not re-verified this run) | Yahoo v8 chart events + quoteSummary, 2026-11-23 |
| MSFT | None in window — last ex-div Nov 19, 2026 ($0.98); payable Dec 10, 2026; next ~Feb 2027 | $0.98/qtr ($3.92/yr) | ~0.80% | None; Sep 15, 2026 raise ($0.91 → $0.98) already reflected | **24 consecutive annual increases** (incl. Sep 2026 raise) per dividend-count-standard.md | Yahoo v8 chart events + quoteSummary; standard file, 2026-11-23 |
| TSLA | None — pays no dividend | $0 | 0% | None | n/a | Yahoo v8 chart + quoteSummary, 2026-11-23 |

- **FACT — NVDA is the only watchlist name with a confirmed, declared ex-div date inside the window:** Dec 2, 2026, $0.25/qtr, record date Dec 2, payable Dec 23, 2026; announced Nov 17, 2026 (Nasdaq dividends calendar API, corroborated by Yahoo quoteSummary). Flat vs Sep 10, 2026 — no increase, cut, or special. What would change it: an NVDA board declaration before Dec 2 (none expected).
- **FACT — SPY's Dec 18 ex-date is issuer-scheduled, not declared.** State Street's published 2026 distribution schedule puts SPY ex-div Dec 18, 2026, pay Jan 29, 2027; Yahoo calendarEvents carries no SPY date yet and the amount is undeclared. The ~$1.89 figure circulating in third-party pages assumes the Sep payment repeats — treated as UNVERIFIED, not used. What would change it: State Street's formal declaration (expected mid-Dec).
- **INFERENCE / UNVERIFIED — QQQ's Dec 21 amount is disputed and its pay date conflicts:** ex-date Dec 21, 2026 corroborated across TipRanks, dripcalc, dividendmax, DivTrkr, FI Handbook, but the amount is $0.7941 per dripcalc ("declared") vs ~$0.75 per FI Handbook/DivTrkr, and pay date Dec 28, 2026 (dripcalc/dividendmax) vs Jan 7, 2027 (DivTrkr). TipRanks states the dividend "has not been announced yet." Date reported as FACT (multi-source agreement); amount/pay date UNVERIFIED. What would change it: Invesco's declaration, expected ~Dec 18.
- **FACT — No increases, cuts, or specials announced on the watchlist this run.** AAPL ($0.27) and MSFT ($0.98) both went ex-div in the last two weeks at current rates. NVDA's June 2026 raise ($0.01 → $0.25/qtr) is the most recent watchlist increase and predates this window.

**Desk verdict:** Quiet window — one confirmed capture (NVDA, Dec 2, $0.25, ~0.61%) and two ETF distributions (SPY Dec 18, QQQ Dec 21) whose amounts are not yet declared; nothing here moves a margin-of-safety read on any watchlist name.

## 3. Overnight Premium desk (IV)

### IV-inputs file status — correction to the run brief's pre-flight read
The file `~/workspace/hedge-desk-research/nightly/2026-11-22-iv-inputs.json`, `as_of` **2026-11-22T14:54:29-07:00** (~22.5h old at run start — **within the 26h guard**), is **populated, not empty**: all six symbols present. The coordinator's pre-flight print showed an empty `symbols` dict because the key filter was applied at the wrong nesting level — corrected by direct re-read this session. The file carries the failover note ("repo hedge_desk.data.options_failover unavailable; legacy Yahoo-only options pull used"). However, its ATM IVs are for expiry **2026-11-23**, which died today at 16:00 ET / 13:00 PT — so the file's IVs are **STALE-BY-TENOR (dead contracts) and not usable as today's IV**. Its levels also run far above today's live prints (SPY 41.5% vs 22.3% live; NVDA 131.6% vs 79.2% live) — Sunday post-close marks on the Monday expiry. **Do not use the file's IVs; the live fallback pull below is the operative snapshot.** The file's window-contingent flags were independently corroborated by the live pull (see below) and are carried as FACT.

### Live fallback pull (FACT — Yahoo v7 options chain, cookie+crumb handshake, as_of 2026-11-23T13:27:46-08:00; zero failures)
Rolled to the nearest **unexpired** expiry (Nov 24 for SPY/QQQ, Nov 25 for singles). Raw output: `/tmp/iv_desk_live_2026-11-23.json`. Realized vol from v8 chart, fully-closed bars only, window 2026-10-26 to 2026-11-20.

| Symbol | ATM IV % (near expiry) | IV rank | Term structure (25DTE) | Earnings in window | Source / as-of |
|---|---|---|---|---|---|
| SPY | 22.3% (Nov 24, 1 DTE) | UNVERIFIED | 22.7% (Dec 18, 25 DTE) — flat | None | Yahoo chain, 13:27 PT |
| QQQ | 32.7% (Nov 24, 1 DTE) | UNVERIFIED | 32.4% (Dec 18, 25 DTE) — flat | None | Yahoo chain, 13:27 PT |
| AAPL | 28.9% (Nov 25, 2 DTE) | UNVERIFIED | 25.8% (Dec 18, 25 DTE) — front +3.1pp | None | Yahoo chain, 13:27 PT |
| MSFT | 39.4% (Nov 25, 2 DTE) | UNVERIFIED | 36.0% (Dec 18, 25 DTE) — front +3.4pp | None | Yahoo chain, 13:27 PT |
| NVDA | 79.2% (Nov 25, 2 DTE) | UNVERIFIED | 63.6% (Dec 18, 25 DTE) — front +15.6pp | None | Yahoo chain, 13:27 PT |
| TSLA | 51.9% (Nov 25, 2 DTE) | UNVERIFIED | 51.5% (Dec 18, 25 DTE) — flat | None | Yahoo chain, 13:27 PT |

IV rank is **UNVERIFIED for all six** — no IV history available from free sources; never guessed. Near-term prints are 1–2 DTE and noisy; the 25DTE column is the cleaner level read.

- **FACT — Massive rally day (see item 1 above).** All IV levels must be read against this tape, not as a quiet-day snapshot.
- **FACT — Every IV-vs-realized verdict is WINDOW-CONTINGENT — no clean cheap/rich call.** Max single-day variance shares (live pull, corroborating the IV-inputs file): SPY 35.5%, QQQ 33.8%, AAPL 46.2%, MSFT 38.2%, NVDA 46.6%, TSLA 43.4% — all >30%. Realized 20d: SPY 26.9%, QQQ 41.0%, AAPL 28.5%, MSFT 38.4%, NVDA 68.3%, TSLA 63.9%. Front IV sits below realized for SPY/QQQ/TSLA, about equal for AAPL/MSFT, above for NVDA — but with windows this contaminated, none of those gaps is a verdict. *What would change it:* the Nov 5 crash day aging out of the 20d window (~Dec 3) and NVDA's Nov 20 −15.1% day aging out (~Dec 18), plus an IV-history source for IV rank.
- **FACT — The Nov 5 crash day still drives SPY/QQQ/TSLA windows.** Worst days: SPY −4.5%, QQQ −6.7%, TSLA −11.4%, all Nov 5; AAPL/MSFT worst days are the Nov 4 rebound (+5.2%/+6.5%); NVDA's window is now dominated by Nov 20's −15.1% (46.6% share), not Nov 5. Today's +4.7% SPY move is **not** in the realized window (fully-closed bars only, through Nov 20).
- **FACT — No earnings inside the window — no binary-event premium to avoid.** All four singles already reported (TSLA Oct 22, MSFT Oct 29, AAPL Oct 30, NVDA Nov 17); next reports fall beyond the sweep window.
- **INFERENCE — Skew notes, from verified call/put IVs.** NVDA puts 87.2% vs calls 71.2% — put skew elevated after a +31% rip, consistent with hedging demand, not complacency. SPY calls 24.6% vs puts 20.0% — call skew on a +4.7% rally day, consistent with upside chasing. Both are reads on today's tape, not structural signals. *What would change them:* tomorrow's chain — if NVDA put skew persists after the move settles, it becomes a real hedging-demand signal.
- **FACT — Term structure is flat to mildly front-elevated.** Only NVDA shows a large front premium (+15.6pp, 2DTE vs 25DTE), reflecting today's governance event already in the tape, not an upcoming binary. No inversion anywhere that would signal acute near-term fear beyond today's move.

**Desk bottom line:** No elevated-IV-rank flag can be issued (rank UNVERIFIED); no earnings binary in window; no clean IV-vs-realized verdict (all six windows contingent). The decision-relevant item is the tape itself: a +4.7% SPY / +7.0% QQQ day led by NVDA +31.5%, with front IVs still below the (contaminated) 20d realized for the indexes — the options market has not repriced the rally into complacency or panic, but the numbers cannot support a premium-selling thesis until the windows clean up.

## 4. Open Quant/AI Model Lab

Coverage: arXiv q-fin listing for Mon Nov 23 (14 new + 1 cross-list + 10 replacements) closes the Nov 19–20 submitted window; the API submittedDate range returned only the 8 Nov-20 items and the no-filter top-40 missed 4 items, so the listing page was again the coverage control. SSRN leg run via web search. **Coverage limitation:** the GitHub leg was skipped this run (the agent read the run brief's "no GitHub operations" research-only boundary as a ban on GitHub discovery — no new-repo discovery, no repo re-checks, no code/license verification). All 11 candidates scored with the repo module (`hedge_desk.research_intelligence.assess_source`, never hand-scored) and appended to the ledger as #328–#338. Ledger verified on disk: 11 rows present, Jidoka entry added, #255 note added.

| # | Candidate | Source | Score | Disp. | Reason (as-of 2026-11-23) |
|---|---|---|---|---|---|
| 328 | Ranco — PINC econophysics covariance forecasting (leakage-free WF, DJIA 1-min) | arXiv:2611.27616 | 48 | WATCH | Vol-forecasting + purged-WF lane; no code link; submitted, not peer-reviewed |
| 329 | Zając/Dyrek — Jev LLM calibration vs NDX, Markov-switching | arXiv:2611.26716 | 48 | WATCH | LLM-calibration-on-markets; look-ahead audit required before any use |
| 330 | Cherrat et al — Distributional Deep Hedging (quantile P&L, ES/entropic) | arXiv:2611.26652 | 53 | WATCH | One policy serves many risk preferences; premium/hedging adjacent; no code |
| 331 | Ko/Yeh/Lin — VerifiQuant, governance-by-execution for financial LLM workflows | arXiv:2611.26649 | 59 | WATCH | **Run's top score.** ICAIF'26; fail-closed numeric-answer gating matches desk evidence discipline; code link stated, NOT verified (GitHub leg skipped) |
| 332 | Li/Yang — HTM accounting, hidden losses, systemic fragility | arXiv:2611.26700 | 45 | WATCH | Band floor; Desk 7 adjacent (bank opacity during tightening); model only |
| 333 | Ruelloux et al — Nonlinear shrinkage, higher moments (Russell 1000 OOS) | arXiv:2611.27274 | 48 | WATCH | Covariance/coskewness cleaning; methodology transfer to vol screens only |
| 334 | Bradrania/Gao — Trust and lottery-related anomalies (MAX effect) | arXiv:2611.27020 | 39 | ARCHIVE | Behavioral anomaly; no methodology transfer |
| 335 | Bénézet et al — Quantile-hedging numerical error analysis | arXiv:2611.26673 | 36 | ARCHIVE | Pure numerics theory; thin desk transfer |
| 336 | Kratsios et al — Reconstructing risk preferences from data | arXiv:2611.27692 | 41 | ARCHIVE | Risk-measure theory; no desk transfer |
| 337 | Miao et al — Risk sharing, infinite-mean background risk | arXiv:2611.27485 | 30 | ARCHIVE | Pure theory; no desk transfer |
| 338 | Clark — Option-implied info and hard-to-value firms (SSRN leg) | SSRN 7682270 | 51 | WATCH | IV-spread predictability × valuation uncertainty; 0.609%/mo HTV differential after FF5; directly premium-desk relevant; licensed OptionMetrics data, no code |

- **Most decision-relevant (FACT, abstract-level, UNVERIFIED beyond abstract):** #338 Clark — IV-spread return predictability is firm-type dependent; if the desk screens on IV spread, the HTV conditioning (market-to-book, R&D intensity, idiosyncratic vol) is the one new input worth a full-paper read.
- **INFERENCE:** #331 VerifiQuant's "refuse rather than emit a confident wrong number" is the same fail-closed discipline the desk already applies to data — worth verifying its repo on a permitted leg and stealing the gating idea, not the code.
- **FACT — Movement:** #255 Brini point-in-time earnings-call encoders v1→v2 (updated 2026-11-20); repo already MIT-verified 2026-11-14; stays WATCH.
- **FACT — Re-checks:** #4/#9/#13/#14/#15/#20/#21/#25/#30/#31/#257 and the #312–#323 spot set — no version movement; all stay WATCH/ARCHIVE as recorded. No TEST/INTEGRATE movement (run max 59).
- **FACT — Triage exclusions, no ledger rows:** 2611.26670 Solvency II longevity (insurance), 2611.26882 Colombia peace (econ), 2611.26948 DeFi lending (crypto), 2611.27210 agents/labor market (labor econ), 2611.27505 AI delegation in banking (banking-ops governance). Replacements: 2611.24266 is #310 (already ledgered).

Ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (rows #328–#338, Jidoka entry, #255 v2 note).

## 5. Weather/War/Logistics Futures Event desk

| Event | Date | What happened / expected | Futures reaction | Source / as-of |
|---|---|---|---|---|
| EIA Weekly Petroleum Status (week ended Nov 13) | Released Wed Nov 18, 10:30 ET | **FACT:** Commercial crude +3.38M bbl to 417.8M vs +0.058M expected; gasoline +5.2M to 215.9M vs +1.6M expected; distillate +1.6M to 104.9M; jet +2.2M to 44.1M; Cushing −1.2M to 26.1M; SPR −3.17M to 276.4M; total commercial petroleum +9.2M to 1,224.9M | **FACT:** Brent settled Wed $91.95 (−1.28%); WTI $83.26 (−3.2%), lowest since Aug 26 | EIA via Reuters/Informist, Nov 18–19 |
| IEA Oil Market Report (Nov) | Week of Nov 16 | **FACT:** IEA flipped to Q4 surplus — supply avg 105 mb/d, +1.7 mb/d above forecast demand; Oct observed global inventories +52M bbl (+1.7 mb/d); floating storage +86M bbl | **INFERENCE:** Surplus framing is the dominant price driver this week, outweighing Gulf attacks | IEA via Reuters/Canada News Group, Nov 18–19 |
| Strait of Hormuz attacks | Nov 13–18, plus weekend Nov 21–22 | **FACT:** UKMTO listed 5 attacks Nov 13–18 (tankers struck, engine-room fires Nov 16); weekend: 2 outbound tankers struck near Khasab, Oman within 50 min; LNG carrier transits plunged from ~8/wk (Sep–Oct avg) to 2 last week; IMO counts 138 confirmed incidents to Nov 17; Kpler: Hormuz clearance 7d to Nov 11 averaged 8,264 kbd, ~48% of pre-war 17,148 kbd. US strikes on IRGC missile site on Qeshm Island Tue, per US official cited by CBS | **FACT:** Oil fell anyway — Brent/WTI down Mon Nov 23 (see below). **INFERENCE:** Market is pricing surplus over war premium for now | IndustryWeek Hormuz Watch (upd. Nov 19); Int'l Trade Council briefing Nov 23; Kpler briefing Nov 13; EuroOilWatch Nov 18 |
| Red Sea / Bab el-Mandeb | Nov 12–17 | **FACT:** Houthis claim drone hits on Saudi East–West pipeline pumping stations Nov 12 and 17 — **UNVERIFIED**, no Saudi confirmation; Yemen govt withdrew from Bab el-Mandeb positions Nov 15; no confirmed attack on Red Sea shipping since Aug 24 | No measurable price response | EuroOilWatch, verified Nov 18 |
| Black Sea shipping | Nov 14–17 | **FACT:** LPG tanker Gas Husky sank off Bulgaria Nov 17, 7th vessel struck in Bulgarian waters since Oct; 3 ships hit near Romania's Sulina canal Nov 14 | No oil-price response observed | EuroOilWatch, verified Nov 18 |
| USDA Nov WASDE + Crop Production | Released Tue Nov 10, noon ET | **FACT (not fresh today):** Corn yield cut to 179.6 bu/ac (Oct 181.2; trade avg 180.5), production 15.893B bu, carryout 1.758B bu — 68M below trade; soy yield record 53.3 bu/ac, production 4.574B bu, carryout 300M — 36M below trade; world wheat ending stocks 280.82 Mt, above highest estimate; corn farm price cut to $4.60 | Grains firmer Mon per Yahoo prints — move **UNVERIFIED** vs independent source | USDA WASDE-677 via Ag Optimus / GrainDecision, Nov 10 |
| Next EIA weekly | Wed Nov 25 (one day early, Thanksgiving) | **FACT:** Next release due Nov 25 | — | TradingNews, Nov 20 |
| OPEC+ ministerial | Sun Nov 29 | **FACT:** 42nd OPEC/non-OPEC ministerial + JMMC; agenda is the 2027 output framework and new baselines; Dec output held at Sep level on Nov 1; ~2M b/d of 2022 cuts still in place through year-end; IEA sees 2027 overhang of 3.8M b/d (per S&P Global) | **INFERENCE:** The key binary for oil into year-end; restraint = support toward $96–100 Brent, restoration = downside toward $84–90 WTI per analyst framing | OPEC/Reuters via Admiral Markets, FinanceFeeds, Nov 20–21 |
| Next USDA WASDE | Thu Dec 10 | **FACT:** No USDA report due today/tomorrow; next WASDE Dec 10 | — | Ag Optimus, Nov 10 |

### Front-month futures snapshot (as-of Mon Nov 23, 13:27 PT, Yahoo v8 chart, UA-only)

| Contract | Price | Day move / note |
|---|---|---|
| WTI (CL=F, Jan 2027 front month after Dec expiry Fri) | **$80.27** | **FACT:** Down ~$3.3 (≈−4%) vs Fri settlement $83.41 — matches OPIS 11:45 ET print of Jan WTI $80.10 (−$3.31). Third straight weekly decline; WTI −5.17% last week |
| Brent (BZ=F) | **$86.70** (Yahoo) vs $88.70 OPIS 11:45 ET, $87.42 MineralPulse 13:27 ET | **FACT:** Falling through the session; all sources agree direction (−3 to −4% on the day), levels differ by timestamp/contract — treat $87–89 as the range, not a single print. Fri settlement $92.57; Brent −3.41% last week |
| Natgas (NG=F) | **$3.52** | **FACT:** Reported −6% to −8% on the day (MineralPulse −6.03%, Capital Street −8.18%) on milder weather forecasts unwinding Friday's heating-demand premium; Yahoo price level matches MineralPulse but its 5d closes are inconsistent — day-change taken from press, not Yahoo closes |
| Gold (GC=F) | **$3,634.80** | **FACT:** +~3.4% vs Fri close $3,515.40 — rebound after Fri −4.62% slide to lowest since Sep 2025; gold had its steepest weekly fall since March; Dec Fed-hike odds >95% cited as the drag |
| Corn (ZC=F) | **$449.00** | Yahoo print only; day-move **UNVERIFIED** (no independent corroboration today) |
| Soybeans (ZS=F) | **$1,227.50** | Yahoo print only; day-move **UNVERIFIED** |

- **INFERENCE — Oil is pricing surplus, not war — the week's key tension.** Three straight weekly declines (Brent −3.41%, WTI −5.17% last week), a much-larger-than-expected EIA build across crude/gasoline/distillate, and the IEA's flip to a +1.7 mb/d Q4 surplus have overwhelmed a genuinely deteriorating Hormuz picture (5 UKMTO attacks Nov 13–18, 2 more tankers struck over the weekend, LNG transits down to 2/wk, clearance at ~48% of pre-war). Monday's ~4% drop to WTI ~$80 / Brent ~$87–89, *after* the weekend tanker strikes, is the market's verdict so far. **What would change it:** a Hormuz incident that demonstrably cuts flows (not just strikes a ship), an OPEC+ restraint signal on Nov 29, or a Nov 25 EIA draw that breaks the build streak.
- **FACT + INFERENCE — OPEC+ Nov 29 is the next real oil binary.** Dec output is already held at September levels; the Nov 29 meeting sets 2027 quotas off a delayed capacity review, with ~2M b/d of 2022 cuts still to be allocated. Until then, leaks about the capacity review are the main scheduled mover. **What would change it:** delegate comments or a capacity-review leak before Nov 29; a decision to restore large volumes would reinforce the IEA surplus case.
- **FACT — Grains: November WASDE is absorbed; nothing fresh until Dec 10.** The Nov 10 WASDE was modestly tighter than expected on corn/soy carryout (68M / 36M bu below trade) but world wheat stocks came in above the highest estimate — a mixed, now-13-day-old print. No USDA release is due today or tomorrow; next WASDE is Dec 10, with weekly Export Sales / Crop Progress as the only interim checkpoints. **What would change it:** a South America weather shift or an export-sales surprise.
- **INFERENCE — Gold/natgas moved on rates and weather, not on the Gulf.** Gold's +3.4% Monday rebound follows its worst week since March on >95%-priced Dec hike odds; natgas fell ~6–8% on milder forecasts. Neither move traces to Hormuz. European TTF gas, by contrast, jumped up to +8.6% intraday on cold forecasts and Troll maintenance — a regional divergence worth noting, not a US signal. **What would change it:** Wednesday's PCE / flash PMIs for gold; a colder US forecast revision for natgas.

**Data-quality notes:** **CONFLICT FLAGGED, NOT USED:** One low-credibility source (finpulse360, Nov 22) claimed a 5.8M-bbl EIA crude *draw* and 94.2% refinery runs — directly contradicting the EIA/Reuters/Informist +3.38M build. Disregarded; the build is corroborated by multiple sources. **Brent level discrepancy:** Yahoo BZ=F ($86.70 at 13:27 PT) sits ~$2 below OPIS ($88.70 at 11:45 ET) and ~$0.70 below MineralPulse ($87.42 at 13:27 ET) — consistent with a fast-falling intraday market and different timestamps, but the exact Brent level is **UNVERIFIED** to better than ±$1; direction (−3 to −4%) is corroborated. No federal shutdown / data-blackout framing applies: EIA and USDA released on schedule (per standing rule; EIA Nov 18 and WASDE Nov 10 both landed normally). No watchlist-name-specific futures catalyst identified today; energy moves are macro, not single-name.

## 6. Box/Parity Observer

- **FACT — Cboe launched AM-settled SPX weeklies under new symbol SPXO, live Nov 9, 2026; first expirations Nov 18 and Dec 16, 2026.** SPXO settles to the SPX opening settlement price (SET), same as monthly AM-settled SPX. Source: Cboe notice (ww2.cboe.com/notices/content/?id=62439), verified live 2026-11-23. Related fee filing SR-CBOE-2026-085 (approved, effective Nov 1, 2026) extends the SPX/SPXW electronic execution surcharge to SPXO. **Parity watch item:** SPXO uses price-time allocation vs. pro-rata for SPX, shares matching unit 33 with SPX, has no separately configurable risk limits, and complex orders across SPX/SPXO/SPXW are permitted but cannot leg into single-leg books when SPXW is involved (separate matching unit). Same-underlying, same-settlement options now trade under three symbols — cross-symbol put-call/box parity on coincident expiries is the thing to monitor.
- **FACT — No put-call parity violation reported in the last few days.** Saxo's daily Options Brief put-call parity checks on the Nov 18 SPX options returned implied VIX in line with settlement on Nov 2 (20.16), Nov 4 (19.96 vs. 19.90 settlement), Nov 5 (17.73 vs. 17.74), and Nov 6 (24.55, in line) — parity holding through the Nov 5–6 selloff. Sources: home.saxo Options Briefs, Nov 2–6, 2026.
- **FACT — SPX box-spread implied financing, measured Nov 12, 2026: 3.86% short end, 5.16% at 435 days, vs. ~5.39% first-tier Interactive Brokers margin.** No dislocation — the gap is thin and in the expected direction. Source: Solvinc blog measurement of the full CBOE delayed SPX chain (31,016 contracts), single-source, not independently verified. **INFERENCE:** boxes remain a financing-rate instrument, not an exploitable arbitrage at these levels.
- **FACT — Apparent extreme box rates (−95% to +186% APR) in naive scans of the same Nov 12 data are stale-quote artifacts, not violations.** Per the same Solvinc measurement, delayed/asynchronous quotes produce impossible prints; a parity regression across strikes is required before any dislocation claim. No credible published parity-violation analysis found in the last few days.
- **INFERENCE — No action for the watchlist (SPY, QQQ, AAPL, MSFT, NVDA, TSLA).** Nothing material for single-name parity; the only live item is the SPXO rollout above. Deterministic parity still governs: no model output in this run contradicts put-call/box parity, so no override applies.

**Bottom line:** Nothing broken; one live structural change to watch — SPXO AM-settled weeklies (first expiry Nov 18 already traded, next Dec 16).

## 7. Bonds & Rates desk (Desk 7)

**Module status:** `rates_desk.rates_environment()` ran clean in REAL_FRED_RATES mode this session. All levels below were independently re-verified via the FRED API-key route (`fred_observations.py`) — the two routes agree exactly on every series. **Defect handling (Sentry W48):** the module's `curve_slope` ("0.035000") does not match its own levels and is discarded — slope below is computed from verified levels. The module's `fed_funds_change_over_window` ("0.00") is unsigned with no baseline and is NOT cited — 60-day change UNVERIFIED. The module's `as_of` ("2026-11-23") is wall clock; actual latest data dates are Nov 19 (DFF/DGS) and Nov 20 (SOFR/EFFR/OBFR). DGS10 came through fine this run, so the key-typo defect did not bite today.

### Rates table (FACT, FRED via two routes)

| Series | Level | As-of |
|---|---|---|
| EFFR (policy rate) | 3.88% | Nov 20 |
| DFF (fed funds, corroboration) | 3.88% | Nov 19 |
| 2Y Treasury (DGS2) | 4.76% | Nov 19 |
| 10Y Treasury (DGS10) | 5.04% | Nov 19 |
| SOFR | 3.92% | Nov 20 |
| OBFR | 3.88% | Nov 20 |
| Target range | 3.75–4.00% | Oct 28 FOMC hold |

**2s10s slope: +28bp** (5.04 − 4.76), upward sloping. Direction: +27bp Nov 18 → +28bp Nov 19 (+1bp); week range +27 to +30bp — essentially flat. **SOFR–EFFR spread: +4bp** (3.92 vs 3.88, Nov 20) — narrow, no funding stress (was +3bp Nov 19). Yields eased over the week: 10Y 5.15% (Nov 13) → 5.04% (Nov 19, −11bp); 2Y 4.88% → 4.76% (−12bp).

### Core-indicator table (FACT, FRED unless noted; pulls this session)

| Indicator | Today's read | Verdict | Broker POV |
|---|---|---|---|
| Core PCE (PCEPILFE) | Sep 2026: y/y +3.12%, m/m +0.32% (130.902) | **HIKE** | Anchor the discount rate to the higher regime. The decision variable is PCE; Oct PCE lands Wed Nov 25 — that is the re-anchor date. |
| Breakevens (T5YIE/T10YIE) | 2.18% / 2.15% (Nov 20), down from 2.31%/2.24% (Nov 12) | NEUTRAL | Anchored expectations: room for 25bp, no credibility crisis forcing 50bp. Tripwire is a break above 2.75%. |
| Michigan expectations (MICH) | 4.3% yr-ahead, Nov prelim (U-M, rel. Nov 6; FRED latest is Oct 4.7% — FRED lags ~1 mo) | **HIKE** | Do not average with breakevens: 4.3% vs 2.15% is a credibility gap the Fed reads as pressure to act. |
| Payrolls, 3-mo avg (PAYEMS) | +137k (Aug +186k, Sep +60k, Oct +165k; Oct level 159,293k) | NEUTRAL | Rule as written: NEUTRAL. The single +165k print does not override the average. |
| Initial claims, 4-wk avg (ICSA) | 197,750 w/e Nov 14 (latest print 203k, new since Nov 7) | NEUTRAL | No action. Check every Thursday; a 4-wk avg above 300k flips labor to CUT before payrolls confirm. |
| Job openings (JTSJOL) | 7,523k Sep (Jun 7,182k → +341k over 3 mo) | **HIKE** | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1) | Q3 +3.37% annualized (24,611.1 vs 24,408.0) | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Backdrop, not trigger. |
| Housing starts (HOUST) | 1,309k Oct; Jul→Oct −4.4% (Sep revised 1,221k → 1,191k) | NEUTRAL | **Flipped CUT → NEUTRAL.** Oct rebound puts the trailing 3-mo change inside the −5% tripwire. The hold case's best evidence just weakened — and it is why the call stays 25bp, not 50bp. |
| HY OAS (BAMLH0A0HYM2) | 3.76% (Nov 20), up from 3.20% (Nov 12); +24bp day-over-day | NEUTRAL | No stress yet, but widening fast (+56bp in 8 days) toward the 4.00% tripwire. Watch, don't act. |
| FOMC vote & guidance | Oct 28 hold 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; Nov 18 minutes: nearly all judged further hikes likely appropriate; several said >25bp could be justified in Dec if inflation data unfavorable | **HIKE** | Weight the vote above any print. Size debate is live: Waller reaffirmed 50bp support (Nov 18); Williams said no "dramatic action" needed (Nov 18); Hammack prefers gradual; Musalem wants "several increases before spring 2027"; Bessent (Treasury, Nov 20) pushed back on 50bp. No hold-leaning Fed voice has emerged. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL** — unchanged from Nov 18. One move inside the tally: housing starts flipped CUT → NEUTRAL on the Oct rebound.

### Market pricing vs indicator read

- **Kalshi, direct API pull this session (~13:35 PT Nov 23, Dec-2026 `KXFEDDECISION-26DEC`):** 25bp hike **$0.93** (bid/ask 0.93/0.94, prev $0.89, 24h vol 663k); >25bp **$0.03** (prev $0.03); hold **$0.04** (prev $0.08); cuts $0.01 each. Sum of lasts $1.02 (2¢ over-round). **Total hike $0.96.** vs Nov 18: 25bp $0.91 → $0.93; **the >25bp tail collapsed $0.08 → $0.03**; hold halved $0.08 → $0.04.
- **CME FedWatch:** could not be read directly (embedded app, no public text API) — secondhand reads converge: **25bp 93–97%** (Barron's 93%, WSJ 97%, FrenzyCap live 96% / >25bp 4%), hold 0–6.8%, 50bp 0–4%. The 50bp outcome is now essentially priced out on every venue.
- **Disagreements:** none on direction — indicators, Kalshi, and FedWatch all say hike. The size disagreement that existed Nov 13–18 (tail $0.08–$0.12 vs FedWatch 9–15%) has **resolved toward 25bp** on both venues. Remaining gap: the indicator set votes direction only, not size; markets now do the sizing, and they say 25bp. (INFERENCE: the tail collapse coincides with yields easing −11bp on the week and with Williams/Hammack gradualist signals outweighing Waller's 50bp advocacy.)

### Graham lens (FACT arithmetic)

10Y at 5.04% (Nov 19) vs 4.98% (Nov 10 anchor): at g = 3.00%, Gordon multiple 1 ÷ (r − g) falls 50.51x → 49.02x, **−2.95%**. Re-anchor to 5.04%. Duration ≈ 8 puts the +6bp move at ≈ −0.48% on a 10-year position. Margin of safety is thinner at the same prices; the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price. Earnings-yield vs bond-yield spread: UNVERIFIED (no primary earnings-side source this session).

### Verdict

- **Thesis:** 25bp hike on Dec 9 holds. Core PCE (+3.12% y/y) sits 112bp above target, labor shows no deterioration on any kept read, growth runs above trend, the 10–2 vote with two hawkish dissents states the Committee's lean, and markets price a hike at $0.96 combined.
- **Evidence:** 5 HIKE / 0 CUT / 5 NEUTRAL; Kalshi 25bp $0.93 (up from $0.91); FedWatch 93–97% for 25bp; 50bp tail collapsed to $0.03; 2s10s +28bp flat; SOFR–EFFR +4bp, no funding stress.
- **What would change it:** Oct core PCE Wed Nov 25 — m/m at or below +0.15% with a downward Sep revision; claims 4-wk avg above 300k; a named speaker arguing for a hold. Nov CPI lands Dec 10, after the decision, so it cannot change December. The live 50bp voice is Waller alone; a second voter joining him plus a hot Oct PCE would reopen size — neither has happened.
- **UNVERIFIED items:** module's 60-day fed-funds change (no baseline pulled); CME FedWatch direct read (secondhand range only); Michigan November final (prelim 4.3% stands until it lands).

Sources: FRED (DFF, DGS2, DGS10, SOFR, EFFR, OBFR, PCEPILFE, T5YIE, T10YIE, MICH, PAYEMS, ICSA, JTSJOL, GDPC1, HOUST, BAMLH0A0HYM2) via repo module + FRED API-key route, pulled Nov 23 ~13:30 PT; Kalshi trade API v2 direct, Nov 23 ~13:35 PT; federalreserve.gov Oct 28 statement + Nov 18 minutes (as previously verified); FedWatch via Barron's/WSJ/FrenzyCap secondhand, Nov 23; Fed speaker remarks via MaceNews/TradingView and xshorts.news, Nov 18–20 (secondhand press reports — INFERENCE-grade for guidance, FACT-grade for the vote).

## Run notes / reconciliation

- **IV-inputs file correction (this session):** the coordinator's pre-flight print suggested an empty `symbols` dict; direct re-read showed all six symbols populated. The error was the pre-flight filter applied at the wrong nesting level. The file is within the 26h guard but STALE-BY-TENOR (Nov 23 expiry, dead today); the live Yahoo fallback pull is the operative IV snapshot. The file's window-contingent flags were independently corroborated by the live pull.
- **Cross-desk consistency checked:** Earnings (no watchlist earnings in window) agrees with Premium (no earnings binary in window; Nasdaq calendar sweep 45 days, zero hits). Dividend prices (SPY $722.51, QQQ $651.03, NVDA $165.05) agree with Premium live levels within intraday drift. Desk 7's >95% Dec-hike pricing agrees with the Futures desk's gold-drag framing. Futures Brent level is the one unresolved cross-source spread ($86.70–$88.70) — reported as a range, not a point.
- **Coverage gaps this run:** Quant Lab GitHub leg skipped (agent read the research-only boundary as a discovery ban — flag for the next run's brief to clarify: read-only GitHub *search* is not a GitHub operation); IV rank UNVERIFIED all six (no free IV-history source); CME FedWatch direct read unavailable (secondhand range only); QQQ Dec 21 distribution amount/pay date UNVERIFIED (conflicting third-party figures); Brent exact level UNVERIFIED to ±$1.
- **No desk failed.** All seven reported. No retry was needed.
- **Desk-failure / recovery log:** none this run.

## Sources (by desk)

- Earnings: api.nasdaq.com/api/calendar/earnings; query1.finance.yahoo.com/v7/finance/quote (cookie+crumb); investor.nvidia.com; sec.gov (NVDA 8-K).
- Dividend: Nasdaq dividends calendar API; Yahoo v8 chart / quoteSummary; State Street 2026 distribution schedule via Dividend Vision; TipRanks / dripcalc / dividendmax / FI Handbook; ~/workspace/hedge-desk-research/dividend-count-standard.md.
- Premium: ~/workspace/hedge-desk-research/nightly/2026-11-22-iv-inputs.json (as_of 2026-11-22T14:54:29-07:00); Yahoo v7 options chain (cookie+crumb), as_of 2026-11-23T13:27:46-08:00; Yahoo v8 chart; raw live pull /tmp/iv_desk_live_2026-11-23.json.
- Quant: arXiv q-fin listing Mon Nov 23; SSRN; hedge_desk.research_intelligence.assess_source; ~/workspace/hedge-desk-research/quant-lab-ledger.md (#328–#338).
- Futures: EIA via Reuters/Informist; IEA via Reuters/Canada News Group; IndustryWeek Hormuz Watch; Int'l Trade Council briefing Nov 23; Kpler; EuroOilWatch; USDA WASDE-677; Yahoo v8 chart; OPIS; MineralPulse.
- Parity: ww2.cboe.com/notices/content/?id=62439; SR-CBOE-2026-085; home.saxo Options Briefs Nov 2–6; Solvinc blog (Nov 12 measurement).
- Rates: FRED (16 series) via repo module + fred_observations.py; Kalshi trade API v2 (KXFEDDECISION-26DEC); federalreserve.gov; Barron's / WSJ / FrenzyCap (FedWatch secondhand).
