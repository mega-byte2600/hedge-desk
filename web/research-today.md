# Hedge-Desk Daily Research — Sat 2026-11-14 (13:30 PT)

**Scope:** Watchlist SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Prices/options as of Fri 2026-11-13 close (last trading session). Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; SPECULATION = untested hypothesis; UNVERIFIED = looked, could not confirm. Paper-only research; no Risk of Ruin, no trade authorization. Government-data rule stands: no federal shutdown (CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11); federal releases ran on schedule this week.

## Headline: the 3–5 most decision-relevant items

1. **NVDA earnings Tue Nov 17 after close — the only watchlist event in the next two weeks.** Options imply ~9.6% (Nov 20 weekly ATM straddle) vs a 4.53% average absolute earnings-day move over the last 4 quarters — ~2.1× history. Premium into this binary event = avoid. (FACT, Nasdaq calendar API + Yahoo; INFERENCE on expensiveness.)
2. **Desk 7 unchanged: 25bp hike call for Dec 9; 10Y at 5.10%.** FRED pull this session: 10Y 5.10% (+12bp since Nov 13), 2Y 4.86% (+13bp), 2s10s +24bp. Tally 5 HIKE / 1 CUT / 4 NEUTRAL, unchanged. Kalshi total hike $0.99 (was $1.00). New: Waller's Nov 10 50bp trigger was met by core CPI +0.3%, giving the tail a named mechanism — tail still ~11%. Graham lens: re-anchor to 5.10%; Gordon multiple −5.72% on the week.
3. **No clean IV-vs-realized verdict anywhere — all six windows WINDOW-CONTINGENT.** The Nov 5 crash day drives 37–54% of 20-day realized variance, above the 30% threshold. IV-inputs file passed the 26h guard (as_of 2026-11-13T14:54:31−07:00) but its ATM IVs are null again (7th consecutive null context — post-expiry guard). Live supplement: NVDA 92.5% ATM IV at Nov 18 expiry (earnings hump); all other front-end IVs unremarkable.
4. **Crude: second straight ~2.5% weekly decline, but the curve still says tight now.** EIA build +4.657M bbl vs an expected draw; IEA calls Q4 surplus; OPEC+ output +1.96M bpd in Oct. Thursday +3.3% spike on Hormuz mine claims — claims UNVERIFIED (Reuters could not confirm; USCENTCOM disputed). WTI Dec-26 $88.56; Brent Jan-27 $95.84; steep backwardation persists. WASDE Nov 10 cut corn (1.758B bu) and soybean (300M bu) ending stocks well below trade estimates.
5. **MSFT goes ex-dividend Thu Nov 19 at the new $0.98 rate** — first cash payment of the 24th consecutive annual increase, payable Dec 10. AAPL's $0.27 payment lands Mon Nov 16 but its ex-date (Nov 12) is already past. NVDA's next declaration is undeclared (expected early December on pattern).

---

## 1. Earnings Event desk

**Question:** Which watchlist names report in the next two weeks, and what move is the options market pricing versus what NVDA has actually done on recent earnings days?

### Upcoming earnings — next 2 weeks (through Fri 2026-11-28)

| Symbol | Report date | Timing | Consensus EPS | Options-implied move | Historical avg \|earnings-day move\| | Source |
|---|---|---|---|---|---|---|
| **NVDA** (Q3 FY27) | **Tue 2026-11-17** | After market close | $2.49 (Nasdaq, 13 ests); Yahoo avg $2.47, range $2.26–$2.70; revenue avg $108.73B | **~9.6%** (Nov 20 weekly ATM 162.5 straddle, $15.70 mid / $162.85 underlying); Nov 18 straddle ~8.6% | **4.53%** (last 4 qtrs) | Nasdaq calendar API + Yahoo calendarEvents + Yahoo v7 options, as of 2026-11-13 close |
| AAPL | 2027-01-28 (estimate) | — | $2.91 est. | — | — | Yahoo calendarEvents |
| MSFT | 2027-01-27 (estimate) | — | $4.86 est. | — | — | Yahoo calendarEvents |
| TSLA | 2027-01-27 (estimate) | — | $0.50 est. | — | — | Yahoo calendarEvents |
| SPY, QQQ | n/a — ETFs, no earnings | — | — | — | — | — |

**FACT:** NVDA is the only watchlist name reporting in the next two weeks. Nasdaq and Yahoo agree on Tue 2026-11-17 after close; Yahoo flags it as a confirmed (non-estimate) date.

### NVDA historical earnings-day moves (Yahoo daily closes, report-day close → next trading-day close)

| Quarter | Reported (after close) | Move |
|---|---|---|
| Q3 FY26 | 2025-11-19 | −3.15% ($186.52 → $180.64) |
| Q4 FY26 | 2026-02-25 | −5.46% ($195.56 → $184.89) |
| Q1 FY27 | 2026-05-27 | +0.78% ($212.60 → $214.25) |
| Q2 FY27 | 2026-08-26 | +8.74% ($209.66 → $227.98) |

**FACT:** Average absolute move over the last 4 quarters = **4.53%**; signed average = −0.02% (2 down, 2 up — no directional bias). Only the Aug 2026 move (+8.74%) approached the currently implied move.

**Verdict (INFERENCE):** The options market prices ~2.1× the recent realized average. The straddle buyer pays for a move NVDA delivered once in four quarters. Through a value lens, that is expensive insurance, not a mispricing to chase. The Nov 20 weekly straddle carries two extra non-earnings days of vol; the Nov 18 (1-day post-earnings) straddle at 8.6% is the cleaner event read and still sits ~2× history.

**What would change it:** A Q3 guide materially above the $108.73B consensus bar would validate the elevated premium; a straddle repricing below ~6% on Monday would close the gap to history. Reassessment waits on the release itself — guidance vs consensus first.

**Earnings-release teardown (last 48 hours):** None required — no watchlist name reported Nov 12–14 (Nasdaq calendar API). Last reports: TSLA Oct 22, MSFT Oct 29, AAPL Oct 30, NVDA Aug 26.

