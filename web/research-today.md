# Hedge-desk daily research — Wed 2026-11-25

Run start 13:30 PT. Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Paper-only research; no trades, no Risk of Ruin, no trade authorization. Lens: value investor — mispricings, intrinsic-value gaps, margin of safety. Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED on every material claim.

**Close snapshot (FACT, Yahoo v8 chart / live options pull, ~13:28–13:35 PT):** SPY 716.70, QQQ 633.93, AAPL 355.58, MSFT 489.93, NVDA 149.30, TSLA 380.14. Day moves vs Nov 24 closes (SPY 718.78, QQQ 638.10, AAPL 354.07, MSFT 496.13, NVDA 155.38, TSLA 384.68 — Nov 24 package): SPY −0.29%, QQQ −0.65%, AAPL +0.43%, MSFT −1.25%, NVDA −3.91%, TSLA −1.18%. NVDA is −9.54% over two sessions vs its Nov 23 close (165.05). Thursday Nov 26 is Thanksgiving — US markets closed; Friday Nov 27 is a short session.

## Decision-relevant items (5)

1. **Core PCE re-anchored hotter, Dec 9 25bp hike call holds.** Oct core PCE y/y +3.3% vs 3.2% consensus (Sep 3.1%), m/m +0.3%; Q3 GDP second estimate +4.3% vs 3.5% consensus. Desk 7 tally unchanged 5 HIKE / 0 CUT / 5 NEUTRAL. Kalshi 25bp $0.93, FedWatch ~96%. The >25bp tail has collapsed to $0.03. (Desk 7, §7)
2. **Gulf escalation is the day's futures catalyst, not the EIA.** Houthi claims on Ras Tanura + Hormuz shipping attacks lifted Brent to a $94.61 wire settlement (+3.51%); damage/supply impact UNVERIFIED. EIA printed smaller-than-expected builds (crude +1.1M bbl) with record US production 14.065M b/d. Gold broke $3,500 to ~$3,469–$3,486, lowest since Sept 2025. USTR proposed Section 301 tariffs on 14 economies this morning (not in force; hearings Jan 25). (Futures, §5)
3. **No clean sell-premium verdict anywhere; first clean read lands Dec 1.** Live 2DTE IVs (Nov 27 expiry): SPY 19.09%, QQQ 30.51%, NVDA 58.81% richest. AAPL/MSFT/NVDA/TSLA windows formally WINDOW-CONTINGENT (single-day variance shares 32–59%); SPY/QQQ carry the jump-inflation caveat. Term structure slopes up into Dec 18 (SPY 24.0%, QQQ 35.5%), straddling Dec 9 FOMC. IV rank UNVERIFIED. (Premium, §3)
4. **NVDA Dec 2 is the only certain ex-div in the window** ($0.25, flat, primary-source confirmed). SPY Dec 18 amount undeclared; QQQ Dec 21 amount and pay date still UNVERIFIED (now a four-way pay-date dispute). No raises, cuts, or specials anywhere. (Dividend, §2)
5. **Quant: a falsification-grade null kills QQQ event-night edges.** Desai (SSRN 7687260, pre-registered, 849 sessions of full QQQ chains): overnight put spreads won 84% but averaged −1.1% of max risk (t=−0.87); six published option signals fail Holm correction. Desk rule from today: never cite a QQQ event-night edge claim without this null alongside. Ledger now ends #360; no TEST/INTEGRATE movement. (Quant, §4)

---

## 1. Earnings Event desk

**Headline: No watchlist earnings in the 2-week window (Nov 25 – Dec 9, 2026). Nothing to trade around, nothing to avoid.**

### In-window sweep — Nasdaq earnings calendar (api.nasdaq.com/api/calendar/earnings)
**FACT:** Queried every calendar date Nov 25 through Dec 9, 2026, one call per day (15 calls, all returned valid JSON). Zero watchlist symbols (AAPL, MSFT, NVDA, TSLA) on any date. SPY and QQQ are ETFs and report no earnings by construction. Source: Nasdaq earnings calendar API, as-of Nov 25, 2026 ~13:26 PT.

### Next earnings dates (outside the window — cross-checked fresh today, not carried from yesterday)
| Symbol | Next report | Timing | Consensus EPS | Consensus revenue | Status |
|---|---|---|---|---|---|
| AAPL | 2027-01-28 | TBA | $2.91 (range $2.83–$3.18) | $156.43B | **FACT** per Yahoo calendarEvents; `isEarningsDateEstimate: false` |
| MSFT | 2027-01-27 | TBA | $4.85 (range $4.82–$4.97) | $96.70B | **FACT** per Yahoo; flagged estimate (`isEarningsDateEstimate: true`) |
| TSLA | 2027-01-27 | TBA | $0.50 (range $0.36–$0.88) | $29.28B | **FACT** per Yahoo; flagged estimate (`isEarningsDateEstimate: true`) |
| NVDA | 2027-02-24 | After close (per Zacks) | ~$2.80–$2.88 (sources disagree) | ~$130.79B | **UNVERIFIED** — third-party estimate only; Zacks and TipRanks agree on the date but not the EPS; Yahoo calendarEvents still shows only the last report (Nov 17). Not confirmed by the company. |

Yahoo data pulled via the cookie+crumb handshake (crumb from query1 `/v1/test/getcrumb`, `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`), as-of Nov 25, 2026 ~13:26 PT. Yesterday's conflict (Yahoo Jan 27/28 vs TipRanks Feb 3/4) is superseded by today's direct Yahoo read: Jan 27 (MSFT, TSLA) / Jan 28 (AAPL). The Feb 3/4 TipRanks figures were not re-verified and are not carried forward.

### Most recent reports (context, not in-window)
- **NVDA — FACT:** Reported Nov 17, 2026 after close: EPS $2.68 vs Zacks consensus $2.47 (+8.5% surprise); revenue $115.84B per the Nov 17 print. (Zacks earnings summary, corroborated by the Nov 17–18 desk record.)
- **AAPL — FACT:** Last call Nov 2, 2026 (Yahoo calendarEvents). **MSFT — FACT:** Last call Oct 28, 2026. **TSLA — FACT:** Last call Oct 21, 2026.

### Options-implied expected move / historical average move
- **None applicable this run:** no earnings inside the window, so no implied-move calculation is warranted. **UNVERIFIED:** historical average earnings-day moves per name were not computed from free sources this run (no in-window event to anchor them to); no figure is offered rather than a guessed one.

### Adjacent large-cap events (outside watchlist, one line)
- **FACT (Nasdaq calendar, Dec 9):** Broadcom (AVGO) reports Dec 9 after close, consensus EPS $3.45; Adobe (ADBE) reports Dec 10 after close, consensus EPS $5.11. Watch for index-level vol spillover into QQQ, not a watchlist earnings event.

### What would change this
A company-confirmed earnings date inside the window (issuer IR / SEC 8-K), or a Nasdaq calendar update adding a watchlist name to a Nov 25–Dec 9 date. Next scheduled check: tomorrow's run; next watchlist event is MSFT/TSLA Jan 27, 2027 (estimates).

### Source notes / failures
- Nasdaq `api/quote/{symbol}/earnings-date` endpoint returned empty/non-JSON for all four names — not a valid route; discarded, calendar sweep + Yahoo used instead.
- Yahoo v10 quoteSummary without crumb returned `{"error": "Invalid Crumb"}` as expected; retried with the handshake and succeeded for all four names.
- No release was in-window, so no earnings-release teardown (statement_analysis reading order) was triggered.

---

## 2. Dividend Opportunity desk

**Window:** ex-dividend dates Nov 25 – Dec 23, 2026. Prices as of Yahoo v8 chart, Nov 25, 2026 ~13:28 PT (SPY $716.70, QQQ $633.93, AAPL $355.58, MSFT $489.93, NVDA $149.30, TSLA $380.14). Nasdaq dividends-calendar sweep (all 29 dates Nov 25–Dec 23, api.nasdaq.com, run today) returned exactly one watchlist row.

