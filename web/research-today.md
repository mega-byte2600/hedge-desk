# Hedge-desk research — Thu 2026-11-26 (Thanksgiving Day)

**Market status:** US equities and Treasury cash CLOSED Thu Nov 26 (Thanksgiving). Fri Nov 27 is a half-day session. All prices, IVs, and reads below carry Wed Nov 25 closes unless labeled otherwise. CME futures on shortened hours, no Thursday settlements. **FACT.**

**Watchlist closes — Wed Nov 25 (Yahoo v8 chart, re-pulled by the synthesizer today; bars verified against Nov 24 closes):**

| Symbol | Nov 25 close | Nov 24 close | Day move |
|---|---|---|---|
| SPY | 716.70 | 718.78 | −0.29% |
| QQQ | 633.93 | 638.10 | −0.65% |
| AAPL | 355.58 | 354.07 | +0.43% |
| MSFT | 489.93 | 496.13 | −1.25% |
| NVDA | 149.30 | 155.38 | −3.91% |
| TSLA | 380.14 | 384.68 | −1.18% |

**Synthesis correction (FACT — independent v8 pull this run):** Desk 3's day-move column (SPY −1.85%, QQQ −3.88%, NVDA −1.10%, etc.) is WRONG — it was computed against Yahoo's `chartPreviousClose` meta field, which is stale (SPY 730.20, QQQ 659.51, NVDA 150.96 are not Nov 24 closes). The table above, computed bar-to-bar from the daily closes, matches yesterday's package exactly. Desk 3's IV levels are unaffected (they come from the options chain, not the chart meta). Do not cite Desk 3's day-move percentages.

## The 5 most decision-relevant items

1. **Brent +3.51% to $94.61 on claimed Houthi strike on Ras Tanura refinery + claimed Iranian mine strikes on Hormuz tankers (Desk 5).** Damage, refinery-throughput loss, and any export-terminal interruption are UNVERIFIED — single-source / claimed only. EIA showed a commercial crude build vs seasonal norm, so the rally is war-risk premium, not a tighter physical balance. OPEC+ meets Sun Nov 29; reported expectation is a rollover of current targets for at least Q1 2027.
2. **Desk 7 unchanged: 5 HIKE / 0 CUT / 5 NEUTRAL; Dec 9 25bp hike call holds.** Kalshi Dec 25bp $0.92 (was $0.93), FedWatch ~96%. The live question moved to January: Kalshi Jan hike lean strengthened to $0.57 (was $0.54). Next decisive prints: Nov payrolls + Michigan Dec prelim, both Dec 4.
3. **IV prints are back after the expiry-day nulls (Desk 3), but no clean premium verdict exists.** Live 1-DTE ATM IV (Nov 27 expiry, Nov 25 marks): SPY 23.35%, QQQ 36.62%, NVDA 72.78%, TSLA 49.90%. SPY/QQQ IV sits ~8–13pts below trailing 20-day realized, but the realized leg is still Nov 5-inflated — not a clean "vol is cheap" call. AAPL, MSFT, NVDA, TSLA are WINDOW-CONTINGENT (single day >30% of realized variance); first clean read lands Dec 1. IV rank UNVERIFIED for all six.
4. **NVDA Dec 2 ex-div ($0.25, flat) is the only certain ex-div in the next four weeks (Desk 2).** SPY Dec 18 amount undeclared (declaration expected Dec 17); QQQ Dec 21 amount undeclared and its pay date is now disputed five ways — a new Jan 11, 2027 candidate citing Invesco is still UNVERIFIED at the issuer. No raises, cuts, or specials anywhere. A low-quality aggregator claim of an NVDA "dividend increase" is contradicted by the primary source and dismissed.
5. **No watchlist earnings in the next two weeks (Desk 1); no parity break (Desk 6); quant added 12 candidates, none promoted (Desk 4).** Next earnings cluster is late January (MSFT/AAPL/TSLA ~Jan 26–28, NVDA ~Feb 24 — all estimates, UNVERIFIED). Saxo's daily VIX parity check holds for a fourth straight session. Quant top of run (tied, 57): #361 news-embeddings look-ahead-bias paper and #370 VIX term-structure carry gate — both WATCH.

---

## 1. Earnings Event desk

**Verdict: No watchlist earnings in the next 2 weeks — nothing material.** [FACT — Nasdaq earnings calendar API, live pull 2026-11-26] The API returned HTTP 200 with live rows on every date checked (Nov 26: 14 rows; Nov 27, Nov 30, Dec 1–4, Dec 7–10) and zero watchlist symbols on any of them. SPY and QQQ are ETFs and report no earnings. No options-implied expected move or historical earnings-day move is computable — none exists inside the window; both are not applicable, not estimated.

**Next report per watchlist name (all outside the window; all estimates, not company-confirmed):**

| Symbol | Next report | Timing | Consensus EPS |
|---|---|---|---|
| MSFT | Jan 26–27, 2027 | After close (est.) | ~$4.86–4.87 |
| AAPL | Jan 27–28, 2027 | After close | ~$2.91–2.96 |
| TSLA | Jan 27, 2027 | After close | ~$0.51 |
| NVDA | Feb 24, 2027 | After close | ~$2.87–2.88 |

The Jan 27/28 AAPL split is a one-day estimation disagreement across aggregators, not a confirmed reschedule. [INFERENCE] Treat every date above as UNVERIFIED until the company confirms it.

**Last watchlist print (context, not upcoming):** NVDA Q3 FY2027, Tue Nov 17 after close — revenue $115.84B vs ~$109.28B expected; EPS $2.68 vs ~$2.49 expected; $130B Q4 guide. Shares fell 2.89% the next session ($155.46 → $150.96). [FACT — TipRanks/Zacks]

**Adjacent (outside watchlist, in window):** Broadcom (AVGO) Dec 9 after close; Adobe (ADBE) Dec 10 after close — carried from the Nov 25 package, not re-verified this run.

**Source failure log:** Yahoo v7 quoteSummary `calendarEvents` is a DEAD END this session — valid cookie + crumb obtained (crumb `Cf8WVjX7qfx`), yet HTTP 404 on both query1 and query2 for all four single names, retried once with backoff. Classified dead-end (endpoint path changed/retired), not transient. Cross-check via Nasdaq calendar (primary, live) + web search corroboration.

**What would change it:** a watchlist company confirming (8-K / IR notice) or advancing a report date into Nov 26–Dec 10, or a Nasdaq calendar update adding a watchlist symbol to any date in the window. The late-January cluster enters the 2-week window around Jan 12–13, 2027.

**Sources:** Nasdaq earnings calendar API, `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`, pulled 2026-11-26 for all 11 dates Nov 26–Dec 10. AAPL/MSFT/TSLA/NVDA next-date estimates via Portfolio Terminal, TipRanks, Zacks, MarketBeat (search, 2026-11-26).

---

## 2. Dividend Opportunity desk

**Window:** ex-dividend dates Nov 27 – Dec 24, 2026.

| Symbol | Ex-div date | Dividend | Yield* | Increase / cut / special | Consecutive increases (per standard) |
|---|---|---|---|---|---|
| NVDA | **Dec 2, 2026** (Wed) | $0.25/qtr ($1.00/yr) | 0.67% | Flat — 3rd consecutive qtr at $0.25; none | n/a |
| SPY | **Dec 18, 2026** (Fri) | **UNVERIFIED — amount not yet declared** (est. ~$1.89 is a repeat-of-Sep projection, not a declaration) | 1.06% TTM ($7.58 trailing) | None — pass-through, varies quarterly | n/a |
| QQQ | **Dec 21, 2026** (Mon) | **UNVERIFIED — $0.7941 quoted by aggregators; DividendMax still lists Dec 2026 as Forecast, no declared amount; declaration expected Dec 18** | 0.49% TTM ($3.09 trailing) | None announced | n/a |
| AAPL | None in window — last ex-div Nov 12, 2026 ($0.27, paid Nov 16); next expected ~Feb 11, 2027 (unannounced) | $0.27/qtr ($1.08/yr) | 0.30% | Last raise Apr 30, 2026: $0.26 → $0.27 (+3.8%) | **15** |
| MSFT | None in window — last ex-div Nov 19, 2026 ($0.98, payable Dec 10, 2026); next ex-div Feb 2027 | $0.98/qtr ($3.92/yr) | 0.80% | No new raise since Sep 15, 2026 board raise to $0.98 | **24** |
| TSLA | None — pays no dividend | $0 | 0% | None | n/a |