**UNVERIFIED / gaps:** Straddle prices are Fri Nov 13 close; Monday's open may reprice them materially. Historical moves computed from unadjusted Yahoo daily closes; the three 2026 report dates were taken as NVDA's reported schedule, not re-verified against SEC EDGAR this session. Consensus gap Nasdaq $2.49 vs Yahoo $2.47 is trivial.

---

## 2. Dividend Opportunity desk

**Question:** Which watchlist names go ex-dividend in the next 4 weeks (through Dec 12, 2026), and is there any announced increase, cut, or special?

### Upcoming ex-dividend dates (next 4 weeks)

| Symbol | Ex-date | Pay date | Amount | Yield* | Flag | Consec. increases† | Source | As-of |
|---|---|---|---|---|---|---|---|---|
| MSFT | **Thu Nov 19, 2026** | Dec 10, 2026 | $0.98/qtr | 0.75% | **INCREASE — Sep 15, 2026 raise, $0.91 → $0.98 (+7.7%)** | **24** | Nasdaq calendar API + Yahoo quoteSummary (agree exactly) | Nov 14, 2026 |
| AAPL | Nov 12, 2026 (just passed) | **Nov 16, 2026** | $0.27/qtr | 0.30% | Increase already in effect (Apr 30, 2026 raise, $0.26 → $0.27, +3.8%) | **14** | Yahoo chart + quoteSummary; MarketBeat/Tickeron | Nov 14, 2026 |
| NVDA | None declared | — | $0.25/qtr (current rate) | 0.61% | **INCREASE in 2026 (May 18: $0.01 → $0.25, 25×)** — next ex-date NOT yet declared | 1 (see note) | NVDA 10-Q (SEC EDGAR) + Yahoo chart; next date undeclared per HeyGoTrade Oct 28 | Nov 14, 2026 |
| SPY | None in window | — | ~$1.89/qtr (variable) | ~1.00% TTM | None; Dec quarterly ex-date falls ~Dec 18, outside window | N/A (ETF) | Yahoo chart (last ex Sep 18, 2026) | Nov 14, 2026 |
| QQQ | None in window | — | ~$0.75/qtr (variable) | ~0.45% TTM | None; Dec quarterly ex-date falls ~Dec 22, outside window | N/A (ETF) | Yahoo chart (last ex Sep 21, 2026) | Nov 14, 2026 |
| TSLA | None — pays no dividend | — | $0.00 | 0.00% | None | N/A | Yahoo chart (zero dividend events, 2y) | Nov 14, 2026 |

\* Yields calculated (INFERENCE): annualized current rate ÷ Nov 14 Yahoo regular-market price (MSFT $523.88, AAPL $356.27, NVDA $162.85, SPY $754.37, QQQ $679.89). SPY/QQQ use trailing-4-quarter sums ($7.58 / $3.09).
† Per `~/workspace/hedge-desk-research/dividend-count-standard.md`: count increments on the announcement date; a year with no announced increase breaks the streak.

**Material findings:**
1. **MSFT ex-date is 5 days out — Nov 19, $0.98, pay Dec 10. FACT.** Nasdaq and Yahoo agree on every field. First payment at the raised rate; defining event of the 24th consecutive annual increase (initiated 2003). **Data conflict flagged:** Nasdaq's own `indicated_Annual_Dividend` still shows $3.64 (= 4 × $0.91, old rate) while its `dividend_Rate` shows $0.98 — the indicated-annual field is stale; $3.92 annualized is correct.
2. **AAPL's Nov 12 ex-date just passed; the $0.27 payment lands Mon Nov 16. FACT.** 2026 raise Apr 30, 2026 ($0.26 → $0.27, +3.85%). Count 14 consecutive annual increases per the desk standard (raised every calendar year since the 2012 reinstatement). Note: ChartRow reports 12 because it counts only *complete* calendar years; under the desk standard the count is 14. No drift.
3. **NVDA's 25× dividend step is real and issuer-confirmed, but the next ex-date is undeclared. FACT (raise) / UNVERIFIED (next date).** Form 10-Q (quarter ended Jul 26, 2026): "On May 18, 2026, we increased our quarterly cash dividend from $0.01 per share to $0.25 per share." First payment at the new rate Jun 26, 2026; latest ex-date Sep 10, 2026, paid Oct 1, 2026. Prior Dec ex-dates fell Dec 5, 2024 and Dec 4, 2025; one tracker estimates ~Dec 10, 2026 — an estimate, not a declaration. **INFERENCE on streak:** 1 consecutive annual increase — the $0.01 rate was flat from the Jun 2024 split rebase through Mar 2026, so the 2026 raise starts a new run.
4. **No cuts, no specials, no suspensions anywhere on the watchlist. FACT** (Nasdaq calendar scan Nov 14–Dec 12 returned only the MSFT row among watchlist names; Yahoo 2y histories show no special distributions).
5. **SPY/QQQ December distributions fall outside the window. INFERENCE from pattern, UNVERIFIED as declared dates.** Neither appears in Yahoo calendarEvents yet.

**Verdict:** Thin week for dividend action: the only live event is MSFT going ex Nov 19 at the new $0.98 rate. AAPL's payment lands Nov 16 but the ex-date is past — no capture left. NVDA's next declaration is the one to watch (expected early December on pattern, undeclared as of now). Nothing here changes a margin-of-safety read: yields run 0.30%–1.00%, and the NVDA raise, while 25× in percentage terms, is $1.00/year against a $162.85 share price.

**What would change it:** an NVDA December declaration (date + any further rate change); a declared SPY/QQQ December ex-date inside the window; any board action altering MSFT's Dec 10 payment before Nov 19.

---

## 3. Overnight Premium desk (IV)

**Question:** Is front-end implied vol rich or cheap versus recent realized vol on the watchlist, and is any premium sitting inside a binary event?