| Symbol | Ex-div date | Dividend | Yield* | Increase / cut / special | Consecutive increases (per standard) | Source / as-of |
|---|---|---|---|---|---|---|
| NVDA | **Dec 2, 2026** (Wed) | $0.25/qtr ($1.00/yr) | 0.67% | Flat — 3rd consecutive qtr at $0.25; no increase/cut/special | n/a (not a growth streak; payout ratio ~11%) | Nasdaq div calendar API + NVIDIA Q3 FY27 release (GlobeNewswire, Nov 17); Yahoo quoteSummary ex-div Dec 2 / pay Dec 23, 2026-11-25 |
| SPY | **Dec 18, 2026** (Fri) | **UNVERIFIED — amount not yet declared** (est. ~$1.89 is a repeat-of-Sep projection, not a declaration) | 1.06% TTM ($7.58 trailing) | None — pass-through distribution varies quarterly; not a raise/cut | n/a (ETF pass-through) | State Street published 2026 distribution schedule via Dividend Vision (ex Dec 18 → pay Jan 29, 2027; "Not yet declared," updated Nov 25); DividendMax (declaration expected Dec 17), 2026-11-25 |
| QQQ | **Dec 21, 2026** (Mon) | **UNVERIFIED — $0.7941 quoted by aggregators, but DividendMax still lists the Dec 2026 row as Forecast with no declared amount; declaration expected Dec 18** | 0.49% TTM ($3.09 trailing) | None announced | n/a (ETF pass-through) | Ex-date consensus: DripCalc, StockInvest, DivTrkr, TipRanks, DividendMax (est.). Pay date now **four-way disputed**: Dec 28, 2026 vs ~Jan 3, 2027 (est.) vs Jan 4, 2027 vs Jan 7, 2027 — **UNVERIFIED**, 2026-11-25 |
| AAPL | None in window — last ex-div Nov 12, 2026 ($0.27, paid Nov 16); next expected ~Feb 11, 2027 (unannounced) | $0.27/qtr ($1.08/yr) | 0.30% | Last raise Apr 30, 2026: $0.26 → $0.27 (+3.8%) | **15** per desk standard (initiation 2012 = yr 1; raises announced every year 2013–2026). Screeners quoting 13 use different conventions — do not copy those counts | Yahoo quoteSummary ex-div Nov 12 / pay Nov 16; dividend-count-standard.md, 2026-11-25 |
| MSFT | None in window — last ex-div Nov 19, 2026 ($0.98, payable Dec 10, 2026); next ex-div Feb 2027 | $0.98/qtr ($3.92/yr) | 0.80% | No new raise since Sep 15, 2026 board raise to $0.98 | **24 consecutive annual increases** (incl. Sep 2026 raise) per dividend-count-standard.md. MarketBeat's "23 years" uses a different convention — do not drift | Yahoo quoteSummary ex-div Nov 19 / pay Dec 10; standard file anchor, 2026-11-25 |
| TSLA | None — pays no dividend | $0 | 0% | None | n/a | Yahoo quoteSummary: exDividendDate and dividendDate both empty, 2026-11-25 |

\* Yields computed on today's ~13:28 PT prices (annualized forward rate for single names; TTM for the ETFs).

