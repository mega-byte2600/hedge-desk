# Hedge-Desk Daily Research — Tue 2026-11-10

**Run:** 13:30 PT, Tue 2026-11-10 (21:30 UTC). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** 7 parallel desks (earnings, dividend, premium IV, quant lab, futures events, parity, bonds & rates).
**Standing rules applied:** Yahoo first / Nasdaq second; Yahoo v7 options+quote need cookie+crumb handshake (worked first try on all desks today); ^TNX = 10Y, ^FVX = 5Y (never 2Y); no federal-shutdown framing — CR funds through Dec 11, EIA/WASDE on schedule; MSFT dividend count per `dividend-count-standard.md` (24, incl. Sep 2026 raise); every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.

---

## Decision-relevant items (synthesis)

1. **NVDA Nov 17 after close is the only watchlist earnings in the window — and the market is charging a top-of-range premium for it.** Options price a ~10.4% move (Nov 18 straddle $17.52 on $168.89 spot) vs a ~4.0% average absolute move over the last 8 prints. The stock fell 5.5% today alone and sits ~30% below its Oct 6 high. Direction is not inferable from the beat alone (last 8 prints: 5 down, 3 up). Premium into a binary event = avoid per standing rule. (FACT — company notice Oct 28; live Yahoo chain Nov 10 ~13:45 PT.)
2. **No clean IV-vs-realized verdict is issuable for any watchlist name today.** All six 20-day realized windows remain WINDOW-CONTINGENT — the Nov 5 crash day drives 43–54% of each window's variance (file screen: SPY 62.6%, QQQ 50.4%, AAPL 55.8%, MSFT 45.8%, NVDA 49.3%, TSLA 51.3%). The Nov 9 IV-inputs file is FRESH (as_of 2026-11-09T14:54:31-07:00, ~22.6h old, inside the 26h guard) but its IV levels are all null — the 13:54 PT pull landed after the Monday weekly expiry died, so the guard failed closed correctly. Live labeled pull: SPY 11.35%, QQQ 19.79%, AAPL 18.76%, MSFT 25.68%, NVDA 57.32%, TSLA 33.86% (1 DTE); term structure upward-sloping everywhere to 3 DTE; no front-end inversion. IV rank is UNVERIFIED (no free IV-history source).
3. **Oil's war premium is unwinding into a live contradiction.** Brent broke below $90 (−22% from the Oct 30 high of $118) on Trump de-escalation and OPEC output recovery (+1.38 mb/d in Oct), yet Hormuz traffic runs at ~8% of normal and Middle East exports are down ≥60%; the curve is still backwardated but spreads narrowed ~30% last week. An IRGC claim of two tankers catching fire in the strait today is UNVERIFIED (single-source state media, no independent confirmation). Highest-conviction watch item.
4. **November WASDE landed today, bullish grains** (corn yield 179.6 bpa / stocks 1.758 bb; soy stocks 300 mb — both below consensus; corn +12¢, soy +36¢ post-report). EIA Nov STEO also today: Brent ~$100/bbl through end-2026 then $77 avg Q4 2027 (forecast finalized Nov 5 — already stale on price); 2027 diesel $5.03/gal, +12% vs October forecast. Distillates are the structural story: 99.3 Mbbl, 13% below the 5-yr avg, lowest since May 2003. Next catalysts: API tonight, OPEC Wed Nov 11, EIA weekly Thu Nov 12 (noon ET, a day late for Veterans Day).
5. **Rates are a mild headwind, not a stress event.** EFFR 3.88%, 10Y 4.88%, 2Y 4.56%, 2s10s +32 bp (flattened from +35 bp on Nov 6), SOFR–EFFR 0 bp (FRED via the repo's rates module, observations dated 2026-11-09, mode REAL_FRED_RATES). Elevated long rates keep pressure on growth multiples; funding is calm.
6. **Dividend calendar is quiet but concrete:** AAPL ex-div Thu Nov 12 ($0.27, unchanged); MSFT ex-div Thu Nov 19 at the new $0.98 rate (24th consecutive annual increase). NVDA's December declaration (~Nov 19–20 on the 2025 pattern) is the re-check item.

**Cross-desk note:** The Futures desk flagged an October CPI release this morning (7:30 CT) via Pro Farmer, as potentially sealing a December rate hike — **UNVERIFIED**: neither desk independently confirmed the print, and the Rates desk's module output contains no CPI figure. Do not treat as fact until verified.

---

## 1. Earnings Event desk

**In-window (next 2 weeks, Nov 10–24): one name.**

| Ticker | Report date | Timing | Quarter | Consensus EPS | Guide to watch |
|---|---|---|---|---|---|
| NVDA | Tue Nov 17, 2026 | After close; call 5:00 p.m. ET / 2:00 p.m. PT | Q3 FY2027 (ended Oct 25, 2026) | $2.49 (Nasdaq, 13 ests) | Revenue $108.0B ±2%; Q4 guide; China / Data Center commentary |

- **Date/timing — FACT.** NVIDIA's own Oct 28, 2026 press release sets the call Tue Nov 17, 2 p.m. PT / 5 p.m. ET; CFO written commentary posted ahead of the call. Corroborated by Nasdaq earnings calendar ("time-after-hours") and Yahoo quote data (`earningsTimestamp` Nov 17 21:00 UTC, `isEarningsDateEstimate: false`). Some aggregators still list Nov 18 — wrong; the company notice governs. Sources: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx ; https://www.globenewswire.com/news-release/2026/10/28/3390809/0/en/nvidia-sets-conference-call-for-third-quarter-financial-results.html ; Nasdaq API `api.nasdaq.com/api/calendar/earnings?date=2026-11-17`.
- **Expectations — FACT (company guide) / INFERENCE (consensus).** Q2 release (Aug 26, 2026) guided Q3 revenue $108.0B ±2%, GAAP and non-GAAP gross margin 74.0% ±50 bps, no Data Center compute revenue from China assumed. Nasdaq consensus EPS $2.49 (13 estimates; last year's Q3 EPS $1.24). Revenue consensus per aggregators ~$108.8–109.2B — secondary-source figure, approximate.
- **Options-implied expected move — FACT (desk-computed from live Yahoo chain, Nov 10 ~13:45 PT, cookie+crumb auth).** Spot $168.89 (Nov 10 close). First expiry after the print, Wed Nov 18 weekly: ATM 170 straddle mid = call $8.35 + put $9.18 = $17.52 → **10.4% of spot**. Fri Nov 20 expiry 170 straddle = $18.48 → 10.9%. ATM IV ~82–84% on the Nov 18 chain. Cross-check: Options Whale (Medium, Nov 8) cites 9.3% — same ballpark, weaker source; the desk's own computation supersedes it.
- **Historical earnings-day moves — FACT (desk-computed from Yahoo v8 daily closes, report-day close → next-session close; matches the independently published Jorgai 67-report series to ±0.1 pp on all 8).**

| Report date | Next-session move |
|---|---|
| Aug 26, 2026 | +8.74% |
| May 20, 2026 | −1.77% |
| Feb 25, 2026 | −5.46% |
| Nov 19, 2025 | −3.15% |
| Aug 27, 2025 | −0.79% |
| May 28, 2025 | +3.25% |
| Feb 26, 2025 | −8.48% |
| Nov 20, 2024 | +0.53% |

  Summary (n=8): mean absolute move **4.0%**, median absolute 3.2%, 3 up / 5 down, mean signed −0.9%. The market prices ~10.4% — at the top of the recent range; only Aug 2026 (+8.7%) and Feb 2025 (−8.5%) came close. **INFERENCE:** the priced move embeds both the binary-event premium and the current tape (stock −5.5% on Nov 10 alone, ~30% below its Oct 6 closing high of $239.24 per Motley Fool; 52-week range $164.27–$243.37 per Yahoo). **What would change it:** the Nov 17 print itself; revenue vs the $108B guide and the Q4 guide matter more than EPS.
- **Release teardown:** not applicable — no Q3 release exists yet (published Nov 17 after close). The Aug 26, 2026 Q2 release is the source of the $108.0B guide above.

**No earnings in window — by name (FACT):** AAPL reported Q4 FY2026 Mon Nov 2, 2026 after close; MSFT reported Q1 FY2027 Wed Oct 28, 2026 after close; TSLA reported Q3 2026 Wed Oct 21, 2026 after close. Next reports for all three are estimated late Jan 2027 (aggregator estimates, not company-confirmed). SPY / QQQ are ETFs — no earnings. Source: SimianX Mag-7 tracker (updated Nov 3, 2026), cross-checked against Nasdaq calendar pulls for Nov 10–24, which returned no watchlist rows on any date. https://www.simianx.ai/stories/magnificent-7-earnings-dates-results-tracker

**Source notes:** Nasdaq earnings calendar API — transient parsing issue on the desk's side (read `data.calendar`, actual key `data.rows`), recovered; company IR + Yahoo had already confirmed the date. Yahoo v7 options worked with the cookie+crumb handshake, no 401s. SEC EDGAR not needed (no release exists in-window).

---

## 2. Dividend Opportunity desk

**Window:** Nov 10 – Dec 8, 2026 (next 4 weeks).

**Ex-dividend dates IN the window (2 names):**

| Symbol | Ex-date | Amount | Record | Payable | Declared | Note |
|---|---|---|---|---|---|---|
| AAPL | Thu Nov 12, 2026 | $0.27/qtr | Nov 12 | Nov 16 | Nov 2, 2026 | Unchanged vs May & Aug 2026 — no increase this cycle |
| MSFT | Thu Nov 19, 2026 | $0.98/qtr | Nov 19 | Dec 10 | Sep 15, 2026 | New rate — the Sep 2026 raise; first payment at $0.98 |

**No ex-date in the window (4 names, stated explicitly):**
- **SPY** — no ex-date in window. Dec quarterly distribution not yet declared (Yahoo `dividendDate` null as of today). Historical pattern is the third Friday of December (Dec 18, 2026), which falls outside the window — INFERENCE, not a declared date. Nasdaq calendars for Dec 3, 4, 8 show no SPY.
- **QQQ** — no ex-date in window. Last ex-date Sep 21, 2026 ($0.75143, paid Oct 8). Dec distribution historically ~Dec 22 — outside the window (INFERENCE). Nasdaq calendar Dec 18/21 shows no QQQ.
- **NVDA** — no ex-date in window, none yet declared. Last ex-date Sep 10, 2026 ($0.25, paid Oct 1). **Watch item:** in 2025 NVDA declared Nov 19 with ex-date Dec 4 — if that pattern repeats, a Dec 3–4 ex-date would fall inside this window, but as of today nothing is announced. Nasdaq calendars Dec 3/4 show no NVDA. Status: UNVERIFIED / pending declaration.
- **TSLA** — pays no dividend (Nasdaq returns N/A, no dividend rows). Nothing to track.

**Increases / cuts / specials — FACT:** No cuts and no specials announced for any watchlist name in this window (Nasdaq dividend rows + calendars checked).
- **MSFT increase — already announced, now going ex:** Sep 15, 2026 board raise $0.91 → $0.98/qtr (+7.7%). Per the dividend-count standard, MSFT stands at **24 consecutive annual increases (incl. the Sep 15, 2026 raise to $0.98/qtr; initiated 2003)** as of this package date. A 2026 raise HAS been announced, so no "no raise this year" flag applies. Next raise would typically come Sep 2027.
- **AAPL:** last raise May 2026 ($0.26 → $0.27, declared Apr 30, 2026), so a 2026 increase has occurred; the Nov 12 dividend holds the $0.27 rate. AAPL's total consecutive-year count is UNVERIFIED in this run (not computed from issuer history; only MSFT is anchored in the standard) — no screener number carried.
- **NVDA — standing rate changed in 2026, not upcoming:** Nasdaq shows $0.01/qtr (Dec 2025, Mar 2026) → $0.25/qtr from Jun 4, 2026 (declared May 20, 2026), repeated Sep 10, 2026. Yahoo corroborates: `dividendRate` $1.00/yr (= $0.25 × 4), yield 0.56%. No further change announced.
- **SPY / QQQ:** variable quarterly ETF distributions; no increase/cut framing applies.

**Value-lens read (INFERENCE):** The only decision-relevant dividend event in the window is the MSFT Nov 19 ex-date at the new $0.98 rate — a confirmed, issuer-declared raise going ex, not a rumor. AAPL Nov 12 is a routine hold at $0.27. Nothing in this desk's window changes a margin-of-safety case for any name; the NVDA December declaration (expected ~Nov 19–20 on the 2025 pattern) is the one item to re-check next week. **What would change this:** an NVDA declaration landing an ex-date inside the window, or a SPY/QQQ December distribution declared earlier than the usual mid/late-December pattern.

**Sources:** Nasdaq per-symbol dividends API (`api.nasdaq.com/api/quote/{SYM}/dividends?assetclass=stocks|etf`); Nasdaq dividends calendar API (`api.nasdaq.com/api/calendar/dividends?date=...`) checked Nov 10, Nov 12, Nov 19, Dec 3, Dec 4, Dec 8, Dec 18, Dec 21; Yahoo v7 quote (cookie+crumb, 200) — AAPL `dividendDate` 1794787200 = Mon Nov 16, 2026 (payment date, corroborates Nasdaq); NVDA `dividendDate` = Oct 1, 2026 (last payment, no forward date); SPY `dividendDate` null. Count definition: `~/workspace/hedge-desk-research/dividend-count-standard.md`.

**Source failures (classified):** Yahoo v8 chart `events=div` returned no dividend events for any symbol (events key absent) — endpoint quirk, not data absence; fell back to Nasdaq + v7 quote. Yahoo v7 quote first attempt used wrong path format (`/quote/AAPL` → 404); retried with `?symbols=` → 200. Nasdaq SPY ETF dividends endpoint returned N/A headers — dead end for SPY history via that route; handled via calendar checks + declared-date absence, labeled INFERENCE where pattern-based.

---

## 3. Overnight Premium desk (IV)

### IV-inputs file — freshness guard verdict: FRESH, but IV levels ALL NULL
- **File:** `~/workspace/hedge-desk-research/nightly/2026-11-09-iv-inputs.json` — FACT, read from disk 13:27 PT.
- **`as_of`: 2026-11-09T14:54:31-07:00** (actual pull 21:55 UTC Nov 9 = 13:55 PST; the `-07:00` offset is the script's hardcoded PDT — cosmetic only). Age at run start ≈ **22h 36m → inside the 26h guard → FRESH**.
- **But every `atm_iv` is null (6/6).** Cause, per the file's own `failures` list: the 13:54 PT Monday pull landed after the Nov 9 (Monday) weekly expiry died at 16:00 ET, so the post-expiry guard failed all six chains closed rather than print solver residuals on dead contracts — FACT, correct fail-closed behavior, not a source outage.

### Stale-jump screen (from that file, realized window 2026-10-12 to 2026-11-06): ALL SIX WINDOW-CONTINGENT
Max single-day variance shares: SPY 62.6%, QQQ 50.4%, AAPL 55.8%, MSFT 45.8%, NVDA 49.3%, TSLA 51.3% (all >30% threshold). The Nov 5 crash day still dominates every 20-day realized window. **Consequence: no clean IV-vs-realized verdict is issuable for any symbol today; all comparisons below are labeled WINDOW-CONTINGENT.**

### Live Yahoo supplement pull — LABELED LIVE, as of 2026-11-10 13:28–13:30 PT
Method: reused `~/workspace/hedge-desk-research/nightly/pull_iv_inputs.py` functions (curl-seeded cookie jar + crumb handshake); read-only script at `/tmp/live_iv_pull.py`, wrote nothing to the nightly dir. Yahoo v7 options + v8 chart both responded; cookie+crumb worked first try. Repo failover module unavailable (same as the nightly file notes) — legacy Yahoo-only path used; CBOE fallback not needed since Yahoo worked.

**Standard nearest-expiry print (post-close, ~13:29 PT):**

| Symbol | ATM IV | Expiry | DTE | Realized 20d (window 10-13→11-09) | Max-day share | Window |
|---|---|---|---|---|---|---|
| SPY | null | — | — | 22.87% | 53.6% | CONTINGENT |
| QQQ | null | — | — | 36.85% | 44.4% | CONTINGENT |
| AAPL | 18.76% | 2026-11-11 | 1 | 27.31% | 49.8% | CONTINGENT |
| MSFT | 25.68% | 2026-11-11 | 1 | 37.12% | 42.5% | CONTINGENT |
| NVDA | 57.32% | 2026-11-11 | 1 | 49.90% | 45.0% | CONTINGENT |
| TSLA | 33.86% | 2026-11-11 | 1 | 62.81% | 46.1% | CONTINGENT |

- **SPY/QQQ null — structural, not transient.** Their nearest expiry was **today, 2026-11-10** (daily SPY/QQQ weeklies), already dead at 16:00 ET when the post-close pull ran; guard failed closed. Same daily structural failure seen Oct 20–Nov 6: every weekday-afternoon pull trips it for SPY/QQQ. The proposed pull-switch rollover remains inert (user decision pending since 2026-10-22). Single names' nearest expiry is Wed 2026-11-11, so they printed normally.

**MANUAL ROLLOVER fallback for SPY/QQQ — LABELED FALLBACK, not a standard print.** Re-fetched the nearest **unexpired** expiry via Yahoo `?date=` (same cookie+crumb), as of ~13:30 PT:
- **SPY: ATM IV 11.35%, expiry 2026-11-11, 1 DTE** — manual rollover, labeled.
- **QQQ: ATM IV 19.79%, expiry 2026-11-11, 1 DTE** — manual rollover, labeled.
- Degenerate-quote check passed on both (non-zero bid/ask, sane IVs). Post-close marks; treat as indicative close-of-day levels, not live intraday prints.

**Term structure — second tenor, Fri 2026-11-13 (3 DTE), same live pull:**

| Symbol | 1 DTE IV | 3 DTE IV | Slope |
|---|---|---|---|
| SPY | 11.35% | 14.89% | +3.5 pp, upward |
| QQQ | 19.79% | 25.74% | +5.9 pp, upward |
| AAPL | 18.76% | 24.10% | +5.3 pp, upward |
| MSFT | 25.68% | 30.09% | +4.4 pp, upward |
| NVDA | 57.32% | 63.11% | +5.8 pp, upward |
| TSLA | 33.86% | 43.34% | +9.5 pp, upward |

**INFERENCE:** Front-end term structure is upward-sloping (contango) across all six names — no inversion, no front-tenor panic bid. TSLA's slope is steepest (+9.5 pp).

### IV-vs-realized — WINDOW-CONTINGENT only (no clean verdicts)
Raw comparisons, each **WINDOW-CONTINGENT** (Nov 5 crash day drives 43–54% of each 20-day realized variance; plus a tenor mismatch — 1-DTE IV vs 20-day realized):
- SPY 1-DTE IV 11.35% vs realized 22.87% — IV below realized.
- QQQ 19.79% vs 36.85% — IV below realized.
- AAPL 18.76% vs 27.31% — IV below realized.
- MSFT 25.68% vs 37.12% — IV below realized.
- NVDA 57.32% vs 49.90% — IV **above** realized (only name where front IV exceeds the crash-inflated realized).
- TSLA 33.86% vs 62.81% — IV well below realized.
- **What would change these:** the Nov 5 jump aging out of the 20-day window (after ~Dec 3), or a fresh realized print that re-weights the window. Until then, do not trade on any "IV cheap vs realized" read — the realized leg is a crash artifact.

### IV rank — UNVERIFIED
No free IV-history source available to this desk, so **IV rank cannot be computed for any symbol — UNVERIFIED, not guessed.** No "elevated IV" flag can be issued on rank. Level-based observation only: NVDA front IV (57–63%) is by far the highest on the watchlist in absolute terms; SPY 1-DTE IV (11.35%) is the lowest.

### Earnings inside the window — NVDA only
- **NVDA next earnings 2026-11-17 — FACT** (Nasdaq calendar sweep, re-confirmed by today's live sweep 13:28 PT; also in the Nov 9 file). No other watchlist name has earnings in the 45-day sweep window.
- **INFERENCE:** The Nov 11 and Nov 13 expiries do **not** span Nov 17, so current front-tenor NVDA IV (57–63%) is **not** earnings-loaded. Premium into the NVDA binary would sit in the Nov 20 expiry — its IV level was not pulled; **UNVERIFIED**. Standard desk rule applies: premium into a binary event = avoid; the earnings-loaded tenor needs its own pull before any read.

### Parity / sanity checks
- **FACT:** ATM IVs are call/put means at the same strike and expiry (straddle construction) — no put-call parity violation observed in any chain pulled. (This construction does not deeply test parity; no box/parity anomaly was detected — nothing to report.)
- **INFERENCE:** IV levels are internally plausible (QQQ/SPY ratio ~1.7× at 1 DTE, consistent with QQQ's higher realized vol; NVDA > TSLA > MSFT > AAPL ordering matches realized-vol ordering except NVDA/MSFT swap at 1 DTE, within normal tenor noise).

### Source-failure classification
- Yahoo v7 options / v8 chart: **working** (cookie+crumb first try, all six symbols returned chains).
- SPY/QQQ nearest-expiry nulls: **dead end by design** (post-expiry guard, structural/daily) — recovered via labeled manual rollover to Nov 11, not by retrying the dead expiry.
- Nasdaq earnings sweep: **working** (live, 13:28 PT).
- Repo failover module (`hedge_desk.data.options_failover`): **unavailable** in this clone checkout — Yahoo-only path used; CBOE fallback not exercised. No impact today since Yahoo worked.
- IV history for rank: **genuine dead end** (no free source) → UNVERIFIED.

---

## 4. Open Quant/AI Model Lab

**Sweep complete. No TEST, no INTEGRATE this run.**

**Sweep coverage (FACT):** arXiv q-fin.* submitted Nov 7–9, 2026 returned 15 papers (13 weekend + 2 on Nov 9); a no-filter control query confirms the newest q-fin paper is arXiv:2611.12389 (submitted Nov 9) — no Nov 10 submissions announced yet at run time. GitHub leg skipped per the run brief (no GitHub operations of any kind), same as Nov 1–9. All 8 new candidates were scored with the repo's own scorer (`hedge_desk.research_intelligence.assess_source`, run, not hand-computed). All claim details below are source-reported from abstracts only (full papers not read) and are labeled UNVERIFIED per the evidence standard; no author code link exists for any of the 8 in the arXiv API record, so reproducibility is not established for any of them.

**New candidates (ledger #246–253, all appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md`):**

| # | Candidate | Score | Disposition |
|---|---|---|---|
| 246 | Chen/Cheng/Hull et al — "Risk-Sensitive RL for an Options Market Maker: Empirical Study with Real S&P 500 Options" (arXiv:2611.10956v1, 7 Nov) | 62 | **WATCH** |
| 247 | Augustyniak/Badescu/Zhang — "Polynomial-Preserving Processes and Volatility Modelling in Discrete Time" (arXiv:2611.10928v1, 7 Nov) | 56 | **WATCH** |
| 248 | Garcin/Pu/Verrier — "Optimal execution in a fractional setting with RL" (arXiv:2611.11373v1, 8 Nov) | 42 | ARCHIVE |
| 249 | Fujiwara/Sato/Kanazawa — "Is price-impact decay statistically identifiable by propagator estimation?" (arXiv:2611.10574v1, 7 Nov) | 42 | ARCHIVE |
| 250 | Chan/Chu — "Objective Diversification of Dynamic Hedging" (arXiv:2611.10333v1, 7 Nov) | 48 | **WATCH** |
| 251 | Escudero et al — "Adjoint Kernel Sensitivity of the Rough Heston Characteristic Exponent" (arXiv:2611.11652v1, 8 Nov) | 36 | ARCHIVE |
| 252 | Li — "Diversification Across Predictors: Heterogeneous Ensemble Learning for Cross-Sectional Return Prediction" (arXiv:2611.12389v1, 9 Nov) | 45 | **WATCH** |
| 253 | Liu/Liu/Shen — "Diversified-Risk-Perception Risk Measures and Portfolio Selection" (arXiv:2611.11803v1, 9 Nov) | 33 | ARCHIVE |

**Most decision-relevant — #246 (run's highest score, 3 points under TEST):** a distributional TD3 hedging agent trained on an empirical replay of S&P 500 options 1996–2017 and evaluated OOS 2018–2023 vs delta hedging, hedge-ratio rules, and GBM/SABR/hybrid simulators. Source-reported claims (UNVERIFIED): CVaR tail loss −3.1% vs delta hedging, −8.9% in volatile/falling markets, but reverses to a 7–10% cost in rising markets; empirical training induces a state-dependent short net delta (under-hedges negative-delta books after falls); the tilt disappears under GBM training. Authors' own caveat: evidence rests on a single test path and the edge is regime-conditional. Premium-desk lesson: a hedging agent trained only in simulation misses crash/vol regimes — treat any desk RL-hedging claim trained only in simulation as UNVERIFIED on real data. Follow-up: re-check for a code release.

**Other WATCH notes:** #247 — S&P 500 returns + large options panel 1996–2023, mean weekly IV RMSE down ~8–41% vs nested benchmarks (UNVERIFIED); sandbox the IV fit on a SPY chain if code lands. #250 — five objective-specific hedge-ratio estimators combined under a fixed evaluation objective; adaptive weighting improved loss in all 16 objective–window comparisons, equal weighting alone already improved downside/quantile hedging (UNVERIFIED); the ensemble-of-objectives pattern is the hedging-lane note. #252 — heterogeneous predictor ensemble, Rank IC +13% over standalone NNs on CSI300 Alpha158 (UNVERIFIED); China data only, method transfers, data doesn't; WATCH at the band floor (45).

**ARCHIVE reasons (band discipline, not lack of interest):** #248 fractional-execution RL (no numbers in abstract, no desk procedure); #249 propagator no-go theorem — but note the caution it carries: any propagator-based impact-decay claim the desk meets is UNVERIFIED as evidence of decay, since the fine-tuned decay is a property of the Wiener–Hopf deconvolution; #251 rough-Heston kernel sensitivity (pure theory, no empirical evaluation); #253 DRP risk measures (risk-capital measurement, not a desk lane — desk never touches the risk engine).

**Re-checks (arXiv API only, no GitHub):** #238 (Vidovich/Zerjal end-of-day reversal), #239 (Tran/Yu microstructure invariance), #241 (Wang/Rachev/Fabozzi factor portfolios) — all still v1, no code link; all stay WATCH. Notes added to their ledger rows.

**Triage exclusions (no ledger rows):** 2611.11436 Pumpfun meme coins (crypto scope), 2611.10972 JUBILEE debt collections, 2611.10926 DeepFinance deal diligence, 2611.10801 quantum-layer equity ranking, 2611.10607 MILP contagion clearing, 2611.10531 comonotonic lognormal approximations (pure theory).

**Ledger confirmation:** 8 new rows #246–253 appended and verified on disk (lines 337–344 of `~/workspace/hedge-desk-research/quant-lab-ledger.md`); re-check notes added to #238/#239/#241; run note added to the Jidoka log. No scorer or source failures — the arXiv API legs all returned cleanly (one initial curl failure was a malformed URL, exit 3, recovered via URL-encoded Python request; not a source failure). Nothing new reached TEST or INTEGRATE.

---

## 5. Weather/War/Logistics Futures Event desk

**Headline: a two-report day — November WASDE + EIA STEO both landed today; oil's war premium is unwinding fast while nat gas squeezes higher.**

### 5.1 USDA November WASDE — RELEASED TODAY, 12:00 ET (11:00 CT)
**FACT** — USDA released the November Crop Production + WASDE reports today, Nov 10, on schedule (USDA release calendar: Nov 10, 12:00 ET; next Dec 10). Sources: https://www.usda.gov/oce/commodity/wasde ; https://esmis.nal.usda.gov/publication/world-agricultural-supply-and-demand-estimates

| Item (2026-27) | Nov | Oct | Avg estimate | Verdict vs expectations |
|---|---|---|---|---|
| Corn yield (bpa) | 179.6 | 181.2 | 180.5 | Below est. — bullish |
| Corn production (bb) | 15.893 | 16.034 | 15.944 | Below est. |
| Corn ending stocks (bb) | 1.758 | 1.849 | 1.826 | Below est. — bullish |
| Soybean yield (bpa) | 53.3 | 53.1 | 53.6 | Above Oct, below est. |
| Soybean production (bb) | 4.574 | 4.562 | 4.601 | Below est. |
| Soybean ending stocks (mb) | 300 | 315 | 336 | Well below est. — bullish |
| Wheat ending stocks (mb) | 743 | 740 | 747 | ~In line |
| Corn farmgate price | $4.60/bu | $4.70 | — | −$0.10 |
| Soybean farmgate price | $12.10/bu | $12.00 | — | +$0.10 |

**FACT** — Market reaction post-report: corn +12¢, soybeans +36¢, wheat +6¢ (was corn +1¢, soy flat, wheat +2¢ pre-report). Source: https://ocj.com/2026/11/november-wasde-bullish-corn-and-soybeans/ (published 2026-11-10 12:33 ET). Full numbers: https://www.dtnpf.com/agriculture/web/ag/news/article/2026/11/10/usda-releases-november-crop-wasde
**FACT** — Soybean ending stocks landed at the low end of the pre-report estimate range (280–404 mb, widest in recent history per Pro Farmer, Nov 6) — the binary risk flagged pre-report resolved bullish. Global: corn ending stocks 281.94 mmt; soy 123.5 mmt; wheat 280.82 mmt (up from 276.04). Brazil soy unchanged at 186 mmt.
**FACT** — Livestock (DTN analyst): beef production 2026 cut 40m lbs, Q4 steer price $220 (Q1–Q3 2027 unchanged $235/$235/$240); pork production +35m lbs, hog prices cut $2 in Q4 2026–Q2 2027 — bearish pork.
**INFERENCE** — The grain complex read is modestly bullish into year-end: both corn and soy stocks came in below consensus, and Dec corn had just hit a four-month low ($4.3875) earlier today before the report. **What would change it:** South American weather/production revisions (Brazil 186 mmt soy is the swing factor) and the Dec 10 WASDE.

### 5.2 EIA November Short-Term Energy Outlook — RELEASED TODAY ~12:00 ET
**FACT** — EIA released the November STEO today, Nov 10; forecast inputs finalized Nov 5 — it does **not** reflect market events after Nov 5 (including Monday's 5.9% Brent slide). Sources: https://www.eia.gov/about/new/?r=5160/1000 ; https://www.gain.consulting/post/eia-raises-its-2027-diesel-forecast-to-5-03-a-gallon
- Brent spot expected near **$100/bbl through end-2026**, then gradually falling to **$77/bbl avg in Q4 2027** as inventories rebuild; assumes most Middle East production ex-Iran returns to pre-conflict averages by mid-2027.
- 2026 avg: WTI **$88.29** (was $88.21), Brent **$97.44** (was $96.32). 2027 avg: WTI $80.54, Brent $85.78.
- U.S. retail diesel 2027 avg **$5.03/gal, +12% vs the October forecast** — a logistics cost headwind, not a tailwind.
- U.S. power demand records: 4,306 BkWh in 2026, 4,370 BkWh in 2027 (from 4,216 in 2025), driven by AI data centers + electrification; nat gas share of generation 40% in 2026, 39% in 2027. Source: https://www.reuters.com/business/energy/us-power-demand-beat-record-highs-2026-2027-ai-use-surges-eia-says-2026-11-10/
- U.S. dry gas production forecast raised to **113.0 Bcf/d (2026)** and **117.6 Bcf/d (2027)** — record highs.
**INFERENCE** — EIA's own forecast is already stale on price (Brent printed ~$90 today vs ~$100 assumed) but its diesel and power-demand numbers are the durable signals. **What would change it:** December STEO (Dec 8–12 window) incorporating the post-Nov 5 price collapse.

### 5.3 Oil — war premium unwinding; curve still backwardated but flattening
**FACT** — Brent fell below $90/bbl today for the first time since Aug 31: −3.15% to **$89.65** at 13:34 GMT; WTI −2.68% to **$84.52**. Monday: Brent −5.85% (settled $92.57), WTI −4.38% ($86.85). Brent is ~22% below its Oct 30 six-month high of $118. Sources: Reuters via https://www.globalbankingandfinance.com/oil-falls-trump-downplays-prospect-escalation-iran/ and https://www.1049thewolf.com/2026/11/09/oil-falls-as-trump-downplays-prospect-of-escalation-with-iran/
**FACT** — Driver: President Trump said Mon Nov 9 he would hold off new strikes on Iran "at this point" after appeals from Gulf states (incl. Qatar's PM); the U.S. naval blockade remains in place. Separately, a Reuters survey (Nov 9) found OPEC output **+1.38 mb/d in October to 22.87 mb/d**, ~90% of its February level, led by Saudi Arabia, Kuwait, Iraq.
**FACT** — Curve (Nov 6 settles): still backwardated but narrowing fast — Brent 1st–6th month spread $10.54 (from $15.21 on Oct 30); WTI 1st–6th $7.54 (from $11.16). Dec 2027 Brent ~$17.73 below front month. Front spreads lost ~30% last week. Sources: https://leprivatebanker.com/2026/11/08/brent-gives-back-a-weeks-spike-but-inventories-and-hormuz-odds-show-a-market-still-tight/ ; https://www.arestradinglab.com/analysis/2026-11-09-weekly-oil/
**INFERENCE** — The market is pricing de-escalation + oversupply, while the curve's remaining backwardation says prompt barrels are still tight — the two are only reconcilable if traders expect the tightness to be temporary. **What would change it:** any renewed strike/blockade escalation or a Hormuz transit incident (see §5.4) would re-widen front spreads first.

### 5.4 Strait of Hormuz — conflicting claims; traffic severely restricted, oil falling anyway
**FACT** — Independent AIS tracker: 2 commercial ships crossed today as of 20:12 UTC (0 tankers); 7-day avg **6.9/day, ~8% of normal** (84.8/day pre-crisis). Status "Restricted / severely restricted" since Oct 19. Source: https://hormuz.now/news
**FACT** — U.S. CENTCOM (via Al Jazeera, Nov 10): strait "open," primary lanes cleared of mines, >900m bbl moved through since early May under U.S. coordination; blockade of Iranian ports active since July 14. Competing Iranian claim: strait closed to "hostile" shipping since Mar 2, transit permits/tolls via PGSA.
**FACT** — Middle East crude exports down **≥60%** as Hormuz stays mostly closed, per shipping data cited by EnergyNow.com (Nov 10). Separately, loaded LNG tankers through Hormuz rose to **31 in October vs 23 in September** (Reuters data) — highest since the conflict began.
**UNVERIFIED (single-source, state media)** — IRGC Navy statement today (PressTV, Nov 10, 10:53 GMT) claims two oil tankers "caught fire" after hitting a mine / incident on an unauthorized southern route, AIS switched off. No independent confirmation found in this sweep; treat as a claim, not a verified incident. Source: https://www.presstv.co.uk/Detail/2026/11/10/780399/irgc-navy-two-violating-oil-tankers-catch-fire-in-strait-of-hormuz
**FACT** — Trump rejected Iran's ceasefire/reopen proposal for the strait (reported Nov 10); war-risk insurance remains 0.85–1.10% of hull value vs 0.05% pre-conflict (Region Alert, refreshed Nov 10 09:00 UTC).
**INFERENCE** — The market is discounting Hormuz risk despite traffic running at ~8% of normal — a striking divergence. Either the U.S.-coordinated corridor is moving enough volume off-AIS, or the market is complacent; the 60% export drop says physical flows are genuinely impaired. **What would change it:** independent confirmation of today's tanker incident, or a further leg down in AIS transits, would likely re-price the premium quickly. This is the desk's highest-conviction watch item.

### 5.5 Natural gas — short-covering rally on cold forecasts + record LNG
**FACT** — Dec NYMEX nat gas **+7.3% Monday to $3.218/MMBtu** (four-week high), ~$3.24–3.29 midday Tue. Drivers per ING/Pro Farmer: colder eastern-U.S. forecasts lifting heating demand + short covering + record LNG feedgas. Sources: https://www.profarmer.com/news/first-thing-today/first-thing-today-grain-firm-overnight-all-eyes-usdas-production-and-wasde-reports ; https://naturalgasintel.com/news/natural-gas-extending-gains-as-forecasters-tease-cooldown/
**FACT** — LNG flows to nine major U.S. terminals averaged a **record 19.3 Bcf/d** so far in November; Lower-48 production 112.1 Bcf/d, down from October. Storage **2.1% above the 5-yr average** (w/e Nov 6); prior EIA storage build +77 Bcf (w/e Oct 30).
**FACT** — Positioning fuel: CFTC funds net short ~**259,000 contracts (0.2 percentile historically)**; gross shorts ~540,000, the highest in years; price is up >10% since that positioning snapshot (Dec ~$2.90). Source: https://www.xtb.com/cy/market-analysis/news-and-research/chart-of-the-day-natgas-are-we-in-for-a-weather-driven-short-squeeze
**INFERENCE** — This is a positioning-driven rally against a still-loose storage fundamental — it holds only if cold verifies. **What would change it:** Thursday's EIA storage report (10:30 ET) confirming another surplus build, or moderating late-November forecasts, would likely unwind it toward $3.00.

### 5.6 EIA weekly petroleum — last print + next print
**FACT** — Last report (w/e Oct 30, released Nov 4): commercial crude **−0.9 Mbbl to 409.8 Mbbl** (5th straight draw, 4% below 5-yr avg, vs Reuters poll expecting +0.88 Mbbl build); gasoline −0.2 to 209.0; **distillate −3.6 to 99.3 Mbbl, 13% below 5-yr avg, lowest since May 2003**; refinery utilization 94.5%; SPR 282.2 Mbbl. Source: https://www.morningstar.com/news/dow-jones/2026110410540/us-crude-oil-stockpiles-post-fifth-straight-weekly-drop
**FACT** — Next EIA Weekly Petroleum Status Report is **Thu Nov 12, 12:00 ET** (a day late for Veterans Day). API industry survey due this afternoon (Tue). OPEC monthly report Wed Nov 11; IEA monthly report Fri Nov 13. Source: https://leprivatebanker.com/2026/11/08/brent-gives-back-a-weeks-spike-but-inventories-and-hormuz-odds-show-a-market-still-tight/
**INFERENCE** — Distillate tightness is the structural story under the oil-price noise: 13% below average into winter, with EIA raising 2027 diesel +12%. **What would change it:** Thursday's print — a distillate build would soften the tightness thesis.

### 5.7 Watchlist relevance (SPY / QQQ / AAPL / MSFT / NVDA / TSLA)
- **FACT** — No watchlist name has a direct futures-catalyst link today; the desk's read is macro: falling oil eases input/transport cost pressure (mild positive for margins broadly), while the +12% 2027 diesel forecast and tight distillates cut the other way for logistics-heavy operations.
- **INFERENCE** — The AI-power-demand signal in today's STEO (record U.S. electricity demand 2026–27 on data centers) is the most watchlist-relevant item: it corroborates the demand backdrop for NVDA/MSFT capex, but it is an EIA forecast, not a company disclosure — treat as context, not a name-level signal.
- **UNVERIFIED** — October CPI was released this morning (7:30 CT) alongside WASDE — noted by Pro Farmer as potentially sealing a December rate hike. The desk did not independently verify the CPI print; Rates desk owns it, and the Rates desk's output contains no CPI figure. Do not treat as fact.

**Source failures / gaps:** None material. All primary sources (USDA, EIA) confirmed on schedule — no shutdown/blackout framing applies. The IRGC tanker-fire claim (§5.4) is the one item the desk could not independently verify; labeled UNVERIFIED rather than reported as fact. No live Yahoo futures quote was pulled (front-month levels above are from Reuters-sourced reporting timed 02:46–13:34 GMT today, not a close); curve-spread figures are Nov 6 settles, the latest published in sources found — labeled as such.

---

## 6. Box/Parity Observer

**Bottom line: one new item worth noting — Cboe's AM-settled weekly SPX options (SPXO) began trading yesterday (Mon Nov 9, 2026). No new parity violation or box-spread finding for SPY/QQQ; quoted put–call parity in SPX remains tightly compressed in price space per the latest published work.**

### 6.1 NEW — Cboe SPXO launch (effective trade date Nov 9, 2026)
- **FACT** (Cboe rollout reported Sep 4, 2026; Cboe SPX product page trade data as of Nov 9, 2026): Cboe Options Exchange (C1) began rolling out AM-settled S&P 500 weekly options, symbol **SPXO**, effective trade date **Nov 9, 2026**, subject to regulatory review. Like monthly AM-settled SPX, SPXO expires at the opening of trading and settles to the SPX opening settlement price (SET). Allocation is **price-time** for SPXO (vs pro-rata for SPX); current SPX risk rules apply; SPXO participates in Global Trading Hours.
  - Sources: https://fxnewsgroup.com/forex-news/exchanges/cboe-options-to-roll-out-sp-500-am-settled-weekly-options/ ; https://certification.cboe.com/tradable-products/sp-500/spx-options/
- **INFERENCE**: Parity/box work on SPX must respect the settlement convention per symbol — an SPXO leg settles AM (opening SET) while SPXW settles PM. A box or conversion mixing SPX/SPXO legs across the same expiry date is not the same settlement and the deterministic payoff identity does not apply across the two. No pricing impact on SPY/QQQ American-style ETF options, which are unaffected.
- Disposition: **WATCH** — note the new expiry grid; no action for the paper desk.

### 6.2 Parity-violation literature — no tradable violation
- **FACT** (Shin, "The Cost of a Free Lunch," arXiv:2604.19604, Aug 24, 2026; companion "The P behind Q," arXiv:2605.12250, May 26, 2026): using minute-level NBBO data on S&P 500 and Russell 2000 options, quoted put–call parity residuals measured against traded futures are **near zero**; however the option-implied discount factor vs the OIS curve leaves a systematic annualized **carry gap (sample median ≈37 bp, >98% positive)** — an implementation wedge in carry space, invisible in price space, attributed to path-dependent enforcement costs (daily settlement, margin, finite capital).
  - Sources: https://arxiv.org/html/2604.19604 ; https://arxiv.org/pdf/2605.12250v5.pdf
- **INFERENCE**: Confirms the desk's standing rule — deterministic parity holds in price space and outranks model output; the wedge is a funding/carry phenomenon, not a capturable box-spread arbitrage after costs. No change to how the desk checks parity.
- Disposition: **WATCH** (already-known recent paper, not new this week; no desk action).

### 6.3 Index methodology — nothing new that touches parity
- **FACT** (S&P DJI growth/value criteria change, reported Oct 28, 2026): revised growth/value classification rules take effect before the open **Dec 21, 2026** (preliminary files from Dec 4) — 12-month momentum removed from growth assessment; free-cash-flow-to-price added to value. Affects S&P style indices, not the headline S&P 500 level or SPX option mechanics.
- **FACT** (S&P DJI, announced Oct 30, 2026): routine constituent change — Okta replaced Kenvue in the S&P 500 before the open **Nov 4, 2026**, following the pending Kimberly-Clark acquisition.
- **FACT**: Nasdaq-100 methodology update went live **May 1, 2026** (quarterly rank-based reviews, fast-entry pathway, float capping) — six months old, no new NDX change in the last few weeks. December annual reconstitution reference date is the last trading day of November, per methodology.
- **INFERENCE**: None of these changes alter put–call/box parity arithmetic for SPY/QQQ options.

### 6.4 Box spreads
No new published box-spread arbitrage or SPY/QQQ-specific parity analysis found in the sweep (SSRN/arXiv/CBOE, last few weeks). One line: nothing material.

**Unverified / not claimed:** No live box-spread implied-rate check was run this session (light-touch desk; no live options-chain pull in scope) — any current SPX box implied rate is **UNVERIFIED**, not estimated here.

**Desk verdict:** Nothing material requiring a change to parity checks. One item to carry forward: SPXO is live as of Nov 9 — flag any future parity/box work to use the correct AM vs PM settlement per symbol.

---

## 7. Bonds & Rates desk

**Status: COMPLETE.** Module ran clean (exit 0, mode `REAL_FRED_RATES`, source `fred-public-csv-http-200`). No fallback used; no Yahoo yields substituted.

### Module output summary (all numbers from `hedge_desk.rates_desk.rates_environment()`)

| Item | Level | As-of |
|---|---|---|
| Fed funds effective rate (DFF) | **3.88%** | 2026-11-09 |
| Treasury 2Y (DGS2) | **4.56%** | 2026-11-09 |
| Treasury 10Y (DGS10) | **4.88%** | 2026-11-09 |
| 2s10s spread | **+32 bp** (slope 0.04) | 2026-11-09 |
| Curve shape | **UPWARD_SLOPING** | 2026-11-09 |
| SOFR | **3.88%** | 2026-11-09 |
| EFFR | **3.88%** | 2026-11-09 |
| OBFR | **3.88%** | 2026-11-09 |
| SOFR − EFFR spread | **0 bp** | 2026-11-09 |

Module `as_of`: 2026-11-10; underlying FRED observations dated 2026-11-09 (latest trading day). Lookback window: 60 days.

### Findings (evidence-labeled)
- **FACT** — Fed funds effective rate is 3.88% as of 2026-11-09 (FRED DFF via module). Module reports a 0.25 pp change over the 60-day window; the module does not state the sign convention, so the direction of that window change is UNVERIFIED from this output alone.
- **FACT** — 10Y at 4.88% and 2Y at 4.56% (2026-11-09), giving a 2s10s spread of +32 bp and an upward-sloping curve (FRED DGS10/DGS2 via module).
- **FACT** — Curve flattened marginally day-over-day: 2s10s was +35 bp on 2026-11-06 (10Y 4.86 − 2Y 4.51) and +32 bp on 2026-11-09 (10Y 4.88 − 2Y 4.56). The 2Y rose 5 bp while the 10Y rose 2 bp over that one session (FRED history in module output).
- **FACT** — Over the 60-day window both ends drifted lower: 2Y from 4.63% (2026-09-11) to 4.56%; 10Y from 4.96% to 4.88%. The spread is essentially unchanged over the window (33 bp on 2026-09-11 vs 32 bp now) — a modest bull drift, not a slope regime change. 10Y peaked at 5.31% on 2026-10-05; 2Y peaked at 4.92% on 2026-09-28.
- **FACT** — SOFR, EFFR, and OBFR are all 3.88% (2026-11-09): SOFR − EFFR spread is 0 bp. No funding stress signal in the overnight complex.
- **INFERENCE** — Premium-pricing read: the 10Y at 4.88% keeps discount rates elevated, which is continued pressure on long-duration growth multiples — most relevant to the watchlist's high-multiple names (NVDA, TSLA, MSFT). The flat-ish, slightly flattening curve (+32 bp, narrowing 3 bp) offers no steepening tailwind to that pressure. What would change it: a sustained 10Y move below ~4.75% or a 2s10s move materially wider/narrower (±15 bp) would change the read.
- **INFERENCE** — Funding conditions are calm (0 bp SOFR–EFFR), so there is no rates-driven reason to haircut premium-selling capacity on funding-stress grounds. What would change it: SOFR–EFFR widening beyond ~5 bp sustained over several sessions.

**Watchlist implication (one line):** Rates are a mild headwind for growth-multiple premium, not a stress event: 10Y 4.88%, curve +32 bp and flattening at the margin, overnight funding spreads at zero.

---

## Run notes

- **No desk failed.** All seven desks produced output. No retries were needed.
- **Open items carried forward:** (1) IV-pull switch/rollover decision still pending since 2026-10-22 — SPY/QQQ nearest-expiry nulls recur daily by design; today's manual rollover was labeled fallback, not a fix. (2) NVDA Nov 20 expiry IV (the earnings-loaded tenor) is UNVERIFIED — needs its own pull before Nov 17. (3) NVDA December dividend declaration expected ~Nov 19–20 — re-check next week. (4) October CPI print flagged by Pro Farmer — UNVERIFIED, not confirmed by any desk. (5) Hormuz tanker-fire claim (PressTV, Nov 10) — UNVERIFIED, single-source.
- **No Risk of Ruin estimated, no trade proposed, no GitHub operations performed.** Paper-only research input.
