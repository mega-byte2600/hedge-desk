# Hedge-Desk Daily Research — Sunday 2026-11-08

**Run:** 13:30 PT, Sun 2026-11-08 (markets closed; all prices Friday 2026-11-06 close unless noted).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; never risk-seeking framing.
**Method:** seven parallel desks; every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**Government data:** NO federal shutdown — CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11. No "data blackout" framing applies. (FACT)

---

## Decision-relevant items (top 5)

1. **NVDA Nov 17 earnings is the only watchlist earnings in the next two weeks, and the market prices ~11.2% — roughly double the ~5% historical average move.** FACT (Nasdaq calendar + Yahoo v7 options, re-verified today). Event-isolated move ~6–7% after corrected time-scaling. Premium into the binary event = avoid. Last print moved +8.74%.
2. **All six IV-vs-realized verdicts are WINDOW-CONTINGENT — no clean "IV cheap" read anywhere.** FACT (2026-11-07 iv-inputs file). The Nov 5 crash day still drives 46–63% of every 20-day realized window; the flag persists until that return rolls out (~early Dec). Any premium-selling thesis built on IV < realized is standing on one day.
3. **Oil's ~13% weekly collapse is the week's dominant futures event — sentiment-led, not inventory-led.** FACT (Yahoo v8 chart, Fri Nov 6 close). WTI $90.83 / Brent $98.32 after the steepest weekly drop since 2022, driven by midterm + Qatari-mediation de-escalation bets — yet US crude stocks (409.8M bbl) are below every comparable week since 2021 and oil vol is still 58.3. Next physical check: EIA petroleum report Thu Nov 12 (12:00 ET, Veterans Day shift).
4. **Front-end rates rally Thursday is the week's rates story: 2Y −12 bp to 4.46%, 2s10s steepening to +38 bp.** FACT (FRED via repo rates module, as of Nov 5 — Friday's prints not yet published). SOFR–EFFR +4 bp: no funding stress. Mild tailwind for growth names and premium pricing; not a low-rate regime.
5. **AAPL goes ex-dividend Thu Nov 12 ($0.27, flat); MSFT ex Thu Nov 19 at the raised $0.98 — and Nasdaq's header yield still shows the stale pre-raise 0.68%.** FACT. Forward MSFT yield ~0.74% at the Nov 6 close; any screen quoting 0.68% understates it by ~0.06pp.

---

## 1. Earnings Event desk

**Question:** Which watchlist names report earnings in the next two weeks (through Sun Nov 22, 2026), and what does the options market price for the move versus history?

| Symbol | Date | Timing | Consensus EPS | Options-implied move | Historical avg earnings-day move | Evidence |
|---|---|---|---|---|---|---|
| NVDA | Tue 2026-11-17 | After close (call ~5:00 PM ET) | $2.49 (Nasdaq, 13 ests) | ~11.2% via Nov-20 ATM straddle ($20.88 / $186.64 spot); event-isolated ~6–7% | ~5% avg absolute move, last 10 reports; last print +8.74% (verified) | FACT — Nasdaq calendar API + Yahoo v7 options |
| AAPL | — none in window — | — | — | — | Last reported 2026-11-02 ($2.10 vs $1.99 est.); next ~2027-01-28 (estimate) | FACT — prior package; next date UNVERIFIED |
| MSFT | — none in window — | — | — | — | Last reported 2026-10-28 ($4.89 vs $4.72 est.); next ~2027-01-27 (estimate) | FACT — prior package; next date UNVERIFIED |
| TSLA | — none in window — | — | — | — | Last reported 2026-10-21 ($0.48 vs $0.45 est.); next ~2027-01-27 (estimate) | FACT — prior package; next date UNVERIFIED |
| SPY / QQQ | — none — | — | — | — | ETFs; no earnings | FACT |

- **Date/timing FACT:** Nasdaq earnings calendar API swept day-by-day Nov 9–21 — NVDA is the only watchlist hit, Tue Nov 17, `time-after-hours`, fiscal Q3 FY2027 (quarter ended Oct 25, 2026). First full reaction session: Wed Nov 18. Source: `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`.
- **Implied move FACT (re-verified today):** Yahoo v7 options chain, cookie+crumb handshake, quotes as of Fri Nov 6 close, NVDA spot $186.64. Nov-20 expiry ATM (185 strike) straddle mid $20.88 = 11.18% of spot (call IV 75.7%, put IV 73.3%) — identical to yesterday's print, as expected with the market closed since. Pre-earnings Nov-16 expiry ATM straddle $13.85 = 7.42%; Nov-11 expiry $10.47 = 5.61%. Term structure steps up sharply into the Nov-20 expiry that straddles the event.
- **Event-isolated move — INFERENCE, method corrected:** time-scaled variance subtraction gives ~5.7% (Nov-13 baseline) to ~6.9% (Nov-16 baseline). Yesterday's 8.9% subtracted the 7-day straddle variance from the 14-day straddle variance without time-scaling, which overstates the event component; the corrected range is ~6–7%. The raw 11.18% straddle is the market quote and is unaffected.
- **Historical move FACT (recomputed):** last report's reaction, Aug 27, 2026: NVDA closed $209.66 on Aug 26 → $227.98 on Aug 27 = +8.74% (recomputed from Yahoo v8 chart closes; sign verified positive). The ~5% ten-report average is a secondary-source figure (Motley Fool, Nov 2, 2026) — not independently recomputed across all 10 reports; direction pattern in the last 10 is UNVERIFIED.
- **Consensus cross-check:** Yahoo v10 quoteSummary `calendarEvents` returned empty fields this run (method gap, not a contradiction); Nasdaq's $2.49 stands. Revenue consensus ~$108.98B carried from the Nov 7 package, NOT re-verified today — treat as carried, not fresh FACT. Company guidance (Aug 26 call): revenue $108.0B ±2%, gross margin 74.0%, no Data Center compute revenue from China assumed.
- **Recent-release teardown:** no watchlist name reported earnings in the last 2–3 days, so the CFA "read the release itself" step has nothing new to read this run. The Nov 17 NVDA release is to be read directly from the issuer/SEC filing when it drops, not via summaries.
- **What would change it:** a pre-report options repricing by Mon Nov 16, or a guidance revision in the release itself (especially Q4 gross-margin outlook — memory costs flagged as a margin headwind — or a Data Center revenue miss vs the ~$108B guide).

