# Hedge-Desk Daily Research — Fri 2026-11-13

**Run start:** 13:30 PT · **Package as-of:** ~14:35 PT, Fri 2026-11-13
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA
**Method:** Seven desks run in parallel; synthesis below resolves cross-desk items. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; SPECULATION = labeled guess; UNVERIFIED = looked, could not confirm. Paper-only research — no trades, no Risk of Ruin, no authorization.
**Standing rules applied:** Yahoo first (cookie+crumb on v7; UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`); ^TNX = 10Y, ^FVX = 5Y, 13W bill is the front-end anchor (never 2Y); no federal shutdown — CR passed 2026-09-01, funding through Dec 11; EIA/USDA releases on schedule. Brief-correction-2026-10-05.md NOT applied (premise false).

## Summary — the 5 most decision-relevant items

1. **NVDA reports Tue Nov 17 after the close — the only watchlist earnings in the window, and the marquee one.** Consensus $2.49 EPS / ~$109B revenue vs $108B ±2% guidance. Options imply an ~8.5% move (Nov 18 straddle), ~1.8× the 4.78% average realized move over the last four prints. First report under interim CEO Colette Kress after Jensen Huang's Nov 11 resignation (8-K, Nov 12). (Earnings desk)
2. **NVDA premium into Nov 17 is the standing avoid — and the market has already marked it up.** NVDA 7-DTE (Nov 20) ATM IV is 81.30%, +38.66pp over the 3-DTE print; the Nov 20 expiry contains earnings, the Nov 16 expiry does not. (Premium desk)
3. **Every IV-vs-realized verdict today is WINDOW-CONTINGENT.** The Nov 5 crash day still drives 37–54% of each name's 20-day realized variance; 3-DTE IV sits below realized on all six names, but that gap is jump-polluted, not a clean "IV cheap" read. The window un-contaminates only after ~Nov 25. (Premium desk)
4. **Rates: the 10Y rose another 12bp to 5.10% (Nov 12 FRED); the Dec 9 call is unchanged — 25bp hike, 5 HIKE / 1 CUT / 4 NEUTRAL.** Kalshi drifted 1¢ ($0.87 25bp / $0.12 tail, total hike $0.99). Gordon multiple at g = 3.00% falls 50.51x → 47.62x (−5.71%); re-anchor the discount rate to 5.10%. (Bonds & Rates desk)
5. **Crude rallied +3.3% Brent on unverified claims, against a bearish EIA print.** EIA crude built +4.657M bbl vs a −0.7M to −3.7M draw consensus; the Houthis claimed hits on the Saudi East–West Pipeline (the Hormuz bypass) and Yanbu — no Saudi confirmation of damage. Risk premium, not confirmed supply loss. (Futures desk)

---

## 1. Earnings Event Desk

**Question:** Which watchlist names report Nov 13–27, 2026, and what does the options market price for the move?

### Earnings calendar — next 2 weeks (watchlist only)

Nasdaq earnings calendar API queried for every trading day Nov 13–27, 2026 (pulled 2026-11-13 ~13:35 PT).

| Symbol | Report date | Timing | Quarter | Consensus EPS | Notes |
|---|---|---|---|---|---|
| **NVDA** | **Tue Nov 17, 2026** | **After close; call 5:00 p.m. ET / 2:00 p.m. PT** | Q3 FY27 (quarter ended ~Oct 26, 2026) | **$2.49** (13 ests) | Only watchlist name in window |
| AAPL | — none — | — | — | — | Last reported Mon Nov 2, 2026 (after close, fiscal Q4 2026) |
| MSFT | — none — | — | — | — | Last reported Wed Oct 28, 2026 (after close, fiscal Q1 2027) |
| TSLA | — none — | — | — | — | Last reported Wed Oct 21, 2026 (after close) |
| SPY / QQQ | — n/a — | — | — | — | ETFs; no earnings |

- **FACT** (Nasdaq calendar, 2026-11-17 row): NVDA fiscal quarter ending Oct/2026, consensus EPS $2.49, 13 estimates, market cap ~$4.005T, last-year report date 11/19/2025.
- **FACT** (company-named date): NVIDIA IR named Nov 17 on the Aug 26, 2026 earnings call; Nasdaq agrees. **INFERENCE:** date is firm, not an aggregator estimate. **Caveat — FACT:** some aggregators disagree (TipRanks lists Nov 25; MarketBeat carried Nov 18 as an estimate). No separate date-announcement 8-K found on EDGAR (filings from Oct 20, 2026 onward checked 2026-11-13).
- **FACT** (AAPL/MSFT/TSLA last-report dates): TSLA Oct 21 per Nasdaq calendar; MSFT Oct 28 and AAPL Nov 2 per company IR pages as reported by secondary sources — Nasdaq's past-date calendar lookup returned no rows for those dates, so these rest on secondary confirmation.

### NVDA Q3 FY27 — setup

| Item | Read | Label / source |
|---|---|---|
| Consensus EPS | $2.49 | FACT — Nasdaq (13 ests); Zacks consensus also $2.49, revised +$0.01 over 60 days |
| Consensus revenue | ~$108.8–109.0B | FACT — Zacks $108.99B; MarketBeat $108.80B |
| Company revenue guidance (given Aug 26) | $108.0B ±2% ($105.8–110.2B) | FACT — corroborated by Zacks, MarketBeat, PrimeXBT |
| Company gross-margin guidance | 74.0% ±0.5pp (GAAP and non-GAAP) | FACT — same sources |
| Prior-year Q3 EPS | $1.30 (Zacks/MarketBeat) vs $1.24 (Nasdaq) | **CONFLICT — UNVERIFIED basis:** sources disagree; do not know which is GAAP vs non-GAAP. Zacks' +91.5% YoY EPS growth claim rests on the $1.30 base |
| Prior-year Q3 revenue | $57.01B | FACT — MarketBeat |
| Q2 FY27 actual (Aug 26 print) | Revenue $96.22B, Data Center $89B | Secondary source only — not verified at primary source |
| Guidance assumption | No Data Center compute revenue from China | Secondary source only |

### Options-implied expected move — NVDA (live Yahoo pull, Fri Nov 13 ~13:00 PT)

Pulled via Yahoo v7 options with cookie+crumb handshake. Underlying **$162.85** at pull time. Nearest expiry (Nov 13) returned dead-contract residual marks ($0.02) and was **excluded**.

| Expiry | ATM straddle (mid) | Implied move | ATM IV (call / put) | Read |
|---|---|---|---|---|
| **Wed Nov 18** (first expiry after the print) | 162.5 straddle, mid **$13.90** | **8.54%** | 82.6% / 84.4% | Cleanest event read |
| Fri Nov 20 (weekly) | 165 straddle, mid **$15.82** | **9.72%** | 80.9% / 81.7% | Includes 2 extra non-earnings days — overstated as a pure event read |

- **FACT:** Nov 18 expiry implies an ~8.5% move; Nov 20 weekly implies ~9.7%.
- **Data-quality flag:** Nov 18 call quotes were crossed at pull time (bid $7.10 > ask $7.00); the mid is still computed but quote quality is impaired — treat the 8.54% as approximate, not exact.
- **Method:** ATM straddle mid ÷ underlying price; simple-return convention; strikes nearest the $162.85 underlying.

### Historical earnings-day moves — NVDA (last 4 prints)

Computed from Yahoo v8 daily closes: simple close-to-close % on the first regular session after the after-close print (new − old, sign set by arithmetic).

| Quarter | Report (after close) | Reaction session | Close before → close after | Move |
|---|---|---|---|---|
| Q3 FY26 | Wed Nov 19, 2025 | Thu Nov 20, 2025 | $186.52 → $180.64 | **−3.15%** |
| Q4 FY26 | Wed Feb 25, 2026 | Thu Feb 26, 2026 | $195.56 → $184.89 | **−5.46%** |
| Q1 FY27 | Wed May 20, 2026 | Thu May 21, 2026 | $223.47 → $219.51 | **−1.77%** |
| Q2 FY27 | Wed Aug 26, 2026 | Thu Aug 27, 2026 | $209.66 → $227.98 | **+8.74%** |

- **FACT:** Average absolute earnings-day move over the last 4 prints = **4.78%**; signed average −0.41%; 3 of 4 prints fell. Report dates verified — Nov 19, 2025 / Feb 25, 2026 / Aug 26, 2026 via Nasdaq calendar; May 20, 2026 via NVIDIA's own IR press release. **Correction made in-run:** an initial May 27 assumption was wrong; the Q1 print was May 20, and the move above uses the corrected window.
- **INFERENCE:** Options imply ~8.5%, roughly **1.8×** the recent 4-print average realized move (4.78%). The market is pricing a bigger swing than NVDA has delivered on average — but the Aug print (+8.74%) shows an 8–9% day is inside the recent range, so the implied move is elevated, not unprecedented.
- **INFERENCE:** The recent pattern is that the print alone does not set the reaction — Q1 FY27 beat consensus on revenue (+$2.8B) and non-GAAP EPS (+$0.10) and still fell 1.77%. The guide, especially Q4 revenue and gross margin, is the swing factor (per the statement-analysis standard: guidance vs consensus first).

### Material context — first report under interim leadership

- **FACT** (SEC EDGAR, 8-K filed Nov 12, 2026, accession 0001045810-26-000082): Jensen Huang resigned as President, CEO and director (event Nov 11); the board appointed CFO Colette Kress interim CEO while it searches for a successor. This is the first earnings report and call under interim leadership — expect governance/leadership questions on the call alongside the numbers.
- **FACT:** No NVDA earnings release or statement is available yet (report is Nov 17) — no statement teardown is possible today. On Nov 18 the teardown order applies: guidance vs consensus first, then GAAP vs adjusted gap, cash-flow conversion, segment margins, balance-sheet deltas, call transcript last.

### Verdict

- **Thesis:** NVDA on Tue Nov 17 after the close is the only earnings event in the watchlist window, and it is the marquee one: consensus expects ~$109B revenue / $2.49 EPS against $108B ±2% guidance, with options pricing an ~8.5% move — well above the 4.78% recent average realized move.
- **Evidence:** Nasdaq calendar + company-named date (Nov 17, after close, call 5:00 p.m. ET); live Yahoo options pull (Nov 18 straddle $13.90 / $162.85 = 8.54%); four verified prior reaction-day moves averaging 4.78% absolute; 8-K confirming the CEO transition.
- **What would change it:** (a) a Q4 revenue guide above ~$113–114B or a margin guide holding 74% would support the priced-in move resolving upward; (b) a guide cut, margin compression blamed on memory costs, or China/restriction news would resolve it downward; (c) any company move of the date off Nov 17 — re-check the Nasdaq calendar and NVIDIA IR on Nov 16.

### Sources
- Nasdaq earnings calendar API: `https://api.nasdaq.com/api/calendar/earnings?date=2026-11-17` (and each date Nov 13–27, 2026)
- Yahoo Finance v7 options (cookie+crumb) and v8 chart, pulled 2026-11-13 ~13:00 PT
- SEC EDGAR: `https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm` (8-K, Huang resignation / Kress interim CEO)
- Zacks (Nov 12, 2026): `https://www.zacks.com/stock/news/3028349/nvidia-gears-up-for-q3-earnings-should-investors-buy-the-stock`
- MarketBeat: `https://www.marketbeat.com/earnings/reports/2026-11-17-nvidia-co-stock/`
- NVIDIA IR, Q1 FY27 release (May 20, 2026): `https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx`

**Desk status: COMPLETE.** All six names covered. One UNVERIFIED item (prior-year EPS basis conflict $1.24 vs $1.30) and one data-quality flag (crossed Nov 18 call quotes) recorded above; no numbers guessed.

---

## 2. Dividend Opportunity Desk

**Question:** Which watchlist names go ex-dividend Nov 13 – Dec 11, 2026, and is there any announced increase, cut, or special?

**Sources (as of ~13:35 PT, 2026-11-13):** Nasdaq dividends calendar API (`api.nasdaq.com/api/calendar/dividends`, queried for every weekday Nov 13 – Dec 11, 2026); Yahoo Finance v8 chart dividend events and v7 quote (cookie+crumb handshake, crumb obtained 13:35 PT); web cross-check for NVDA's 2026 raise (Motley Fool, Sep 25, 2026; Zacks dividend history, Nov 2, 2026). Prices below are Yahoo regular-market prices at fetch time, 2026-11-13 ~13:35 PT. Yields are computed as trailing/forward annual dividend ÷ that price — simple convention, stated per row.

### Ex-dividend calendar — next 4 weeks (Nov 13 – Dec 11, 2026)

| Ticker | Ex-date | Amount | Pay date | Forward annual | Yield* | Status |
|---|---|---|---|---|---|---|
| MSFT | **Thu Nov 19, 2026** | $0.98/qtr | Dec 10, 2026 | $3.92 | 0.75% | **FACT** — Nasdaq calendar + Yahoo quote agree |
| NVDA | ~Dec 10, 2026 (est.) | $0.25/qtr (if declared) | — | $1.00 | 0.61% | **UNVERIFIED** — estimate only, not declared |
| SPY | — | — | — | $5.66 (trailing) | 0.75% | **UNVERIFIED** — no ex-date published yet |
| QQQ | — | — | — | $1.77 (trailing) | 0.26% | **UNVERIFIED** — no ex-date published yet |
| AAPL | — (just went ex Nov 12) | — | — | $1.08 | 0.30% | **FACT** — ex-date was yesterday |
| TSLA | — | — | — | $0.00 | 0.00% | **FACT** — pays no dividend |

\* Yield = annual dividend ÷ Yahoo price at fetch (SPY $754.21, QQQ $679.89, AAPL $356.27, MSFT $523.88, NVDA $162.85). MSFT and AAPL yields use the forward annual rate; SPY/QQQ use trailing annual (Yahoo `trailingAnnualDividendRate`), since ETF distributions vary quarter to quarter — do not compare the two bases as if identical.

### Per-name detail

**MSFT — the only declared ex-date in the window.** **FACT:** Ex-dividend Thu Nov 19, 2026, $0.98/qtr, payable Dec 10, 2026, record Nov 19 (Nasdaq calendar API, announcement date Sep 15, 2026; Yahoo v7 quote: `dividendDate` Dec 10, 2026, forward rate $3.92). **FACT:** This is the first payment at the raised rate — the Sep 15, 2026 board raise to $0.98/qtr from $0.91, a +7.7% increase. **FACT (per the desk's standing standard, `dividend-count-standard.md`):** 24 consecutive annual increases as of this package date, the streak defined by the Sep 15, 2026 announcement. **Reconciliation note:** Nasdaq's `indicated_Annual_Dividend` field still shows $3.64 (= 4 × $0.91, the pre-raise rate) — it lags the raise; Yahoo's $3.92 (= 4 × $0.98) is the correct forward annual. $3.92 is used here and the Nasdaq field is flagged as stale, not as a second basis.

**AAPL — just went ex, no change.** **FACT:** Ex-dividend Thu Nov 12, 2026, $0.27/qtr, payable Mon Nov 16, 2026, announced Nov 2, 2026 (Nasdaq calendar API; Yahoo chart dividend event Nov 12, $0.27). **FACT:** Amount unchanged — $0.27 in May, Aug, and Nov 2026 (Yahoo 2-yr dividend history: $0.25 Feb 2025 → $0.26 May 2025 → $0.27 May 2026). The May 2026 raise to $0.27 was the last increase; the Nov 2 announcement held the rate — no increase, no cut, no special. **UNVERIFIED:** AAPL's full consecutive-increase streak length — not verified against issuer history this session, so no count is stated. Next ex-date ~Feb 2027, outside the window.

**NVDA — the 25-fold raise is old news; next date undeclared.** **FACT:** NVIDIA raised its quarterly dividend from $0.01 to $0.25 (+2,400%) on May 18, 2026; first payment at the new rate Jun 26, 2026 (ex Jun 4); latest ex-date Sep 10, 2026, paid Oct 1, 2026 (Yahoo chart events; Motley Fool Sep 25, 2026; Zacks, Nov 2, 2026). **FACT:** No future dividend has been declared — Zacks dividend history (Nov 2, 2026): "NVIDIA Corporation (NVDA) does not have any future dividends declared." **UNVERIFIED:** the ~Dec 10, 2026 next ex-date circulating on third-party trackers (Talval, Investingly, Snowball) is an estimate extrapolated from the quarterly cadence, not an announcement. It falls inside the window, so it is flagged here as a watch item, not a date. **INFERENCE:** At $1.00/yr forward against a $162.85 price, the 0.61% yield is immaterial to total return — the raise was a capital-return signal (payout jumped to ~$6.0B in fiscal Q2 per Motley Fool), not an income event; buybacks (~$19–20B/qtr) remain the real return-of-capital channel. Disconfirming check: none — no source claims a cut or a further raise.

**SPY / QQQ — no ex-date published in the window.** **FACT:** Nasdaq's calendar returned no SPY or QQQ rows for any queried date Nov 13 – Dec 11, 2026, and no rows for Dec 18 / Dec 21 either. **UNVERIFIED:** the next ex-dates for both ETFs — the usual quarterly pattern points to mid-December (third Friday), but nothing is declared/published as of today, so no date is stated. Trailing annual distributions: SPY $5.66 (yield 0.75%), QQQ $1.77 (yield 0.26%) per Yahoo v7 quote.

**TSLA — no dividend.** **FACT:** TSLA pays no dividend (Yahoo: trailing and forward rates $0.00, yield 0.0%); nothing to calendar.

### Increases / cuts / specials — flags

- **Increase (already in effect, first payment this window):** MSFT +7.7% to $0.98/qtr (announced Sep 15, 2026; first payment Dec 10, 2026). **FACT.**
- **Increase (announced earlier in 2026, no action this window):** NVDA 25× raise to $0.25/qtr (May 18, 2026); AAPL raise to $0.27/qtr (May 2026). Both already reflected in current rates. **FACT.**
- **Cuts:** none announced for any watchlist name. **FACT** (no cut appears in Nasdaq calendar or Yahoo actions for the window).
- **Specials:** none announced. **FACT** (same basis).

### Verdict

**Thesis:** The dividend desk is quiet this week — one actionable calendar event (MSFT ex-div Nov 19 at the new $0.98 rate) and one undeclared watch item (NVDA ~Dec 10 estimate). Nothing in the window changes any name's income profile or margin-of-safety math: MSFT's raise is +7.7% on a 0.75% yield, NVDA's raise is large in percentage and trivial in yield, and AAPL held its rate. **Evidence:** Nasdaq calendar scan of all weekdays Nov 13 – Dec 11 (only MSFT row returned); Yahoo chart/quote cross-checks; NVDA raise corroborated by Yahoo payment history plus Motley Fool and Zacks. **What would change it:** (1) NVDA declaring its December dividend — if declared at $0.25, the ~Dec 10 date becomes FACT and enters the calendar; if raised again, that is a new flag; (2) SPY/QQQ December ex-dates publishing (expected mid-Dec, likely just outside this window); (3) any new increase/cut announcement — none is pending on any known board calendar. **SPECULATION (labeled, not a conclusion):** if NVDA holds its quarterly cadence, a December declaration is likely, but the date and amount are unknowable until announced.

**Desk status: COMPLETE.** All six names covered; no source failures — Nasdaq calendar API and Yahoo (v8 chart + v7 quote with crumb) both returned data this session.

---

## 3. Overnight Premium Desk (IV)

**Sources and as-of:**
- **IV-inputs file (inside 26h guard, usable with STALE label):** `~/workspace/hedge-desk-research/nightly/2026-11-12-iv-inputs.json`, `as_of` **2026-11-12T14:54:31-07:00** (~23.6h old at live pull; inside the 26h freshness guard). Source: Yahoo Finance options chains + v8 chart, via `pull_iv_inputs.py`.
- **Live Yahoo pull (today):** options chains + v8 chart, cookie+crumb handshake (jar seeded via curl `fc.yahoo.com`, crumb from `query1.finance.yahoo.com/v1/test/getcrumb`), `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`. Pulled **2026-11-13 14:29–14:30 PT**. No failures on either leg.
- **Tenor note (FACT):** today's 2026-11-13 expiry died at 16:00 ET / 13:00 PT, ~30 min before run start, so the nearest *live* expiry is 2026-11-16 (3 DTE). All live ATM IVs below are 3-DTE (Nov 16) and 7-DTE (Nov 20) prints. Yesterday's file prints were 1-DTE (Nov 13 expiry) — **day-over-day IV comparisons across the two files are tenor-mismatched and are NOT a clean IV-compression read.**
- **IV rank: UNVERIFIED** — no IV history is available from free sources (Yahoo publishes point-in-time IV only); no rank can be computed without guessing.

### IV snapshot

| Symbol | Live ATM IV 3-DTE (exp 2026-11-16) as of 2026-11-13 14:29 PT | Live ATM IV 7-DTE (exp 2026-11-20) as of 2026-11-13 14:30 PT | File ATM IV 1-DTE (exp 2026-11-13) as of 2026-11-12 14:54 PT — STALE | 20d realized vol (live window 2026-10-16 to 2026-11-12) | Max single-day variance share | Window-contingent? |
|---|---|---|---|---|---|---|
| SPY | 10.36% (call 8.01% / put 12.71%, strike 754, spot 754.21) | 15.11% (call 13.95% / put 16.26%) | null — nearest expiry already dead at pull time, failed closed per rule | 22.88% | 0.544 | YES |
| QQQ | 18.05% (call 14.63% / put 21.47%, strike 680, spot 679.89) | 27.41% (call 25.29% / put 29.52%) | null — same dead-expiry fail-closed | 36.70% | 0.465 | YES |
| AAPL | 13.28% (call 13.53% / put 13.04%, strike 357.5, spot 356.27) | 20.03% (call 20.58% / put 19.48%) | 17.59% | 28.26% | 0.464 | YES |
| MSFT | 18.15% (call 17.51% / put 18.79%, strike 525, spot 523.88) | 29.35% (call 28.25% / put 30.45%) | 29.12% | 37.50% | 0.416 | YES |
| NVDA | 42.64% (call 41.24% / put 44.04%, strike 162.5, spot 162.85) | **81.30%** (call 80.91% / put 81.69%, strike 165) | 64.16% | 55.43% | 0.373 | YES |
| TSLA | 31.92% (call 31.24% / put 32.59%, strike 390, spot 390.22) | 44.28% (call 43.58% / put 44.97%) | 41.11% | 62.08% | 0.461 | YES |

ATM IV = mean(call IV, put IV) at the strike nearest spot, overlapping call/put strikes only, Yahoo `impliedVolatility` field. Realized vol = sample stdev of 19 log returns on fully-closed bars × √252. All figures FACT, sourced as above.

### Stale-jump screen — WINDOW-CONTINGENT on every symbol
- **FACT:** every symbol's 20-day realized window is WINDOW-CONTINGENT — max single-day variance share 0.37 (NVDA) to 0.54 (SPY), all above the 0.30 threshold, in both the file window (2026-10-15 to 2026-11-11) and the live window (2026-10-16 to 2026-11-12). The Nov 5 crash day dominates the window.
- **Consequence:** any IV-vs-realized verdict built on this window is **WINDOW-CONTINGENT, not clean**. At 3 DTE, every name's IV sits below its 20d realized (SPY −12.5pp, QQQ −18.7pp, AAPL −15.0pp, MSFT −19.4pp, NVDA −12.8pp, TSLA −30.2pp) — but that gap is inflated by the crash day in realized, so it is **not** a clean "IV cheap / premium buyers underpaying" read. **INFERENCE:** the gap says realized is backward-looking and jump-polluted, not that the market is complacent; the 7-DTE prints (closer to realized for most names) support that reading.

### Term structure
- **FACT:** term structure is upward-sloping on all six names, 3-DTE → 7-DTE: SPY +4.75pp, QQQ +9.36pp, AAPL +6.75pp, MSFT +11.20pp, TSLA +12.36pp, NVDA **+38.66pp**.
- **FACT:** NVDA's 7-DTE ATM IV of 81.30% is the only print on the board above its 20d realized vol (55.43%, +25.9pp). The Nov 17 earnings date sits inside the Nov 20 expiry — this is the textbook earnings hump: front-month IV elevated exactly where the binary event lives.
- **INFERENCE:** outside NVDA, the upward slope is consistent with near-term IV having compressed after the Nov 5 event passed while the 7-DTE still carries normal weekly premium — not a fear signal by itself.

### Skew note
- **FACT:** index downside skew is visible at the front: SPY put IV exceeds call IV by 4.70pp at 3 DTE (12.71% vs 8.01%) and 2.32pp at 7 DTE; QQQ by 6.84pp at 3 DTE (21.47% vs 14.63%) and 4.24pp at 7 DTE. Single names are near-flat (call/put gaps ≤2.8pp at both tenors). Normal equity skew, more pronounced at the front — no inversion, no upside-chase signal.

### Elevated-IV flags
- **NVDA — ELEVATED (earnings-driven, expected not anomalous):** 81.30% at 7 DTE, +38.66pp over its 3-DTE print. Expected given Nov 17 earnings inside the expiry; elevated IV here is the event being priced, not "rich" premium in the value sense.
- **QQQ / MSFT / TSLA — MODERATELY ELEVATED at 7 DTE** (27.41% / 29.35% / 44.28%) relative to SPY (15.11%), but each remains below its own 20d realized vol — and the realized comparison is window-contingent, so no clean richness call.
- **SPY / AAPL — LOW at 3 DTE** (10.36% / 13.28%), well below realized; window-contingent, do not read as a clean buy-premium signal.
- **IV rank: UNVERIFIED for all six** (no free IV history).

### Earnings inside the window
- **FACT:** NVDA next earnings **2026-11-17** (per the Nov 12 IV-inputs file; verified at source by the Earnings desk — Nasdaq calendar + NVIDIA IR). The Nov 16 expiry (3 DTE) does **not** contain earnings; the Nov 20 expiry (7 DTE) **does**.
- **Desk rule applied:** premium into a binary event = avoid. NVDA premium expiring Nov 20 is priced for the event (81.30% IV) — selling it collects event premium the market has already marked up, and buying it pays for a binary outcome. No premium thesis on NVDA into Nov 17 from this desk.

### Intraday spot context (FACT, Yahoo quote field at pull time, ~14:29 PT)
SPY 754.21 (−0.38% vs Nov 12 close 757.12); QQQ 679.89 (−1.20% vs 688.17); AAPL 356.27 (+0.39% vs 354.88); MSFT 523.88 (+0.17% vs 523.00); NVDA 162.85 (−2.01% vs 166.19); TSLA 390.22 (−1.82% vs 397.45). Intraday marks, not closes.

### Verdict
- **Thesis:** No clean premium edge on the board today. Near-term (3-DTE) IV is low versus a crash-polluted realized window, and the one genuinely elevated print (NVDA 7-DTE, 81.30%) is an earnings hump, not mispricing.
- **Evidence:** all six realized windows window-contingent (single-day share 0.37–0.54); NVDA 7-DTE IV exceeds realized only because Nov 17 earnings sits inside the Nov 20 expiry (+38.66pp hump vs 3 DTE); index put skew intact at the front.
- **What would change it:** the realized window rolling past Nov 5 (after ~Nov 25 the crash day exits the 20-day window) would un-contaminate the IV-vs-realized comparison; a flat or inverted NVDA term structure after Nov 17 (post-earnings IV crush) would reopen a clean read; a free IV-history source would let IV rank be computed instead of marked UNVERIFIED.
- **What matters most:** (1) NVDA Nov 17 earnings is inside the Nov 20 expiry — avoid premium into it; (2) every IV-vs-realized verdict today is WINDOW-CONTINGENT — do not trade the "IV below realized" gap as a signal until the Nov 5 day ages out of the window.

**Desk status: COMPLETE.** No failures on the live legs: all six symbols returned live ATM IV at both tenors and realized vol. Yesterday's file had SPY/QQQ ATM IV null (nearest expiry dead at 13:54 PT pull, failed closed per the post-expiry guard) — explained, not a live failure. IV rank UNVERIFIED for all six (no free IV history) — stated, not guessed. Put-call parity check: not run as a formal screen; ATM call/put IVs are close on single names and show normal index skew, no parity violation observed in the ATM marks pulled. (No box/parity claim made — that is the Parity desk's lane.)

---

## 4. Open Quant/AI Model Lab

**Question:** What new papers, preprints, datasets, or free APIs from the last ~2 days are relevant to the desks, and how do they score on the repo's own rubric?

**Coverage checked (FACT):** arXiv API, `cat:q-fin.*`, submitted 11–12 Nov 2026 — 16 items, all read at abstract level via the API (source: export.arxiv.org, fetched 2026-11-13 ~13:30 PT). This closes the provisional Nov 11 window flagged in the 2026-11-12 Jidoka log. **Nov 13 submissions announce 14 Nov 00:00 UTC and are NOT yet covered** — next run re-covers them. Secondary leg: one web search for recent IV-surface work (surfaced Boucher #284; Tirhekar, Li/Wang 2608.26115, and Sung were already ledgered). **GitHub leg skipped per the run brief's ban** — no repo discovery, re-checks, or license/content verification; any repo-linked claim is marked reproducibility NOT established.

**Scoring (FACT):** All 17 candidates scored by running `hedge_desk.research_intelligence.assess_source` on `ResearchSource` objects (module, never hand-scored). All claims below are **source-reported, UNVERIFIED** — abstract-only reads, full papers not read.

### New candidates

| # | Candidate | Source | Score | Disp. | Reason | Re-check item |
|---|---|---|---|---|---|---|
| 269 | Huang — TAPES: Terminal Adjoint-Propagated Error Scheduling for Financial Diffusion Samplers | arXiv:2611.16484v1, 12 Nov 2026; accepted ICAIF'26 | 56 | WATCH | Run's top score. Offline time-grid construction for frozen diffusion samplers; lowest audit-report errors in all 24 dataset–budget–report rows; ~10–11% error reduction on Regime-SV, ~1% on Mag7 (Bonferroni intervals excluding zero). Directly adjacent to the desk's IV-surface diffusion lane (#25/#20/#21/#261). No code link → reproducibility not established. | Code release? If code lands, test TAPES grids against the desk's own scenario-generation error before adopting any diffusion sampler as a scenario source |
| 284 | Boucher — Options-Implied Information Content for Cross-Asset Return and Volatility Prediction (3.8B contracts) | Zenodo 23933385, UQO WP No. 7 v1.2, Oct 2026 | 54 | WATCH | IV-surface features raise HAR-RV in-sample R² 0.415→0.457 (next-day) and 0.421→0.515 (weekly) across all nine subperiods, 69 US underlyings, 2010–2025. v1.2 honestly withdraws inflated v1.1 weekly-return results (R² 5–19%, Sharpe 2.33) — a credibility plus. No code/data release → reproducibility not established. | Full-paper read: does the HAR-RV lift survive an out-of-sample, purged split (abstract reports in-sample R²)? Code/data release? |
| 270 | Bayraktar/Deng/Huang/Norgilas — Price-impact Martingale Optimal Transport (PIMOT) | arXiv:2611.17247v1, 12 Nov 2026 | 51 | WATCH | Model-independent option-price bounds with quadratic temporary price impact; bounds widen with order size; SPX numerical examples. Parity-desk-relevant doctrine point: deterministic bounds that account for impact. No code link → reproducibility not established. | Code release? |
| 268 | Otranto — Parsimonious and Flexible Parameterizations for Realized Covariance Matrix Models | arXiv:2611.15619v1, 11 Nov 2026 | 48 | WATCH | Parsimonious realized-covariance parameterizations with positive-definiteness conditions; Monte Carlo + empirical application. Multi-asset vol-forecasting method reference; transfer to the desk's single-name RV read is indirect. No code link → reproducibility not established. | Code release? |
| 271 | Platen — Least Expensive Standard Pensions | arXiv:2611.15211v1 | 33 | ARCHIVE | Pensions/retirement design; no desk lane. |
| 272 | Alòs/Burés/Lucic — Gatheral's Conjecture refutation conditions | arXiv:2611.15391v1 | 33 | ARCHIVE | Pure rough-vol theory; no desk procedure. |
| 273 | Ma/Ninomiya — High-order recombination SDE approximation | arXiv:2611.15564v1 | 42 | ARCHIVE | SDE numerics (Heston/sSABR support cuts 137×/1488×); no desk procedure. |
| 274 | Butler/Zawadzki/Butler — Idiosyncratic Market Effects in Global Time Series Momentum | arXiv:2611.15646v1 | 42 | ARCHIVE | Momentum factor research; no desk lane. |
| 275 | Butler/Butler/Zawadzki — Global Seasonality Factor Investing | arXiv:2611.15657v1 | 42 | ARCHIVE | Factor investing; cost-honesty noted (fast patterns negative net of costs) but no desk transfer. |
| 276 | Abi Jaber et al — Signature expansion convergence rates | arXiv:2611.16087v1 | 33 | ARCHIVE | Pure theory; no desk procedure. |
| 277 | Choulli/Elazkany — Esscher concepts under random horizon | arXiv:2611.16129v1 | 30 | ARCHIVE | Credit/life-insurance theory; no desk lane. |
| 278 | Mattesini/Wiesel — Continuity of martingale optimal transport | arXiv:2611.16429v1 | 30 | ARCHIVE | Pure theory; no desk procedure. |
| 279 | Jiaqu — Accuracy Is Not Welfare: AI Buyers in a Synthetic Duopoly | arXiv:2611.16471v1 | 39 | ARCHIVE | AI-agent market microstructure; no desk lane (no execution). |
| 280 | Fabi/Leloup — Verifiable Settlement for Local Energy Markets (Besu) | arXiv:2611.16495v1 | 36 | ARCHIVE | Local/EU energy; futures desk is USDA/EIA, not power. |
| 281 | Mensah et al — Dynamic Scenario-Based Portfolio Optimization for Multi-Asset ETFs | arXiv:2611.16540v1 | 39 | ARCHIVE | Portfolio construction; no desk lane. |
| 282 | Gamrani/Pham — Media Trading with Censored Auction Prices | arXiv:2611.16992v1 | 33 | ARCHIVE | Ad-auction control; no desk lane. |
| 283 | Hirsch/Schaurecker/Wozabal — BESS Intraday Electricity Price Forecasts | arXiv:2611.17170v1 | 42 | ARCHIVE | EU intraday power; futures desk is USDA/EIA, not power. |

### Version re-checks (FACT, arXiv API id_list, 2026-11-13)
- **#25 (Han et al, diffusion IV surface) MOVED v3 → v4 (updated 2026-11-10).** No journal ref. v4 abstract now links code as `yinbinhan/volatility-surface` (vs `volatility-surface-simulation` in the ledger) — repo identity **UNVERIFIED**, GitHub leg banned, noted not resolved. Stays WATCH; OptionMetrics-pipeline block unchanged.
- No movement: #4 (v1), #9 (v2), #13 (v1), #14 (v3), #15 (v1), #20 (v2), #21 (v3), #30 (v3), #31 (v3), #261 (v1), #262 (v1), #263 (v3, revised 10 Nov — as ledgered), #264 (v2), #265 (v2), #266 (v3). All stay WATCH.

### Verdict
**Thesis:** Nothing in this sweep is decision-relevant today — no TEST, no INTEGRATE (run max 56, 9 under TEST).
**Evidence:** 4 WATCH (all diffusion/vol-bounds adjacent, all blocked on code release), 13 ARCHIVE on band discipline; one version movement (#25 v4) with an unresolved repo-identity discrepancy.
**What would change it:** A code release for #269 (TAPES), #284 (Boucher), or #270 (PIMOT) would open a sandbox; a full-paper read of #284 confirming the HAR-RV lift out-of-sample would make it the premium desk's most actionable item. **What would change the #25 note:** a permitted-leg check of which `yinbinhan` repo the v4 code link actually resolves to.

**Ledger:** all 17 candidates appended as #268–#284 in `~/workspace/hedge-desk-research/quant-lab-ledger.md`, #25 status updated, 2026-11-13 Jidoka entry added. Coordinator verified the appends on disk (rows #268–#284 present, #25 re-check note present). No source failures beyond the standing GitHub-leg ban; no candidates invented.

**Desk status: COMPLETE.**

---

## 5. Weather/War/Logistics Futures Event Desk

**Run as-of:** Fri 2026-11-13 ~16:30 ET (13:30 PT)
**Question:** What fresh catalysts printed since the last run, and what are the relevant futures curves pricing?

### Catalyst table

| # | Event | Date / time | What printed | Consensus (if verifiable) | Futures read |
|---|---|---|---|---|---|
| 1 | **EIA Weekly Petroleum Status Report** (week ended Nov 6) | Released **Thu Nov 12** — one day late for the Veterans Day holiday (Wed Nov 11) | **FACT:** Commercial crude **+4.657M bbl to 414.4M** (+1.1% w/w, −3.1% y/y, ~4% below 5-yr avg). Gasoline **+1.8M to 210.8M** (1% above 5-yr avg). Distillates **+4.1M to 103.3M** (8% below 5-yr avg). SPR **−2.6M to 279.5M**. Total commercial petroleum +11.4M bbl. Refinery runs +322k b/d to 17.0M b/d, utilization 95.2%. Crude imports +~325k b/d to ~6.7M b/d; production 14.013M b/d (+10k). (EIA via Rigzone/Morningstar-Dow Jones/FXEmpire, Nov 12–13) | Crude: WSJ survey **−0.7M**; InvestingLive-cited survey **−1.109M**; Macquarie **−3.7M**. Distillates: WSJ **−1.2M**. Gasoline: WSJ **unchanged**. → Bearish surprise vs every survey: crude surprise **+5.4M to +8.4M bbl** depending on survey. (Morningstar, Nov 12; fxnews, Nov 12) | See futures table below — crude rallied *despite* the build; geopolitics outweighed the print on the day. |
| 2 | **USDA WASDE-677** | Released **Tue Nov 10, 2026** (next: Dec 10) | **FACT:** Corn 2026/27: production cut **141M bu to 15,893M** (yield 179.6 bu/ac, −1.6 from Oct's 181.2); ending stocks **−91M to 1,758M**. Soybeans: production **+12M to 4,574M** (yield 53.3, +0.2); exports **+25M to 1,720M**; ending stocks **−15M to 300M**. Wheat: ending stocks **+3M to 743M** (still −19% y/y). Season-avg prices: corn $4.60 (−$0.10), soy $12.10 (+$0.10), wheat $6.20 (−$0.10). (USDA via Iowa Farm Bureau / RFD-TV / Feed & Grain, Nov 10) | Corn yield 179.6 vs trade avg **180.5**; corn ending stocks 1,758M vs avg **1,826M**; soy yield 53.3 vs avg **53.6**; wheat ending stocks 743M vs avg **747M**. (Oklahoma Farm Report survey table, Nov 10) → Corn modestly tighter than expected; soy roughly in line, stocks tighter on exports. | Corn +2.2% and soy +3.6% on WASDE day (Nov 10), then faded (see futures table). |
| 3 | **EIA Weekly Natural Gas Storage Report** (week ended Nov 6) | Released **Fri Nov 13, 10:30 ET** — one day late for Veterans Day | **FACT:** Injection **+61 Bcf to 3,862 Bcf**; surplus vs 5-yr avg widened to **+75 Bcf** (from +54 Bcf). (WSJ, Nov 13; FXEmpire, Nov 13) | WSJ survey **67 Bcf** (range 55–82); FXEmpire cited a ~65 Bcf estimate — **two consensus figures conflict; use 67 Bcf (WSJ) as primary, 65 Bcf as secondary**. 5-yr avg for the week: 40 Bcf. → Smaller than expected, but above the 5-yr avg; still a build. | Natgas +4.0% Thu Nov 12 on cold forecasts, giving back some Fri (see futures table). |
| 4 | **EIA Short-Term Energy Outlook** | Released **Tue Nov 10** | **FACT (via secondary):** Henry Hub annual avg forecast cut to **$3.37/MMBtu for 2026 and $2.88 for 2027** (from $3.48 / $3.16); winter Nov–Mar avg **$2.87/MMBtu**; global oil inventories projected to shift to a build in Q4 after a Q3 draw of 1.2M b/d, averaging builds of 3.5M b/d in H1 2027. (FXEmpire, Nov 12; fxnews, Nov 12) | — | EIA's own view is bearish for oil/gas prices vs the market's Thu rally — a tension, not a resolution. |
| 5 | **Houthi claims of attacks on Saudi energy sites** (geopolitical, <48h) | Claims published **Thu Nov 12** | **FACT:** Yemen's Houthis said they attacked Pumping Station No. 7 on Saudi Arabia's East–West oil pipeline (drone, then ballistic missile), an oil facility at Yanbu on the Red Sea coast, and an Aramco building in Riyadh — 12 attacks claimed in total. (Reuters, Nov 12; Demócrata, Nov 13) **FACT:** Saudi-led coalition said it intercepted/destroyed two drones (Riyadh region, Eastern Province). **UNVERIFIED:** No Saudi confirmation of damage at any of the three sites; the Houthis did not say which day the attacks took place. (Reuters, Nov 12) **UNVERIFIED:** Iran's military separately claimed four oil tankers were hit by explosions in the Strait of Hormuz; Reuters said it could not immediately verify. (Reuters via aiagentupdate, Nov 13) | — | Crude's +3.3% Brent / +2.6% WTI settlement Thu was priced on the *claims*, before any confirmation — risk premium, not confirmed supply loss. |
| 6 | **US–Iran war / Hormuz context** (background, not new) | Ongoing since Feb 2026 | **FACT:** War began with US/Israel attacking Iran in February 2026; Strait of Hormuz flows disrupted; Saudi Arabia has rerouted ~4M b/d (~4% of global supply) via the East–West Pipeline to Yanbu, bypassing Hormuz. (Reuters, Nov 12) **FACT:** On Nov 12 President Trump posted the US "does not need a deal with Iran" and "already has their Strait." (CNBC via Bay Area Brief, Nov 12) Prior context: Houthi missiles fired at Riyadh Sun Nov 8; Saudi Energy Ministry confirmed only minor shrapnel damage to an Aramco administrative building, no injuries. (Defense and Tech / Reuters, Nov 9) | — | The East–West Pipeline is precisely the bypass the Houthis now claim to have hit — that is why the claim moved crude despite no confirmed damage. |
| 7 | **OPEC+ calendar** | Next meeting **Sun Nov 29, 2026** | **FACT:** Seven OPEC+ participants set Nov 29 for their next meeting. (el7.ai, Nov 12) | — | No new output decision until then; watch for pre-meeting signaling. |

### Futures moves — one named series per row (Yahoo Finance v8 chart, continuous front-month, daily closes; simple returns)

| Series (Yahoo) | Close Nov 11 | Close Nov 12 | Change | Close Nov 10 (WASDE day) vs Nov 9 | Intraday last, Fri Nov 13 ~16:28 ET* |
|---|---|---|---|---|---|
| WTI crude CL=F ($/bbl) | 86.53 | **88.74** | **+2.21, +2.6%** | — | 88.99 |
| Brent crude BZ=F ($/bbl) | 92.76 | **95.82** | **+3.06, +3.3%** | — | 96.25 |
| Natgas NG=F ($/MMBtu) | 3.21 | **3.34** | **+0.13, +4.0%** | — | 3.24 |
| Corn ZC=F (¢/bu) | 448.00 | 442.50 | −5.50, **−1.2%** | 439.25 → 449.00, **+2.2%** | 446.00 |
| Soybeans ZS=F (¢/bu) | 1,229.00 | 1,227.00 | −2.00, **−0.2%** | 1,182.25 → 1,224.50, **+3.6%** | 1,232.75 |
| Wheat ZW=F (¢/bu) | 599.50 | 584.25 | −15.25, **−2.5%** | 588.00 → 592.75, **+0.8%** | 593.50 |
| Gold GC=F ($/oz) | 4,000.50 | 3,885.30 | −115.20, **−2.9%** | — | 3,877.60 |
| Copper HG=F ($/lb) | 6.27 | 6.18 | −0.09, **−1.4%** | — | 6.07 |

\* Nov 13 values are intraday lasts at ~16:28 ET, **not closes** — do not treat as settlement. All % changes recomputed as (new − old)/old from the two closes named in the row; signs verified against the arithmetic. Sources: Yahoo Finance v8 chart, pulled Fri Nov 13 16:28 ET; Reuters settlement prints agree (Brent $95.82 +3.3%, WTI $88.74 +2.6%, Nov 12).

**Reconciliation note — FACT:** Crude reversed violently within Thu Nov 12: early Asian session Brent fell >$1 to ~$91.29 and WTI to ~$85.29 on easing-war hopes (Reuters, Nov 12 01:52 ET), then reversed to settle +3.3%/+2.6% after the Houthi claims and the Trump post. Early-session reports quoting Brent ~$91.81 / WTI ~$85.64 for Nov 12 (SNSUC, Arbiterz) are pre-reversal prints, not settlements — the settlement figures above are the ones that reconcile across Reuters, Yahoo, and the commodity-board curve note (WTI Dec-26 settled 88.74; Brent Jan-27 ~95.7–96.0; curve steeply backwardated, prompt Dec/Jan WTI spread ~+$1.05/bbl).

**Curve read — INFERENCE:** The crude curve is pricing prompt tightness / war risk, not the EIA's glut: front-month rallied on unverified claims while the EIA printed a bearish all-barrels build and its own STEO projects H1-2027 builds of 3.5M b/d. Backwardation + a +3.3% day on unconfirmed claims = a market paying up for prompt supply insurance. Gold −2.9% and copper −1.4% on the same day argue against a broad risk-off read; this was an oil-specific risk-premium repricing. **SPECULATION:** If the pipeline/Yanbu damage claims are confirmed or repeated, prompt crude likely holds the premium; if Saudi/Aramco confirms no damage, the premium should fade toward the EIA/STEO glut view — but that fade is a scenario, not a forecast.

### What did NOT print / checked and empty
- **No new USDA report beyond WASDE-677** (Nov 10); next WASDE Dec 10. **FACT.**
- **No fresh logistics/shipping chokepoint closure** beyond the Hormuz situation already in the background (no new canal/port closure found in the last ~48h). **UNVERIFIED** as a negative — searched news for shipping disruptions; nothing new surfaced, but absence of a headline is not proof of absence.
- **No new EIA petroleum print beyond Nov 12**; next WPSR due Wed Nov 18 on the normal schedule. **FACT** (schedule per EIA).
- EIA primary page (eia.gov/petroleum/supply/weekly/) confirms the report exists and was released, but its data tables did not render in the text fetch — inventory numbers above are EIA figures quoted verbatim by Rigzone, Morningstar/Dow Jones, and FXEmpire, three independent secondaries in agreement. **FACT (secondary-corroborated).**

### Verdict
- **Thesis:** The week's two scheduled prints were both fundamentally bearish-to-neutral (EIA all-barrels build vs draw consensus; WASDE a modest corn/soy tightening, wheat a small build), but the market's price action was set by an unscheduled geopolitical claim, not by either print. Crude's +3.3% Brent settlement on Thu Nov 12 is a risk-premium move on *unverified* Houthi claims against the one pipeline that bypasses Hormuz.
- **Evidence:** EIA +4.657M bbl crude build vs −0.7M/−1.109M/−3.7M surveys; WASDE corn stocks −91M bu, soy −15M bu; Yahoo/Reuters settlements Brent 92.76 → 95.82 (+3.3%), WTI 86.53 → 88.74 (+2.6%) on Nov 12; no Saudi confirmation of damage (Reuters).
- **What matters for the watchlist:** Nothing in this desk's catalysts is a direct watchlist earnings/dividend event. The read-through is macro: a sustained crude risk premium is a cost-push input, not a margin-of-safety signal — and a premium built on unconfirmed claims is the weakest kind. The EIA build + STEO glut outlook is the fundamental counterweight. Value lens: no mispricing to hunt here; the ags WASDE pop already faded (corn −1.2%, wheat −2.5% on Nov 12).
- **What would change it:** (1) Saudi/Aramco confirmation or denial of damage to the East–West Pipeline or Yanbu — confirmation sustains the premium, denial should unwind it; (2) a verified Hormuz shipping incident (tanker claim currently UNVERIFIED); (3) next EIA WPSR Wed Nov 18 — a second consecutive build would strengthen the glut case; (4) OPEC+ meeting Nov 29.

### Sources
- EIA Weekly Petroleum Status Report, released Nov 12, 2026 (week ended Nov 6): https://www.eia.gov/petroleum/supply/weekly/ (page fetched Nov 13; tables did not render — figures via Rigzone https://www.rigzone.com/news/usa_crude_oil_stocks_rise_almost_5mm_barrels_week_on_week-13-nov-2026-185081-article/ ; Morningstar/Dow Jones https://www.morningstar.com/news/dow-jones/2026111212107/us-crude-oil-stockpiles-post-unexpected-weekly-build ; FXEmpire https://www.fxempire.com/forecasts/article/oil-prices-rebound-as-middle-east-risks-offset-u-s-inventory-builds-1644517)
- USDA WASDE-677, Nov 10, 2026: https://www.iowafarmbureau.com/Article/USDA-Cuts-202627-Corn-Ending-Stocks-91-Million-Bushels-to-176-Billion ; survey table https://www.oklahomafarmreport.com/2026/11/10/rich-nelson-breaks-down-neutral-wheat-balances-corn-demand-risks-and-cattle-trade-dynamics/
- EIA Natural Gas Storage, released Fri Nov 13 (week ended Nov 6): WSJ https://www.wsj.com/finance/commodities-futures/u-s-natural-gas-futures-return-some-gains-1b28586d ; FXEmpire https://www.fxempire.com/forecasts/article/natural-gas-news-weekly-gain-holds-as-traders-await-weekend-forecasts-1644595
- Houthi claims / Reuters: https://www.reuters.com/world/middle-east/yemens-houthis-say-they-attacked-pumping-station-saudi-arabias-east-west-oil-2026-11-12/
- Futures closes: Yahoo Finance v8 chart (CL=F, BZ=F, NG=F, ZC=F, ZS=F, ZW=F, GC=F, HG=F), pulled Fri Nov 13 ~16:28 ET.
- No federal shutdown framing used; EIA and USDA releases on schedule per the standing government-data rule.

**Desk status: COMPLETE.**

---

## 6. Box/Parity Observer

Nothing material — no new index-methodology doc or published parity-violation analysis since the last daily run.

**Checks run (all FACT, sources as of 2026-11-13):**
- S&P DJI growth/value methodology overhaul (momentum dropped from growth, FCF-to-price added to value; effective Dec 21, 2026) was announced Oct 23, 2026 — not new since yesterday; not re-flagged. Source: https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/
- CBOE Europe Equity Indices methodology changes took effect Nov 2, 2026 (announced Jul 13) — stale, Europe-only, no watchlist relevance. Source: https://cdn.cboe.com/resources/indices/notices/europe/Announcement-Regarding-Effective-Date-of-Methodology-Changes-to-the-Cboe-Europe-Equity-Indices.pdf
- CBOE SR-CBOE-2026-085 is a fee-schedule filing (SPXO AM-settled SPX weeklies, launched Nov 9) — a product launch, not an index-methodology change or parity finding; no new development since the last run. Source: https://cdn.cboe.com/resources/regulation/rule_filings/approved/2026/SR-CBOE-2026-085.pdf
- No new published box-spread / put-call parity violation study found. The most recent relevant paper, Shin (Aug 24, 2026, arXiv 2604.19604), finds quoted put-call parity residuals near zero with a systematic ~37 bp carry gap — dated Aug 2026, not new. Source: https://arxiv.org/html/2604.19604
- Corroborating parity check (secondary source, week-old): Saxo's daily options briefs Nov 2–6, 2026 report put-call parity on the 18 Nov VIX options returning values in line with settlements each day — no violation observed. Source: https://www.home.saxo/en-mena/content/articles/options/vote-premium-drains-from-the-front---options-brief---5-november-2026-05112026

**Verdict:** No parity violation, no new methodology doc, no action. Deterministic parity math stands unchallenged this session; nothing in today's sweep changes any desk's pricing inputs.

**Desk status: COMPLETE.**

---

## 7. Bonds & Rates Desk

**Question in one sentence:** Does today's fresh rates pull change the consolidated Dec 9 call (25bp hike) in `desk7-core-indicators.md`? **Answer: No — direction and tally unchanged; the 10Y rose another 12bp and Kalshi drifted 1¢, both inside the existing call.**

**Method note (FACT):** Ran the repo's rates module fresh this session (`rates_desk.rates_environment()`, mode `REAL_FRED_RATES`, `as_of` 2026-11-13, source `fred-public-csv-http-200`). The module returns rates only — there is no core-indicator function in `rates_desk.py` (only `rates_environment()` is the public entry), so the 10-indicator table below is carried from this morning's consolidated snapshot pulls (~08:35–08:45 PT), with its as-ofs intact. No kept indicator can have printed new data intraday: the monthly/quarterly series (PCE, payrolls, JOLTS, GDP, housing, Michigan) publish on fixed release dates, and the daily series (breakevens, HY OAS) publish with a lag — Nov 13 values are not out yet (INFERENCE from release calendars, stated as such).

### 1. Rates table — fresh FRED pull, data as of Nov 12, 2026

| Series | Level | As of | Change vs morning snapshot |
|---|---|---|---|
| EFFR (fed funds effective) | 3.88% | Nov 12 (FRED) | Within target 3.75–4.00% (FACT) |
| SOFR | 3.90% | Nov 12 (FRED) | — |
| OBFR | 3.88% | Nov 12 (FRED) | — |
| 2Y Treasury (DGS2) | 4.86% | Nov 12 (FRED) | +13bp vs Nov 10 (4.73%) (FACT) |
| 10Y Treasury (DGS10) | 5.10% | Nov 12 (FRED) | +12bp vs Nov 10 (4.98%) (FACT) |
| 2s10s slope (10Y − 2Y) | +24bp | Nov 12 | Narrowed 1bp vs Nov 10 (+25bp) (FACT, arithmetic) |
| Curve shape | Upward sloping | Nov 12 (module) | Unchanged (FACT) |
| Fed funds change over 60-day window | +0.25pp | Module output | October hike, already in the call (FACT) |

**Direction of change (FACT, signs recomputed):** Both legs rose Nov 10 → Nov 12 — 2Y +13bp (4.73 → 4.86), 10Y +12bp (4.98 → 5.10). The 2Y rose 1bp more than the 10Y, so the slope narrowed 25bp → 24bp. No Nov 11 observation exists in either series (Veterans Day market holiday — FACT from the history arrays).

**SOFR vs EFFR funding spread (FACT, arithmetic):** SOFR 3.90% − EFFR 3.88% = **+2bp**. No funding stress signal — a 2bp spread is noise, not dislocation (INFERENCE).

### 2. Core-indicator table — reads unchanged from this morning's snapshot

Tally carried: **5 HIKE / 1 CUT / 4 NEUTRAL**. No indicator printed new data since the morning pull (see method note).

| Indicator | Today's read (as-of in consolidated doc) | Signal | Broker POV (carried — read unchanged) |
|---|---|---|---|
| Core PCE (PCEPILFE, BEA/FRED) | y/y +3.121%, m/m +0.317% (130.902, Sep 2026) | HIKE | Anchor the discount rate to the higher regime. Next PCE print (Nov 25, provisional) is the re-anchor date. |
| Breakevens (T5YIE / T10YIE, FRED) | 2.31% / 2.24% (Nov 12) | NEUTRAL | Anchored expectations: room for 25bp, not a forced 50bp. Tripwire above 2.75%. |
| Michigan expectations (MICH, U-M) | 4.3% yr-ahead, Nov prelim (Oct 4.7%), rel. Nov 6 | HIKE | 4.3% vs 2.24% breakevens is a credibility gap the Fed reads as pressure to act. |
| Payrolls, 3-mo avg (PAYEMS, BLS) | 3-mo avg +137k; Oct +165k (Oct 2026) | NEUTRAL | Rule as written: NEUTRAL. One +165k print does not override the average. |
| Initial claims, 4-wk avg (ICSA, DOL) | 200k w/e Nov 7; 4-wk avg 195,250 | NEUTRAL | Check every Thursday; >300k 4-wk avg flips labor to CUT. |
| Job openings (JTSJOL, BLS) | 7,523k, Sep 2026 (Jul 7,335k, Aug 7,190k) | HIKE | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA) | Q3 +3.37% annualized (Q2 +2.22%) | HIKE | Above-trend growth removes the "restraint is biting" objection. |
| Housing starts (HOUST, Census) | 1,221k; −10.8% Jul→Sep (Sep 2026) | CUT | The hold argument's evidence — why the call is 25bp, not 50bp. Do not bury it. |
| HY OAS (BAMLH0A0HYM2, ICE BofA/FRED) | 3.20% (Nov 12) | NEUTRAL | No credit stress; watch a break above 5.00%. |
| FOMC vote & guidance (federalreserve.gov) | Oct 28: held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; "Inflation remains elevated" | HIKE | Weight the vote above any single print. Nov 18 minutes are the check on division. |

### 3. Market pricing vs indicators — fresh Kalshi pull, ~13:30 PT

Direct API pull this session (`api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXFEDDECISION`, Dec-2026 meeting):

| Outcome | Last | Bid / Ask | Prev | vs 12:00 PT pull |
|---|---|---|---|---|
| 25bp hike (KXFEDDECISION-26DEC-H25) | $0.87 | 0.87 / 0.88 | 0.86 | −$0.01 (was $0.88) |
| >25bp hike (H26) | $0.12 | 0.10 / 0.11 | 0.12 | Unchanged |
| Hold (H0) | $0.03 | 0.02 / 0.03 | 0.03 | Unchanged |
| 25bp cut (C25) | $0.01 | 0.00 / 0.01 | 0.01 | Unchanged |
| >25bp cut (C26) | $0.01 | 0.00 / 0.01 | 0.01 | Unchanged |

Total hike priced: **$0.99** (was $1.00 at 12:00 PT). Five lasts sum to $1.04 (4-cent over-round, was $1.05). **The 1¢ drift in the 25bp leg is noise, not a repricing — direction and tail are unchanged** (INFERENCE). CME FedWatch: direct read still not possible (embedded app, no public text API) — UNVERIFIED by direct read; secondhand reads Nov 10–13 converge at 87–91% for 25bp, 9–15% for 50bp, per the morning doc. Kalshi ($0.87 / $0.12) sits inside that range on both legs — markets agree with each other and with the indicator direction (INFERENCE).

**Disagreement named:** None new. The standing disagreement remains size, not direction: indicators vote hike, no rule distinguishes 25bp from 50bp, and the $0.12 tail is market-priced, not data-driven (INFERENCE, unchanged from morning).

### 4. Graham lens — updated for the fresh 10Y

- 10Y 4.98% (Nov 10) → **5.10%** (Nov 12): at assumed perpetual growth g = 3.00%, Gordon multiple 1 ÷ (r − g) falls 50.51x → **47.62x, −5.71%** (FACT, arithmetic: 1/0.0198 = 50.51; 1/0.0210 = 47.62; −2.89/50.51 = −5.72%, rounded −5.71% on unrounded inputs). Cumulative from Nov 6 (4.86%, 53.76x): **−11.43%**.
- Duration ≈ 8: the +12bp move is about **−0.96%** on a 10-year position, incremental to the same-sized move Nov 6 → Nov 10 (approximation; ignores convexity).
- Margin of safety is thinner again at the same prices: any intrinsic-value estimate carried at the 4.98% anchor overstates value by ~5.7% on this sensitivity. **Re-anchor to 5.10%.**
- Earnings-yield vs bond-yield spread: UNVERIFIED (bond side verified at 5.10%; earnings side unverified from any primary source this session — no live spread asserted).

### 5. Verdict

- **Thesis:** 25bp hike on Dec 9 (FOMC Dec 8–9, target 3.75–4.00%). Core PCE at 3.12% y/y with no labor deterioration, above-trend growth, a 10–2 vote with two hawkish dissents, and markets pricing a hike at $0.99. (INFERENCE from the FACTs above.)
- **Evidence:** 5 HIKE / 1 CUT / 4 NEUTRAL across the 10 core indicators; Kalshi total hike $0.99; 10Y at 5.10% with the curve still upward sloping (+24bp) and funding calm (SOFR−EFFR +2bp).
- **What would change it:** October core PCE (Nov 25, provisional) at m/m ≤ +0.15% with a downward September revision; claims 4-wk avg above 300k; Nov 18 minutes or a named speaker arguing for a hold. Nothing in this session's fresh pulls triggers any of these.

### 6. Changes vs this morning's consolidated snapshot — explicit

1. **10Y Treasury: 4.98% (Nov 10) → 5.10% (Nov 12), +12bp** — fresh FRED pull. Gordon multiple 50.51x → 47.62x (−5.71%); re-anchor discount rate to 5.10%.
2. **2Y Treasury: 4.73% (Nov 10) → 4.86% (Nov 12), +13bp** — fresh FRED pull. 2s10s narrowed 25bp → 24bp.
3. **Kalshi 25bp leg: $0.88 → $0.87 (−1¢); total hike $1.00 → $0.99; >25bp tail unchanged at $0.12** — fresh direct pull ~13:30 PT. Immaterial drift; call unchanged.
4. **Core-indicator reads: NO CHANGE.** No kept indicator printed new data between the morning snapshot and this pull.
5. **No correction to `desk7-core-indicators.md` is needed.** The morning doc's numbers were correct at their stated as-ofs; the changes above are new data, not errors. No edit made; none requested.

**Desk status: COMPLETE.** Module ran clean (REAL_FRED_RATES, HTTP 200); all numbers above are from pulls run this session or the morning snapshot with as-ofs stated. No UNVERIFIED numbers are asserted as FACT. Sources: FRED (fred.stlouisfed.org, via repo module), Kalshi trade API (`api.elections.kalshi.com`), BEA/BLS/DOL/U-M via FRED as cited in the consolidated doc, federalreserve.gov for the vote.

---

## Cross-desk reconciliation (coordinator)

- **NVDA Nov 17 confirmed on two independent legs:** Earnings desk verified the date at source (Nasdaq calendar + NVIDIA IR); Premium desk's IV file listed the same date; both agree. The Earnings desk's implied move (~8.5%, Nov 18 straddle) and the Premium desk's 81.30% 7-DTE IV are the same event priced two ways — consistent, not contradictory.
- **No contradiction between desks:** Dividend (MSFT ex Nov 19) and Premium (no earnings in window except NVDA) agree on the calendar; Futures catalysts carry no watchlist earnings/dividend event; Parity reports nothing that changes any pricing input; Quant Lab reports nothing decision-relevant today; Desk 7's call is unchanged.
- **Standing items carried forward:** IV rank UNVERIFIED for all six names (no free IV history); every IV-vs-realized verdict WINDOW-CONTINGENT until the Nov 5 crash day exits the 20-day window (~Nov 25); NVDA prior-year EPS basis conflict ($1.24 vs $1.30) UNVERIFIED; FedWatch direct read UNVERIFIED (embedded app); #25 repo-identity discrepancy (yinbinhan/volatility-surface vs volatility-surface-simulation) UNVERIFIED pending a permitted leg; Nov 13 arXiv submissions not yet covered (announce Nov 14 00:00 UTC) — next run re-covers them.
- **No desk FAILED.** All seven desks delivered. No retry was needed; no desk was dropped or invented.
