# Hedge-Desk Daily Research — Sat 2026-10-17

**Run:** daily research, 1:30pm PT slot. Research + input only — no git, no PRs, no code changes.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; never risk-seeking framing.
**Evidence standard:** every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it.
**Market-data rule:** Yahoo first, Nasdaq second, fallbacks after. Yahoo calls sent with `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`.
**Quotes as-of:** Fri Oct 16 close (run day is Saturday; no new session). FRED latest observations Oct 15 (one-business-day publication lag).
**Synthesis note:** desks corroborate each other on the two earnings straddles (TSLA 7.41%, MSFT 6.04%) and on SPY close 763.25. One cross-desk discrepancy is resolved below (AAPL earnings date). No desk failed; no desk was dropped.

## Top 5 decision-relevant items (synthesized)

1. **Vol regime jumped — premium elevated, but most IV-vs-realized verdicts are WINDOW-CONTINGENT.** VIX 19.99, +21% Friday, 81st percentile of its 1-year range (FACT). For SPY, QQQ, AAPL, MSFT a single day drives >30% of the 20-day realized variance, so no clean "rich premium" call is valid there (FACT, stale-jump screen). Clean reads only: NVDA IV above realized; TSLA pre-event IV ≈ realized. **Avoid premium into TSLA (Oct 21) and MSFT (Oct 28) earnings humps.**
2. **Two in-window earnings, both AMC, both priced roughly in line with history — no clean mispricing.** TSLA Wed Oct 21 (implied 7.41% vs hist. mean 7.77% / median 4.46%); MSFT Wed Oct 28 (implied 6.04% vs mean 7.02% / median 6.12%). The trade on each print is guidance + cash conversion, not the EPS headline (INFERENCE, CFA reading order).
3. **Rates: front end pinned, long end easing from its peak — discount-rate headwind persists but is no longer intensifying.** 10Y 5.10%, 2Y 4.77%, 2s10s +33 bp (flattened from +52 bp over 60 days), EFFR 3.88%, SOFR–EFFR +1 bp = funding orderly (all FACT, FRED module). 10Y peaked 5.31% Oct 5, down 21 bp since.
4. **Energy disruption is the dominant macro catalyst — crude backwardated, diesel crunch into 2H 2027.** WTI Nov $101.41 (+10.4% w/w), Mar $93.53 (−7.8% vs Nov); Brent Dec $109.86; IEA: diesel stocks unlikely rebuilt before 2H 2027; tanker freight now segmenting the market by route (FACTs, see Futures desk). Grains run the opposite way: post-WASDE glut + record Brazilian crops coming, corn/soy/wheat all in contango (carry).
5. **Nothing goes ex-dividend in the 4-week window.** Only declared upcoming watchlist dividend: MSFT $0.98, ex Nov 19 (five days outside the window). AAPL's November dividend is not yet declared — expected with its earnings. No cuts, no specials (FACT, Nasdaq calendar sweep).

## Cross-desk discrepancy — resolved

- **AAPL earnings date:** Earnings desk reports **Mon Nov 2, 2026, AMC** from the Nasdaq earnings calendar (FACT per Nasdaq; corroborated by MarketBeat). Dividend desk's "~Oct 29–30" was a pattern-based expectation, NOT a calendar fact — superseded by the Nasdaq calendar date. Premium desk's Nasdaq calendar check returned zero rows (endpoint uninformative on that pull, not a contradiction) and its file-sourced Nov 2 date agrees with the Earnings desk. **Package standard: AAPL = Nov 2 AMC per Nasdaq.** Note Nov 2 is a Monday, atypical for AAPL — re-verify against the company release if it moves.
- **NVDA earnings:** Earnings desk Nov 18 (Nasdaq, timing UNVERIFIED); secondaries disagree (Nov 17 / Nov 25). Treat Nov 18 as Nasdaq-sourced, timing UNVERIFIED.
- **Consensus-EPS basis:** Nasdaq EPS forecasts differ from secondaries (TSLA $0.21 vs $0.37–$0.40; MSFT $4.71 vs $3.89) — basis (GAAP vs non-GAAP) UNVERIFIED. Do not mix. Re-verify against the release on print day.

---

## 1. Earnings Event desk

**In-window (Oct 17–31):** TSLA Wed Oct 21 AMC; MSFT Wed Oct 28 AMC. AAPL Mon Nov 2 AMC (just outside window). NVDA Nov 18 (timing UNVERIFIED). SPY/QQQ: no earnings (FACT).

| Name | Date | Timing | Nasdaq EPS fcst | Options-implied move | Hist. avg earnings-day move (8 qtrs) |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21, 2026 | AMC (FACT — Nasdaq `time-after-hours`; confirmed by Tesla IR) | $0.21 | **7.41%** | Mean \|move\| **7.77%**, median \|move\| **4.46%** |
| MSFT | Wed Oct 28, 2026 | AMC (FACT — Nasdaq `time-after-hours`; TipRanks concurs) | $4.71 | **6.04%** | Mean \|move\| **7.02%**, median \|move\| **6.12%** |

**Implied-move method (FACT):** ATM straddle mid ÷ underlying, first expiry after the print, quotes as of Fri Oct 16 close. TSLA: Oct 23 expiry, 355 strike, straddle $26.27 ÷ $354.72 = 7.41%. MSFT: Oct 30 expiry, 530 strike, straddle $31.95 ÷ $529.05 = 6.04%. Caveat (INFERENCE): each expiry is 2 sessions after its print, so the straddle embeds ~2 extra days of time value and slightly overstates the pure event move — treat implied as an upper-ish bound on the event-only move.

**Historical reactions (FACT — Yahoo daily closes, next-trading-day close vs report-day close, all 8 prints AMC):**
- TSLA: Jul 22, 2026 −14.52%; Apr 22, 2026 −3.56%; Jan 28, 2026 −3.45%; Oct 22, 2025 +2.28%; Jul 23, 2025 −8.20%; Apr 22, 2025 +5.37%; Jan 29, 2025 +2.87%; Oct 23, 2024 +21.92%. Mean signed +0.34%; mean |move| 7.77%; median |move| 4.46%. The mean is outlier-driven; the median is the decision-relevant center.
- MSFT: Jul 29, 2026 +15.51%; Apr 29, 2026 −3.93%; Jan 28, 2026 −9.99%; Oct 29, 2025 −2.92%; Jul 30, 2025 +3.95%; Apr 30, 2025 +7.63%; Jan 29, 2025 −6.18%; Oct 30, 2024 −6.05%. Mean signed −0.25%; mean |move| 7.02%; median |move| 6.12%.

**Read (INFERENCE):** TSLA implied ≈ historical mean, well above historical median (market pricing the fat-tail history). MSFT implied ≈ historical median and just below mean — roughly in line. Neither is a clean mispricing. Past reactions do not determine the next print.

**Desk notes:** TSLA Q2 2026 actuals disagree across secondaries (EPS $0.27–$0.34) — same GAAP/adjusted basis problem. On print day, read the release itself: guidance vs consensus first, then GAAP income statement vs headline adjusted figure, then OCF vs net income, segment margins, balance-sheet deltas, call last. MSFT beat consensus EPS in all 8 of the last 8 prints in the TwelveData table (FACT per that source, basis caveat applies) — the trade on the print is Azure growth + guidance, not the EPS beat streak (INFERENCE).

**What would change the verdicts:** the actual releases (guidance, GAAP-vs-adjusted gap, cash conversion, segment margins); a rescheduled date; a verified consensus-basis reconciliation that moves the hurdle.

