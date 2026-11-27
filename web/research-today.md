# Hedge-Desk Daily Research — Fri 2026-11-27

**As-of:** Fri 2026-11-27 ~13:30 PT. Markets closed Thu Nov 26 (Thanksgiving); today a half-day session (1:00pm ET close). Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Research-only: no pushes, PRs, or code changes. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; UNVERIFIED = looked, could not confirm.

## Decision-relevant items (top 5)

1. **Desk 7 — Dec 9 hike call holds, tally unchanged 5 HIKE / 0 CUT / 5 NEUTRAL.** Kalshi 25bp $0.94 (total hike $0.97, up from $0.95), FedWatch ~97–99%. 10Y fell 6bp to 4.85%, 2s10s flattened to +24bp. Next decisive prints: Oct JOLTS ~Dec 2, claims Dec 3, Nov payrolls + Michigan prelim Dec 4.
2. **Gulf supply-risk premium is now the marginal crude driver.** Brent $96.57 Thu (highest since Nov 6) on the Ras Tanura/Jazan refinery strikes; OPEC+ meets Sun Nov 29. USTR Section 301 tariff proposals (up to 20% China, 35% Vietnam) are a live Jan-2027 tail-risk for watchlist semis/electronics/autos supply chains — proposed only, not priced.
3. **Index vol normalized off the Nov 5 shock; single-name vol still unreadable.** SPY/QQQ windows cleared the stale-jump screen (27.1%/25.5%); all four singles still WINDOW-CONTINGENT. Live 30d IVs sit below 20d realized for all six, but no clean "cheap premium" call. IV rank UNVERIFIED for all names.
4. **No watchlist earnings in the next two weeks; one routine dividend.** Next reports are the late-January cluster (MSFT Jan 26 earliest, dates UNVERIFIED). Adjacent prints to watch: CRM/SNOW Dec 2, AVGO/ADBE Dec 9, COST Dec 10. Only ex-date in the 4-week window: NVDA Dec 2, unchanged $0.25.
5. **Watchlist prices rebounded sharply off Nov 20 lows into the holiday.** NVDA +19.9% ($125.53 → $150.49), TSLA +15.7%, QQQ +7.0%, SPY +5.6% — mechanically compressing forward yields (MSFT 0.80%, NVDA 0.66%, AAPL 0.30%); none is an income opportunity at current prices.

---

## 1. Earnings Event desk

**Verdict: No watchlist earnings in the next 2 weeks — nothing material.**

**Window:** Fri Nov 27 – Fri Dec 11, 2026. Nasdaq earnings calendar API returned HTTP 200 with live rows on every date checked — 253 rows total — and **zero watchlist symbols on any of them**. [FACT — Nasdaq earnings calendar API, live pull Fri 2026-11-27 ~13:30 PT] SPY and QQQ are ETFs and report no earnings. No options-implied expected move or historical earnings-day move is computable — none exists inside the window; both are not applicable, not estimated.

**Next report per watchlist name (all outside the window; all estimates, not company-confirmed — treat as UNVERIFIED):**

| Symbol | Next report | Timing | Consensus EPS |
|---|---|---|---|
| MSFT | Tue Jan 26, 2027 | After close (est.) | ~$4.86–4.87 (carried from 2026-11-26 package, not re-verified) |
| AAPL | Jan 27 – Feb 4, 2027 | After close (est.) | ~$2.91–2.96 (carried, not re-verified) |
| TSLA | Jan 26 – Feb 3, 2027 | After close (est.) | ~$0.51 (carried, not re-verified) |
| NVDA | Feb 23–24, 2027 | After close (est.) | ~$2.87–2.88 (carried, not re-verified) |

Estimator disagreement widened since yesterday: AAPL was Jan 27–28, now Jan 27 (summitcapnews) vs Feb 4 (TradingView); TSLA was Jan 27, now Jan 26 vs Feb 3; NVDA Feb 23 vs Feb 24. MSFT is the only name with a single-date consensus (Jan 26). No company has confirmed any of these dates. [INFERENCE]

**Last watchlist print (context):** NVDA Q3 FY2027, Tue Nov 17 after close — revenue $115.84B vs ~$109.28B expected; EPS $2.68 vs ~$2.49 expected; $130B Q4 guide. Shares fell 2.89% the next session ($155.46 → $150.96). [FACT — carried from prior verified runs] No statement teardown this run: no watchlist release exists in the window to read.

**Adjacent (outside watchlist, in window — verified at the Nasdaq feed this run):**

| Date | Symbol | Timing | Consensus EPS (Nasdaq feed) | Note |
|---|---|---|---|---|
| Tue Dec 1 | MRVL | After close | $0.79 (12 est.; last yr $0.62) | AI-chip read-through |
| Tue Dec 1 | OKTA / MDB | After close | $0.43 / $0.08 | Software |
| Wed Dec 2 | CRM | After close | $2.41 (13 est.; last yr $2.66 — forecast *below* last year) | Enterprise software / AI spend |
| Wed Dec 2 | SNOW | After close | ($0.32) (11 est.; last yr ($0.84)) | Data/AI spend |
| Wed Dec 9 | AVGO | After close | $3.45 (10 est.; last yr $1.61) | $1.4T — the week's anchor print |
| Wed Dec 9 | ADBE | After close | $5.11 (12 est.; last yr $4.55) | Same evening as AVGO |
| Thu Dec 10 | COST | After close | $4.89 (11 est.; last yr $4.34) | Consumer bellwether |
| Thu Dec 10 | CIEN | Pre-market | $1.77 (8 est.; last yr $0.64) | Optical/AI networking |

**Basis conflict flagged (do not resolve by picking one):** MarketBeat/TipRanks quote AVGO $3.83 and ADBE $6.33 for Dec 9 — materially above the Nasdaq feed's $3.45 / $5.11. [INFERENCE] The gap is consistent with a GAAP vs adjusted-non-GAAP basis difference (Nasdaq's AVGO last-year EPS is $1.61 vs the $3.32 actually reported Sep 2 on an adjusted basis), but the basis of each feed was not confirmed at source, so both figures stay source-attributed and neither is cited as the consensus.

**What would change it:** a watchlist company confirming (8-K / IR notice) or advancing a report date into Nov 27–Dec 11, or a Nasdaq calendar update adding a watchlist symbol to any date in the window. The late-January cluster enters the 2-week window around Jan 12–13, 2027.

**Sources:** Nasdaq earnings calendar API (`https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`, all 11 dates Nov 27–Dec 11). Next-date estimates: summitcapnews.com, tradingview.com, smartcalendars.ai (search, 2026-11-27). AVGO/ADBE consensus conflict: MarketBeat, TipRanks.

---

## 2. Dividend Opportunity desk

**As-of:** Fri 2026-11-27 ~13:30 PT. **Window:** Nov 27 – Dec 25, 2026 (4 weeks). Sources: Nasdaq dividends calendar API (per-date pull, full row detail), Yahoo v7 quote (cookie+crumb, this session), issuer announcements. The two bases agree on every ex-date below.

### Upcoming ex-dividend dates in window

