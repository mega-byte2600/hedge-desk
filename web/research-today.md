# Hedge-Desk Daily Research — Fri 2026-11-20

**Run:** 13:30 PT / 16:30 ET (post-close). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** 7 desks fanned out in parallel; CFA evidence discipline (FACT / INFERENCE / SPECULATION / UNVERIFIED, source + as-of on every material claim). No federal shutdown — CR funding through Dec 11; EIA/USDA releases on schedule.
**IV inputs file:** `nightly/2026-11-19-iv-inputs.json`, as_of 2026-11-19T21:57:07-07:00 — FRESH under the 26h guard (~15.5h old at run start), but its ATM IVs are DTE=1 on expiry 2026-11-20 and are solver residuals on dead contracts, not usable levels (see §3).

## Market close — Fri Nov 20 [FACT, Yahoo v8 chart, post-close]

| Symbol | Close | Day move |
|---|---|---|
| SPY | $689.81 | −3.64% |
| QQQ | $608.45 | −5.67% |
| AAPL | $342.56 | −1.90% |
| MSFT | $484.52 | −2.77% |
| NVDA | $125.53 | **−14.01%** |
| TSLA | $345.82 | −7.64% |

## The 5 most decision-relevant items

1. **NVDA collapsed 14.01% to $125.53 on 609.5M shares — three-session post-print drift now −19.26%.** Reuters reported Friday that the SEC enforcement division has opened an investigation into Nvidia's accounting, focused on its Singapore revenue reclassification. Label: Reuters-reported, NOT SEC-confirmed — no SEC statement or filing seen. The Q3 print itself was a clean beat-and-raise (revenue $115.8B, +103% YoY; EPS $2.68 vs $2.47 consensus; $130B Q4 guide). NVDA's 10-Q is still not filed (EDGAR: only Nov 12 and Nov 17 8-Ks since Nov 1), so the cash-flow quality check stays UNVERIFIED and is now more urgent. Do not cite the Nov 17 −2.89% as "the NVDA earnings move" — the catalyst arrived three sessions after the print. (§1)
2. **Desk 7: 25bp hike Dec 9 holds; tally unchanged 5 HIKE / 0 CUT / 5 NEUTRAL.** Michigan final cooled hard — yr-ahead expectations 3.7% (prelim 4.3%, Oct 4.7%) — still fires the HIKE trigger (>3.5%), margin now only 20bp. Kalshi repriced toward hold and away from the tail in one session: 25bp $0.92→$0.90, >25bp $0.07→$0.02, hold $0.04→$0.11; total hike $0.99→$0.92. Treasury Secretary Bessent pushed back on 50bp (CNBC, Nov 20) — first senior administration voice against the tail; he is not an FOMC voter. HY OAS widened a 5th straight session to 3.52%, still NEUTRAL, 48bp from the 4.00% watch level. (§7)
3. **No premium edge demonstrable today.** Dec 18 ATM IV jumped 6–25pp day-over-day on all six names (NVDA 52.9% → 77.8%), flipping yesterday's at/below-realized pattern to above-realized everywhere — but every 20-day realized window is WINDOW-CONTINGENT (single day drives 35–50% of variance; Nov 5 crash day), so no clean IV-vs-realized verdict is issuable. IV rank UNVERIFIED (no IV history from free sources). Today's tape is a risk event to observe, not premium to sell into. (§3)
4. **Surplus narrative won the oil week despite a fourth tanker strike.** Brent −5% / Dec WTI −6.5 to −8% on the week (third straight weekly decline); UKMTO confirmed a new tanker strike/fire ~8nm north of Khasab Fri ~15:00 UTC. The Trump–Xi–Putin trilateral (Thu, Shenzhen) pledged more refined-product supply — no volumes, no timetable, no mechanism; Capital Economics: "political noise." Gold's worst week in 8 months (−8.9%, spot ~$3,552) during a Hormuz shooting war: rate-hike repricing is beating safe-haven demand for a second straight day. USDA Cattle on Feed today: Oct placements 1.891m head, −7.3% YoY — lowest October on record. (§5)
5. **No watchlist earnings in the next 2 weeks; one routine ex-date in the next 4 weeks.** Next reports are all late January (AAPL Jan 28, MSFT Jan 27, TSLA Jan 27, all estimates; NVDA ~Feb 23, 2027 estimate). NVDA ex-date Wed Dec 2, $0.25/qtr — a re-declaration at the unchanged rate, NOT a raise. MSFT went ex Nov 19 at the raised $0.98; 24 consecutive annual increases intact. SPY's December distribution expected ~Dec 18, not yet declared. (§1, §2)

---

# 1. Earnings Event desk — Fri 2026-11-20 (13:30 PT run)

**Window:** Nov 20 – Dec 4, 2026 (2 weeks). **As-of:** Nov 20 ~13:30 PT / 16:30 ET (post-close). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Sources:** Nasdaq earnings-calendar API (all 10 trading days in window, per-date pull), Yahoo v10 quoteSummary `calendarEvents` (cookie+crumb), Yahoo v8 chart + v7 quote (prices), SEC EDGAR (NVDA submissions), Reuters/WSJ via web search (NVDA probe — secondhand, see labels).

## Upcoming earnings in the window — NONE for the watchlist

| Symbol | Earnings in window? | Next known report |
|---|---|---|
| SPY | No — ETF, no earnings | n/a |
| QQQ | No — ETF, no earnings | n/a |
| AAPL | No | **Jan 28, 2027 (estimate)** — Yahoo calendarEvents, `isEarningsDateEstimate: true` |
| MSFT | No | **Jan 27, 2027 (estimate)** — Yahoo calendarEvents, `isEarningsDateEstimate: true` |
| NVDA | No — reported Tue Nov 17, after close (see below) | **~Feb 23, 2027 (estimate)** — Finnhub quarterly table; exact date UNVERIFIED |
| TSLA | No | **Jan 27, 2027 (estimate)** — Yahoo calendarEvents, `isEarningsDateEstimate: true` |

**Verification [FACT]:** Nasdaq calendar returned 260 rows across the 10 trading days Nov 20, 23, 24, 25, 27, 30, Dec 1–4 (Nov 26 Thanksgiving — market closed, no session); zero rows for any watchlist symbol. Yahoo `calendarEvents` independently confirms no watchlist report date before Jan 27, 2027. Two independent sources agree — no earnings inside the window.

**Options-implied expected move:** N/A for all six — no earnings inside the window, so no binary-event premium to price. [FACT]

## NVDA — the live earnings item: post-print collapse, now −19.26% in three sessions

**Prices [FACT, Yahoo v8 chart + v7 quote, two bases agree; Finnhub third basis on the close]:**

| Session | Close | Day move | Volume |
|---|---|---|---|
| Mon Nov 16 (pre-print) | $156.14 | — | 333.8M |
| Tue Nov 17 (print, after close) | $155.46 | −0.44% | 407.0M |
| Wed Nov 18 | $150.96 | **−2.89%** | 349.8M |
| Thu Nov 19 | $145.98 | **−3.30%** | 322.9M |
| **Fri Nov 20** | **$125.53** | **−14.01%** | **609.5M** |