Sources: Nasdaq earnings calendar API (Nov 9–21, 2026); Yahoo Finance v7 options `query2.finance.yahoo.com/v7/finance/options/NVDA` (cookie+crumb), expiries Nov 11 / Nov 16 / Nov 20; Yahoo v8 chart NVDA daily closes; Motley Fool Nov 2, 2026 (secondary); Nvidia Aug 26, 2026 earnings call (guidance).

---

## 2. Dividend Opportunity desk

**Question:** Which watchlist names go ex-dividend in the next four weeks (through Sun 2026-12-06), and has anything changed since yesterday's run?

| Ticker | Ex-date | Amount | Record | Pay date | Yield | Flag | Consecutive-increase count (desk standard) | Evidence |
|---|---|---|---|---|---|---|---|---|
| AAPL | Thu 2026-11-12 | $0.27/qtr | 2026-11-12 | 2026-11-16 | 0.31% (Nasdaq; 0.32% Zacks/Koyfin at Nov 6 close) | No change — flat vs Aug/May 2026 | 14 consecutive annual increases (2013–2026), verified from Nasdaq's 84-row dividend history; 15 if the 2012 reinstatement counts as year 1 per the standard's initiation rule | FACT |
| MSFT | Thu 2026-11-19 | $0.98/qtr | 2026-11-19 | 2026-12-10 | 0.68% Nasdaq header — **STALE, do not use**; forward yield ~0.74% on $3.92 annualized (stockanalysis, Nov 6 close) | **INCREASE — $0.91 → $0.98 (+7.7% recomputed; Microsoft release says "7 cent or 8%"), declared 2026-09-15** | 24 consecutive annual increases per the standing count standard, incl. the Sep 15, 2026 raise; initiated 2003, no skipped year | FACT |

Outside the window / no dividend:

- **NVDA** — FACT: no dividend declared for the December quarter as of 2026-11-08. Last ex 2026-09-10, $0.25, paid 2026-10-01. Current increase streak is 1 year (2026 only): the May 2026 raise ($0.01→$0.25) followed a flat 2025; prior raise was May 2024. INFERENCE: next ex likely early December on cadence (Dec 5, 2024 and Dec 4, 2025) — UNDECLARED and UNVERIFIED until the board acts, expected with Q3 FY2027 results in late November.
- **SPY** — FACT: last ex 2026-09-18, $1.8888, paid 2026-10-30. Next ex Dec 18, 2026 — OUTSIDE the window (Wall Street Horizon / TipRanks). Amount UNVERIFIED. Wall Street Horizon also lists a 2026-12-31 "XOTH" entry — a possible year-end extra distribution, amount unknown, UNVERIFIED.
- **QQQ** — FACT: last ex 2026-09-21, $0.75143, paid 2026-10-08. Next ex Dec 21, 2026 — OUTSIDE the window (projected, not yet announced). Amount UNVERIFIED: third-party estimates conflict ($0.7514 flat vs ~$0.79).
- **TSLA** — FACT: pays no dividend; Nasdaq dividends endpoint returns an empty history.

**Cuts: none announced. Specials: none announced.**

Decision-relevant findings:

