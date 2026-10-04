# Hedge-desk daily research — Sunday 2026-10-04

**As-of:** 2026-10-04 ~14:00 PDT. Markets closed (weekend). All market data anchored on the Friday 2026-10-02 session unless noted.
**Mandate:** research + input only. Paper-only context. Evidence labels FACT / INFERENCE / SPECULATION / UNVERIFIED on every material claim. CFA technique standard applied per desk. Value-investor lens: mispricings, intrinsic-value gaps, margin of safety — never risk-seeking framing.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Hard boundaries honored:** no Risk of Ruin generated or estimated; no trade authorization proposed; no licensed material reproduced; unverifiable numbers marked UNVERIFIED, never guessed. No git/GitHub operations.

**Method note on desks:** all six desks ran in parallel. The Futures Event desk agent's handoff arrived late; its section below is the agent's own work, incorporated after the initial write and cross-checked by the coordinator on WTI ($91.11 via Yahoo) and the 10Y (5.277% via Yahoo). The Overnight Premium desk's CBOE-chain snapshot was independently re-pulled by the coordinator today (CBOE delayed_quotes API, data as-of Friday's close) and confirms the desk's figures within 0.1–0.5pp on all six names — recorded in the package as a cross-check.

**Correction 2026-10-04 ~15:45 PDT:** FOMC September-meeting minutes release day verified as **Wed Oct 7, 2:00 PM ET** (was flagged UNVERIFIED: Tue 10/6 vs Wed 10/7). Sources: Federal Reserve Board October 2026 calendar (federalreserve.gov/newsevents/2026-october.htm) plus 5 concurring independent week-ahead calendars (tradingkey, Schaeffer's, SKN, cambridgecurrencies, days.to). Three in-file references updated below.

---

## Coordinator synthesis — the 5 most decision-relevant items

**1. Binary-event premium dominates four of six names; the avoid-rule binds on Oct-30/Nov-20 expiries.** TSLA 10/21 AMC (company-confirmed), MSFT ~10/27–28 (date UNVERIFIED), AAPL ~10/29 (date UNVERIFIED), NVDA 11/17 (cited, exact date UNVERIFIED) all sit inside the Oct-30 / Nov-20 expiries. Term-structure humps confirmed by an independent coordinator CBOE pull today: MSFT 28d IV 32.2% vs 7d 22.6% (+9.6pp hump), TSLA 28d 43.5% vs 7d 34.7%, AAPL 28d 25.3% vs 7d 20.9%, NVDA 49d 34.2% vs 28d 28.8%. Implied 28d moves: TSLA ±12.0%, MSFT ±8.9%, NVDA ±8.0%, AAPL ±7.0% (computed from verified IV via IV·√(T/365) — INFERENCE, standard formula). None of the four reports inside the 2-week earnings window — reconciled: the window is clear, but the expiries are not. **[FACT on IV/humps/dates; INFERENCE on avoid-rule application]**

**2. The market is pricing smaller earnings moves than last quarter's actual prints.** MSFT implied ~8.9% (desk: ~6.7% event-specific) vs +15.51% actual on 2026-07-29; AAPL implied ~7.0% (desk: ~4.5%) vs −7.35% actual on 2026-07-30. Either complacency or genuine de-risking — indistinguishable from today's data (INFERENCE). What would resolve it: the actual prints on 10/21–10/29. **[FACT on prints; INFERENCE on interpretation]**

**3. SPY is the only un-conflicted premium on the watchlist.** IV30 12.5% vs 20d realized ~10.1% = +2.4pt cushion, nearly free of single-day contamination (max-day share 29.4%, just under the 30% WINDOW-CONTINGENT line). QQQ's wider gap (18.6% vs 15.0%) is window-contingent — the stale 9/21 +2.74% day contributed 41.9% of 20-day variance; re-read it after that day rolls out. VIX closed 15.31 (−6.59% Friday), futures in contango — broad vol is not in a hedging regime, which makes SPY's modest IV premium cheap-looking insurance against the macro-dense week below (INFERENCE). **[FACT on numbers; INFERENCE on reading]**

**4. This week is macro-dense inside front-month expiries — with the 10Y at a 24-year high.** Monday: ISM Services PMI (10:00 ET). Tuesday: EIA STEO, $58B 3Y auction, API crude. Wednesday: EIA petroleum (10:30 ET), **$39B 10Y auction (1:00 PM)**; **FOMC minutes (Sep 15–16 meeting, post-hike to 3.75–4.00%) — verified Wed 10/7, 2:00 PM ET** (Fed Board October calendar; 5 independent week-ahead sources concur — correction 2026-10-04). Thursday: jobless claims, $22B 30Y auction. Friday: U-Mich sentiment prelim, **October WASDE (12:00 PM ET)**. The 10Y touched 5.34% intraweek — highest since 2002 — and settled 5.277% Friday (Yahoo). Energy: Brent–WTI spread $11.14 is the live Hormuz war premium (volumes recovered, risk-adjusted cost didn't); diesel — not crude — is the bottleneck (G7 100M-barrel emergency diesel release + China export halt), making Wednesday's EIA the week's highest-signal print. September CPI lands next Wednesday (10/14), not this week. Front-month IV may be underpricing the auction + minutes density (SPECULATION — no evidence of underpricing in Friday's chain). **[FACT on calendar/yields/energy prints; FACT on minutes day (Fed Board calendar, verified 2026-10-04); SPECULATION flagged]**

**5. The dividend window is dead, and the quant lab's one TEST item plugs a real hole.** Zero watchlist ex-dates 10/05–11/01 (verified per-name). First actionable ex-div after the window: MSFT 11/19 ($0.98, the Sept-15-declared 8% raise). NVDA now runs a $1.00/yr dividend (0.43% yield) — a cash-confidence signal, not income. On the lab side, `cme-fedwatch` (MIT, pip-installable, score 70/TEST) is the only free programmatic path to FOMC rate-path expectations found — directly usable context for this week's minutes/auction repricing of the Oct 27–28 decision. CPCV engine (61/WATCH) and the five-step IC diagnostic (58/WATCH) together strengthen the lab's own validation discipline. **[FACT]**

**Contradictions checked:** none material. Earnings-desk "window clear" and premium-desk "avoid expiries" reconcile as above. Dividend-desk closes match premium-desk spots within cents. Premium-desk snapshot cross-checked against independent coordinator pull — consistent.

---

## 1. Earnings Event desk

*As-of: Sunday 2026-10-04, ~13:40 PDT. Window: 2026-10-05 to 2026-10-18.*

### Verdict
**No watchlist name reports earnings in the window.** Each of the six names was checked individually — zero hits on the Nasdaq earnings calendar API for every date in the window, and each name's next confirmed/estimated report date falls after 10/18. Options-implied expected-move calculations are **not applicable** this run, and the desk flags **no earnings-driven premium-selling avoidances** for the coming two weeks. **[FACT]**

### Per-name earnings check

| Ticker | Next report date | Timing | Status | Source (as of 2026-10-04) |
|---|---|---|---|---|
| TSLA | Wed 2026-10-21 | After market close; Q&A webcast 5:30pm ET | **Confirmed (company-issued)** | Tesla IR press release (Q3 2026 Production, Deliveries & Deployments, issued 2026-10-02) — https://ir.tesla.com/press-release/tesla-third-quarter-2026-production-deliveries-and-deployments **[FACT]** |
| MSFT | 2026-10-27 *or* 2026-10-28 | After market close | **Estimated — exact date UNVERIFIED** (Trefis: Oct 27; smartcalendars.ai + tradingnews.com: Oct 28) | https://www.trefis.com/stock/msft/articles/617316/which-dates-could-move-microsoft-stock-most/2026-10-01 ; https://www.smartcalendars.ai/en/feeds/magnificent-7-earnings-calendar **[UNVERIFIED as to exact date; FACT that both estimates are outside the window]** |
| AAPL | 2026-10-28 *or* 2026-10-29 | After market close | **Estimated — exact date UNVERIFIED** (tradingpedia: Oct 28; smartcalendars.ai: Oct 29; consensus EPS $2.02 / rev $115.06B per tradingpedia) | https://www.tradingpedia.com/2026/10/02/apple-tests-key-technical-level-ahead-of-q4-earnings/ ; https://www.smartcalendars.ai/en/feeds/magnificent-7-earnings-calendar **[UNVERIFIED as to exact date; FACT that both estimates are outside the window]** |
| NVDA | mid–late Nov 2026 (Nov 17 / 18 / 25 cited) | After market close | **Estimated — exact date UNVERIFIED** (Trefis: Nov 17; MarketBeat: Nov 18; TipRanks: Nov 25; FY2027 Q3) | https://www.tipranks.com/stocks/nvda/earnings ; https://www.marketbeat.com/stocks/NASDAQ/NVDA/earnings/ ; https://www.trefis.com/stock/nvda/articles/616804/what-could-stop-nvidia-stock-over-the-next-six-months/2026-09-27 **[UNVERIFIED as to exact date; FACT that all estimates are outside the window]** |
| SPY | n/a | n/a | Index ETF — has no earnings | Structural fact **[FACT]** |
| QQQ | n/a | n/a | Index ETF — has no earnings | Structural fact **[FACT]** |

**Implied expected move (%):** not applicable — no watchlist name has an options-expiry-spanning binary event inside the window. **[FACT]**
**Historical average earnings-day move:** not reported — applicable only to names reporting in-window; none do. Marked UNVERIFIED by construction rather than guessed. **[UNVERIFIED]**

### Earnings releases published since Friday 2026-10-02
None — no watchlist company published an earnings release since Friday, so the CFA reading order (guidance vs consensus → GAAP statements → cash flow → segments → balance sheet) has **no new financial statements to tear down** this run. The one company release in the period is Tesla's Oct 2 Q3 2026 Production, Deliveries & Deployments update: Model 3/Y production 457,387 / deliveries 478,237; total production 464,391 / deliveries 486,532. Tesla's own release explicitly states deliveries "should not be relied on as an indicator of quarterly financial results" — per the reading order, the trade-relevant numbers (revenue, margin, cash flow) arrive with the Oct 21 release, not this update. **[FACT]**

### Desk's 3 most decision-relevant items
1. **Earnings calendar is clear through 10/18** — verified per-name, not just by absence from the daily calendar. For the Overnight Premium desk: no watchlist earnings inside the window means no automatic "premium into a binary event = avoid" flags on that basis this run. **[FACT]**
2. **TSLA Oct 21 (AMC, company-confirmed) is the nearest binary event — 3 days outside the window.** IV typically reprices as a confirmed binary event enters the near-term window (INFERENCE); the Oct 2 deliveries beat (486,532 deliveries vs 464,391 produced) sets revenue/margin expectations the Oct 21 release must validate (FACT on figures). **[FACT on dates/figures; INFERENCE on IV expansion]**
3. **MSFT's report lands the week after (Oct 27 or 28, exact date UNVERIFIED)** with the decisive number already telegraphed: Azure growth vs the ~45% constant-currency guide given on the July 29, 2026 call, plus the first read on fiscal Q1 2027 capex against the ~$175B calendar-2026 plan. Any position spanning Oct 27/28 should treat the date as not-yet-firm. **[FACT on guide/capex figures per Trefis citing the July 29 call; UNVERIFIED on exact report date]**

### What would change these verdicts
- A watchlist company confirming or moving an earnings date **into** 10/05–10/18 (recheck triggers: Tesla IR, Microsoft IR, Apple investor relations, NVIDIA IR announcements).
- Resolution of the MSFT Oct 27-vs-28 and AAPL Oct 28-vs-29 discrepancies — the "outside the window" conclusion stands regardless, but the Premium desk needs the firm date for IV positioning the following week.
- Any new earnings release or pre-announcement from a watchlist name before 10/18.

### Method notes
- Queried the Nasdaq earnings calendar API (`api.nasdaq.com/api/calendar/earnings?date=`) for each date 2026-10-05 through 2026-10-18 with a browser user agent: zero hits for all six names. **[FACT, verified via direct API responses 2026-10-04]**
- Yahoo Finance quoteSummary calendarEvents returned "Invalid Crumb" (auth required) — recorded as a source failure, not as evidence of absence; the Nasdaq API + per-name next-date sources carry the verification. **[FACT — tool failure disclosed]**
- Direct fetch of ir.tesla.com returned HTTP 403 (bot block) — Tesla's date verified instead via the company-issued BusinessWire press release carried by Tesla IR's press-release page, Morningstar, and ad-hoc-news.de, all citing the same company statement. **[FACT — failure disclosed, triangulation used]**

---

## 2. Dividend Opportunity desk

**Window:** 2026-10-05 → 2026-11-01 (4 weeks). All prices anchored on the Friday 2026-10-02 session close. All calendar/API checks run 2026-10-04.

### Window verdict: NO ex-dividend dates for any watchlist name in the window
FACT: Nasdaq's October 2026 dividends calendar API (populated current-month calendar, 182 rows, fetched 2026-10-04) contains zero watchlist entries. Nov 1, 2026 is a Sunday — a non-trading day, so no ex-date is possible on the window's final day. Combined: no watchlist name goes ex-div anywhere in the 4-week window.

### Per-name status

| Ticker | Ex-div in 10/05–11/01 window? | Most recent declared dividend | Yield at Fri 10/02 close (as-of 2026-10-02) |
|---|---|---|---|
| SPY | **No** — last ex 2026-09-18 ($1.904); next is the December distribution (not declared) | $1.889, ex 2026-09-18, paid 2026-09-21 | 0.99% (trailing $7.583 / $769.64) |
| QQQ | **No** — last ex 2026-09-21 ($0.751); next is the December distribution (not declared) | $0.751, ex 2026-09-21, paid 2026-09-23 | 0.41% (trailing $3.091 / $749.58) |
| AAPL | **No** — last ex 2026-08-10 ($0.27); nothing new declared as of 2026-10-04 | $0.27, ex 2026-08-10, declared 2026-07-30, paid 2026-08-13 | 0.32% (trailing $1.06 / $333.69) |
| MSFT | **No** — next ex-date 2026-11-19 ($0.98) sits **18 days past the window's end** | $0.98, declared 2026-09-15, ex 2026-11-19, record 2026-11-19, paid 2026-12-10 | 0.70% trailing ($3.64) / **0.76% forward-indicated ($3.92)** at $517.53 |
| NVDA | **No** — last ex 2026-09-10 ($0.25), paid 2026-10-01 (three days before the window); next expected early Dec | $0.25, ex 2026-09-10, declared 2026-08-26, paid 2026-10-01 | 0.22% trailing ($0.52) / **0.43% forward-indicated ($1.00)** at $233.95 |
| TSLA | **No — pays no dividend** (zero dividend events; Nasdaq quote API shows ex-div N/A) | Never declared | 0.00% |

Sources: Yahoo Finance v8 chart events=div (ex-dates, amounts, Friday closes); Nasdaq `api/nasdaq.com/api/calendar/dividends?date=2026-10-01` (October calendar, 182 rows); Nasdaq `api.nasdaq.com/api/quote/{AAPL,MSFT,NVDA}/dividends?assetclass=stocks` (declared/record/pay dates); Nasdaq `api/quote/TSLA/dividends` (N/A). Trailing SPY/QQQ sums from Yahoo v8, 2025-10-01→2026-10-03.

### Flagged increases (all cross-checked against issuer releases)
1. **MSFT — INCREASE, +$0.07/+8% to $0.98/quarter.** FACT: Microsoft's own release (news.microsoft.com, Sept. 15, 2026): board declared $0.98, "reflecting a 7 cent or 8% increase over the previous quarter's dividend," payable Dec. 10, 2026, record/ex-div Nov. 19, 2026. Confirmed independently by Nasdaq's quote API. Ex-date is just outside the window.
2. **NVDA — INCREASE, 25× from $0.01 to $0.25/quarter.** FACT: NVIDIA's Q1 FY2027 press release (investor.nvidia.com, May 20, 2026): board approved the increase (May 18, 2026); first $0.25 payment went to holders of record June 4, 2026, paid June 26, 2026. Nasdaq API confirms both $0.25 payments. Annualized run rate now $1.00 (0.43% indicated yield) vs. $0.04 before. Second $0.25 payment landed 2026-10-01, just before the window.
3. **AAPL — INCREASE, +4% from $0.26 to $0.27/quarter.** FACT: Apple's Q2 2026 Form 10-Q (SEC filing): "On April 30, 2026, the Company announced the Board of Directors raised the Company's quarterly cash dividend from $0.26 to $0.27 per share." Nasdaq API confirms the $0.27 payments (ex 05/11/2026 declared 04/30/2026; ex 08/10/2026 declared 07/30/2026, paid 08/13/2026).

**Cuts / specials / suspensions: none detected on any watchlist name** (FACT — full dividend histories from Nasdaq quote APIs for AAPL/MSFT/NVDA, Yahoo events for SPY/QQQ, and TSLA pays none).

### Near-window watch (INFERENCE, not yet declared)
- **AAPL's next declaration** — not yet made as of 2026-10-04. INFERENCE: per the 2025 pattern (declared 10/30/2025 alongside fiscal Q4 results → ex 11/10/2025), the next declaration likely lands with fiscal Q4 earnings in late October 2026 and the ex-date in early-to-mid November — just past the window.
- **MSFT ex-div 2026-11-19** — declared and dated (FACT), 18 days past the window; the first actionable ex-div on the watchlist after the window.
- **NVDA's next dividend** — INFERENCE: per the 2025 pattern (declared 11/19/2025 → ex 12/04/2025), expect a declaration alongside earnings in mid-November with an early-December ex-date — outside the window.
- **SPY/QQQ December distributions** — INFERENCE from quarterly pattern (2025-12-19 / 2025-12-22); exact December 2026 dates not declared (UNVERIFIED).

### The 3 most decision-relevant items
1. **Zero dividend-capture opportunity in the window.** No watchlist name goes ex-div between Oct 5 and Nov 1 — the window is dividend-dead. *What would change it:* an AAPL declaration with late-October earnings setting an ex-date on or before Nov 1 — implausible given the 2025 pattern (ex was Nov 10) and the window ends on a Sunday.
2. **MSFT's 8% raise is the freshest dividend signal on the board** (declared Sept 15, first payment Dec 10). INFERENCE: at a 0.76% forward yield the raise is immaterial to total return, but 23 consecutive years of increases plus ~24% payout ratio supports the margin-of-safety/income-growth framing for MSFT — it doesn't change any premium-selling calculus.
3. **NVDA is now a $1.00/year dividend payer** — a 25× hike that still yields only 0.43%. INFERENCE: the payout consumes roughly 2% of earnings, so it is a cash-confidence signal, not income.

**Methodology notes:** Yahoo quoteSummary dividendDate was unavailable (401 without crumb; crumb endpoints returned 404 from this network), so forward-looking dates come from Nasdaq's calendar and per-ticker quote APIs instead. Nasdaq's November 2026 calendar returns `rows: null` (not yet populated) — but the window's only November date (Nov 1) is a non-trading day, so the populated October calendar (zero watchlist hits) closes the window completely. Yields use Friday 2026-10-02 closes from Yahoo v8: SPY $769.64, QQQ $749.58, AAPL $333.69, MSFT $517.53, NVDA $233.95, TSLA $370.59.

---

## 3. Overnight Premium desk

**Data anchor:** Friday 2026-10-02 session (markets closed Sun 10-04; no fresher source exists). Chain snapshot: CBOE 15-min-delayed quotes, as-of ~13:26 PT Fri 10-02 (desk's 10-02 run, parity-consistency checks passed). Realized vol: Yahoo Finance v8 daily closes through Fri 10-02. Fresh-pull attempts by the desk today all failed (Yahoo policy-blocked; Nasdaq options API upstream 500; stooq timeout) — fail-closed, nothing extrapolated.

**Coordinator cross-check (2026-10-04 ~13:50 PDT):** independently re-pulled all six chains via CBOE's `cdn.cboe.com/api/global/delayed_quotes/options/{T}.json` (data as-of Friday's close; raw snapshots cached in the goal's hidden_files). ATM IV at ~28 DTE matches the desk's snapshot on every name: SPY 12.5 vs 12.45, QQQ 18.6 vs 18.67, AAPL 25.3 vs 25.40, MSFT 32.2 vs 32.03, NVDA 28.8 vs 28.85, TSLA 43.5 vs 43.01 — all within 0.5pp. Term-structure humps independently confirmed (see table). **[FACT]**

### IV snapshot — Friday 2026-10-02 (CBOE delayed chain)

| Ticker | Spot (Fri 10-02) | ~7d | ~28–30d | ~49–59d | Term shape | Earnings in expiry | IV rank |
|---|---|---|---|---|---|---|---|
| SPY | 769.64 (+0.79%) | 10.2% | 12.5% | 13.4% | gentle contango | None | UNVERIFIED |
| QQQ | 749.55 (+1.05%) | 15.4% | 18.6% | 19.5% | gentle contango | None | UNVERIFIED |
| AAPL | 333.60 (+0.94%) | 20.9% | 25.3% | 25.1% | hump at Oct 30 | YES — ~10-29 (est.) | UNVERIFIED |
| MSFT | 517.19 (+0.90%) | 22.6% | 32.2% | 30.9% | big hump, decays post-event | YES — ~10-27/28 (est.) | UNVERIFIED |
| NVDA | 234.22 (+1.33%) | 25.9% | 28.8% | 34.2% | hump at Nov 20 | YES — ~11-17 (cited) | UNVERIFIED |
| TSLA | 371.43 (+4.58%) | 34.7% | 43.5% | 41.4% | spike at Oct 30 | YES — 10-21 AMC (confirmed IR) | UNVERIFIED |

*ATM IVs are the coordinator's independent pull (expiries 7/28/49–59 DTE from Oct 2); desk's 10-02 snapshot agrees within 0.5pp. Call/put ATM IV parity holds (e.g., SPY 10.24 vs 10.26) — deterministic parity check passed.*

**Skew character:** UNVERIFIED — strike-level IV by delta was not measured (no put-call skew shape claimed).

**Computed 28d implied move ±** (IV·√(28/365), arithmetic from verified IV — INFERENCE): SPY 3.5% | QQQ 5.2% | AAPL 7.0% | MSFT 8.9% | NVDA 8.0% | TSLA 12.0%. Desk's event-attribution humps: AAPL ~4.5%, MSFT ~6.7%, TSLA ~8.0%, NVDA ~7.2% (event attribution INFERENCE). Cross-check vs last actual prints (FACT, from 9-30 sweep: MSFT +15.51% on 2026-07-29; AAPL −7.35% on 2026-07-30): the market is pricing earnings moves **smaller** than what these names actually delivered last quarter (INFERENCE).

### IV vs 20-day realized (FACT, with window-contingency rule applied — 30% single-day threshold)

| Ticker | 20d RV | ~30d IV | Gap | Contingent? |
|---|---|---|---|---|
| SPY | 10.07% | 12.5% | +2.4 pts | No (max-day share 29.4% — just under the line) |
| QQQ | 15.00% | 18.6% | +3.7 pts | **WINDOW-CONTINGENT** — 9/21 +2.74% day = 41.9% of variance |
| AAPL | 22.50% | 25.3% | +2.9 pts | **WINDOW-CONTINGENT** — 9/10 = 30.5% |
| MSFT | 21.71% | 32.2% | event pricing | **WINDOW-CONTINGENT** — 9/25 = 34.6% |
| NVDA | 24.25% | 28.8% | +4.6 pts | Not contingent — clean |
| TSLA | 38.03% | 43.5% | +5.0 pts | **WINDOW-CONTINGENT** — 9/4 = 32.5% |

**Weekend context touching the desk (FACT, from the 10-03 nightly scan):** VIX closed 15.31, −6.59% Friday; VIX futures curve in contango — broad options market is not in an acute hedging regime. Wednesday 10/7 carries three inside-the-window catalysts: Microsoft Windows/Surface event (Huang expected to appear in person — NVDA attention), FOMC minutes 2:00 PM, and the $39B 10Y auction, inside a $119B Tue–Thu Treasury auction gauntlet. TSLA is −23% YTD, the only red Mag 7 name (Motley Fool, Oct 1). NVDA earnings cited 11-17 on the 8/26 call (MarketBeat).

### Verdicts per name (INFERENCE — labeled, with what would change each)
- **SPY — fairly priced, modestly rich.** +2.4pt cushion, nearly window-clean — the cleanest premium on the watchlist. *Changes if:* realized overtakes IV (regime break), or the 10/7 FOMC minutes repricing macro vol.
- **QQQ — fair-to-rich, but the verdict is WINDOW-CONTINGENT.** The +3.7pt gap is inflated by the stale 9/21 day; cannot be labeled rich until that day rolls out. *Changes if:* the 9/21 day exits the 20-day window and the gap persists.
- **AAPL — fairly priced for a binary event; not a mispricing.** Gap is event pricing (hump at Oct-30 expiry, ~10-29 earnings est.) on top of a contaminated RV window. *Changes if:* earnings date shifts out of the Oct-30 expiry (hump collapses) or the 9/10 day rolls out.
- **MSFT — fairly priced for a binary event; not a mispricing.** IV30 32.2% vs RV 21.7% looks rich, but the hump is earnings-event pricing — smaller than the +15.51% last actual print. *Changes if:* an earnings-date shift, or actual print overshooting the implied move.
- **NVDA — fairly priced; cleanest single-name read.** +4.6pt gap with no window contamination; Nov-20 hump aligns with the cited 11-17 earnings. Watch item: 10/7 Microsoft event / Huang appearance may be bid into front-month IV. *Changes if:* RV accelerates past IV.
- **TSLA — fairly priced for binary risk; compensated but avoid.** +5.0pts (contingent on 9/4); confirmed 10-21 AMC earnings inside the Oct-30 expiry; IV stayed flat on Friday's +4.58% rally — vol did not chase the move (FACT). *Changes if:* realized vol breaks above IV after deliveries-print digestion, or the 9/4 day rolls out.

**Standing desk rule applied:** premium into any expiry covering a binary event (Oct 21–29 cluster: TSLA confirmed 10/21, MSFT ~10-27/28, AAPL ~10-29; NVDA ~11-17 in the Nov-20 expiry) = avoid. None of the four names reports inside the 2-week desk window (FACT, earnings desk), but all four events sit inside front-month expiries.

### 3 most decision-relevant items
1. **Binary-event premium dominates four of six names — and the market is pricing smaller moves than last time.** Term structures hump exactly over earnings dates; these gaps are event pricing, not mispricings — premium into any of the four expiries = avoid per the binary-event rule (INFERENCE).
2. **SPY is the only un-conflicted premium on the watchlist.** +2.4pts, nearly window-clean — a modest margin-of-safety cushion. QQQ's wider gap is a mirage of one stale day (9/21 = 41.9% of variance); re-read it after that day rolls out (INFERENCE).
3. **Broad vol is complacent into a macro-dense week.** VIX 15.31, −6.59% Friday, futures in contango — but ISM services (Mon), FOMC minutes + $39B 10Y auction (Wed), a $119B auction gauntlet (Tue–Thu), and the MSFT/Huang event (Wed) all sit inside front-month expiries. Front-month IV may be underpricing the week's macro density (SPECULATION — no evidence yet of underpricing in Friday's chain).

**What would change any verdict:** (1) realized vol overtaking IV on any name (regime break); (2) the 9/4, 9/10, 9/21, or 9/25 single-day contributors rolling out of the 20-day window; (3) an earnings-date shift collapsing a term-structure hump; (4) real 52-week IV-rank history becoming available (currently UNVERIFIED for all six); (5) Monday's chain showing the 10/7 macro/event cluster repricing front-month IV.

**Explicit data gaps (fail-closed):** IV figures are Friday-close chain data (coordinator cross-check), not intraday; strike-level put-call skew character UNVERIFIED; IV rank UNVERIFIED for all six names (no free IV history); MSFT/AAPL earnings dates are estimates — treated as risk zones.

Sources: CBOE 15-min-delayed chain via desk 10-02 run (~/workspace/hedge-desk-research/2026-10-02.md §3) + coordinator independent pull 2026-10-04 (CBOE delayed_quotes, raw JSON cached in goal hidden_files/2026-10-04/); realized vol via Yahoo Finance v8 daily; implied-vs-last-print cross-check via ~/workspace/hedge-desk-research/nightly/2026-09-30-iv-sweep.json; VIX/curve and weekend context via ~/workspace/hedge-desk-research/nightly/2026-10-03.md; earnings dates via the earnings desk section above (Tesla IR press release; MarketBeat NVDA 8/26 call).

---

## 4. Open Quant/AI Model Lab — sweep 2026-10-04

**Lane completed:** 2026-10-04 ~13:28–13:55 PDT. Scope: new papers, preprints, open datasets, free APIs published roughly since 2026-09-04, relevant to the desks (options microstructure, vol forecasting, earnings drift, dividend forecasting, purged walk-forward, IV estimation). Excludes the 2026-09-22 sweep items — no re-score.

Scoring: read-only run of the repo's `hedge_desk.research_intelligence.assess_source` (repo untouched). Attribute ratings are the lab's (credibility reads = inference); thresholds/dispositions are the module's. All numbers/claims below carry source + as-of timestamps per evidence_standards.md.

### Scored candidates

| # | Title (venue/date) | What it claims | Score / Disposition | Reason |
|---|---|---|---|---|
| 1 | tjdwls101010/cme-fedwatch — programmatic CME FedWatch (PyPI `cme-fedwatch`, MIT; updated ~14 days ago) | One-line Python + CLI for FOMC rate-change probabilities from CME 30-day Fed Funds futures settlements + FRED EFFR/target + Fed schedule; accuracy table pins to CME FedWatch's own numbers for 2026-09-18 to the first decimal (e.g., 2026-10-28: 42.4% hold / 57.6% hike) — https://github.com/tjdwls101010/CME-FedWatch | **70 — TEST** (TEST_BEFORE_ADOPTION) | Only free, maintained path to FOMC expectations for the futures/macro desk's rate context on premium pricing & discount rates. MIT license declared on GitHub (confirm one line → adopt path clear). Caveats: solo dev, 5 stars/3 forks; README claims "no API keys" yet reads FRED — has `target_source: "estimated"` fail-closed path when FRED unreachable (source-reported). |
| 2 | snowjug/trading-bot — Combinatorial Purged CV report + `src/research/cpcv.py` (report generated 2026-09-16 IST; file updated ~7 days ago) | CPCV with N=10 subsets, k=2 test subsets, 45 splits, 5-day purge + 2-day embargo; self-reported PBO: Velocity-5 0.31, Zen Curvature 0.28, Apex VRP 0.36 (NOT OVERFIT), MACD Crossover 0.82 (OVERFIT); purge/embargo changes PBO 8–15% vs. no-gap — https://github.com/snowjug/trading-bot/blob/HEAD/reports/CPCV_REPORT.md | **61 — WATCH** (MONITOR_FOR_EVIDENCE) | Most concrete runnable CPCV/PBO implementation surfaced since the 9/22 sweep — direct reference implementation of López de Prado Ch. 12 for the lab's own overfit vetting. Held at WATCH: strategy numbers are repo-claimed (UNVERIFIED); author unaffiliated; license undeclared → REVIEW_REQUIRED. |
| 3 | xieguaiwu/glaubenskrieg — Five-Step IC Validation Diagnostic + purged walk-forward protocol (updated ~20 days ago) | Walk-forward with train 1000d / purge 126d / val 200d / step 63d; five-step diagnostic (held-out test IC, Ridge baseline, window stability, per-stock binomial test, loss-gap analysis) that flags a v3 run where WF IC=0.14 collapsed to test IC=0.006; QLIKE + Diebold–Mariano; GARCH(1,1) reportedly beats ML on 300/300 stocks in their vol test — https://github.com/xieguaiwu/glaubenskrieg/blob/HEAD/paper/00_paper_outline.md | **58 — WATCH** (MONITOR_FOR_EVIDENCE) | Five-step checklist is a drop-in template for the lab's own candidate vetting; parameter table is a comparable reference to our walkforward harness. Held at WATCH: anonymous author(s), not peer-reviewed, dataset access unverified; the Nature (2025) reproducibility-survey claim is repo-asserted (UNVERIFIED here). |
| 4 | Buchegger & Gonon: "Arbitrage-Aware Multi-Step Forecasting of Implied Volatility Surfaces" (arXiv:2608.22478, submitted 2026-08-23) | Conditional latent-diffusion model generating joint 30-day trajectories of IV surfaces + equity returns; autoencoder regularized toward no-static-arbitrage; evaluated on SPX, beats persistence baseline in point forecasting; reproducible dataset protocol from OptionMetrics/WRDS; CC-BY-4.0 — https://arxiv.org/abs/2608.22478 | **57 — WATCH** (MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED) | Directly on the Overnight Premium Desk's mandate (SPX surface forecasting vs. persistence). Held at WATCH: not peer-reviewed; dataset needs paid OptionMetrics/WRDS license; code link published in paper but **UNVERIFIED — the GitHub URL returned 404 as of 2026-10-04**, so reproducibility is not established today. |
| 5 | Flugum, Bergsma Lovelace & Wang: "Does the Market Information Processing Context Matter?" (SSRN working paper; surfaced 2026-09-29 via Hull Tactical) | Constructs "information processing frictions" (IPF) from firms' 8-K filing history: disclosures arriving in hard-to-process environments (competing FOMC/CPI/earnings) leave unresolved information that drifts into prices later; high-IPF firms outperform low-IPF by ~3.52%/yr (source-reported via Hull Tactical) — https://www.hulltactical.com/2026/09/29/how-information-overload-can-create-market-inefficiencies/ | **48 — WATCH** (MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED) | New attention-based moderator of post-announcement drift for the Earnings Desk — complements the Subrahmanyam microcap critique by asking *when* attention was scarce rather than *what* was disclosed. Held at WATCH: read via Hull Tactical summary only (INDUSTRY_BLOG secondary source); SSRN full paper not pinned/read; Hull itself flags the identification issue (firms disclosing in busy environments may differ in other ways). |
| 6 | Wang, Liu & Vuik (TU Delft): "Latent-Space No-Arbitrage Geometry of Generative Models for IV Surfaces" (arXiv:2609.00332v1, submitted 2026-08-31) | Theory: latent codes carry a no-arbitrage margin; admissible codes form a set with zero-margin boundary; level-set dynamics can repair violating codes; applies to VAEs/GANs; tested on analytic examples + VAE on Heston surfaces — https://arxiv.org/abs/2609.00332v1 | **47 — WATCH** (MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED) | Quality-control geometry for any generative IV-surface work the lab may do later; math-first paper from established authors. No empirical market data, no verified code link, no production use today — monitor only. |
| 7 | Bhaskara & Jerfy: "Public Opinion as an Option" — Kalshi crypto event contracts as volatility hedges (arXiv:2609.14267, submitted 2026-09-13) | Treats Kalshi crypto event contracts as option contracts; dynamic Kalshi/BTC hedge portfolios reportedly outperform simplistic ones across bull/bear/flat regimes — https://arxiv.org/abs/2609.14267v1 | **22 — ARCHIVE** (INSUFFICIENT_CURRENT_VALUE) | Bitcoin + Kalshi only; zero watchlist relevance, no open dataset. |

**Negative results (inference):** no new free historical-options API surfaced this week — consistent with the 9/22 finding (Cboe delayed/yfinance snapshot-only; historical chains paid). No new dividend-forecasting paper in-window; dividend coverage stands on the prior sweep (Dong state-space, WATCH). The Buchegger code-repo 404 and the stale PyPI (0.1.0) vs. GitHub README (newer numbers) of cme-fedwatch were observed today, 2026-10-04.

### The 3 most decision-relevant items
1. **cme-fedwatch is the week's only TEST item — and it plugs a real hole.** No free programmatic path to FOMC rate-path expectations exists today; this MIT package (pip install, one dependency `curl_cffi`, CLI + API + tests) pins to CME FedWatch's own numbers and documents its failure modes honestly. Recommended next step (TEST, sandbox-only): install in a throwaway venv, call `get_probabilities("next")`, compare one settlement's output to cmegroup.com FedWatch — no repo changes until verified. (FACT: the README accuracy-table numbers are source-reported, not independently verified today — UNVERIFIED until the sandbox run.)
2. **Two independent references for the lab's validation standard arrived this month — neither INTEGRATE-ready, but together they strengthen the discipline.** snowjug's CPCV engine (61, runnable code) and glaubenskrieg's five-step IC diagnostic (58, fully-specified thresholds) both implement purged/embargoed validation with PBO/DM/QLIKE gating. Pair them with the existing TEST item (sp500-walkforward-harness): the harness is the runnable sandbox, CPCV adds the fold-combination layer, the five-step diagnostic adds the acceptance checklist.
3. **The SPX IV-forecasting frontier moved toward trajectory modeling, but usability is poor.** Buchegger & Gonon (57) is the first paper found this month to beat a persistence baseline on joint 30-day IV-surface trajectories with economic admissibility built in — exactly the Premium Desk's problem space. The dead code link and licensed-data requirement keep it at WATCH; revisit when the code repo is back online.

### Method notes
Desk section also written to ~/workspace/hedge-desk-research/parts/2026-10-04-quant-lab.md. Repo scoring run was read-only (driver in /tmp); no code changes, no git operations. No desk produced nothing: all six scoped areas covered. No new open datasets relevant to the desks found this week.

---

## 5. Futures Event desk

*As-of: Sunday 2026-10-04 ~13:30 PDT. Markets closed; all futures prints anchored to the Friday 2026-10-02 session unless noted. Geopolitical/news context from public reporting published Oct 2-4. (Desk agent handoff arrived late; this is the agent's own section, replacing the coordinator's reconstruction.)*

### 1. Catalyst calendar - this week

| Date (ET) | Release / event | Why it matters | Source |
|---|---|---|---|
| Sun Oct 4 | OPEC+ / OPEC-JMMC meeting (all day) | Supply-policy signal for crude; watch Sunday-evening futures reaction | FACT - nordfx 10/03 + linkedin market-maps 10/04 |
| Mon Oct 5, 10:00 AM | ISM Services PMI (Sep) | Services inflation read into Oct FOMC pricing | FACT - fxify trading-desk brief (~Oct 2): https://fxify.com/blog/trading-desk-brief-5-october/ |
| Tue Oct 6 | EIA Short-Term Energy Outlook (Oct) | EIA's Hormuz-flow / diesel-inventory forecast update | FACT - EIA STEO "scheduled for October 6" via tradingnews: https://www.tradingnews.com/news/ng-2-919-usd-clears-50-day-ma-as-storage-surplus-shrinks-to-3-percent |
| Tue Oct 6, 1:00 PM | $58B 3Y Treasury auction; API weekly crude stocks (4:30 PM) | First leg of the $119B auction gauntlet; API pre-read for Wednesday EIA | FACT - eoption weekly calendar: https://www.eoption.com/weekly-event-calendar-10-05-2026-10-09-2026/ |
| Wed Oct 7, 2:00 PM ET | FOMC September-meeting minutes | How far officials want to go after the Sep hike | **FACT — verified 2026-10-04.** Fed Board October 2026 calendar (http://www.federalreserve.gov/newsevents/2026-october.htm) lists "FOMC Minutes — Meeting of September 15-16" on the 7th; 5 independent week-ahead sources concur (tradingkey, Schaeffer's, SKN, cambridgecurrencies, days.to). Supersedes the earlier UNVERIFIED (Tue 10/6 vs Wed 10/7) flag. |
| Wed Oct 7, 10:30 AM | **EIA Weekly Petroleum Status Report** | Crude/gasoline/distillate stocks; lands inside the G7 diesel-release week | FACT - Dow Jones Newswires via Morningstar (Sep 11) |
| Wed Oct 7, 1:00 PM | **$39B 10Y auction** | Prices duration appetite at 24-year-high yields | FACT - eoption calendar |
| Thu Oct 8, 8:30 AM | Jobless claims; EIA natural gas (10:30); **$22B 30Y auction (1:00 PM)** | Duration gauntlet continues; claims feed the soft-labor narrative | FACT - eoption calendar |
| Fri Oct 9, 10:00 AM | U. Michigan consumer sentiment (prelim) + inflation expectations | Bonds move on the expectations pair if hot | FACT - moomoo week-ahead: http://www.moomoo.com/community/feed/a-tick-in-the-market-week-of-october-5-9-117377089994757 |
| Fri Oct 9, 12:00 PM | **USDA Oct WASDE + Crop Production** | Yield/production revisions into corn's record fund long | FACT - USDA official 2026 schedule |
| **Next week:** Wed Oct 14, 8:30 AM | September CPI | Single most important release before Oct 28-29 FOMC | FACT - fxify brief |

### 2. Futures snapshot - Friday 2026-10-02 closes

| Contract | Fri 10-02 close | Day / week move | Curve shape | Source |
|---|---|---|---|---|
| WTI front-month (CL, Nov 26) | **$91.11** | -$1.76 / -1.90% day; -$1.30 / -1.41% week; range $88.06-$93.51 | UNVERIFIED (fail closed) | FACT - EnergyNow Friday report (Oct 2): https://energynow.ca/2026/10/oil-ends-volatile-week-mixed-as-emergency-reserve-release-knocks-wti-lower-but-brent-holds-above-102/ ; coordinator Yahoo v8 pull confirms $91.11 |
| Brent front-month (Dec 26) | **$102.25** | -$0.06 / -0.06% day; +0.11% week; spent three sessions below $100 mid-week | UNVERIFIED | FACT - same EnergyNow report + wenewsenglish: https://wenewsenglish.com/brent-oil-rebounds-above-102-after-midweek-fall/ |
| Brent-WTI spread | **$11.14** (derived from the two closes above) | -- | Wide - crude war premium | Derived FACT (arithmetic from reported closes) |
| Natural gas (NG, Nov 26, Henry Hub) | **$3.035**/MMBtu | +$0.068 / +2.29% day; -5.04% week | UNVERIFIED | FACT - skn-finance, Oct 2 session |
| Gold (GC, Dec 26) | **~$4,172/oz** | -$33.70 Friday (DTN intraday); -3.68% week; pulled back from late-Aug high | UNVERIFIED | FACT - DTN quick-takes Oct 2 + toptradersunplugged weekly review |
| Silver (SI) | **~$60.71** | -6.77% week | UNVERIFIED | Weekly review (likely Thursday close; session UNVERIFIED) |
| Corn (ZC, Dec 26) | **$4.97-3/4/bu** | -4.5c day; below $5, below 60-day, tested $4.95 | UNVERIFIED | FACT - Grain Ledger Friday rundown Oct 2: https://chasekoopmans.substack.com/p/the-grain-ledger-rundown-friday-october (note: a DJN/Morningstar Oct 2 item printed $5.11 - session conflict, Grain Ledger used as closer-specific source) |
| Soybeans (ZS, Nov 26) | **$12.78-1/4/bu** | -5.75c day; one-month-low close | UNVERIFIED | FACT - same Grain Ledger rundown |
| Wheat (ZW, Dec 26 Chicago) | **$6.83/bu** (+0.25c day); KC Dec $7.35-1/4 (-2.25c) | 5th straight weekly loss; holding 100-day | UNVERIFIED | FACT - same Grain Ledger rundown |
| DXY (DX) | Level UNVERIFIED | -0.18 intraday Friday | UNVERIFIED | FACT on direction only (DTN Oct 2) - **precise Friday close not obtained; marked UNVERIFIED** |
| 10Y Treasury (^TNX) | **5.277%** (Yahoo); hit a **24-year high of 5.35%** in Thursday Oct 1 trading | +4bp Fri; +9.3bp WoW | n/a | FACT - Investopedia pre-open Oct 2 + coordinator Yahoo v8 pull |

### 3. Fresh catalysts - triaged

**A. Diesel is the actual bottleneck, not crude.** FACT: IEA reported ~325M of the 400M-barrel March emergency pledge already released by Oct 2; G7/Europe then agreed a fresh **100M-barrel release of diesel and other emergency reserves**; China's refiners suspended refined-product exports for October; a prospective U.S. diesel export ban hangs over the market (DJN via TradingView, Oct 2). FACT: EIA Sep STEO estimates Hormuz flows averaged only 4.9 mbpd in Q2 2026 (vs 21.6 mbpd in Q4 2025), ~6.7 mbpd of regional production shut in during August, and low diesel inventories persisting. **INFERENCE:** the curves are pricing crude-supply normalization (Brent fell sub-$100 mid-week, WTI -1.41% on the week) while refined-product tightness is unpriced-or-underpriced - diesel, not the prompt crude barrel, is where the war premium still lives. Would change the verdict: the Oct 6 EIA STEO or Oct 7 WPSR showing distillate stocks rebuilding toward the 5-yr average.

**B. Hormuz adapted, but fragile - war premium embedded.** FACT: Kpler data shows 16.5+ mbpd exited the Middle East in September, matching pre-war averages ex-Iran (Mar low was 10.5 mbpd); ~40% now bypasses Hormuz via Saudi/UAE pipelines vs 17% pre-war; Saudi restarted the East-West pipeline Sep 22; Iranian exports effectively at/near zero since the mid-July U.S. naval blockade (from ~1.7 mbpd pre-conflict). FACT: on Oct 1 an unidentified projectile hit near Saudi Arabia's Yanbu port, briefly halting tanker loading before operations resumed; origin, damage extent, and full operational impact **not independently established - UNVERIFIED**. FACT: six tankers struck in/near the strait this week; U.S. deploying an additional carrier + ~10,000 troops. **INFERENCE:** Brent's $11+ premium over WTI reflects that shippers/insurers still price attack risk on every Hormuz transit - volume recovered, risk-adjusted cost did not. Would change: a verified durable ceasefire or strait reopening to peacetime traffic patterns.

**C. Grains: record fund long meets Friday's USDA report.** FACT: Sept 30 USDA Grain Stocks report was bearish on corn; funds held a near-record ~415k-contract net long in corn (CFTC COT) and spent Friday liquidating; StoneX forecasts U.S. corn at 16.12B bu (182.1 bpa yield) vs USDA Sept 15.80B bu, and soybean yield 54.1 bpa / 4.65B bu - both above last month's USDA and record territory. FACT: Oct WASDE/Crop Production lands Friday Oct 9, 12:00 PM ET (USDA). **INFERENCE:** ZC/ZW/ZS are positioned for a two-sided surprise: long liquidation pressure into the report vs. any yield cut from dry harvest weather; options into Friday should be treated as binary-event premium (avoid per desk mandate). Would change: the Oct 9 NASS yield/production numbers themselves.

**D. Macro: soft payrolls reset the hike path; CPI on Oct 14 is the boss fight.** FACT: September NFP printed **+29K** (fxstreet, Oct 2) - soft; October hike odds fell into the low-20s; the Fed hiked in September to 3.75-4.00%; Sep CPI prints Wed Oct 14; Oct 28-29 FOMC decision. **INFERENCE:** with the 10Y at 5.277% after a 5.35% 24-year high, duration is the tax on everything with a multiple - premium pricing on watchlist names lives in a high-rate, low-growth-scare regime, which favors value-margin-of-safety framing over risk-seeking structures. Would change: a hot Oct 14 CPI pushing the October hike back above 50%.

**E. Natural gas: domestic island, calm for now.** FACT: Henry Hub Nov at $3.035; U.S. storage 3,351 Bcf as of Sep 18 (95 Bcf above 5-yr avg); EIA projects 3,969 Bcf by Oct 31 (decade-high end-October); Lower-48 production near record ~115 Bcf/d; Europe TTF 74.06 EUR (+135% y/y), JKM $29.56 (4-yr high), yet U.S. LNG terminals are capacity-bound so none of it reaches Henry Hub. **INFERENCE:** NG curve is pricing a well-supplied domestic winter - the global gas crisis is a basis trade, not a Henry Hub trade. Watchlist impact negligible.

### 4. Watchlist margin impact (all INFERENCE - none directly measured)
- **TSLA:** most exposed - diesel/refined-product tightness raises freight and outbound-logistics costs; elevated crude lifts charging/electricity input costs indirectly. Directional headwind, magnitude UNVERIFIED.
- **AAPL / MSFT / NVDA:** second-order - Red Sea / Hormuz rerouting raises component-shipping costs and transit times; diesel-constrained logistics is a supply-chain cost, not a demand shock, at these levels. NVDA's data-center customers face power-cost pressure, which could trim AI capex intensity at the margin (SPECULATION - customer capex decisions depend on many factors; flagged as speculation, not fact).
- **Valuation channel:** 10Y at 5.277% is the dominant watchlist impact - it reprices the discount rate on all four names' duration. That is an INFERENCE from rates levels, not a trade call.

### 5. Desk's 3 most decision-relevant items
1. **Diesel, not crude, is the war trade.** Crude flows recovered to pre-war volumes (Kpler), yet refined-product shipments stay severely constrained - the G7's emergency 100M-barrel diesel release + China's export halt + a possible U.S. diesel export ban make Wednesday's EIA report (Oct 7, 10:30 AM) the highest-signal scheduled print of the week. If distillate draws persist ~14% below the 5-yr average, treat energy-cost pressure on TSLA logistics as structural into Q4, not a blip.
2. **Friday Oct 9 is a double binary: USDA WASDE + Crop Production at noon, U.Mich inflation expectations at 10 AM.** Corn's near-record fund long is already unwinding into the report; any yield/production surprise moves ZC/ZW/ZS hard, and any expectations jump moves the 10Y - which at 5.277% is the single biggest valuation headwind for the watchlist. Premium into Friday = binary event; avoid per mandate.
3. **The Brent-WTI spread ($11.14) is the live war premium.** It held even as volumes normalized, because the export system now runs on pipelines, escorts, and transponder-dark ship-to-ship transfers - costlier and fragile. Any renewed Hormuz attack (six tankers struck this week; Yanbu hit Oct 1) reprices crude sharply; that is the right-tail energy shock to watch, while diesel is the already-realized left tail on margins.

**Items with no material desk finding this run:** silver (no fresh catalyst; weekly -6.77% was trend, not news), 2Y Treasury and DXY levels (UNVERIFIED - not obtained), USDA WASDE release itself (still scheduled; outcome UNVERIFIED by definition).

---
*Desk agent handoff 2026-10-04. Coordinator cross-checks: Brent-WTI spread arithmetic verified; WTI cross-checked via Yahoo v8 ($91.11, Friday close); 10Y cross-checked via Yahoo (5.277% Friday close). FOMC-minutes release day VERIFIED 2026-10-04 ~15:45 PDT: Wed Oct 7, 2:00 PM ET — Fed Board October 2026 calendar (federalreserve.gov/newsevents/2026-october.htm) + 5 concurring independent week-ahead sources (tradingkey, Schaeffer's, SKN, cambridgecurrencies, days.to). Supersedes the earlier UNVERIFIED (Oct 6 vs Oct 7) flag.*

---

## 6. Box/Parity Observer

Nothing material found today: no new index-methodology changes affecting SPY/QQQ option parity, no fresh published parity-violation analysis (only dated studies surfaced — e.g. a 2016 Thailand box-spread paper and a 1997 SSRN note on post-1987-crash SPX boxes), no splits/special dividends or option-deliverable adjustments for SPY, QQQ, AAPL, MSFT, NVDA, or TSLA in the window, and the only CBOE news — the exclusive S&P 500 options license extension through 2051 with exploratory tokenized-products language (announced 2026-09-29, reported via TradingView/SEC 8-K) — is commercial licensing, not methodology, and changes nothing about put-call or box parity math. Per the desk's deterministic-parity standard: parity relations hold as ground truth; any apparent deviation should be treated as a data/quote artifact until proven with live quotes. **[FACT — desk agent handoff 2026-10-04]**

---

## 7. Macro driver check (oil + bonds)

| Driver | Friday 2026-10-02 print | Move | Directional read |
|---|---|---|---|
| WTI front-month (CL=F) | $91.11 | −1.9% Fri; −1.4% WoW | Easing energy-cost pressure on watchlist margins (logistics, data-center power, auto freight) — marginal tailwind, INFERENCE |
| 10Y Treasury (^TNX) | 5.277% | +4bp Fri; +9.3bp WoW; touched 5.34% intraweek (highest since 2002, per market reporting) | Higher discount rates pressure growth-multiple valuations (NVDA, TSLA, AAPL); higher yields also support option premium pricing via carry — INFERENCE |
| 5Y Treasury (^FVX) | 5.055% | +5bp Fri; +4.8bp WoW | Curve: 10Y–5Y +22bp; front end anchored (13W 3.993%, −7.7bp WoW) — the long end is doing the tightening **[FACT on levels; INFERENCE on read]** |

*Note: the brief's ^TNX/^FVX mapping is 10Y/5Y (no clean Yahoo 2Y ticker exists); the 2Y leg is covered by the 13W bill at 3.993% as the front-end anchor. Causal claims are labeled INFERENCE; no causal claim is presented as fact.*

All prints via Yahoo Finance v8 chart API, coordinator pull 2026-10-04 ~13:35 PDT. **[FACT]**

---

## Cross-desk notes & data gaps

- **Desk coverage:** all six desks produced output. The Futures Event desk's handoff arrived after the initial write; its section is the agent's own work (coordinator cross-checked WTI and 10Y). No desk was silently dropped.
- **IV rank:** UNVERIFIED for all six names (no free IV-history source). Do not treat any "elevated IV" language as rank-based.
- **Earnings dates MSFT/AAPL/NVDA:** estimates only (TSLA 10/21 is company-confirmed). The Oct 21–29 cluster is a risk zone, not a dated certainty.
- **Brent/gold/silver/BTC prints:** single-source (nordfx 10/03); WTI independently verified via Yahoo.
- **Curve shapes (futures term structure beyond front month):** not pulled — UNVERIFIED.
- **What would invalidate the package's core read:** (1) an OPEC+ surprise or Hormuz escalation repricing crude; (2) FOMC minutes shifting the Oct 27–28 rate path; (3) an earnings-date shift into the Oct-30 expiry cluster collapsing term humps; (4) realized vol breaking above IV on any name.

*Research and input only. No positions, no authorizations, no Risk of Ruin. Every number above carries its source and as-of; every material claim carries its evidence label.*