- **Three-session post-print move: $155.46 → $125.53 = −19.26%.** [FACT, arithmetic on verified closes]
- **Friday's session [FACT, Yahoo v7 quote]:** open $143.52, high $143.73, low $124.51 — a $19.22 intraday range (~13% of the open). Volume 609.5M, ~1.8× the prior sessions' ~330–407M. After-hours ~$127.78 (+1.79% vs close, Finnhub).
- **Weekly: −23% for the week** (WSJ, citing Dow Jones Market Data) — worst week since 2008 per the WSJ headline. [FACT as reported; WSJ is the source, not this desk's computation]

**Why Friday moved [FACT as reported by Reuters; the probe itself is NOT primary-source confirmed]:** Reuters reported Friday that the SEC's enforcement division has opened an investigation into Nvidia's accounting practices, with its Singapore revenue reclassification in focus. Reported by Reuters and carried by WSJ, Motley Fool, and Coinotag the same day. **Label: the probe is Reuters-reported, not SEC-confirmed — no SEC statement or filing has been seen by this desk.** Yesterday this desk carried the probe as UNVERIFIED on two outlets; today's Reuters report upgrades it to secondhand-reported, still not primary-verified.

**Context that frames the move [FACT, prior desk reads + today's reporting]:** the stock was already down ~26% since reports of Huang's resignation first surfaced (Fool, Nov 20), and the Q3 print itself was a clean beat-and-raise (revenue $115.8B +103% YoY, non-GAAP EPS $2.68 vs $2.47 consensus, Q4 guide $130B ±3%). The three-day slide is therefore not about the print — it is about governance/accounting overhang: CEO transition (Huang resigned Nov 11; interim CEO Colette Kress), guided margin step-down (71–72% vs 74.9%), and now the reported SEC accounting probe. [INFERENCE on causation; FACT on the underlying items]

**10-Q status [FACT, SEC EDGAR submissions data, pulled this session]:** no 10-Q has been filed since Nov 1 — only the Nov 12 8-K (Huang resignation) and the Nov 17 8-K (Q3 release, accession 0001045810-26-000088). The cash-flow quality check (OCF vs net income, capex, buybacks-vs-issuance) remains **UNVERIFIED and now more urgent**: the reported probe centers on accounting/revenue classification, so the 10-Q cash-flow statement is the first primary document that can test whether the accounting concern touches cash reality. **What would change the read:** the 10-Q filing itself, or an SEC/Nvidia statement confirming or denying the probe.

## Historical earnings-day moves [FACT, Yahoo v8 chart, close-to-close report day → next session]

| Symbol | Last 4 earnings-day moves | Avg absolute | Avg signed |
|---|---|---|---|
| NVDA | Feb 25: −5.46% · May 28: −1.45% · Aug 26: +8.74% · Nov 17: −2.89% | **4.64%** | −0.27% |
| AAPL | Most recent only (Oct 30): −1.83% | UNVERIFIED (4-print avg not computed) | — |
| MSFT | Most recent only (Oct 29): −1.55% | UNVERIFIED | — |
| TSLA | Most recent only (Oct 22): −0.63% | UNVERIFIED | — |

Note: the Nov 17 −2.89% is the *first-session* reaction only. The full post-print drift through Nov 20 is −19.26% — the earnings-day table understates the realised move because the catalyst (reported SEC probe) arrived three sessions after the print, not on it. Do not use the −2.89% as "the NVDA earnings move" without the drift. [FACT + INFERENCE on framing]

## Verdict

**No binary earnings event in the next two weeks for any watchlist name — nothing to position around, nothing to avoid.** The live earnings item is NVDA's post-print collapse: a clean beat-and-raise now down 19.26% in three sessions, with Friday's −14.01% on 609.5M shares driven by a Reuters-reported SEC accounting probe (Singapore revenue reclassification) that is **not yet primary-source confirmed**. **What would change this verdict:** (a) a newly announced report date inside the window; (b) the NVDA 10-Q — if OCF trails net income materially, the quality read changes; (c) an SEC or Nvidia statement confirming/denying the probe — confirmation would extend the governance overhang, denial would remove Friday's stated catalyst.

**Value-lens note [INFERENCE]:** NVDA at $125.53 is ~48% below its Oct 6 intraday peak of $243.37 (Finnhub) — the margin-of-safety question has flipped from "is the multiple too high" to "is the accounting/governance discount now excessive relative to a $115.8B quarter growing 103%?" That question cannot be answered until the 10-Q and the probe status are primary-sourced. No valuation call is made here.

## Sources

- Nasdaq earnings calendar API: `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD` (Nov 20, 23, 24, 25, 27, 30, Dec 1, 2, 3, 4 — 260 rows total, zero watchlist hits)
- Yahoo v10 quoteSummary `calendarEvents` (cookie+crumb, crumb acquired this session): AAPL/MSFT/TSLA next-estimate dates; NVDA last report Nov 17
- Yahoo v8 chart + v7 quote: NVDA closes/volumes Nov 16–20 (two bases agree on $125.53 / −14.01%)
- SEC EDGAR submissions: `https://data.sec.gov/submissions/CIK0001045810.json` — no 10-Q filed since Nov 1
- Reuters-reported SEC probe (secondhand via): https://www.fool.com/investing/2026/11/20/nvidia-stock-plunge-wipes-out-nearly-usd500-billion-in-one-day-as-sec-reportedly-probes-its-accounting/ ; https://www.reuters.com/business/view-nasdaq-plunges-5-day-after-anthropic-debut-investors-still-believe-ai-2026-11-20/ ; https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-11-20-2026/card/nvidia-stock-is-having-its-worst-week-since-2018-jIhbOst83m4aksKYQ5YK
- Finnhub quote snapshot (third basis on Nov 20 close $125.53, after-hours $127.78; Oct 6 peak $243.37): https://finnhub.io/?q=%22NVDA%22
- NVDA Q3 FY27 release (EDGAR, read Nov 19): https://www.sec.gov/Archives/edgar/data/1045810/000104581026000088/q3fy27pr.htm

---
# 2. Dividend Opportunity desk — Fri 2026-11-20

**As-of:** Fri 2026-11-20 ~13:30 PT / 16:30 ET (post-close). **Window:** Nov 20 – Dec 18, 2026 (4 weeks). Sources: Nasdaq dividends calendar API (per-date pull, Nov 20–Dec 18), Yahoo v7 quote (cookie+crumb) and v8 chart, issuer announcements.

## Upcoming ex-dividend dates in window

| Symbol | Ex-date | Amount | Record | Payable | Forward yield* | Status |
|---|---|---|---|---|---|---|
| NVDA | **Wed Dec 2, 2026** | $0.25/qtr | Dec 2, 2026 | Dec 23, 2026 | 0.80% ($1.00/yr on $125.53) | FACT — Nasdaq calendar + Yahoo quote (divRate 1.00) + NVDA Q3 FY2027 release Nov 17, 2026 |

\*Yield from Yahoo v7 quote pulled this session (16:30 ET, post-close prices — indicative, not live).

## Increases, cuts, specials
- **No new increase, cut, or special dividend announced in this window.** [FACT]
- **NVDA — re-declared, NOT a new increase:** the Nov 17, 2026 earnings release declared the $0.25 quarterly dividend at the **unchanged** rate; announcement date on the Nasdaq calendar row is 11/17/2026. The actual increase was May 2026: $0.01 → $0.25 (+2,400%). [FACT] Do not report the Nov 17 declaration as a raise. NVDA's "3 consecutive years" streak figure is third-party only and not issuer-verified this run.
- **MSFT — increase already in effect, not new:** Sep 15, 2026 board raise $0.91 → $0.98 (+$0.07, ~8%); ex-date was **yesterday, Thu Nov 19** — now outside this window. First payment at the new rate Dec 10, 2026. [FACT, Microsoft newsroom] Consecutive-increase count: **24 consecutive annual increases** (incl. the Sep 2026 raise), per the desk's standardized definition in `~/workspace/hedge-desk-research/dividend-count-standard.md`. [FACT]

## Names with nothing in the window
- **SPY — nothing in window.** [FACT] Last distribution $1.889, ex Sep 18, 2026. Next quarterly distribution expected ~Dec 18 (third Friday) — INFERENCE from cadence, **not yet declared**: no SPY row on the Nasdaq calendar Dec 18 (8 rows that day, none SPY), and no SPY row on any scanned date Nov 20–Dec 18.
- **QQQ — nothing in window.** [FACT] Last distribution $0.751, ex Sep 21, 2026. Next expected ~Dec 21–22 — INFERENCE, outside the window and not yet declared.
- **AAPL — nothing in window; went ex last week.** [FACT] $0.27/qtr, ex-date Thu Nov 12, 2026, paid Nov 16, 2026. Next expected ~Feb 2027 (INFERENCE from quarterly cadence). AAPL's consecutive-increase count (third-party figure: 14) is **UNVERIFIED** per desk standard — not checked against Apple IR this run; payment history confirms annual May raises ($0.25→$0.26 May 2025, $0.26→$0.27 May 2026).
- **TSLA — no dividend.** [FACT] (Yahoo quote: dividendYield 0.0; pays no dividend.)

## Price context for the yield math — sharp down day at today's close
[FACT, Yahoo v8 chart closes, Nov 20 vs Nov 19] SPY 689.81 (−3.64%), QQQ 608.45 (−5.67%), AAPL 342.56 (−1.90%), MSFT 484.52 (−2.77%), NVDA 125.53 (−14.01%), TSLA 345.82 (−7.64%). NVDA's −14.01% is its third straight post-print down session (Nov 18 −2.89%, Nov 19 −3.30%, Nov 20 −14.01%; cumulative −19.3% from the Nov 17 close of $155.46). The cause of today's move is outside this desk's brief — no dividend announcement explains it (no NVDA dividend news today; the Dec 2 declaration is unchanged from Nov 17). Yields below are mechanically higher than yesterday's on the lower prices; that is arithmetic, not a dividend change.

| Symbol | Close Nov 20 | Forward yield (today) | Forward yield (Nov 19) |
|---|---|---|---|
| MSFT | $484.52 | 0.81% ($3.92/yr) | 0.77% |
| NVDA | $125.53 | 0.80% ($1.00/yr) | 0.66% |
| AAPL | $342.56 | 0.32% ($1.08/yr) | ~0.31% |
| SPY | $689.81 | 0.79% trailing (Yahoo) | — |
| QQQ | $608.45 | 0.27% trailing (Yahoo) | — |
| TSLA | $345.82 | 0.00% | 0.00% |

## Value-lens read [INFERENCE]
Yields remain thin (MSFT 0.81%, NVDA 0.80%, AAPL 0.32%) — none is an income opportunity at current prices; the dividend signal here is balance-sheet strength, not margin of safety. Today's move changed the arithmetic, not the dividend facts: NVDA's $1.00/yr run-rate is unchanged, and MSFT's 24-year raise streak is intact with its first $0.98 payment due Dec 10. The only dated dividend event in the next four weeks is NVDA's Dec 2 ex-date — a routine $0.25 payment, not a catalyst.

**Verdict:** One routine ex-date in the window (NVDA, Dec 2, unchanged $0.25). No increases, cuts, or specials announced. SPY's December distribution is the item to watch — expected ~Dec 18, not yet declared. **What would change this verdict:** an SPY/QQQ December distribution declaration, or any issuer announcement of a raise/cut/special.

**Sources:** Nasdaq dividends calendar API (`https://api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD`, per-date Nov 20–Dec 18, 2026); Yahoo v7 quote (cookie+crumb, 16:30 ET) + v8 chart (5-day closes); Microsoft newsroom Sep 15, 2026: https://news.microsoft.com/source/2026/09/15/microsoft-announces-quarterly-dividend-increase-7/ ; NVDA Q3 FY2027 release Nov 17, 2026; desk standard `~/workspace/hedge-desk-research/dividend-count-standard.md`

---

# 3. Overnight Premium desk (IV)

## IV-inputs file status — FRESH but its ATM IVs are EXPIRED (STALE as levels)
- File: `~/workspace/hedge-desk-research/nightly/2026-11-19-iv-inputs.json`, `as_of` **2026-11-19T21:57:07-07:00** — ~15.5h old at run start, **within the 26h guard → FRESH**. Label: yesterday's post-close pull.
- **ATM IVs in that file are NOT usable today [FACT]:** all six are DTE=1 on expiry **2026-11-20 (today)** — the expiry moment (16:00 ET) passed before this pull. The file's prints (SPY 34.1%, QQQ 51.2%, AAPL 35.8%, MSFT 52.1%, NVDA 82.4%, TSLA 71.7%) are solver residuals on dead contracts, not tradeable IV. No IV level is taken from this file.
- Realized 20d in that file (window 2026-10-22 → 2026-11-18): SPY 23.5%, QQQ 36.1%, AAPL 27.6%, MSFT 37.6%, NVDA 52.2%, TSLA 59.9%.

## Stale-jump screen — ALL SIX SYMBOLS WINDOW-CONTINGENT
Live realized window (2026-10-23 → 2026-11-19, 20 closes, 19 log returns, ann. ×√252) — the single-day driver is Nov 5 for SPY/QQQ/NVDA/TSLA and Nov 4 for AAPL/MSFT:

| Symbol | Realized 20d (live) | Max single-day variance share | Driver day | Window-contingent? |
|---|---|---|---|---|
| SPY | 24.3% | 0.461 | Nov 5, −4.51% | YES |
| QQQ | 36.7% | 0.450 | Nov 5, −6.71% | YES |
| AAPL | 27.9% | 0.482 | Nov 4, +5.17% | YES |
| MSFT | 37.9% | 0.402 | Nov 4, +6.47% | YES |
| NVDA | 52.3% | 0.354 | Nov 5, −9.72% | YES |
| TSLA | 60.6% | 0.495 | Nov 5, −11.40% | YES |

[FACT] Any IV-vs-realized verdict built on these windows is **WINDOW-CONTINGENT**, never clean. One day drives 35–50% of 20-day variance. What would change it: the Nov 4/5 returns aging out of the 20-day window (~Dec 4–7) or a second comparable move diluting the share below 30%.

## Live Yahoo pull — today's close snapshot (labeled live, not the file)
Source: Yahoo v7 options (cookie+crumb handshake; crumb acquired, 0 failures) + v8 chart. As-of **2026-11-20 13:30 PT / 16:30 ET**; quotes are the **16:00 ET close**.

**Context — broad rout at the close [FACT, Yahoo v8 chart close vs Nov 19 adj close]:** SPY 689.81 (−3.64%), QQQ 608.45 (−5.69%), AAPL 342.56 (−1.90%), MSFT 484.52 (−2.77%), NVDA 125.53 (**−14.01%**), TSLA 345.82 (−7.64%). NVDA's −14% is corroborated by a second basis (Motley Fool: NVDA −13.80% to below $126; WSJ: 14% decline Friday, worst week since 2008, weekly −23%; Barron's: Reuters reported an SEC accounting probe Friday). The broad selloff is corroborated (Fool: S&P 500 −3.95%, Nasdaq Composite −5.52% intraday). NVDA is now down seven straight sessions.

| Symbol | ATM IV, nearest live expiry (Nov 23, 3 DTE) | ATM IV, Dec 18 (28 DTE) | Realized 20d | IV (Dec 18) vs realized |
|---|---|---|---|---|
| SPY | 24.8% (call 31.3 / put 18.3) — strike 700 vs spot 689.81, low-confidence, see flags | **30.8%** (call 33.4 / put 28.2) | 24.3% | Above (+6.5pp) — WINDOW-CONTINGENT |
| QQQ | 45.1% (call 54.3 / put 35.8) — strike 600 vs spot 608.45, low-confidence, see flags | **41.1%** (call 45.5 / put 36.7) | 36.7% | Above (+4.4pp) — WINDOW-CONTINGENT |
| AAPL | 30.8% (call 35.4 / put 26.1) | **31.5%** (call 33.6 / put 29.3) | 27.9% | Above (+3.6pp) — WINDOW-CONTINGENT |
| MSFT | 43.4% (call 42.6 / put 44.2) | **43.3%** (call 44.7 / put 42.0) | 37.9% | Above (+5.4pp) — WINDOW-CONTINGENT |
| NVDA | 95.3% (call 103.4 / put 87.2) — crossed quotes, low-confidence | **77.8%** (call 81.0 / put 74.7) — put crossed, lower-confidence | 52.3% | Above (+25.6pp) — WINDOW-CONTINGENT |
| TSLA | 56.4% (call 59.7 / put 53.1) — put crossed, lower-confidence | **63.3%** (call 65.5 / put 61.2) | 60.6% | Above (+2.7pp) — WINDOW-CONTINGENT |

**Day-over-day move in Dec 18 ATM IV vs yesterday's Dec 18 print [FACT]:** SPY 23.4% → 30.8% (+7.4pp); QQQ 32.1% → 41.1% (+9.0pp); AAPL 25.3% → 31.5% (+6.2pp); MSFT 34.2% → 43.3% (+9.1pp); NVDA 52.9% → 77.8% (**+24.9pp**); TSLA 51.3% → 63.3% (+12.0pp). IV repriced sharply higher across the board on today's selloff — the pattern flipped from yesterday (Dec 18 IV at/below realized on all six) to above realized on all six. [INFERENCE on the cause: the selloff repriced IV; the flip itself is FACT.]

## Term structure & earnings
- **Term structure [FACT from the two sampled expiries]:** AAPL flat (30.8% → 31.5%); MSFT flat (43.4% → 43.3%); QQQ front-elevated (45.1% → 41.1%); NVDA front-elevated (95.3% → 77.8%, both prints low-confidence); SPY upward-sloping (24.8% → 30.8%, front print low-confidence); TSLA upward-sloping (56.4% → 63.3%). No clean event hump is readable — the front prints are noisy (see flags) and no earnings sit in the window.
- **Earnings inside the window: none [FACT].** Nasdaq earnings-calendar sweep Nov 20 – Dec 4 (this session) returned no watchlist name; the file's `next_earnings` is null for all six. NVDA reported Nov 17 after close (already passed), AAPL/MSFT reported late Oct. **Premium into a binary event = avoid: no watchlist name currently carries that flag.**
- **IV above realized (all six) is NOT a premium-selling signal [INFERENCE per the desk's sanity-check rule]:** every comparison is window-contingent, and today's IV jump is a same-day repricing on a −14% NVDA / −5.7% QQQ tape, not a measured premium-vs-realized edge. What would change it: Nov 4/5 aging out of the window (~Dec 4–7) restoring a clean realized baseline, plus a sourced IV-history series establishing rank.

## IV rank — UNVERIFIED
No IV history is available from free sources in this pull; **IV rank cannot be computed — UNVERIFIED, never guessed.** No symbol is flagged "elevated IV rank" on this evidence. What would change it: a sourced IV-history series (e.g., a paid vol feed or a built local IV history).

## Data-quality flags
- **NVDA crossed markets on both sampled expiries [FACT]:** Nov 23 call bid $5.75 / ask $5.60, put bid $4.50 / ask $4.10; Dec 18 put bid $11.05 / ask $10.50. Both NVDA IV prints rest partly on crossed legs — treat as lower-confidence than the other names' Dec 18 prints.
- **TSLA Nov 23 put crossed [FACT]:** bid $7.55 / ask $6.95 — the 56.4% front print is lower-confidence; the Dec 18 print (bid/ask normal) is the usable TSLA tenor.
- **SPY/QQQ Nov 23 ATM strikes are off-spot [FACT]:** SPY ATM strike 700 vs spot 689.81 (nearest overlapping call/put strike; 690 lacked a two-sided IV pair); QQQ strike 600 vs spot 608.45. Call IV exceeds put IV by 12.9pp (SPY) and 18.5pp (QQQ) at those strikes — the front prints are not clean ATM reads. Dec 18 call–put gaps are narrower but still wide (SPY 5.2pp, QQQ 8.8pp, AAPL 4.3pp, MSFT 2.7pp, NVDA 6.4pp, TSLA 4.3pp) vs 1.8–3.8pp yesterday.
- Call IV > put IV at Dec 18 on all six names — **[FACT as printed]**, but these are Yahoo solver marks on American options around dividends; no parity-violation claim is made. Put-call/box parity was **not independently verified** from this pull (only ATM legs sampled, no rates/dividend inputs) — **UNVERIFIED**, no violation asserted.
- All other sampled ATM legs had two-sided live quotes (bid/ask present, non-degenerate) — [FACT].

## Verdict (thesis / evidence / what would change it)
- **Thesis:** No premium edge is demonstrable today. Dec 18 IV now sits above jump-inflated realized vol on all six names after a violent repricing day, but every comparison is window-contingent, IV rank is unverified, and the front-month prints are noisy (crossed quotes, off-spot strikes). Today's tape is a risk event to observe, not a premium to sell into — NVDA's −14% day on an SEC-probe report is exactly the kind of headline vol that punishes short premium.
- **Evidence:** Dec 18 ATM IV up 6–25pp day-over-day on all six; realized windows still 35–50% single-day-driven; no watchlist earnings within 45 days; NVDA −14.01% to $125.53 (second basis: Fool/WSJ/Barron's).
- **What would change it:** Nov 4/5 aging out of the window (~Dec 4–7) restoring a clean realized baseline; a sourced IV-history series establishing rank; or IV settling back toward realized on a calm tape after the NVDA headline clears.

**Sources:** `~/workspace/hedge-desk-research/nightly/2026-11-19-iv-inputs.json` (as_of 2026-11-19T21:57:07-07:00); Yahoo v7 options + v8 chart, live pull 2026-11-20 16:30 ET, cookie+crumb; Nasdaq earnings calendar API sweep Nov 20 – Dec 4, 2026 (no watchlist rows); NVDA corroboration: https://www.fool.com/investing/2026/11/20/nvidia-stock-plunge-wipes-out-nearly-usd500-billion-in-one-day-as-sec-reportedly-probes-its-accounting/ ; https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-11-20-2026/card/nvidia-stock-is-having-its-worst-week-since-2018-jIhbOst83m4aksKYQ5YK ; https://www.barrons.com/articles/nvidia-stock-fall-ai-chips-835a38ae ; technique: `~/workspace/custom-skills/local-cfa-financial-analysis/references/derivatives_options.md`

---
# 4. Open Quant/AI Model Lab — 2026-11-20

Sweep: arXiv q-fin new submissions announced Fri 20 Nov 2026 (submitted 18–19 Nov) + search leg.
GitHub leg SKIPPED per the run brief's ban on GitHub operations — no new-repo discovery, no repo re-checks, no repo contents/license verification. All scores run through the repo scorer (`hedge_desk.research_intelligence.assess_source`), never hand-scored. All paper claims below are source-reported UNVERIFIED (abstract only, full paper not read) unless stated otherwise. Evidence labels per `local-cfa-financial-analysis/references/evidence_standards.md`.

## Coverage control

- arXiv API `submittedDate:[202611190000 TO 202611192359]` returned 13 v1 items.
- Listing page (Fri 20 Nov, read at source): 15 new + 5 cross-list + 8 replacements. The listing caught 4 items the range query missed: **2611.25047** (submitted 18 Nov 19:00:45Z — AFTER yesterday's cutoff 18:47:16Z, so it was genuinely uncovered, not a miss), and 2611.25869 / 2611.26168 / 2611.26338 (all econ.GN-primary, out of scope). The no-filter top-40 control agrees with the range query on the 13 q-fin items.
- Replacements (8): 1910.14023, 2408.03134, 2505.19276, 2509.08096, 2510.15942, 2610.01897, 2610.16151, 2609.37957. Only 2408.03134 is in the ledger (already-excluded CAPM-equilibria theory, v3 withdrawal noted 2026-11-12) — no disposition change. No other replacement touches a ledgered item.
- SSRN leg: web search surfaced no new SSRN paper. Boucher WP7 (Zenodo, v1.2, Oct 2026) and Li/Wang arXiv:2608.26115 are already ledgered (#284 and earlier). VolModel's Nov 2–6 earnings-recap blog is a weekly data recap, not a paper — noted, no row.

## New candidates (12 scored, #312–#323)

| # | Candidate | Venue/Date | Score | Disp. | Reason (one line) |
|---|---|---|---|---|---|
| 312 | Grasselli/Stanghellini/Svaluto-Ferro — "A joint framework for SPX, VIX and VXX" | arXiv:2611.25047v1, submitted 18 Nov 2026, announced 20 Nov (q-fin.MF) | 59 | WATCH | Run's top score. Joint SPX–VIX calibration via truncated signatures; proxy errors below bid-ask (source-reported, UNVERIFIED). No code. |
| 313 | Abou Daya/Bernard/Vanduffel — "Feasible sub-replicating portfolios for basket options via the block rearrangement algorithm" | arXiv:2611.26119v1, submitted 19 Nov 2026 (q-fin.CP/q-fin.MF/q-fin.PR) | 51 | WATCH | Model-free basket-option price bounds, bracket ≤0.1% wide, sparse (2 strikes/asset); parity-adjacent. No code. |
| 314 | Qadi/Schröder/Medda — "A Three-Factor Hull-White Scenario Generator for Macro-Financial Stress Forecasting" | arXiv:2611.26200v1, submitted 19 Nov 2026 (q-fin.RM/econ.GN) | 51 | WATCH | Yield-curve → macro-outcome scenario engine, OOS 2017–2024, honest negative result (curve adds nothing once lags controlled). Desk 7 adjacent. No code. |
| 315 | Hoshisashi — "Quantum Calibration of Local-Volatility Surfaces from Sparse Option Quotes" | arXiv:2611.25344v1, submitted 19 Nov 2026 (q-fin.CP) | 47 | WATCH | Dupire LV calibration on a logical gate simulator; accepted IEEE SSCI 2027 / CIFEr. Code link stated in comment, NOT verified (GitHub leg banned). Synthetic examples only. |
| 316 | Cai et al — "Auto-Alpha: A Framework for Autonomous Factor Research" | arXiv:2611.25732v1, submitted 19 Nov 2026 (q-fin.CP) | 45 | WATCH | Band floor. LLM agent factor-research loop, 62 retained factors, CSI1000 backtest; authors flag controlled evaluation still needed. Look-ahead audit required. No code. |
| 317 | Ruelloux — "Bond yield dynamics: a multi-country multi-horizon string model" | arXiv:2611.26466v1, submitted 19 Nov 2026 (q-fin.ST) | 45 | WATCH | Band floor. Forward-rate string model extended multi-country; 1.7% reconstruction error on 9 euro-zone curves. Desk 7 adjacent. No code. |
| 318 | Qureshi — "Trading Before a Committed Rebalance" | arXiv:2611.25762v1, submitted 19 Nov 2026 (q-fin.TR) | 36 | ARCHIVE | Bayesian execution game; information value reverses under optional participation. Execution theory, no desk lane. |
| 319 | Laloux/Srinivasan — "Neckpinches in a Positively Curved Market: Ricci Flow with Surgery on the Nikkei-225" | arXiv:2611.25860v1, submitted 19 Nov 2026 (q-fin.ST) | 42 | ARCHIVE | Correlation-graph clustering via Ricci flow; Nikkei-only, descriptive. No desk transfer. |
| 320 | van der Burgt — "Statistical moments, risk weighting and percentiles of a loss distribution of a finite homogeneous credit portfolio; extending the Vasicek distribution" | arXiv:2611.25881v1, submitted 19 Nov 2026 (q-fin.MF) | 33 | ARCHIVE | Finite-portfolio Vasicek extension for Basel RWA; credit-capital, no desk lane. |
| 321 | Blanchet/Liu/Mao/Wang — "Equity and Aggregate Ambiguity" | arXiv:2611.26197v1, submitted 19 Nov 2026 (q-fin.RM/econ.GN) | 35 | ARCHIVE | Public-planning equity-vs-ambiguity theory; no desk transfer. |
| 322 | Kozhevnikov — "Optimal Control in Pairs Trading with Negative-Power Utility" | arXiv:2611.26568v1, submitted 19 Nov 2026 (q-fin.MF/math.OC) | 30 | ARCHIVE | Closed-form pairs-trading control; theory only, no empirical, no desk lane. |
| 323 | Schlegel/Mamageishvili — "Path-Independent Deleveraging Rules" | arXiv:2611.26623v1, submitted 19 Nov 2026 (cs.GT/q-fin.RM, cross-list) | 33 | ARCHIVE | Crypto-exchange auto-deleveraging rules (Hyperliquid replay); no desk transfer. |

## Per-candidate detail

### #312 — SPX/VIX/VXX joint framework (59, WATCH — run's top score)
- **What:** Specify the VIX, recover instantaneous SPX variance from the requirement that its risk-neutral 30-day conditional expected average equals squared VIX; truncated signatures of time-extended polynomial diffusions reduce the recovery to finite-dimensional linear algebra, giving explicit access to the VXX futures underlying. Regularized model + quantified pricing errors for tractable VIX/VXX proxies.
- **Claims (source-reported, UNVERIFIED — abstract only):** short-dated option smiles jointly calibrated across SPX/VIX/VXX; Monte Carlo proxy error bounds "well below quoted bid-ask spreads".
- **Desk relevance (INFERENCE):** directly the premium desk's lane — a single specification governing equity variance and rolling vol exposure, with an error bound stated against market spreads. Worth watching for code; the signature machinery is the transferable piece.
- **Scorer (run):** signal 4 / data 3 / impl 3 / risk 3 / cred 4, reproducible False. No code link in record. 37 pages, 5 figures.
- **Follow-up:** re-check code release; idea transfer — joint SPX–VIX calibration as a consistency check on the premium desk's IV screens.

### #313 — Basket-option sub-replicating portfolios via BRA (51, WATCH)
- **What:** Sub-replicating portfolios of vanilla options for a basket call when marginals are known and dependence is not; n-asset problem reduced to n two-asset problems (Hobson–Laurence–Wang 2005a), Block Rearrangement Algorithm approximates the minimising dependence. Cash component exact → valid lower bound; reassembled BRA output gives an upper bound by quadrature.
- **Claims (source-reported, UNVERIFIED — abstract only):** log-normal 3- and 6-asset examples, bracket relative width ≤0.1%; portfolios sparse (two strikes per asset); bounds tighter than general-purpose multi-marginal optimal transport on a grid.
- **Desk relevance (INFERENCE):** model-free price bounds are parity-adjacent — deterministic math outranks model output, same doctrine as #305 (TP2). Basket options themselves are not on the watchlist; the bound construction is the transfer.
- **Scorer (run):** signal 4 / data 3 / impl 2 / risk 3 / cred 3, reproducible False. No code link in record.
- **Follow-up:** re-check code release; idea transfer — BRA/bracketing pattern for multi-asset option bounds.

### #314 — Three-factor Hull-White scenario generator (51, WATCH)
- **What:** Scenario engine mapping a yield-curve path into macro-financial outcomes. Three-factor Hull-White generates arbitrage-free curves simulated under the physical measure (market price of risk estimated and reported); Minnesota-prior VARX maps curves into weekly equity returns, fed funds rate, Weekly Economic Index, inflation, and a bank Marginal Expected Shortfall proxy; sign-restricted policy shock at weekly frequency.
- **Claims (source-reported, UNVERIFIED — abstract only):** OOS 2017–2024, term-structure block lowest forecast error in 13 of 20 maturity/horizon cells; density forecasts well calibrated. Honest negative result: at weekly frequency the curve carries no incremental information once own lags are controlled — the engine's value is conditioning on a specified curve path, which no benchmark can do.
- **Desk relevance (INFERENCE):** Desk 7 adjacent — curve-path conditioning is exactly the rates desk's scenario question (what does a given curve path imply). The honest null on incremental information is the kind of result the desk trusts.
- **Scorer (run):** signal 3 / data 4 / impl 2 / risk 3 / cred 3, reproducible False. No code link in record. 33 pages, 3 figures, 15 tables.
- **Follow-up:** re-check code release; idea transfer — curve-path-conditioned scenarios for Desk 7 stress reads.

### #315 — Quantum local-vol calibration (47, WATCH)
- **What:** Hybrid quantum/classical calibration of Dupire local-vol surfaces from sparse quotes; positive-coefficient local-variance representation, Hamiltonian-simulation pricing evolution, measurement counts as the classical optimiser's objective. Implemented in a logical gate simulator; assessed against classical solvers and alternative surface models.
- **Claims (source-reported, UNVERIFIED — abstract only):** multi-maturity synthetic examples reconstruct smiles/skews; gate counts and sampling budgets identify the main computational costs.
- **Status (FACT, from arXiv record):** accepted at IEEE SSCI 2027 / CIFEr; comment states code at github.com/khoshisashi/quantum-local-vol — contents and license NOT verified (GitHub leg banned this run), so reproducibility remains unestablished.
- **Desk relevance (INFERENCE):** vol-surface calibration is a desk lane, but this is a gate-simulator proof of concept on synthetic data — years from desk use. WATCH on the code link and the conference version, not on the quantum path.
- **Scorer (run):** PEER_REVIEWED (accepted), signal 3 / data 2 / impl 2 / risk 2 / cred 4, reproducible False.
- **Follow-up:** re-check repo contents + license via a permitted leg.

### #316 — Auto-Alpha autonomous factor research (45, WATCH — band floor)
- **What:** Framework connecting report-guided initialization to self-directed research through a test-driven implementation loop: idea agent proposes mechanisms/signals, research agent develops them with backtest feedback; semantic audit, quantitative review, human admission select factors for a persistent library; Experience Library retains insights. Starts from 120 research reports → 32-factor library, then 420 implementations, 62 additional factors retained.
- **Claims (source-reported, UNVERIFIED — abstract only):** fixed 105-factor snapshot, median 1-day Rank IC 0.0301; weekly Top-300 portfolio 16.81% annualized after stated costs over 2020–2026 vs 1.71% for CSI 1000. Authors' own caveat: "controlled evaluation is needed to isolate the contribution of its components."
- **Desk relevance (INFERENCE):** factor-research process design transfers to the purged walk-forward lane — but the backtest is China A-shares (CSI1000), retrospective, and the retained-factor library is selection-shaped. Look-ahead audit required before any use (same caution as #306).
- **Scorer (run):** signal 3 / data 3 / impl 2 / risk 2 / cred 3, reproducible False. No code link in record.
- **Follow-up:** re-check code release; do NOT adopt the pipeline without a look-ahead audit.

### #317 — Bond yield dynamics string model (45, WATCH — band floor)
- **What:** Extends the Baaquie–Bouchaud (2004) / Le Coz–Bouchaud (2024) forward-rate string model to multi-country government bond markets; each country gets an idiosyncratic time scale structuring cross-curve interactions, reproducing the asymmetry of cross-country correlation blocks.
- **Claims (source-reported, UNVERIFIED — abstract only):** captures the full set of cross-curve correlations simultaneously at daily and intra-day frequencies; calibrated on 9 euro-zone countries, typical reconstruction error 1.7%.
- **Desk relevance (INFERENCE):** Desk 7 adjacent — yield-curve dynamics and cross-country correlation structure. Euro-zone only; US curve transfer is the open question.
- **Scorer (run):** signal 3 / data 3 / impl 2 / risk 2 / cred 3, reproducible False. No code link in record.
- **Follow-up:** re-check code release; US-curve applicability is the transfer question.

### #318–#323 — ARCHIVE on band discipline (30–42)
- **#318 (36):** Qureshi, rebalance execution game — information value reverses under optional participation; execution theory, no desk lane.
- **#319 (42):** Laloux/Srinivasan, Ricci-flow Nikkei clustering — 226-node correlation graph, 29 terminal clusters; descriptive, Nikkei-only, no desk transfer.
- **#320 (33):** van der Burgt, finite-portfolio Vasicek — Basel RWA adjustment relevant only for portfolios <100 obligors; credit-capital, no desk lane.
- **#321 (35):** Blanchet et al, equity-vs-ambiguity — public-planning theory; no desk transfer.
- **#322 (30):** Kozhevnikov, pairs-trading control — closed-form HJB solution; theory only, no empirical, no desk lane.
- **#323 (33):** Schlegel/Mamageishvili, deleveraging rules — crypto-exchange ADL (Hyperliquid Oct 10 2025 replay); no desk transfer.

## Triage exclusions (no ledger rows)
- 2611.25393 Humans/AI coevolution (cs.AI/q-fin.GN cross) — out of scope.
- 2611.26180 Stablecoin runs as safe-asset stress signals (q-fin.GN) — crypto surveillance, out of scope.
- 2611.25869 National production networks, 2611.26168 legume subsidies, 2611.26338 digital-transformation structural change (all econ.GN) — out of scope.
- 2508.05022 Multivariate generalized Cox model for default times (math.PR cross) — credit-default theory, out of scope.
- 2611.25218 American Medical Directory Panel (cs.DB cross) — medical data, out of scope.
- 2611.26365 Interpreting the Morbidity Gap (stat.AP cross) — health, out of scope.

## Re-checks (arXiv API id_list, no version movement — all stay as recorded)
Core version-triggered set: #4 (2510.20699, still v1), #9 (2608.22478, still v2), #13 (2609.00332, still v1), #14 (2509.11928, still v3), #15 (2509.05911, still v1), #20 (2609.22893, still v2), #21 (2608.00616, still v3), #25 (2609.13402, still v4, 2026-11-10), #30 (2607.08500, still v3), #31 (2511.07571, still v3), #257 (2611.13616, still v2, 2026-11-12). Recent cohort: #298 (2611.22604), #299 (2611.22277), #300 (2611.23126), #301 (2611.22730), #305 (2611.23495), #306 (2611.23723), #307 (2611.23587), #308 (2611.24845), #309 (2611.24028), #310 (2611.24266), #311 (2611.24912) — all still v1.

## Run summary
- 12 new candidates scored with the repo scorer; 6 WATCH (#312–#317), 6 ARCHIVE (#318–#323).
- Run max 59 (#312, SPX/VIX/VXX joint framework) — no TEST/INTEGRATE movement.
- Ledger now ends at #323. All 12 appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md`.
- FAILED/UNVERIFIED: none failed. UNVERIFIED items: all paper claims are abstract-only (source-reported UNVERIFIED by standard); #315's stated code link is NOT verified (GitHub leg banned); #316's backtest needs a look-ahead audit before any use.

---

# 5. Weather / War / Logistics Futures Event desk

**As-of:** Fri 2026-11-20, ~13:30 PT / 16:30 ET. All prices are futures settlements or timestamped intraday prints; nothing is estimated. No federal shutdown — CR funding through Dec 11; EIA and USDA releases on schedule. No USDA report was due today except Cattle on Feed (3:00 PM ET, released — see below); the operative WASDE remains Nov 10, next WASDE Thu Dec 10. No EIA petroleum or gas report today; next EIA petroleum Wed Nov 25 (Thanksgiving shift), next gas storage also Wed Nov 25.

## Catalyst table

| # | Catalyst | What happened | Market read |
|---|---|---|---|
| 1 | **Hormuz — fourth tanker strike in five days (Fri Nov 20)** | UKMTO Warning 214-26: outbound tanker struck by unidentified projectile on port bow ~8nm north of Khasab, ~15:00 UTC, fire onboard, no casualties / no environmental impact initially reported. IRGC claimed the tanker hit a naval mine — weapon not independently verified. Follows UKMTO-confirmed *On Phoenix* projectile strike Thu Nov 19 and IRGC mine claims for 2–3 tankers Nov 18–19. | Oil fell anyway: Brent ~$91.31 (−0.7%) and Dec WTI ~$82.85 (−0.4%) at 14:14 GMT Fri; third straight weekly decline. |
| 2 | **Hormuz flows — contradiction persists, new data leans tighter** | Reuters (Fri): crude shipments through Hormuz "returned to roughly pre-war levels." Counter-evidence: S&P Global Commodities at Sea — daily vessel transits fell to 14 on Nov 9 vs 32 at end-Oct; weekly LNG transits 8 → 2 vessels/week (RegionAlert, single aggregator); ShipUniverse: weekly Hormuz transit −14.6%. Kpler preliminary ~8.5mb/d, ~half pre-war (carried from Nov 19, still unresolved). | Market is pricing the Reuters flow read, not the vessel-count read — surplus narrative winning the week. |
| 3 | **Trump–Xi–Putin trilateral, Shenzhen Thu Nov 19** | First-ever three-leader summit; joint four-point declaration: (2) "plan to increase the production and supply of refined petroleum products for the benefit of all nations" + "reaffirmed the importance of stable energy flows"; (4) "a nuclear war cannot be won and must never be fought," dialogue on nuclear risks. Declaration made **no mention of Ukraine or Iran**. Trump reiterated Iran must fully reopen Hormuz. | Oil/diesel fell on the news despite no volumes or timetable. Capital Economics (via Al Jazeera): treat as "political noise rather than the first step to boosting global fuel supplies." No enforcement mechanism stated. |
| 4 | **Houthi strike on Riyadh — confirmed, campaign seen stretching into 2027** | Thu Nov 19 pre-dawn: Houthi missile hit the 80-storey PIF Tower (KAFD), windows blown out across 7–8 floors, metal facade bent, no injuries (Saudi Civil Defense; SPA photo). Second KAFD landmark hit in 11 days (Aramco Tower Nov 8). Coalition intercepted 4 ballistic missiles + 2 drones, destroyed a launchpad in Dhamar; Saudi FM reserved right to "all necessary measures." Reuters: Saudi officials foresee the campaign stretching up to six months / well into 2027. | No physical oil-supply interruption reported. Oil rose ~0.3–0.9% Thu on the headlines, then gave it back Fri — the market treats Riyadh strikes as a Saudi-economy/Vision 2030 risk, not a prompt crude-supply risk. |
| 5 | **EIA petroleum (Wed Nov 18, week ending Nov 13) — carried, second straight build** | Commercial crude **+3.4mb to 417.8mb** (vs +0.058mb Reuters-survey / +1.0mb WSJ-survey expected); gasoline **+5.2mb to 215.9mb**; distillates **+1.6mb to 104.9mb**; total petroleum ex-SPR +9.2mb. Cushing −1.209mb to 26.147mb; SPR −3.174mb to 276.361mb (lowest since Aug 1982 per Kobeissi chart). Refinery utilization 95.2% → 95.7% (above 10-yr range). Prior week crude +4.7mb. | Bearish surprise; WTI Dec settled −3.2% Wed to $83.26. Two consecutive builds totalling +8.1mb crude. |
| 6 | **EIA natural gas storage (Thu Nov 19, week ending Nov 13) — carried** | Working gas **+20 Bcf to 3,882 Bcf** — above 5-yr-avg build (+15 Bcf), below WSJ survey (+32 Bcf). +80 Bcf (+2.1%) vs 5-yr avg, −66 Bcf (−1.7%) vs year ago. | Dec NYMEX gas closed −3.08% Thu (~$3.27); Fri intraday ~$3.18–3.24, down ~2.5–2.9% (CME snapshot 04:10 CT Fri: Dec $3.175, −2.85%). |
| 7 | **USDA Cattle on Feed — today Fri Nov 20, 3:00 PM ET** | Oct placements **1.891m head, −7.3% YoY — lowest October on record**, vs ~−3.5% expected (nearly twice the expected decline). Nov 1 on-feed 11.590m head, −1.0% YoY. Oct marketings 1.620m, −4.6% YoY (lowest October since 1996). | Bullish for deferred live-cattle (fewer cattle entering the finishing pipeline = tighter 2027 fed supply); Feb live cattle ~$227.85 midday Fri (+$0.65). Report cannot split placements by sex, so herd-rebuilding inference is UNVERIFIED. |
| 8 | **Grains — Fri close, mixed** | Dec corn **$4.34¼, −4½¢** (7th weekly decline in 8 weeks); Jan soy **$12.20¾, +13¼¢** (soymeal +$8.70 to $341.00, +~3%); Dec Chicago wheat **$5.74¼, −4¢**. Thu export-sales context carried: corn 1.59 MMT (−45% w/w, commitments −28% YoY), soy 1.50 MMT (+30% w/w, China 580,700 MT; China commitments 17.22 MMT = 69% of the 25-MMT White House target), wheat 344,800 MT (+89% w/w). IGC raised 2026-27 global wheat production +220.5m bu to 30.35bn bu. | Soy/soymeal bounce vs corn/wheat fade; wheat on track for 11th weekly decline in 12 weeks. Black Sea shipping disruption still cited as wheat support. |
| 9 | **Metals rout deepens — worst gold week in 8 months** | Spot gold **~$3,551.68 early Fri (−1.9% session, −8.9% week)** — lowest in ~14 months; Dec COMEX gold ~$3,551.90 (−3.6%). Silver ~$41.90 (−2%); copper Dec ~$5.543 (−1.61%); platinum ~$1,317, palladium ~$888.66. Driver per Reuters/Kitco: hawkish Dec-hike repricing + stronger dollar + forced liquidation from the AI-equity selloff. | Safe-haven demand is losing to rate-hike repricing for a second straight day *during* a shooting war — the Nov 19 inference strengthens. UBS (Thu) still recommends long-term gold allocation on central-bank buying. |
| 10 | **Refining / runs — Wood Mackenzie cut** | Wood Mackenzie cut its Q4 global crude-run forecast by **1.4mb/d** as the Middle East conflict drags on (via OilNOW, Nov 19). Asia MR tanker freight fell 125 Worldscale points on a benchmark Middle East route (S&P Global, Nov 18) — refined-product cargoes out of the Gulf are scarce, tankers competing for fewer cargoes. | Refined-product tightness and crude surplus can coexist while Hormuz product flows are disrupted — supports cracks even as flat crude falls. |
| 11 | **Russia–Ukraine refinery campaign — carried, no new strike reported today** | Ukrainian drone attacks on 13 Russian refineries since Nov 1; combined Russian crude-processing down ~45% since late Oct per industry sources via Reuters; Rystad: runs 4.2mb/d first 10 days of Nov vs 5.0mb/d late Oct. (Single-wire sourcing — see labels.) | Supportive for refined-product cracks; the trilateral's refined-products pledge (item 3) is in part a response to this tightness. |

## Facts

- **Oil price — [FACT]:** Thu Nov 19 settlements: Brent Jan **$92.57 (+0.64%)**, Dec WTI **$83.98 (+0.93%)**. Fri Nov 20 intraday (Reuters, 14:14 GMT): Brent **$91.31 (−0.7%)**, Dec WTI **$82.85 (−0.4%)**, Jan WTI **$82.85 (−0.2%)**. Dec WTI expires today. Weekly: Brent on track −5%, Dec WTI −6.5 to −8% — third straight weekly decline.
- **Curve — [FACT, carried from Nov 19, no fresh full-curve print verified today]:** Still in steep backwardation as of Nov 19 (OilMeme, ICE/NYMEX): Brent front vs 12m out +19.8%, WTI +14.7%; Brent Jan 2027 $92.56. Physical cash vs futures (Morgan Downey, Fri 05:34 ET): WTI cash $85.36, +$3.77 over futures; Brent cash $91.59, +$3.65 DFL — prompt physical tightness persists even as flat price falls. **A fresh 12-month curve print today is UNVERIFIED — not re-pulled this session.**
- **Nat gas — [FACT]:** EIA storage 3,882 Bcf (+20 Bcf, week ending Nov 13). US LNG feedgas record 21.2 Bcf/d (Morgan Downey, Fri). JKM Asian LNG +$1.02 (+4%) Fri on Middle East supply disruption (Morgan Downey). Europe storage 70% full vs 5-yr avg 88% (carried from Nov 19).
- **Grains — [FACT, Brownfield closing prices Fri Nov 20]:** Dec corn $4.34¼ (−4½¢); Jan soy $12.20¾ (+13¼¢); Dec soybean meal $341.00 (+$8.70); Dec soybean oil 59.81 (−28 pts); Dec Chicago wheat $5.74¼ (−4¢).
- **Cattle — [FACT, USDA NASS via Brownfield / Protein Pulse, Nov 20 3:00 PM ET]:** Nov 1 on-feed 11.590m head (−1.0% YoY); Oct placements 1.891m (−7.3% YoY, lowest October on record); Oct marketings 1.620m (−4.6% YoY). Pre-report expectations: on-feed ~99.7–99.8%, placements ~96.5%, marketings ~94.8–94.9%.
- **WASDE (Nov 10, still operative) — [FACT]:** US corn carryout 1,758mb (68mb below trade), yield 179.6 bpa; soy carryout 300mb (36mb below), record yield 53.3 bpa; wheat carryout 743mb; world wheat stocks 280.82 Mt (above top of estimate range), world soy stocks 123.50 Mt (below bottom). Season-avg prices: corn $4.60, soy $12.10. Next WASDE Thu Dec 10.
- **OPEC+ — [FACT]:** Nov 1 agreement kept December production quotas unchanged.
- **Watchlist link — [FACT]:** No watchlist name (SPY, QQQ, AAPL, MSFT, NVDA, TSLA) is directly exposed to these futures; the transmission channel is macro — oil/inflation expectations and Dec rate-hike pricing, plus the metals/equity selloff correlation (gold −8.9% week alongside the broad equity down day).

## Inference (labeled, not fact)

- **[INFERENCE]:** The market has now resolved the Nov 19 "surplus vs war premium" standoff in favour of surplus — for this week at least. Brent −5% and WTI −6.5 to −8% on the week, *after* a fourth tanker strike and a second KAFD hit, means flow continuity (Reuters' "pre-war levels" read) is what traders are pricing, not the vessel-count decline. The vessel-count data (14 transits/day vs 32) is not yet reconciled with the flow claim; if flows are being maintained by fewer, larger, or rerouted loadings, the two can coexist — but no source has shown that reconciliation.
- **[INFERENCE]:** The trilateral refined-products pledge is best read as political signalling, not a supply event: no volumes, no timetable, no mechanism, and the October Russian-diesel deal it echoes has shipped nothing because traders refuse the cargoes. It moved prices down on the headline, which is a sentiment effect, not a balance-sheet effect.
- **[INFERENCE]:** The SPR-vs-commercial split from the Nov 18 EIA print still softens the bearish headline: total US crude rose only +0.2mb once the −3.174mb SPR draw is netted against the +3.4mb commercial build. Two consecutive commercial builds (+8.1mb) remain a real loosening signal; the SPR offset is a one-week accounting nuance, not a rebuttal.
- **[INFERENCE]:** Gold's −8.9% week during a Hormuz shooting war + Riyadh strikes is now a two-day pattern, not a single-day co-movement: rate-hike repricing and dollar strength are currently the dominant force on precious metals, safe-haven demand the weaker one. What would change it: a verified Hormuz closure or a dovish turn in Dec-hike pricing.

## Speculation / Unverified — flagged, not resolved

- **CONTRADICTORY — UNVERIFIED:** Hormuz crude flows. Reuters (Fri): shipments "returned to roughly pre-war levels." Kpler preliminary (carried): ~8.5mb/d, ~half pre-war. IEA: Q3 Hormuz crude+fuels 9.1mb/d, +7% q/q, vs 21.4mb/d a year earlier. S&P Global vessel counts (14/day vs 32 end-Oct) and LNG transits (8 → 2/week) support reduced traffic but do not measure crude barrels. The desk does **not** pick one. What would change it: a Kpler/IEA/Vortexa dated flow print with a stated baseline.
- **UNVERIFIED:** IRGC claim that 2–4 tankers hit mines Nov 18–19 (counts differ by outlet; no vessel names, no UKMTO/CENTCOM confirmation). Only the *On Phoenix* projectile strike (Thu) and today's unnamed tanker (UKMTO Warning 214-26, Fri) are UKMTO-confirmed as incidents; the weapon in both cases is unidentified.
- **UNVERIFIED (single aggregator, carried):** US precision airstrikes on an IRGC missile facility on Qeshm Island (RegionAlert only); Iran shooting down a US MQ-9 east of Hormuz (PakistanTV live blog only). No corroboration surfaced today.
- **UNVERIFIED (single wire, industry sources, carried):** "45% cut in Russian refinery processing since late Oct" (Reuters citing industry sources); treat as directional, not precise.
- **UNVERIFIED:** Fresh 12-month crude curve (Brent/WTI front-vs-12m) as of today — not re-pulled this session; Nov 19 levels carried and labelled as such.
- **Nothing material:** No fresh USDA report beyond Cattle on Feed today; no US weather/logistics disruption (port, rail, hurricane) surfaced in today's sweep; no new EIA release until Wed Nov 25.

## Desk verdict

Net catalyst stance for the next 24–72h: **surplus narrative winning the week; war premium failing to hold the price.** Brent −5% / WTI −6.5 to −8% on the week despite a fourth tanker strike, a second KAFD landmark hit, and a trilateral pledge that produced no volumes — the market is pricing continued Hormuz flows and building US inventories over disruption headlines. The backwardation + physical-cash premium says prompt barrels are still tight, so the curve is pricing a surplus that arrives later, not now. **What would change it:** (a) a verified Hormuz closure or verified tanker loss (flows print, not a claim); (b) next EIA petroleum report Wed Nov 25 — a third consecutive large build would confirm the surplus read; a draw would break it; (c) any US decision on Iran strikes after the new year (Trump via Axios, carried: "we'll see what happens in Iran after the new year" — no immediate escalation signalled); (d) the trilateral pledge acquiring volumes/timetable — until then it is noise.

## Sources

- EIA WPSR Nov 18 (week ending Nov 13): https://www.oilpriceapi.com/data/inventory ; https://www.morningstar.com/news/dow-jones/202611186375/us-crude-oil-stockpiles-rise-for-second-straight-week
- Oil Fri intraday / weekly (Reuters, 14:14 GMT Nov 20): https://www.lse.co.uk/news/oil-prices-set-for-third-straight-weekly-decline-on-middle-east-export-flows-qp84b5zsu0mheqd.html ; Thu settlements: https://live.euronext.com/en/financial-news/oil-gains-iran-war-worries-and-short-covering-ahead-thanksgiving-holiday
- Hormuz Fri tanker strike (UKMTO Warning 214-26): https://www.marinelink.com/news/tanker-fire-struck-projectile-near-strait-544511 ; https://www.shipuniverse.com/news/another-tanker-catches-fire-in-hormuz-as-shipping-traffic-falls-15/
- Hormuz traffic / freight (S&P Global via OilNOW): https://oilnow.gy/news/oil-tanker-freight-rates-plunge-in-asia-as-strait-of-hormuz-attacks-disrupt-fuel-shipments
- Trilateral summit declaration: https://www.thetimes.com/business/wsj/article/trump-xi-putin-end-historic-summit-with-denunciation-of-nuclear-war-qv23d3np0 ; https://antiguatribune.com/trump-putin-xi-pledge-to-increase-global-petrol-supplies/
- Houthi Riyadh strike (Reuters Nov 19): https://srnnews.com/houthi-missile-threat-towards-riyadh-causes-damage-saudi-led-coalition-says/ ; https://www.wsj.com/world/middle-east/houthi-attack-damages-saudi-capitals-tallest-tower-f4e15874
- Nat gas storage Nov 19: https://mlq.ai/news/us-natural-gas-storage-rises-20-bcf-to-3882-bcf-in-the-week-to-nov-13-eia-says/ ; Fri gas/metals snapshot: https://thelibraryestate.com/global-commodities-market-opening-metals-extend-sharp-decline-as-hawkish-fed-bets-weigh-nov-20-2026/
- Gold worst week (Reuters via GoldRates): https://goldrates.com/news/gold-prices-plunge-14-month-low-november-2026/
- USDA Cattle on Feed Nov 20, 3:00 PM ET: https://brownfieldagnews.com/news/october-cattle-placements-all-time-low-for-the-month/ ; https://proteinpulse.beehiiv.com/p/the-protein-pulse-usda-cattle-on-feed-special-report-november-20-2026-the-sparks-group ; NASS schedule: https://www.nass.usda.gov/release/cattle-feed
- Grains Fri close: https://brownfieldagnews.com/news/closing-grain-and-livestock-futures-november-20-2026/ ; export sales / China commitments: https://www.farmprogress.com/markets-and-quotes/morning-market-review?index
- Commodity snapshot Fri (Morgan Downey): https://commoditynews.morgandowney.com/news
- WASDE Nov 10 (operative): https://agoptimus.com/november-2026-wasde-actual-vs-estimates/

---

# 6. Box / Parity Observer — Fri 2026-11-20, 13:30 PT

**Verdict: no new parity violation and no new core index-methodology document in the last few days. One new published SPX box-spread measurement (Nov 12) is worth one line: the box-implied financing curve is near the risk-free curve at the short end and ~SOFR + 120bp at the long end — a funding-cost observation, not an arbitrage opportunity.**

## Parity / box spreads — new measurement, no violation
- **FACT** (Solvinc blog, measurement run Nov 12, 2026; page re-fetched Nov 20, 2026): a parity-regression scan of the full CBOE delayed SPX chain (31,016 contracts) put the box-implied financing rate at **3.86% at 15 days** (SPXW Nov 27) rising to **5.16% at 435 days** (SPX Jan 21, 2028), vs SOFR 3.89% and 13-week T-bill 3.94% (both Nov 10, per the author). Source: https://blog.solvinc.io/posts/box-spread-financing-spx-rate-scanner/
- **FACT** (same source): the author compares the 435-day 5.16% to ~5.39% for the first tier of Interactive Brokers' margin schedule (benchmark + 1.5%), a ~23bp edge before execution costs, and states a four-leg round trip costs ~40–60bp of notional plus commissions — i.e. the edge does not survive execution at retail scale.
- **INFERENCE**: the curve shape (short end ≈ risk-free rate, long end ≈ SOFR + ~120bp) is consistent with put-call parity holding and dealers charging a term funding premium — not with a parity violation. The author's own method treats parity as the measurement tool (regressing C − P on strike per expiry, R² ≥ 0.995 gate), and 33 expiries passed that gate. What would change it: a same-day SPX/SPY/QQQ parity residual exceeding transaction costs in a published, reproducible scan.
- **FACT** (same source, method note): naive per-pair box math on the delayed CBOE feed produced impossible rates (−95.66% to +186% APR on the Nov 19 expiry) from stale-quote noise — a data-quality warning, not a market break. Any box rate quoted from a delayed feed without a parity-regression (or equivalent) filter should be treated as UNVERIFIED.
- **FACT** (arXiv, Shin): the put-call parity "carry gap" papers are not new — "The Cost of a Free Lunch" is dated Aug 24, 2026 and "The P behind Q" May 26, 2026 (arXiv:2604.19604 / 2605.12250v5). No new arXiv q-fin parity paper surfaced in this sweep. Their standing finding (quoted parity residuals near zero vs traded futures; a systematic ~37bp median carry gap vs OIS, interpreted as an implementation/funding wedge, not a price-space violation) is unchanged. Sources: https://arxiv.org/html/2604.19604 ; https://arxiv.org/pdf/2605.12250v5.pdf
- **FACT**: no published SPY/QQQ/single-name US equity parity-violation analysis from the last few days surfaced in this sweep.

## Index methodology — nothing new; standing items carried forward
- **FACT** (CBOE, updated ~Nov 9–13, 2026): three new Tuttle index methodology PDFs posted on cdn.cboe.com (Option Strategy & Capital Tail Risk Indices; US LargeCap Volatility Spread Index; US LargeCap Shallow Hedge Index). Niche strategy indices, not SPX/VIX core methodology; no watchlist impact. Sources: https://cdn.cboe.com/resources/indices/governance/Tuttle_Capital_Tail_Risk_Indices_Methodology.pdf ; https://cdn.cboe.com/resources/indices/governance/Tuttle_US_LargeCap_Volatility_Spread_Index_Methodology.pdf ; https://cdn.cboe.com/resources/indices/governance/Tuttle_US_LargeCap_Shallow_Hedge_Index_Methodology.pdf
- **FACT** (Cboe rule filing SR-CBOE-2026-085, approved Oct 30, 2026, effective Nov 1): SPX a.m.-settled options under new root **SPXO** begin listing Nov 9, 2026, with the SPX/SPXW electronic execution surcharge ($0.14/contract) extended to SPXO. A fee/symbol change, not a methodology or parity change; watch only for SPX/SPXW/SPXO quote-feed handling. Source: https://cdn.cboe.com/resources/regulation/rule_filings/approved/2026/SR-CBOE-2026-085.pdf
- **FACT** (carried forward from Nov 12 desk note; announced Oct 23, 2026, not new): S&P U.S. Style Indices methodology changes take effect before market open **Dec 21, 2026**; pro-forma files reach clients **Dec 4, 2026**. Growth drops 12-month price momentum; value adds intangibles-adjusted book-to-price and free cash flow-to-price. SPY tracks the S&P 500, not the style sub-indices, so no direct SPY composition change. Next check date: Dec 4 pro-forma files.

## Failures / gaps
- None. All searches returned and the lead source (Solvinc) was re-fetched in full.
- **UNVERIFIED**: the Solvinc box-curve numbers are a single blog measurement on a delayed feed (one author, one day, Nov 12); the reported R² = 1.0000 on every passing expiry is the author's rounded output, not independently reproduced here. Treat the 3.86% / 5.16% prints as single-source, not corroborated.
- **UNVERIFIED**: the "$375B+ in passive funds tied to the affected style gauges" figure (Bloomberg Intelligence estimate relayed by secondary sources) remains unconfirmed against a primary source — carried from Nov 12, still not primary-sourced.

**One-line version for the package:** No new parity violation or core index-methodology change; a Nov 12 SPX box-spread scan puts box financing at 3.86% (15d) to 5.16% (435d) — parity holding, long end ≈ SOFR + ~120bp, edge vs retail margin erased by execution costs; S&P style changes still effective Dec 21, pro-forma files Dec 4.

---

---

# 7. Bonds & Rates — Desk 7 — Fri 2026-11-20

**Desk status: RAN CLEAN.** Rates module `rates_environment()` returned `REAL_FRED_RATES`, as_of 2026-11-20, latest obs Nov 19. All 10 core indicators re-pulled from FRED this session (via the repo module's `fred_series_rows`); Kalshi pulled direct from API this session (~13:30 PT). Michigan final (Nov 20, 10:00 ET) verified via multiple secondhand reports of the U-M release. No Yahoo substitution anywhere. **One indicator read changed (Michigan final: 4.3% prelim → 3.7% final) but no indicator changed call. Tally unchanged: 5 HIKE / 0 CUT / 5 NEUTRAL. Call holds: 25bp hike Dec 9.** Baseline: ~/workspace/hedge-desk-research/desk7-core-indicators.md (Nov 13 snapshot).

## Most decision-relevant items

1. **Michigan final cooled hard — yr-ahead expectations 3.7%, down from the 4.3% prelim and 4.7% in October — but still fires the HIKE trigger (>3.5%).** The credibility gap vs market breakevens narrowed from 2.11pp to 1.54pp (3.7% vs 2.16%). This was the named what-would-change-it item for today; it moved toward neutral without flipping. [FACT, U-M release Nov 20 via multiple reports]
2. **Kalshi repriced toward hold and away from the tail in one session.** Dec 25bp $0.92 → **$0.90**; >25bp $0.07 → **$0.02**; hold $0.04 → **$0.11** (24h vol on hold $1.26M — the day's heaviest Dec contract). Total hike $0.99 → **$0.92**. January 25bp also fell $0.60 → $0.48. The move followed the Michigan final and Treasury Secretary Bessent's Friday pushback against a 50bp hike. [FACT, Kalshi direct pull]
3. **Bessent pushed back on 50bp — a new voice, not a voter.** Treasury Secretary Scott Bessent told CNBC Friday he would encourage the Fed not to embrace a half-point increase in December. He is not an FOMC voter; this is political pressure, not Committee guidance — but it is the first senior administration voice against the tail Waller put on the table. Chicago's Goolsbee on Thursday declined to rule out a bigger move. [FACT as reported]
4. **HY spreads widened a fifth straight session — 3.52%, +32bp since Nov 12 — still NEUTRAL, 48bp from the 4.00% watch level.** The direction is one-way and the minutes corroborated it. [FACT, FRED BAMLH0A0HYM2]
5. **No new claims print this week; next is the Thanksgiving-week release.** 4-wk avg 197,750 (Nov 7 revised 200k → 202k in FRED). No labor deterioration on any kept read. [FACT, FRED ICSA]

## Rates table (module pull, FRED, as_of 2026-11-20; latest obs Nov 19)

| Series | Nov 19 | Nov 18 | Change since Nov 18 |
|---|---|---|---|
| EFFR (fed funds effective) | 3.88% | 3.88% | 0.00 (60-day window change 0.00) |
| 2Y Treasury (DGS2) | 4.76% | 4.80% | −4bp |
| 10Y Treasury (DGS10) | 5.04% | 5.07% | −3bp |
| **2s10s slope** | **+28.0bp** | +27bp | **+1bp steepening** (Nov 13: +27bp; Nov 10: +25bp) |
| SOFR | 3.91% | 3.90% | +1bp |
| OBFR | 3.88% | 3.88% | 0bp |
| **SOFR − EFFR funding spread** | **+3bp** | +2bp | Funding calm |

Curve shape: UPWARD_SLOPING. Both ends rallied after the Michigan final; the 10Y is still +6bp above the Nov 10 anchor (4.98%) used in the Nov 13 Graham lens. [FACT, module output]

## Core-indicator table — today's reads vs Nov 19

| Indicator | Trigger rule | Today's read | Call | Change | Broker POV |
|---|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA via FRED) | HIKE if y/y >2.5% or m/m >+0.25% | **No new print.** Sep y/y +3.121%, m/m +0.317% (130.902) — still latest in FRED | HIKE | — | Anchor the discount rate to the higher regime. Oct PCE (Nov 25) is the re-anchor date and the last print that can move December. |
| Breakevens (T5YIE/T10YIE, FRED) | HIKE >2.75%; CUT <1.75% | **2.22% / 2.16% (Nov 19)** vs 2.23%/2.19% (Nov 18) | NEUTRAL | — (edged down 1bp/3bp) | Anchored; no credibility crisis. Tripwire remains a break above 2.75%. |
| Michigan expectations (MICH, U-M) | HIKE if yr-ahead >3.5% | **NEW PRINT — FINAL: yr-ahead 3.7%** (prelim 4.3%, Oct 4.7%); 5-yr 3.3% (prelim 3.4%, Oct 3.5%); sentiment 51.5 (prelim 51.0, Oct 48.0). Rel. Nov 20, 10:00 ET. FRED MICH still shows only Oct 4.7% (lags ~2 months — do not use as current) | HIKE | Read fell 60bp vs prelim; call unchanged (3.7% still >3.5%, margin now only 20bp) | The 3.7%-vs-2.16% credibility gap vs breakevens narrowed to 1.54pp — still the pressure to act, but the sharpest softening in the series this cycle. Do not average Michigan with breakevens. |
| Payrolls 3-mo avg (PAYEMS, BLS via FRED) | HIKE >+150k; CUT <+50k | **No new print.** Aug +186k, Sep +60k, Oct +165k = **+137k avg**, confirmed | NEUTRAL | — | Rule as written: NEUTRAL. Do not cherry-pick the +165k print. |
| Initial claims 4-wk avg (ICSA, DOL via FRED) | CUT if >300k; NEUTRAL <250k | **No new print.** Latest w/e Nov 14, 203k. 4-wk avg **197,750** (195+191+202+203)/4 — Nov 7 revised 200k → 202k in FRED since yesterday's read | NEUTRAL | — (avg +500 on the revision) | No action on this read. It turns first — a 4-wk avg above 300k flips labor to CUT before payrolls confirm. Next release is the Thanksgiving-week print. |
| Job openings (JTSJOL, BLS via FRED) | HIKE if 3-mo change positive | **No new print.** Sep 7,523k (Jul 7,335k, Aug 7,190k) | HIKE | — | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA via FRED) | HIKE >2.5% ann.; CUT <1.0% | **No new print.** Q3 +3.37% annualized confirmed (24,611.077) | HIKE | — | Above-trend growth removes the "restraint is biting" objection. |
| Housing starts (HOUST, Census via FRED) | CUT if −5% over 3 mo; HIKE if rising through high rates | **No new print.** Oct 1,309k; Jul→Oct −4.4% | NEUTRAL | — | One month is not "rising through high rates" — NEUTRAL, not HIKE. Nov starts is the confirmation print. |
| High-yield OAS (BAMLH0A0HYM2, ICE BofA via FRED) | CUT >5.00%; NEUTRAL <4.00% | **3.52% (Nov 19)** vs 3.47% (Nov 18): 3.20% Nov 12 → 3.52% — **+32bp in 5 sessions** | NEUTRAL | — (widening, 5th straight) | No stress yet, but the direction is one-way and the minutes corroborate it (HY spreads "widened notably," esp. data-center construction debt). Watch is a break above 4.00%; 48bp away. |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening / language turns hawkish | **New voice, not a voter:** Treasury Secretary Bessent (CNBC, Nov 20) urged the Fed not to embrace a 50bp December hike; Goolsbee (Nov 19) declined to rule out a bigger move. Standing: Oct 28 held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; minutes (Nov 18) "almost all" see further hikes as likely appropriate; "a couple" said >25bp could warrant consideration; Waller (Nov 18) for 50bp unless January is clearly signaled; Williams (Nov 18) against dramatic action | HIKE | — | Weight the Committee above any print — and above the Treasury Secretary, who does not vote. The minutes' ">25bp" sentence is the on-the-record basis for the size debate; Bessent is pressure on the tail, not on the direction. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL** (unchanged from Nov 19; Nov 13 was 5/1/4). No indicator changed call today.

## Market pricing vs indicator read

**Kalshi, direct API pull Nov 20 ~13:30 PT, Dec-2026 meeting (`KXFEDDECISION-26DEC-*`):** 25bp hike **$0.90** (bid 0.89 / ask 0.90, prev 0.91; 24h vol $240,908); more than 25bp **$0.02** (bid 0.01 / ask 0.02, prev 0.07; 24h vol $652,489); hold **$0.11** (bid 0.10 / ask 0.11, prev 0.04; 24h vol $1,261,386); 25bp cut $0.01; >25bp cut $0.01. **Total hike $0.92** (was $0.99); sum of lasts $1.05 (5-cent over-round). vs Nov 19: 25bp $0.92→$0.90 (softened), >25bp $0.07→$0.02 (tail collapsed — now cheaper than the Nov 13 $0.12 by 10 cents), hold $0.04→$0.11 (nearly tripled). [FACT]

**Kalshi further out (same pull):** Jan 2027 25bp hike **$0.48** (prev $0.60) / hold $0.49 (prev $0.40); Mar 2027 25bp **$0.54** (prev $0.59) / hold $0.40 (prev $0.38). The hiking-sequence case weakened in step with December — January is now priced as a coin flip, not the street's base case. [FACT]

**CME FedWatch — secondhand only, could not be read directly (embedded app, no public text API):** Barron's (Nov 20): 100% hike, 94% 25bp / 6% 50bp. Reuters (Nov 20): 97.3% 25bp / 2.7% 50bp. Frenzycap futures-derived replication (Nov 20, 1:51 PM ET): 96% 25bp / 4% hold. Converged range: ~94–97% 25bp, ~3–6% 50bp, ~0–4% hold. [FACT as secondhand reports; direct CME read UNVERIFIED.]

**Agreement/disagreement:** A new disagreement opened today *between* markets. Futures (FedWatch/frenzycap) still price hold at ~0–4%; Kalshi's decision market prices hold at $0.11 — nearly triple its own $0.04 yesterday. The Michigan final (3.7%) and Bessent's pushback are the only new inputs in the window, and both point the same way: softer expectations, political pressure against the tail. The tail is now priced as dead ($0.02) on Kalshi while FedWatch still gives 50bp ~3–6% — the venues disagree on the tail, not the direction. No indicator rule distinguishes 25bp from 50bp — the size call rests on Oct core PCE (Nov 25) and whether Waller's view gains a second voice on the Committee. [FACT on prices; INFERENCE on the cause of the move.]

## Verdict — Desk 7

- **Thesis:** 25bp hike on Dec 9. The decision variable (core PCE, 3.12% y/y) is 112bp above target with no softening print since Nov 13; labor shows no deterioration on any kept read (claims 197,750 avg); the Committee's own minutes say "almost all" see further hikes as likely appropriate; markets price a hike at ~92–100% depending on venue. Michigan's final softened the expectations case but did not flip it — 3.7% still fires the trigger. [INFERENCE from FACTs above]
- **Evidence:** 5 HIKE / 0 CUT / 5 NEUTRAL (unchanged); Michigan final 3.7% yr-ahead (still >3.5% trigger); minutes' "almost all" + ">25bp could warrant consideration"; Kalshi total hike $0.92, 25bp $0.90; FedWatch ~94–97% 25bp; 2s10s +28bp; SOFR–EFFR +3bp (funding calm — no market-functioning objection to hiking).
- **What would change it:** (a) **Direction (to hold):** effectively nothing on the data calendar — would require Oct core PCE collapsing (Nov 25) or a market-functioning event; Nov CPI lands Dec 10, after the decision, and cannot change December. Kalshi's hold at $0.11 is a market repricing, not a data case for a hold — no kept indicator supports it. (b) **Size (25bp → 50bp):** a hot Oct core PCE on Nov 25 (m/m ≥ +0.3% range, the Waller threshold) plus Waller gaining a second voice on the Committee; Bessent's pushback now works against this path. (c) **Size (25bp → 25bp + January signal):** a soft Oct PCE would keep 25bp but strengthen the January-hike case — though Kalshi now prices January as a coin flip ($0.48/$0.49), so the street's sequence case has weakened. (d) Claims 4-wk avg above 300k would flip labor to CUT — no sign of it (197,750). (e) Michigan is now settled for November (3.7% final); the next read on this line is the December prelim (early Dec).

## Graham lens (update to §5 of the Nov 13 doc)

10Y 5.04% (Nov 19) vs Nov 18's 5.07%: at assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) rises 48.31x → 49.02x, **+1.47%** — arithmetic, not opinion. vs the Nov 10 anchor 4.98%: 50.51x → 49.02x, **−2.95%**. Duration ≈ 8 puts the same −3bp move at about +0.24% on a 10-year position (approximation; ignores convexity). Re-anchor to 5.04%. The margin of safety is thinner by ~3% on this sensitivity vs the Nov 10 anchor: any intrinsic-value estimate carried at 4.98% overstates value by ~3%. Earnings-yield vs bond-yield spread: UNVERIFIED (no S&P earnings-yield figure from a primary source this session). The defensive read stands: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price. [FACT on yields; INFERENCE on the valuation read]

**Sources + as-of (all pulled this session unless noted):** Rates + all 10 indicators: FRED via repo module `hedge_desk.rates_desk` (rates_environment + fred_series_rows), run Nov 20 ~13:28–13:35 PT; latest obs Nov 19 unless a series is monthly (then the latest vintage is named). Michigan final: U-M Surveys of Consumers release Nov 20, 10:00 ET, via multiple secondhand reports (dpa-AFX via TradingView; investinglive; ZeroHedge) — all agree 3.7% yr-ahead, 3.3% 5-yr, sentiment 51.5; direct U-M site read not attempted. FRED MICH lags U-M by ~2 months — Oct 4.7% is FRED's latest. Kalshi: api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXFEDDECISION, direct pull Nov 20 ~13:30 PT. FedWatch: secondhand only (Barron's Nov 20; Reuters Nov 20; frenzycap FedWatch replication Nov 20). Direct CME read UNVERIFIED. Speakers: Bessent CNBC Nov 20 (Bitcoin Magazine report); Goolsbee Nov 19 (CoinCentral); Waller/Williams/Musalem Nov 18 carried from prior sessions. No source failures this session.

**UNVERIFIED items:** Direct CME FedWatch read (secondhand range only). No other UNVERIFIED items — every indicator read comes from a FRED pull or the U-M release this session.

---

## Run status & UNVERIFIED register

- **All 7 desks delivered.** No desk FAILED. No retry needed (self-recovery Rung 1 not invoked).
- **Desk parts on disk:** `parts/2026-11-20-{earnings,dividend,premium,quantlab,futures,parity,rates}.md`.
- **UNVERIFIED items (by name):** NVDA cash-flow quality (10-Q not filed); NVDA exact next report date (~Feb 23, 2027 estimate only); IV rank (all six symbols — no IV history from free sources); put-call/box parity from the Premium desk's pull (only ATM legs sampled); direct CME FedWatch read (secondhand range ~94–97% 25bp only); Hormuz crude flows (Reuters "pre-war levels" vs Kpler ~8.5mb/d unresolved); IRGC mine claims for 2–4 tankers; alleged US Qeshm airstrike and MQ-9 shootdown (single aggregator each); "45% cut" in Russian refinery processing (single wire); fresh 12-month crude curve as of today (Nov 19 levels carried, labelled); Solvinc box-curve prints 3.86%/5.16% (single-source, single-day, delayed feed); "$375B+ passive funds tied to style gauges" (unconfirmed vs primary source); AAPL consecutive-increase count (third-party figure 14, not issuer-verified); NVDA "3 consecutive years" streak figure (third-party only); #315 quantum local-vol stated code link (not verified — GitHub leg banned); all Quant Lab paper claims abstract-only (source-reported).
- **STALE items (by name):** IV-inputs file ATM IVs (DTE=1, expiry 2026-11-20 — solver residuals on dead contracts; replaced by labeled live Yahoo pull in §3).
- **Desk 7 note:** this section IS the Desk 7 deliverable; no dashboard, no second page.