1. **AAPL goes ex-dividend Thursday (Nov 12, $0.27, flat) — the capture window closes at the Wed Nov 11 close.** FACT (Nasdaq per-symbol endpoint + Zacks, both pulled today; unchanged from yesterday's run). The only in-window ex-date in the coming week, and the second of only two in-window ex-dates overall (MSFT Nov 19).
2. **MSFT's $0.98 is the first payment at the raised rate — and Nasdaq's own header yield is still wrong.** FACT: Nasdaq still shows annualized dividend $3.64 / yield 0.68%, which is $0.91 × 4, the pre-raise rate. Forward annual at the declared rate is $3.92 ($0.98 × 4; recomputed), yield ~0.74% at the Nov 6 close. Any screen quoting 0.68% understates MSFT's forward yield by ~0.06pp. INFERENCE: the $0.98 payment landing Dec 10 is the cleanest near-term dividend-capture date on the watchlist, and the only in-window event carrying an increase.
3. **NVDA's December dividend is the open item — declaration expected with late-November results, amount UNVERIFIED.** What would change this: an NVDA declaration with Q3 FY2027 results.

Method gaps (flagged, not dropped): Nasdaq `api/calendar/dividends?date=...` returned a string payload instead of calendar rows for all four weekly queries — endpoint unusable this run, same failure as 2026-11-07. Yahoo v8 chart `events=div` returned empty dividend events for all five dividend-paying tickers — not usable as a cross-check, same as yesterday. Nasdaq per-symbol endpoints worked for AAPL/MSFT/NVDA/TSLA and QQQ; SPY returns "Symbol not exists" (NYSE Arca listing) — SPY figures from Wall Street Horizon/TipRanks instead. AAPL count note: third-party screeners conflict (14 vs 15 vs 12 under different counting rules); 14 is verified directly from Nasdaq's own 84-row history, with the 15 convention disclosed rather than silently adopted.

Sources: `https://api.nasdaq.com/api/quote/{AAPL,MSFT,NVDA,TSLA}/dividends?assetclass=stocks`, `https://api.nasdaq.com/api/quote/QQQ/dividends?assetclass=etf` (pulled Sun 2026-11-08 ~13:35 PT); Microsoft Sep 15, 2026 dividend-increase release https://news.microsoft.com/source/2026/09/15/microsoft-announces-quarterly-dividend-increase-7/ ; https://stockanalysis.com/stocks/msft/dividend/ ; https://www.zacks.com/stock/research/AAPL/dividend-history ; https://wallstreethorizon.com/spy-dividend-calendar ; https://www.tipranks.com/etf/spy/dividends ; https://wallstreethorizon.com/qqq-dividend-calendar ; https://www.tipranks.com/etf/qqq/dividends. Count standard: `~/workspace/hedge-desk-research/dividend-count-standard.md`. Math recomputed: MSFT ($0.98−$0.91)/$0.91 = +7.69% ≈ +7.7%; AAPL ($0.27−$0.26)/$0.26 = +3.85% ≈ +3.8%; MSFT forward annual $0.98 × 4 = $3.92; AAPL annual $0.27 × 4 = $1.08.

---

## 3. Overnight Premium desk (IV)

**Question:** Is front-month implied vol pricing in more or less movement than the market just delivered, and is any of it an earnings event rather than a genuine premium?

**Freshness guard — PASS.** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-07-iv-inputs.json`, `as_of` **2026-11-07T14:54:30-07:00** (FACT — read from disk). Age at run start ~22.5h — inside the 26h guard. All IV levels from the file carry the **STALE (Saturday post-close print, Friday 2026-11-06 close data)** label. File caveat (FACT): the pull ran on the legacy Yahoo-only path — repo failover module unavailable on the clone's branch (`failures[0]`). No CBOE cross-check in the file. DTE note (FACT): the file's `iv_dte: 2` was as of Sat Nov 7; as of today (Sun Nov 8) the 2026-11-09 expiry is **1 DTE**; it dies Mon Nov 9, 16:00 ET.

### IV snapshot

| Symbol | ATM IV — file print (STALE, Sat post-close) | ATM IV — live Yahoo pull (Sun, weekend marks) | Expiry / DTE | 20d realized (file) | Max 1-day var. share | IV-vs-realized verdict |
|---|---|---|---|---|---|---|
| SPY | 18.01% | 22.06% (Nov 9) | 2026-11-09 / 1 DTE today | 20.76% | 0.626 | **WINDOW-CONTINGENT** — IV < realized, no clean verdict |
| QQQ | 25.28% | 32.95% (Nov 9) | 2026-11-09 / 1 DTE today | 33.59% | 0.504 | **WINDOW-CONTINGENT** — IV < realized, no clean verdict |
| AAPL | 22.77% | 27.89% (Nov 9) | 2026-11-09 / 1 DTE today | 25.89% | 0.558 | **WINDOW-CONTINGENT** — IV < realized, no clean verdict |
| MSFT | 27.08% | 33.17% (Nov 9) | 2026-11-09 / 1 DTE today | 35.70% | 0.458 | **WINDOW-CONTINGENT** — IV < realized, no clean verdict |
| NVDA | 49.77% | 60.96% (Nov 9) | 2026-11-09 / 1 DTE today | 49.08% | 0.493 | **WINDOW-CONTINGENT** — IV ≈ realized, no clean verdict |
| TSLA | 48.98% | 60.03% (Nov 9) | 2026-11-09 / 1 DTE today | 59.38% | 0.513 | **WINDOW-CONTINGENT** — IV < realized, no clean verdict |

- **Stale-jump screen (FACT, verified from file):** all six symbols `window_contingent: true` — the Nov 5 crash day drives 46–63% of each 20-day realized-variance window (realized window 2026-10-12 to 2026-11-06). Every IV-vs-realized verdict above is therefore WINDOW-CONTINGENT by the standing rule; none is a clean "IV cheap/rich" call. **What would change it:** the Nov 5 return rolling out of the 20-day window (~early Dec) or a fresh 20-day window computed after it exits.
- **Live-pull method (FACT):** Yahoo v7 options, cookie+crumb handshake (curl-seeded jar, crumb via query1), pulled Sun 2026-11-08 13:28 PT / 21:28 UTC; markets closed, so quotes are Friday-close marks. ATM IV = mean of ATM call/put `impliedVolatility` at the nearest overlapping strike. Friday closes (FACT, Yahoo quote): SPY 735.29 (+0.31% Fri), QQQ 656.10, AAPL 342.37, MSFT 530.61, NVDA 186.64, TSLA 358.22.
- **Live-vs-file gap (INFERENCE, cause UNVERIFIED):** the live pull runs systematically ~4–11 pts above the Saturday file print on every symbol (e.g. SPY 22.06% vs 18.01%, NVDA 60.96% vs 49.77%). Markets were closed between the two pulls, so this is **not** a market move — most plausibly Yahoo's weekend solver inputs (spot/rate) differing from the post-close print. Cause is UNVERIFIED; the file print stays the authoritative level, the live pull is a shape cross-check only.

### Term structure (live Yahoo pull, Sun 2026-11-08 — weekend marks, shape only)

| Symbol | Nov 9 (1 DTE) | Nov 20 (12 DTE) | Dec 18 (40 DTE) | Shape |
|---|---|---|---|---|
| SPY | 22.06% | 23.16% | 20.57% | Mild hump at Nov 20 |
| QQQ | 32.95% | 34.97% | 29.90% | Mild hump at Nov 20 |
| AAPL | 27.89% | 29.39% | 27.33% | Mild hump at Nov 20 |
| MSFT | 33.17% | 34.69% | 30.44% | Mild hump at Nov 20 |
| NVDA | 60.96% | **74.52%** | 54.62% | **Sharp earnings hump at Nov 20** |
| TSLA | 60.03% | 58.71% | 51.41% | Downward-sloping, no hump |

- **NVDA earnings hump (INFERENCE from FACTs):** NVDA next earnings 2026-11-17 (FACT — Nasdaq-calendar sweep). The Nov 20 expiry is the first expiry after earnings, and its IV (74.52%) sits ~14 pts above the Nov 9 front and ~20 pts above Dec 18 — the textbook earnings hump. Elevated Nov 20 NVDA IV is **expected, not "rich"**. **Premium into this binary event = avoid.** What would change it: an earnings-date move or the hump collapsing after Nov 17.
- **No other watchlist earnings inside the window (FACT — file):** next_earnings null for SPY, QQQ, AAPL, MSFT, TSLA in the file's 45-day Nasdaq sweep. The mild Nov 20 humps on the other four names are small (~1–2 pts) and not earnings-driven on current calendars — treat as term-structure noise, not an event signal.
- **Parity/stale-quote check (FACT):** weekend marks show crossed/locked quotes — AAPL Nov 9 call bid 2.72 > ask 2.65 (crossed), NVDA Nov 9 put bid = ask 3.75, MSFT Nov 9 call spread 5.00/5.75 ($0.75 wide on a 1-DTE option). Per the skill's sanity check #5, these are stale weekend marks; **no parity-violation conclusion can be drawn from them** — parity math outranks the model, but the inputs here are not tradeable quotes.

### Elevated-IV flags

- **IV rank: UNVERIFIED for all six symbols.** No IV-history series is available from free sources, so no IV-rank number can be computed or stated — per the fail-closed protocol the desk does not rank. Absolute front-month levels (file print): NVDA 49.77% and TSLA 48.98% are high in absolute terms; SPY 18.01% and QQQ 25.28% are elevated versus a quiet-tape baseline but that comparison is INFERENCE without a history series, not a rank.
- **No clean "IV cheap" signal anywhere:** on the file print, IV sits below the (crash-polluted) 20-day realized on five of six names — but with every window WINDOW-CONTINGENT, that gap is an artifact of the Nov 5 jump still in the window, not evidence of underpriced premium. **What would change it:** a post-roll-off realized window, or IV holding below realized after the jump exits.

Decision-relevant findings: (1) All six verdicts WINDOW-CONTINGENT — do not trade on any "IV cheap" read today. (2) NVDA Nov 20 expiry carries a genuine earnings hump ahead of Nov 17 earnings — premium into that binary event is to be avoided. (3) Live weekend Yahoo marks run 4–11 pts above the Saturday post-close file on every symbol, with crossed/wide quotes — use the file print as the level and the live pull for shape only. Weekend IV levels are not tradeable; Monday's open will re-price the 1-DTE Nov 9 expiry, which dies at 16:00 ET.

Sources: IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-07-iv-inputs.json`, `as_of` 2026-11-07T14:54:30-07:00; live supplement Yahoo Finance v7 options (`https://query1.finance.yahoo.com/v7/finance/options/{SPY,QQQ,AAPL,MSFT,NVDA,TSLA}`), cookie+crumb auth, pulled Sun 2026-11-08 13:28 PT; raw pull saved at `/tmp/premium_live_pull2.json`. Technique: `~/workspace/custom-skills/local-cfa-financial-analysis/SKILL.md` + `references/derivatives_options.md` + `references/evidence_standards.md`. No desk failures. IV rank UNVERIFIED (no free IV-history source); live-vs-file IV gap cause UNVERIFIED.

---

## 4. Open Quant/AI Model Lab

**Question:** What new (Nov 6–8, 2026) papers, preprints, datasets, or free APIs relevant to options microstructure, vol forecasting, earnings drift, dividend forecasting, or purged walk-forward methodology have appeared since yesterday's sweep?

**Answer in one line:** Nothing new in the Nov 6–8 window — the arXiv q-fin feed is genuinely empty (Sunday, no weekday announcement) — but the web-search leg caught three earlier items missed by prior sweeps, all scored WATCH, none TEST/INTEGRATE.

Coverage check (FACT): arXiv API, date-filtered `submittedDate:[20261106 TO 20261108]`, returned 0 results (first attempt over plain http returned an empty body; https retry returned HTTP 200, `totalResults: 0`). No-filter control confirms the window is genuinely empty: newest q-fin item is still 2026-11-05, arXiv:2611.07464 (FINCOSMOS, already ledger #221). GitHub leg skipped per the run brief's ban on GitHub operations (same as Nov 1–7) — no new-repo discovery, no repo re-checks, no repo contents/license verification. No broad WATCH re-check this run (full 111-row re-check done in the 2026-11-07 kaizen run).

### New candidates (scorer-run via `hedge_desk.research_intelligence.assess_source`, read-only import — no repo modification)

| # | Candidate | Source / Date | Topic | Score | Disposition + reason | Evidence label |
|---|---|---|---|---|---|---|
| 235 | Tirhekar — "Regime-Conditioned Convolutional Autoencoders with Recurrent Networks for Implied Volatility Surface Forecasting" | MDPI conference proceedings (2nd Int. Online Conf. on Risk and Financial Management, Nov 2–4, 2026), published 28 Oct 2026 — https://sciforum.net/paper/35918 | IV-surface forecasting | 45 | **WATCH** — 5.7% RMSE gain over persistence at 20d, but Diebold-Mariano p=0.646 (not significant); OptionMetrics licensed data; no code link (poster PDF only). Reproducibility not established. | FACT: abstract read at source; paper's RMSE/DM figures are source-reported, **UNVERIFIED** (full paper/poster not read) |
| 236 | Fan/Wang/Ye — "On options-driven realized volatility forecasting: Information gains via rough volatility model" (HAR-RV-RHeston) | arXiv:2604.02743v3, submitted 3 Apr 2026, revised 10 Apr 2026 — https://arxiv.org/abs/2604.02743 | Vol forecasting (options → realized vol) | 45 | **WATCH** — options-derived rough-vol spot estimators augment HAR-RV; beats Heston/Bates/SVCJ/VIX on source-reported numbers; no code link on abs page. Reproducibility not established. | FACT: abstract read at source; OOS MAE 0.2137 / RMSE 0.2762 are source-reported, **UNVERIFIED** (full paper not read) |
| 237 | QuanterLab (Girgin) — "Post-Earnings Drift, Decomposed: 81 Walks, a Predictability Spread That Was Market Exposure, and a Screen That Picks Better Announcements and a Worse Book" | quanterlab.com research, ~Sep 2026 — https://quanterlab.com/research/post-earnings-drift-decomposed-81-walks-a-predictability-spread-that-was-market- | Earnings drift + purged walk-forward methodology | 57 | **WATCH** — run's best score; 81 sealed walk-forwards, point-in-time S&P 500; the unhedged +9.6pp spread was market exposure (hedged +0.1pp); data/code not open (platform engine). | FACT: abstract + §§1–2 read at source; headline numbers read at source, cell-by-cell tables **UNVERIFIED** (not re-checked) |

Scorer inputs (run, not hand-computed): #235 PEER_REVIEWED proceedings, signal 3 / data 2 / implementation 2 / risk 3 / credibility 3, reproducible False; #236 PREPRINT, 3/2/2/3/3, reproducible False; #237 INDUSTRY_BLOG, 4/3/3/4/3, reproducible False. All carry `MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED, LICENSE_REVIEW_REQUIRED`.

Ledger confirmation: appended **#235, #236, #237** to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (rows verified on disk, lines 298–300), plus a 2026-11-08 run-log entry after the 2026-11-07 entry. No duplicates: Bastola #157, Wu/Tao #197, Buchegger #9, Jin/Agarwal #31 re-surfaced by search and were confirmed already ledgered. Triage exclusions (no ledger rows): Medium ETF-band backtest (Nov 2026, portfolio-allocation lane, no purged validation); AEHR post-earnings case study (single-stock trade journal); Wang/Wei/Yu synchronicity (Mar 2026 journal article, old).

Most decision-relevant findings:

1. **#237 — unhedged PEAD returns are beta, not alpha (INFERENCE from source-read findings).** The 81-walk decomposition shows the steady-vs-erratic +9.6pp/yr spread at 42 days collapses to +0.1pp once net market exposure is charged daily, and the short leg lost money in all nine cohorts. **What would change it:** a beta-hedged replication on the desk's own earnings universe, or the site's first paper (220 sector walks) showing a surviving hedged spread. Earnings-desk implication: any drift screen must be beta-hedged before claiming edge.
2. **#235 — an honest null worth copying (FACT: DM p=0.646 reported in the abstract).** The best IVS model beats persistence by 5.7% RMSE at 20 days and the author still reports non-significance rather than claiming victory. **What would change it:** a code release plus a larger OOS test set that moves the DM test. Premium-desk lesson: same discipline as #233 — a vol edge that fails its significance test is not an edge.
3. **#236 — options-implied spot vol as a HAR input (INFERENCE).** If code is ever released, the HAR-RV augmentation is the most sandboxable of today's three on desk data (SPY realized vol is computable in-house). **What would change it:** code/data release; until then it stays WATCH with claims UNVERIFIED beyond the abstract.

**Verdict:** No TEST or INTEGRATE movement today. No new dataset or free API surfaced. All three new candidates are WATCH, blocked on the same external, binary triggers as the rest of the ledger (code release / journal version).

---

## 5. Weather/War/Logistics Futures Event desk

**Question:** What fresh futures-relevant catalysts land this week, and what are front-month futures pricing after last week's sharp oil selloff?

### Catalyst table

| Event | Date / time | Status | Relevance | Source | Label |
|---|---|---|---|---|---|
| USDA Crop Progress | Mon Nov 9, 4:00 PM ET | Scheduled | Harvest-progress read into Tue WASDE | NASS release calendar — https://www.nass.usda.gov/data-and-statistics/calendar/release/6632 | FACT |
| USDA WASDE + Crop Production | Tue Nov 10, 12:00 PM ET | Scheduled — the week's ag binary | Corn/soy/wheat balance sheets; trade focused on soybean crop size after a week of pressure | USDA schedule via AGSIST — https://agsist.com/usda-calendar ; American Ag Network, Nov 6 — https://www.americanagnetwork.com/2026/11/06/grain-markets-look-for-direction-ahead-of-wasde-after-a-week-of-pressure/ | FACT |
| EIA Short-Term Energy Outlook (Nov) | Tue Nov 10 | Scheduled | Oct STEO assumed Middle East flows constrained thru Q4 (4.5M b/d shut-in) and Brent averaging $105 in Q4 — Nov edition tests that assumption | Morningstar/PR Newswire, Nov 2 — https://www.morningstar.com/news/pr-newswire/20261102ln86532/oil-enters-november-with-opec-holding-steady-and-five-producers-set-to-report | FACT |
| Russia–Ukraine talks resume, Abu Dhabi | Tue–Wed Nov 10–11 | Reported scheduled | Ceasefire headlines are a second de-escalation channel for the oil risk premium | The Private Banker, Nov 8 — https://leprivatebanker.com/2026/11/08/brent-gives-back-a-weeks-spike-but-inventories-and-hormuz-odds-show-a-market-still-tight/ | FACT (secondary source) |
| OPEC Monthly Oil Market Report | Wed Nov 11, 4:00 AM ET | Scheduled | First official OPEC read on October production rebound | ReadGeo schedule, updated Nov 8 — https://www.readgeo.net/guides/opec-meeting-dates | FACT (secondary, cites official schedule) |
| EIA Weekly Petroleum Status Report | **Thu Nov 12, 12:00 PM ET — shifted from Wed for Veterans Day** | Scheduled | Weekly crude/product stocks; last print: commercial crude 409.760M bbl, draw 0.865M w/e Oct 30; refinery utilization 94.5% | EIA schedule — https://www.eia.gov/petroleum/supply/weekly/schedule.php? ; last print via CommoditiesChart/EIA — https://commoditieschart.net/crude-oil/us-eia-commercial-crude-oil-inventory | FACT |
| EIA Weekly Natural Gas Storage Report | **Fri Nov 13, 10:30 AM ET — shifted from Thu for Veterans Day** | Scheduled (holiday shift) | Withdrawal-season storage read; confirm on eia.gov before relying on the shifted time | PetroEyes reading of EIA schedule tables — https://petroeyes.com/deep-dives/eia-report-release-schedule-explained/ | FACT (secondary source; EIA primary page not re-checked this run) |
| IEA Oil Market Report | Fri Nov 13 (10:00 Paris) | Scheduled | IEA demand/supply balances; Oct report flagged record 2026 surplus and Q4 demand −2.5M b/d y/y | IEA 2026 publishing schedule — https://www.iea.org/files/0832f875-dc2f-45e2-925e-6adc34ebb1ba/-11DEC2025_OilMarketReport.pdf ; https://www.iea.org/events/oil-market-report-november-2026 | FACT |
| OPEC+ ministerial meeting (2027 quotas) | Sun Nov 29 | Scheduled | Next supply-policy decision; Dec quotas held unchanged at Nov 1 meeting | OPEC+ decision via Rigzone/Swiss FT — https://www.swissfinancialtime.ch/2026/11/brent-settles-at-9832-as-oil-posts-its.html | FACT |
| US CPI (Oct) | Tue Nov 10 | Scheduled | Dollar/risk channel into energy and equities | Noted in Swiss FT oil wrap (above) | FACT |

**Government-data note:** No shutdown framing applies — federal releases are on schedule per the standing rule (CR through Dec 11). The EIA shifts above are routine Veterans Day holiday moves, not disruptions. No USDA/EIA release this week is delayed or cancelled on any source checked. [FACT]

### Front-month futures — as of Fri Nov 6, 2026 close (Yahoo Finance v8 chart, pulled Sun Nov 8, 13:27 PT)

| Contract | Close | Day | Week (vs Fri Oct 30) | Label |
|---|---|---|---|---|
| WTI crude Dec (CL=F) | $90.83 | +0.34% | **−12.76%** (104.12 → 90.83) | FACT |
| Brent Jan (BZ=F, continuous) | $98.32 | +0.03% | −16.42% on the continuous series — **roll artifact**: Dec contract expired Oct 30. Same-contract Jan Brent: 113.43 → 98.32 = **−13.3%** | FACT (both figures; roll explanation per Private Banker, Nov 8) |
| Brent–WTI spread | $7.49 (98.32 − 90.83) | — | — | FACT (arithmetic on closes above) |
| Natural gas (NG=F) | $3.00 | +1.69% | +3.45% (2.90 → 3.00) | FACT |
| Corn (ZC=F) | 441.50¢ | +0.34% | −1.40% (447.75 → 441.50) | FACT |
| Wheat (ZW=F) | 591.25¢ | −1.34% | −2.03% (603.50 → 591.25) | FACT |
| Soybeans (ZS=F) | 1,193.75¢ | +1.08% | −2.33% (1,222.25 → 1,193.75) | FACT |

### Geopolitics / logistics — facts vs inference

- **FACT:** Oil posted its steepest weekly drop since 2022: front-month Brent and WTI each fell ~13% on the week (same-contract basis), after trading a ~$19 range since Monday. Drivers cited by Rigzone/Bloomberg: US midterm results plus Qatari mediation raising de-escalation expectations, and recovering Persian Gulf exports. [Rigzone via Swiss FT, Nov 6–7]
- **FACT:** OPEC crude production rose in October toward pre-war levels, led by Saudi Arabia (Bloomberg survey via Rigzone). OPEC+ held December quotas unchanged at its Nov 1 meeting. US Baker Hughes rig count rose 1 to 604 in the week to Nov 6, highest since 2024; oil rigs 463. [Swiss FT / Rigzone]
- **FACT:** US commercial crude stocks (409.8M bbl, w/e Oct 30) sit below every comparable week from 2021–2025 (low for the period was 421.2M). Money managers' net long in Brent fell 48.5K contracts to 171.6K in the week to Nov 3. Oil vol index closed 58.3 vs VIX 25.6. [EIA via Private Banker, Nov 8; CFTC via Private Banker]
- **FACT — with a reported conflict:** Hormuz transit counts disagree by measure. FoodExpoConnect (updated Nov 2) reports ~2 transits on Oct 25 vs a pre-war ~85/day and calls the strait "effectively closed" to commercial shipping since early March. UANI (Nov 5) reports US-facilitated transits averaged 31.5/day over Nov 1–4 (126 transits, 96 hours), cumulative 3,215 over 138 monitored days. These measure different things (all commercial transits vs US-facilitated transits) — no winner picked; treat the strait's status as contested, not settled.
- **FACT:** Two oil tankers and a tug caught fire in the Strait of Hormuz on Nov 5 after entering unauthorized passages (IRNA/Al Jazeera). Saudi air defense intercepted a Houthi missile near Yanbu the same day. [Hummini briefing, Nov 5]
- **UNVERIFIED:** A Nov 7 flash item (HamerIntel, single OSINT aggregator) claims an Iranian Army spokesman declared Hormuz "closed" until the US accepts seven conditions, and that Houthis are issuing "transit clearance" at Bab el-Mandeb. No primary source or major-wire corroboration found in this run — do not treat as fact.
- **INFERENCE:** The market is pricing de-escalation, not resolution: a ~13% weekly oil drop alongside an oil-vol index still above 58 and prediction-market odds of a US invasion of Iran before 2027 at only 10.5% (Polymarket via Private Banker, down 7 pts on the week) says traders expect talks to continue but have not priced out a supply shock. **What would change it:** a confirmed Hormuz incident/closure notice (NOTAM/NAVWARN), a breakdown in the Nov 10–11 Abu Dhabi talks, or a Nov 12 EIA print showing the inventory draw reversing.
- **INFERENCE:** The oil selloff is sentiment-led, not inventory-led: US crude stocks are at a 5-year low for the week while prices fell ~13%. If the Nov 12 EIA print confirms continued draws, the "loose market" read weakens. **What would change it:** Nov 12 WPSR showing a build, or OPEC's Nov 11 report confirming the October production rebound is larger than the Bloomberg survey implied.
- **INFERENCE:** Grains drifting lower into Tuesday's WASDE (corn −1.4%, wheat −2.0%, soy −2.3% on the week) is pre-report positioning, not a verdict on the balance sheet — soybean crop-size uncertainty is the named swing factor. **What would change it:** the Nov 10 12:00 ET WASDE/Crop Production print itself.

Most decision-relevant findings: (1) Oil's ~13% weekly collapse is the week's dominant futures event, sentiment-led not inventory-led; watchlist read: fading energy shock eases input-cost/inflation pressure, but the premium can return fast; the Nov 12 EIA print is the next physical check. (2) Catalyst-dense week ahead, both lanes at once: WASDE + EIA STEO Tue Nov 10, OPEC monthly Wed Nov 11, EIA petroleum Thu Nov 12 (12:00 ET, Veterans Day shift), EIA gas storage Fri Nov 13 (10:30 ET, shifted) + IEA monthly Fri Nov 13. (3) Hormuz status is genuinely contested — do not trade the headline. Transit counts range from ~2/day to 31.5/day depending on the measure, and the Nov 7 "closure declaration" is single-source UNVERIFIED. The tradable watchpoints are NOTAMs/NAVWARNs, the Nov 10–11 Abu Dhabi talks, and any confirmed incident — not the flash headline.

Desk status: COMPLETE. No desk item failed. One item flagged UNVERIFIED (Nov 7 Hormuz "closure declaration"). EIA gas-storage holiday shift sourced from a secondary reading of EIA tables — confirm on eia.gov before relying on the Fri Nov 13 time.

---

## 6. Box/Parity Observer

**Question:** Has anything in the last ~2 weeks changed index methodology, broken put-call/box parity, or moved SPX box-spread rates anomalously for the watchlist?

**Verdict: Nothing material to parity.** No published parity violation for SPX/SPY/QQQ in the window; the one new index-methodology change touches S&P style (growth/value) classification only, not headline S&P 500 membership or SPX settlement; SPX box rates sit in their normal range per secondary sources, with no anomaly reported. One live rate check remains UNVERIFIED (see below).

| Item | Finding | Evidence label | Source / as-of |
|---|---|---|---|
| S&P DJI style-index methodology change | S&P Dow Jones Indices revised U.S. growth/value classification (release dated Oct 23, 2026): 12-month price momentum dropped from growth scoring; value adds intangibles-adjusted book-to-price, a trailing/forward earnings-to-price blend, and free-cash-flow-to-price. Effective before the open Dec 21, 2026 (annual reconstitution); preliminary files from Dec 4. Affects S&P 500 Growth/Value and related style indices; Bloomberg Intelligence estimates ≥$375bn in passive funds tied to the affected gauges. | **FACT** (per multiple agreeing secondary reports of the Oct 23 S&P DJI release; the primary S&P DJI release itself was not opened — see caveat) | TradingView/CNBC TV18, Oct 24, 2026: https://www.tradingview.com/news/cnbctv:efc13bb28094b:0/ ; Briefs.co, Oct 23, 2026: https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/ ; EL7.AI, Oct 28, 2026: https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing |
| Relevance to this desk | The change reclassifies stocks between growth and value style indices; it does not change headline S&P 500 membership criteria or SPX options settlement, so it does not alter put-call/box parity math for SPX. | **INFERENCE** (follows from the reported scope: style indices only) | Same sources as above |
| Cboe complex-order rule change (watch item, just outside window) | Cboe filed SR-CBOE-2026-081 (Oct 9, 2026; Federal Register Oct 22, 2026) to let complex orders with legs in different series groups leg into the Simple Book where the groups are designated related, and to set risk controls on a related-group basis. The filing notes SPX (A.M.) / SPXW (P.M.) are separately grouped today and flags a planned Weekly A.M.-settled SPX ("SPXO") launch. This is execution mechanics, not a methodology or parity change. | **FACT** | Federal Register Vol. 91 No. 203, Oct 22, 2026: https://www.govinfo.gov/content/pkg/FR-2026-10-22/html/2026-21576.htm |
| Put-call parity check (VIX futures, 18 Nov expiry) | Saxo's daily Options Brief reports put-call parity on the 18 November options in line with the VIX futures settlement on three consecutive closes: 20.27 (Nov 2 close), 19.96 vs 19.90 settlement (Nov 3 close), 17.73 vs 17.74 settlement (Nov 4 close) — "the series has not rolled." No violation. | **FACT** (Saxo's reported check; VIX-futures parity, not a direct SPX box print) | Saxo Options Brief, Nov 4, 2026: https://www.home.saxo/content/articles/options/blue-wave-meets-a-one-day-premium---options-brief---4-november-2026-04112026 ; Nov 5, 2026: https://www.home.saxo/en-mena/content/articles/options/vote-premium-drains-from-the-front---options-brief---5-november-2026-05112026 |
| SPX box-spread rates | No box-spread rate anomaly reported in the last ~2 weeks. Secondary sources put SPX boxes at roughly 4.1–4.4% fixed in late 2026 against SOFR ~3.88% (Buck by Buck, late 2026); Tulan Capital (Oct 2026) cites ~4.3–4.4% for ~2-month Dec 2026 SPX boxes vs ~4.1% 1-month Treasury. The wider 69bp premium over SOFR cited by SummitWard is August 2026 Cboe data, not new. | **FACT** for the cited secondary levels; current live rate **UNVERIFIED** — no live boxtrades.com quote was pulled for this run, so no Nov 7–8 box rate is asserted | Tulan Capital, Oct 2026: https://www.tulancapital.com/insights/box-spreads.pdf ; Buck by Buck, late 2026: https://buckbybuck.com/blog/best-firms-to-borrow-against-stocks-margin-rates-box-spreads ; SummitWard (Aug 2026 Cboe figures): https://summitward.com/learn/box-spread-loans |
| Crypto-venue parity scanner | Optionly's live scanner shows put-call parity breaks on crypto venues (BTC/ZEC on Derive vs Deribit, largest $306.35/contract on BTC Mar 2027). Not an equity-index finding and not a published study; no bearing on SPY/QQQ/SPX parity. Checked and excluded. | **FACT** (scanner's own live read, Nov 8, 2026) | https://www.optionly.com/arb |