| Symbol | Ex-date | Amount | Record | Payable | Forward yield | Increase / cut / special | Consecutive-increase count |
|---|---|---|---|---|---|---|---|
| NVDA | **Wed Dec 2, 2026** | $0.25/qtr ($1.00/yr) | Dec 2, 2026 | Dec 23, 2026 | 0.66% ($1.00 on $150.49) | None — re-declared at unchanged rate | UNVERIFIED (third-party figures only; not issuer-verified this run) |

[FACT — Nasdaq calendar row (announced 11/17/2026) + Yahoo v7 quote (exDividendDate 2026-12-02, divRate 1.00)]

### Increases, cuts, specials
- **No new increase, cut, or special dividend announced in this window.** [FACT — Nasdaq calendar scan Nov 27–Dec 25]
- **NVDA — re-declared, NOT a new increase:** the Nov 17, 2026 earnings release declared the $0.25 quarterly dividend at the **unchanged** rate. The actual increase was May 2026: $0.01 → $0.25. [FACT] Do not report the Nov 17 declaration as a raise.
- **MSFT — increase already in effect, not new:** Sep 15, 2026 board raise $0.91 → $0.98 (+$0.07, ~7.7%); ex-date was Thu Nov 19 — now outside this window. First payment at the new rate Dec 10, 2026. [FACT, Microsoft newsroom]
- **MSFT streak-count conflict, resolved per desk standard:** third-party screeners disagree — Pluang/WiseVoter/Finbold say "25 consecutive years," AlgoDip says 20. The standardized definition (`dividend-count-standard.md`, issuer-verified Oct 5) is **24 consecutive annual increases** (incl. the Sep 2026 raise; initiated 2003; count increments on announcement date). [FACT] Do not drift to the screener figures.

### Names with nothing in the window
- **SPY — nothing in window; December distribution not yet declared.** [FACT] Last distribution $1.889, ex Sep 18, 2026. Next quarterly distribution expected ~Dec 18 (third Friday) — INFERENCE from cadence, not yet declared: no SPY row on the Nasdaq calendar Dec 18, and no SPY row on any scanned date Nov 27–Dec 25. Trailing yield 0.78% ($5.662/yr on $728.32). [FACT, Yahoo v7 quote]
- **QQQ — nothing in window; December distribution not yet declared.** [FACT] Last distribution $0.751, ex Sep 21, 2026. Next expected ~Dec 21–22 — INFERENCE, not yet declared. Trailing yield 0.27% ($1.77/yr on $650.99). [FACT, Yahoo v7 quote]
- **AAPL — nothing in window; went ex two weeks ago.** [FACT] $0.27/qtr, ex-date Thu Nov 12, 2026, paid Nov 16, 2026. Next expected ~Feb 2027 (INFERENCE from quarterly cadence). Forward yield 0.30% ($1.08/yr on $358.54). AAPL's consecutive-increase count remains **UNVERIFIED** per desk standard — not checked against Apple IR this run; payment history confirms annual May raises ($0.25→$0.26 May 2025, $0.26→$0.27 May 2026).
- **TSLA — no dividend.** [FACT] (Yahoo quote: dividendYield 0.0.)

### Price context for the yield math — sharp rebound since last Friday
[FACT, Yahoo v7 quote closes, Nov 27 vs Nov 20] SPY 728.32 (+5.6% from 689.81), QQQ 650.99 (+7.0% from 608.45), AAPL 358.54 (+4.7% from 342.56), MSFT 492.85 (+1.7% from 484.52), NVDA 150.49 (+19.9% from 125.53), TSLA 400.00 (+15.7% from 345.82). Yields are mechanically lower than last week's on the higher prices; that is arithmetic, not a dividend change. NVDA's rebound follows the Nov 23 board reinstatement of Huang as President/CEO (verified at NVIDIA Newsroom Nov 23) — context only; the dividend facts are unchanged.

| Symbol | Close Nov 27 | Forward yield (today) | Forward yield (Nov 20) |
|---|---|---|---|
| MSFT | $492.85 | 0.80% ($3.92/yr) | 0.81% |
| NVDA | $150.49 | 0.66% ($1.00/yr) | 0.80% |
| AAPL | $358.54 | 0.30% ($1.08/yr) | 0.32% |
| SPY | $728.32 | 0.78% trailing | 0.79% trailing |
| QQQ | $650.99 | 0.27% trailing | 0.27% trailing |
| TSLA | $400.00 | 0.00% | 0.00% |

### Value-lens read [INFERENCE]
Yields remain thin (MSFT 0.80%, NVDA 0.66%, AAPL 0.30%) — none is an income opportunity at current prices; the dividend signal here is balance-sheet strength, not margin of safety. The only dated dividend event in the next four weeks is NVDA's Dec 2 ex-date — a routine $0.25 payment, not a catalyst.

**Verdict:** One routine ex-date in the window (NVDA, Dec 2, unchanged $0.25). No increases, cuts, or specials announced. SPY's December distribution is the item to watch — expected ~Dec 18, not yet declared; QQQ's ~Dec 21–22 likewise undeclared. **What would change this verdict:** an SPY/QQQ December distribution declaration, or any issuer announcement of a raise/cut/special.

**Sources:** Nasdaq dividends calendar API (per-date Nov 27–Dec 25, 2026); Yahoo v7 quote (cookie+crumb, Fri Nov 27 half-day close); Microsoft newsroom Sep 15, 2026; NVDA Q3 FY2027 release Nov 17, 2026; desk standard `~/workspace/hedge-desk-research/dividend-count-standard.md`.

---

## 3. Overnight Premium desk (IV)

### IV-inputs freshness — FRESH (guard passed)
- **File:** `~/workspace/hedge-desk-research/nightly/2026-11-26-iv-inputs.json`, `as_of` **2026-11-26T14:54:30-07:00** — **23.5h old** at run start (13:26 PT), inside the 26h guard. **Printed 6/6** — breaks the recent null streak. [FACT]
- **Why it printed:** Nov 26 was Thanksgiving (market closed), so the Nov 27 expiry's 16:00 ET death moment had not passed at pull time; the guard never tripped. [INFERENCE]
- **Data vintage — label this:** the file's quotes and realized window (Oct 29–Nov 25) are effectively **Nov 25 close data**, not Nov 26. Do not present as Nov 26 data. [FACT]
- **File caveat:** `failures` notes the repo failover module was unavailable, so this is the **legacy Yahoo-only pull**. [FACT]

### Per-symbol snapshot

| Symbol | ATM IV, Nov 26 file (1 DTE, exp Nov 27) | Realized 20d (Oct 29–Nov 25) | Max single-day var. share | Window-contingent? | Live ATM IV today, Nov 27 13:27 PT post-close (3 DTE, exp Nov 30) | Live ~30d IV (27 DTE, exp Dec 24) | Spot (live) |
|---|---|---|---|---|---|---|---|
| SPY | 23.35% | 32.53% | 27.1% | No | 14.31% | 19.73% | 728.32 |
| QQQ | 36.62% | 49.01% | 25.5% | No | 21.88% | 29.24% | 650.99 |
| AAPL | 23.77% | 28.87% | 44.7% | **Yes** | 15.74% | 22.94% | 358.54 |
| MSFT | 35.07% | 39.46% | 36.6% | **Yes** | 24.54% | 33.92% | 492.85 |
| NVDA | 72.78% | 130.67% | 58.2% | **Yes** | 51.71% | 65.52% | 150.49 |
| TSLA | 49.90% | 74.89% | 32.3% | **Yes** | 34.27% | 49.87% | 400.00 |