**Sources:** Nasdaq earnings calendar API (`https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`, checked Oct 19–30 daily; Nov 2, Nov 18, Nov 25 out-of-window); Tesla IR https://ir.tesla.com/; Yahoo Finance options chain (crumb-authenticated) + v8 chart daily closes, UA header; TipRanks, MarketBeat (https://www.marketbeat.com/earnings/reports/2026-11-2-apple-inc-stock/), TwelveData, TradingKey, CoinCodex (dates/consensus cross-checks only, basis UNVERIFIED).

---

## 2. Dividend Opportunity desk

**Verdict:** Nothing goes ex-dividend inside the 4-week window (Oct 17 – Nov 14, 2026). Only declared upcoming watchlist dividend is MSFT $0.98, ex Nov 19 — five days outside the window. No cuts, no specials, no new increases in the window (FACT). **What would change it:** an AAPL declaration with its FQ4 earnings setting a November ex-date, or any new board declaration.

| Name | Ex-date in window? | Next ex-date | Amount | Yield (computed) | Increase / cut / special | Consecutive-increase count (per standard) |
|---|---|---|---|---|---|---|
| SPY | None — FACT | ~mid-Dec 2026, UNVERIFIED (pattern-based) | Last: $1.889 (ex 2026-09-18) — FACT | ~0.99% trailing — INFERENCE | None — FACT | N/A — variable ETF distribution, streak concept does not apply |
| QQQ | None — FACT | ~mid-Dec 2026, UNVERIFIED (pattern-based) | Last: $0.751 (ex 2026-09-21) — FACT | ~0.44% trailing — INFERENCE | None — FACT | N/A — variable ETF distribution |
| AAPL | None — FACT (not yet declared) | ~Nov 9–10, UNVERIFIED (pattern; declaration expected with FQ4 earnings) | Last: $0.27 (ex 2026-08-10) — FACT | ~0.31% on $1.08 annualized — INFERENCE | No new declaration; May 2026 raise $0.26→$0.27 already in effect — FACT | **15** (2012 initiation + announced increase every year 2013–2026). 2013–2026 verified in Nasdaq history; 2012 initiation corroborated by secondary sources — see caveat |
| MSFT | None in window — FACT | **Nov 19, 2026**, pay Dec 10, 2026 — FACT (declared Sep 15, 2026) | **$0.98** — FACT | ~0.74% on $3.92 annualized — INFERENCE | **Increase already declared**: $0.91→$0.98 (+7.7%), announced Sep 15, 2026 — FACT | **24** per the standing count standard (incl. Sep 2026 raise; initiated 2003) — FACT per standard doc |
| NVDA | None — FACT | ~early Dec 2026, UNVERIFIED (not yet declared) | Last: $0.25 (ex 2026-09-10, paid Oct 1) — FACT | ~0.47% on $1.00 annualized — INFERENCE | **Large increase already in effect**: $0.01→$0.25 (25×), declared May 20, 2026, repeated Aug 26, 2026 — FACT (Yahoo + Nasdaq agree) | **1** (2026 only). Flat $0.01 in 2024–2025 broke any earlier run; 2024 split-adjusted nuance does not extend the streak — INFERENCE from Nasdaq history |
| TSLA | None — FACT | None expected — INFERENCE | $0 — pays no dividend — FACT | 0% — FACT | None — FACT | 0 — non-payer |

**Verification notes:**
- Nasdaq dividend calendar swept day-by-day Oct 17 – Nov 14, 2026: zero watchlist rows in-window — FACT. Endpoint validity spot-checked: the same query for Nov 19 returned the MSFT $0.98 declaration.
- Nasdaq per-name dividend history cross-checked against Yahoo Finance chart dividend events: amounts and ex-dates agree for all payers, including NVDA's $0.25 — FACT.
- Yahoo quoteSummary endpoint returned 401 "Invalid Crumb" — classified as auth-gated dead end for that endpoint; worked around via the chart endpoint + Nasdaq. No data taken from the failed endpoint.
- MSFT nuance: Nasdaq's calendar row shows "indicated annual dividend" $3.64 (= $0.91 × 4, stale) alongside the declared $0.98 rate. The $0.98 declared rate governs; the $3.64 field has not updated — FACT, flagged so the package does not copy $3.64.
- AAPL count caveat: Nasdaq's history window starts Jan 2013, so the 2012 initiation year is outside it. The 15-count = 2012 initiation (year 1 per the standard) + 14 verified increase years (2013–2026). Initiation corroborated by multiple secondary sources, not by Nasdaq/issuer history in this pull — label the 2012 leg as corroborated-secondary, not primary-verified.
- NVDA $0.25 is real, not a data error: two independent sources (Yahoo, Nasdaq) show identical amounts, ex-dates, and declaration dates for both the June and September $0.25 payments. It is a 25× regular-dividend increase, not a special (both sources type it "Cash").
- Yields computed (annualized rate ÷ Yahoo regularMarketPrice, Fri Oct 16): SPY 763.25, QQQ 709.80, AAPL 343.46, MSFT 529.05, NVDA 214.13, TSLA 354.72 — prices FACT per Yahoo; yields INFERENCE. SPY/QQQ yields use trailing-4-quarter sums (variable distributions — no forward rate exists).
- No cuts, no specials declared for any watchlist name in this pull — FACT (Nasdaq history shows only regular "Cash" dividends; calendar sweep shows no specials).

**What would change each verdict:** AAPL — declaration with FQ4 earnings (amount and ex-date UNVERIFIED; a hold at $0.27 leaves the 15-streak intact; a raise would not change the count either until a 2027 raise). MSFT — nothing pending; only a board reversal (no precedent signal). NVDA — Q3 earnings declaration sets the December ex-date; amount UNVERIFIED until then. SPY/QQQ — December amounts UNVERIFIED until declared in December; pattern timing is INFERENCE only. TSLA — any initiation would be a new fact; none signaled.

**Sources:** Nasdaq dividends calendar API (`https://api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD`, swept 2026-10-17 → 2026-11-14; spot-check 2026-11-19); Nasdaq quote dividend history (`https://api.nasdaq.com/api/quote/{T}/dividends?assetclass=stocks`); Yahoo Finance chart API (`https://query1.finance.yahoo.com/v8/finance/chart/{T}?events=div,split`, UA header); count standard `~/workspace/hedge-desk-research/dividend-count-standard.md`.

---

## 3. Overnight Premium desk (IV)

**IV-inputs freshness guard — FRESH (within 26h).** File checked: `~/workspace/hedge-desk-research/nightly/2026-10-16-iv-inputs.json`. `as_of`: 2026-10-16T13:54:32.251757-07:00 → age ≈ 23h40m at this run → **FRESH** per the 26h guard. **Critical caveat:** the file's `atm_iv` values are **0-DTE same-day-expiry values** (`iv_dte: 0`, `iv_expiry: 2026-10-16`), now expired — e.g. SPY 1.94%. They are NOT comparable to term IV and must not be quoted as current IV levels. The file's usable content is `realized_20d`, `max_single_day_variance_share`, `window_contingent`, and `next_earnings`. File's own note: `_failover` — legacy Yahoo-only pull; `hedge_desk.data.options_failover` unavailable in this clone.

**Verdict:** Vol jumped Friday on a broad selloff (VIX +21% to 19.99, 81st percentile of its 1-year range) — premium is ELEVATED at the index level, not cheap. Per-symbol IV exceeds trailing 20-day realized for every name, but for SPY, QQQ, AAPL, and MSFT the verdict is WINDOW-CONTINGENT (one day drives >30% of each realized window), so no clean "rich premium" call is valid there. The two clean reads: NVDA IV (29–40%) sits above realized (25.0%); TSLA pre-event IV (~33–36%) ≈ realized (31.4%). Two earnings humps are priced and must be avoided for premium-selling: TSLA (Oct 21) and MSFT (Oct 28).