\* Yields computed on Wed Nov 25 closes (annualized forward rate for single names; TTM for the ETFs).

- **FACT — NVDA Dec 2 is the only declared, confirmed ex-div in the window.** Nasdaq dividends-calendar sweep (every date Nov 27–Dec 24) returned exactly one watchlist row: NVDA, ex Dec 2, $0.25, pay Dec 23, record Dec 2, announced Nov 17. Corroborated at the primary source — NVIDIA's Q3 FY2027 release: "NVIDIA will pay its next quarterly cash dividend of $0.25 per share on December 23, 2026, to all shareholders of record on December 2, 2026" (GlobeNewswire, Nov 17, 2026). Yahoo quoteSummary independently confirms divRate $1.00 / exDiv Dec 2.
- **FACT — SPY Dec 18 ex-div / Jan 29, 2027 pay is issuer-scheduled; amount undeclared.** State Street's published 2026 distribution calendar (via Dividend Vision, updated Nov 26, 2026): "Not yet declared," last paid Sep 18, $1.88883. Last three 2026 distributions: Mar 20 $1.797, Jun 18 $1.904, Sep 18 $1.88883 (total $5.58935 YTD). DividendMax expects declaration Dec 17, 2026.
- **FACT (date) / UNVERIFIED (amount, pay date) — QQQ Dec 21.** Ex-date is consensus across DripCalc, StockInvest, DivTrkr, TipRanks, DividendMax (est.), Wall Street Horizon. Pay date is now **five-way disputed**: Dec 28, 2026 (DripCalc, DividendMax forecast, dividend-wealth) vs ~Jan 3, 2027 (Dividend101 est.) vs Jan 4, 2027 vs Jan 7, 2027 (DivTrkr, which lists $0.75) vs **Jan 11, 2027 (new today — Wall Street Horizon / financialregulationcourses, claiming it is scheduled by Invesco per Invesco's distribution history)**. The Jan 11 candidate is the first to cite an issuer source, but it was not verified at invesco.com itself, so it stays UNVERIFIED. Amount candidates unchanged: $0.7941 (repeat of Dec 2025, DripCalc's "declared" label) vs $0.7514 (repeat of Sep, AlgovestIQ est.) vs $0.75. Do not cite any QQQ amount or pay date as fact.
- **FACT — AAPL and MSFT are out of window; both last went ex-div this month.** MSFT's Dec 10 payment lands inside the window but its ex-div does not — holders of record Nov 19 receive it; no action window remains. Yahoo forward rates re-pulled today are unchanged (AAPL $1.08, MSFT $3.92), ruling out any new raise announced since yesterday.
- **FACT — No increases, cuts, or specials announced among watchlist names this run.**
- **Dismissed conflicting claim (do not use):** a low-quality aggregator page (dopepics.io) claims NVDA "declared a dividend increase" on Nov 20, 2026, citing "$0.04 per share" — contradicted by the primary source (NVIDIA's Nov 17 release: $0.25 flat), the Nasdaq calendar ($0.25, announced Nov 17), and MarketBeat's announcement table ($0.25, 11/17/2026). The $0.04 figure is NVDA's pre-split-era quarterly rate. Treat as UNVERIFIED/false; no NVDA raise exists.
- **INFERENCE — Nasdaq calendar absence for SPY/QQQ is a coverage artifact, not a contradiction.** SPY is NYSE Arca. QQQ is Nasdaq-listed yet absent, most likely because its December distribution is not yet declared through Nasdaq's feed (declaration expected Dec 18) — consistent with DividendMax's Forecast status.
- **Gap note:** the news-search tool failed once today on the AAPL/MSFT/NVDA dividend-announcement sweep (tool failure, not a source failure; not retried per instruction). Coverage is preserved by two independent checks — the full Nasdaq calendar sweep found no new watchlist ex-div rows, and Yahoo forward dividend rates for all three payers are unchanged vs yesterday — so a new board action would have had to leave both signals untouched, which is unlikely but not impossible. Mark the news sweep itself UNVERIFIED for today.

**Desk verdict:** Quiet window; one actionable date. NVDA Dec 2 ($0.25, flat, primary-source confirmed) is the only certain ex-div in the next four weeks. Nothing here changes a margin-of-safety read on any watchlist name: all six yields are sub-1.1% and none of the three December dates involves a raise, cut, or special. **What would change it:** a State Street declaration for SPY (~Dec 17) or an Invesco declaration for QQQ (~Dec 18) with an amount materially above/below last quarter; an Invesco-published pay date settling the QQQ five-way dispute; any new AAPL/MSFT/NVDA board action; a TSLA dividend initiation (none indicated).

**Sources:** api.nasdaq.com/api/calendar/dividends (full sweep Nov 27–Dec 24, 2026, run today); Yahoo v10 quoteSummary (cookie+crumb handshake) + v8 chart (Nov 25 closes), Nov 26, 2026; NVIDIA Q3 FY27 release (GlobeNewswire, Nov 17, 2026); State Street 2026 distribution schedule via Dividend Vision (updated Nov 26, 2026); DividendMax (SPY/QQQ forecast rows, declaration Dec 17/18); DripCalc, StockInvest, DivTrkr, Dividend101, TipRanks, Wall Street Horizon, financialregulationcourses.com, AlgovestIQ (third-party estimates, UNVERIFIED); MarketBeat announcement table; ~/workspace/hedge-desk-research/dividend-count-standard.md. Yahoo v8 chart returned two empty responses on first attempt (QQQ, MSFT) and succeeded on retry after backoff — transient.

---

## 3. Overnight Premium desk (IV)

**Market status:** Thanksgiving — US markets CLOSED. All IVs below are Wed Nov 25 close marks, not live trading. **FACT.**

### Freshness guard — PASS
- File: `~/workspace/hedge-desk-research/nightly/2026-11-25-iv-inputs.json`
- `as_of`: **2026-11-25T14:54:29-07:00**; age at pull **23.5h** — **within the 26h guard, accepted**. **FACT.**
- ATM IV **null 6/6** in the file — expiry-day guard again (nearest expiry Nov 25 expired 16:00 ET before the 13:54 PT pull; Yahoo's post-expiry marks are solver residuals, failed closed per the no-invent rule). Seventh straight null run in this sequence (Nov 18/23/25). **FACT** (file `failures` array).

### Table 1 — Nightly file: 20-day realized vol + stale-jump screen (window Oct 28–Nov 24)

| Symbol | Realized 20d | Max single-day var share | Window-contingent? |
|---|---|---|---|
| SPY | 32.53% | 27.03% | No |
| QQQ | 49.09% | 25.30% | No |
| AAPL | 29.28% | 43.30% | **Yes** |
| MSFT | 39.33% | 37.10% | **Yes** |
| NVDA | 130.47% | 58.90% | **Yes** |
| TSLA | 74.82% | 32.40% | **Yes** |

Attribution carried from the Nov 21 desk correction: Nov 5 crash day drives SPY/QQQ/TSLA; AAPL/MSFT ride a Nov 4 up-day; NVDA rides Nov 20. **FACT** (desk record). Nov 5 ages out of the 20-day window Fri Nov 28; **first clean realized read lands Dec 1**. **FACT** (calendar arithmetic).

### Table 2 — LIVE Yahoo supplement pull, Thu Nov 26 ~13:26 PT (labeled live; quotes are Nov 25 close marks)

Method: v7 options chain, cookie+crumb handshake (curl-seeded jar, `fc.yahoo.com` → `/v1/test/getcrumb`), ATM = mean(call IV, put IV) at nearest overlapping strike; nearest **unexpired** expiry (Nov 27) + Dec 18 monthly for term structure. 0 failures. Sources: `https://query1.finance.yahoo.com/v7/finance/options/{SYM}` and `.../v8/finance/chart/{SYM}?interval=1d&range=5d`.

| Symbol | Spot (Nov 25 close) | ATM IV 1-DTE (Nov 27) | ATM IV 22-DTE (Dec 18) | Term shape |
|---|---|---|---|---|
| SPY | 716.70 | **23.35%** (call 24.18 / put 22.52) | **24.46%** | Mildly upward |
| QQQ | 633.93 | **36.62%** (35.76 / 37.48) | **36.31%** | Flat |
| AAPL | 355.58 | **23.77%** (24.39 / 23.15) | **26.20%** | Upward |
| MSFT | 489.93 | **35.07%** (35.49 / 34.66) | **38.18%** | Upward |
| NVDA | 149.30 | **72.78%** (73.73 / 71.83) | **73.33%** | Flat, very high |
| TSLA | 380.14 | **49.90%** (50.16 / 49.63) | **57.26%** | Upward |

*(Desk 3's day-move column omitted — see the synthesis correction at the top of this package; the corrected day moves are in the closes table.)* ATM bid/ask tight on all six straddles (e.g. SPY 1-DTE call 4.91/4.97, put 4.89/4.92) — quotes are tradeable Nov 25 marks, not degenerate prints. **FACT.** Note Nov 25 was a broad selloff and is **not yet inside** the Table 1 realized window (ends Nov 24) — tomorrow's realized print will absorb it. **INFERENCE.**

### IV vs realized verdicts (22-DTE IV vs 20-day realized)
- **SPY: IV 24.5% vs realized 32.5% — IV ~8pts BELOW realized.** Clean comparison (not window-contingent), but the realized leg still carries Nov 5 at a 27% share, so part of the gap is stale-jump inflation, not a live cheap-vol signal. **FACT + INFERENCE.**
- **QQQ: IV 36.3% vs realized 49.1% — IV ~13pts BELOW realized.** Clean comparison (25.3% share), same Nov 5 caveat. **FACT + INFERENCE.**
- **AAPL (26.2% vs 29.3%), MSFT (38.2% vs 39.3%), NVDA (73.3% vs 130.5%), TSLA (57.3% vs 74.8%): WINDOW-CONTINGENT — no clean IV-vs-realized verdict.** A single day drives >30% of each 20-day window; any premium-cheap/rich call on these four is invalid until the Dec 1 clean read. **FACT (screen) — verdict withheld by rule.**
- **IV rank: UNVERIFIED for all six** — no 1-year IV history available from free sources; no rank number is estimated or implied. Cross-sectional levels only: NVDA (~73%) and TSLA (~50–57%) run far above index IV (SPY ~23–24%); QQQ (~36%) elevated vs SPY. **FACT (levels) — not a rank claim.**

### Term structure & events
- No earnings hump anywhere: front IV is at or below back IV on every name; term structure is flat-to-upward (normal contango), with no front-month elevation. **FACT.**
- **No earnings inside the IV window: next_earnings null for all six symbols** in the nightly file (45-day Nasdaq sweep). NVDA reported Nov 17 (already past). Premium into a binary event is not a factor this window — nothing to avoid on earnings grounds. **FACT** (file; earnings calendar is the Earnings desk's to confirm — confirmed above, §1).
- 1-DTE Nov 27 expiry is a half-day session (early close Fri) — the 1-DTE prints are one-day, expiry-week prints; read them as the market's overnight/weekend gap price, not as a 30-day vol signal. **INFERENCE.**

### Parity sanity check (derivatives_options.md)
- Call vs put ATM IV gaps are small on every chain (≤1.7pts at 1-DTE, ≤3.6pts at 22-DTE) and ATM bid/ask spreads are tight — no put-call parity violation evident in the marks. Where a model and parity disagree, the math wins; nothing here disagrees. **FACT (observed marks) + INFERENCE (no arbitrage signal).**

### Desk 3 bottom line
1. **IV prints are back** after the expiry-day nulls: live 1-DTE ATM IV SPY 23.4%, QQQ 36.6%, NVDA 72.8%, TSLA 49.9% (Nov 25 close marks; markets closed today). **FACT.**
2. **SPY/QQQ IV sits well below trailing realized** (SPY −8pts, QQQ −13pts) on clean windows — but the realized leg is still Nov 5-inflated, so this is not a clean "vol is cheap" verdict. **INFERENCE.**
3. **Four of six names are WINDOW-CONTINGENT** (AAPL, MSFT, NVDA, TSLA) — no IV-vs-realized verdict on them until the Dec 1 clean read. **FACT.**
4. **No earnings inside the window; no event hump; IV rank UNVERIFIED.** Nothing in this desk's read supports paying up for premium into a binary event, and nothing supports a short-premium call on the contingent names. **INFERENCE.**
5. **What would change it:** Nov 28 roll (Nov 5 exits the window) + Dec 1 clean realized print; a fresh IV-history source would unlock IV rank.

---

## 4. Open Quant/AI Model Lab

**Coverage (FACT, as of ~13:30–14:00 PT today, Thu 26 Nov 2026 — Thanksgiving, US markets closed):** arXiv q-fin Thu 26 Nov announcement (10 new + 4 cross-list), read at source via the listing page as coverage control; the listing also caught 3 Wed-25 items the Nov-25 API range query missed (2611.32420/31860/31518 — all econ.GN, out of scope). arXiv API quirk: `http://export.arxiv.org` returned empty twice (transient, as on 2026-11-25); `https://export.arxiv.org` worked for id_list batches. SSRN leg: 2 searches surfaced 5 papers new to the ledger (verified 0 grep hits each) — the SSRN search leg keeps surfacing Oct/Nov papers earlier sweeps missed. All 12 candidates scored with the repo module (`hedge_desk.research_intelligence.assess_source`, never hand-scored). Ledger now ends at **#372**. GitHub leg skipped per the run brief's ban on GitHub operations — no repo/license verification this run. All findings below are abstract-level (source-reported, UNVERIFIED beyond the abstract) per the evidence standard; no full papers were read.

**Top of the run (tied, 57):**
- **#361 — "The Information Content of News Embeddings" (arXiv:2611.33458v1, 24 Nov).** FACT (abstract): event categories account for most of news embeddings' short-horizon predictive power, and simple forecasts from historical average returns after news in each event category outperform the embeddings; at longer horizons, firm information already in earlier coverage accounts for a substantial share. For Llama-2, embeddings from news >3 years old still predict returns, but its advantage over RoBERTa concentrates in firm identity + historical level and largely disappears by its pretraining cutoff; calibration shows pretraining memory (look-ahead bias) can account for the pattern. INFERENCE: directly earnings/news-drift lane — describing news more fully is not measuring news surprises, and persistent predictability from news text does not by itself establish slow incorporation. No code link in API record → WATCH, not TEST. *What would change it: code release → test whether the event-category historical-average forecast beats the desk's own news-drift read on watchlist names, and whether the pretraining-memory calibration changes how the desk treats LLM-embedding signals.*
- **#370 — Ratnaike, "The Shape of a Public-Data Volatility Surface: Term-Structure Carry, and the Limits of Measuring Skew" (SSRN 7670046, posted 31 Oct).** FACT (abstract): VIX3M−VIX slope has a long history, so its carry backtests — gating a short-vol position to contango beyond one vol point lifts Sharpe 1.73→2.94 full-sample and cuts hold-out drawdown ~73% by standing aside on stress days (COVID 2020, Feb 2018, Aug 2024); but the gain sits in those few episodes, so the pre-registered t-statistic on the daily difference is 1.31, under the committed 2 — term structure buys tail protection, no daily edge survives. Skew has no such history: a tradable 25-delta risk reversal needs a wings time series free data never built. INFERENCE: directly premium-desk — a free-data term-structure carry gate as a stress-day stand-aside rule, reported with an honest pre-registered null. No code → WATCH. *What would change it: full-paper read — verify the contango-gate rule and hold-out split; does the VIX3M−VIX gate transfer to the desk's own short-vol screens?*

**Other WATCH:**
- **#369 — Kargarzadeh et al., "Buy the Rumor, Sell the News: When is News Priced in?" (SSRN 7673798, posted 4 Nov), 54.** 4.57M news articles, ~3,000 US stocks 2023–2026; 1.68M stock-day events, 364,405 neutral-sentiment placebo events. FACT (abstract): price move concentrates before/at publication (cumulative move by publication-day close is 2.8× its value 20 days later); rumor-flagged events' directional return concentrates around the rumor, little incremental return at the linked non-rumor event; quantified fundamental news (earnings, dividends, guidance, analyst actions) keeps drifting in the news direction for weeks while soft story-driven news gives back its move; neutral news raises publication-day volatility. Produces a per-event-tag drift table usable as a prior in news-conditioned forecasting. Directly earnings + dividend desks. No code.
- **#362 — "Graph-Informed Deep Factor Model for Statistical Arbitrage" (arXiv:2611.34209v1), 51.** Latent-network factor model (FADE reconstruction + signed-edge graph attention); daily US equities 2015–2024, OOS Sharpe 1.78 under Avellaneda–Lee. Look-ahead audit required on the FADE network reconstruction window before any use. No code.
- **#368 — Barski/Wiśniewolski, "Implied volatility models without static arbitrage" (arXiv:2611.18937v1, submitted 13 Nov), 51 — LATE CATCH.** Submitted 13 Nov but missed by the Nov 13/14 runs (API submittedDate-range gap); surfaced by today's search leg. Explicit arbitrage-probability formulas for Gaussian factor IV models; deterministic no-static-arbitrage conditions; arbitrage-free Cont–Vuletić modification via Jacobi diffusions. Premium-desk IV-surface sanity lane. No code.
- **#363 — "Large deviations for integrated exponentials of Gaussian Volterra processes — application to variance options" (arXiv:2611.34567v1), 48.** Short-maturity asymptotics for OTM/ATM variance options in rough-vol models + IV expansions, validated numerically. Vol-surface lane. No code.
- **#372 — Feng/Michaely/Schmid, "Corporate Dividend Policies: A Systematic Review" (SSRN 7616082, posted 15 Oct; Palgrave Handbook, forthcoming), 47, band floor.** Replication through 2025 + seven non-US markets: dividends-as-commitment facts remain robust, while dividends' role as news about future earnings has weakened; 1,000+ articles classified. Dividend-desk framing for payout-announcement reads.
- **#364 — "How LLM Agents Reshape Financial Knowledge Graphs: A Survey" (arXiv:2611.33584v1), 45, band floor.** Survey; its unresolved questions — how an agent tells whether it has enough evidence for a financial decision, how a correction propagates to earlier conclusions — are the desk's own evidence-discipline questions. No new method, no code.

**ARCHIVE on band discipline (no ledger action beyond the row):** #365 monetary-policy VAR constants (39, Desk 7 adjacent only); #366 cash-subadditive risk measures (39, pure theory); #367 rank-size portfolio weights (42, portfolio lane); #371 Taleb "A Century of the Dividend Puzzle" (39, untested conjecture).

**Triage exclusions (no ledger rows):** 2611.34771 ETS climate credit risk, 2611.33603 retirement planning, 2611.34234 AI-automation fiscal pressure, 2611.34099 AI-replaces-juniors labor, 2611.32420 Grokipedia politics, 2611.31860 remote-work waste, 2611.31518 agentification value-added, 2611.34696 merchant underwriting ChainIT, 2611.34068 auction-bidding reasoning models, 2611.33593 Uganda microgrid, 2611.33050 chatbot response-time HCI, 2611.32139 healthcare failure demand, 2611.31613 synthetic-respondent decision models — all no desk lane.

**Movement:** #343 (Valeyre MaxVar) **v2→v3** (updated 2026-11-25) — abstract reads the same method/figures; stays WATCH. #334 journal_ref now present (IREF 2026, 106078) — still ARCHIVE. Re-checks via arXiv API id_list: #4 (v1), #9 (v2), #13 (v1), #14 (v3), #15 (v1), #20 (v2), #21 (v3), #25 (v4), #30 (v3), #31 (v3), #257 (v2), #255 (v2), #312 (v1), #331–#333/#335–#337 (all v1), #339–#342/#344–#351 (all v1), #352–#357 (all v1) — no other movement.

**Gaps / failures:** None blocking. http://export.arxiv.org empty twice — recovered via https (transient, classified, alternate route worked). Housekeeping: ledger numbering has a pre-existing gap — row #246 is absent (sequence jumps 245→247); no rows lost this run.

**Files:** ledger at `~/workspace/hedge-desk-research/quant-lab-ledger.md` (rows #361–#372 + 2026-11-26 jidoka entry, verified on disk).

---

## 5. Weather / War / Logistics Futures Event desk

**Thu 2026-11-26 (Thanksgiving Day — US equities, Treasury cash closed; CME futures on shortened hours, no Thursday settlements)**

### Bottom line
Material day. The two EIA weeklies both landed Wed Nov 25 (petroleum on its normal slot; gas moved a day early for the holiday), and the Middle East supplied the session's real catalyst: a claimed Houthi strike on Saudi Arabia's largest refinery plus claimed Iranian mine strikes on tankers in the Strait of Hormuz drove Jan Brent +3.5% on Wed. The Section 301 tariff determinations (Nov 25) are the watchlist-relevant overhang — but they are proposals only, with no tariff in effect. No new USDA report today; next WASDE is Dec 10.

### 5.1 EIA — both weeklies released Wed Nov 25, on schedule
**[FACT]** Weekly Petroleum Status Report, week ending Nov 20, released Wed Nov 25, 10:30 ET — its normal slot, NOT shifted for Thanksgiving (EIA petroleum data page lists release date Nov 25, 2026; Econoday confirms release 11/25/2026 10:30 AM for wk 11/20). Weekly Natural Gas Storage Report was moved a day early to Wed Nov 25, 12:00 ET for Thanksgiving (EIA schedule; next gas report Thu Dec 3, 10:30 ET). No federal-data blackout: both reports published normally.
- Commercial crude **418.9M bbl, +1.11M bbl w/w** — vs a 5-yr-average draw of 2.19M for the same week, i.e. +3.30M vs seasonal norm; level sits just below the 5-yr range for the week (419.1–449.7M). Days of supply 24.2. **[FACT — EIA via Arc Research]**
- Cushing **25.6M bbl, −0.53M bbl** (in 5-yr range 21.8–28.5M). **[FACT]**
- Gasoline **217.7M bbl, +1.73M bbl** (in range); distillate **105.6M bbl, +0.72M bbl** — **below** its 5-yr range (110.8–123.9M), 27.0 days. Jet fuel 43.2M bbl, −0.94M. **[FACT]**
- SPR **273.5M bbl, −2.90M bbl w/w**, far below its 5-yr range (351.6–602.6M). **[FACT]** Combined commercial + SPR crude therefore fell ~1.79M bbl on the week — the headline commercial "build" was more than offset by the reserve draw. **[INFERENCE — arithmetic on the two EIA prints]**
- Refinery utilization **97.5%, +1.8 pts** — above the 5-yr range top (95.2%). Crude inputs 17,346 kb/d (+428). US field production 14,065 kb/d (+33). Total product supplied 21,239 kb/d (+863). Crude imports 6,250 kb/d (+674); crude exports 3,269 kb/d (−1,219). **[FACT — EIA via Arc Research]**
- API preview (Tue Nov 24, industry estimate, not official): crude +0.126M bbl, gasoline −0.047M, distillate +1.647M, Cushing −0.666M, SPR −2.9M — directionally consistent with EIA on crude/SPR/Cushing; EIA gasoline/distillate builds were larger than API implied. **[FACT — API via Bloomberg/press reports; API is a voluntary industry survey, EIA is the official print]**
- Next petroleum report: Wed Dec 2, 10:30 ET. **[FACT]**

**[FACT]** Natural gas storage, week ending Nov 20, released Wed Nov 25, 12:00 ET: working gas **3,858 Bcf, −24 Bcf (first withdrawal of the season)**; **+2.1% (+80 Bcf) vs the 5-yr average (3,778 Bcf)** and **−2.0% (−79 Bcf) vs year-ago (3,937 Bcf)**. East drove the draw (−19 of −24 Bcf); South Central injected +8 Bcf. The 24 Bcf draw was exactly in line with the 5-yr average for the week and larger than the 17 Bcf WSJ analyst-survey estimate. **[FACT — EIA Weekly Natural Gas Storage Report, corroborated by WSJ/Natural Gas Intelligence]**
- Dec 2026 NYMEX nat-gas contract expired Wed at **$3.269/MMBtu (−1.6%)**. **[FACT — WSJ]**

### 5.2 Middle East — Ras Tanura + Hormuz mine claims (the day's catalyst)
**[FACT — as reported]** Yemen's Houthis said Wed Nov 25 they attacked Saudi Arabia's Ras Tanura refinery (550,000 b/d, ~16% of Saudi refining capacity, alongside one of the world's largest crude export terminals) and Riyadh's financial district; Houthi spokesman Yahya Saree said the refinery attack caused fires. NASA and Planet Labs satellite imagery reviewed by Reuters showed thick black smoke over the installation; a source with knowledge confirmed an attack on the refinery to Reuters. The Saudi-led coalition said air defences intercepted and destroyed four drones over Ras Tanura Wed morning (fragments fell, no injuries in initial assessment) but did **not** say the refinery had been struck. Aramco and the Saudi government did not immediately respond to requests for comment.
- **[UNVERIFIED]** Extent of damage, any reduction in refinery throughput, and any interruption to the adjacent crude-export terminal. A shipping source told CNN Thu that loadings at the terminal were suspended after the attack, resumption unclear — single-source, unconfirmed.
- **[FACT]** Thu Nov 26 (after the Wed close): a projectile struck an oil refinery in southwestern Jazan, killing one Nepalese worker and injuring several, sparking a fire and temporarily suspending some operations there — Saudi Ministry of Energy via CNN. The coalition also said it downed a Houthi drone near Jeddah Islamic Port, no civilian injuries.
- **[FACT — as claimed, not independently confirmed]** Iran's Revolutionary Guards said Thu that two tankers exploded and caught fire after hitting sea mines north of Oman's Khasab port while crossing the Strait of Hormuz through an unauthorised route; one was described as a supertanker carrying >2M bbl of crude. Iranian state media (Fars) had reported Wed that a tanker hit a mine in a "restricted zone" in the strait. UKMTO reported an explosion caused by an unknown projectile near a tanker ~50 nm west of Dubai on Thu. Reuters notes maritime security agencies frequently report fewer incidents than the Guards claim and the accounts do not always align — treat tanker count and cause as **claimed**, not verified. **[INFERENCE]** If Hormuz transits are in fact being mined/restricted, it threatens the recent recovery in Gulf crude exports (Reuters: Persian Gulf crude exports rose last week but remain on a declining trend; Kpler via press: Hormuz oil flows ~10M b/d by mid-Nov vs 13.4M at the start of the month).
- Context: this is an escalation of an ongoing campaign, not a first incident — Houthis previously claimed Ras Tanura attacks Oct 27 and Oct 30, and a Nov 9 attack set fire to the East-West pipeline. **[FACT — Reuters/ISW]**
- **[FACT]** Separately, Ukraine said Wed it struck a major Russian air base, damaging five planes. No direct energy-market read established; one line only.

### 5.3 Section 301 — determinations on 14 economies (Nov 25)
**[FACT — USTR, primary source]** USTR Jamieson Greer determined Nov 25 under Section 301 that acts/policies/practices creating structural excess capacity in manufacturing are unreasonable and burden/restrict US commerce for 14 economies: **China, EU, Singapore, Switzerland, Indonesia, Malaysia, Cambodia, Thailand, Korea, Vietnam, Taiwan, Bangladesh, Japan, India**. No determinations yet for Mexico or Norway. Proposed additional ad valorem tariffs: EU/Japan/Korea/Switzerland/Taiwan up to 15%; Bangladesh/Cambodia/Indonesia/Malaysia/Thailand up to 18%; China up to 20% (up to 10% for Annex A goods; Annex B exempt; alternative up to 40% if engagement is found inadequate); Singapore up to 20%; India up to 25%; Vietnam up to 35% (lower if trade agreements are reached). Rates are generally net of existing duties/MFN — not automatically additive on top.
- **[FACT]** These are **proposals only — no new tariff is in effect, and no effective date has been stated**. Written comments / hearing requests due Jan 5, 2027; public hearings begin Jan 25, 2027; final action not expected until after the hearings. Rates, scope and exemptions may change.
- **[INFERENCE]** Watchlist relevance is real but not yet quantifiable: Taiwan/Korea/Japan (15%), Vietnam (up to 35%), Malaysia/Thailand (up to 18%) and China (up to 20%) cover the core electronics/semiconductor supply chain for AAPL, MSFT, NVDA and TSLA. Until a final action with product coverage exists, any earnings or margin impact is **[SPECULATION]** — do not model a cost hit from the proposed rates. What matters now is the Jan 5 / Jan 25 calendar and any company comment on exposure.

### 5.4 Futures-curve read — Wed Nov 25 settlements (last full session)
| Contract | Wed Nov 25 settle | Day change | Prior (Tue) |
|---|---|---|---|
| Brent Jan'27 (ICE) | **$94.61/bbl** | **+3.51%** | $91.40 |
| WTI Jan'27 (NYMEX) | **$83.68/bbl** | **+1.99%** | $82.05 |
| Brent–WTI spread | **$10.93/bbl** | — | — |
| Nat gas Jan'27 (NYMEX) | **$3.658/MMBtu** | −0.14% | — |
| RBOB Dec'26 | $2.4423/gal | −0.49% | — |
| Heating oil Dec'26 | $3.7025/gal | −0.01% | — |
| Gold Dec'26 (COMEX) | **$3,535.80/oz** | −0.73% | — |
| Copper Dec'26 (COMEX) | $5.3365/lb | −0.61% | — |

**[FACT — settlements per Goodman-Macro/Edge Consultancy price-feed tables; Brent/WTI corroborated across both]** Brent had settled $92.57 on Fri Nov 20, so Wed's $94.61 is +2.2% on the week despite the Tue dip to $91.40. Oil rallied Wed on the Ras Tanura/Hormuz headlines against a backdrop Reuters described as expectations of a coming global surplus — i.e. the market priced a higher geopolitical risk premium into the prompt contract, not a tighter physical balance (EIA showed a commercial build vs seasonal norm).
- **[FACT]** Gold spot (XAU/USD, Finnhub daily candle Nov 25): open $3,559.65, low **$3,426.81**, close **$3,589.44** — fell below $3,500 intraday (weakest since Aug 2025) after hot core PCE (3.3% vs 3.2% expected) and Q3 GDP revised to 4.3%, then recovered to close near $3,583–3,589. The Dec COMEX settle ($3,535.80) and the spot close differ by contract/timing; do not mix them. *(Synthesis note: yesterday's package carried a ~$3,469–$3,486 intraday snapshot; today's Finnhub daily candle is the fuller Nov 25 read — low $3,426.81, close $3,589.44.)*
- **[INFERENCE]** The curve read is: prompt crude up on war-risk premium; prompt gas flat despite the first storage draw (ample storage, +2.1% vs 5-yr avg, offsets it); metals/gold down on the hot inflation print. Full term-structure shape (contango/backwardation beyond the Jan contract) is **[UNVERIFIED]** — only front-month settlements were verified this run; no deferred-month prices were sourced, and none are asserted.
- **[FACT]** Thu Nov 26: **no CME settlements** (Thanksgiving). Energy/metals futures halt 2:30 PM ET, equity-index/rate futures halt 1:00 PM ET, reopen 6:00 PM ET for Friday's trade date; grains closed all day, reopen Fri 9:30 AM ET. Fri Nov 27 early close: equities/rates 1:15 PM ET, energy/metals 2:45 PM ET, grains 1:05 PM ET. Brent (ICE London) trades Thu — Reuters early-Asia Thu print ~$94.71 (+0.1% at 0137 GMT); later Thu intraday prints near $96.48 were reported but are intraday, not settlements. Treat all Thu moves as thin-holiday tape. **[FACT — CME holiday schedule; Reuters]**

### 5.5 USDA / ags — nothing new today
**[FACT]** November WASDE (WASDE-677) was released Tue Nov 10: 2026/27 US corn ending stocks cut 91M bu to 1,758M on a smaller crop. Next WASDE: **Thu Dec 10, 2026, 12:00 ET** (USDA calendar). No USDA release scheduled today; weekly Export Sales next due in the normal Thu slot next week. Grain futures did not trade Thu (Thanksgiving closure). No fresh ag catalyst triaged today.

### 5.6 What to watch (calendar)
- **Sun Nov 29, 13:00 GMT: OPEC+ ministerial (4 meetings, incl. 42nd OPEC/non-OPEC)** — decides 2027 output policy / capacity-based quotas. **[FACT — scheduled]** Reuters sources Nov 26: likely to **roll over current output targets for at least Q1 2027** amid capacity-assessment disputes and Iran-war export disruption; no decision reached yet, talks continue; Novak said the capacity review completes by year-end. Rapidan also expects no change Sun. Rystad sees a ~5M b/d global surplus next year (~5% of demand) even with only partial Gulf recovery; ~2M b/d of 2022 cuts expire at year-end; UAE left OPEC in May and sets its own output. **[INFERENCE]** A rollover would leave the surplus narrative intact and cap any war-premium rally once headlines fade; a failure to agree (no framework past Dec 31) is the tail risk. Treat the rollover as reported-sources expectation, not a decision.
- **Wed Dec 2, 10:30 ET: EIA petroleum; Thu Dec 3, 10:30 ET: EIA nat gas** (week ending Nov 27). **[FACT]**
- **Thu Dec 10, 12:00 ET: WASDE.** **[FACT]**
- **Mon Nov 30: planned reopening of the Nogales, AZ cattle port** (per Nov WASDE coverage) — watch for confirmation; no price read today. **[FACT — as scheduled]**
- **Jan 5 / Jan 25, 2027: Section 301 comments / hearings.** **[FACT]**

### What would change this read
Confirmation (or refutation) of Ras Tanura refinery/terminal damage and of Hormuz mine incidents from independent sources; an OPEC+ decision Sun that breaks from the reported rollover; a Dec 2 EIA print showing distillate/commercial crude rebuilding vs seasonal norms; a Section 301 final action with product-level coverage.

**Sources:** EIA petroleum data page (release date Nov 25, 2026): https://www.eia.gov/petroleum/data.php ; EIA Weekly Petroleum Status Report detail (Arc Research, EIA-sourced): https://www.getarcresearch.com/commodities/crude-oil/inventories ; Econoday EIA Petroleum Status Report (released 11/25/2026 10:30 AM, wk 11/20): https://global-premium.econoday.com/byevent?fid=672430&year=2026&lid=0 ; EIA Weekly Natural Gas Storage Report (3,858 Bcf, −24 Bcf): https://ir.eia.gov/secure/ngs/ngs.html ; EIA natural-gas schedule (Wed Nov 25, 12:00 ET, Thanksgiving shift): https://www.eia.gov/naturalgas/data.php ; USTR Section 301 determinations (Nov 25, 2026): https://ustr.gov/about/policy-offices/press-office/press-releases/2026/november/ustr-makes-determinations-and-proposes-actions-14-section-301-investigations-relating-structural ; Section 301 proposed rates / timeline (Lexology): https://www.lexology.com/library/detail.aspx?g=c7f2941e-21be-4864-84f2-51e960f28910 ; Reuters — oil rises on mine strikes / Ras Tanura (Nov 26): https://www.reuters.com/business/energy/oil-rises-supply-concerns-iran-claims-mine-strikes-ships-2026-11-26/ ; Reuters — IRGC: two tankers hit mines near Khasab (Nov 26): https://www.reuters.com/world/middle-east/irans-revolutionary-guards-say-two-oil-tankers-hit-sea-mines-near-omans-khasab-2026-11-26/ ; Reuters via Hydrocarbon Processing — Houthis say they attacked Ras Tanura: https://hydrocarbonprocessing.com/news/2026/11/yemens-houthis-say-they-attacked-saudi-arabias-ras-tanura-refinery/ ; CNN — Houthis strike Saudi oil infrastructure; Jazan refinery hit Thu (Nov 26): https://www.cnn.com/2026/11/26/middleeast/houthi-saudi-oil-refinery-strike-satellite-imagery-intl ; ISW Iran Update, Nov 25, 2026: https://understandingwar.org/research/middle-east/iran-update-november-25-2026/ ; Wed Nov 25 settlements (Brent $94.61 / WTI $83.68 / gold / gas): https://www.goodman-macro.com/en/articles/20261126-oil/ and https://edgeconsultancykw.com/commodities-wrap-25-november-2026/ ; OPEC+ likely rollover (Reuters via Kitco, Nov 26): https://www.kitco.com/news/off-the-wire/2026-11-26/opec-likely-roll-over-oil-output-targets-q1-capacity-disputes-persist ; WSJ — OPEC+ tough choices / surplus vs Hormuz (Nov 26): https://www.wsj.com/business/energy-oil/opec-allies-face-tough-choices-as-surplus-builds-hormuz-risks-persist-769f8d98 ; CME holiday/trading hours (Thanksgiving): https://www.cmegroup.com/trading-hours.html ; USDA WASDE calendar / Nov 10 release: http://www.usda.gov/oce/commodity/wasde/ ; API estimates (Nov 24): https://piqmarkets.com/story/api-estimates-us-crude-stocks-rose-126-000-barrels-last-week

**Source failures:** None. All primary sources (EIA, USTR, USDA calendar, CME schedule, Reuters) returned usable data this run; no retry was needed. One scope limit, stated above: deferred-month futures prices for a full curve shape were not verified — marked UNVERIFIED rather than asserted.

---

## 6. Box/Parity Observer

**Bottom line: parity holding; one new daily cross-check, nothing broken. US markets closed today (Thanksgiving) — no new trading data; all reads below carry Wednesday Nov 25's close.**

**New since yesterday:**
- **FACT — Saxo Options Brief, Nov 26 — daily VIX parity check holds.** A parity check on December VIX options at Wednesday's close put the contract near **25.08** (up from 24.17 a session earlier), vs the December future at **24.55** at 05:00 CET and January at ~23.85 — the futures curve stays in backwardation, no parity break flagged. This is the desk's standing daily cross-check; it reads clean for a fourth consecutive session (Nov 23: Dec ~27.53 vs VIX 35.89; Nov 24: ~23.91; Nov 25 brief carried Tuesday's close with no break flagged). Note: this is VIX-futures parity, not SPX put-call parity. Source: https://www.home.saxo/en-sg/content/articles/options/index-recovers-near-term-fear-stays---options-brief---26-november-2026-26112026 (published Nov 26, 04:30 CET; carries Wed Nov 25 US close: S&P 500 7,182.78, −0.25%; VIX 28.29).

**No change / nothing new:**
- **Cboe notices / SPXO:** no new notice surfaced since yesterday. The SPXO correction (notice id 62439, final-trading-day cutoff 5:00 p.m. ET) remains the latest item; only listed expiries remain Nov 18 (settled cleanly) and Dec 16, 2026. No new SPXO expirations added. Next watch item remains the Dec 16 expiry (final trading day Tue Dec 15).
- **Cboe binary options (SR-CBOE-2026-087):** no new development since the Nov 25 package — rules published Nov 24, listings permitted but no contracts traded yet, so still no live parity/box data for this product. Not re-reported as new.
- **Box-spread financing:** no new dated measurement since the Nov 23 nyasekai single-snapshot test (fill-realistic lending 2.57–3.28% on the widest box vs Treasuries 4.33–4.62%; already logged Nov 25). Last standing prints unchanged: Nov 12 Solvinc scan (short end 3.86%, 435-day 5.16% vs ~5.39% IBKR first-tier margin) and ZeroMargin ZMR 5.22% as of Nov 16. No dislocation signal.
- **S&P DJI methodology:** no new methodology document since yesterday. The growth/value style-framework overhaul (momentum out of growth; free-cash-flow/intangibles into value; effective Dec 21, pro-forma files Dec 4) was announced Oct 23 and is already known. No new S&P 500 membership/methodology release in the last 24h.
- **Published parity-violation analysis:** none new found in today's sweep. The Shin (2026) arXiv papers on the SPX/RUT carry gap remain the latest in the record.

**Watch items carried forward:** SPXO Dec 16 expiry (final trading day Tue Dec 15) — second cross-symbol SPXO/SPX/SPXW parity observation on a VIX settlement date. S&P DJI style reconstitution: pro-forma files Dec 4, effective Dec 21. Box-rate re-measurement: next dated print after Nov 12/Nov 16; a print materially above ~5.4% or below ~4% would reopen the dislocation question. Cboe binary options: first listings, if any, would be the first parity/box observation for that product class.

**What would change it:** a published parity-violation analysis, a Cboe notice adding SPXO expirations or changing settlement/allocation rules, a box-rate print materially off the ~5% financing band, or a Saxo parity check flagging a break.

**Desk status:** COMPLETE — light-touch sweep done; no material parity break or new methodology item today.

---

## 7. Bonds & Rates desk (Desk 7)

**Status: Desk ran. Module `rates_desk.rates_environment()` executed this session, REAL_FRED_RATES mode. All rates levels independently verified against FRED. Tally UNCHANGED: 5 HIKE / 0 CUT / 5 NEUTRAL. Dec 9 25bp hike call HOLDS. Thanksgiving Day — US markets closed, no federal data releases today; Nov 25 closes are the latest data.**

### 7.0 Sentry W48 verification (rates_desk.py CONDITIONAL KEEP — module numbers NOT taken on trust)

Independent FRED pulls this session (`fred_observations.py`, `--limit=N` form):

| Finding | Module says | Independent check | Verdict |
|---|---|---|---|
| F1 — fed-funds change unsigned, no baseline | `fed_funds_change_over_window: 0.00` | DFF Nov 24 / 23 / 22: **3.88% every day**; EFFR identical 3.88 | **VERIFIED as 0.00** — the number is right; the process finding (no baseline in output) stands |
| F2 — DFF is the wrong series | DFF 3.88 | FRED EFFR 3.88, Nov 24 — identical level | No material discrepancy in the level; finding noted, not load-bearing |
| F3 — curve-slope unit mix | `spread_10y_2y_points: 28.00`, `curve_slope: 0.035000` | Independent: 4.91 − 4.63 = **+28bp** | **CONFIRMED LIVE — do not cite `curve_slope`.** 0.035 equals neither 0.28 (pp) nor 28 (bp). The 28bp spread figure agrees with the independent calc; the slope field does not |
| F4 — as_of defaults to wall clock | `as_of: 2026-11-26` | Latest FRED obs in the pull are **Nov 24** (no Nov 25 obs posted yet in FRED) | as_of is the run date, not the data date. All figures below are data-as-of Nov 24 (indicators as noted) |
| F5 — DGS10 candidate dropped by key typo | DGS10 4.91 | Independent FRED DGS10 Nov 24: **4.91** | Level verified regardless; typo itself not confirmed from this session's output |

### 7.1 Rates table (FACT — FRED via module, independently verified; data as-of Nov 24, Wed close)

| Series | Read | Prior session(s) | Change |
|---|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 3.88% Nov 21–24 | 0.00 — flat 60+ days |
| Treasury 2Y (DGS2) | **4.63%** | 4.63% Nov 20, 23, 24 | Flat 3 sessions; −13bp since Nov 19 |
| Treasury 10Y (DGS10) | **4.91%** | 4.92% Nov 20, 23; 5.04% Nov 19 | −1bp vs Nov 23; −13bp since Nov 19 |
| **2s10s slope (independent calc)** | **+28bp** | +29bp Nov 20 & 23; +28bp Nov 19 | **Essentially flat, −1bp d/d; upward-sloping, no inversion** |
| SOFR | **3.94%** | 3.92% Nov 23, 20 | +2bp d/d |
| EFFR / OBFR | **3.88% / 3.88%** | Flat | — |
| **SOFR–EFFR funding spread** | **+6bp** | +6bp Nov 25; +4bp Nov 23 | Narrow; no funding stress (INFERENCE) |

Module shape call "UPWARD_SLOPING" agrees with the independent +28bp. Target range 3.75–4.00% (FACT, Oct 28 FOMC hold, federalreserve.gov).

### 7.2 Core-indicator table — today's read + broker POV

| Indicator | Trigger rule | Today's read (source, as-of) | Call | Broker POV — discount rate / margin of safety |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA) | HIKE if y/y > 2.5% or m/m > +0.25% | **Oct y/y +3.26% (cons 3.2%, Sep 3.1%), m/m +0.29%**; index 131.312 vs Sep 130.929 vs Oct 2025 127.165 — computed from FRED levels this session, matches the Nov 25 release (+3.3% / +0.3% rounded). No new print today | **HIKE** | Anchor the discount rate to the higher regime. The decision variable rose and consensus missed low — no re-anchor down. The §7.4 tripwire (m/m ≤ +0.15% with a downward Sep revision) did NOT fire on either leg. |
| Breakevens (T5YIE / T10YIE, FRED) | HIKE if > 2.75%; CUT if < 1.75% | **2.13% / 2.12%, Nov 25** (was 2.11% / 2.12% Nov 24; 2.31% / 2.24% Nov 12) | NEUTRAL | Anchored and ~20bp below Nov 12: no credibility crisis, room for 25bp, not a forced 50bp. Tripwire remains a break above 2.75%. |
| Michigan expectations (U-M, manual) | HIKE if yr-ahead > 3.5% | **FINAL Nov yr-ahead 3.7%** (prelim 4.3%, Oct 4.7%), rel. Nov 20; 5–10yr 3.3% (Oct 3.5%). FRED MICH cross-check: Oct 4.7 — lagging as usual, confirms the lag, not the level. No new print today | **HIKE** | Still fires, but barely: 20bp above the tripwire. The household-vs-market gap narrowed hard (3.7% vs 2.13% breakeven) — the credibility-gap argument is weakening even as the trigger still fires. Do not average with breakevens. |
| Payrolls, 3-mo avg (PAYEMS, BLS/FRED) | HIKE if > +150k; CUT if < +50k | **+137k** (Oct +165k, Sep +60k, Aug +186k; levels Oct 159,293k). No new print since the Oct report; Nov payrolls due Dec 4 | NEUTRAL | Rule as written: NEUTRAL. One +165k print does not override the average. Note the margin: 13k below the HIKE tripwire — a strong Nov print flips this line. |
| Initial claims, 4-wk avg (ICSA, DOL/FRED) | CUT if > 300k; NEUTRAL < 250k | **196k** (w/e Nov 21: 189k; Nov 14: 202k; Nov 7: 202k; Oct 31: 191k). Next release Fri Nov 27 (w/e Nov 22) | NEUTRAL | No action. Claims are drifting DOWN, away from the 300k tripwire. Check every Thursday — it turns first. |
| Job openings (JTSJOL, BLS/FRED) | HIKE if 3-mo change positive | **7,523k, Sep 2026** (Jul 7,335k → Sep +188k). No new print (Oct JOLTS expected ~Dec 2) | HIKE | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA/FRED) | HIKE if > 2.5% ann.; CUT if < 1.0% | **Q3 second estimate +4.3% annualized** (advance 3.4%, cons 3.5%), BEA Nov 25. FRED levels confirm: 24,665.201 vs 24,408.011 = +4.28% ann. No new print today | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Note the split: growth revised UP while the deflator revised DOWN (1.8% vs 2.3% exp) — real strength, less price pressure — which argues for 25bp, not 50bp. |
| Housing starts (HOUST, Census/FRED) | CUT if −5% over 3 months | **Oct 1,309k** (Sep revised 1,221k → 1,191k); Jul→Oct **−4.4%**; Oct +9.9% m/m. No new print today | NEUTRAL | Confirms the Nov 18 flip: the −5% CUT tripwire no longer fires. Single-month rebound, 3-mo trend still negative — NEUTRAL, not HIKE. The strongest hold argument in the set has faded. |
| HY OAS (BAMLH0A0HYM2, ICE BofA/FRED) | CUT if > 5.00%; NEUTRAL < 4.00% | **3.72%, Nov 24** (3.63% Nov 23; 3.20% Nov 12) | NEUTRAL | No stress at the level, but **+52bp widening since Nov 12** is the largest move in the set — watch. A break above 5.00% is the tripwire; at the current pace that is not imminent (INFERENCE). |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening / hawkish language | Oct 28: held 3.75–4.00%, **10–2, Cook + Hammack dissenting for +25bp**; statement: "Inflation remains elevated." Nov 18 minutes already digested Nov 23. No new guidance verified this session (Thanksgiving; no speakers) | **HIKE** | Weight the vote above any single print: two dissents for an immediate hike is the Committee stating its lean. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL — unchanged from Nov 23 and Nov 25.**

### 7.3 Market pricing vs the indicator read

- **Kalshi, direct API pull Nov 26 ~13:35 PT (Dec-2026 meeting, `KXFEDDECISION-26DEC`)**: 25bp hike **$0.92** (bid/ask 0.92/0.93, 24h vol ~168k, OI ~3.07M); more than 25bp **$0.03** (0.02/0.03, vol ~121k); hold **$0.05** (0.04/0.05, vol ~215k); cuts $0.01 each. Total hike $0.95. **Essentially unchanged from Nov 25 ($0.93 / $0.03 / $0.06)** — the last ticked −1c, bid/ask identical. The >25bp tail stays collapsed at $0.03 (was $0.12 on Nov 13).
- **CME FedWatch (secondhand — CME's own tool not directly readable; converging reads)**: FrenzyCap /ZQ replication, **live Nov 26, 12:59 PM ET: 96% for 25bp, 4% hold, 0% for >25bp**, expected +24bp, EFFR after 4.120%. Other secondhand reads today span 94.4%–98.6% (FXStreet 98.1%; TheStreet ~97–98%; CoinCentral 94.4%). Level: ~96%, unchanged from Nov 25.
- **Agreement**: markets and indicators agree on direction (25bp hike) and size (tail ~$0.03 / 0%). One named gap: futures-implied 25bp (~96–98.6%) sits ~4–6pp above Kalshi's $0.92–0.93 (predictionmarketspicks cross-venue table, Nov 26 12:00 PM ET: Kalshi 92.5% vs futures 98.6%, 6.1pp spread) — futures price the hike slightly harder than the prediction market; both agree it happens.
- **Jan 2027 is the live question, and it moved**: Kalshi Jan H25 **$0.57** (bid/ask 0.56/0.57) vs hold $0.43, up from $0.54/$0.46 yesterday; >25bp $0.02. Secondhand Jan read (TheStreet): ~58% cumulative 50bp by Jan — consistent with the Kalshi lean. The Dec decision is priced; the January follow-through is not settled.
- **NVDA governance note (rates relevance only)**: the Nov 23 reinstatement rally (+32% to ~$166) loosened financial conditions into the meeting; it changes no Desk 7 trigger. The counter-signal is HY OAS widening +52bp since Nov 12 — credit, not equities, is where any tightening-by-markets would show, and it is not showing stress yet (INFERENCE).

### 7.4 Verdict — thesis / evidence / what would change it

- **Thesis**: 25bp hike on Dec 9. **Holds.**
- **Evidence**: Core PCE re-anchored hotter (y/y 3.26% vs 3.2% cons, up from 3.1%; m/m +0.29% still above the +0.25% trigger); Q3 GDP revised up to +4.3%; the Oct 28 vote already leans hike (10–2 with two hawkish dissents); markets price it at ~96% / $0.92. The two dovish-leaning moves — Michigan final expectations falling to 3.7% and breakevens to ~2.12% — narrow the case for 50bp, they do not touch the case for 25bp. Housing's CUT signal is gone. Nothing printed today (Thanksgiving) to move any line.
- **What would change it**: (a) November core PCE (Dec 23) is after the decision — cannot change December; (b) initial claims 4-wk avg above 300k — currently 196k and falling; next read Fri Nov 27; (c) November payrolls (Dec 4) — the decisive pre-meeting print: a strong month flips the 3-mo avg above +150k (HIKE, strengthening the call), a weak one leaves it NEUTRAL; (d) Michigan Dec 4 prelim below 3.5% flips one HIKE line to NEUTRAL but would not alone overturn a 5–0 tally with markets at ~96%; (e) Oct JOLTS (~Dec 2) — a negative 3-mo change flips the JOLTS line; (f) a named speaker arguing for a hold, or the Dec 9 statement softening — none verified this session.

### 7.5 Graham lens (arithmetic from verified yields)

10Y **4.91%** (Nov 24) — unchanged from Nov 25, vs 4.98% (Nov 10) vs 4.86% (Nov 6). At assumed perpetual growth g = 3.00%, Gordon multiple 1 ÷ (r − g): **52.36x today** (1 ÷ 0.0191), unchanged from yesterday — **no re-anchor**. Duration ≈ 8 puts the 0bp move at ~0% on a 10-year position. The margin of safety is unchanged from yesterday on the bond side — but the bond side still pays ~4.9% on a contractual claim, so equity risk must be compensated from price; a wider required discount, not a chase for yield. Earnings-yield vs bond-yield spread: UNVERIFIED (no S&P earnings-yield figure from a primary source this session; no spread asserted).

**Sources:** FRED (fred-public CSV via `rates_desk.rates_environment()`, module run this session; independently re-pulled via `fred_observations.py`): DFF, DGS2, DGS10, SOFR, EFFR, OBFR, PCEPILFE, T5YIE, T10YIE, MICH, PAYEMS, ICSA, JTSJOL, GDPC1, HOUST, BAMLH0A0HYM2 — data as-of Nov 24 (daily series); monthly/quarterly series as noted. BEA, Personal Income and Outlays, October 2026 (released Nov 25, 8:30 ET): https://bea.gov/news/2026/personal-income-and-outlays-october-2026 ; BEA, GDP Second Estimate Q3 2026 (released Nov 25): https://bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-3rd-quarter-2026 . U-M Surveys of Consumers, final November results (released Nov 20): yr-ahead 3.7%, 5–10yr 3.3% — carried from the Nov 24 verification; FRED MICH still shows Oct 4.7 (lagging). Kalshi trade API v2, `KXFEDDECISION-26DEC` and `KXFEDDECISION-27JAN` event tickers, direct pull Nov 26 ~13:35 PT. CME FedWatch: secondhand converging reads — FrenzyCap /ZQ replication (live Nov 26, 12:59 PM ET, https://www.frenzycap.com/fedwatch/2026-12-09), FXStreet, TheStreet, CoinCentral, predictionmarketspicks cross-venue table — labeled as such; CME tool itself not directly readable. Desk 7 consolidated deliverable: ~/workspace/hedge-desk-research/desk7-core-indicators.md (Nov 13 snapshot; today's reads supersede it line by line above). Prior-day Desk 7 section: ~/workspace/hedge-desk-research/2026-11-25.md §7.

**Desk 7 summary for the package: no new data today (Thanksgiving); tally unchanged 5 HIKE / 0 CUT / 5 NEUTRAL; Dec 9 25bp hike call holds; Kalshi 25bp $0.92, FedWatch ~96%; Jan 2027 hike lean strengthened to $0.57. Next decisive print: Nov payrolls + Michigan prelim, Dec 4.**

---

## Cross-desk notes (synthesis)

- **NVDA, three desks agree:** no earnings in window (§1); Dec 2 ex-div $0.25 flat, primary-source confirmed, and the "dividend increase" claim is false (§2); IV ~73% flat term structure, WINDOW-CONTINGENT realized (Nov 20 drives 58.9% of the 20-day window) — no clean IV-vs-realized verdict (§3); governance reinstatement rally loosened financial conditions but changes no Desk 7 trigger (§7).
- **Section 301 ↔ watchlist (§5 + §1/§3):** Taiwan/Korea/Japan/Vietnam/Malaysia/Thailand/China cover the core electronics/semiconductor supply chain for AAPL, MSFT, NVDA, TSLA — but determinations are proposals only, no tariff in effect, no product coverage yet. Do not model a cost hit. Calendar: comments Jan 5, hearings Jan 25, 2027.
- **Desk 3 day-move correction (see top of package):** yesterday's package day moves are correct; Desk 3's were computed against a stale Yahoo `chartPreviousClose` meta field. The synthesizer re-pulled v8 chart bars this run and verified Nov 24 closes. Desk 3's IV levels are unaffected.
- **Desk 7 Sentry F3 confirmed live again (§7.0):** `curve_slope: 0.035` is wrong; use the independent +28bp 2s10s spread. Do not cite the AM report's fed-funds change or curve slope until F1–F5 close.
- **Gold (§5 vs Nov 25 package):** yesterday's ~$3,469–$3,486 was an intraday snapshot; today's Finnhub daily candle is the fuller Nov 25 read — low $3,426.81, close $3,589.44; Dec COMEX settle $3,535.80. Do not mix spot close and futures settle.

## Run log
- All seven desks completed and reported. No desk FAILED. No git/GitHub operations performed (research-only run).
- IV inputs file `2026-11-25-iv-inputs.json` as_of 2026-11-25T14:54:29-07:00, 23.5h old at pull — within the 26h guard, accepted.
- Quant ledger now ends at #372 (rows #361–#372 appended + 2026-11-26 jidoka entry, verified on disk).
- Desk 3 run logged to `~/memory/2026-11-26.md`; live-pull script at `/tmp/desk3_live_iv_pull.py`, raw output at `/tmp/desk3_live_iv_out.json`.
- Next scheduled run: Fri Nov 27, 2026, 13:30 PT (half-day session; initial claims w/e Nov 22 due).