**What was checked:** Cboe/SPX methodology and rule filings; S&P Dow Jones Indices methodology news (Oct 23–Nov 8 window); published put-call parity checks (Saxo Options Brief, Nov 3–5); SPX box-spread rate reporting (boxtrades-referencing secondary sources); a crypto-venue arbitrage scanner (excluded as out of scope). No new CBOE SPX index-methodology document was found in the window — the only Cboe methodology item surfaced was a Feb 2026 consultation on the S&P 500 15% Buffer IC Index Series, stale for this desk. No published put-call parity / box-spread violation study for equities in the last ~2 weeks was found.

**What would change this verdict:** a new S&P DJI or Cboe methodology document affecting headline S&P 500/SPX construction or settlement; a published parity break on SPX/SPY/QQQ options; or a live boxtrades.com quote showing SPX box rates materially outside the ~SOFR +0–50bp band reported for 2026.

**Caveats:** The S&P DJI finding rests on secondary reporting (Bloomberg via aggregators) — the primary S&P DJI release was not opened in this run. The Saxo parity check covers VIX futures via 18 Nov options, not a direct SPX box print. No live box-spread quote was pulled, so the current rate is UNVERIFIED rather than confirmed.

---

## 7. Bonds & Rates desk

**Question:** What do current Treasury levels, curve shape, and funding spreads imply for premium pricing on the watchlist this week?