**Live IV snapshot (supplemental live pull, labeled).** Sources: Nasdaq option-chain API (bid/ask mids, Fri Oct 16 close — prices cross-checked to Yahoo Fri Oct 16 closes exactly, though Nasdaq's own "as of Oct 15" label is stale by one day) + Yahoo chart API v8 for closes/VIX/VXN + FRED DGS3MO for the rate. Method: Black-Scholes inversion on ATM call/put mids; r = 4.28% (FRED DGS3MO, 2026-10-15, latest available); q = 0 (dividend omission — biases SPY/QQQ call IV low / put IV high; visible in the call–put IV gap and in SPY/QQQ parity diffs ≈ −$0.50, consistent with omitted dividends; single-name parity diffs ≈ $0). T in calendar days from Fri Oct 16 close (weekend effect understates the 3-DTE Monday-expiry IVs). Nasdaq returned only ≤14-DTE expiries, so **30-day chain IV is UNVERIFIED from the chain**; VIX 19.99 is the 30-day anchor.

| Symbol | Fri close | Realized 20d (file) | Max 1-day var share | Window | ATM IV, near expiry | ATM IV, far expiry (14-DTE) | Earnings hump? |
|---|---|---|---|---|---|---|---|
| SPY | 763.25 (−1.1% Fri) | 9.84% | 33.8% | **WINDOW-CONTINGENT** | 10.1% C / 12.4% P (3-DTE) | 14.2% C / 15.1% P | None — smooth upward slope |
| QQQ | 709.80 (−2.5% Fri) | 16.57% | 41.0% | **WINDOW-CONTINGENT** | 18.3% C / 20.1% P (3-DTE) | 23.9% C / 24.6% P | None — smooth upward slope |
| AAPL | 343.46 (+0.4% Fri) | 16.66% | 36.4% | **WINDOW-CONTINGENT** | 19.6% C / 20.1% P (3-DTE) | 25.2% C / 24.7% P | None in window (earnings Nov 2, outside shown expiries) |
| MSFT | 529.05 (−1.9% Fri) | 21.07% | 36.1% | **WINDOW-CONTINGENT** | 18.8% C / 19.0% P (3-DTE) | **38.4% C / 38.9% P (Oct 30, contains Oct 28 earnings)** | **YES — Oct 30 expiry** |
| NVDA | 214.13 (−1.4% Fri) | 25.03% | 22.9% | Not contingent | 28.9% C / 30.5% P (3-DTE) | 36.8% C / 37.1% P | None (earnings Nov 18, outside window) |
| TSLA | 354.72 (−2.1% Fri) | 31.36% | 29.5% (borderline) | Not contingent* | 33.3% C / 35.6% P (3-DTE, pre-earnings) | **56.0% C / 56.6% P (Oct 30)**; Oct 23 expiry 66.8% C / 67.3% P | **YES — Oct 23 expiry** |

\* TSLA 29.5% is just under the 30% threshold — treat as borderline; one more large day flips it to WINDOW-CONTINGENT.

**IV-vs-realized verdicts (each states what would change it):**
- SPY — WINDOW-CONTINGENT. Live IV (10–15%) > realized (9.8%), but the realized window is polluted by one day (33.8% share). *Would change:* a clean 20-day window with no single day >30%, or a 30-day chain read.
- QQQ — WINDOW-CONTINGENT. Live IV (18–25%) > realized (16.6%), same pollution (41.0% share). *Would change:* same as SPY.
- AAPL — WINDOW-CONTINGENT. Live IV (20–26%) > realized (16.7%), polluted (36.4% share). *Would change:* clean window; confirmation of the Nov 2 earnings date (confirmed by Earnings desk — see cross-desk note).
- MSFT — WINDOW-CONTINGENT + earnings hump. Pre-event IV (19–25%) ≈ realized (21.1%); Oct 30 expiry (38–39%) is elevated by earnings, not naive "richness." *Would change:* clean window; post-earnings IV crush observation.
- NVDA — IV above realized (clean window). Live IV 29–40% vs realized 25.0%; no contamination. Premium not obviously cheap; NVDA fell 6.7% over the 5-day window (229.28 → 214.13), so realized may be re-rating up. *Would change:* realized re-measurement after this week's selloff washes through, or an IV crush.
- TSLA — IV ≈ realized pre-event; event premium dominates after. Pre-earnings expiry IV 33–36% ≈ realized 31.4% (no edge either way); event expiries 56–67% are pure binary-event premium. *Would change:* post-earnings crush; a single large day pushing the window over 30% (would void the clean read).

**Elevated-IV flags:**
- ELEVATED (index level, FACT): VIX 19.99, +21% Friday (16.46 → 19.99), **81.1st percentile** of its 1-year range (n=254, min 13.47, max 31.05, median 17.1). VXN 27.13, **79.7th percentile** (n=251, median 23.24). Top-quintile vol regime — premium is elevated, not cheap.
- Per-symbol IV rank: UNVERIFIED. No free source for 52-week per-symbol IV history was available this run. The VIX/VXN percentiles above are an index-level regime gauge, NOT per-symbol IV rank — do not present them as such.
- Yahoo options endpoint FAILED (401) on direct pull; crumb/cookie route also failed (connection closed). Fallback was the Nasdaq chain API per the market-data rule — labeled above.

**Earnings inside the window (premium into a binary event = avoid):**
- TSLA — Oct 21 (Wed), INSIDE window — AVOID premium into it. Oct 23 expiry IV (66.8–67.3%) is ~2× the pre-event Oct 19 expiry (33.3–35.6%); Oct 23 ATM straddle mid $26.27 implies a **7.41% move** through earnings. The hump itself is FACT; the attribution to earnings is INFERENCE from the calendar date.
- MSFT — Oct 28 (Wed), INSIDE window — AVOID premium into it. Oct 30 expiry IV (38.4–38.9%) vs 24% at Oct 26; Oct 30 ATM straddle mid $31.95 implies a **6.04% move** (covers earnings + 2 extra days, so the pure earnings component is smaller).
- AAPL — Nov 2, OUTSIDE shown window. No hump observable in ≤14-DTE expiries. Date confirmed by Earnings desk (Nasdaq calendar).
- NVDA — Nov 18, OUTSIDE window. No hump; date Nasdaq-sourced, timing UNVERIFIED.
- SPY/QQQ: no earnings; no hump; gently upward-sloping term structure (normal, no event).

**Parity check (deterministic math outranks models):** Put-call parity checked on every ATM pair: single-name parity diffs ≈ $0.00–$0.30 (PASS); SPY/QQQ diffs ≈ −$0.50 to −$0.67, sign and size consistent with the omitted dividend yield (PASS with explained cause). No parity violation found; no chain data rejected on parity grounds. *Would change:* a diff >$1.00 unexplained by dividends would indicate stale quotes, and that expiry's IV would be discarded.

**Sources:** iv-inputs file `~/workspace/hedge-desk-research/nightly/2026-10-16-iv-inputs.json`; Yahoo chart API (`https://query1.finance.yahoo.com/v8/finance/chart/{^VIX,^VXN,SPY,QQQ,AAPL,MSFT,NVDA,TSLA}` — Yahoo options v7 endpoint 401-blocked this run); Nasdaq option-chain API (`https://api.nasdaq.com/api/quote/{symbol}/option-chain?assetclass={stocks|etf}&limit=2500`); FRED DGS3MO (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO`, 4.28% as of 2026-10-15).

**UNVERIFIED, fail closed:** per-symbol IV rank (no free 52-week IV history); 30-day per-symbol chain IV (Nasdaq returned only ≤14-DTE expiries). No Risk of Ruin computed or estimated; no trade authorization proposed.

---

## 4. Open Quant/AI Model Lab

**Verdict:** 19 new candidates scored; **none reached TEST or INTEGRATE** (scorer max 63; TEST needs 65). 9 new WATCH, 10 new ARCHIVE. No candidate lives only in a daily file — all 19 appended to the ledger (`~/workspace/hedge-desk-research/quant-lab-ledger.md`, rows #85–103, verified present).

**Sweep coverage (FACT):** arXiv API across q-fin.PR/ST/RM/MF/CP/TR/PM/GN + stat.AP/stat.ML for submittedDate 2026-10-15→17, plus catch-up abstracts for missed Oct 1–13 items. GitHub search API returned empty bodies twice (proxy-level) → classified transient-exhausted after 2 strikes, switched to direct `/repos/` endpoints + web search (per kaizen rule). Weekend window Oct 16–17 is genuinely empty for q-fin (verified against a no-filter control — arXiv announces weekdays). No new q-fin submissions Oct 16–17.

**New WATCH (scored with repo scorer, reasons on file):**

| # | Candidate | Score | Disposition | One-line reason |
|---|---|---|---|---|
| 85 | "When Does 'Post-Call' Begin?" — Availability Contract for Earnings-Call NLP Benchmarks (arXiv:2610.21659, ICAIF 2026) | 51 | WATCH | Within-event timing mismatch: chronological splits don't prevent lookahead inside events. Availability-contract checklist for any earnings-call NLP input. No code. |
| 86 | End-of-month option in futures + Gittins index (arXiv:2610.21196 + github.com/ebayr/eom-gittins) | 63 | WATCH | Code verified (code/ dir) but **NO LICENSE → line-stopped at WATCH** per #20/#32 precedent. Delivery-option pricing, futures-desk relevant. |
| 87 | conformalForecast R package (arXiv:2610.21648 + CRAN 0.2.0, GPL-3) | 63 | WATCH | Conformal intervals for multistep time-series forecasts; CRAN tarball + GPL-3 verified. TEST opens on sandbox evidence (65 needed). |
| 88 | RTCARE expectile VaR/ES forecasting (arXiv:2610.13446) | 51 | WATCH | Realized tail measures in expectile dynamics; US stock application, claims source-reported UNVERIFIED. No code. |
| 89 | Negative Oil & Nickel Squeeze feedback model (arXiv:2610.00951) | 48 | WATCH | Catch-up (1 Oct, missed earlier). Roll-option + delivery-constraint imbalance framing; futures-desk relevant. No code. |
| 90 | CorrFlow correlation-elliptope flow matching (arXiv:2610.13606 + code, MIT verified) | 57 | WATCH | Valid correlation-matrix generation without projection. Marginal desk relevance (scenario generation). |
| 91 | L₀ Feature Selection via MCTS (arXiv:2610.13574, ICAIF '26) | 45 | WATCH | Subsets scored by OOS validation, not in-sample — purged-WF-adjacent. Band floor. No code. |
| 92 | E-Backtesting ES without VaR forecasts (arXiv:2610.17681) | 45 | WATCH | Anytime-valid e-backtests; #34 frozen-referee theme. Band floor. No code. |
| 93 | OAS shrinkage extension to general distributions (arXiv:2610.22144) | 45 | WATCH | 4th-cumulant correction, closes OAS–Ledoit-Wolf gap (source-reported). Marginal (covariance, not a desk input). Band floor. No code. |

**New ARCHIVE (band discipline, all <45, abstracts read at source):** #94 LLM earnings forecasts tone-vs-surprise (40, synthetic data); #95 American commodity options Schwartz ADE (37); #96 long-horizon delayed info (36); #97 rough SABR boundary (33); #98 fundamental theorem discrete asset pricing (30); #99 algorithmic collusion Q-learning (30); #100 LVR with transaction costs (30, crypto-AMM); #101 SABR right wing absorbing boundary (30); #102 ML portfolio attribution (42); #103 STOCK-JEPA (34).

**Ledger updates confirmed:** 19 new rows (#85–103) verified present in `~/workspace/hedge-desk-research/quant-lab-ledger.md`. Also updated #51: **deep-hedging-lab repo no longer resolves** — owner's full repo list (12 repos) contains no deep-hedging-lab → deleted or renamed, not a transient miss; sandbox blocked until it resolves. Added 2026-10-17 Jidoka + Kaizen entries (GitHub search leg, arXiv weekend-window control, CRAN 303 check).

**Evidence labels:** All scores recomputed with the repo scorer this run (inputs documented above); abstract-level claims are source-reported and labeled UNVERIFIED where not run. Code/license facts verified via GitHub API / CRAN directly (FACT). No TEST/INTEGRATE claims made — nothing was sandboxed this run; #80 sandbox remains pending next cycle. Triage exclusion (no row): anthonymakarewicz/volatility-trading — created 2025-06-18, stale since 2026-04-01, ORATS paid-data gated.

**What would change the verdicts:** #86/#87 advance on license resolution (86) / sandbox run (87); WATCH items advance only on code release + sandbox evidence, never on interest.

---

## 5. Weather / War / Logistics Futures Event desk

**Verdict:** The dominant catalyst is war-driven energy disruption, not weather or harvest. The US–Israel–Iran war's shipping attacks around Hormuz, record tanker freight, a diesel crunch the IEA now says lasts into 2H 2027, and China's October fuel-export halt have put a large, front-loaded risk premium into crude — WTI Nov settled $101.41 Fri Oct 16 (+10.4% w/w), in steep backwardation. Against that, the ag complex is a supply-glut story: the Oct 9 WASDE raised corn/soy/wheat carryouts and knocked futures down, CONAB's Oct 15 first 2026/27 survey projects record Brazilian soy and bigger corn, and US harvest is only modestly behind pace. Natural gas sits between the two: a lean +67 Bcf storage build and regional tightness, but a curve that prices a January winter peak and then collapses into spring.

### Fresh catalysts triaged

**A. Middle East war / Hormuz shipping — DOMINANT, still live**
- FACT: Attacks on tankers/shipping in and around the Strait of Hormuz hit their highest weekly count since the war began in the week before Oct 8, as Gulf producers raised exports (Reuters, Oct 8). [Source](https://www.reuters.com/business/energy/oil-rises-middle-east-supply-concerns-persist-amid-shipping-attacks-2026-10-08/)
- FACT: A Saudi-led coalition said it intercepted a ballistic missile aimed at the Red Sea export port of Yanbu on Fri Oct 16, with no damage reported (Reuters, via FinanceFeeds). [Source](https://financefeeds.com/brent-crude-oil-price-110-week-ahead-highest-settle-since-may-bull-115-bear-100/)
- FACT: IEA Oct 14 Oil Market Report: Gulf crude exports surged +4.4 mb/d to 13.9 mb/d in September (>75% of pre-war); Hormuz flows +3.7 mb/d to 10.9 mb/d; but refined-product exports only 1.9 mb/d vs 4.7 mb/d pre-war, and "recent escalation in attacks… is threatening to derail further gains." [Source](https://www.iea.org/reports/oil-market-report-october-2026)
- FACT: Kpler data (via OilPrice, week to Oct 13): ~11.62 mb/d through Hormuz vs a 17.15 mb/d baseline. *Note the baseline differs from IEA's pre-war framing — reported as-is, not reconciled.* [Source](https://financefeeds.com/brent-crude-oil-price-110-week-ahead-highest-settle-since-may-bull-115-bear-100/)
- INFERENCE: The market is pricing crude as "flowing but interruptible": volumes recovered, but the premium stayed. **What would change it:** a verifiable ceasefire / sustained multi-week halt in attacks, or Hormuz flows back near pre-war levels with product exports recovering too.
- UNVERIFIED (freshness): LNG flows through Hormuz "still more than 75% below pre-war levels, QatarEnergy still under force majeure" was reported in an ~Oct 6 piece and was **not** re-verified in this week's sources. [Source](https://www.orivyn.com/insights/geopolitical-risk-trading-and-risk-systems.html)

**B. Record tanker freight / insurance — the transmission mechanism**
- FACT: OPEC+ ministers (Declaration of Cooperation, Riyadh, Oct 12) warned shipping + insurance costs "exceeded one-third of the value of the commodities being transported," delaying shipments and adding to inflationary pressure. [Source](https://www.logisticsmanager.com/opec-warns-soaring-shipping-costs-are-disrupting-global-oil-trade/)
- FACT: Poten & Partners figures (via ShipUniverse): Middle East→Asia VLCC earnings >$1.2M/day; freight share ~27% of delivered oil value vs ~3% historically; US Gulf→Europe ~$24.50/bbl (vs ~$4/bbl pre-war); US Gulf→Asia ~$40/bbl. *OPEC published no route-by-route methodology for its "one-third" figure — do not read it as applying to every cargo.* [Source](https://www.shipuniverse.com/news/opec-warns-shipping-and-insurance-now-consume-more-than-one-third-of-energy-cargo-value/)
- FACT: Reuters (Oct 9, via UrbanPetro): chartering a VLCC for ~2M bbl US Gulf→China in November reached ~$80M, making some US→Asia crude uneconomic. [Source](https://urbanpetro.com/global-oil-trade-tanker-costs-october-2026/)
- FACT: Reuters (Oct 13): freight for Russian Urals, Black Sea→India, hit record $27–30M per Suezmax voyage (vs ~$19M in September); Baltic→western India Aframax $21–23M (vs ~$13–16M in September); cross-Mediterranean rates exceeded Worldscale 900. [Source](https://www.reuters.com/business/energy/freight-rates-russian-urals-oil-shipments-india-hit-fresh-records-early-october-2026-10-13/)
- INFERENCE: Freight is no longer a rounding error — it is segmenting the market by route and origin, favoring nearby barrels. **What would change it:** a sustained drop in VLCC rates / war-risk premiums on published fixtures.

**C. Diesel crunch + emergency stock releases**
- FACT: IEA Oct 14: global diesel/gasoil availability cut 1.5 mb/d in 2Q26 and 1.7 mb/d in 3Q26 vs a year earlier; combined Middle East + Russia net diesel exports fell 1.3 mb/d to 820 kb/d; diesel stocks "unlikely to be rebuilt before 2H 2027." North Sea Dated averaged $116.89/bbl in September (+$26.17 m/m) and was ~$134 at report writing; Brent futures ~$107, +13% since early September. [Source](https://www.iea.org/reports/oil-market-report-october-2026)
- FACT: IEA Oct 14: 2026 global oil demand −2.6 mb/d to 102.4 mb/d; 2027 demand +2.0 mb/d (620 kb/d below 2025); 2026 supply −5.8 mb/d; effective OPEC+ spare capacity 0.27 mb/d excl. shut-in Iranian/Russian barrels. [Source](https://www.thefinancialeconomy.com/iea-oil-market-report/)
- FACT: IEA members agreed Oct 15 to expedite release of >20M bbl of diesel and accelerate the emergency oil draw; ~330M bbl of the March 400M-bbl coordinated release had been released by end-September (IEA via TankTerminals/OilPrice). [Source](https://tankterminals.com/news/iea-speeds-emergency-oil-release/)
- UNVERIFIED (single secondary source): FinanceFeeds reports the US DOE on Fri Oct 16 issued an RFP to exchange up to 17M bbl from the SPR. Not corroborated by a second source in this sweep — treated as unconfirmed. [Source](https://financefeeds.com/brent-crude-oil-price-110-week-ahead-highest-settle-since-may-bull-115-bear-100/)
- INFERENCE: Releases are bridging a product (diesel) shortage, not a crude shortage — they cap but do not remove the premium. **What would change it:** Middle East + Russian product exports recovering toward pre-war levels, or diesel cracks collapsing on verified inventory rebuilds.

**D. Russia / Ukraine refinery war**
- FACT: A Ukrainian drone strike shut a main unit at a large Russian refinery on Fri Oct 16 (Reuters, via FinanceFeeds). [Source](https://financefeeds.com/brent-crude-oil-price-110-week-ahead-highest-settle-since-may-bull-115-bear-100/)
- FACT (second-hand): Russia extended its producer diesel-export ban through Oct 31 (Energy News Beat, Oct 1). [Source](https://energynewsbeat.com/diesel/china-now-adding-stress-to-diesel-markets-where-do-we-go-from-here/)
- INFERENCE: Russian product exports are a second, independent leg of the diesel shortage alongside the Gulf. **What would change it:** verified resumption of Russian refinery runs / lifting of the export ban.

**E. China halts October refined-fuel exports**
- FACT: Chinese refiners suspended October exports of diesel, gasoline, and jet fuel except to Hong Kong/Macao; PetroChina canceled some gasoline/jet cargoes; Beijing granted no October export approvals (Reuters, via EIR, Oct 1–2). September exports were 1.4M tons diesel, 500k tons gasoline, ≥2M tons jet fuel. [Source](https://eir.news/2026/10/news/china-halts-fuel-exports-for-october/)
- INFERENCE: Removes a swing supplier exactly when Gulf/Russian products are short — a marginal but real tightening for Asian diesel. **What would change it:** Beijing granting November export quotas / a reported resumption of cargoes.

**F. EIA Weekly Petroleum Status — big crude draw (Thu Oct 15, delayed from Wed by Columbus Day)**
- FACT: EIA: commercial crude −8.6M bbl w/e Oct 9 to 415.6M bbl, vs ~0.3M-bbl expected draw (RTT/Dow Jones polls differed: −0.3M vs +0.1M); second straight large draw (prior week −3.2M). API had reported −11.12M bbl. [Sources](https://www.tradingview.com/news/dpa_afx:c08dc7aaf5771:0-u-s-crude-oil-inventories-slump-much-more-than-expected/) / [Source](https://oilprice.com/Latest-Energy-News/World-News/US-Crude-Oil-Inventories-See-Massive-Drop-Off.html)
- ⚠️ PROVIDER CONFLICT (reported, not resolved): OilPrice says 415.6M bbl is **3% above** the five-year average; RTT/TradingView says **3% below** the five-year average. Per trace rules, no winner picked — the draw size (−8.6M) is consistent across sources; the vs-average framing is not.
- FACT: Gasoline +3.5M bbl to 208.3M (−4% vs 5-yr avg per RTT); distillates −2.5M bbl to 102.6M (−12% vs 5-yr avg); Cushing +1.9M bbl; refinery utilization 93.5% (runs 16.6M b/d); total products supplied 21.1M b/d 4-wk avg (+2% y/y); SPR unchanged at 283M bbl. [Sources](https://informistmedia.com/CommodityWire/62206/US-Crude-US-crude-oil-stocks-fall-2-37-to-415-6-mln-bbl-in-week-ended-Oct-9-says-EIA) / [Source](https://en.hathalyoum.net/articles/301797)
- INFERENCE (DTN): The draw partly reflects hurricane-induced offshore production shut-ins coinciding with the end of emergency stock releases; DTN also reports >132M bbl of SPR oil reached the market end-March to early October. **What would change it:** next Wednesday's report showing whether the draw repeats once shut-ins recover.

**G. EIA Natural Gas Storage — lean build (Thu Oct 15, 10:30 ET)**
- FACT: +67 Bcf injection w/e Oct 9 vs ~75 Bcf WSJ survey and ~90 Bcf five-year average; working gas 3,567 Bcf — +45 Bcf (+1.3%) vs 5-yr avg 3,522 Bcf, −143 Bcf (−3.9%) vs year-ago 3,710 Bcf. [Sources](https://www.haawks.com/blog/2026/10/15/eia-natural-gas-storage-37-tick-market-reaction) / [Source](https://naturalgasintel.com/news/following-bullish-storage-print-natural-gas-futures-sustain-rally/)
- FACT: Regional split matters: South Central stocks 1,097 Bcf vs 1,132 Bcf 5-yr avg; salt-cavern inventory 236 Bcf vs 279 Bcf avg (FXEmpire, from EIA data). [Source](https://www.fxempire.com/forecasts/article/natural-gas-eyes-dip-buyers-as-3-level-and-50-day-ema-offer-support-1638614)
- FACT (single-source): Columbia Gas Transmission suffered a second pipeline outage in three weeks (Energy Intelligence, Oct 16 headline). Not independently corroborated in this sweep.
- INFERENCE: National surplus is thin and regionally uneven — a cold snap bites faster in the South Central salt complex than the headline suggests. **What would change it:** next Thursday's build vs the ~90 Bcf seasonal norm; pipeline-restoration notices.

**H. Weather — brief cold snap, not a regime change**
- FACT (forecast, via Price Group citing Fox Weather): A sharp early-season cold front swept the central/eastern US into the weekend of Oct 17–18, with 30–40°F drops, first widespread hard freezes in the Dakotas/Minnesota/Wisconsin/Iowa; high pressure and above-normal temperatures return next week. [Source](https://blog.pricegroup.com/2026/10/16/roll-out-the-barrels-the-energy-report-10-16-2026/)
- INFERENCE: A short-lived heating-demand spike that trims the next storage build, then mild weather caps sustained withdrawals. **What would change it:** model convergence (ECMWF vs GFS) on sustained cold in the 10–15-day window.

**I. USDA WASDE Oct 9 — bearish grains (past, still pricing)**
- FACT: Corn yield raised to **181.2** bu/acre (ADMIS/RFD-TV; one secondary source printed 181.1 — 0.1 bu discrepancy flagged, production/ending-stocks figures agree), production 16.034B bu (+234M), ending stocks 1.849B bu (+282M), season-avg farm price cut $0.10 to $4.70/bu. Second-largest US corn crop if realized. [Sources](https://www.admis.com/usda-oct-9-usda-bearish-corn-neutral-wheat/) / [Source](https://www.rfdtv.com/wasde-recap-usda-raises-grain-supplies-as-futures-fall-sharply)
- FACT: Soybean yield record 53.1 bu/acre, production record 4.562B bu, ending stocks 315M bu (+5M), exports +10M to 1.695B bu, price unchanged $12.00/bu. Wheat production 1.534B bu (smallest since 1970), ending stocks 740M bu (+23M), price cut $0.10 to $6.30/bu. [Source](https://www.brownfieldagnews.com/news/u-s-corn-soybean-wheat-ending-stocks-all-up-on-month/)
- FACT: Market reaction on WASDE day: corn futures ~−5%, soybeans ~−2%, wheat ~−3% (RFD-TV). [Source](https://www.rfdtv.com/wasde-recap-usda-raises-grain-supplies-as-futures-fall-sharply)
- FACT: Next WASDE: **Tue Nov 10, 2026, 12:00 ET** (USDA official calendar). *One stale/contradictory search result floated a Nov 14 date tied to shutdown-delay framing — disregarded per the standing government-data rule and the official USDA calendar.* [Source](https://www.usda.gov/oce/commodity/wasde/?mod=article_inline)

**J. USDA Crop Progress (released Tue Oct 13, Columbus Day delay) — harvest behind, Iowa worst**
- FACT: As of Sun Oct 11: corn 33% harvested vs 39% five-year avg; soybeans 46% vs 50%; corn 91% mature; corn good-to-excellent 56%. Iowa: corn 14% vs 34% avg; soybeans 31% vs 59% avg. [Source](https://www.dtnpf.com/agriculture/web/ag/crops/article/2026/10/13/usda-crop-progress-corn-33-harvested)
- INFERENCE: Delayed harvest + big crop = harvest-pressure selling and storage/bin pressure, consistent with the contango in the corn/soy curves below. **What would change it:** next Crop Progress (expected Mon Oct 19) showing a catch-up week, or a wet forecast stalling the Midwest.

**K. CONAB Brazil first 2026/27 survey (Thu Oct 15) — big South American crops coming**
- FACT: Total grain 367.1M tons (+1.4%); soybeans record 181.6M tons (+0.7%) on 49.3M ha (+1.4% — slowest area expansion in 20 years); corn 148.0M tons (+2.4%) on area +4.9% (implied yields down); soybeans 9.4% planted by Oct 2 (vs 8.8% 5-yr avg); first-crop corn 30.8% planted. [Sources](https://brownfieldagnews.com/news/conab-sees-sizable-soybean-corn-crops-in-brazil/) / [Source](https://revistacultivar.com/news/Conab-forecasts-367.1-million-tons-of-grains-in-2026.)
- FACT: CONAB's next update: Nov 13 (per Brownfield). [Source](https://brownfieldagnews.com/news/conab-sees-sizable-soybean-corn-crops-in-brazil/)
- INFERENCE: US export competition intensifies into early 2027; the bearish WASDE carryout has a Southern Hemisphere echo. **What would change it:** an El Niño disruption to Brazilian planting (flagged as a risk by CONAB coverage, not yet an event).

### What the futures curves appear to be pricing (Yahoo Finance, Fri Oct 16 closes, UA header)

| Market | Front | Deferred | Shape | Read |
|---|---|---|---|---|
| WTI crude | Nov (CLX26) **$101.41** | Dec **$99.02**, Jan **$97.44**, Feb **$95.48**, Mar **$93.53** | Backwardation: Mar −$7.88 (−7.8%) vs Nov | Prompt war-risk premium; market prices disruption fading over ~5 months |
| Brent crude | Dec (BZZ26) **$109.86** | — | Brent–WTI Dec spread **+$10.84** | Atlantic-basin / war-risk premium wider than usual; physical Dated ($134 at IEA writing) > futures |
| Heating oil (diesel proxy) | Nov **$4.8991/gal** | — | — | Product premium intact; Fri +1.10% |
| RBOB gasoline | Nov **$3.2354/gal** | — | — | Firmer than crude's product siblings would suggest, +1.74% Fri |
| Nat gas | Nov **$3.116** | Dec **$3.386** (+8.7%), Jan **$3.759** (+11.0% vs Dec), Apr **$2.564** (−31.8% vs Jan) | Contango into winter peak, then sharp backwardation to spring | Winter heating-demand peak priced; market does NOT price a sustained winter shortage — spring collapses |
| Corn | Dec **474.25¢** ($4.7425/bu) | Mar **486.5¢** (+12.25¢), May **493.5¢** (+7¢) | Contango (carry) | Market pays to store a big crop; no near-term scarcity |
| Soybeans | Nov **1261.25¢** ($12.6125/bu) | Jul **1298¢** (+36.75¢) | Contango (carry) | Same carry logic; record crop + Brazil coming |
| Wheat | Dec **660.5¢** ($6.605/bu) | Mar **675¢** (+14.5¢) | Contango (carry) | Carry despite smallest crop since 1970 — stocks adequate |
| Soybean oil | Dec **67.13¢/lb** | — | — | Matches the 67.13¢ print cited in WASDE-preview coverage |

**Week context (FACT):** WTI +10.4% w/w, Brent +4.9% w/w (Reuters via FinanceFeeds); Yahoo 5-day closes confirm the WTI run: $93.74 → $94.14 → $95.09 → $97.97 → $101.41. Friday's +$3.44 WTI / +$3.94 Brent settle is corroborated by Yahoo contract closes and the commodities wrap. [Source](https://edgeconsultancykw.com/commodities-wrap-16-october-2026/)

**Curve inference (labeled):** Crude backwardation + products at premiums + grains in carry = a market pricing *energy disruption now, energy normalization later, and grain abundance throughout*. The crude curve's ~$8 fade by March is the market's implied "disruption half-life" — it is a price, not a forecast. **What would change it:** either a ceasefire (front collapses faster than deferred) or a Hormuz closure / major refinery loss (front spikes, backwardation steepens).

**EIA STEO (second-hand, via FinanceFeeds citing EIA Oct 6):** EIA expects Brent to average **$105** in Q4 2026, $14 above its September forecast, assuming Middle East shut-ins average 4.5 mb/d this quarter. Current Dec Brent ($109.86) trades above that quarterly-average assumption.

### Watchlist read (equity context — INFERENCE, magnitude UNVERIFIED)

Sustained diesel tightness + record freight is a margin and logistics-cost headwind that falls unevenly: hardware / physical-supply-chain names (AAPL, NVDA, TSLA) face higher inbound freight and component-shipping costs, while MSFT's exposure runs more through data-center energy / diesel-backup operating costs. No watchlist-specific catalyst from this desk this week; nothing here is a trade input. **What would change it:** verified freight-rate normalization or a company-specific disclosure quantifying exposure.

### Catalyst calendar — what is next
- **Mon Oct 19:** USDA Crop Progress (expected, ~4pm ET)
- **Tue Oct 20:** API weekly inventories (expected)
- **Wed Oct 21:** EIA Weekly Petroleum Status, ~10:30 ET (expected; this week's was delayed to Thu by Columbus Day)
- **Thu Oct 22:** EIA Natural Gas Storage, 10:30 ET (expected); USDA Export Sales, 8:30 ET (expected)
- **Tue Nov 10:** WASDE + Crop Production, 12:00 ET (USDA official calendar)
- **Thu Nov 13:** CONAB update (per Brownfield)
- **Ongoing, unscheduled:** Hormuz / Red Sea attacks, Houthi attacks, Russian refinery strikes, any ceasefire diplomacy, Beijing's November fuel-export quota decision.

### Disconfirming evidence checked
- The "crude squeeze" reading is tempered by: gasoline built (+3.5M bbl), Cushing built (+1.9M), and the vs-5-yr-average conflict on crude (see §F) — the draw is real, a national stock-out is not established.
- The "gas shortage" reading is tempered by: storage still +1.3% above the 5-yr average and the April contract 32% below January — the market is not pricing a winter stock-out.
- The "grain glut" reading is tempered by: harvest still behind pace (esp. Iowa), CONAB yields implied down, and El Niño flagged as a live Brazilian risk — supply is large, not yet secured.

### Sources (primary where available)
EIA via secondary reporting (OilPrice, RTT/TradingView, Informist, NGI, HAAWKS); IEA Oil Market Report Oct 2026 (primary); USDA WASDE calendar (primary, usda.gov); USDA Crop Progress via DTN; CONAB via Brownfield/Cultivar; OPEC+ via Logistics Manager; Reuters via FinanceFeeds/UrbanPetro; Yahoo Finance contract closes (CLX26, CLZ26, CLF27, CLG27, CLH27, BZZ26, NGX26, NGZ26, NGF27, NGJ27, ZC=F, ZCH27, ZCK27, ZS=F, ZSN27, ZW=F, ZWH27, HO=F, RB=F, ZL=F, LE=F).

---

## 6. Box / Parity Observer

**Verdict: Parity holds. No new watchlist-relevant methodology change today. No new published parity-violation analysis found. One item new to this desk: Cboe began disseminating a 2026 SPX box-rate index (BOX20X26).**

### Deterministic parity check — SPY Oct 23, 2026 expiry [FACT — computed from live Yahoo bid/ask]
- **As-of:** Yahoo Finance options chain pulled Sat 2026-10-17 ~1:27pm PT; quotes are Fri 2026-10-16 closing marks (regularMarketTime 20:00 UTC). S = **763.25**.
- Put-call parity implied forwards (F ≈ K + C − P, mid quotes): K=755 → F = **763.42**; K=760 → **763.40**; K=763 → **763.38**; K=765 → **763.37**; K=770 → **763.29**. Implied forwards cluster within a **13¢** range, ~0.1–0.17 above spot — consistent with a small forward premium (rates minus dividends) over 7 days, not a dislocation.
- **Box test, strikes 755/770 (payoff 15.00 at expiry):** mid-price cost **15.12**; **executable at the touch: 15.80** (buy C755 ask 12.14 − sell P755 bid 3.39 − sell C770 bid 2.62 + buy P770 ask 9.67) for a 15.00 payoff = **−0.80 gross**. **No executable arbitrage.**
- **Caveats [INFERENCE]:** SPY options are American-style, so parity is an inequality (early-exercise premium), and these are closing marks. The math wins: the executable box loses money, so there is no violation to trade.
- *What would change this verdict:* an executable box netting more than all-in transaction costs on live (non-close) quotes.

### Index methodology — nothing new for the watchlist
- **Cboe box-rate index, new to this desk [FACT as reported]:** Cboe Global Indices Feed began disseminating "Box Rate on 2026 SPX Option" (symbol **BOX20X26**), effective **Oct 7, 2026**. This is an index *of* box-implied rates, not a methodology change — no parity impact. Source: https://cdn.cboe.com/resources/release_notes/2026/20261006_Update_Index_Vendor_BOX20X26.pdf
- **Nasdaq-100 methodology update — NOT new [FACT]:** implemented May 1, 2026 (published May 8, updated Aug 6): full-market-cap eligibility incl. unlisted shares, rank-based quarterly reviews, Fast Entry for top-40 listings, graduated float-based weight cap replacing the 10% minimum-float rule. Already covered in prior runs; no fresh action. Source: https://www.nasdaq.com/newsroom/nasdaq100-index-methodology-update-why-now
- **S&P 500 constituent changes — NOT new, already effective [FACT as reported]:** Twilio (TWLO) replaced Warner Bros. Discovery, Vylor (VYLR) replaced Corteva, effective before open Oct 6 (announced Oct 1). Routine corporate-action-driven changes, not methodology. Source: https://www.prnewswire.com/news-releases/vylor-added-to-the-sp-500-twilio-set-to-join-sp-500-others-to-join-sp-midcap-400-and-sp-smallcap-600-302896675.html
- **S&P/TSX eligibility change — NOT new, no watchlist impact [FACT as reported]:** foreign-incorporated TSX issuers with a "material and substantive connection" to Canada become eligible effective Dec 21, 2026. Canadian indices only. Source: https://www.reuters.com/world/americas/sp-dow-jones-indices-loosens-canadian-index-inclusion-criteria-2026-09-13/
- **Nasdaq index terminations — irrelevant [FACT as reported]:** Nasdaq will cease calculation of two Iceland bond indices (NOMXIBBTA, NOMXINOMTA) after close Thu Oct 29, 2026. No watchlist impact. Source: https://www.nasdaqtrader.com/tradernews.aspx?id=fpnews2026-67

### Published parity-violation analysis — none new found
- Sweep returned only evergreen educational material, trade-idea blogs, and the already-known BOXX tax coverage — **no new empirical box-spread / put-call parity violation study found**. [Finding of this sweep, not proof of nonexistence.]
- **Corroborating secondary evidence [FACT as reported]:** Saxo's Oct 15 Options Brief reports the VIX futures parity forward consistent to **0.05** across the five nearest strikes — parity holding in that market too. Source: https://www.home.saxo/en-gb/content/articles/options/front-end-reprices-long-end-holds---options-brief---15-october-2026-15102026

### Standing watch item — IRS Notice 2026-62, no new development
- No new guidance, designation, or reporting since prior runs. Comments remain due **Oct 28** (docket IRS-2026-1255). This is a tax-character challenge to the box-spread ETF wrapper, **not** a challenge to box pricing or parity [INFERENCE, unchanged]. Sources re-checked: https://summitward.com/learn/boxx-irs-notice-2026-62 ; https://wealthstrategiesjournal.com/2026/09/29/daily-update-sept-29-irs-treats-%c2%a7-351-etf-conversions-as-taxable-flags-exchange-funds-and-tax-aware-strategies/

**Desk line:** Parity is clean (SPY Oct-23 box: −$0.80 executable gross, no arbitrage); no new methodology doc or parity-violation analysis; Cboe's new BOX20X26 box-rate index noted; IRS Notice 2026-62 comments due Oct 28 unchanged.

---

## 7. Bonds & Rates desk

**Module output — SUCCEEDED.** Ran `rates_desk.rates_environment()` from `~/workspace/github/hedge-desk` (exit 0). Mode: `REAL_FRED_RATES`, source `fred-public-csv-http-200`, schema `hedge-desk-rates-desk-1.0.0`. `trade_authorized: false`.

| Field | Value |
|---|---|
| as_of | 2026-10-17 |
| Fed funds effective rate (DFF) | **3.88%**, latest date 2026-10-15 |
| Fed funds change over window | **+0.25 pp** (60-day window) |
| Treasury 2Y (DGS2) | **4.77%**, 2026-10-15 |
| Treasury 10Y (DGS10) | **5.10%**, 2026-10-15 |
| Spread 10Y−2Y | **33.00 bp** |
| Curve slope | 0.041250 (module-computed) |
| Curve shape | **UPWARD_SLOPING** |
| SOFR | **3.89%**, 2026-10-15 |
| EFFR | **3.88%**, 2026-10-15 |
| OBFR | **3.88%**, 2026-10-15 |
| Lookback | 60 days, full daily histories returned for 2Y and 10Y |

**Data-lag note (FACT):** `as_of` is 2026-10-17 but the latest observation in every series is 2026-10-15 — a one-business-day FRED publication lag. Friday 2026-10-16 observations were not yet in the pull. Nothing here is today's (Saturday's) data; Saturday has no new FRED observations.

### The five reported items
1. **Fed funds effective rate: 3.88%** (DFF, 2026-10-15) — FACT. Up 0.25 pp over the module's 60-day window (FACT, module output).
2. **10Y / 2Y levels: 10Y 5.10%, 2Y 4.77%** (both 2026-10-15) — FACT.
3. **2s10s slope: +33 bp, upward-sloping — and FLATTENING over the window** — FACT (arithmetic on module history). At window start (2026-08-18): 10Y 4.71% − 2Y 4.19% = +52 bp. At 2026-10-15: +33 bp. Net flattening of **19 bp** over 60 days, driven by the 2Y rising faster (+58 bp: 4.19% → 4.77%) than the 10Y (+39 bp: 4.71% → 5.10%). Recent direction (past week): the long end is falling faster — 10Y 5.24% (Oct 9) → 5.10% (Oct 15), −14 bp, vs 2Y 4.80% → 4.77%, −3 bp. The 10Y peaked at 5.31% on Oct 5 and has declined 21 bp since.
4. **SOFR vs EFFR spread: +1 bp (3.89% vs 3.88%)** — FACT (arithmetic on module output). Funding-stress read: **no stress signal** — SOFR, EFFR, and OBFR are effectively coincident (all 3.88–3.89%). INFERENCE: overnight funding markets are orderly; nothing here argues for a liquidity-driven premium distortion.
5. **Directional read for premium pricing** — INFERENCE, from the FACTs above:
   - Long rates remain elevated in absolute terms (10Y 5.10%) even after the recent 21 bp pullback from the Oct 5 peak. Higher discount rates continue to pressure growth multiples — the value-lens implication is that duration-heavy, cash-flow-distant names (watchlist: NVDA, TSLA most exposed; MSFT/AAPL less so on cash generation) still face a valuation headwind, not a tailwind.
   - The flattening curve (52 → 33 bp) with the front end pinned near 4.77% while the long end eases is consistent with the market pricing a higher-for-longer front end and modestly less long-run inflation/term pressure — not with a recession-style bull-steepening or an inversion warning. No curve-inversion signal: the curve is still upward-sloping by 33 bp.
   - For premium selling: elevated absolute yields + orderly funding (1 bp SOFR–EFFR) = no rates-driven reason to demand extra premium or to avoid premium collection on rates grounds alone. The recent long-end decline (−21 bp from Oct 5) is a mild easing of the discount-rate headwind, not a regime change.

**Evidence labels:** All levels, dates, spreads, and histories: **FACT** — traced to the module's FRED public-CSV pull (HTTP 200), as-of 2026-10-15 observations. Spread arithmetic (52 → 33 bp, +58/+39 bp moves, −21 bp pullback, +1 bp SOFR–EFFR): **FACT** — deterministic arithmetic on module output. Funding-orderly and multiple-pressure interpretations: **INFERENCE**. No **SPECULATION** and no **UNVERIFIED** items — the module ran clean and no Yahoo fallback was needed or used. No yields were retyped from memory. Yield labeling: ^TNX = 10Y, ^FVX = 5Y (never 2Y); 13W is the front-end anchor, not 2Y.

**What would change the read:** A fresh FRED observation set (Monday's pull, covering Fri Oct 16) showing the 10Y resuming its climb above 5.31% or the 2Y breaking above ~4.90% would re-establish the steepening discount-rate headwind. 2s10s compressing toward zero or inverting would flip the read to a slowdown/recession warning with very different premium-pricing implications (vol expansion risk, not just discount-rate pressure). SOFR–EFFR widening beyond ~5–10 bp would signal funding stress and would argue for wider risk margins on any premium exposure. An FOMC action or a sharp move in the front end would supersede the current "front end pinned, long end easing" characterization.

---

## Desk status

All seven desks delivered. No desk FAILED. No desk silently dropped.
- Earnings: complete. Dividend: complete. Premium: complete (IV inputs FRESH, 26h guard). Quant Lab: complete (19 candidates → ledger #85–103). Futures: complete. Box/Parity: complete. Bonds & Rates: complete (FRED module succeeded).

## Standing rules applied this run
- Yahoo UA header on Yahoo calls; Nasdaq second.
- ^TNX = 10Y, ^FVX = 5Y (never 2Y); 13W front-end anchor.
- No federal-shutdown / data-blackout framing; CR through Dec 11; EIA + WASDE on schedule. Brief-correction-2026-10-05 NOT applied.
- Stale-jump screen: WINDOW-CONTINGENT flags where single-day variance share >30%.
- IV-inputs 26h freshness guard: file FRESH (as_of 2026-10-16T13:54 PT), IV levels supplemented with labeled live pull; 0-DTE atm_iv values NOT quoted as current IV.
- Dividend consecutive-increase counts per ~/workspace/hedge-desk-research/dividend-count-standard.md; MSFT 24 per standard.
- No Risk of Ruin generated or estimated. No trade authorization proposed. No licensed material reproduced.
