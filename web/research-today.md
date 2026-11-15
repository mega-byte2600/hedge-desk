# Hedge-Desk Daily Research — Sun 2026-11-15 (13:30 PT)

**Scope:** Watchlist SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Prices/options as of Fri 2026-11-13 close (last trading session); markets closed Sat–Sun. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; SPECULATION = untested hypothesis; UNVERIFIED = looked, could not confirm. Paper-only research; no Risk of Ruin, no trade authorization. Government-data rule stands: no federal shutdown (CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11); federal releases ran on schedule this week.

## Headline: the 3–5 most decision-relevant items

1. **NVDA earnings Tue Nov 17 after close — the only watchlist event in the next two weeks.** Options imply ~9.6% (Nov 20 weekly ATM straddle) vs a 4.53% average absolute earnings-day move over the last 4 quarters — ~2.1× history. The cleaner Nov 18 straddle implies 8.6%. Premium into this binary event = avoid. **Correction to yesterday's package:** the signed average of the last 4 earnings-day moves is **+0.23%**, not −0.02% as printed Nov 14 (−3.15 −5.46 +0.78 +8.74 = +0.91 ÷ 4). No directional bias either way. (FACT, Nasdaq calendar API + Yahoo; INFERENCE on expensiveness.)
2. **Hormuz escalated over the weekend; crude has not repriced yet — Monday's open is the test.** IRGC claims a supertanker sank after a mine strike Sun Nov 15 (SPECULATION — no vessel name, flag, or imagery; no independent confirmation). UKMTO Warning 205-26 confirms a tanker was attacked in the Arabian Gulf before entering the Strait, crew safe (FACT the warning exists; cause and any link to the mine claim UNVERIFIED). Houthis' 4th Riyadh attack in 6 days was intercepted early Sun (FACT, coalition via Reuters). Friday's crude close was flat (WTI $88.56, Brent $95.84) — the paper market is still pricing the IEA/OPEC supply-restoration story over the shipping-risk story. A confirmed sinking or a hit on a US-escorted vessel would flip that read overnight.
3. **Desk 7 unchanged: 25bp hike call for Dec 9; 10Y at 5.10%.** FRED pull this session: the Nov 13 DGS obs has still not posted — 10Y 5.10% and 2Y 4.86% are Nov 12 obs, unchanged from yesterday. Tally 5 HIKE / 1 CUT / 4 NEUTRAL, unchanged. Kalshi total hike $0.99 (was $1.00 Nov 13). New: five more hawkish speaker remarks Thu–Fri (Collins, Goolsbee, Daly, Williams, Hammack) — weekly count now 12 hawkish / 0 dovish. Graham lens: re-anchor to 5.10%; Gordon multiple −5.72% on the week.
4. **No clean IV-vs-realized verdict anywhere — all six windows WINDOW-CONTINGENT.** The Nov 5 crash day drives 37–54% of 20-day realized variance, above the 30% threshold. IV-inputs file passed the 26h guard (as_of 2026-11-14T14:54:31−07:00) and its ATM IVs are populated this time — the null streak is broken. Live supplement: NVDA 103.43% ATM IV at Nov 18 expiry (earnings hump, +42.8pp over Nov 16); all other front-end IVs unremarkable.
5. **MSFT goes ex-dividend Thu Nov 19 at the new $0.98 rate** — first cash payment of the 24th consecutive annual increase, payable Dec 10, confirmed three ways (Nasdaq + Yahoo + Microsoft newsroom). AAPL's $0.27 payment lands Mon Nov 16 but its ex-date (Nov 12) is already past. NVDA's next declaration is undeclared — the window opens with its Tue Nov 17 earnings release, which on pattern is where the declaration would appear.

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

**FACT:** NVDA is the only watchlist name reporting in the next two weeks. Nasdaq and Yahoo agree on Tue 2026-11-17 after close; Yahoo flags it as a confirmed (non-estimate) date (`isEarningsDateEstimate: false`). Nasdaq calendar scan of every trading day Nov 16–25 and Nov 27 returned no other watchlist name (Nov 26 is Thanksgiving, market closed; Nov 28 is Saturday). All quotes below are the Fri Nov 13 close — markets closed Sat–Sun.

### NVDA straddle detail (Yahoo v7 options, Fri Nov 13 close, underlying $162.85)

| Expiry | ATM 162.5 straddle mid | Implied move | ATM IV |
|---|---|---|---|
| Wed 2026-11-18 (1 day post-earnings) | $14.05 (call 7.10/7.30 + put 6.80/6.90) | **8.63%** | ~103% |
| Fri 2026-11-20 (weekly) | $15.70 (call 8.05/8.05 + put 7.60/7.70) | **9.64%** | ~94% |

**FACT:** Both straddles are essentially unchanged from yesterday's read (~8.6% / ~9.6%) — no repricing over the weekend, as expected with markets closed. The Nov 18 straddle is the cleaner event read (one day post-earnings); the Nov 20 weekly carries two extra non-earnings days of vol.

### NVDA historical earnings-day moves (Yahoo v8 chart daily closes, report-day close → next trading-day close; recomputed this session)

| Quarter | Reported (after close) | Move |
|---|---|---|
| Q3 FY26 | 2025-11-19 | −3.15% ($186.52 → $180.64) |
| Q4 FY26 | 2026-02-25 | −5.46% ($195.56 → $184.89) |
| Q1 FY27 | 2026-05-27 | +0.78% ($212.60 → $214.25) |
| Q2 FY27 | 2026-08-26 | +8.74% ($209.66 → $227.98) |

**FACT:** Average absolute move over the last 4 quarters = **4.53%** (confirmed, identical to yesterday). **Correction to yesterday's package:** the signed average is **+0.23%**, not −0.02% as printed 2026-11-14 (−3.15 −5.46 +0.78 +8.74 = +0.91 ÷ 4). 2 down, 2 up — no directional bias either way. Only the Aug 2026 move (+8.74%) approached the currently implied move.

**Verdict (INFERENCE):** The options market prices ~2.1× the recent realized average (9.64% Nov 20 weekly; 8.63% on the cleaner Nov 18 read). The straddle buyer pays for a move NVDA delivered once in four quarters. Through a value lens, that is expensive insurance, not a mispricing to chase. Premium into this binary event = avoid.

**What would change it:** A Q3 guide materially above the $108.73B revenue consensus bar would validate the elevated premium; a straddle repricing below ~6% on Monday would close the gap to history. Reassessment waits on the release itself — guidance vs consensus first.

**Earnings-release teardown (last 48 hours):** None required — no watchlist name reported Nov 13–14 (Nasdaq calendar API, 205 rows on Nov 13, zero watchlist hits). Last reports: TSLA Oct 22, MSFT Oct 29, AAPL Oct 30, NVDA Aug 26.

**UNVERIFIED / gaps:** Straddle prices are Fri Nov 13 close; Monday's open may reprice them materially. Historical moves computed from unadjusted Yahoo daily closes; the four report dates were taken as NVDA's reported schedule, not re-verified against SEC EDGAR this session. Consensus gap Nasdaq $2.49 vs Yahoo $2.47 is trivial.

---

## 2. Dividend Opportunity desk

**Question:** Which watchlist names go ex-dividend in the next 4 weeks (through Sat Dec 12, 2026), and is there any announced increase, cut, or special?

### Upcoming ex-dividend dates (next 4 weeks)