**Source:** repo module `hedge_desk.rates_desk.rates_environment()`, mode `REAL_FRED_RATES`, run 2026-11-08 13:27 PT. All figures below are module output (FRED daily series via `fred-public-csv-http-200`); nothing is retyped from memory. **Latest observation date is Thursday 2026-11-05, not Friday 2026-11-06** — the FRED DGS/DFF series had not yet published the 11-06 observation at run time, so this desk is one trading day stale by construction; label accordingly.

### Rates table (FACT — FRED, as of 2026-11-05 unless noted)

| Series | Level | Date | Change |
|---|---|---|---|
| Fed funds effective rate (DFF / EFFR) | **3.88%** | 2026-11-05 | +0.25 pp over the 60-day window (module output) |
| Treasury 2Y (DGS2) | **4.46%** | 2026-11-05 | −12 bp vs 2026-11-04 (4.58%) |
| Treasury 10Y (DGS10) | **4.84%** | 2026-11-05 | −6 bp vs 2026-11-04 (4.90%) |
| 2s10s slope | **+38 bp** (upward sloping) | 2026-11-05 | +6 bp steeper vs 2026-11-04 (32 bp) |
| SOFR | **3.92%** | 2026-11-05 | — |
| OBFR | **3.88%** | 2026-11-05 | — |
| SOFR − EFFR spread | **+4 bp** | 2026-11-05 | — |