Sources: Nov 26 file; live pull via Yahoo v7 options, cookie+crumb handshake, nearest **unexpired** expiry — the Nov 27 expiry died at 13:00 PT today (half-day close), so the live read rolls to Nov 30 by necessity, not by the (still inert) pull switch. Full live JSON saved to `~/workspace/goals/hedge-desk-daily-research/hidden_files/2026-11-27-live-iv-supplement.json`. **IV rank: UNVERIFIED for all six** — no free IV-history source; never guessed. [FACT]

### Stale-jump screen — what changed
- **SPY/QQQ cleared the screen on Nov 24** (shares 35.5%/33.8% on Nov 23 → 27.1%/25.8% Nov 24) as new variance entered the window; they stay sub-30% in the Nov 26 file. IV-vs-realized reads for the indexes are usable again, with the caveat that realized is backward-looking and still carries the Nov 5 crash regime. [FACT]
- **Singles still WINDOW-CONTINGENT:** AAPL 44.7% (Nov 4 up-day), MSFT 36.6% (Nov 4), NVDA 58.2% (Nov 20), TSLA 32.3% (Nov 5). No clean IV-vs-realized verdict for any single name. [FACT]
- **Calendar correction to the standing note:** Nov 28, 2026 is a **Saturday** (verified via `date`); the next window roll is Mon Nov 30, and by close-count the Nov 5 return stays inside the 20-close window until the Dec 7 pull — the "ages out Fri Nov 28" note does not match the file's window dates. Treat the Nov 28 aging-out as **UNVERIFIED**; the sub-30% clearing for SPY/QQQ already happened Nov 24 instead. [INFERENCE from file windows + calendar]

### IV vs realized — no clean "cheap premium" call
- All six 30d live IVs sit below their 20d realized vols (e.g. SPY 19.7% vs 32.5%, NVDA 65.5% vs 130.7%). For SPY/QQQ this is a usable observation (clean windows); for the four singles it is **WINDOW-CONTINGENT, not a verdict** — the realized leg is dominated by one day each. [INFERENCE]
- Term structure is upward-sloping (front 3 DTE < 30d) for all six in today's live pull — normal contango, no front-month hump. The Nov 26 file's 1 DTE prints ran hotter than today's 3 DTE prints (SPY 23.4% vs 14.3%); different dates/tenors, so that gap is noted, not interpreted as a move. [FACT + INFERENCE]

### Elevated-IV flags
- **NVDA (51.7% / 65.5%) and TSLA (34.3% / 49.9%)** are elevated in absolute terms — but both realized windows are window-contingent, so "rich" vs "cheap" is **UNVERIFIED**; no flag beyond the level itself. [FACT]
- **No elevated-IV-rank flag can be verified** for any name (IV rank UNVERIFIED — see above).

### Earnings inside the window — none
- `next_earnings: null` for all six in the Nov 26 file (45-day lookahead). No watchlist earnings in the next 2 weeks; nothing binary is priced into the front month, consistent with the flat term structure. [FACT]
- Note: Yahoo's quote `earningsTimestamp` returns the **last-reported** date (AAPL Nov 2, MSFT Oct 28, NVDA Nov 17, TSLA Oct 21) — not a next date; not used. [FACT]

### Expectation for today's 13:54 nightly pull
- [INFERENCE] Likely **null 6/6 on the expiry-day guard** — the Nov 27 expiry died at 13:00 PT today and the pull switch remains inert, so the nearest-expiry chain is dead contracts. If it prints, that itself is the story.

**Verdict — thesis:** index vol has normalized off the Nov 5 shock (SPY/QQQ screens clear, 30d IV 19.7%/29.2% vs realized 32.5%/49.0%), but single-name vol is still unreadable against one-day-dominated realized windows. **Evidence:** Nov 26 file + live Nov 27 pull, both 6/6. **What would change it:** singles' variance shares falling below 30% (next real test: Mon Nov 30 window roll), or a verifiable IV-rank source.

---

## 4. Open Quant/AI Model Lab

**Coverage note (FACT, arXiv listing + API, as of 2026-11-27 21:30 UTC):** No new arXiv announcement today — the q-fin listing still shows Thu 26 Nov (10 new + 4 cross, all accounted for in the 2026-11-26 run), and the API `submittedDate` range Nov 26 00:00Z–Nov 27 23:59Z returns **0** q-fin submissions (newest overall: 2611.34771, 2026-11-25T17:36:04Z). Thanksgiving lull; the Nov 26–28 window re-covers next run. GitHub leg skipped per the run brief's ban — no repo contents/license verification; code links below are stated, NOT verified. All candidate claims below are source-reported from abstracts read at source, labeled **UNVERIFIED** (abstract only, full papers not read).

### New candidates (all scorer-run with the repo module, never hand-scored)

| # | Candidate | Venue / Date | Score | Disp. | Relevance / reason |
|---|---|---|---|---|---|
| 411 | Gauthier/Godin/Legros — "Deep Implied Volatility Factor Models for Stock Options" | SSRN 5283770, posted 12 Jun 2025, rev 21 Feb 2026 | 54 | **WATCH** | Deep IV factor model for daily single-name IV surfaces; time-to-earnings improves performance around announcements; stock-level VIX-style indices track official benchmarks; results incl. **AAPL** + 5 stocks. Directly premium/earnings-desk relevant. No code link. Scorer: signal 4 / data 3 / impl 3 / risk 3 / cred 3, reproducible False. |
| 410 | Ammon/Heinz — "Exploiting Common Volatility Dynamics in High-Dimensional Portfolio Selection" | arXiv:2611.23952v1, 18 Nov 2026 (econ.EM — missed by the q-fin listing) | 51 | **WATCH** | Pooled ARMA vol models admit an exact dynamic factor representation; with realized DCC + nonlinear shrinkage, OOS min-variance S&P 500 portfolios — pooling beats alternatives across constraints. Covariance-forecasting lane; overlaps #328/#333. No code link. Scorer: 3/3/3/3/3, reproducible False. |
| 412 | Chuang et al — "Statistical Predictability vs Economic Value: TSFMs vs GARCH-MIDAS" | SSRN 7383932, posted 1 Sep 2026 | 48 | **WATCH** | TimesFM 2.5 / Chronos / Moirai vs GARCH-MIDAS on WTI, S&P 500, gold vol: TSFM strategies stronger at short horizons, but gains clearest in crude, less robust for SPX/gold; GARCH-MIDAS remains a strong interpretable benchmark. Feeds the #399 horse race. No code link. Scorer: 3/3/2/3/3, reproducible False. |
| 413 | Neururer/Papadakis — "Skew Premiums around Earnings Announcements" | SSRN 3648496, posted 10 Aug 2020, rev 19 Aug 2025 | 48 | **WATCH** | Delta-neutral risk-reversal skew premiums around earnings are economically significant and not explained by VRP changes; negative-skew firms' negative premiums triple on announcements. Earnings/premium-desk prior. No code link. Scorer: 3/3/2/3/3, reproducible False. |
| 414 | Singh et al — "Machine Learning, Market Volatility, and the Changing Dynamics of Risk" | SSRN 7681368, posted 10 Nov 2026 | 34 | **ARCHIVE** | NIFTY 50 only; target is a 5-day squared-returns proxy, not intraday RV; 6-page note. Band discipline. Scorer: 2/2/2/2/2, reproducible False. |
| 415 | Nishat — "Mitigating Transaction-cost Degradation via Volatility-gated Inference" | SSRN 7405518, posted 4 Sep 2026 | 31 | **ARCHIVE** | FX-only (EUR/USD), 4-page note; vol-gated trade-abstention rule with no desk lane. Band discipline. Scorer: 1/2/2/2/2, reproducible False. |

