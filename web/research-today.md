# Hedge-desk daily research package — Wed 2026-10-21

**Run:** scheduled 13:30 PT 2026-10-21 · **Mode:** research/input only, no git ops · **Profile:** research (trace claims to evidence; FACT/INFERENCE/SPECULATION/UNVERIFIED) · **Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety.

**IV-inputs freshness:** consumed `~/workspace/hedge-desk-research/nightly/2026-10-20-iv-inputs.json`, `as_of` **2026-10-20T13:54:05-07:00** (~23.6h before run start — **within the 26h guard**, labeled throughout as yesterday's post-close data). Supplemented with a **live Yahoo v7 options pull** (~13:52 PT today, cookie+crumb; first attempt's sad-panda HTML classified transient, recovered on fresh jar — labeled LIVE below) and the earnings desk's post-close live chains for TSLA/MSFT/AAPL.

**Desk health:** 6 of 7 desks delivered. Bonds & Rates **FAILED** (FRED unreachable — see §7).

---

## Synthesis — the 5 decision-relevant items

1. **TSLA reported AMC today; the binary is over.** Q3 2026: revenue $28.05B (~flat YoY, slight miss vs Tesla's own $28.34B consensus), non-GAAP EPS $0.48 beat ($0.45), but GAAP operating income $718M — down ~56% YoY, opex-driven (auto gross ex-credits actually improved QoQ). PROVISIONAL: secondary sources only (ir.tesla.com 403, EDGAR 8-K not yet filed / 503), and two source sets conflict materially — verdict fails closed on Set A. Pre-event straddle priced ±5.56% vs 7.77% historical avg — the market underpriced the magnitude; the avoid-premium-into-binary rule was the right call. Stock +~1.9% shortly after (Barron's).
2. **Prompt energy tightness is the macro read of the day.** WTI curve in steep backwardation (−$16.37/−16.7% Dec26→Dec27), distillates 9% below 5-yr avg after today's on-schedule EIA print (crude −3.06 MMbbl, 3rd straight draw), ≥18 vessel attacks in 2 weeks with Iran targeting tankers beyond Hormuz. Ags price abundance (carry, harvest rolling, China buying beans aggressively). Caveat: the rates desk failed today, so the discount-rate leg of the growth-multiple read is blind — do not infer a rates regime from this package.
3. **NVDA front-week IV collapsed −570 bps** (36.19% → 30.48% on healthy 65k/11k quotes) — the largest single-day repricing on the board. Still ~6 pts above trailing realized on a clean window. INFERENCE: event-calendar drift (nothing in the front week), not mispricing — but a re-expansion above ~34% with no catalyst would merit investigation.
4. **MSFT Oct 28 earnings priced correctly in term shape** (Oct-30 36.2% hump vs 24.27% near-weekly). Binary ahead — short gamma into Oct 28 stays on the avoid list. AAPL Nov 2 straddle ±5.00% is the market's binary price, window-inflated vs its 2.46% single-day history.
5. **Quant lab: 5 new candidates, 3 WATCH (#121/#122/#123, scorer max 61), none at TEST.** #114 vol-lab pushed today (content commits, stays WATCH). #87 conformalForecast still live on CRAN.

**Nothing material:** dividends (no in-window events; MSFT $0.98 ex Nov 19 is 1 day outside the window; AAPL declaration watch Nov 2), parity (no methodology changes affecting SPX/VIX settlement; no published violation analysis).

---

---

## 1. Earnings Event desk

### In-window calendar (all verified today, 2026-10-21 ~16:35 ET)

| Symbol | Report date | Timing | Status |
|---|---|---|---|
| TSLA | Wed Oct 21 | **AMC — REPORTED today** | Release crossed ~16:10–16:13 ET (The Circuitry, verified timestamp 4:13 PM EDT 2026-10-21) |
| MSFT | Wed Oct 28 | AMC | Nasdaq earnings calendar API (fetched today) |
| AAPL | Mon Nov 2 | AMC | Nasdaq earnings calendar API (fetched today) |
| NVDA | Wed Nov 18 | — | Nasdaq calendar confirms Nov 18 — **out of window** (timing not listed; typically AMC) |
| SPY / QQQ | — | — | Index ETFs; no earnings (definitional) |

**TSLA release-access status (FACT):** the primary release could NOT be read. ir.tesla.com returned HTTP 403 to the fetcher; SEC EDGAR 8-K listing for CIK 1318605 at 16:33 ET showed the latest 8-K dated 2026-10-02 (no earnings 8-K filed yet), and the EDGAR recheck returned HTTP 503 (rate-limited), so post-16:33 ET 8-K status is UNVERIFIED. Tesla files the deck on IR before the 8-K, consistent with the numbers circulating in press. The statement-teardown step is therefore incomplete — flagged below.

### TSLA Q3 2026 — reported AMC today (secondary-source numbers, conflicts labeled)

**Set A** (TeslaNorth and The Circuitry, both attributing figures to Tesla's Q3 2026 Update deck; TeslaNorth: "posted to its investor relations site after the market closed"):
- Revenue **$28.05B**, ~flat YoY (vs $28.10B Q3 2025) — in line with Zacks $27.79B (primexbt, 2026-10-14 estimate) and longbridge $27.94B; slight miss vs Tesla's own company-compiled consensus of **$28.34B** (optionsearnings, citing Tesla's Oct 19 consensus sheet)
- GAAP EPS **$0.22**; Barron's live coverage reports "24 cents vs 45 cents expected" — minor conflict ($0.22 vs $0.24), attributed to rounding/diluted-share detail, unresolved
- Non-GAAP EPS **$0.48** — beat vs $0.45 company-compiled and $0.43 Zacks
- GAAP operating income **$718M**, 2.6% margin — down ~56% YoY per The Circuitry
- Auto gross margin **18.5% GAAP / 18.1% ex-reg-credits**, up from 16.9%/16.3% in Q2
- OCF **$6.26B**, FCF **$1.53B** after $4.73B capex; cash **$45.45B** (+$1.9B QoQ)
- Deliveries 486,532 / production 464,391 / storage 13.7 GWh (FACT, pre-announced Oct 2 per Tesla IR)
- FSD: >75% of NA deliveries included it; 1.74M subscriptions, +67% YoY
- Barron's: stock up ~1.9% shortly after the release

**Set B** (Teslarati): revenue $28.095B, non-GAAP EPS $0.50, op margin 5.8%, op income $1.624B, FCF $3.99B — **materially conflicts with Set A** on every profit/cash line. Marked UNRESOLVED; Set B is not used in any verdict.

### Options-implied moves (live Yahoo v7 chains, pulled 2026-10-21 ~16:34 ET post-close, cookie+crumb handshake; ATM straddle mids ÷ spot)

| Symbol | Expiry used | DTE | Spot | ATM strike | Call mid / put mid | Straddle | Implied |
|---|---|---|---|---|---|---|---|
| TSLA | 2026-10-23 | 1.2 | 386.47 | 387.5 | 10.32 / 11.18 | 21.50 | **±5.56%** |
| MSFT | 2026-10-30 | 8.2 | 532.95 | 532.5 | 14.93 / 14.03 | 28.95 | **±5.43%** |
| AAPL | 2026-11-06 | 15.2 | 343.99 | 345.0 | 8.43 / 8.77 | 17.20 | **±5.00%** |

Notes: TSLA implied move shrank from yesterday's ±6.48% into the print (FACT, recomputed both days). MSFT/AAPL expiries are the nearest weekly containing each event, but their 8.2- and 15.2-day windows include many non-event sessions — these are **window** implied moves, not pure event moves (FACT, stated as given).

### Historical reaction-day moves (report-day close → next-session close; recomputed from Yahoo v8 daily closes, signs set by arithmetic)

**TSLA** (n=8): avg |move| **7.77%**, signed mean +0.34%, 4 up / 4 down.
- 2026-07-22: 374.01 → 319.69 = **−14.52%** (largest |move| in the set)
- 2026-04-22: 387.51 → 373.72 = −3.56%; 2026-01-28: 431.46 → 416.56 = −3.45%
- 2025-10-22: 438.97 → 448.98 = +2.28%; 2025-07-23: 332.56 → 305.30 = −8.20%
- 2025-04-22: 237.97 → 250.74 = +5.37%; 2025-01-29: 389.10 → 400.28 = +2.87%
- 2024-10-23: 213.65 → 260.48 = +21.92%

**MSFT** (n=8): avg |move| **7.02%**, signed mean −0.25%, 3 up / 5 down.
- 2026-07-29: 389.81 → 450.25 = **+15.51%** (dominant observation in the set)
- 2026-04-29: 422.75 → 406.13 = −3.93%; 2026-01-28: 478.59 → 430.77 = −9.99%
- 2025-10-29: 537.13 → 521.47 = −2.92%; 2025-07-30: 508.22 → 528.28 = +3.95%
- 2025-04-30: 390.67 → 420.46 = +7.63%; 2025-01-29: 436.32 → 409.35 = −6.18%
- 2024-10-30: 425.80 → 400.03 = −6.05%

**AAPL** (n=8): avg |move| **2.46%**, signed mean −1.53%, 2 up / 6 down.
- 2026-07-30: 333.14 → 308.64 = −7.35% (largest in the set); 2026-04-30: 270.87 → 279.64 = +3.24%
- 2026-01-29: 257.58 → 258.78 = +0.46%; 2025-10-30: 270.40 → 269.37 = −0.38%
- 2025-07-31: 206.57 → 201.41 = −2.50%; 2025-05-01: 212.02 → 204.09 = −3.74%
- 2025-01-30: 235.88 → 234.30 = −0.67%; 2024-10-31: 224.04 → 221.06 = −1.33%

### Pre-release consensus (for MSFT/AAPL; TSLA now superseded)

- **MSFT** FY2027 Q1: EPS $4.71–$4.73 (TipRanks $4.71; tradingkey $4.73), revenue **$90.65B** (tradingkey) — FACT, pages crawled within the last day.
- **AAPL** FY2026 Q4: EPS **$1.99** (TipRanks), vs $1.85 last year. Revenue consensus: UNVERIFIED (not found on the sources checked).
- **TSLA** (was): company-compiled adj EPS $0.45 / revenue $28.34B (optionsearnings citing Tesla Oct 19); Zacks adj EPS $0.43 / revenue $27.79B (primexbt). Superseded by actuals above.

### Verdicts (each states what would change it)

1. **TSLA print (PROVISIONAL, contingent on Set A):** revenue in line-to-slightly-light vs Tesla's own consensus ($28.05B vs $28.34B), non-GAAP EPS beat ($0.48 vs $0.45), but GAAP operating income sharply down YoY ($718M, 2.6% margin). Auto gross margin ex-credits improved QoQ (16.3% → 18.1%) while total op income fell — INFERENCE: the profit decline is opex-driven (+39% per Set A), not gross-margin-driven. *Would change it: reading the actual Q3 Update deck / 8-K; the Set B conflict is unresolved and this verdict fails closed if Set A proves wrong.*
2. **Implied vs historical:** TSLA options priced ±5.56% vs 7.77% historical average |move| — the market priced a below-average-magnitude reaction tonight (FACT arithmetic; the read is INFERENCE). MSFT ±5.43% vs 7.02% historical — but on an 8.2-day window, so not apples-to-apples; labeled as such. AAPL ±5.00% on a 15.2-day window vs 2.46% single-day historical average — window-inflated, not directly comparable; labeled as such.
3. **Direction:** historical TSLA reactions are a coin flip (4 up / 4 down, signed mean +0.34%); no directional edge is claimed. Nothing in the verified data contradicts this, and per the brief there is no speculation on price direction.

**Desk status:** all three in-window names covered; NVDA out of window confirmed; SPY/QQQ non-events noted. Data gaps by name: AAPL revenue consensus (UNVERIFIED), TSLA primary-release teardown (BLOCKED — IR 403, EDGAR 503; two conflicting secondary sets), TSLA GAAP EPS $0.22 vs $0.24 (minor unresolved conflict).

---

## 2. Dividend Opportunity desk

| Name | In-window ex-date (through ~Nov 18)? | Detail |
|---|---|---|
| AAPL | None declared | Next quarterly $0.27 **not yet declared** — FACT (stockinvest.us, crawled ~13:30 PT today: "has not yet announced its next dividend date"). Declaration expected with FQ4 earnings **Mon Nov 2** — FACT (Apple's IR calendar, confirmed via MacDailyNews/9to5Mac/appleinsider). INFERENCE: ex-date ~Mon Nov 9 following the 2025 cadence (declared Oct 30, 2025; ex Nov 10, 2025). |
| MSFT | **Just outside window** — Thu Nov 19 | $0.98 quarterly, first payment of the **Sep 15, 2026 raise** (record Nov 19, payable Dec 10) — FACT (Microsoft issuer release, news.microsoft.com, 2026-09-15; reconfirmed live today via stockanalysis.com). Consecutive-increase count **24** per desk standard (`dividend-count-standard.md`), incl. the Sep 2026 raise — no drift. (stockanalysis.com displays a different methodology's "20" — desk standard is binding.) |
| NVDA | None | $0.25/qtr; last paid Oct 1 (ex Sep 10) — FACT (NVIDIA Q2 FY27 earnings release, nvidianews.nvidia.com). Next not yet declared (finbold, 2026-10-11: "has yet to declare the payout officially"). INFERENCE from pattern: next ex ~early Dec (~Dec 3) — UNVERIFIED. |
| SPY | None | Last ex 2026-09-18 ($1.889) — FACT (Yahoo v8 chart events=divs, pulled today). Next ex ~Dec 18 (pattern) — INFERENCE. |
| QQQ | None | Last ex 2026-09-21 ($0.751) — FACT (same Yahoo pull). Next ex ~Dec 21 (pattern) — INFERENCE. |
| TSLA | N/A | Pays no dividend — FACT (Yahoo v8 chart events=divs returns no dividend events in history). |

- **Increases/cuts/specials in window:** none announced. No declarations, raises, cuts, or specials on watchlist names verified in the last 7 days. Apple's next raise cycle is annual-in-May (May 2026 → $0.27), so a November raise is not expected — INFERENCE.
- **Desk verdict:** no in-window dividend event for capture trades. Two named near-window events: MSFT's $0.98 ex-div Thu Nov 19 (1 day outside the window, FACT); AAPL's declaration watch on Nov 2 (ex-date expected ~Nov 9, outside window, UNVERIFIED). What would change it: an issuer declaration inside the window (none pending on IR calendars).
- **Coverage note:** Nasdaq dividends calendar API returned zero rows for all five symbols two days running — classified transient/unreliable; desk verified via issuer releases and web (labeled above). **Sources:** Nasdaq calendar API (0 rows, transient), Yahoo v8 chart events=divs (pulled 2026-10-21 13:31 PT), Microsoft issuer release (news.microsoft.com/source/2026/09/15/), stockanalysis.com (accessed 2026-10-21), stockinvest.us, NVIDIA newsroom Q2 FY27 release, Apple IR calendar via MacDailyNews/9to5Mac.

---

## 3. Overnight Premium (IV) desk

### Data vintages
- **IV-inputs file** `~/workspace/hedge-desk-research/nightly/2026-10-20-iv-inputs.json`, `as_of` 2026-10-20T13:54:05−07:00 — within the 26h guard, **ACCEPTED**. All realized-20d figures below are yesterday's post-close; all ATM-IV figures from the file are yesterday's live session.
- **Fresh live v7 options pull** (this run, one retry): success. Cookie jar seeded via curl + crumb handshake (crumb valid from `query1`), then per-expiry chains. All calls ATM within 0.5% of spot, call/put impliedVolatility mean, non-degenerate volume (SPY 10-23 call 17k/put 13k; QQQ 10-23 19k/21k; NVDA 10-23 call 65k/put 11k). Pull time **~13:52 PT 2026-10-21** (quotes aligned to spots below, FACT). Spots: SPY 773.09, QQQ 725.20, AAPL 343.99, MSFT 532.95, NVDA 221.97, TSLA 386.47. (The first attempt's sad-panda error HTML classified as a transient Yahoo session flap, recovered on a fresh jar.)
- **TSLA/MSFT/AAPL straddle reads**: today's post-close (~16:34 ET) live chains pulled by the Earnings desk, verified live — labeled as such.
- **Yesterday's live session values** (2026-10-20) shown for DoD context only, explicitly labeled YESTERDAY.

### Live IV snapshot — ATM implied vol (%)
| Name | Spot (13:36 PT) | Oct-23 (DTE ~1.2) | Oct-30 (DTE ~8.2) / Nov-6 | Vintage |
|---|---|---|---|---|
| SPY | 773.09 | **10.83** | **13.04** | today's live chain |
| QQQ | 725.20 | **19.03** | **22.66** | today's live chain |
| AAPL | 343.99 | 23.39 YESTERDAY | 24.5 (Nov-6, straddle-implied) | earnings desk post-close chain |
| MSFT | 532.95 | 24.27 YESTERDAY | 36.2 (straddle-implied) | earnings desk post-close chain |
| NVDA | 221.97 | **30.48** | **32.51** | today's live chain |
| TSLA | 386.47 | 77.69 YESTERDAY (pre-report) | 56.54 YESTERDAY (pre-report) | pre-event relic — binary OVER |

DoD move (FACT): SPY −1.1/−0.3 pts, QQQ −2.1/−0.2, NVDA −5.7/−3.7 vs yesterday's session. NVDA's front-week fell ~570 bps — the largest single-day change on the board.

### IV-vs-realized (realized = 20d trailing, yesterday's post-close file)
| Name | 20d realized | Near-term IV (today's vintage) | Read |
|---|---|---|---|
| SPY | 9.18% | 10.83% (Oct-23) | IV modestly above realized; window clean (share 0.204) — mild premium available. FACT/INFERENCE |
| QQQ | 15.86% | 19.03% (Oct-23) | **WINDOW-CONTINGENT** (0.341) — no clean verdict; single day drives >30% of window variance |
| AAPL | 16.47% | 24.5% (Nov-6) | **WINDOW-CONTINGENT** (0.374) — no clean verdict |
| MSFT | 22.08% | 36.2% (Oct-30) | **WINDOW-CONTINGENT** (0.347); Oct-28 earnings inside window — elevation is expected, not "rich" |
| NVDA | 24.23% | 30.48% (Oct-23) | IV ~6 pts above realized; window clean (0.237). Caveat: 1.2-DTE IV vs 20d trailing — directional only, not arbitrage |
| TSLA | 33.10% | pre-event relic | No verdict — binary event over (reported AMC today); pricing is mid-collapse |

### Term-structure notes
- **MSFT earnings hump intact**: Oct-30 IV 36.2% vs near-weekly 24.27% (yesterday) — the hump sits exactly on the Oct-28 earnings inside the Oct-30 window (FACT). Textbook vol surface behavior.
- **TSLA inversion resolved**: Oct-23 77.69% vs Oct-30 56.54% yesterday (inverted — earnings in front week). Event reported AMC today; the inversion unwinds overnight. No residual premium opportunity; IV crush is vega collecting its due (INFERENCE from term shape + reported event).
- SPY/QQQ/NVDA show mild upward term slope into next week — consistent with normal carry, no binary priced into front weeks (FACT from chain data; MSFT is the exception).

### Binary-event flags
- **TSLA — PAST**: Q3 2026 reported AMC today (~16:10–16:13 ET). Premium INTO the event = avoided; premium AFTER = no play. (FACT, earnings desk verified)
- **MSFT — AHEAD**: earnings Oct 28 sit inside the Oct-30 window — elevated Oct-30 IV is warranted. Selling premium into Oct 28 = short gamma into a binary; avoid. (FACT, per calendar)
- **AAPL — AHEAD**: Nov 2 earnings, outside the Oct-30 window but inside Nov-6. The Nov-6 straddle ±5.00% (24.5% implied) prices the binary; same avoid rule. (FACT/INFERENCE)
- **NVDA — AHEAD but distant**: Nov 18 earnings — no hump in front month; no event premium to harvest or avoid in near windows. (FACT)

### Verdicts (each labeled; what would change it stated)
1. **SPY — mild sell-side skew only; nothing actionable.** Near-weekly IV 10.83% vs 9.18% realized on a clean window = ~1.6 pts of premium, normal front-week carry. FACT: neither rich nor cheap. *Changes if: IV compresses below ~9% with no vol event (complacency signal) or realized breaks above 12% on a regime shift.*
2. **QQQ — UNVERIFIED read.** 19.03% vs 15.86% realized looks premium-rich, but the window is CONTINGENT (0.341) — one day drives >30% of the variance, so the 20d number is polluted. FACT: no clean verdict possible. *Changes if: the contingent day rolls out of the 20d window or NVDA/MSFT event vol passes through.*
3. **AAPL — no premium read before Nov 2.** Near-window pricing is pre-event; the Nov-6 straddle ±5.00% is the market's binary price. Selling into Nov 2 = short gamma into earnings — avoid per desk rule. INFERENCE from calendar + chain. *Changes if: implied move collapses post-Nov-2 without a volatility regime change.*
4. **MSFT — earnings hump expected; no edge.** Oct-30 36.2% vs 24.27% near-weekly is the Oct-28 earnings priced correctly in term shape (window CONTINGENT, 0.347 — no clean verdict on the level). INFERENCE: the hump is the market agreeing with our calendar. *Changes if: hump inverts or disappears before Oct 28 (signals date move or stale calendar).*
5. **NVDA — watch the front-week collapse, no trade.** 30.48% today vs 36.19% yesterday (−570 bps) with healthy quotes is a real DoD repricing (FACT: volumes 65k/11k, strikes ATM). IV still above 24.23% realized on a clean window (0.237) — not complacent. INFERENCE: the drop reflects event-calendar drift (nothing in front week), not mispricing. *Changes if: front IV re-expands above ~34% with no new catalyst — would signal information leakage worth investigating.*
6. **TSLA — event over, no premium desk position.** Pre-event straddle ±5.56% is a relic; the crush is underway. Desk rule: premium into a binary = avoid was the correct call; now there is nothing to price. FACT. *Changes if: nothing — the binary has occurred.*

### Sources
- Live chains: `https://query1.finance.yahoo.com/v7/finance/options/{SPY,QQQ,NVDA}` with cookie+crumb, pulled ~13:52 PT 2026-10-21 (files `/tmp/opt_retry_{SPY,QQQ,NVDA}.json`, all HTTP 200 JSON — the first attempt's sad-panda HTML classifies as a transient Yahoo session flap, recovered on fresh jar).
- Realized/atm_iv/window_contingent: `~/workspace/hedge-desk-research/nightly/2026-10-20-iv-inputs.json` (`as_of` 2026-10-20T13:54:05−07:00).
- TSLA/MSFT/AAPL straddles: earnings desk post-close chains `/tmp/earn/ch_tsla_1023.json`, `/tmp/earn/ch_msft_1030.json`, `/tmp/earn/ch_aapl_1106.json`.
- Technique: `~/workspace/custom-skills/local-cfa-financial-analysis/references/derivatives_options.md` (vol surface/term structure, IV sanity checks, parity-as-ground-truth).
- UNVERIFIED items: QQQ/AAPL/MSFT IV-vs-realized verdicts (window-contingent per standing rule); TSLA post-collapse IV level (not pulled — event over, no desk use).

---

## 4. Open Quant/AI Model Lab

**Sweep window:** since 2026-10-20 sweep (ledger closed at #118). Ledger rows #119–#123 appended today and verified on disk.

### New candidates

| # | Item | Scorer | Disposition |
|---|---|---|---|
| 119 | Johansen/Lange/Skovmand — "Arithmetic Models for Commodity Futures, Vanilla, and Calendar Spread Options" (arXiv:2610.28071v1, 20 Oct 2026, q-fin.PR) | 42 | ARCHIVE — arithmetic multi-factor SV for commodity futures + vanilla/calendar-spread options, UKF on WTI panel 2013–2024; no author code → reproducibility not established; commodity-specific, not watchlist-transferable |
| 120 | Perez Mendoza/Godin — "Deep catastrophic-risk-aware reinforcement learning" (arXiv:2610.27214v1, 19 Oct 2026, cs.LG/q-fin.RM) | 39 | ARCHIVE — EVT-CVaR deep hedging via peaks-over-threshold; no code; tail-risk-RL is risk-engine-adjacent, not a desk lane |
| 121 | kavinilas20/options-pricing-lab — BSM/binomial/MC + American pricer + delta-hedging sim, 193 tests (GitHub, created 2026-10-21, MIT) | 52 | WATCH — 193 tests (175 pass), deterministic seed-42 byte-identical run_summary.json, parity to machine precision; honest "study, not a trading strategy" framing; crowded deterministic-tooling lane |
| 122 | Amitav507/energy-derivatives-pricing — Black-76/BSM energy & commodity derivatives library, analytic Greeks, CI (GitHub, created 2026-10-21, MIT) | 58 | WATCH — value is futures-desk pattern (free forward-curve fetch path needs audit); energy-specific |
| 123 | mrailouis/zpew — C++20 vol forecasting terminal (GARCH/EWMA) + OOS backtests + VaR backtesting (GitHub, created 2026-10-21, Apache-2.0) | 61 | WATCH — top of band; OOS-discipline framing is the premium-desk-relevant value; TEST opens only on sandbox evidence |

- **Sweep summary:** 5 new candidates (2 arXiv, 3 GitHub), all README/abstract verified at source; scorer run for each (no hand-scoring). Scorer max 61 → no TEST, no INTEGRATE. Band discipline held.
- **Triage exclusions (no ledger rows):** 12 NOLICENSE GitHub repos + 11 arXiv scope misses (RV aR portfolio opt, LOB-impact, baseball ABS, labor economics, GB electricity, stat-arb neural filtering, etc.).
- **Re-checks:** #105 options-engine unchanged (MIT, stale since 2026-10-19); #106 options-backtester unchanged; #114 vol-lab PUSHED TODAY (2026-10-21T07:43Z, readme/devlog/links — no license/results change), stays WATCH; #87 conformalForecast still live on CRAN (303).
- **Process notes (kaizen):** arXiv API host export.arxiv.org unreachable from sandbox today (2 attempts, connection-level) — routed via arXiv web abs pages + academ.us mirror as window-coverage evidence. GitHub search API healthy (no 403s). Scorer arithmetic discipline re-confirmed.

---

## 5. Weather/War/Logistics Futures Event desk

### Catalyst table (last 24–48h)

| # | Catalyst | Evidence |
|---|---|---|
| 1 | **EIA Weekly Petroleum Status Report released ON SCHEDULE today (Wed 10:30 ET), week ending Oct 16** — crude −3.06 MMbbl to 412.5 MMbbl (3% below 5-yr avg, 3rd straight draw); gasoline −3.0 MMbbl to 205.3; **distillates +1.7 MMbbl to 104.3 (9% below 5-yr avg — big miss vs −1.3 expected)**; refinery inputs 16.6 MMb/d at 93.4% utilization; Cushing +0.9 MMbbl. WSJ/DJ survey expected crude −0.3, gasoline unch, distillates −1.3. | **FACT** — triangulated across Reuters (TradingView 14:47 UTC), Dow Jones/Morningstar (11:16 ET), Oilprice, XTB, OilVoice; EIA data page shows "Weekly stocks — Release date: October 21, 2026." Primary ir.eia.gov text was behind a signed URL; numbers used are secondary but consistent to the second decimal |
| 2 | **API (Tue) showed crude −4.93 MMbbl, gasoline −2.0, distillates −1.6** — direction matched EIA on crude/gasoline but distillates printed opposite (build vs API draw). | **FACT** — Oilprice API report (Oct 20); XTB notes the divergence |
| 3 | **Middle East escalation: ≥18 vessel attacks in 2 weeks (Kpler); Iran targeting tankers beyond Hormuz into Gulf of Oman (LSEG), threatening Gulf loadings and ship-to-ship transfers; Houthis claimed Mon attacks on Aramco Yanbu, Shaybah oilfield, Riyadh/Abha airports; Yemen govt death toll 73.** Iran told Pakistan's army chief no talks with Washington until demands met (Nournews, Oct 20); Qatari delegation in Tehran; mediation hopes deemed distant. | **FACT** — Reuters, Oct 21 (syndicated) |
| 4 | **SovEcon cut Ukraine 2026/27 grain exports −5.1 MMT to 33 MMT** (corn −3.8, wheat −1.2); Odesa ports blocked, Danube ships targeted even in Romanian/Bulgarian waters. | **FACT** — SovEcon via WSJ/Dow Jones commodities roundup (Morningstar, Oct 21) |
| 5 | **USDA daily flash sales: Oct 20 — 612,000 MT soybeans to China; Oct 21 — 134,000 MT to China + 165,000 MT to Spain (2026/27).** ~2.084 MMT reported over the past week; China ~14 MMT committed toward 25 MMT trade-deal target. | **FACT** — Barchart, Pro Farmer, Farm Progress, Oct 20–21 |
| 6 | **NASS Crop Progress (Mon Oct 19): soy harvest 64% complete (~1pt behind normal); corn 44% complete; winter wheat planting 63%** — warm/dry → rapid harvest completion. | **FACT** — USDA NASS via Barchart/Pro Farmer/Price Group, Oct 20–21 |
| 7 | **Brazil: Mato Grosso soy planting 33% done (Oct 9), temps near 40°C stressing young plants; strongest El Niño on record.** SE Asia drought is now physical palm supply disruption (Indonesia river drought stranding supply); MPOC notes 9–12 month output lag. Russia trimmed winter sowing plan to 19M ha on input costs. | **FACT** — Grain Central Daily Market Wire, Oct 20 |
| 8 | **UK approved a controversial gas field amid soaring energy prices** (WSJ commodities roundup). | **FACT** — Morningstar/Dow Jones, Oct 21 (long-dated supply, no prompt impact) |

### What the curves appear to be pricing (all closes Tue Oct 20, 2026 — Yahoo v8, UA header; cents shown as ¢)

- **WTI: steep backwardation.** Dec26 $97.80 → Mar27 $92.40 → Jun27 $87.85 → Dec27 $81.43 (−$16.37/−16.7% over 12 mo). **INFERENCE:** curve prices acute prompt supply risk (items 3 + low US/distillate stocks) fading within a year — either expected de-escalation or supply response. Would change: a credible US-Iran channel or next week's inventories printing a build flattens the front; a Hormuz/Gulf loading hit extends it.
- **Brent: same shape, wider front.** Dec26 $109.76 → Mar27 $99.75 → Jun27 $94.57; Dec26 Brent–WTI spread $11.96. **INFERENCE:** global prompt tightness vs softer US Gulf pricing — consistent with tanker-risk premium offshore and US inventory draws onshore.
- **Natgas (Henry Hub): normal seasonal, but +27.6% y/y.** Nov26 $2.77 → Dec26 $3.17 → Jan27 peak $3.24 → Jun27 trough $2.69 → Dec27 $4.04. **INFERENCE:** market prices a tighter forward balance (LNG pull / winter risk); no panic shape. Would change: a mild winter or strong storage builds Thu.
- **Wheat/corn/soy: carry (contango), no fear premium.** Wheat Dec $6.28¼ → Mar $6.43 (+2.3%); corn Dec $4.64¼ → Mar $4.78¼ (+3.0%); soy Nov $12.46¼ → Jan $12.59¼ (+1.0%) → May $12.75¼. **INFERENCE:** ample supply / harvest pressure priced; even SovEcon's −5.1 MMT Ukraine cut (item 4) hasn't inverted the front — market treats it as EU/US-replaceable. Would change: a Brazil weather scare or a second Ukraine port hit could flip soy/corn fronts toward inversion.
- **Context prints:** gold front $4,151.70 (+$9.10 Tue) — record territory, risk bid consistent with item 3. Oil Wed morning oscillated (Reuters 0350 GMT: WTI +$1.36 to $99.18, Brent +$1.59 to $110.38 on items 1–3; Oilprice mid-morning had WTI $97.69 −0.13%) — **INFERENCE:** market is headline-chasing between mediation hopes and tanker risk; do not read direction from any single snapshot.
- **Caution:** curve snapshot is Tue closes — today's EIA print and Wednesday's Middle East headlines are not yet in these structures. WTI Nov26 $101.79 quote is the *expired* contract's last settlement — excluded from the curve (roll artifact, not a −3.9% move).

### Calendar — next 48h
- **Thu Oct 22, 10:30 ET:** EIA Weekly Natural Gas Storage Report (standard Thursday slot). **FACT** per EIA schedule convention.
- **Thu Oct 22, 8:30 ET:** USDA Weekly Export Sales (standard Thursday slot). **FACT** per USDA convention.
- **Fri Oct 23:** CFTC Commitments of Traders; USDA Cattle on Feed (Oct 1; expected 11.441M head per ADMIS).
- Next WASDE early November — exact date **UNVERIFIED** (last was Fri Oct 9).

### Top items for synthesis
1. **Crude curve in steep backwardation (−16.7%/yr) + distillate stocks 9% below 5-yr avg** — prompt energy tightness is the single most priced risk on the board; watch for Thu natgas storage and any Strait/Gulf-of-Oman incident.
2. **Middle East tanker risk is the live binary** — 18 vessel attacks/2 wks, Iran hitting ships beyond Hormuz; mediation (Qatar/Pakistan) deemed distant.
3. **Ags are pricing abundance, not fear** — harvest is rolling (64% soy, 44% corn), fronts in carry; China is buying US beans aggressively (~2 MMT/week) and it still isn't lifting the curve — demand is the thing to watch for a turn.

---

## 6. Box/Parity Observer (light touch)

- **Nothing material.** No published put-call/box parity-violation analysis in the last 7 days — FACT (checked arXiv q-fin.CP 11 entries and q-fin.MF 17 entries incl. q-fin.TR cross-lists; closest adjacent: arXiv:2610.25671 "Arbitrage-Free Implied Volatility Surface Reconstruction via Additive Martingales," Oct 19 — no-arb by construction in IV-surface fitting, not a violation finding). No new VIX methodology or SPX settlement-procedure documents in the last 7 days — FACT.
- CBOE Fixed Income/ETF BuyWrite indices (BXTB, BXHB, BXLB, BXVBW, BXWBW) methodology change effective Oct 15 close / calculations from Oct 16: option pricing in the 3:45–4:00pm ET window switched from VWAP to last-traded price (Cboe Hanweck theoretical fallback) — FACT (CBOE announcement ref C2026090301). Watch-relevant only for BuyWrite tracking, not SPX/VIX settlement or parity mechanics.
- MSCI finalized "non-operating companies" index methodology Oct 15; Strategy (MSTR) flagged for potential deletion, final list Nov 11, effective Nov 30 close — FACT (CoinDesk/financefeeds, Oct 15–17). MSTR is not on the watchlist; index-eligibility change, not a parity signal.
- Parity spot-check: NOT RUN (no options pull warmed in this desk; not fabricated).
- **Sources checked Oct 21:** cdn.cboe.com announcement C2026090301; fxnewsgroup.com CBOE digest; prnewswire-via-summamoney.com S&P DJI/Kaiko Oct 13 announcement; arXiv q-fin.CP + q-fin.MF recent listings.

---

## 7. Bonds & Rates desk — **FAILED**

The desk produced no output today. The repo's own rates module could not reach FRED — two module-level failures (~13:35 PT pre-run test and ~13:36 PT directed retry with 120s timeout), each after the module's own internal retries: `ValueError: fred fetch failed for DFF (status 0) The read operation timed out`. A plain urllib GET to `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF` also stalls on read (TimeoutError at 20s) — failure is at the network layer between this VM and FRED's host, not an API-key/parse/code issue. Whether FRED's service is degraded or this VM's egress path is blocked is UNVERIFIED (FRED status page not checked). **Late-session refinement (~13:58–14:01 PT):** a plain `curl` to `fred.stlouisfed.org/graph/fredgraph.csv?id=DFF` returned **HTTP 200 in 0.8s** — the host is alive and the path works — but the rates module immediately after still stalled on DFF, and three minutes later the same curl command failed entirely (000, 20s timeout) for both curl and Python. Pattern: **intermittent flapping**, not a hard outage and not a UA/TLS-fingerprint block (the browser-UA curl failed identically when the path was down). Recovery guidance for the module owner: longer backoff / retry across minutes, not a transport rewrite. Fixing the module's retry behavior is a code change — out of scope for this research-only run; flagged as a follow-up. Per desk rules, no Yahoo-yield substitution was made. The fed funds effective rate, DGS10, DGS2, 2s10s slope, and SOFR/EFFR spread are all UNVERIFIED for today. What would change it: a later retry succeeding (transient stalls resolve) — consider a late-session standalone retry of the rates desk.