### Slope / direction read

- **FACT:** The curve is upward sloping at +38 bp and steepened +6 bp on Thursday, driven entirely by the front end: the 2Y fell twice as far (−12 bp) as the 10Y (−6 bp). Over the full 60-day window the slope is essentially flat (40 bp on 2026-09-09 → 38 bp now, −2 bp).
- **FACT:** Thursday's −12 bp 2Y move is the second-largest single-day 2Y decline in the 60-day window (largest: −16 bp on 2026-10-22, 4.81% → 4.65%). The 10Y at 4.84% is its lowest since 2026-09-09 (4.83%).
- **INFERENCE:** A front-end-led rally with the long end falling less is consistent with the market pricing easier policy or softer near-term growth expectations, not with a growth scare at the long end. **What would change it:** a 10Y move back above 5.00% or a 2Y reversal above 4.58% would flip the read to "rates pressure returning."

### SOFR–EFFR spread read

- **FACT:** SOFR 3.92% vs EFFR 3.88% = +4 bp; OBFR sits exactly on EFFR at 3.88%. All three funding gauges are clustered within 4 bp.
- **INFERENCE:** No funding stress. A +4 bp SOFR–EFFR spread is inside the normal operating band; stress historically shows up as a widening, persistent gap, not a 4 bp print. **What would change it:** SOFR–EFFR widening past ~10–15 bp and persisting for several sessions, or OBFR decoupling from EFFR.