**Ledger append confirmed:** rows #410–#415 added to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (414 rows total, verified on disk); jidoka log entry for 2026-11-27 appended. Triage exclusions (no rows): Pimentel 6006035 (#324, already ARCHIVE); JBF 2017 "Volatility spread and stock market response to earnings" (paywalled, no open code/data, prior already known); Tinbergen "Option Pricing of Earnings Announcement Risks" (identity/date not verified at source this run).

### Movement on existing items
- **#209 v1→v3** (updated 2026-11-24, retitled "Evaluating LLM Research Agents as Tests of Return Predictability"): abstract now quantifies — agents report beat-the-mean in 16–44% of 110 null samples vs 8% Holm-adjusted; a 5%-level instruction cuts false positives to 0–3% but detection at population R²=1% falls sharply (Claude Opus 5.5 74%→45%, GPT-6.1 Sol 59%→6%, Terra 71%→15%). Stays **WATCH**.
- **#330 v1→v2** (updated 2026-11-25, "introduction clarified, references added"; no method/results change). Stays **WATCH**.
- **2611.20589 WITHDRAWN** (accidental duplicate submission; was a triage exclusion, no ledger row).
- Re-checks via arXiv API id_list: #4 (v1), #9 (v2), #13 (v1), #14 (v3), #15 (v1), #20 (v2), #21 (v3), #25 (v4, 2026-11-10), #30 (v3), #31 (v3), #255 (v2, 2026-11-20), #257 (v2), #312, #331–#333, #335–#337, #339–#342, #344–#351, #352–#357 — no other version movement; all stay WATCH/ARCHIVE as recorded. **No TEST/INTEGRATE movement (run max 54).**

**Verdict:** Most decision-relevant item is **#411 (Gauthier/Godin/Legros deep IV factor model)** — the only new candidate that touches a watchlist name (AAPL) with an earnings-timed single-name IV surface; otherwise a thin Thanksgiving-week sweep, nothing material enough to change any desk's method today.

---

## 5. Weather / War / Logistics Futures Events

**As of ~13:26 PT Fri 2026-11-27** (US half-day session closed 10:00 PT; CME grains closed 10:00 PT). Markets were closed Thu Nov 26 (Thanksgiving).

### Catalyst table