**Freshness guard — PASS (within 26h):** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-13-iv-inputs.json`, `as_of` **2026-11-13T14:54:31−07:00**, age ~23.6h at run start — inside the 26h guard. **STALE label applies to its IV levels only:** every `atm_iv` in the file is **null** — the 13:54 PT pull landed after the Nov 13 weekly expiry died (16:00 ET) and the post-expiry guard failed closed on all six symbols. The file's realized vols and window flags are current through the Nov 12 close and are used below.

### IV snapshot — live Yahoo supplement (labeled live pull, not the file)

Live pull Sat 2026-11-14 ~13:29 PT via cookie+crumb handshake; markets closed, so quotes are the Fri Nov 13 close. Nearest *unexpired* expiry used (the Nov 13 weekly is dead). ATM IV = mean(call IV, put IV) at the strike nearest spot. Raw JSON saved at `~/workspace/goals/hedge-desk-daily-research/hidden_files/live_iv_2026-11-14.json`.

| Symbol | Spot (Nov 13 close) | ATM IV, nearest unexpired expiry | ATM IV, next expiry | 20d realized (file, thru Nov 12) | Max 1-day var share | Window |
|---|---|---|---|---|---|---|
| SPY | 754.37 | 11.77% — Nov 16, 2 DTE (call 8.66 / put 14.89) | 14.11% — Nov 17, 3 DTE | 22.88% | 54.35% | **CONTINGENT** |
| QQQ | 679.89 | 20.72% — Nov 16, 2 DTE (16.44 / 24.99) | 25.34% — Nov 17, 3 DTE | 36.70% | 46.54% | **CONTINGENT** |
| AAPL | 356.27 | 15.34% — Nov 16, 2 DTE (15.61 / 15.06) | 19.73% — Nov 18, 4 DTE | 28.26% | 46.37% | **CONTINGENT** |
| MSFT | 523.88 | 21.22% — Nov 16, 2 DTE (20.74 / 21.70) | 28.83% — Nov 18, 4 DTE | 37.50% | 41.62% | **CONTINGENT** |
| NVDA | 162.85 | 49.06% — Nov 16, 2 DTE (47.95 / 50.17) | **92.50% — Nov 18, 4 DTE** | 55.43% | 37.27% | **CONTINGENT** |
| TSLA | 390.22 | 36.68% — Nov 16, 2 DTE (35.72 / 37.63) | 46.39% — Nov 18, 4 DTE | 62.08% | 46.07% | **CONTINGENT** |

**IV-rank — UNVERIFIED for all six.** No free IV-history source is available, and the iv-inputs files' ATM IVs are null across the recent streak, so no 52-week IV rank can be computed. Never guessed.

**IV-vs-realized verdict — WINDOW-CONTINGENT for all six (no clean verdict).** FACT: every ATM IV above sits below its 20-day realized vol. INFERENCE blocked from a clean verdict: every window is WINDOW-CONTINGENT — a single day drives 37–54% of 20-day variance (the Nov 5 crash day), above the 30% desk threshold. The realized vols are jump-inflated, so "IV below realized" does **not** cleanly mean premium is cheap. What would change it: the window rolling past Nov 5 (after ~Dec 3) or a fresh 20-day window with no single day above 30% of variance.

**Elevated-IV flags:**
- **NVDA — elevated, but expected, not "rich" (FACT, with INFERENCE):** 49.06% at 2 DTE rising to 92.50% at 4 DTE is a textbook earnings hump — the Nov 18 expiry is the first expiry after the Nov 17 earnings event. Elevated IV into a known binary event is expected pricing, not a mispricing.
- **TSLA — elevated in absolute terms (36.68% / 46.39%), consistent with its own history (FACT):** its 20-day realized is 62.08%, the highest on the watchlist; no richness claim can be made while its window is contingent.
- **SPY / QQQ / AAPL / MSFT — no elevated-IV flag.** Front-end IVs of 12–29% are unremarkable against their realized vols; SPY and QQQ show steep downside skew (put IV well above call IV: SPY 14.89% vs 8.66% at 2 DTE; QQQ 24.99% vs 16.44%) — FACT, consistent with normal equity skew after a down week, not a standalone signal.

**Earnings-in-window warning — NVDA, Nov 17.** NVDA reports 2026-11-17, inside the Nov 18 expiry window — that is exactly what the 92.50% print is pricing. **Premium into this binary event = avoid** (front-week premium selling on NVDA). Date corroborated by the Earnings desk (Nasdaq calendar API + Yahoo calendarEvents); the IV desk's own Yahoo v7 quote check for the date 404'd, but the IV hump itself corroborates an event inside the Nov 18 window (INFERENCE, strong: +43.4 vol points Nov 16 → Nov 18 cannot be explained by 2 extra days of ordinary term structure). No other watchlist name has earnings in the window.

**Sanity checks:** All IVs positive and finite; term structure rises front-to-back in every name. Stale-quote caveat (FACT): Saturday pull on Friday-close marks. Two crossed quotes observed — NVDA Nov 16 call bid 3.10 > ask 3.00; TSLA Nov 16 call bid 5.20 > ask 5.15 — stale-mark artifacts. ATM IVs come from Yahoo's solver IVs, not those marks, but treat the 2-DTE prints as close-marks, not live quotes. Put-call parity not independently verified this run (no rate/dividend inputs pulled); no parity violation is asserted.

**Null-streak note (standing, since 2026-10-22):** The iv-inputs file's ATM IVs are null again (Nov 13 pull, post-expiry guard — the 7th consecutive null context dating to Oct 20). Today's live supplement succeeded only because it used the nearest *unexpired* expiry. The pull-switch decision remains pending; the file's nulls stand as the official record and the live levels above are a labeled supplement, not a replacement.

---

## 4. Open Quant/AI Model Lab

**Question:** What new papers, preprints, or methods in the last ~7 days are worth the desks' attention, scored on the repo's own rubric?

**Sweep scope (FACT, arXiv listing read at source 2026-11-14 21:30 UTC):** Friday 13 Nov 2026 announcement — 19 new + 9 cross-list q-fin submissions, closing the Nov 10–13 window. GitHub leg skipped per the run brief (no GitHub operations). SSRN leg not run this cycle. Coverage note: the arXiv API's submittedDate-descending top-40 missed 7 of the 19 new items — the listing page is now the coverage control, not the API top-40. Nov 13 submissions announce Mon 16 Nov — next run re-covers the Nov 13–15 window.

### New candidates (all scored with the repo module `hedge_desk.research_intelligence.assess_source`; all claims source-reported from abstracts, UNVERIFIED beyond abstract level)

| # | Candidate | Venue / Date | Score | Disp. | Reason |
|---|---|---|---|---|---|
| 285 | Gençay — "Can a search hold its own bar? In-loop deflation and its exploits in autonomous strategy discovery" | arXiv:2611.14539v1, submitted 14 Oct 2026, announced 13 Nov | 51 | **WATCH** | In-loop deflated-Sharpe bars admit a variance-dilution exploit (near-duplicate candidates lower the bar); proposes pre-registered variance floor + monotone high-water-mark bar. Direct hit on the desk's purged-validation lane. No code link → reproducibility not established. |
| 286 | Graeber/Roth/Sammon/Schesch — "Huge If True: Learning from the Size of the Surprise" | arXiv:2611.15747v1, submitted 11 Nov 2026, announced 13 Nov | 51 | **WATCH** | Earnings-surprise response under multiplier uncertainty: greater uncertainty attenuates the average response but steepens it near zero. Incentivized experiment + real earnings announcements. Earnings-desk prior for how surprise size maps to move size. No code link. |
| 287 | Zarei et al — "Conformal Risk Certificates for Portfolio Optimization Under Uncertainty: A Gated RL Approach" | arXiv:2611.14699v1, submitted 10 Nov 2026, announced 13 Nov | 34 | **ARCHIVE** | Gated PPO + LLM semantic risk states on 9 sector SPDR ETFs; portfolio-optimization lane, not options/vol/earnings/dividend; LLM stack not desk-adoptable. |
| 288 | Feng et al — "Track or Follow? A Jev-Compatible Multi-Agent Trading System When Web News Lags the Market" | arXiv:2611.10414v1, submitted 7 Nov 2026, announced 13 Nov | 48 | **WATCH** (band floor) | Negative result: 72% of earnings news appears AFTER the issuer's filing; news-reaction association falls to 0.023 from the first trade after publication; no weekly rank info over code-only features. Desk rule: grade any news-based signal from publication, not from the event. No code link in arXiv record. |

**Ledger:** all four appended as rows #285–288 to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (verified on disk, one copy each), plus a jidoka-log entry for this run. Triage exclusions (no rows): 2611.14708, 2611.14938, 2611.15017, 2611.15371, 2611.15430, 2611.16058, 2611.16095, 2611.16657, 2611.16747 — all out of scope.

**Re-checks (FACT, arXiv API id_list):** core version-triggered WATCH set #4/#9/#13/#14/#15/#20/#21/#30/#31 — no version movement, all stay WATCH. #25 (Han et al) still v4 (updated 2026-11-10). #257 (2611.13616) now v2 (updated 2026-11-12) — ARCHIVE, no disposition change.

**Worth immediate desk attention:** #288 (Feng et al) — the 72%-post-filing / 0.023 finding is the sharpest item this run: a standing caution against any web-news earnings signal the desks might adopt, and its hash-committed, publication-time-graded test design is a template worth borrowing. #285 (Gençay) is second: if the desk ever automates strategy search, its in-loop bar needs the variance-floor / high-water-mark defences.

**What would change the verdicts:** peer review or a code/data release on #285/#286/#288 (all currently WATCH on abstract-only evidence, reproducibility not established); a full-paper read confirming the defences in #285 are implementable rules and the surprise-response curve in #286 is quantitative, not just a shape.

**Bottom line:** no TEST or INTEGRATE movement this run (max score 51). Nothing new and material beyond the two WATCH items above.

---

## 5. Weather / War / Logistics Futures Event desk

**Question:** What fresh catalysts moved energy, grain, and shipping futures this week, and what are the curves pricing?

**As-of:** Sat 2026-11-14, ~13:30 PT (futures settles Fri 2026-11-13).

### Catalyst triage

| Event | Date/time | What happened | Source | Label |
|---|---|---|---|---|
| EIA Weekly Petroleum Status Report, week ending Nov 6 — released **Thu Nov 12 ~12:00 ET**, a day late (Veterans Day) | Nov 12 | Crude **+4.657M bbl to 414.4M** (vs Reuters poll ~−1.1M draw; prior week −0.865M); gasoline **+1.8M to 210.8M** (~1% above 5-yr avg); distillate **+4.1M to 103.3M** (still ~8% below 5-yr avg); Cushing +0.106M to 27.4M; refinery runs 17.0M bpd, 95.2% util.; imports +325k bpd to 6.7M bpd; total commercial petroleum +11.4M bbl. US production **record 14.013M bpd**. SPR 279.5M bbl. API survey Tue had shown +8.97M crude. | EIA WPSR via Reuters/OilPriceAPI | **FACT** |
| EIA Short-Term Energy Outlook | Tue Nov 10 | Brent expected **~$100/bbl in Nov–Dec**; Middle East crude production outages averaged **2.5M bpd in Oct vs 10.9M bpd May peak**; global liquid-fuels consumption 2026 seen **down 2M bpd y/y to 102.4M bpd**; global inventories expected to begin building in Q4. | EIA STEO via Goodman Macro, Nov 11 | **FACT** (consumption figure single-source, as reported) |
| IEA Oil Market Report | Fri Nov 13 | Oil market expected to **return to surplus in Q4**, supply ahead of demand; global supply **+2.3M bpd in Oct to 105.36M bpd**, driven by Gulf producers; Russian output **+210k bpd to 8.73M bpd**; IEA raised 2026 supply estimates by ~920k bpd. | IEA via Reuters/Bloomberg | **FACT** |
| OPEC+ output | Oct (reported this week) | Output **+1.96M bpd to 27.16M bpd** in October. Next OPEC+ meeting **Sun Nov 29** (output unchanged Nov 1). | BMCE Capital via HDFC Sky, Nov 14 | **FACT** |
| USDA WASDE-677 | Tue Nov 10, 12:00 ET | Corn yield cut 1.6 bu to **179.6 bpa**; production **15.893B bu (−141M)**; ending stocks **1.758B bu** (vs 1.846B trade avg, 1.849B Oct). Soybean yield 53.3 bpa (+0.2); production 4.574B bu; ending stocks **300M bu** (vs 332M expected, 315M Oct); exports +25M bu. Wheat ending stocks 743M bu (+3M). Cotton 13.18M bales (−267k). Beef production cut; pork up. Last yield update for corn/soy until January. Next WASDE **Dec 10**. | USDA WASDE-677 via DTN/RFD-TV/Feed & Grain, Nov 10 | **FACT** |
| EIA Weekly Natural Gas Storage, week ending Nov 6 — released **Fri Nov 13, 10:30 ET**, delayed by Veterans Day | Nov 13 | Injection **+61 Bcf to 3,862 Bcf** (vs 67 Bcf WSJ survey, 77 Bcf prior week); **75 Bcf above 5-yr avg (3,787 Bcf), 92 Bcf below year-ago**. Regional: South Central +27, Midwest +18, East +12, Mountain/Pacific +2 each. Next release Thu Nov 19. | EIA via IndexBox; WSJ | **FACT** |
| Strait of Hormuz — tanker mine claims | Wed Nov 11 – Fri Nov 13 | Iran's navy (Nov 11) and IRGC Navy (Nov 12–13) claimed tankers struck naval mines / explosions: Nov 11 a tanker caught fire after a mine strike (no name given); Nov 12 claims of **four tankers** hit by explosions; Nov 13 an LPG/LNG carrier mine strike, then **two oil tankers** exploding after mine strikes. **None independently verified** — Reuters could not confirm; UKMTO logged a Nov 11 tanker incident without confirming cause/vessel; US Central Command disputed the mine narrative. Separately, UKMTO Nov 10: VLCC *Fujairah Energy* hit by projectile, 4 crew injured. Washington Institute data via Reuters: **≥10 ships hit in first 10 days of Nov; 37 attacks in Oct**; IMO ~134 incidents since Feb, 25 seafarers dead; Hormuz traffic **~65% below pre-war levels** (UKMTO). | Reuters via multiple outlets, Nov 11–14 | **FACT that the claims were made; UNVERIFIED whether the mine strikes occurred as claimed** |
| Houthi–Saudi exchanges | Tue Nov 11 – Fri Nov 13 | Houthis claimed missile strikes on Riyadh (King Khalid Intl Airport), Abqaiq/pumping stations, and drone strikes on Saudi East-West pipeline Pumping Stations 3 and 7 (~4M bpd Hormuz-bypass route to Yanbu); Saudi-led coalition said it intercepted missiles/drones aimed at Riyadh. **Saudi authorities have not confirmed the Houthi claims.** Houthis also fired two ballistic missiles toward Al-Tuwal, Jazan, Fri Nov 13. | Reuters/Dawn, Nov 11–14 | **FACT that claims/intercepts were reported; UNVERIFIED whether strikes hit their targets** |
| Abu Dhabi talks (Russia–Ukraine–US) | Wrapped Wed Nov 11 | Prisoner exchange agreed; **no announcement on Black Sea shipping**. | PGI Klarenbach grain report, Nov 11 | **FACT** |
| US–Iran standoff | Ongoing, Fri Nov 13 | President Trump maintaining blockade on Iran (Truth Social); US–Iran deal uncertainty cited as the offset to the bearish EIA build in Thursday's rally. No deal announced as of Fri close. | Maaal, Nov 14; XTB, Nov 12 | **FACT** (blockade stance as reported); deal outcome **SPECULATION** |

### Futures curve reads (Friday Nov 13 settlements, verified)

- **WTI (CL=F, Dec-26): $88.56, −$0.18 (−0.2%) Fri; −~2.5% on the week, second straight weekly decline.** Week range: low $83.88, prior-week close $90.35. Thu Nov 12: +2.55% to $88.74 on the Hormuz/Houthi claims. **INFERENCE:** the market is pricing a war-risk premium that is real but fading — Brent is ~20% below its late-October high near $118.
- **Brent (BZ=F, Jan-27): $95.84, +$0.02 Fri; −~2.5% on the week.** Thu Nov 12: +3.3% to $95.82. **Brent–WTI spread $7.28** at Friday close.
- **Curve shape — crude: steep backwardation (FACT, corroborated).** Yahoo v8 chart serves only front-month futures symbols, so deferred levels below are from secondary curve reporting, not a direct Yahoo pull: WTI Dec-26 $88.74 vs Jan-27 $87.69 at Nov 12 settles, prompt Dec/Jan spread ~**+$1.05/bbl, top decile since 2010**; Brent Jan-27 vs Dec-27 spread **>$15/bbl**; WTI strip falls to ~$53 by 2033–36. Physical cash confirms it: WTI cash $92.53 vs front futures, +$3.97 backwardation. **INFERENCE:** prompt barrels still command a premium — physical tightness now, with the market pricing normalization lower over time; nobody is paying to store crude yet.
- **Nat gas (NG=F, Dec-26): $3.230, −3.3% Fri but +7.7% on the week.** Cash $3.202 vs futures — **contango, loose**. EIA STEO still expects Henry Hub to average just **$2.87/MMBtu this winter** on mild weather, ample storage, rising output — i.e., the official view treats this week's rally as borrowed time. First nor'easter of the season is the near-term demand test.
- **Grains (Yahoo v8 chart, Fri Nov 13 closes): corn Dec-26 445.5¢/bu; soybeans Jan-27 1,231.5¢/bu ($12.315); Chicago wheat Dec-26 593.25¢/bu.** Jan soybeans rose $0.39¾ to $12.28 on WASDE day (Nov 10). **INFERENCE:** WASDE's below-consensus corn (1.758B bu) and soybean (300M bu) ending stocks are the tightest US balance-sheet prints of the season and set the floor into year-end; deferred grain curve shape **UNVERIFIED** — Yahoo serves only front-month grain symbols and no deferred quotes were confirmed this run.
- **Logistics:** Hormuz shipping ~65% below pre-war levels; Etihad Abu Dhabi–Riyadh/Dammam flights cancelled through Nov 19. No verified closure of the strait; traffic continues under elevated risk.

### Verdict

**Thesis:** The week was a tug-of-war the bears won on flat price but not on curve structure — a second straight ~2.5% weekly decline in crude on a surprise EIA build, IEA's Q4 surplus call, and OPEC+ supply growth, against a Thursday +3.3% spike on unverified Hormuz mine claims and Houthi attacks on Saudi infrastructure. The curve says the physical market is still tight *now* (steep backwardation, $1.05 prompt WTI spread, cash $4 over futures) while pricing a looser future (strip sliding toward the low-$50s–$60s). Grains tightened on paper: November WASDE cut both corn and soybean ending stocks well below trade estimates, with no further yield update until January. Nat gas is the mirror image — a +7.7% week on cold, but storage 75 Bcf above the 5-yr average and EIA's $2.87 winter Henry Hub forecast argue the rally is weather, not structure.

**What would change it:** (1) Independent confirmation (UKMTO/shipowner/USCENTCOM) of Hormuz mine strikes or an actual strait disruption — would reprice the war premium up fast; (2) next WPSR Wed Nov 18 — a second consecutive build, especially at Cushing into Dec WTI expiry Fri Nov 20, would undercut the prompt backwardation; (3) OPEC+ Nov 29 — any output change; (4) next gas storage Thu Nov 19 — a sub-consensus build/withdrawal as the nor'easter bites; (5) next WASDE Dec 10.

**UNVERIFIED / gaps:** deferred crude/grain contract levels beyond the reported spreads above; whether any Hormuz tanker actually struck a mine; whether Houthi missiles/drones hit Riyadh airport, Abqaiq, or pipeline pumping stations; the IEA's exact 2026 demand-growth figure as carried by one secondary source (omitted — not independently confirmed). No USDA releases are due before Dec 10 WASDE; no EIA release is due before Wed Nov 18 WPSR.

**Forward calendar:** WPSR Wed Nov 18, 10:30 ET · Gas storage Thu Nov 19, 10:30 ET · Dec WTI expiry Fri Nov 20 · OPEC+ Sun Nov 29 · EIA STEO Tue Dec 8 · WASDE Thu Dec 10.

---

## 6. Box / Parity Observer

**One material item: CBOE launched SPXO, AM-settled SPX weeklies, effective trade date Mon Nov 9, 2026 (FACT, CBOE via FX News Group, Sep 4, 2026).** New symbol SPXO, same SPX underlying, AM-settled to the SPX opening settlement price (SET) like third-Friday SPX — but with price-time allocation (SPX stays pro-rata), a minimum quote size of 1, and no separate TPH risk limits (SPXW keeps separate limits; SPXO does not). Parity-relevant microstructure note: complex orders may combine any two of SPX/SPXO/SPXW, but SPXW combined with SPX or SPXO cannot leg into the single-leg books because the books sit on separate matching units — so cross-symbol box/conversion legs face an execution friction that same-symbol boxes do not (INFERENCE from the stated matching-unit structure). SPXO trades in Global Trading Hours, but trading ceases at 4:00pm ET on the final day before AM settlement with no evening GTH session. No index-methodology change to SPX itself was found — this is a new listing/settlement convention, not a reweighting.

**Parity check — no violation found.** Saxo's daily options briefs (Nov 4 and Nov 5, 2026) report put-call parity on the Nov 18 VIX options holding within a few cents of settlement: parity-implied 17.73 vs 17.74 settlement (Nov 4 close) and 19.96 vs 19.90 (Nov 3 close) (FACT, Saxo/Bloomberg/CBOE). No published box-spread or put-call parity violation analysis in the last ~2 weeks surfaced in the sweep (crypto-only scanner Optionly shows only sub-0.3% BTC conversion edges on Derive/Deribit, not equity-index parity — not watchlist-relevant).

**Box-spread rates vs Treasuries — no current print verifiable.** Latest dated print: Tulan Capital (Oct 20, 2026, CFA author) puts Dec 2026 SPX boxes at ~4.3–4.4% for ~2 months vs ~4.1% 1-month Treasury (FRED) — i.e. roughly 20–30bp over bills, consistent with CBOE's whitepaper range of 10–55bp over 3-month bills (FACT, dated Oct 2026, now ~3.5 weeks stale). No Nov 14 SPX box rate could be verified from free sources today — boxtrades.com publishes no dated current quote in search results and CBOE's Box Rate indices were not pulled live this session — **UNVERIFIED for today; do not quote a current box rate.** SPY 30-day ATM IV 15.7% (Nov 13 close, 70th percentile since 2024) is noted for context only, not a parity input.

**Scope checked:** CBOE index/product notices, box-spread rate sources (boxtrades.com, Tulan Capital, CBOE whitepaper, boxloancalc.com), parity-violation/arb scanners, Saxo options briefs Nov 3–5. Nothing else material.

**Bottom line:** No parity violation; one structural item to watch — SPXO's Nov 9 launch adds an AM-settled weekly with different allocation and legging constraints, which matters for any future SPX box/conversion construction.

---

## 7. Bonds & Rates desk (Desk 7 — consolidated deliverable)

**Status:** Worked from the consolidated deliverable (`desk7-core-indicators.md`, Nov 13 snapshot). Module ran clean this session in `REAL_FRED_RATES` mode; all 10 core indicators re-pulled fresh from FRED this session via the repo's `rates_desk.fred_series_rows`. No kept indicator printed new data since Nov 13 — the changes are in market yields and market pricing. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; UNVERIFIED = looked, could not confirm.

### 1. Rates table (FRED, module pull `rates_desk.rates_environment()`, as_of 2026-11-14; latest obs Nov 12 — Nov 13 DGS obs not yet posted in FRED at pull time)

| Series | Read | As-of |
|---|---|---|
| Effective fed funds (DFF) | 3.88% | Nov 12 |
| 2Y Treasury (DGS2) | 4.86% | Nov 12 |
| 10Y Treasury (DGS10) | 5.10% | Nov 12 |
| SOFR | 3.90% | Nov 12 |
| EFFR | 3.88% | Nov 12 |
| Overnight bank funding rate (OBFR) | 3.88% | Nov 12 |

**2s10s slope: +24bp** (5.10 − 4.86), curve UPWARD_SLOPING. Direction of change: **narrowed 1bp since Nov 10** (25bp → 24bp) and 11bp since Nov 6 (35bp → 24bp) — the front end rose faster than the long end as the December hike repriced. Both legs up hard on the week: 10Y 4.86% (Nov 6) → 5.10% (Nov 12), +24bp; 2Y 4.51% (Nov 6) → 4.86% (Nov 12), +35bp. Since the Nov 13 snapshot: 10Y +12bp (4.98 → 5.10), 2Y +13bp (4.73 → 4.86).

**SOFR vs EFFR funding spread: +2bp** (3.90 − 3.88). No funding stress — SOFR sits on top of EFFR, not gapping above it. (FACT, FRED.)

Note: press reports put the 2Y close on Fri Nov 13 at ~4.87% — consistent with the FRED Nov 12 read but UNVERIFIED from FRED, whose Nov 13 DGS obs had not posted at pull time.

### 2. Core-indicator table (fresh FRED pull this session unless noted)

| Indicator | Trigger rule | Today's read | Signal | Broker POV |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA via FRED) | HIKE if y/y > 2.5% or m/m > +0.25%; CUT if y/y < 2.2% | y/y +3.121%, m/m +0.317% (130.902, Sep 2026; Sep 2025 126.94, Aug 130.489). Unchanged from Nov 13. | **HIKE** | Anchor the discount rate to the higher regime. The decision variable is PCE; the next print (Oct PCE, Nov 25, date provisional) is the re-anchor date. |
| Breakevens (T5YIE / T10YIE, FRED) | HIKE if > 2.75%; CUT if < 1.75%; NEUTRAL 2.0–2.5% | 2.30% / 2.24% (Nov 13). Unchanged. | **NEUTRAL** | Anchored expectations: room for 25bp, not a forced 50bp. Tripwire is a break above 2.75%. |
| Michigan expectations (MICH, U-M) | HIKE if yr-ahead > 3.5%; CUT if < 2.5% | 4.3% yr-ahead, Nov prelim (rel. Nov 6). Carried forward from Nov 13 — FRED MICH lags ~2 months (latest FRED obs Sep 4.6%) and is not the current read. | **HIKE** | Do not average with breakevens: 4.3% vs 2.24% is a credibility gap the Fed reads as pressure to act. |
| Payrolls, 3-mo avg (PAYEMS, BLS via FRED) | HIKE if 3-mo avg > +150k; CUT if < +50k | 3-mo avg +137k (Jul→Aug +186k, Aug→Sep +60k, Sep→Oct +165k; Oct level 159,293k). Unchanged. | **NEUTRAL** | Rule as written: NEUTRAL. The single +165k print does not override the average. |
| Initial claims, 4-wk avg (ICSA, DOL via FRED) | CUT if 4-wk avg > 300k; NEUTRAL < 250k | 200k w/e Nov 7; 4-wk avg 195,250. Unchanged. | **NEUTRAL** | No action. Check every Thursday: a 4-wk average above 300k flips the labor read to CUT before payrolls confirm. |
| Job openings (JTSJOL, BLS via FRED) | HIKE if 3-mo change positive; CUT if −500k over 3 months | 7,523k, Sep 2026 (Jul 7,335k → +188k over 3 mo). Unchanged. | **HIKE** | Demand has not rolled over: rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA via FRED) | HIKE if > 2.5% annualized; CUT if < 1.0% | Q3 +3.37% annualized (24,611.077 vs Q2 24,408.011). Unchanged. | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Growth is backdrop, not trigger — PCE, claims, and the minutes are the prints that can move the call before Dec 9. |
| Housing starts (HOUST, Census via FRED) | CUT if −5% over 3 months; HIKE if rising through high rates | 1,221k; −10.8% Jul→Sep (Sep 2026). Unchanged. | **CUT** | Report it, don't bury it: the evidence a hold argument would cite, and why the call is 25bp, not 50bp. |
| High-yield OAS (BAMLH0A0HYM2, ICE BofA via FRED) | CUT if > 5.00%; NEUTRAL < 4.00% | 3.20% (Nov 12; Nov 13 obs not yet in FRED). Unchanged. | **NEUTRAL** | No stress: the market is neither doing the Fed's tightening work nor forcing an easing response. Watch is a break above 5.00%. |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening or language turns hawkish; CUT if the reverse | Oct 28: held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; statement: "Inflation remains elevated." Unchanged. | **HIKE** | Weight the vote above any single print. The Nov 18 minutes are the check on whether 10–2 understates division. |

**Tally: 5 HIKE / 1 CUT / 4 NEUTRAL — unchanged from Nov 13.** No kept indicator changed signal this session.

**New guidance color since Nov 13 (INFERENCE, single-basis press reports — not verified against federalreserve.gov):** Fri Nov 13, Boston Fed's Collins told Bloomberg TV a "careful adjustment" was her best case and declined to say how high or how fast; Chicago's Goolsbee told CNBC the same morning without signaling speed. Neither votes in 2026. Earlier in the week, Gov. Waller (Nov 10, London) said a 50bp December hike should be considered if core CPI printed ~0.3% or higher — and October core CPI did print +0.3% — while Dallas Fed's Logan called for at least two more quarter-point rises. Net: no named voice for a hold has appeared; the 50bp tail now has a named mechanism (Waller's trigger, met), not just market drift. One press claim in the same coverage asserts October 2025 data went uncollected during a government shutdown — that contradicts the standing verified rule (no shutdown; CR passed Sep 1, signed Sep 2, funding through Dec 11) and is NOT adopted; no shutdown framing is used.

### 3. Market pricing vs indicators

**Kalshi, direct API pull this session (Sat Nov 14 ~13:35 PT, event `KXFEDDECISION-26DEC`):** 25bp hike $0.88 (bid/ask 0.88/0.89, prev 0.88), more than 25bp $0.11 (0.10/0.11, prev 0.12), hold $0.04 (0.03/0.04, prev 0.03), 25bp cut $0.01, more than 25bp cut $0.01. Five lasts sum to $1.05 (same 5-cent over-round as Nov 13). **Total hike $0.99** (was $1.00 Nov 13) — a 1-cent drift, hold ticking up a cent: noise, not signal.

**CME FedWatch (secondhand, Nov 14 morning reads):** 25bp 88.5%, 50bp 11.5%, hold/cut 0% — agrees with Kalshi (88/11) on direction and tail. Polymarket secondhand: 25bp ~88%, 50bp ~9%.

**Disagreements named:** markets and indicators agree on direction (hike) and on the tail's size (~11–12% for >25bp). The remaining disagreement is the same as Nov 13: the indicator set votes direction, not size — no rule distinguishes 25bp from 50bp. The new element is Waller's stated trigger: the 50bp tail is now traceable to a governor's explicit condition that the data met, which is a stronger basis for the tail than the Nov 13 "market-driven repricing" read. The tail did not grow on it ($0.12 → $0.11), so the market is treating Waller's trigger as a live possibility, not a base case.

### 4. Verdict — call UNCHANGED: 25bp hike on Dec 9

- **Thesis:** Core PCE at 3.12% y/y against a 2% target, no labor deterioration on any kept read, above-trend growth, and a 10–2 hold vote with two dissents for an immediate hike all point one way. Markets price the hike at $0.99 combined and the 25bp size at $0.88. The call is 25bp, not 50bp, because housing starts (−10.8% over 3 months) is the live counter-evidence and no indicator rule separates the two sizes.
- **Evidence:** 5 HIKE / 1 CUT / 4 NEUTRAL across the 10 core indicators (all re-pulled from FRED this session); 2Y +35bp and 10Y +24bp on the week as the market repriced the hike in; Kalshi total hike $0.99; FedWatch 88.5% / 11.5%.
- **What would change it:** October core PCE (Nov 25, date provisional) at m/m ≤ +0.15% with a downward revision to September; initial claims 4-week average above 300k; the November 18 minutes, or a named speaker arguing for a hold, showing the Committee more worried about overtightening than the 10–2 vote suggested. A named 50bp endorsement from a voter would move the size call, not the direction call.

### 5. Graham lens (updated)

10Y 4.98% (Nov 10) → 5.10% (Nov 12). At assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) falls 50.51x → 47.62x, **−5.72%** — arithmetic, not opinion. Duration ≈ 8 puts the same +12bp move at about −0.96% on a 10-year position (approximation; ignores convexity). The margin of safety is thinner at the same prices: any intrinsic-value estimate carried at the old 4.98% anchor overstates value by ~6% on this sensitivity. **Re-anchor to 5.10%.** Earnings-yield vs bond-yield spread: UNVERIFIED — bond side verified (5.10%); earnings side unverified from any primary source this session. No live spread is asserted. The defensive read stands: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price.

### 6. What changed since Nov 13 (summary)

1. Yields: 10Y +12bp to 5.10%, 2Y +13bp to 4.86% (Nov 12 FRED obs); 2s10s 25bp → 24bp; SOFR−EFFR +2bp, no funding stress.
2. Kalshi: total hike $1.00 → $0.99; 25bp flat at $0.88; >25bp $0.12 → $0.11; hold $0.03 → $0.04.
3. FedWatch: 88.5% / 11.5%, in line with Kalshi.
4. Speakers: Collins + Goolsbee Fri Nov 13 (cautious, no speed signal); Waller's Nov 10 50bp trigger (met by core CPI +0.3%) now the named mechanism behind the tail — single-basis press reports.
5. No kept indicator printed new data; tally unchanged at 5 HIKE / 1 CUT / 4 NEUTRAL. Next data that can move the call: Oct 27–28 minutes Nov 18, Oct PCE Nov 25 (provisional), November jobs report before Dec 9 (date unconfirmed), November CPI Dec 10 (after the decision, cannot change December).

**Desk status: COMPLETE.** Module succeeded; all 10 indicators pulled fresh from FRED this session; market pricing pulled direct from Kalshi this session. UNVERIFIED items: FRED Nov 13 DGS obs (not yet posted at pull time; 2Y Nov 13 close ~4.87% press-reported only); HY OAS Nov 13 obs (not yet in FRED); FedWatch read secondhand (no public text API); Waller/Logan/Collins/Goolsbee remarks single-basis press reports, not verified against federalreserve.gov; earnings-yield spread (no earnings-side source this session).

---

## Cross-desk notes (synthesis)

- **NVDA date resolved:** the IV desk's Yahoo v7 quote check for the earnings date 404'd; the Earnings desk verified Tue Nov 17 after close via Nasdaq calendar API + Yahoo calendarEvents, and the IV hump (92.5% at Nov 18) corroborates an event inside that window. Date stands as FACT.
- **The Nov 5 jump still dominates every vol read:** all six 20-day realized windows are WINDOW-CONTINGENT (37–54% single-day variance share). No clean IV-vs-realized verdict this run; the window rolls past Nov 5 after ~Dec 3.
- **Rates vs premium desks agree:** the discount-rate anchor moved up (10Y 5.10%) while front-end IVs ex-NVDA are unremarkable — no vol signal contradicts the rates call.
- **No parity violation; SPXO launch (Nov 9) is the structural watch item** for any future SPX box/conversion construction.
- **Quant lab:** 4 new candidates appended to the ledger (#285–288); #288 (72% of earnings news appears after the filing) is the caution most relevant to the Earnings desk's sourcing discipline.

## Desk status
All seven desks delivered: Earnings ✓ · Dividend ✓ · Premium IV ✓ · Quant Lab ✓ · Futures Events ✓ · Box/Parity ✓ · Bonds & Rates ✓. No desk FAILED. No retry needed.

## Sources
Nasdaq earnings/dividends calendar APIs; Yahoo Finance v7 options, v10 quoteSummary, v8 chart (cookie+crumb where required); SEC EDGAR (NVDA 10-Q); FRED via `hedge_desk.rates_desk` (REAL_FRED_RATES); Kalshi API (`KXFEDDECISION-26DEC`); EIA WPSR/STEO; USDA WASDE-677; IEA Oil Market Report; arXiv q-fin listings; CBOE product notices; Saxo options briefs. Full per-item sources in each desk section above.