### Premium-pricing directional read

- **INFERENCE:** Directionally supportive for premium sellers and for growth-multiple names on the watchlist, modestly. A 10Y at 4.84% — its lowest in ~two months — lowers the discount rate applied to long-duration cash flows relative to the 5.2–5.3% prints of late September/early October, which eases pressure on NVDA, TSLA, and MSFT multiples; falling front-end rates also reduce the carry cost of holding the underlying. But the effect is small (a −6 bp weekly move in the 10Y) and the curve is still upward sloping with the 10Y nearly 100 bp above fed funds — this is not a low-rate regime, just a less-tight one.
- **SPECULATION:** If the front-end rally extends (2Y through ~4.30%), premium buyers could see IV drift lower as rate-driven equity risk premium compresses — but that chain has no evidence yet and is not the basis for any conclusion here.
- **UNVERIFIED:** Friday 2026-11-06 closes for all series (not yet published by FRED at run time); any Friday rate move is unknown to this desk. The 13W bill front-end anchor was not pulled — the module's DGS2 serves as the front-end read, and no Yahoo yield is substituted per the desk brief.

Most decision-relevant findings: (1) Front-end rally Thursday is the week's rates story: 2Y −12 bp to 4.46%, steepening 2s10s to +38 bp — the second-biggest one-day 2Y drop in 60 days. Mild tailwind for growth names (NVDA, TSLA, MSFT) and for premium pricing; watch whether Friday's (unpublished) print confirms or reverses it. (2) No funding stress anywhere: SOFR–EFFR +4 bp, OBFR = EFFR. Nothing in the funding complex argues for defensive premium pricing. (3) Fed funds at 3.88%, +25 bp over the 60-day window, with a +38 bp upward-sloping curve: no inversion signal, no recession pricing from the curve — the rates backdrop is neutral-to-mildly-supportive, not a risk-off trigger.