| Event | Date/time | What happened | Futures-curve read | Source / as-of |
|---|---|---|---|---|
| **Houthi claim: Ras Tanura refinery strike** | Wed Nov 25 (claim) | Houthis claimed a hit on Saudi Arabia's 550,000 b/d Ras Tanura refinery, the kingdom's largest refinery and a major crude export hub. Satellite imagery reviewed by ISW/CTP showed a likely hit (two storage tanks burnt, per OilPrice); Saudi authorities did not confirm damage. **FACT (claim + imagery) / UNVERIFIED (damage extent).** | Brent +3.5% Wed to $94.61; WTI +2% to $83.68. Risk premium, not a verified supply loss. | Reuters via LA Post / TBS News; Strategic Energy Map log; OilPrice, Nov 27 |
| **Jazan refinery projectile strike** | Thu Nov 26 | Projectile struck Saudi Aramco's Jazan refinery; some operations temporarily halted; one Nepalese worker killed, several wounded. **FACT** — confirmed by Saudi Energy Ministry statement. | Brent settled Thu $96.57 (+$1.96, +1.2%), highest close since Nov 6. WTI did not settle (US holiday). | Reuters via LA Post / TBS News, Nov 27 |
| **IRGC claims two tankers hit mines in Hormuz** | Thu Nov 26 | Iran's IRGC claimed two tankers, incl. a supertanker said to carry >2m bbl, hit sea mines north of Oman's Khasab and caught fire. **UNVERIFIED** — single-source claim, no independent confirmation found. | Contributed to Thu/Fri risk premium; no verified export-volume impact. | Strategic Energy Map log, Nov 27 (labelled "military unverified") |
| **Crude — Fri session** | Fri Nov 27 | Brent ~$95.20 at 10:16 ET (−$1.42 on the day); WTI ~$84.95 (+1.5%). On track for first weekly gain in November, snapping a 3-week losing streak. **FACT** (Reuters prints). | Curve pricing a war-risk premium on top of a still-soft physical balance; Dated Brent nearing $100 while 2027-surplus forecasts persist — tension, not resolution. | Reuters via LA Post; Morningstar DJ, Nov 27 |
| **EIA Weekly Petroleum Status Report** | Released Wed Nov 25, 10:30 ET; week ending Nov 20 | Commercial crude +1.1m bbl to 418.9m bbl (vs Reuters poll +1.5m) — 3rd straight weekly build, ~3% below 5-yr avg. Gasoline +1.7m to 217.7m; distillate +0.7m to 105.6m (−6% vs 5-yr avg). SPR −2.9m to 273.5m (ongoing draw under the DOE's 172m-bbl release). Production record 14.065m b/d. Refinery runs 97.5%. Cushing 25.6m. **FACT.** | Builds are bearish on paper, but price rose anyway — geopolitical premium outweighed the inventory signal this week. | EIA table1.pdf (primary); WSJ/Reuters, Nov 25 |
| **EIA Natural Gas Storage** | Released Wed Nov 25, 12:00 ET (moved a day early for Thanksgiving); week ending Nov 20 | First withdrawal of the heating season: −24 Bcf to 3,858 Bcf, vs ~−19 Bcf consensus; +2.1% vs 5-yr avg, −2.0% vs year ago. **FACT.** | Jan futures ~$3.63–3.66 post-print; mild-weather ceiling ~$3.68, floor ~$3.50. Next report Thu Dec 3. | EIA Weekly Natural Gas Storage Report (primary); TradingNews/Natural Gas Intelligence, Nov 25 |
| **USDA Weekly Export Sales** | Released Fri Nov 27 morning (delayed from Thu); week ending Nov 19 | Corn 1.93 MMT (+21% w/w, near top of expectations; Mexico top buyer). Wheat 564,700 t (+64%). Soybeans 755,800 t (−50% w/w, below expectations) but soybean meal 543,500 t — a marketing-year high. Flash sale: 132,000 t soybeans to Netherlands. **FACT.** | Jan soybeans +1.8% Fri to $12.66¼; Mar corn +1.4% to $4.63; Mar wheat +0.6% to $5.91 — broad post-holiday commodity rebound, not an export-sales repricing alone. | USDA via Morningstar DJ / CME Group, Nov 27 |
| **USTR Section 301 determinations — 14 economies** | Wed Nov 25 | USTR determined "structural excess capacity" practices of China, EU, Singapore, Switzerland, Indonesia, Malaysia, Cambodia, Thailand, Korea, Vietnam, Taiwan, Bangladesh, Japan, India are unreasonable/burdensome under Section 301(b). Proposed additional tariffs: China up to 20%, EU/Japan/Korea/Switzerland/Taiwan 15%, SE Asia up to 18%, Singapore up to 20%, India up to 25%, Vietnam up to 35%. **FACT — but proposed only, NOT in effect.** Comments due Jan 5, 2027; hearings begin Jan 25, 2027; Mexico/Norway undecided. Sectors named: autos, steel, semiconductors, pharma, chemicals, electronics, solar, textiles, shipbuilding. **FACT** (verified at USTR primary source). | No tariff is priced into any futures curve yet — the curve read is *absence*: a Jan 2027 decision tail-risk for semis/electronics/autos supply chains (watchlist: NVDA, AAPL, MSFT, TSLA). **INFERENCE.** | ustr.gov press release, Nov 25; Lexology/Wiley summaries |
| **BEA: Oct PCE + Q3 GDP 2nd estimate** | Wed Nov 25, 08:30 ET | Core PCE +0.3% m/m, 3.3% y/y (vs 3.2% expected, 3.1% Sep); headline 3.8% y/y. Q3 GDP revised to 4.3% annualized from 3.4% advance. **FACT** — corroborated across BEA-via-T. Rowe Price, Barron's, Zacks, Kitco, ING. | Gold fell below $3,500 Wed (15-month low) on the hot print, then rebounded Fri (see below). ING view: 3-mo annualized core PCE 3.6% "all but seals a 25bp hike on Dec 9" — **INFERENCE (ING's, not BEA's).** Desk 7 owns the Fed call. | BEA via multiple wires, Nov 25 |
| **Precious metals reversal** | Fri Nov 27 | Front-month gold +2.9% Fri to $3,639.60; silver +7.8% to $43.167 (largest single-day % gain since Feb 3); platinum +6% to $1,313.90. Weekly: gold +3.5%, silver +5.1%. Driver cited: AI/tech rebound + risk appetite + weaker dollar after Wed's selloff. **FACT (prices) / INFERENCE (driver attribution).** | Snap-back from a 15-month low, not a new trend — thin holiday trade; no single confirmed trigger. | WSJ / Morningstar DJ Commodities Roundup, Nov 27 |
| **OPEC+ meeting** | Sun Nov 29 | Group meets Sunday to review production policy. Reuters (3 sources): expected to keep Q1 2027 output targets unchanged. Counter-pressure: Iraq pushing OPEC for higher output (Barchart). **INFERENCE on outcome; FACT that the meeting is scheduled.** | Market pricing "unchanged" into the weekend; any surprise cut/hike vs the Hormuz disruption reprices crude Monday. | Reuters via LA Post, Nov 27; Barchart, Nov 26 |
| **Ukraine drone strikes on Russian refineries** | This week | Ukraine struck Slavyansk ECO refinery (70,000 b/d), seriously damaging the main crude distillation unit. **FACT** (reported). | Marginal vs the Gulf premium; adds to the global refining-tightness bid. | OilPrice, Nov 27 |

### Data-quality flags (CFA reconciliation)
- **Yahoo futures feed conflicts with Reuters on crude Friday:** Yahoo v8 chart printed CL=F $83.08 / BZ=F $90.84 intraday, vs Reuters ~$84.95 WTI / ~$95.20 Brent at 10:16 ET. Yahoo's Wed closes matched the reported settles exactly (CL $83.68, BZ $94.61), so the Friday divergence is a feed/contract-roll artifact, not a market move. Reuters prints used above; Yahoo crude prints treated as **UNVERIFIED** for Friday. Yahoo ags/metals cross-checked clean (corn $4.63, wheat $5.91, soy $12.66¼, gold ~$3,660–3,668, silver ~$43.70 all match wire reports).
- **Term structure:** no verified contango/backwardation read from free sources today — curve shape **UNVERIFIED**, not guessed. Front-month levels only.
- **Background context, not fresh catalyst:** Strait of Hormuz has been closed to normal traffic since the Feb 2026 US–Israeli strikes on Iran and Hormuz crude clearance is ~55% of the pre-war baseline (Kpler via House of Saud / Strategic Energy Map). This is the standing condition behind this week's premium, not a new event.

### Watchlist relevance
- **No direct watchlist earnings/dividend catalyst from this desk.** Indirect: Section 301 tariff proposals name semiconductors, electronics and autos — the supply-chain tail-risk for NVDA / AAPL / MSFT / TSLA is a Jan 2027 decision, not a priced event. Oil/gas moves matter to SPY/QQQ only via the inflation → Dec 9 FOMC channel (Desk 7's lane).

### Ahead
- Sun Nov 29: OPEC+ meeting. Mon Nov 30: USDA Grain Export Inspections 11:00 ET, Crop Progress 16:00 ET. Tue Dec 1: USDA Grain Crushings 15:00 ET. Wed Dec 2: EIA petroleum 10:30 ET. Thu Dec 3: EIA gas storage 10:30 ET. Tue Dec 9: FOMC decision.
- Government-data status: no shutdown; CR funds through Dec 11; EIA/USDA on schedule (both Thanksgiving-week releases arrived, shifted a day). **FACT.**

**Verdict — most decision-relevant: the Gulf supply-risk premium is now the marginal crude driver — Brent $96.57 Thu (highest since Nov 6) on the Ras Tanura/Jazan strikes, with the OPEC+ meeting Sunday as the next repricing point; and USTR's proposed Section 301 tariffs (up to 20% China, 35% Vietnam) are a live Jan-2027 tail-risk for watchlist semis/electronics/autos supply chains, not yet priced.**

---

## 6. Box / Parity Observer

**Verdict: No actionable parity violation; parity holds within the funding/friction band.**

### 1. CBOE launches AM-settled weekly SPX options (SPXO) — material, in window
**FACT (Cboe, 9 Nov 2026):** Cboe now lists AM-settled weekly options on the S&P 500 under new symbol **SPXO**, extending AM settlement beyond the standard monthly third-Friday SPX. Initial expirations: **18 Nov and 16 Dec 2026**, aligned to standard monthly VIX settlement dates; additional weeklies to follow. SPXO settles to the SPX opening settlement price (SET), like monthly AM SPX. Source: https://www.cboe.com/insights/posts/cboe-introduces-am-settled-weekly-options-on-the-s-p-500-index/

**FACT (Cboe notice / SEC):** SPXO is price-time allocation (SPX remains pro-rata), minimum quote size 1 above $0, same matching unit 33 as SPX; complex orders may combine SPX/SPXO/SPXW but can only leg into single-leg books when all books share a matching unit — SPXW is separate, so SPXW + SPX/SPXO combos cannot leg in. Trading stops 17:00 ET the day before expiry with no GTH resumption that evening. Underlying SEC approval: Release No. 34-105678, SR-CBOE-2026-044, 12 Jun 2026. Fee filing applying the SPX/SPXW surcharge to SPXO: SR-CBOE-2026-085, filed 2 Nov, noticed 13 Nov 2026.

**INFERENCE:** Parity math itself is unchanged, but SPXO is a *different settlement basis* — an AM-settled SPXO box and a PM-settled SPX/SPXW box expiring the same calendar date are not interchangeable. Do not mix roots in a box or parity check. The 18 Nov SPXO expiry has already passed; the next live test is **16 Dec 2026**.

### 2. SPX box-spread financing measured — no exploitable violation
**FACT (Solvinc blog, data pulled 12 Nov 2026, ~15 days ago — just at the edge of the 2-week window):** A parity-regression scan of the full CBOE delayed SPX chain (31,016 contracts) found implied box rates of **3.86% at 15 days** (expiry 27 Nov 2026) rising to **5.16% at 435 days** (expiry 21 Jan 2028), vs SOFR 3.89% and 13-week T-bill 3.94% (10 Nov benchmarks) and ~5.39% for IBKR tier-1 margin (SOFR + 1.50%). 33 expiries passed the R² ≥ 0.995 gate, all reported R² = 1.0000. Source: https://blog.solvinc.io/posts/box-spread-financing-spx-rate-scanner/

**FACT (same source):** Naive per-box arithmetic on the delayed feed produced impossible prints (−95.66% to +186% APR) — attributed to stale-quote noise (±5 pts per leg), not to parity violations; the regression across 50–180 strikes per expiry is what cleans it.

**INFERENCE:** The curve reads as funding cost plus ~120 bp dealer rent at the long end, not a mispricing — the ~23 bp edge of a 435-day box over small-balance margin is real but small (~$117/yr on $50k) and largely consumed by four-leg execution spread (~40–60 bp round trip). No actionable arbitrage. Caveat: single-author blog, delayed (15-min) feed, not peer-reviewed and not independently replicated here — treat the levels as indicative, the *method* (regress synthetics, gate on R², never take minimum-of-noise) as the takeaway.

### 3. Index methodology — no change to the S&P 500 or Nasdaq-100 themselves
- **FACT (S&P DJI, announced 23 Oct 2026; effective before open 21 Dec 2026):** U.S. Style indices change — growth drops 12-month price momentum; value adds intangible-adjusted book-to-price, forward earnings yield (averaged with trailing), and free-cash-flow-to-price. **Parent-index admission criteria for the S&P 500 are unchanged.** Pro-forma files to clients from 4 Dec 2026; ~$375bn in linked passive assets per Bloomberg Intelligence estimate cited in coverage. Watch item for the 21 Dec reconstitution only — no SPX parity impact.
- **FACT (Nasdaq):** No new Nasdaq-100 methodology change in the last ~2 weeks. The May 1, 2026 changes (Full vs Modified Market Cap, Fast Entry, removal of minimum free-float, low-float share-count cap) have been in force since the June 2026 review. Recent Nasdaq filings are fees/ORF and a non-substantive rename of Outcome-Related Options to Nasdaq Event Options (SR-MRX-2026-28) — no parity impact.
- **No new empirical parity-violation paper in window:** the Quantopia put-call parity guide (24 Nov 2026) is a general primer, not new evidence; the arXiv SPX/RUT wedge paper (Shin, 26 May 2026) predates the window.

**Watch:** SPXO 16 Dec 2026 expiry (first live AM-weekly settlement test after launch) and S&P Style reconstitution 21 Dec 2026 (pro-formas 4 Dec).

---

## 7. Bonds & Rates desk (Desk 7)

**Status: Desk ran. Module `rates_desk.rates_environment()` executed this session, REAL_FRED_RATES mode. All rates levels independently verified against FRED. Tally UNCHANGED: 5 HIKE / 0 CUT / 5 NEUTRAL. Dec 9 25bp hike call HOLDS. Thanksgiving week — US markets closed Thu Nov 26, half-day Fri Nov 27; Nov 25 closes are the latest Treasury data, DFF posted Nov 26.**

### 7.0 Sentry W48 verification (rates_desk.py CONDITIONAL KEEP — module numbers NOT taken on trust)

Independent FRED pulls this session (`fred_observations.py`, `--limit=N` form):

| Finding | Module says | Independent check | Verdict |
|---|---|---|---|
| F1 — fed-funds change unsigned, no baseline | `fed_funds_change_over_window: 0.00` | DFF Sep 28, 2026: **3.88%** → Nov 26: **3.88%** | **VERIFIED as 0.00pp** — the number is right; the process finding (no baseline in output) stands |
| F2 — DFF is the wrong series | DFF 3.88 | FRED EFFR 3.88, Nov 25 — identical level | No material discrepancy in the level; finding noted, not load-bearing |
| F3 — curve-slope unit mix | `spread_10y_2y_points: 24.00`, `curve_slope: 0.030000` | Independent: 4.85 − 4.61 = **+24bp** (0.24pp) | **CONFIRMED LIVE — do not cite `curve_slope`.** 0.03 equals neither 0.24 (pp) nor 24 (bp). The 24bp spread figure agrees with the independent calc; the slope field does not |
| F4 — as_of defaults to wall clock | `as_of: 2026-11-27` | Latest FRED obs are **Nov 25** (DGS/SOFR/EFFR/OBFR) and **Nov 26** (DFF, HY OAS) | as_of is the run date, not the data date. All figures below are data-as-of Nov 25/26 as noted |
| F5 — DGS10 candidate dropped by key typo | DGS10 4.85 | Independent FRED DGS10 Nov 25: **4.85** | Level verified regardless; typo itself not confirmed from this session's output |

### 7.1 Rates table (FACT — FRED via module, independently verified; data as-of Nov 25, DFF Nov 26)

| Series | Read | Prior session(s) | Change |
|---|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 3.88% Nov 21–26 | 0.00 — flat 60+ days |
| Treasury 2Y (DGS2) | **4.61%** | 4.63% Nov 20, 23, 24 | −2bp vs Nov 24 |
| Treasury 10Y (DGS10) | **4.85%** | 4.91% Nov 24; 4.92% Nov 20, 23; 5.04% Nov 19 | −6bp vs Nov 24; −19bp since Nov 19 |
| **2s10s slope (independent calc)** | **+24bp** | +28bp Nov 24; +29bp Nov 20 & 23 | **−4bp d/d — flattening, still upward-sloping, no inversion** |
| SOFR | **3.95%** | 3.94% Nov 24; 3.92% Nov 23 | +1bp d/d |
| EFFR / OBFR | **3.88% / 3.88%** | Flat | — |
| **SOFR–EFFR funding spread** | **+7bp** | +6bp Nov 24; +4bp Nov 23 | Narrow; no funding stress (INFERENCE) |

Module shape call "UPWARD_SLOPING" agrees with the independent +24bp. Target range 3.75–4.00% (FACT, Oct 28 FOMC hold, federalreserve.gov).

### 7.2 Core-indicator table — today's read + broker POV

| Indicator | Trigger rule | Today's read (source, as-of) | Call | Broker POV — discount rate / margin of safety |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA) | HIKE if y/y > 2.5% or m/m > +0.25% | **Oct y/y +3.26%, m/m +0.29%**; index 131.312 vs Sep 130.929 vs Oct 2025 127.165 — recomputed from FRED levels this session (m/m +0.293%, y/y +3.261%), matches the Nov 25 release. No new print today | **HIKE** | Anchor the discount rate to the higher regime. The decision variable rose and consensus missed low — no re-anchor down. Next PCE (Nov, Dec 23) is after the decision and cannot change December. |
| Breakevens (T5YIE / T10YIE, FRED) | HIKE if > 2.75%; CUT if < 1.75% | **2.13% / 2.12%, Nov 25** (unchanged from Nov 24: 2.11%/2.12% — 5Y +2bp, 10Y flat; 2.31%/2.24% Nov 12) | NEUTRAL | Anchored and ~20bp below Nov 12: no credibility crisis, room for 25bp, not a forced 50bp. Tripwire remains a break above 2.75%. |
| Michigan expectations (U-M, manual) | HIKE if yr-ahead > 3.5% | **FINAL Nov yr-ahead 3.7%** (prelim 4.3%, Oct 4.7%), rel. Nov 20; 5–10yr 3.3% (Oct 3.5%). FRED MICH cross-check: Oct 4.7 — lagging as usual, confirms the lag, not the level. No new print today | **HIKE** | Still fires, but barely: 20bp above the tripwire. The household-vs-market gap is 3.7% vs 2.13% breakeven = 1.57pp. Dec 4 prelim is the flip watch — below 3.5% turns this line NEUTRAL. Do not average with breakevens. |
| Payrolls, 3-mo avg (PAYEMS, BLS/FRED) | HIKE if > +150k; CUT if < +50k | **+137k** (Oct +165k, Sep +60k, Aug +186k; levels Oct 159,293k, Sep 159,128k, Aug 159,068k — recomputed this session: (165+60+186)/3 = 137k). No new print; Nov payrolls due Dec 4 | NEUTRAL | Rule as written: NEUTRAL. One +165k print does not override the average. Note the margin: 13k below the HIKE tripwire — a strong Nov print flips this line. |
| Initial claims, 4-wk avg (ICSA, DOL/FRED) | CUT if > 300k; NEUTRAL < 250k | **196k** (w/e Nov 21: 189k; Nov 14: 202k; Nov 7: 202k; Oct 31: 191k — (189+202+202+191)/4 = 196k, matches the Reuters/DOL table's 196,000). **Correction to the Nov 26 package: the w/e Nov 21 release came out Wed Nov 25 (Thanksgiving-week shift), not Fri Nov 27; next release Dec 3.** Continuing claims 1.697M, down 95k | NEUTRAL | No action. Claims are drifting DOWN, away from the 300k tripwire. Next read Dec 3 — it turns first. |
| Job openings (JTSJOL, BLS/FRED) | HIKE if 3-mo change positive | **7,523k, Sep 2026** (Jul 7,335k → Sep +188k). No new print (Oct JOLTS expected ~Dec 2) | HIKE | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA/FRED) | HIKE if > 2.5% ann.; CUT if < 1.0% | **Q3 second estimate +4.3% annualized** (advance 3.4%, cons 3.5%), BEA Nov 25. FRED levels confirm: 24,665.201 vs 24,408.011 = +4.28% ann. No new print today | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Note the split: growth revised UP while the deflator revised DOWN (1.8% vs 2.3% exp) — real strength, less price pressure — which argues for 25bp, not 50bp. |
| Housing starts (HOUST, Census/FRED) | CUT if −5% over 3 months | **Oct 1,309k** (Sep revised 1,221k → 1,191k); Jul→Oct **−4.4%** (1,309 vs 1,369). No new print today | NEUTRAL | Confirms the Nov 18 flip: the −5% CUT tripwire no longer fires. Single-month rebound, 3-mo trend still negative — NEUTRAL, not HIKE. The strongest hold argument in the set has faded. |
| HY OAS (BAMLH0A0HYM2, ICE BofA/FRED) | CUT if > 5.00%; NEUTRAL < 4.00% | **3.77%, Nov 26** (3.77% Nov 25; 3.72% Nov 24; 3.20% Nov 12) | NEUTRAL | No stress at the level, but **+57bp widening since Nov 12** is the largest move in the set — watch. A break above 5.00% is the tripwire; at the current pace that is not imminent (INFERENCE). |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening / hawkish language | Oct 28: held 3.75–4.00%, **10–2, Cook + Hammack dissenting for +25bp**; statement: "Inflation remains elevated." Nov 18 minutes already digested Nov 23 (nearly all judged further hikes likely appropriate; several said >25bp could be justified in Dec if inflation data unfavorable). **No new guidance Nov 26–27** (Thanksgiving; no speakers). Carried: Williams (Mon Nov 23) "inflation too high," "more work to do" (secondhand); Waller remains the lone 50bp voice (would consider 50bp if Oct core CPI ≥ +0.3% — it printed +0.3% Nov 10, yet the tail sits at $0.03; markets did not follow him) | **HIKE** | Weight the vote above any single print: two dissents for an immediate hike is the Committee stating its lean. No hold-leaning Fed voice has emerged. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL — unchanged from Nov 23, Nov 25, and Nov 26.**

### 7.3 Market pricing vs the indicator read
- **Kalshi, direct API pull this session (~13:30 PT Nov 27, Dec-2026 `KXFEDDECISION-26DEC`):** 25bp hike **$0.94** (bid/ask 0.93/0.94, prev $0.93, +1¢; 24h vol ~332.5k, OI ~3.25M); >25bp **$0.03** (bid/ask 0.02/0.03, prev $0.03, flat); hold **$0.04** (bid/ask 0.04/0.05, prev $0.05, −1¢); cuts $0.01 each. Sum of lasts $1.03 (3¢ over-round). **Total hike $0.97 — up from $0.95 Nov 26 and $0.96 Nov 24.** The >25bp tail stays collapsed at $0.03 (was $0.12 on Nov 13).
- **CME FedWatch (secondhand — CME's own tool not directly readable; converging reads):** FrenzyCap /ZQ replication, **live Nov 27, 11:59 AM ET: 99% for 25bp, 1% hold, 0% for >25bp**, expected +25bp, EFFR after 4.127%. Other secondhand reads today: FXStreet 99% (citing CME FedWatch); wallstreetconservative 98.9%; TMGM 97%. Range **~97–99%**, up from ~96% Nov 26.
- **Agreement:** markets and indicators agree on direction (25bp hike) and size (tail ~$0.03 / 0%). One measurement gap, not a directional disagreement: futures-implied 25bp (~98.6% per predictionmarketspicks cross-venue table, Nov 27 1:00 PM ET) sits ~5pp above Kalshi's 93.5–94% — futures price the hike slightly harder than the prediction market; both agree it happens. Polymarket 25bp ~94.5%.
- **Jan 2027 is the live question, and it did not move:** Kalshi Jan H25 **$0.57** (bid/ask 0.56/0.57, prev $0.57 — flat vs Nov 26) vs hold $0.41 (was $0.43); >25bp $0.02. Total Jan hike $0.59. The Dec decision is priced; the January follow-through is not settled.

### 7.4 Verdict — thesis / evidence / what would change it
- **Thesis:** 25bp hike on Dec 9. **Holds.**
- **Evidence:** Core PCE re-anchored hotter (y/y 3.26% vs 3.2% cons, up from 3.1%; m/m +0.29% still above the +0.25% trigger); Q3 GDP revised up to +4.3%; the Oct 28 vote already leans hike (10–2 with two hawkish dissents); markets price it at ~97–99% / $0.94. The two dovish-leaning moves — Michigan final expectations falling to 3.7% and breakevens to ~2.12% — narrow the case for 50bp, they do not touch the case for 25bp. Housing's CUT signal is gone. Yields fell into the holiday (10Y −6bp, 2Y −2bp; 2s10s flattened 4bp to +24bp) without moving any trigger. Nothing printed today to move any line.
- **What would change it:** (a) November core PCE (Dec 23) is after the decision — cannot change December; (b) initial claims 4-wk avg above 300k — currently 196k and falling; next read Dec 3; (c) November payrolls (Dec 4) — the decisive pre-meeting print: a strong month flips the 3-mo avg above +150k (HIKE, strengthening the call), a weak one leaves it NEUTRAL; (d) Michigan Dec 4 prelim below 3.5% flips one HIKE line to NEUTRAL but would not alone overturn a 5–0 tally with markets at ~99%; (e) Oct JOLTS (~Dec 2) — a negative 3-mo change flips the JOLTS line; (f) a named speaker arguing for a hold, or the Dec 9 statement softening — none verified this session. The live 50bp voice is Waller alone; his stated CPI condition was met Nov 10 and the tail still sits at $0.03 — a second voter joining him plus a hot Nov CPI (Dec 10, after the decision) would matter for January, not December.
- **UNVERIFIED items:** CME FedWatch direct read (secondhand range only); Williams "too high" remark (secondhand press reports — INFERENCE-grade for guidance); earnings-yield vs bond-yield spread (no primary earnings-side source this session).

### 7.5 Graham lens (arithmetic from verified yields)
10Y **4.85%** (Nov 25) vs 4.91% (Nov 24) vs 4.98% (Nov 10) vs 4.86% (Nov 6). At assumed perpetual growth g = 3.00%, Gordon multiple 1 ÷ (r − g): **54.05x today** (1 ÷ 0.0185), up from 52.36x yesterday — **+3.23%**. Re-anchor to 4.85%. Duration ≈ 8 puts the −6bp move at ≈ **+0.48%** on a 10-year position. The margin of safety is slightly wider at the same prices on the bond side — but the bond side still pays ~4.9% on a contractual claim, so equity risk must be compensated from price; a wider required discount, not a chase for yield. Earnings-yield vs bond-yield spread: UNVERIFIED (no S&P earnings-yield figure from a primary source this session; no spread asserted).

**Sources:** FRED (fred-public CSV via `rates_desk.rates_environment()`, module run this session; independently re-pulled via `fred_observations.py` skill-CLI route): DFF, DGS2, DGS10, SOFR, EFFR, OBFR, PCEPILFE, T5YIE, T10YIE, MICH, PAYEMS, ICSA, JTSJOL, GDPC1, HOUST, BAMLH0A0HYM2 — data as-of Nov 25 (daily series), Nov 26 (DFF, HY OAS); monthly/quarterly series as noted. BEA, Personal Income and Outlays, October 2026 (released Nov 25, 8:30 ET): https://bea.gov/news/2026/personal-income-and-outlays-october-2026 ; BEA, GDP Second Estimate Q3 2026 (released Nov 25): https://bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-3rd-quarter-2026 . U-M Surveys of Consumers, final November results (released Nov 20): yr-ahead 3.7%, 5–10yr 3.3% — carried from the Nov 24 verification; FRED MICH still shows Oct 4.7 (lagging). DOL, Unemployment Insurance Weekly Claims, Nov 25 release (w/e Nov 21, 189k; 4-wk avg 196k): https://www.dol.gov/index.php/newsroom/releases/eta . Kalshi trade API v2, `KXFEDDECISION-26DEC` and `KXFEDDECISION-27JAN` event tickers, direct pull Nov 27 ~13:30 PT. CME FedWatch: secondhand converging reads — FrenzyCap /ZQ replication (live Nov 27, 11:59 AM ET, https://www.frenzycap.com/fedwatch/2026-12-09), FXStreet, wallstreetconservative, TMGM, predictionmarketspicks cross-venue table — labeled as such; CME tool itself not directly readable. Desk 7 consolidated deliverable: ~/workspace/hedge-desk-research/desk7-core-indicators.md (Nov 13 snapshot; today's reads supersede it line by line above). Prior-day Desk 7 section: ~/workspace/hedge-desk-research/2026-11-26.md §7.

**Desk 7 summary: no new indicator print today (Thanksgiving week); tally unchanged 5 HIKE / 0 CUT / 5 NEUTRAL; Dec 9 25bp hike call holds; Kalshi 25bp $0.94 (total hike $0.97), FedWatch ~97–99%; 10Y fell 6bp to 4.85%, 2s10s flattened to +24bp; Jan 2027 hike lean flat at $0.57. Next decisive prints: Oct JOLTS ~Dec 2, claims Dec 3, Nov payrolls + Michigan prelim Dec 4.**

---

## Cross-desk notes / corrections carried forward

- **Claims schedule correction:** the Nov 26 package said the next claims release was Fri Nov 27 — wrong. The w/e Nov 21 claims (189k, 4-wk avg 196k) were released Wed Nov 25 (Thanksgiving-week shift, confirmed at DOL + Reuters table); next release is Dec 3. The 4-wk avg (196k) is unchanged — only the schedule was wrong.
- **Nov 5 aging-out correction:** Nov 28, 2026 is a Saturday; the next 20-day window roll is Mon Nov 30, and by close-count the Nov 5 return stays inside the 20-close window until the Dec 7 pull. The standing "ages out Fri Nov 28" note is UNVERIFIED; SPY/QQQ already cleared the stale-jump screen Nov 24 instead.
- **Sentry F3 (rates_desk.py):** module `curve_slope: 0.030000` discarded a third straight session; use the independent +24bp 2s10s spread. F1 verified this session with a named baseline (DFF Sep 28 3.88% → Nov 26 3.88% = 0.00pp). Do not cite the module's fed-funds change or curve slope as FACT.
- **No desk failed.** All seven desks delivered; no retries needed. Quant Lab ledger rows #410–#415 appended (414 rows total). Live IV supplement saved to `~/workspace/goals/hedge-desk-daily-research/hidden_files/2026-11-27-live-iv-supplement.json`.