| Symbol | Ex-date | Pay date | Amount | Yield* | Flag | Consec. increases† | Source | As-of |
|---|---|---|---|---|---|---|---|---|
| **MSFT** | **Thu Nov 19, 2026** | Dec 10, 2026 | $0.98/qtr | 0.75% | **INCREASE — Sep 15, 2026 raise, $0.91 → $0.98 (+7.7%)** | **24** | Nasdaq calendar API + Yahoo quoteSummary + Microsoft newsroom (agree exactly) | Nov 15, 2026 |
| AAPL | Nov 12, 2026 (passed) | **Mon Nov 16, 2026** | $0.27/qtr | 0.30% | No change — Nov 2 declaration held $0.27 flat after record Q4 | **14** | Yahoo quoteSummary + Zacks + AppleInsider | Nov 15, 2026 |
| NVDA | None declared | — | $0.25/qtr (current rate) | 0.61% | **WATCH: declaration expected with Nov 17 earnings release** (pattern); forecast ex-dates Dec 3–17, all estimates, none declared | 1 (see note) | Zacks (Nov 2) + TipRanks + Yahoo quoteSummary; forecasts: DividendMax / Investingly / Optionistics | Nov 15, 2026 |
| SPY | None in window | — | ~$1.89/qtr (variable) | 1.01% TTM | None; Dec quarterly ex-date falls ~Dec 18–19, outside window | N/A (ETF) | Yahoo chart dividend events (last ex Sep 18, 2026, $1.889) | Nov 15, 2026 |
| QQQ | None in window | — | ~$0.75/qtr (variable) | 0.45% TTM | None; Dec quarterly ex-date falls ~Dec 22, outside window | N/A (ETF) | Nasdaq quote dividends API + Yahoo chart (last ex Sep 21, 2026, $0.75143) | Nov 15, 2026 |
| TSLA | None — pays no dividend | — | $0.00 | 0.00% | None | N/A | Yahoo quoteSummary (yield 0.00%, trailing $0.00) | Nov 15, 2026 |

\* Yields calculated (INFERENCE): annualized current rate ÷ Fri Nov 13 Yahoo close (MSFT $523.88, AAPL $356.27, NVDA $162.85, SPY $754.37, QQQ $679.89). SPY/QQQ use trailing-4-distribution sums from Yahoo chart dividend events ($7.583 / $3.091), cross-checked for QQQ against Nasdaq.
† Per `~/workspace/hedge-desk-research/dividend-count-standard.md`: count increments on the announcement date; a year with no announced increase breaks the streak.