Raw module output:

```json
{"schema_version": "hedge-desk-rates-desk-1.0.0", "mode": "REAL_FRED_RATES", "as_of": "2026-11-08", "fed_funds_effective_rate": "3.88", "fed_funds_latest_date": "2026-11-05", "fed_funds_change_over_window": "0.25", "treasury_2y": "4.46", "treasury_2y_date": "2026-11-05", "treasury_10y": "4.84", "treasury_10y_date": "2026-11-05", "spread_10y_2y_points": "38.00", "curve_slope": "0.047500", "curve_shape": "UPWARD_SLOPING", "lookback_days": 60, "sofr": "3.92", "sofr_date": "2026-11-05", "effr": "3.88", "effr_date": "2026-11-05", "obfr": "3.88", "obfr_date": "2026-11-05", "data_source": "fred-public-csv-http-200", "trade_authorized": false, "note": "Observations of official FRED daily series. Fed funds/src curve change is a measured fact, not a forecast and not advice. No order placed."}
```

Desk status: **COMPLETE — no failures.**

---

## Run status

- All seven desks reported: Earnings, Dividend, Overnight Premium (IV), Quant Lab, Futures Events, Box/Parity, Bonds & Rates. **No desk FAILED.**
- IV inputs: file `2026-11-07-iv-inputs.json`, as_of 2026-11-07T14:54:30-07:00 — inside the 26h guard; all IV levels from it labeled STALE (Saturday post-close print).
- Rates desk: FRED latest observation Thu 2026-11-05 (Friday unpublished at run time).
- Quant Lab: 3 new WATCH candidates appended to the ledger (#235, #236, #237); no TEST/INTEGRATE movement.
- UNVERIFIED items carried: IV rank for all six symbols (no free IV-history source); live-vs-file IV gap cause; Nov 7 Hormuz "closure declaration" (single OSINT source); SPY/QQQ December dividend amounts; live SPX box-spread rate; NVDA December dividend declaration.
- Method gaps flagged, not dropped: Nasdaq dividends calendar endpoint unusable (string payload); Yahoo v8 `events=div` empty; Yahoo v10 quoteSummary calendarEvents empty; IV-inputs pull ran on legacy Yahoo-only path (repo failover module unavailable on the clone's branch).
- No git push/pull, PRs, code changes, or GitHub operations in this run. Research and input only.