- **FACT — NVDA Dec 2 is the only declared, confirmed ex-div in the window.** Nasdaq calendar sweep returned exactly one watchlist row: NVDA, ex Dec 2, 2026, $0.25, pay Dec 23, 2026, record Dec 2, announced Nov 17, 2026. Corroborated at the primary source — NVIDIA's Q3 FY2027 results release: "NVIDIA will pay its next quarterly cash dividend of $0.25 per share on December 23, 2026, to all shareholders of record on December 2, 2026" (GlobeNewswire, Nov 17, 2026). Yahoo quoteSummary independently confirms ex-div Dec 2 / dividend date Dec 23.
- **FACT — SPY Dec 18 ex-div / Jan 29, 2027 pay is issuer-scheduled; amount undeclared.** State Street's published 2026 distribution calendar (via Dividend Vision, updated Nov 25, 2026): SPY Dec 18 → Jan 29, "Not yet declared," last paid Sep 18, $1.8888. Last three 2026 distributions: Mar 20 $1.797, Jun 18 $1.904, Sep 18 $1.88883 (total $5.58935 YTD). DividendMax expects declaration Dec 17, 2026. No change from yesterday.
- **FACT — QQQ Dec 21 ex-div date is consensus; INFERENCE/UNVERIFIED — the $0.7941 amount and the pay date (re-checked today, still unresolved).** DividendMax still lists the Dec 2026 row as **Forecast** with no declared amount and a Dec 18, 2026 declaration date; DripCalc's "declared" $0.7941 label conflicts with that and with Dividend101, which states the pay date "hasn't been announced yet" and estimates ~Jan 3, 2027. $0.7941 is exactly last December's (Dec 22, 2025) declared amount. Pay date is now a **four-way** dispute: Dec 28, 2026 (DripCalc, DividendMax forecast) vs ~Jan 3, 2027 (Dividend101 est.) vs Jan 4, 2027 (yesterday's third source) vs Jan 7, 2027 (DivTrkr, which lists $0.75). Amount candidates: $0.7941 (repeat of Dec 2025) vs $0.7514 (repeat of Sep) vs $0.75. No Invesco declaration found at any primary source. Treat $0.7941 as a forecast, not a declaration.
- **FACT — AAPL and MSFT are out of window; both last went ex-div this month.** MSFT's Dec 10 payment lands inside the window but its ex-div does not — holders of record Nov 19 receive it; no action window remains.
- **FACT — No increases, cuts, or specials announced among watchlist names this run.** NVDA flat; SPY/QQQ amounts undeclared (nothing to raise or cut); AAPL/MSFT last raises were Apr 2026 / Sep 2026 respectively.
- **Dismissed conflicting claim (do not use):** a low-quality aggregator page (dopepics.io) claims NVDA "declared a dividend increase" on Nov 20, 2026, even citing "$0.04 per share" — contradicted by the primary source (NVIDIA's Nov 17 release: $0.25 flat), the Nasdaq calendar ($0.25, announced Nov 17), and MarketBeat's announcement table ($0.25, 11/17/2026). The $0.04 figure is NVDA's pre-split-era quarterly rate. Treat as UNVERIFIED/false; no NVDA raise exists.
- **INFERENCE — Nasdaq calendar absence for SPY/QQQ is a coverage artifact, not a contradiction.** The calendar lists Nasdaq-listed names; SPY is NYSE Arca. QQQ is Nasdaq-listed yet absent, most likely because its December distribution is not yet declared through Nasdaq's feed (declaration expected Dec 18) — consistent with DividendMax's Forecast status.

**Desk verdict:** Quiet window; one actionable date. NVDA Dec 2 ($0.25, flat, fully declared and primary-source confirmed) is the only certain ex-div in the next four weeks. SPY Dec 18 and QQQ Dec 21 are real calendar dates, but with amounts undeclared they carry no yield or income signal yet — and QQQ's pay date is now disputed four ways, so do not cite any QQQ amount or pay date as fact. Nothing here changes a margin-of-safety read on any watchlist name: all six yields are sub-1.1% and none of the three December dates involves a raise, cut, or special. **What would change it:** a State Street declaration for SPY (~Dec 17) or an Invesco declaration for QQQ (~Dec 18) with an amount materially above/below last quarter; any new AAPL/MSFT/NVDA board action; a TSLA dividend initiation (none indicated).

**Sources:** api.nasdaq.com/api/calendar/dividends (29-date sweep, Nov 25–Dec 23, 2026); Yahoo v10 quoteSummary (cookie+crumb) + v8 chart, Nov 25, 2026 ~13:28 PT; NVIDIA Q3 FY27 release (GlobeNewswire, Nov 17, 2026); State Street 2026 distribution schedule via Dividend Vision (updated Nov 25, 2026); DividendMax (SPY/QQQ forecast rows); DripCalc, StockInvest, DivTrkr, Dividend101, TipRanks, FI Handbook (QQQ/SPY third-party estimates, UNVERIFIED); MarketBeat announcement table; ~/workspace/hedge-desk-research/dividend-count-standard.md. No source failed; Nasdaq API returned data.calendar.rows (not data.calendar as a list — parse accordingly).

---

## 3. Overnight Premium desk (IV)

### Inputs file (freshness guard — PASS)
**FACT:** `~/workspace/hedge-desk-research/nightly/2026-11-25-iv-inputs.json`, `as_of` **2026-11-25T07:54:49-07:00** — ~5.5h old at run start, **within the 26h guard (FRESH, not stale)**. Realized window Oct 28–Nov 24 (20 closes, 19 returns). One file note: repo failover module unavailable on this checkout, so the file's leg is legacy Yahoo-only (disclosed in its `failures`).

**Stale-jump screen (FACT, from the file):**

| Symbol | ATM IV (premarket, DTE-0) | Realized 20d | Max single-day var. share | Window |
|---|---|---|---|---|
| SPY | 29.44% | 32.53% | 0.270 | Not contingent |
| QQQ | 38.45% | 49.09% | 0.253 | Not contingent |
| AAPL | 27.37% | 29.28% | 0.433 | **WINDOW-CONTINGENT** |
| MSFT | 34.35% | 39.33% | 0.371 | **WINDOW-CONTINGENT** |
| NVDA | 91.72% | 130.47% | 0.589 | **WINDOW-CONTINGENT** |
| TSLA | 56.80% | 74.82% | 0.324 | **WINDOW-CONTINGENT** |

**Caveat on the file's DTE-0 prints (FACT + INFERENCE):** those premarket ATM IVs are on the Nov 25 expiry, which died at 16:00 ET / 13:00 PT — they are no longer tradeable and are **not** today's IV levels. The live supplement below replaces them. The DTE-0 prints were also expiry-day inflated (gamma/pinning), so the drop to the live 2DTE prints is tenor, not a vol collapse.

### Live Yahoo supplement (labeled live, not yesterday's data)
**FACT:** Live Yahoo v7 options pull, cookie+crumb handshake, **~13:35 PT Nov 25 (post-close)** — **6/6 printed, no nulls** (the recent expiry-day-guard nulls did not recur; the pull rolled to the nearest unexpired expiry). Rollover is explicit: nearest expiry Nov 25 was dead, so all prints are the **Fri Nov 27 expiry, DTE 2** (Thu Nov 26 Thanksgiving — market closed; Nov 27 is the next trading day, short session). Raw pull saved at `/tmp/iv_live_2026-11-25.json`. Spot closes from the same payload: SPY 716.70 (−0.29% on the day; Yahoo-reported day range 695.45–718.43, a wide range), QQQ 633.93.

| Symbol | Live ATM IV (Nov 27, DTE 2) | Call / Put IV | ATM strike vs spot | Bid/ask |
|---|---|---|---|---|
| SPY | **19.09%** | 18.89 / 19.28 | 717 vs 716.70 | 3–4c, tight |
| QQQ | **30.51%** | 28.76 / 32.25 | 634 vs 633.93 | 6–7c, tight |
| AAPL | **19.41%** | 19.92 / 18.90 | 355 vs 355.58 | 29–32c |
| MSFT | **28.64%** | 28.98 / 28.30 | 490 vs 489.93 | 60–65c |
| NVDA | **58.81%** | 58.35 / 59.28 | 149 vs 149.30 | 0c (locked) |
| TSLA | **40.74%** | 40.96 / 40.53 | 380 vs 380.14 | 0–15c |

**Term structure (FACT, second live pull):** Dec 18 monthly, DTE 23 — SPY **23.98%**, QQQ **35.49%**. Curve slopes **up** (SPY 19.1% → 24.0%; QQQ 30.5% → 35.5%). **INFERENCE:** front end is compressed into the Thanksgiving lull (one trading day to expiry); part of the rise to Dec 18 is event premium — that expiry straddles the Dec 9 FOMC meeting. No front-month hump anywhere, consistent with no earnings in the window.

**Parity sanity check (CFA):** call/put ATM IVs track within ~1pt on SPY/AAPL/MSFT/NVDA/TSLA; QQQ puts run ~3.5pts rich to calls — normal equity downside skew, not a parity violation. No parity violation observed. Tight SPY/QQQ markets = live quotes, not stale marks. **Guard confirmation:** a mis-aimed fetch of the dead Nov 25 expiry returned solver-residual junk (SPY 4.2%, QQQ 7.2%) — correctly excluded, per the post-expiry fail-closed rule.

### IV-vs-realized verdicts
- **SPY / QQQ — no clean verdict; JUMP-INFLATION CAVEAT (not formally contingent).** Live IV sits well below realized (SPY 19.1% vs 32.5%; QQQ 30.5% vs 49.1%), but the realized window still contains the Nov 5 crash day (share 27.0% SPY / 25.3% QQQ — under the 30% threshold only because the Nov 23 jump day diluted Nov 5's share; the flip from contingent to not-contingent is arithmetic, not a clean window). **Do not read this as "premium is cheap."**
- **AAPL / MSFT / NVDA / TSLA — WINDOW-CONTINGENT, no verdict.** Single-day shares 32–59%; any IV-vs-realized comparison built on these windows is invalid. NVDA is the extreme case: realized 130.5% is dominated by one day (58.9% share); its live 58.8% IV is the richest name on the board but cannot be judged rich or cheap against that window.
- **What would change it:** the Nov 5 crash day ages out of the 20-day window after **Fri Nov 28** close — the first clean realized read lands in the Mon Nov 30 / Dec 1 file. Until then, all four contingent names and the SPY/QQQ caveat stand.

### Earnings in window — none
**FACT:** the file's 45-day Nasdaq earnings sweep (this morning) returns `next_earnings: null` for all six names. **No binary event inside the window — no premium-into-earnings avoid flag.** NVDA reported Nov 17 (post-earnings; IV normalized off the event). Nothing on the calendar until the late-January reporting season (outside the sweep — no date asserted).

### IV rank — UNVERIFIED
**UNVERIFIED:** no free IV-history source was available in this run, so IV rank cannot be computed. **No elevated-IV-rank flag can be issued today** — the compressed front-month IVs above are a level-vs-realized observation, not a rank claim. Do not cite an IV rank for any name.

### Decision-relevant items
1. **No earnings binary in window; no avoid flag.** Premium is not being sold into an event on any watchlist name.
2. **No clean "sell premium" verdict anywhere.** SPY/QQQ IV < realized only against a jump-inflated window (caveat applies); AAPL/MSFT/NVDA/TSLA formally WINDOW-CONTINGENT. First clean read: Dec 1 file, after Nov 5 ages out Nov 28.
3. **Term structure slopes up into Dec 18 (SPY 19.1% → 24.0%, QQQ 30.5% → 35.5%)** — front compressed by the holiday lull; Dec 18 straddles Dec 9 FOMC (INFERENCE: event premium in the back leg).
4. **IV rank UNVERIFIED** — no elevated-IV flag issuable from free sources today.
5. **NVDA still the richest name (58.8% 2DTE)** but its realized window is unusable (58.9% single-day share) — no rich/cheap call until the window cleans.

Sources: `~/workspace/hedge-desk-research/nightly/2026-11-25-iv-inputs.json` (as_of 2026-11-25T07:54:49-07:00); live Yahoo Finance v7 options chains via cookie+crumb, pulled ~13:35 PT 2026-11-25 (Nov 27 + Dec 18 expiries; raw output `/tmp/iv_live_2026-11-25.json`); CFA derivatives_options.md (parity/sanity-check standard).

---

## 4. Open Quant/AI Model Lab

**Coverage (FACT, as of 13:30–14:10 PT today):** Thin pre-Thanksgiving window — 9 q-fin items submitted 23 Nov 18:00Z–24 Nov 15:18Z; API submittedDate range and no-filter top-40 control agree (0 missing; control newest 2611.32791). No replacements (lastUpdatedDate range returns only new v1 items). SSRN leg (2 searches) surfaced 3 papers new to the ledger, released 12/17/18 Nov — earlier sweeps' search leg missed them; all three abstracts read at source. All 9 candidates scored with the repo module (`hedge_desk.research_intelligence.assess_source`, never hand-scored). Ledger now ends at **#360**; rows #352–#360 appended to ~/workspace/hedge-desk-research/quant-lab-ledger.md, plus a jidoka entry and a #343 v2 note. **No TEST/INTEGRATE movement — run max 60, all WATCH except one ARCHIVE.**

**Top of the run (tied, 60 → WATCH)**
- **#356 — Colombi/Di Francesco/Rossi, "Delta-Vega Hedging with Deep Reinforcement Learning" (arXiv:2611.32790v1, 24 Nov).** PPO hedges price + vol risk (underlying + longer-dated option) under transaction costs, state restricted to market observables. FACT (abstract): on historical S&P 500 index options, two-instrument strategies roughly halve P&L dispersion vs Delta hedge; PPO beats Delta-Vega on P&L vol at comparable costs, advantage concentrated in high-vol episodes. INFERENCE: directly premium-desk — hedging-cost discipline under vol moves. No code link in API record → WATCH, not TEST. *What would change it: code release → sandbox PPO delta-vega vs practitioner Delta-Vega on a live SPY chain with costs.*
- **#360 — Desai, "Do Option Markets Predict the Nasdaq-100? Pre-Registered Tests on QQQ Option Chains" (SSRN 7687260, posted 12 Nov).** Pre-registered (rules hashed before any return computed), cost-honest **negative result** on QQQ: 15 primary tests, 849 sessions of full EOD QQQ chains (Jun 2023–Oct 2026), filled at bid/ask. FACT (abstract): overnight put spreads won 84% but averaged −1.1% of max risk/trade (t=−0.87); overnight iron condors −3.5% (t=−2.05); short iron butterflies before CPI/payrolls/FOMC/mega-cap earnings no better than ordinary nights; six published option signals fail Holm correction. INFERENCE: kills widely-quoted QQQ event-night ideas with a falsification-grade protocol — desk rule: never cite a QQQ event-night edge claim without this null alongside. Full paper not read (UNVERIFIED beyond abstract). *What would change it: full-paper read verifying the Holm table.*

**Also WATCH**
- **#358 — Khan, "Dealer Gamma Exposure, Intraday Volatility and Liquidity in the NASDAQ-100" (SSRN 7699738, posted 18 Nov), 54.** Hedging-feedback model; FACT (abstract): net GEX −$6bn/1% move raises daily vol +7.9% (continuous hedging) / +12.2% (close-concentrated), lifts P(>3% intraday range) 9.6%→13.7%. Caveat: **no empirical estimates reported** — simulation + estimation spec only. *What would change it: revised version with NDX/QQQ estimates.*
- **#352 — Gawronsky, "Pretrained Tabular Features and the Measurement of Financial Proximity" (arXiv:2611.31491v1), 51.** Frozen TFM representations as a financial-dissimilarity measure in S-APT on US equities 2011–2025; peer selection / risk attribution read for the earnings and dividend desks. No code.
- **#354 — Cesarone et al., "Semivariance and Semivolatility in Portfolio Selection" (arXiv:2611.32638v1), 51.** Downside-risk taxonomy; risk-parity / Sortino / risk-budgeting well-posedness; OOS backtest on DJ + Nasdaq-100 constituents with block-bootstrap. Portfolio construction is not a desk lane, but the risk-budgeting machinery transfers to margin-of-safety thinking.
- **#353 — Filipovic/Tissot-Daguette, "A Kernel Framework for Linear Operator Equations" (arXiv:2611.31626v1), 48.** RKHS collocation for pricing PDEs/PIDEs incl. multi-asset and jump-diffusion options; Greeks by direct differentiation. Methodology transfer only, no code.
- **#357 — Sepp/Rakhmonov, "Rough log-normal SV with quadratic drift" (arXiv:2611.32791v1), 48.** Exact second-moment thresholds, conditional squared VIX, martingale condition. Calibration on Bitcoin/Ether smiles only (crypto data — methodology transfer, not SPX evidence). No code.
- **#359 — Sharma, "Neural Spectral Dimension… American Options under Rough SV" (SSRN 7694798, posted 17 Nov), 45 (band floor).** Variance-reduction framework claiming >4× under bank calibrations; central eigenvalue law is **Conjecture 4.5** (unproven). No code.

**ARCHIVE (band discipline)**
- **#355 — Soloviev/Kirsopp, "Large-Scale Streaming Portfolio Optimization with Pauli Correlation Encoding" (arXiv:2611.32769v1), 39.** Quantum + portfolio-construction lane; no desk transfer.

**Triage exclusions (no ledger rows):** 2611.32389 AgentBank (blockchain banking), 2611.32488 fractional-order stochastic-dominance group decision-making (no desk lane); SSRN 7705802 prediction markets (excluded per 2026-11-12); SSRN 7672058 entrepreneurial decision-making (out of scope).

**Movement:** #343 (Valeyre MaxVar) **v1→v2** (updated 2026-11-24) — title/abstract unchanged, same 1.28/1.24/1.17 Sharpe figures; stays WATCH. Re-checks via arXiv API id_list: #4 (v1), #9 (v2), #13 (v1), #14 (v3), #15 (v1), #20 (v2), #21 (v3), #25 (v4), #30 (v3), #31 (v3), #257 (v2), #255 (v2), #339–#342/#344–#351 (all v1) — no other movement.

**Gaps / failures:** None blocking. GitHub leg: no repo links in any new candidate, so no license verification was required and no new-repo discovery was run. arXiv API via exec curl worked this run (yesterday it returned empty — transient). All material findings above are abstract-level (source-reported, UNVERIFIED beyond the abstract) per the evidence standard; no full papers were read.

---

## 5. Weather/War/Logistics Futures Event desk

**Bottom line — 4 things that matter:** (1) Hot core PCE (3.3% y/y vs 3.2% expected) + Q3 GDP revised to 4.3% **confirmed** Tuesday's gold fade — gold broke $3,500 to its lowest since Sept 2025. (2) EIA petroleum printed a smaller-than-expected build; crude rose anyway, but the driver was the Gulf, not the EIA — Houthi strikes claimed on Ras Tanura + Hormuz shipping attacks lifted Brent ~3.5% to settle $94.61. (3) Brent level: yesterday's Yahoo/DTN spread is superseded by a wire-converged settlement, but Yahoo's live Brent quote is again ~$4 below the wires — do not use Yahoo Brent as a settled level today. (4) USTR proposed Section 301 tariffs on 14 economies this morning (not yet in force; hearings Jan 25) — a fresh trade/demand headwind for 2027, and gold fell ~$37 in the 40 minutes after the announcement. Thursday is Thanksgiving (US markets closed, thin liquidity into Friday).

### 5.1 EIA Weekly Petroleum Status — week ended Nov 20, released 10:30 ET today [FACT, EIA via Reuters/WSJ/Oilprice]

| Item | Print | vs consensus | vs 5-yr avg |
|---|---|---|---|
| Commercial crude | **+1.1M bbl to 418.9M** (3rd straight build; prior wk +3.4M) | Below Reuters +1.5M / +2.0M; API had +0.126M | −3% |
| Gasoline | **+1.7M bbl to 217.7M** (prior +5.2M) | In line (+1.7M) | +3% |
| Distillates | **+0.715M bbl to 105.6M** | Below +1.3–1.5M expected | −6 to −7.7% |
| Cushing | −0.534M bbl to 25.6M | — | — |
| SPR | −2.9M bbl to 273.5M | — | — |
| Refinery runs / utilisation | +428k b/d to 17.3M b/d; **97.5%** (+1.8pp) | — | — |
| Production | **14.065M b/d, record high** (+33k b/d) | — | — |
| Imports / exports | Imports +673k to 6.3M b/d; exports −1.2M to 3.3M b/d | — | — |

**Read [INFERENCE]:** smaller-than-expected builds across all three products = modestly supportive, and crude rose on the print — but the day's +3.5% Brent move tracks the Gulf headlines, not the EIA. Record US production + a 3rd weekly build undercuts any structural-tightness story. **What would change it:** a Cushing draw accelerating toward tank-bottoms, or a confirmed Ras Tanura supply loss (see §5.4).

### 5.2 Core PCE + macro — released 08:30 ET today [FACT, BEA via Reuters/FXStreet/KPMG]

| Print | Actual | Expected | Prior |
|---|---|---|---|
| Headline PCE m/m / y/y | +0.3% / **3.8%** | 3.8% y/y | +0.5% / 3.6% (Sept y/y revised to 3.7% per FXStreet) |
| Core PCE m/m / y/y | +0.3% / **3.3%** | 3.2% y/y | +0.3% / 3.1% |
| Super-core services y/y | 3.6% | — | 3.6% |
| Personal income / spending | +0.7% / +0.3% | +0.4% / +0.4% | +0.3% / +0.6% (Sept, per Hindu BusinessLine) |
| Real PCE | −$5.8B (<0.1% decline) | — | — |
| Q3 GDP, 2nd estimate (same 08:30 slot) | **4.3% annualised** | 3.5% | 3.4% advance |

**Market reaction [FACT]:** Dec 25bp hike "almost fully priced" (~96.4% per CME FedWatch via TradingKey); Jan additional hike ~55–56% (FXStreet). DXY ~103.90 (+0.10%) at release, later above 104 per TradingKey. **Read [INFERENCE]:** the print **confirms** Tuesday's pre-positioning for a hot PCE — core y/y at 3.3% is the hottest since Nov 2023 and, with GDP at 4.3%, gives the Fed no reason to deviate from the hike path. This is the rates desk's re-anchor; for futures it is a headwind to gold and a neutral-to-negative for crude demand expectations. **What would change it:** Dec 9 FOMC dot/guidance softening, or a Nov PCE (due Dec 23) back toward 3.1% core.

### 5.3 Energy levels — Brent spread: resolved on wires, Yahoo discrepant again

| Benchmark | Level | As-of / source |
|---|---|---|
| Brent Jan-27, **settlement** | **$94.61, +$3.21 (+3.51%)** | Dow Jones via Morningstar 15:08 ET; corroborated Rigzone 16:16 ET ("settled under $95, highest in over a week") |
| Brent Tue settle (anchor) | $91.40 (+2.3% Mon→Tue) | Reuters via FinanceFeeds; corroborated by Yahoo daily close $91.40 |
| Brent intraday path today | ~$89.93–$90.97 early → $92.41 13:05 GMT → $93.14 10:35 ET → $93.79 18:21 UTC → $94.61 settle | Reuters/Euronext, FinanceFeeds (Yahoo data), Oilprice, OilpriceAPI |
| WTI Jan-27 settlement | **$83.68, +2%** | Rigzone 16:16 ET; Oilprice 10:35 ET had $83.08 (+1.26%) |
| Natgas Jan-28 | **$3.66–3.68/MMBtu** (+0.5–0.7%) | WSJ/Seeking Alpha/Energy Edge, ~12:00 ET; Dec contract expiring today $3.29–3.34 |
| Gold spot | **~$3,469–$3,486, −2.0 to −2.8% on the day**; intraday low $3,468.15; Tue close $3,555.55 | Reuters/Kitco 09:15 ET $3,483.59; FXStreet ~$3,469; Ausecure 09:15 ET $3,486.35 |

**Yahoo discrepancy [FACT, desk's own pull 13:16–13:17 PT via v8 chart]:** Yahoo BZ=F shows $90.74 and GC=F $3,601.10 — i.e. Brent ~$3.87 below the settlement wires and gold ~$115 *above* the spot wires and moving the wrong way on the day. Yahoo CL=F $84.12 and NG=F $3.68 are close to the wires. **Do not use Yahoo BZ=F or GC=F as settled levels today** — same failure mode as yesterday's unresolved Yahoo ($88.31) vs DTN ($90.54) Brent spread, now wider. The wire settlement ($94.61) is the usable level; the Yahoo gap itself is UNRESOLVED (likely a Yahoo contract/refresh artifact — no independent confirmation). A low-quality outlier (thefoxdaily $87.54 Brent) was disregarded. **What would change it:** an Aramco/export-loading confirmation of Ras Tanura damage, or tomorrow's wire settles re-converging with Yahoo.

### 5.4 Geopolitics / logistics — Gulf escalation is today's catalyst [FACT unless noted]

- **Ras Tanura [FACT, Reuters]:** Houthis claimed drone/missile strikes on Saudi Arabia's largest refinery (550k b/d) and Riyadh's financial district (2nd strike on the district in a week). Saudi-led coalition said air defences intercepted 4 drones at Ras Tanura but did **not** confirm the refinery was struck. NASA/Planet satellite imagery reviewed by Reuters shows thick black smoke over the refinery; a source confirmed an attack; Aramco and the Saudi government had not commented at last check. **Damage / supply impact = UNVERIFIED** — no confirmed outage, export-loading, or throughput figure yet.
- **Strait of Hormuz [FACT, Reuters/UKMTO via Barchart/FinanceFeeds]:** container ship targeted and stopped Tue; 3 vessels struck by unidentified projectiles Mon; Iran claims more tankers hit mines since Tue — **no independent confirmation**. Flows continue: IEA — Hormuz crude+fuels flows +7% q/q in Q3 to 9.1M b/d (vs 21.4M b/d year-earlier); Gulf exports (SA/UAE/Iraq/Kuwait) +10% to 15.53M b/d in Oct; Saudi Oct production +970k b/d to 9.2M b/d. Vortexa: floating storage −5.5% w/w to 79.3M bbl (wk ended Nov 20).
- **Offset [FACT, Reuters]:** Libya's Sharara pipeline reopened after a valve closure by an "unlawful group" — bearish offset to the Gulf premium.
- **Read [INFERENCE]:** market is pricing a *risk premium on prompt barrels*, not a realised supply loss — flows are still recovering and the glut narrative (EIA STEO Q1-27 +3.0M b/d surplus, Q2 +4.9M b/d) is intact underneath. **What would change it:** confirmed Ras Tanura outage/export curtailment, a Hormuz transit halt, or a ceasefire/de-escalation headline.

### 5.5 EIA Natural Gas Storage — week ended Nov 20, released 12:00 ET today (pulled forward from Thu for Thanksgiving) [FACT, EIA via WSJ/Energy Edge/Seeking Alpha]

**−24 Bcf to 3,858 Bcf — first withdrawal of the season**, in line with the 5-yr average draw; matched Bloomberg −24 consensus (Seeking Alpha consensus −19). Surplus unchanged at **+80 Bcf (+2.1%) over the 2021–25 average**; 79 Bcf below year-ago 3,937 Bcf. Regional: East −19, Midwest −11, South Central **+8** (injection), Mountain −1, Pacific −1. Dec contract expires today (~$3.29–3.34); Jan $3.66–3.68. **Read [INFERENCE]:** neutral print — an in-line first draw with the surplus intact; the curve (Dec ≪ Jan) is doing the work, not the storage number. Next release Dec 3. **What would change it:** a sustained cold snap driving back-to-back >average draws, or a production freeze-off.

### 5.6 USDA / grains — quiet pre-holiday [FACT]

- **FY2027 ag trade outlook [FACT, USDA ERS/FAS, Nov 24]:** export forecast raised to **$188.5B** (+$2.0B vs Aug, +$7.3B vs FY26 $181.2B); imports $213.5B. Soybeans $23.8B (from $21.9B), corn $18.5B. China accounts for the entire y/y export gain even after USDA cut its Beijing outlook.
- **Export inspections, wk ended Nov 19 (reported Mon Nov 23) [FACT, USDA]:** corn 1.19M MT (+36.9% w/w; MYTD 13.66M vs 17.55M year-ago); soybeans 1.56M MT (−10.4% w/w; MYTD 17.46M vs 10.95M); wheat 344,886 MT (−16.6%; MYTD 8.59M vs 12.86M).
- **Today [FACT, DTN 08:33–08:36 CT]:** private exporters reported **132,000 MT soybeans to China** for 2026/27. Futures in quiet pre-holiday trade: Mar corn +1¾¢, Jan soybeans −6¾¢, Mar KC wheat −2¢, Mar Chicago wheat −2¼¢. Portland grain bids: HRW wheat lower, spring wheat higher; next report Mon Nov 30 (Thanksgiving). No WASDE today; next WASDE is December (date UNVERIFIED — not asserted).
- **Read [INFERENCE]:** no grain catalyst today; the soybean-to-China sale + strong MYTD soybean inspections are the only modestly supportive grain signal, and it is small against the trade-policy overhang in §5.7.

### 5.7 Trade policy — USTR Section 301 tariffs proposed this morning [FACT, USTR via Reuters/JD Supra]

Proposed excess-capacity tariffs on **14 economies** (China, EU, Japan, South Korea, India, Vietnam, Taiwan, Thailand, Indonesia, Malaysia, Singapore, Switzerland, Bangladesh, Cambodia) after an 8-month Section 301 probe; Mexico and Norway excluded (investigations ongoing). Headline/capped rates: China 20% capped (40% if the US-China truce expiring Jan 10 unravels; stacked on ~25% first-term duties), Vietnam 35% / 20% if a deal is reached, India 25% / 17% if a deal, EU/Japan/Korea/Taiwan/Switzerland 15% capped, Singapore 10% capped. Separate: proposed 10% tariff on Brazilian Embraer aircraft + higher sugar duties above quota. **Not in force** — comments due Jan 5, 2027, hearings from Jan 25, implementation likely Feb. **Market footprint today [FACT, Ausecure step-log]:** gold fell ~$37 in the 40 minutes after the ~06:19 ET announcement (after an earlier overnight −$30 slide), then −$30 in the 10 minutes after the 08:30 ET data. **Read [INFERENCE]:** near-term futures impact is via risk-off/liquidity (gold sold with equities, not bought as haven) and a 2027 demand overhang for industrial commodities and ag exports — not a same-day supply shock. **What would change it:** the Jan 5 comment / Jan 25 hearing outcome, or a China-truce break before Jan 10.

### 5.8 Curve — what futures are pricing [FACT as-of Nov 19 settles, INFERENCE on interpretation]

Steep **backwardation persists**: WTI Dec-26 $83.89 / Jan-27 $83.09 / Feb-27 $82.21, Dec-27 <$73, Dec-28 ~$68; Brent Jan-27 $92.68 / Feb-27 $90.18, mid-70s by mid-2027, ~$62 by early 2038 (commodity-board, Nov 19 settles — **not today's curve**; today's front end is ~$3 higher on Brent). **Read [INFERENCE]:** the curve says *tight/risky now, softer later* — a war/logistics premium on prompt barrels rolling off into the forecast 2027 surplus, not a demand boom. Value lens: front-month crude strength on headlines offers no margin of safety — it is event premium over a record-US-production, surplus-forecast base. **Next tests:** OPEC+ meeting **Nov 29** (2027 framework); next EIA petroleum Wed Dec 2; EIA gas Thu Dec 3; FOMC Dec 9; Fed Beige Book 14:00 ET today; new home sales 10:00 ET today (results not yet in at writing).

### Sources & as-of
EIA petroleum status 10:30 ET + EIA gas storage 12:00 ET (eia.gov via Reuters/WSJ/Oilprice/Energy Edge/Seeking Alpha); BEA Personal Income & Outlays / Q3 GDP 08:30 ET (Reuters, FXStreet, KPMG); ICE Brent/WTI settlements via Dow Jones/Morningstar 15:08 ET + Rigzone 16:16 ET; spot gold Reuters/Kitco 09:15 ET, FXStreet, Ausecure 09:15 ET; Gulf/Hormuz Reuters via Barchart/FinanceFeeds/Rigzone; USTR announcement via Reuters/JD Supra (morning, ~06:19 ET per Ausecure); USDA ERS/FAS Nov 24 + USDA inspections Nov 23 + DTN 08:33 CT; curve levels commodity-board Nov 19 settles. Yahoo v8 chart pull by the desk 13:16–13:17 PT (BZ=F $90.74, CL=F $84.12, GC=F $3,601.10, NG=F $3.68) — **BZ=F and GC=F discrepant vs wires, flagged above, not used as settled levels**. Jobless claims exact print not independently verified — not asserted. No USDA WASDE or EIA blackout: federal releases ran on schedule (CR through Dec 11).

---

## 6. Box/Parity Observer

**Bottom line: quiet on parity violations; two new items to log, neither a parity break.**

**New since yesterday:**

1. **Cboe binary equity options — new listed product class (FACT, SEC filing published Nov 24, 2026).** Cboe rule filing SR-CBOE-2026-087, filed Nov 13 and published by the SEC Nov 24, adopts rules permitting European-style, cash-settled binary options on eligible individual stocks, ETFs and ETNs (fixed $100 settlement; min $290B market cap / 4M ADV / $200M ADTV for single stocks; 25,000-contract position limit). The SEC waived the 30-day operative delay, so listings can begin, but no contracts have traded yet (INFERENCE: no live parity/box data exists for this product yet). Cboe separately launched KPI binary options on Nov 24. Relevance to this desk: binary options have a discontinuous payoff with no standard put-call parity — watch for any future parity/box analysis once they list, but nothing to measure today. Sources: SEC SRO rulemaking page (SR-CBOE-2026-087, Nov 24); fxnewsgroup.com Cboe news, Nov 24–25.
   - Note: this is a new product, not an index-methodology change and not a parity violation.
2. **Fresh published box-spread test — no exploitable lending edge (FACT, dated Nov 23, 2026).** An independent test (nyasekai.com, "Lending cash through an index box spread," Nov 23) measured SPX box spreads from a single delayed-chain snapshot (Nov 23, 07:23 ET, Friday-close quotes): fill-realistic implied rates on the widest ($50k face) box were 2.57% / 2.97% / 3.28% at ~3/6/12 months vs Treasury yields 4.33% / 4.42% / 4.62% — i.e. long boxes underpay T-bills after spreads and fees; narrow boxes were deeply negative (−8.81% to −3.77%). Verdict: dead idea, costs ate it. Caveats (FACT): single snapshot, pre-open stale quotes, no in-session fills measured — weak evidence, but directionally consistent with the Nov 12 solvinc.io measurement (short-end box 3.86%, long-end 5.16% vs ~5.39% IBKR margin) that boxes track, not beat, funding costs. No mispricing to exploit; consistent with parity holding. Source: https://www.nyasekai.com/strategies/box-spread-as-usd-loan/

**No change / nothing new:**
- **Cboe notices:** no new index-methodology notice surfaced since yesterday. The SPXO correction (notice id 62439) remains the latest surfaced item — not re-reported as new. Cboe notice id 61537 likewise unchanged.
- **S&P DJI:** no new methodology document since yesterday. The U.S. style-index overhaul (momentum out of growth, free-cash-flow into value; effective Dec 21, pro-forma files Dec 4) was announced ~Oct 28 and is already known; the S&P/TSX foreign-issuer eligibility change (Sept 11) is older still. No new S&P 500 membership/methodology release in the last 24h.
- **Published parity-violation analysis:** none new. The arXiv put-call parity papers (Shin, May 2026) are months old; no new box-spread or parity-violation study published in the last 24h beyond the nyasekai test above.
- **Parity verdict for the watchlist:** no evidence of a tradable put-call or box parity violation in SPY/QQQ/AAPL/MSFT/NVDA/TSLA today — UNVERIFIED by direct quote check (this desk did not pull live chains; deterministic parity math stands as the check, and no published source reports a violation).

---

## 7. Bonds & Rates desk (Desk 7)

**Status: Desk ran. Module `rates_desk.rates_environment()` executed this session, REAL_FRED_RATES mode. All rates levels independently verified against FRED. Tally UNCHANGED: 5 HIKE / 0 CUT / 5 NEUTRAL. Dec 9 25bp hike call HOLDS — today's core PCE re-anchor came in hotter, not softer.**

### 7.0 Sentry W48 verification (rates_desk.py CONDITIONAL KEEP — module numbers NOT taken on trust)

Independent FRED pulls this session (`fred_observations.py`, `--limit=N` form), all as of Nov 24 unless noted:

| Finding | Module says | Independent check | Verdict |
|---|---|---|---|
| F1 — fed-funds change unsigned, no baseline | `fed_funds_change_over_window: 0.00` | DFF pulled 65 obs, Sep 21–Nov 24: **3.88% every single day, min = max = 3.88** | **VERIFIED as 0.00** — the number happens to be right; the process finding (no baseline in output) stands |
| F2 — DFF is the wrong series | DFF 3.88 | FRED EFFR 3.88, Nov 24 — identical level today | No material discrepancy in the level; finding noted, not load-bearing today |
| F3 — curve-slope unit mix | `spread_10y_2y_points: 28.00`, `curve_slope: 0.035000` | Independent: 4.91 − 4.63 = **+28bp** | **CONFIRMED LIVE — do not cite `curve_slope`.** 0.035 equals neither 0.28 (pp) nor 28 (bp). The 28.00 spread figure agrees with the independent calc; the slope field does not |
| F4 — as_of defaults to wall clock | `as_of: 2026-11-25` | Latest FRED obs in the pull are **Nov 24** | as_of is the run date, not the data date. All figures below are data-as-of Nov 24 (indicators as noted) |
| F5 — DGS10 candidate dropped by key typo | DGS10 4.91 | Independent FRED DGS10 Nov 24: **4.91** | Level verified regardless; typo itself not confirmed from this session's output |

### 7.1 Rates table (FACT — FRED via module, independently verified; data as-of Nov 24)

| Series | Read | Prior session(s) | Change |
|---|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 3.88% Nov 21–23 | 0.00 — flat 60+ days |
| Treasury 2Y (DGS2) | **4.63%** | 4.63% Nov 20, 23; 4.76% Nov 19 | Flat 3 sessions; −13bp since Nov 19 |
| Treasury 10Y (DGS10) | **4.91%** | 4.92% Nov 20, 23; 5.04% Nov 19 | −1bp d/d; −13bp since Nov 19 |
| **2s10s slope (independent calc)** | **+28bp** | +29bp Nov 20 & 23; +28bp Nov 19 | **Essentially flat, −1bp d/d; upward-sloping, no inversion** |
| SOFR | **3.94%** | 3.92% Nov 23, 20; 3.91% Nov 19 | +2bp d/d |
| EFFR / OBFR | **3.88% / 3.88%** | Flat | — |
| **SOFR–EFFR funding spread** | **+6bp** | +4bp Nov 23 | Narrow; no funding stress (INFERENCE) |

Module shape call "UPWARD_SLOPING" agrees with the independent +28bp. Target range 3.75–4.00% (FACT, Oct 28 FOMC hold, federalreserve.gov).

### 7.2 Core-indicator table — today's read + broker POV

| Indicator | Trigger rule | Today's read (source, as-of) | Call | Broker POV — discount rate / margin of safety |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA) | HIKE if y/y > 2.5% or m/m > +0.25% | **Oct y/y +3.3% (cons 3.2%, Sep 3.1%), m/m +0.3% (cons 0.3%)**; index 131.312 vs Sep 130.929 (Sep revised UP from 130.902). BEA release Nov 25, 8:30 ET; Econoday consensus. **Re-anchor: HOTTER, not softer** | **HIKE** | Anchor the discount rate to the higher regime. The decision variable rose and consensus missed low — no re-anchor down. The §7.4 tripwire (m/m ≤ +0.15% with a downward Sep revision) did NOT fire on either leg. |
| Breakevens (T5YIE / T10YIE, FRED) | HIKE if > 2.75%; CUT if < 1.75% | **2.11% / 2.12%, Nov 24** (was 2.31% / 2.24% Nov 12) | NEUTRAL | Anchored and falling ~20bp since Nov 12: no credibility crisis, room for 25bp, not a forced 50bp. Tripwire remains a break above 2.75%. |
| Michigan expectations (U-M, manual) | HIKE if yr-ahead > 3.5% | **FINAL Nov yr-ahead 3.7%** (prelim 4.3%, Oct 4.7%), rel. Nov 20; 5–10yr 3.3% (Oct 3.5%). FRED MICH cross-check: Oct 4.7 — lagging as usual, confirms the lag, not the level | **HIKE** | Still fires, but barely: one more 0.2pp down flips this line to NEUTRAL. The household-vs-market gap narrowed hard (3.7% vs 2.11% breakeven, from 4.3% vs 2.24%) — the credibility-gap argument is weakening even as the trigger still fires. Do not average with breakevens. |
| Payrolls, 3-mo avg (PAYEMS, BLS/FRED) | HIKE if > +150k; CUT if < +50k | **+137k** (Oct +165k, Sep +60k, Jul +186k; levels Oct 159,293k). No new print since the Oct report | NEUTRAL | Rule as written: NEUTRAL. One +165k print does not override the average. |
| Initial claims, 4-wk avg (ICSA, DOL/FRED) | CUT if > 300k; NEUTRAL < 250k | **196k** (w/e Nov 21: 189k, new; Nov 14: 202k; Nov 7: 202k; Oct 31: 191k) | NEUTRAL | No action. Claims are drifting DOWN, away from the 300k tripwire. Check every Thursday — it turns first. |
| Job openings (JTSJOL, BLS/FRED) | HIKE if 3-mo change positive | **7,523k, Sep 2026** (Jul 7,335k → Sep +188k). No new print (Oct JOLTS not yet released) | HIKE | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA/FRED) | HIKE if > 2.5% ann.; CUT if < 1.0% | **Q3 second estimate +4.3% annualized** (advance 3.4%, cons 3.5%), BEA Nov 25; revised up 0.9pp on investment + consumption; consumer spending 4.2% (adv 3.8%); GDP deflator 1.8% (exp 2.3%). FRED levels confirm: 24,665.201 vs 24,408.011 = +4.28% ann. | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Note the split: growth revised UP while the deflator revised DOWN — real strength, less price pressure — which argues for 25bp, not 50bp. |
| Housing starts (HOUST, Census/FRED) | CUT if −5% over 3 months | **Oct 1,309k** (Sep revised 1,221k → 1,191k); Jul→Oct **−4.4%**; Oct +9.9% m/m | NEUTRAL | Confirms the Nov 18 flip: the −5% CUT tripwire no longer fires. Single-month rebound, 3-mo trend still negative — NEUTRAL, not HIKE. The strongest hold argument in the set has faded. |
| HY OAS (BAMLH0A0HYM2, ICE BofA/FRED) | CUT if > 5.00%; NEUTRAL < 4.00% | **3.72%, Nov 24** (3.63% Nov 23; 3.20% Nov 12) | NEUTRAL | No stress at the level, but **+52bp widening since Nov 12** is the largest move in the set — watch. A break above 5.00% is the tripwire; at the current pace that is not imminent (INFERENCE). |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening / hawkish language | Oct 28: held 3.75–4.00%, **10–2, Cook + Hammack dissenting for +25bp**; statement: "Inflation remains elevated." Nov 18 minutes already digested Nov 23. No new guidance verified this session | **HIKE** | Weight the vote above any single print: two dissents for an immediate hike is the Committee stating its lean. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL — unchanged from Nov 23.**

### 7.3 Market pricing vs the indicator read

- **Kalshi, direct API pull Nov 25 ~13:30 PT (Dec-2026 meeting, `KXFEDDECISION-26DEC`)**: 25bp hike **$0.93** (bid/ask 0.92/0.93, 24h vol 193k, OI ~2.96M); more than 25bp **$0.03** (0.02/0.03, vol 501k); hold **$0.06** (0.05/0.06, vol 1.16M); cuts $0.01 each. Total hike $0.96. **Unchanged from Nov 23 ($0.93 / $0.03)** — the hot core PCE print moved nothing in Kalshi's Dec pricing by midday PT. The >25bp tail has collapsed from $0.12 (Nov 13) to $0.03.
- **CME FedWatch (secondhand — CME's own tool not directly readable; converging reads)**: ~**96% for 25bp, ~4% hold, ~0% for >25bp** (FrenzyCap replication of FedWatch methodology from /ZQ futures, live Nov 25 12:26 PM ET: 96% / 4% / 0%, expected +24bp, EFFR after 4.120%; FXStreet/Biggo ~96–97%). Intraday wobble around the PCE print per FX Empire (97.8% pre-print → 95.8% after) — secondhand, direction unclear; the level is what matters: ~96%.
- **Agreement**: markets and indicators agree on direction (25bp hike) and now agree on size too — the tail is small on both venues. The Nov 13 disagreement (markets pricing a $0.12 tail the indicators could not justify) is gone. No material disagreement to name today. Jan 2027 is the live question: Kalshi Jan H25 $0.54 vs hold $0.46 — a coin flip (FACT, same pull); FedWatch-derived reads put a Jan hike ~56–60% (secondhand, FXStreet).
- **NVDA governance note (rates relevance only)**: the Nov 23 reinstatement rally (+32% to ~$166) loosened financial conditions into the meeting (press framing: "muddied the December call"); it changes no Desk 7 trigger. The counter-signal is HY OAS widening +52bp since Nov 12 — credit, not equities, is where any tightening-by-markets would show, and it is not showing stress yet (INFERENCE).

### 7.4 Verdict — thesis / evidence / what would change it

- **Thesis**: 25bp hike on Dec 9. **Holds.**
- **Evidence**: Core PCE re-anchored hotter (y/y 3.3% vs 3.2% cons, up from 3.1%; m/m +0.3% still above the +0.25% trigger); Q3 GDP revised up to +4.3%; the Oct 28 vote already leans hike (10–2 with two hawkish dissents); markets price it at 96% / $0.93. The two dovish-leaning moves — Michigan final expectations falling to 3.7% and breakevens to ~2.11% — narrow the case for 50bp, they do not touch the case for 25bp. Housing's CUT signal is gone.
- **What would change it**: (a) November core PCE (Dec 23) is after the decision — cannot change December; (b) initial claims 4-wk avg above 300k — currently 196k and falling; (c) a named speaker arguing for a hold, or the Dec 9 statement softening — none verified this session; (d) Michigan yr-ahead falling below 3.5% would flip one HIKE line to NEUTRAL but would not alone overturn a 5–0 tally with markets at 96%.

### 7.5 Graham lens (arithmetic from verified yields)

10Y 4.91% (Nov 24) vs 4.98% (Nov 10) vs 4.86% (Nov 6). At assumed perpetual growth g = 3.00%, Gordon multiple 1 ÷ (r − g): **52.36x today** (1 ÷ 0.0191), up from 50.51x at 4.98% — the 7bp fall in the 10Y since Nov 10 re-inflated the multiple ~3.7%. **Re-anchor the discount rate to 4.91%.** Duration ≈ 8 puts the −7bp move at about +0.56% on a 10-year position (approximation, ignores convexity). The margin of safety is slightly wider than Nov 10 on the bond side alone — but the bond side still pays ~4.9% on a contractual claim, so equity risk must be compensated from price; a wider required discount, not a chase for yield. Earnings-yield vs bond-yield spread: UNVERIFIED (no S&P earnings-yield figure from a primary source this session; no spread asserted).

### Sources
- FRED (fred-public CSV via `rates_desk.rates_environment()`, module run this session; independently re-pulled via `fred_observations.py`): DFF, DGS2, DGS10, SOFR, EFFR, OBFR, PCEPILFE, T5YIE, T10YIE, MICH, PAYEMS, ICSA, JTSJOL, GDPC1, HOUST, BAMLH0A0HYM2 — data as-of Nov 24 (monthly/quarterly series as noted).
- BEA, Personal Income and Outlays, October 2026 (released Nov 25, 8:30 ET): https://bea.gov/news/2026/personal-income-and-outlays-october-2026 ; BEA, GDP Second Estimate Q3 2026 (released Nov 25): https://bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-3rd-quarter-2026
- Econoday consensus table (core PCE m/m 0.3% cons, y/y 3.2% cons) via Fidelity Econoday.
- U-M Surveys of Consumers, final November results (released Nov 20): yr-ahead 3.7%, 5–10yr 3.3%, sentiment 51.5 — corroborated across U-M release coverage (TheStreet, Kitco, TradingView/dpa, InvestingLive).
- Kalshi trade API v2, `KXFEDDECISION` series, direct pull Nov 25 ~13:30 PT.
- CME FedWatch: secondhand converging reads (FrenzyCap /ZQ replication, FXStreet, Biggo) — labeled as such; CME tool itself not directly readable.
- Desk 7 consolidated deliverable: ~/workspace/hedge-desk-research/desk7-core-indicators.md (Nov 13 snapshot; today's reads supersede it line by line above).

---

## Run notes / reconciliation

- **Cross-desk price consistency checked:** Premium desk spot closes (13:35 PT: SPY 716.70, QQQ 633.93, AAPL 355.58, MSFT 489.93, NVDA 149.30, TSLA 380.14) agree exactly with Dividend desk prices (~13:28 PT). Day moves vs Nov 24 closes (SPY 718.78, QQQ 638.10, AAPL 354.07, MSFT 496.13, NVDA 155.38, TSLA 384.68 — Nov 24 package): SPY −0.29%, QQQ −0.65%, AAPL +0.43%, MSFT −1.25%, NVDA −3.91%, TSLA −1.18% — arithmetic from the two closes named.
- **Earnings (no watchlist earnings in window) agrees with Premium (no earnings binary in window; Nasdaq calendar sweep 45 days, zero hits).** Next-earnings dates updated from today's direct Yahoo read: MSFT/TSLA Jan 27, AAPL Jan 28, 2027; NVDA Feb 24 stays UNVERIFIED (third-party estimate only). Yesterday's TipRanks Feb 3/4 figures not re-verified, not carried forward.
- **Desk 7's 25bp call (Kalshi $0.93, FedWatch ~96%) agrees with the Futures desk's core-PCE read** (hot print confirms Tuesday's gold fade; Dec hike "almost fully priced"). The Jan 2027 hike is the live open question on both desks (Kalshi Jan $0.54 vs hold $0.46; FedWatch-derived ~56–60%).
- **Brent level is the one unresolved cross-source spread, now wider:** wire settlement $94.61 (Dow Jones/Morningstar + Rigzone) vs Yahoo BZ=F $90.74; gold spot wires ~$3,469–$3,486 vs Yahoo GC=F $3,601.10. Wire levels used; Yahoo BZ=F/GC=F flagged discrepant, not used as settled levels. The Yahoo gap itself is UNRESOLVED.
- **IV window flip stands:** SPY/QQQ not contingent (Nov 5 share diluted below 30% by the Nov 23 jump day); AAPL/MSFT/NVDA/TSLA formally WINDOW-CONTINGENT. First clean realized read lands in the Dec 1 file, after Nov 5 ages out Nov 28.
- **Correction carried:** Michigan Nov final 3.7% (not the 4.3% prelim) is the live Desk 7 read. QQQ Dec 21 amount/pay date remain UNVERIFIED (now four-way pay-date dispute). IV rank UNVERIFIED all six (no free IV-history source). CME FedWatch direct read unavailable (secondhand range only). Jobless claims exact print not independently verified — not asserted.
- **Sentry W48 rates findings:** F1 verified (fed-funds change 0.00 is correct; DFF flat at 3.88% for 65 obs), F3 confirmed live (do not cite `curve_slope` 0.035; use the independently computed +28bp spread), F2/F5 levels verified (EFFR 3.88, DGS10 4.91), F4 noted (module as_of is run date, data is Nov 24). The Desk 7 section above carries the verified figures, not the module's slope field.
- **No desk failed.** All seven reported. No retry was needed. One telemetry note: the Quant leg's run recorded a single nonzero exec exit in its sub-process log, but the sweep completed, all 9 candidates were scored, and the ledger append was verified on disk (ends #360).
- **Desk-failure / recovery log:** none this run.

## Sources (by desk)

- Earnings: api.nasdaq.com/api/calendar/earnings (15 daily calls Nov 25–Dec 9); Yahoo v10 quoteSummary (cookie+crumb); Zacks; TipRanks (NVDA date, UNVERIFIED).
- Dividend: Nasdaq dividends calendar API (29-date sweep); Yahoo v8 chart / quoteSummary; NVIDIA Q3 FY27 release (GlobeNewswire, Nov 17); State Street 2026 distribution schedule via Dividend Vision; TipRanks / DripCalc / DividendMax / FI Handbook / DivTrkr / Dividend101; ~/workspace/hedge-desk-research/dividend-count-standard.md.
- Premium: ~/workspace/hedge-desk-research/nightly/2026-11-25-iv-inputs.json (as_of 2026-11-25T07:54:49-07:00, FRESH within 26h guard); Yahoo v7 options chain (cookie+crumb), as_of 2026-11-25T13:35 PT; Yahoo v8 chart; Nasdaq earnings calendar API; raw live pull /tmp/iv_live_2026-11-25.json.
- Quant: arXiv q-fin listing Nov 23–24; SSRN; hedge_desk.research_intelligence.assess_source; ~/workspace/hedge-desk-research/quant-lab-ledger.md (#352–#360).
- Futures: EIA petroleum status 10:30 ET + gas storage 12:00 ET via Reuters/WSJ/Oilprice/Energy Edge/Seeking Alpha; BEA Personal Income & Outlays / Q3 GDP 08:30 ET via Reuters/FXStreet/KPMG; ICE Brent/WTI settlements via Dow Jones/Morningstar + Rigzone; spot gold Reuters/Kitco/FXStreet/Ausecure; Gulf/Hormuz Reuters via Barchart/FinanceFeeds; USTR via Reuters/JD Supra; USDA ERS/FAS Nov 24 + inspections Nov 23 + DTN; Yahoo v8 chart (BZ=F/CL=F/GC=F/NG=F, discrepant — flagged).
- Parity: SEC SRO rulemaking SR-CBOE-2026-087 (Nov 24); fxnewsgroup.com Cboe news; nyasekai.com box-spread test (Nov 23); cboe.com notices id 62439 / 61537; S&P DJI methodology (Oct 28 overhaul, already known).
- Rates: FRED (16 series) via repo module + fred_observations.py (independent re-pull); BEA Personal Income & Outlays Oct 2026 + GDP Second Estimate Q3 2026; Econoday consensus; U-M Surveys of Consumers final Nov 2026; Kalshi trade API v2 (KXFEDDECISION-26DEC); federalreserve.gov; FrenzyCap / FXStreet / Biggo (FedWatch secondhand).