**Material findings:**
1. **MSFT ex-date Thu Nov 19 stands — confirmed three ways. FACT.** Nasdaq calendar API (Nov 19 row: $0.98, pay Dec 10, record Nov 19, announced Sep 15, 2026), Yahoo quoteSummary (ex Nov 19, pay Dec 10, dividendRate $3.92, yield 0.75%), and the issuer's own newsroom (Sep 15, 2026: "$0.98 per share, reflecting a 7 cent or 8% increase… payable Dec. 10, 2026, to shareholders of record on Nov. 19, 2026. The ex-dividend date will be Nov. 19, 2026"). First payment at the raised rate; defining event of the 24th consecutive annual increase (initiated 2003). **Data conflict flagged, no drift:** Nasdaq's `indicated_Annual_Dividend` still shows $3.64 (= 4 × $0.91, old rate) while its `dividend_Rate` shows $0.98 — the indicated-annual field is stale; $3.92 annualized is correct. MarketBeat's compare table shows "23 Years" for MSFT — a stale third-party count that has not picked up the Sep 2026 raise; per the desk standard the count is **24**. Do not copy the 23.
2. **AAPL's $0.27 payment lands Mon Nov 16; ex-date (Nov 12) is past — no capture left. FACT.** Declared Nov 2, 2026 alongside record Q4 earnings; rate held flat at $0.27 (AppleInsider, Zacks). 2026 raise was Apr 30, 2026 ($0.26 → $0.27, +3.8%). Count 14 consecutive annual increases per the desk standard — corroborated by MarketBeat's "14 Years" this run (last run's ChartRow "12" discrepancy does not recur in the sources checked today).
3. **NVDA still undeclared — but the declaration window opens Tue Nov 17. FACT (undeclared) / INFERENCE (timing).** Zacks (updated Nov 2): "does not have any future dividends declared"; TipRanks: "no upcoming dividends"; Yahoo quoteSummary still shows last ex Sep 10, 2026 / pay Oct 1, 2026, dividendRate $1.00. Nasdaq calendar scan Nov 16–Dec 12 returned no NVDA row. **The pattern to watch:** in 2026 NVDA announced each dividend in its quarterly results release (Feb 25: $0.01; May 20: raise to $0.25; Aug 26: Oct 1 payment). It reports Q3 FY27 **Tue Nov 17 after close** — the declaration, if it follows pattern, lands with that release. Tracker forecasts for the ex-date disagree and are all estimates, not declarations: DividendMax forecasts declaration Nov 18 / ex Dec 3 / pay Dec 24; Investingly ~Dec 10; Optionistics Dec 11 (explicitly "estimated… company has not declared it yet"); StockLrn Dec 17 (estimated from past payout interval). Prior Dec ex-dates: Dec 5, 2024 and Dec 4, 2025. **If declared Nov 17, the ex-date likely falls inside this window (early Dec) — the next run's first check.** Streak stays 1 consecutive annual increase (the $0.01 rate was flat from the Jun 2024 split rebase through Mar 2026; the May 18, 2026 raise to $0.25 starts a new run). MarketBeat corroborates "increasing its dividend for 1 years."
4. **No cuts, no specials, no suspensions anywhere on the watchlist. FACT.** Nasdaq calendar scan of every trading day Nov 16–Dec 12 returned only the MSFT row among watchlist names; no new board action surfaced in the Nov 2026 dividend-announcement search for any watchlist name. (Nov 26, Dec 9, Dec 12 returned empty Nasdaq calendars — Thanksgiving and no-dividend days, not data failures.)
5. **SPY/QQQ December distributions fall outside the window. INFERENCE from pattern, UNVERIFIED as declared dates.** Neither appears in Yahoo calendarEvents or the Nasdaq calendar scan. Pattern: SPY Dec ex-dates Dec 19, 2025 / Dec 20, 2024; QQQ Dec 22, 2025. **Yahoo data-quality note:** Yahoo quoteSummary's `trailingAnnualDividendRate` for these ETFs ($5.66 SPY / $1.77 QQQ) is wrong against its own dividend-event feed — the event-derived trailing-4 sums are $7.583 (SPY) and $3.091 (QQQ), cross-checked for QQQ against Nasdaq's dividend history ($0.79408 + $0.73282 + $0.81349 + $0.75143 = $3.09182). Yields above use the event-derived sums; do not use Yahoo's trailing field for SPY/QQQ.

**Verdict:** Thin week for dividend action, unchanged from yesterday: the only live event is MSFT going ex Thu Nov 19 at the new $0.98 rate — first cash payment of the 24th consecutive annual increase, payable Dec 10. AAPL's payment lands Mon Nov 16 but the ex-date is past. The one thing to watch is NVDA's Nov 17 earnings release, which on pattern is where the next declaration would appear; if declared, the ex-date likely lands in early December, inside the window. Nothing here changes a margin-of-safety read: yields run 0.30%–1.01%, and the NVDA raise, while 25× in percentage terms, is $1.00/year against a $162.85 share price.

**What would change it:** an NVDA declaration with the Nov 17 earnings release (date + any further rate change); a declared SPY/QQQ December ex-date moving inside the window; any board action altering MSFT's Dec 10 payment before Nov 19.

**UNVERIFIED / gaps:** NVDA's next ex-date and amount (undeclared; all tracker dates are estimates); SPY/QQQ December ex-dates (not declared); MSFT's Nov 19 ex-date is confirmed, but Monday's open could still in principle carry a corporate-action change — none is indicated.

---

## 3. Overnight Premium desk (IV)

**Question:** Is front-end implied vol rich or cheap versus recent realized vol on the watchlist, and is any premium sitting inside a binary event?

**Freshness guard — PASS (within 26h):** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-14-iv-inputs.json`, `as_of` **2026-11-14T14:54:31−07:00**, age ~22.6h at run start — inside the 26h guard. **Null streak broken:** ATM IVs are populated for all six symbols this time (the Nov 13 file's nulls are gone). Raw live pull saved to `~/workspace/goals/hedge-desk-daily-research/hidden_files/live_iv_2026-11-15.json`.

**Live supplement — LABELED LIVE, Yahoo v7 options (cookie+crumb), pulled 2026-11-15 13:29 PT.** Markets closed Sunday; all quotes are the **Friday Nov 13 close** (16:00 ET) — no live Sunday session exists. Zero pull failures. Nearest unexpired expiry is Nov 16 (1 DTE Monday); next expiry Nov 17 (SPY/QQQ) or Nov 18 (single names).

### IV snapshot

| Symbol | File ATM IV (STALE, Nov 14 pull, Nov 16 exp, 2 DTE) | Live ATM IV Nov 16 (1 DTE) | Live ATM IV next exp | Realized 20d (STALE, Oct 19–Nov 13) | Max 1-day var share |
|---|---|---|---|---|---|
| SPY | 11.77% | 14.42% | 16.29% (Nov 17) | 22.83% | 54.4% |
| QQQ | 20.72% | 25.37% | 29.25% (Nov 17) | 36.50% | 46.5% |
| AAPL | 15.34% | 18.78% | 22.06% (Nov 18) | 28.24% | 46.3% |
| MSFT | 21.22% | 25.99% | 32.24% (Nov 18) | 37.35% | 41.9% |
| NVDA | 49.06% | 60.61% | **103.43% (Nov 18)** | 54.48% | 36.9% |
| TSLA | 36.68% | 44.92% | 50.34% (Nov 18) | 61.48% | 47.8% |

*Sources: file values from `2026-11-14-iv-inputs.json` (FACT, STALE — yesterday's pull); live values from Yahoo v7 options chain, Fri Nov 13 close (FACT). Underlyings at Fri close: SPY 754.37, QQQ 679.89, AAPL 356.27, MSFT 523.88, NVDA 162.85, TSLA 390.22.*

**IV-vs-realized verdict — WINDOW-CONTINGENT for all six (no clean verdict).** FACT: every ATM IV above sits below its 20-day realized vol. INFERENCE blocked from a clean verdict: every window is WINDOW-CONTINGENT — a single day drives 37–54% of 20-day variance (the Nov 5 crash day), above the 30% desk threshold. The realized vols are jump-inflated, so "IV below realized" does **not** cleanly mean premium is cheap. What would change it: the window rolling past Nov 5 (after ~Dec 3) or a fresh 20-day window with no single day above 30% of variance.

**IV-rank — UNVERIFIED for all six.** No free IV-history source is available, and no 52-week IV rank can be computed from Yahoo point-in-time IVs. Never guessed. Absolute levels: NVDA and TSLA are elevated in absolute terms (NVDA 60–103%, TSLA 45–50%); whether that is elevated *for them* is UNVERIFIED without history. MSFT 26–32% is high in absolute terms for a mega-cap but likewise rank-UNVERIFIED.

**Elevated-IV flags:**
- **NVDA — elevated, but expected, not "rich" (FACT, with INFERENCE):** 60.61% at 1 DTE rising to 103.43% at Nov 18 is a textbook earnings hump — the Nov 18 expiry is the first expiry after the Nov 17 earnings event. Call and put IV agree (103.42% / 103.44%), so the print is not a one-sided artifact. Elevated IV into a known binary event is expected pricing, not a mispricing.
- **TSLA — elevated in absolute terms (44.92% / 50.34%), consistent with its own history (FACT):** its 20-day realized is 61.48%, the highest on the watchlist; no richness claim can be made while its window is contingent.
- **SPY / QQQ / AAPL / MSFT — no elevated-IV flag.** Front-end IVs of 14–32% are unremarkable against their realized vols; SPY and QQQ show steep downside skew (put IV well above call IV: SPY 18.24% vs 10.60% at 1 DTE; QQQ 30.60% vs 20.14%) — FACT, consistent with normal equity skew after a down week, not a standalone signal.

**Earnings-in-window warning — NVDA, Nov 17.** NVDA reports 2026-11-17, inside the Nov 18 expiry window — that is exactly what the 103.43% print is pricing. **Premium into this binary event = avoid** (front-week premium selling on NVDA). Date corroborated by the Earnings desk (Nasdaq calendar API + Yahoo calendarEvents); the IV hump itself corroborates an event inside the Nov 18 window (INFERENCE, strong: +42.8 vol points Nov 16 → Nov 18 cannot be explained by 2 extra days of ordinary term structure). No other watchlist name has earnings in the window.

**Sanity checks:** Term structure upward-sloping (contango) for all six — no inversion (FACT, live pull). Put skew present everywhere (OTM put IV ~5% below strike minus OTM call IV ~5% above): QQQ steepest at +12.55pp (Nov 16) / +15.04pp (Nov 17), MSFT +10.64pp, SPY +5.76pp, NVDA +5.66pp, AAPL +6.45pp, TSLA +6.74pp (FACT, live pull). Open interest corroborates put demand: QQQ Nov 17 ATM put OI 5,739 vs call 434; SPY Nov 16 put OI 1,285 vs call 675 (FACT, live pull). Stale-quote caveat (FACT): Sunday pull on Friday-close marks. Two crossed quotes observed — NVDA Nov 16 call bid 3.10 > ask 3.00; TSLA Nov 16 call bid 5.20 > ask 5.15 — stale-mark artifacts. ATM IVs come from Yahoo's solver IVs, not those marks, but treat the 1-DTE prints as close-marks, not live quotes. Put-call parity not independently verified this run (no rate/dividend inputs pulled); no parity violation is asserted.

**Data-quality flags:** Same-expiry IV moved between pulls: SPY Nov 16 ATM IV was 11.77% in the Sat Nov 14 pull and 14.42% in today's pull, on the same Friday close and same expiry (FACT). Cause is UNVERIFIED — likely Yahoo IV-solver refresh / strike-selection noise at 1–2 DTE. At 1 DTE, small premium changes move IV a lot; do not over-read single-print moves this close to expiry (INFERENCE). 1-DTE noise warning: Nov 16 is 1 DTE on Monday; all Nov 16 IVs are hyper-sensitive to Friday's closing prints and will reprice hard at Monday's open. Nothing in this snapshot is a Monday-morning quote (INFERENCE).

**UNVERIFIED / gaps:** IV rank / IV percentile for all six (no free history source); cause of the SPY Nov 16 IV revision between the Nov 14 and Nov 15 pulls; no fresh calendar check re-run by this desk — the Earnings desk's read governs.

---

## 4. Open Quant/AI Model Lab

**Question:** What new papers, preprints, or methods in the last ~7 days are worth the desks' attention, scored on the repo's own rubric?

**Sweep scope (FACT, arXiv listing read at source 2026-11-15 ~13:30 PT):** arXiv q-fin listing page (`arxiv.org/list/q-fin/new`) — the coverage control per the 2026-11-14 lesson (the API top-40 missed 7 of 19 new items on Nov 13). Listing still shows the **Fri 13 Nov announcement: 19 new + 9 cross-list + 20 replacements**. No new announcement today — arXiv announces weekday-only, and Fri Nov 13 submissions announce **Mon 16 Nov**. Next run re-covers the Nov 13–15 window. GitHub leg SKIPPED per the run brief (no GitHub operations). SSRN leg not run (optional; nothing to chase on a no-announcement Sunday). Scorer: no new candidates, so no scorer runs this cycle (module-scored only, never hand-scored).

### New candidates: NONE

Zero new candidates. Every item on the current listing is already accounted for: all **19 new** submissions are ledgered as candidates **#268–#288** across the Nov 13 and Nov 14 runs (e.g. #285 Gençay 2611.14539, #286 Graeber et al 2611.15747, #287 Zarei et al 2611.14699, #288 Feng et al 2611.10414). All **9 cross-lists** accounted for: 6 ledgered (#273, #276, #278, #279, #280, #285), 3 triage-excluded with no ledger row per the 2026-11-14 note (2611.15017 AI-agent institutions, 2611.16058 worker-firm match, 2611.16095 data-center electricity costs — all out of scope). No candidate rows appended; ledger still ends at **#288 (287 rows)**.

**Ledger append verification:** No candidate appends required (nothing new). The run's re-check record was appended to the Jidoka log at the top of `~/workspace/hedge-desk-research/quant-lab-ledger.md` and verified on disk (entry dated 2026-11-15 present; candidate-row count unchanged at 287, last row #288).

**Re-checks (FACT, arXiv API id_list):** core version-triggered WATCH set #4/#9/#13/#14/#15/#20/#21/#30/#31 — no version movement, all stay WATCH. #25 (Han et al) still v4 (updated 2026-11-10). #257 (2611.13616) now v2 (updated 2026-11-12) — ARCHIVE, no disposition change. The other 18 replacements in the Nov 13 listing were checked against the ledger — none touches a ledgered item.

**Row-text staleness noted (no disposition change):** #30's row still says its v3 "appears in one mirror — UNVERIFIED" — the arXiv API now confirms v3 (updated 2026-09-26). #31's row still says v2 (8 May 2026) — v3 since 2026-10-22, known since the 2026-11-12 re-check. Recorded in the Jidoka log; rows not edited (no disposition change).

**What would change the verdicts:** Mon 16 Nov announcement (Nov 13–15 submissions) landing on the listing — the next run's window; any desk-relevant new paper gets scorer-run and ledgered then. Any version movement in the WATCH set (esp. #25 v5, #31 v4, #9 code release) or a journal-ref/code-link appearing for #4/#13/#14/#15. GitHub leg unban: TEST blockers (#1/#32 license, #3 code/license, #80 sandbox, #24 free-key signup) remain unretried this run.

**Bottom line:** Empty sweep by design — Sunday, no arXiv announcement. Nothing new to score, nothing to append, no TEST/INTEGRATE movement. The Nov 13 window is fully closed (19 new + 9 cross, all ledgered or triage-excluded); the next material input is the Mon Nov 16 announcement.

---

## 5. Weather / War / Logistics Futures Event desk

**Question:** What fresh catalysts moved energy, grain, and shipping futures this week, and what are the curves pricing?

**As-of:** Sun 2026-11-15, ~13:30 PT (futures settles Fri 2026-11-13). No EIA/USDA releases due before Wed Nov 18.

### Catalyst triage — fresh since Fri Nov 13 close

| # | Event | Date/time | What happened | Source | Label |
|---|---|---|---|---|---|
| 1 | **Hormuz: IRGC claims supertanker sank** | Sun Nov 15 (afternoon, Tehran time) | IRGC Navy claimed two tankers on an "unauthorized route" in the southern Strait struck mines; one, a supertanker carrying 2M+ bbl, **sank**; the second left burning. No vessel name, flag, owner, position, or imagery released. | IRGC statement via AFP/Ynetnews; reported by Reuters/AFP | **SPECULATION** — claim only; no independent confirmation of any sinking as of Sun evening |
| 2 | **UKMTO Warning 205-26: tanker attacked in Arabian Gulf** | Sun Nov 15 | UKMTO, citing Indian shipping authorities: a tanker transiting eastbound through the Arabian Gulf **prior to entering** the Strait was attacked; crew accounted for and safe; damage and environmental impact unknown; vessels advised to transit with caution. Cause/weapon not stated; UKMTO does **not** link it to the mine claims or the claimed sinking. | UKMTO alert, via Reuters/Fox News | **FACT** (that UKMTO issued the warning and what it says); cause and any link to event #1 **UNVERIFIED** |
| 3 | **Hormuz: Iran claims 3 tankers hit mines** | Sat Nov 14 | IRGC Navy: two tankers (one a supertanker) exploded/caught fire after striking mines south of the strait; Iran's conventional navy: a third tanker caught fire after striking a mine east of the strait. No names/flags/cargoes given. USCENTCOM dismissed the mine claims as "false" / intimidation. | Iranian state media via Reuters/AFP; USCENTCOM | **SPECULATION** — Iranian claim, explicitly disputed by USCENTCOM, no independent confirmation. Note the pattern: The Red Zone's audit of Oct 23–Nov 10 found Iran claimed 41 mine strikes on 19 days while **zero** of 16 UKMTO attack reports recorded a mine (11 projectile, 1 attached device, 1 waterline explosion, 3 no cause) — the mine narrative is assessed as likely deterrence messaging (55–80%) |
| 4 | **Hormuz: IRGC claims gas tanker hit mine** | Fri Nov 13 | IRGC Navy: a liquefied gas carrier (LNG per Reuters, LPG per Middle East Eye) struck a mine on an "unauthorized route"; no vessel/flag/owner/crew details; no UKMTO or owner confirmation as of Fri morning. | Reuters via Jerusalem Post / MLQ | **SPECULATION** — unconfirmed claim |
| 5 | **Houthi–Saudi: 4th Riyadh attack in 6 days** | Early Sun Nov 15 (~04:08 Riyadh) | Saudi-led coalition: air defences destroyed **2 ballistic missiles toward Riyadh** and **3 drones over the Eastern Province**; civil-defence alert issued then lifted; no damage/casualties reported. Houthis had made no claim for these launches by Sun morning. Separately Sat Nov 14, Houthi spokesman Yahya Saree claimed a drone hit King Khalid Intl Airport, 2 drones hit an East–West Pipeline pumping station, and 2 ballistic missiles hit Saudi troops at Al-Tuwal (Jazan) — **Saudi authorities have not confirmed** the airport/pipeline hits. | Reuters (Nov 15, 02:58 UTC); coalition spokesman al-Maliki via X; Houthi statement via Particle News | **FACT** (coalition interceptions as reported by Reuters); Houthi damage claims **SPECULATION / UNVERIFIED** |
| 6 | **US Mission security alert, Saudi Arabia** | Sat Nov 14 | US Mission issued a nationwide security alert urging Americans to treat every Saudi airport as at risk, citing Houthi attacks on civilian airports and critical infrastructure; restated the Oct 23 ordered departure of non-emergency staff/families. | US Mission in Saudi Arabia, via thesaudi.info | **FACT** |
| 7 | **Trump: "We don't need a deal with Iran"; Vance pulled from talks** | Thu Nov 12 (Truth Social) | Trump: US needs no Iran deal; "We've got their money… and we've got their Strait!"; directed VP Vance off Iran diplomacy to domestic issues. White House has **not** said talks are over; Tehran says it is still waiting for Washington's answer to its 7 conditions (sanctions relief, frozen-asset release, end of blockade). Mossad chief Gofman was in Washington Fri Nov 14 pressing for resumed hostilities (Axios/Israeli media). | Truth Social via Silent Dossier/AIEON; Axios | **FACT** (the post and the Vance instruction); whether talks are dead **UNVERIFIED** — no formal end announced |
| 8 | **IEA Oil Market Report** | Fri Nov 13 | Q4 2026 surplus expected; global supply +2.3M bpd in Oct to 105.36M bpd; 2026 demand **−2.7M bpd** to 102.3M bpd, +2.0M bpd rebound in 2027. North Sea Dated down >30% from Oct 8 high of $136 to ~$93. | IEA OMR Nov 2026 | **FACT** |
| 9 | **OPEC MOMR** (released Wed Nov 11, digested Fri) | Wed Nov 11 | Demand forecasts unchanged: 2026 +0.2M bpd to 105.7M bpd; 2027 +2.6M bpd to 108.3M bpd. OPEC+ crude output +2.04M bpd in Oct to 41.23M bpd. Saudi self-reported output 10.563M bpd in Oct (vs 8.372M in Sep) but supply-to-market 9.203M bpd — gap looks like stock-building, not market supply. | OPEC MOMR Nov 2026 via Argus/Egypt Oil & Gas | **FACT** (figures); stock-building read **INFERENCE** |
| 10 | **USDA export sales (grains)** | Fri Nov 13 | USDA announced 134,000 mt soybeans to China, 120,000 mt to Vietnam, 100,000 mt to unknown destinations, all 2026/27 — helped lift Jan soy +12.5¢ on the day. | USDA via Barchart | **FACT** |
| 11 | **Weather: first nor'easter, cold Nov 16–20** | Thu Nov 12 – Fri Nov 13 storm; cold through Nov 20 | Season's first nor'easter moved through the Northeast Thu–Fri (snow interior, rain I-95; temps 20–25°F below normal; first freeze to the Carolinas/Georgia/Alabama). Forecasts keep the East below normal Nov 16–20, then warming toward normal after Nov 20. LNG feedgas near-record 19.3–19.7 Bcf/d. EIA Nov outlook still sees Henry Hub averaging $2.87/MMBtu this winter. | Premier Energy Management (Nov 12); NRG Daily Market Update (Nov 13); Commodity Weather Group via TradingView | **FACT** (observed storm, feedgas); Nov 16–20 cold **INFERENCE** (forecast, subject to revision) |

**No fresh official releases this weekend:** no EIA/USDA releases due before Wed Nov 18 WPSR (10:30 ET) and Thu Nov 19 gas storage. No federal shutdown — CR funding runs through Dec 11; do not use a blackout framing.

### Futures curve reads — Fri Nov 13 settles (re-verified via Yahoo Finance v8 chart, UA header, Sun Nov 15)

| Contract | Front month | Fri Nov 13 settle | Day | Week |
|---|---|---|---|---|
| WTI (CL=F, Dec-26) | Dec-26 | **$88.56** | −$0.18 (−0.20%) | ~−2.5%, 2nd straight weekly decline |
| Brent (BZ=F, Jan-27) | Jan-27 | **$95.84** | +$0.02 (+0.02%) | ~−2.5%, 2nd straight weekly decline |
| Nat gas (NG=F, Dec-26) | Dec-26 | **$3.230** | −$0.11 (−3.3%)* | +7.7% on the week |
| Corn (ZC=F, Dec-26) | Dec-26 | **445.5¢** | +3.0¢ (+0.68%) | +4.0¢ |
| Soybeans (ZS=F, Jan-27) | Jan-27 | **$12.315** | +12.5¢ (+1.03%) | +37.75¢ |
| Wheat SRW (ZW=F, Dec-26) | Dec-26 | **593.25¢** | +9.0¢ (+1.54%) | Mar-27 +4.0¢, ending a 10-week string of lower weekly closes |

\* Nat gas day move per NRG/Daily Board (−3.3%); Yahoo front-month closes confirm $3.34 Thu → $3.23 Fri. Corn/soy/wheat settles cross-checked against USDA AMS Wyoming grain report (Nov 13) — identical. Brent/WTI settles corroborated by Reuters/Bloomberg via multiple outlets. **Deferred-month levels (e.g. WTI Dec/Jan ~+$1.05 backwardation carried from yesterday) were NOT re-verified this run — Yahoo serves front-month symbols only; treat the curve shape as UNVERIFIED until a deferred quote is pulled.**

**What the curves appear to be pricing (INFERENCE):** crude — surplus, not war. Despite a weekend of escalating Hormuz claims and a claimed supertanker sinking, Friday's flat close and the second straight ~2.5% weekly decline say the paper market is pricing the IEA/OPEC supply-restoration story (OPEC+ back to ~97% of February output, US production at a record 14.013M bpd, EIA build +4.657M bbl) over the shipping-risk story — because the *count* of attacks stays high while no sinking or infrastructure hit has been independently confirmed. The war premium that took Brent to $136 on Oct 8 has mostly bled out (~$93 North Sea Dated). Nat gas is the opposite: a weather-driven rally (+7.7% wk) on a real cold snap plus record LNG feedgas, but with a thin fundamental cushion — storage 3,862 Bcf is only 75 Bcf above the 5-yr average and EIA's $2.87 winter Hub forecast caps the bullish case if the Nov 16–20 cold does not extend. Grains: the WASDE-677 tightness (corn 1.758B bu, soy 300M bu ending stocks) is still being digested — soy +37.75¢ on the week with fresh China export sales; wheat's bounce off a 4-month low ended a 10-week losing streak but HRW March extended its slide to 11 weeks, so the wheat turn is not yet confirmed.

**SYNTHESIS CORRECTION — Hormuz traffic level:** the Futures desk's draft inference said physical flows through Hormuz have "largely recovered toward pre-war volumes." That is **NOT adopted**: it contradicts the desk's own cited figure — the last hard count is ~65% below pre-war levels (UN) / ~36 transits/day vs 130–140 pre-war — and no fresh weekend count was verified. The carried read is: traffic remains well below pre-war levels; the market's flat pricing rests on no *confirmed* disruption to flows, not on recovered volumes. The recovery claim is UNVERIFIED.

### Verdict

- **Thesis:** The desk's central tension is unchanged and widening: **physical supply is recovering while shipping risk is escalating**. The market is currently resolving that tension in favour of supply (flat-to-down crude). That resolution is fragile — it rests on flows continuing through a strait where attacks are now near-daily and where a *confirmed* sinking or a hit on a US-escorted vessel would reprice the war premium fast.
- **Evidence:** IEA Q4 surplus call + OPEC+ +2.04M bpd in Oct + record US output (FACT); Brent −20% from late-Oct $118 peak, −2.5% this week despite the claims (FACT); Hormuz attacks near-daily but no independently confirmed sinking and no confirmed damage to Saudi oil infrastructure — only an Aramco *administrative* building damaged by shrapnel Nov 8 (FACT); nat gas cold snap real and priced (FACT).
- **What would change it:** (1) a named/flagged vessel confirmed sunk or a US-escorted ship hit — would flip the crude read from "surplus" to "supply disruption" overnight; (2) a confirmed hit on Abqaiq/Khurais or an East–West Pipeline pumping station (so far only Houthi claims, unconfirmed); (3) the Nov 16–20 cold extending into December (would sustain the nat-gas rally) vs a warm revision after Nov 20 (would unwind it); (4) Wed Nov 18 WPSR — a second straight large build would reinforce surplus; a draw would challenge it.

### UNVERIFIED / gaps
- Whether any tanker actually sank on Nov 14–15, and whether UKMTO 205-26 is the same incident as the IRGC's claim — no owner/flag-state confirmation as of Sun evening.
- Deferred crude curve (Dec/Jan backwardation) — front-month only from Yahoo; needs a deferred quote.
- Houthi claims of airport/pipeline damage Nov 14 — unconfirmed by Saudi authorities.
- Whether US–Iran talks are formally over — Trump post says no deal needed; no White House statement ending talks.
- Hormuz traffic level this weekend — last hard figure ~65% below pre-war (UN) / ~36 transits/day vs 130–140 pre-war; no fresh weekend count verified.

### Forward calendar
- **Mon Nov 16:** markets reopen — first read on whether the weekend's Hormuz claims move crude; USDA Crop Progress (Mon afternoon).
- **Wed Nov 18, 10:30 ET:** EIA Weekly Petroleum Status Report (week ending Nov 13).
- **Thu Nov 19, 10:30 ET:** EIA Weekly Natural Gas Storage Report.
- **Sun Nov 29:** OPEC+ meeting (online) — 2027 production targets.
- **Wed Dec 10:** USDA WASDE-678.
- **Fri Dec 11:** federal funding (CR) expires — watch for any appropriations/shutdown headlines; no shutdown framing until/unless a primary source says otherwise.

---

## 6. Box / Parity Observer

**Bottom line:** No new index-methodology doc and no new published parity-violation analysis since yesterday. Put–call parity on the Nov 18 VIX options held within a few cents of settlement in every Saxo brief checked this week; the current SPX box rate remains UNVERIFIED from a direct dated print.

**New since yesterday's check (FACT, sources as noted):**
- **Saxo Options Briefs, Nov 6 and Nov 11 — parity holding.** Nov 6 brief (Thu Nov 5 close): put–call parity on the 18 Nov options returned **24.55**, in line with Thursday's settlement. Nov 11 brief (Tue Nov 10 close): parity check read **19.82**; Saxo drew no session comparison because the future fell ~0.7 in overnight trade. Nov 5 brief (Wed Nov 4 close): **17.73 vs 17.74** settlement. No violation flagged in any of them. (Sources: home.saxo Options Briefs, 5/6/11 Nov 2026.)
- **Saxo briefs for Nov 12 and Nov 13 exist** ("Volatility drains then Nvidia slips after hours", "One-day protection jumps as the index slips") — their parity lines were not verified in this sweep (UNVERIFIED for those two dates, not assumed to match).
- **SPXO first-expiry detail (FACT, new colour on the standing item):** Options Matrix Pro, Nov 10, 2026, notes the first SPXO expiry (Wed Nov 18) stops trading Tue Nov 17 — the AM-settled contract's final trading day is the business day before its Wednesday settlement, unlike the PM-settled SPXW same-date expiry which trades through Wednesday's close. Cboe's Available Weeklys list as of 11/13/26 confirms SPXO listed and trading. No change to the SPXO facts reported yesterday.
- **Box-rate estimate, dated but not a direct print (FACT, labelled estimate):** Alaska Wealth Advisors (rates as of Nov 6, 2026) puts box-spread rates at ~0.53% above comparable Treasuries across 1-month to 5-year terms, working out to ~**4.90% on a one-year loan** (after-tax estimate ~3.40% at a 30.6% blended rate for a taxpayer with gains to offset). This is an adviser's estimate, not a tradeable SPX box quote.

**Unchanged / standing:**
- **Current SPX box rate: UNVERIFIED.** Latest direct dated print remains Tulan Capital, Oct 20, 2026 — Dec 2026 SPX boxes ~4.3–4.4% vs ~4.1% 1-month Treasury — now ~3.5 weeks stale. No newer boxtrades.com / CBOE Box Rate index print was verifiable from free sources today. The Nov 6 AK Wealth 4.90% figure above is a 1-year estimate, not a substitute for a dated box print.
- **SPXO remains the standing watch item** (Cboe AM-settled SPX weeklies, effective trade date Mon Nov 9, 2026; first expiries Nov 18 and Dec 16, 2026; price-time allocation; min quote size 1; SPXW combined with SPX/SPXO cannot leg into single-leg books).

**No new index-methodology docs, no new published parity-violation analysis.** One background item surfaced but is not new: arXiv preprint "The Cost of a Free Lunch" (Shin, Aug 24, 2026) finds quoted put–call parity residuals near zero on SPX/RUT but a systematic ~37bp median carry gap vs OIS — a carry-space wedge, not a price-space violation; flagged for the Quant Lab ledger, not a desk finding.

---

## 7. Bonds & Rates desk (Desk 7 — consolidated deliverable)

**Status:** Worked from the consolidated deliverable (`desk7-core-indicators.md`, Nov 13 snapshot). Module ran clean this session in `REAL_FRED_RATES` mode; all 10 core indicators re-pulled fresh from FRED this session via the repo's `rates_desk.fred_series_rows`. No kept indicator printed new data since Nov 13 — the changes are in market pricing and speaker remarks. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; UNVERIFIED = looked, could not confirm.

**Sources this session:** repo rates module (`rates_desk.rates_environment()`, REAL_FRED_RATES, pulled ~13:35 PT) + `fred_series_rows` for the 10 core indicators + Kalshi direct API (`KXFEDDECISION-26DEC`, pulled ~13:37 PT) + web search for FOMC-speaker remarks. No federal shutdown — CR funding runs through Dec 11; no "data blackout" framing applies.

### 1. Rates table (FRED, module pull `rates_desk.rates_environment()`, as_of 2026-11-15; latest obs Nov 12 — Nov 13 DGS obs not yet posted in FRED at pull time)

| Series | Read | As-of |
|---|---|---|
| Effective fed funds (DFF) | 3.88% | Nov 12 |
| 2Y Treasury (DGS2) | 4.86% | Nov 12 |
| 10Y Treasury (DGS10) | 5.10% | Nov 12 |
| SOFR | 3.90% | Nov 12 |
| EFFR | 3.88% | Nov 12 |
| Overnight bank funding rate (OBFR) | 3.88% | Nov 12 |

**2s10s slope: +24bp** (5.10 − 4.86), curve UPWARD_SLOPING. Direction of change: **flat since Nov 12** (24bp, unchanged from yesterday's snapshot). Both legs up hard on the week: 10Y 4.86% (Nov 6) → 5.10% (Nov 12), +24bp; 2Y 4.51% (Nov 6) → 4.86% (Nov 12), +35bp.

**SOFR vs EFFR funding spread: +2bp** (3.90 − 3.88). No funding stress — SOFR sits on top of EFFR, not gapping above it. (FACT, FRED.)

Note: a single-basis press report (ainvest, Nov 14) puts the 10Y Friday close at 5.152%, +5bp vs the FRED Nov 12 read — **UNVERIFIED against FRED until the obs posts; not used as the anchor.**

### 2. Core-indicator table (fresh FRED pull this session unless noted)

| Indicator | Trigger rule | Today's read | Signal | Broker POV |
|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA via FRED) | HIKE if y/y > 2.5% or m/m > +0.25%; CUT if y/y < 2.2% | y/y +3.121%, m/m +0.317% (130.902, Sep 2026; Sep 2025 126.94, Aug 130.489). Unchanged from Nov 13. | **HIKE** | Anchor the discount rate to the higher regime. The decision variable is PCE, not CPI — the Oct CPI print (+0.3% core m/m, meeting Waller's trigger) corroborates but does not re-anchor. The next print (Oct PCE, Nov 25, date provisional) is the re-anchor date. |
| Breakevens (T5YIE / T10YIE, FRED) | HIKE if > 2.75%; CUT if < 1.75%; NEUTRAL 2.0–2.5% | 2.30% / 2.24% (Nov 13). 5Y eased 1bp from 2.31%. | **NEUTRAL** | Anchored expectations: room for 25bp, not a forced 50bp. Tripwire is a break above 2.75%. |
| Michigan expectations (MICH, U-M) | HIKE if yr-ahead > 3.5%; CUT if < 2.5% | 4.3% yr-ahead, Nov prelim (rel. Nov 6). Carried forward from Nov 13 — FRED MICH lags ~2 months (latest FRED obs Sep 4.6%) and is not the current read. | **HIKE** | Do not average with breakevens: 4.3% vs 2.24% is a credibility gap the Fed reads as pressure to act. |
| Payrolls, 3-mo avg (PAYEMS, BLS via FRED) | HIKE if 3-mo avg > +150k; CUT if < +50k | 3-mo avg +137k (Jul→Aug +186k, Aug→Sep +60k, Sep→Oct +165k; Oct level 159,293k). Unchanged. | **NEUTRAL** | Rule as written: NEUTRAL. The single +165k print does not override the average. |
| Initial claims, 4-wk avg (ICSA, DOL via FRED) | CUT if 4-wk avg > 300k; NEUTRAL < 250k | 200k w/e Nov 7; 4-wk avg 195,250. Unchanged. | **NEUTRAL** | No action. Check every Thursday: a 4-wk average above 300k flips the labor read to CUT before payrolls confirm. |
| Job openings (JTSJOL, BLS via FRED) | HIKE if 3-mo change positive; CUT if −500k over 3 months | 7,523k, Sep 2026 (Jul 7,335k → +188k over 3 mo). Unchanged. | **HIKE** | Demand has not rolled over: rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA via FRED) | HIKE if > 2.5% annualized; CUT if < 1.0% | Q3 +3.37% annualized (24,611.077 vs Q2 24,408.011). Unchanged. | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Growth is backdrop, not trigger — PCE, claims, and the minutes are the prints that can move the call before Dec 9. |
| Housing starts (HOUST, Census via FRED) | CUT if −5% over 3 months; HIKE if rising through high rates | 1,221k; −10.8% Jul→Sep (Sep 2026). Unchanged. | **CUT** | Report it, don't bury it: the evidence a hold argument would cite, and why the call is 25bp, not 50bp. |
| High-yield OAS (BAMLH0A0HYM2, ICE BofA via FRED) | CUT if > 5.00%; NEUTRAL < 4.00% | 3.20% (Nov 12; Nov 13 obs not yet in FRED). Unchanged. | **NEUTRAL** | No stress: the market is neither doing the Fed's tightening work nor forcing an easing response. Watch is a break above 5.00%. |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening or language turns hawkish; CUT if the reverse | Oct 28: held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; statement: "Inflation remains elevated." Unchanged. | **HIKE** | Weight the vote above any single print. New since the Nov 13 snapshot: five more hawkish named statements Thu–Fri (Collins, Goolsbee, Daly, Williams, Hammack) — weekly count now **12 hawkish / 0 dovish** (INFERENCE, single-basis press reports). The Nov 18 minutes are the check on whether 10–2 understates division. |

**Tally: 5 HIKE / 1 CUT / 4 NEUTRAL — unchanged from Nov 13.** No kept indicator changed signal this session.

### 3. Speaker watch — new since Fri Nov 13

- **Collins (Boston, Fri Nov 13, Bloomberg TV via Reuters):** "more rate hikes are coming… soon some additional firming, tightening of policy is appropriate" — hawkish, and "more than she initially expected." (FACT, single-basis press; not verified against federalreserve.gov.)
- **Goolsbee (Chicago, Thu Nov 12, Yahoo Finance):** inflation "well above target," Oct CPI "wasn't a one-off," Fed "inching into a historically tough spot" and "failing on the inflation side of the mandate"; AI investment "starting to look more just like old-fashioned demand overheating." (FACT, FXStreet/Bloomberg Law, single-basis press.)
- **Daly (San Francisco, Thu Nov 12, Stanford SIEPR keynote):** AI has fuelled price pressure, inflation bleeding into services where it turns sticky, "prevailing bias is that further tightening will be needed"; comfortable with the September hike. (FACT, single-basis press summary.)
- **Williams (New York, Thu Nov 12):** economy strong, inflation persistent. (FACT, single-basis press summary.)
- **Hammack (Cleveland, Thu Nov 12):** inflation outlook worsening; supports a gradual approach to hiking. (FACT, single-basis press.)
- **Warsh (Chair):** gave opening remarks Fri Nov 13 at a Fed event; no substantive Dec signal found in search. He "doesn't believe in pre-judging meetings" — the chair has not signaled December, so the hike call rests on data + dissents + the speaker chorus, not chair guidance. (INFERENCE.) The Fed confirmed Nov 13 it will hold **no rate vote at its October 2027 meeting** (Warsh's fewer-decisions revamp) — institutional, not a Dec signal. Warsh delivers opening remarks Mon Nov 16 in San Francisco — watch item. (FACT, press reports.)

### 4. Market pricing vs indicators

**Kalshi, direct API pull this session (Sun Nov 15 ~13:37 PT, event `KXFEDDECISION-26DEC`):** 25bp hike $0.88 (bid/ask 0.87/0.88, prev 0.88, 24h vol 29,866); more than 25bp $0.11 (0.10/0.11, prev 0.11, vol 57,060); hold $0.03 (0.03/0.04, prev 0.04, vol 382,521); 25bp cut $0.01; more than 25bp cut $0.01. Five lasts sum to $1.04 (4-cent over-round). **Total hike $0.99** (was $1.00 Nov 13) — a 1-cent drift, hold ticking down a cent: noise, not signal.

**CME FedWatch (secondhand, no public text API):** Newsquawk primer puts the 50bp-hike probability at **10%** and Dec pricing at 27.6bp (prev 24.7bp); a Nov 12 roundup puts the 50bp odds at **15%** and a 60% chance rates reach 4.25–4.50% by the January meeting. Secondhand range for 50bp: **10–15%**.

**Disagreements named:** None on direction — indicators (5/1/4), Kalshi ($0.99 total hike), and FedWatch (hike unanimously expected, per secondhand) all point to a December hike. The only movement is size: the Kalshi 50bp tail eased $0.12 → $0.11 and the hold leg $0.04 → $0.03, while FedWatch secondhand still spans 10–15% for 50bp — Kalshi's $0.11 sits inside that range. The indicator set votes direction, not size, and no rule in it distinguishes 25bp from 50bp. (INFERENCE.)

### 5. Verdict — call UNCHANGED: 25bp hike on Dec 9

- **Thesis:** Core PCE at 3.12% y/y against a 2% target, no labor deterioration on any kept read, above-trend growth, and a 10–2 hold vote with two dissents for an immediate hike all point one way. Markets price the hike at $0.99 combined and the 25bp size at $0.88. The call is 25bp, not 50bp, because housing starts (−10.8% over 3 months) is the live counter-evidence and no indicator rule separates the two sizes.
- **Evidence:** 5 HIKE / 1 CUT / 4 NEUTRAL across the 10 core indicators (all re-pulled from FRED this session); 2Y +35bp and 10Y +24bp on the week as the market repriced the hike in; Kalshi total hike $0.99; FedWatch secondhand unanimous on a hike; Friday's PPI +6.5% y/y (BLS, reported Nov 13) is the latest print corroborating the inflation side. The single CUT vote (housing starts, −10.8% Jul→Sep) is why the call is 25bp, not 50bp.
- **What would change it:** October core PCE (Nov 25, date provisional) at m/m ≤ +0.15% with a downward revision to September; initial claims 4-week average above 300k; the November 18 minutes, or a named speaker arguing for a hold, showing the Committee more worried about overtightening than the 10–2 vote suggested. A named 50bp endorsement from a voter would move the size call, not the direction call.

### 6. Graham lens (updated)

10Y 4.98% (Nov 10) → 5.10% (Nov 12). At assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) falls 50.51x → 47.62x, **−5.72%** — arithmetic, not opinion. Duration ≈ 8 puts the same +12bp move at about −0.96% on a 10-year position (approximation; ignores convexity). The margin of safety is thinner at the same prices: any intrinsic-value estimate carried at the old 4.98% anchor overstates value by ~6% on this sensitivity. **Re-anchor to 5.10%.** If the press-reported Friday close of 5.152% is confirmed when the FRED Nov 13 obs posts, the multiple would be ~46.5x — a further ~2.4% thinner margin of safety (sensitivity, single-basis press, UNVERIFIED against FRED). Earnings-yield vs bond-yield spread: UNVERIFIED — bond side verified (5.10%); earnings side unverified from any primary source this session. No live spread is asserted. The defensive read stands: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price.

### 7. What changed since Nov 13 (summary)

1. Yields: unchanged on FRED (Nov 13 DGS obs still pending); 10Y 5.10%, 2Y 4.86% (Nov 12 obs); 2s10s flat at 24bp; SOFR−EFFR flat at +2bp, no funding stress.
2. Kalshi: total hike $1.00 → $0.99; 25bp flat at $0.88; >25bp $0.12 → $0.11; hold $0.04 → $0.03.
3. FedWatch: 50bp secondhand range 10–15%, in line with Kalshi.
4. Speakers: five more hawkish named remarks Thu–Fri (Collins, Goolsbee, Daly, Williams, Hammack) — weekly count 7 → 12 hawkish, 0 dovish; Chair Warsh gave no Dec signal.
5. No kept indicator printed new data; tally unchanged at 5 HIKE / 1 CUT / 4 NEUTRAL. Next data that can move the call: Oct 27–28 minutes Nov 18, Oct PCE Nov 25 (provisional), November jobs report before Dec 9 (date unconfirmed), November CPI Dec 10 (after the decision, cannot change December).

**Desk status: COMPLETE.** Module succeeded; all 10 indicators pulled fresh from FRED this session; market pricing pulled direct from Kalshi this session. UNVERIFIED items: FRED Nov 13 DGS obs (not yet posted at pull time; 10Y Nov 13 close ~5.152% press-reported only); HY OAS Nov 13 obs (not yet in FRED); FedWatch read secondhand (no public text API); Waller/Logan/Collins/Goolsbee/Daly/Williams/Hammack remarks single-basis press reports, not verified against federalreserve.gov; earnings-yield spread (no earnings-side source this session).

---

## Cross-desk notes (synthesis)

- **NVDA date resolved three ways:** the Earnings desk verified Tue Nov 17 after close via Nasdaq calendar API + Yahoo calendarEvents (confirmed, non-estimate); the IV desk's file scan agrees and the 103.43% Nov 18 IV hump corroborates an event inside that window; the Dividend desk notes the Nov 17 release is on pattern where the next dividend declaration would appear. Date stands as FACT.
- **Correction carried:** yesterday's package printed the signed average of NVDA's last 4 earnings-day moves as −0.02%; recomputed this session it is **+0.23%** (−3.15 −5.46 +0.78 +8.74 = +0.91 ÷ 4). Absolute average 4.53% unchanged. No directional bias either way.
- **The Nov 5 jump still dominates every vol read:** all six 20-day realized windows are WINDOW-CONTINGENT (37–54% single-day variance share). No clean IV-vs-realized verdict this run; the window rolls past Nov 5 after ~Dec 3. The IV null streak is broken (file ATM IVs populated), but the file's levels are yesterday's pull — STALE — and the live supplement is Friday-close marks.
- **Futures-desk inconsistency corrected in synthesis:** the desk's draft said Hormuz flows had "largely recovered toward pre-war volumes"; its own cited figure is ~65% below pre-war (~36 transits/day vs 130–140). The recovery claim is NOT adopted — carried as UNVERIFIED. The market's flat pricing rests on no *confirmed* disruption, not on recovered volumes.
- **Rates vs premium desks agree:** the discount-rate anchor moved up (10Y 5.10%) while front-end IVs ex-NVDA are unremarkable — no vol signal contradicts the rates call. QQQ put skew is steepest (+12.6–15.0pp) with heavy Nov 17 put OI — downside protection is the expensive side of the board, consistent with post-crash positioning (INFERENCE).
- **No parity violation; SPXO first expiry Wed Nov 18** (stops trading Tue Nov 17) is the structural watch item for any future SPX box/conversion construction. Box/Parity flagged arXiv preprint "The Cost of a Free Lunch" (Shin, Aug 24, 2026) — quoted put–call parity residuals near zero on SPX/RUT but a ~37bp median carry gap vs OIS; flagged for the Quant Lab's next sweep to score (not a desk finding, not ledgered this run).
- **Quant lab:** empty sweep by design (Sunday, no arXiv announcement); Nov 13 window fully closed; next material input is the Mon Nov 16 announcement. #288 (Feng et al — 72% of earnings news appears after the filing) remains the caution most relevant to the Earnings desk's sourcing discipline.
- **Monday is the test day:** crude's reaction to the weekend's Hormuz claims, NVDA straddle repricing, AAPL's $0.27 payment landing, and Warsh's opening remarks in San Francisco.

## Desk status
All seven desks delivered: Earnings ✓ · Dividend ✓ · Premium IV ✓ · Quant Lab ✓ · Futures Events ✓ · Box/Parity ✓ · Bonds & Rates ✓. No desk FAILED. No retry needed.

## Sources
Nasdaq earnings/dividends calendar APIs; Yahoo Finance v7 options, v10 quoteSummary, v8 chart (cookie+crumb where required); FRED via `hedge_desk.rates_desk` (REAL_FRED_RATES); Kalshi API (`KXFEDDECISION-26DEC`); EIA WPSR/STEO; USDA WASDE-677 + export sales; IEA Oil Market Report; OPEC MOMR; arXiv q-fin listings; CBOE product notices; Saxo options briefs; UKMTO Warning 205-26; US Mission Saudi Arabia security alert. Full per-item sources in each desk section above.
