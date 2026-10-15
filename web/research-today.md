# Hedge-Desk Daily Research — Thu 2026-10-15

**Package as-of:** ~13:30–14:00 PT Thu 2026-10-15 (16:30–17:00 ET). Research + input only — paper-only context, no trade authorization, no Risk of Ruin.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** Seven parallel desks; every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED. Standing rules applied: Yahoo-first source order with UA header; ^FVX = 5Y (never 2Y); no shutdown/blackout framing for federal releases; IV 26h freshness guard; stale-jump screen (>30% single-day variance share ⇒ WINDOW-CONTINGENT); dividend-count standard (MSFT = 24).

---

## Synthesis — the 5 most decision-relevant items

1. **Two binary earnings events in the next 2 weeks — avoid premium into both.** TSLA Wed Oct 21 after close; MSFT Wed Oct 28 after close. TSLA front ATM IV is 69% (1-day) and its Oct 30-expiry straddle implies ~8.2%; MSFT's Oct 30 expiry carries a clean earnings hump (36.7% IV vs 21.8% at Oct 21) with a ~5.96% straddle. Premium into a binary event = avoid for TSLA Oct 21, MSFT Oct 28, and AAPL Nov 2 expiries.
2. **Rates remain restrictive and the curve bear-flattened.** FRED module (DFF/DGS): fed funds effective 3.88%, 2Y 4.82%, 10Y 5.19% (obs. 2026-10-14); 2s10s +37 bp, flattened ~16 bp over 60 days (2Y +63 bp vs 10Y +47 bp); SOFR−EFFR = 0 bp (no funding stress). Directional read: elevated discount rates keep pressure on long-duration growth multiples (NVDA, TSLA, MSFT, QQQ more than SPY).
3. **Oil is physically tight but the market is pricing demand weakness over disruption.** EIA (released Thu Oct 15, Columbus Day delay — not Wed) showed a −8.6M bbl crude draw vs a small expected build, yet Brent fell ~1.3–1.8% to ~$104–105 on the IEA's deepened 2026 demand cut (−2.6M bpd) plus two vessel sinkings near Hormuz. Diesel/distillate is the tightest leg. No catalyst maps directly to any single watchlist name.
4. **Dividend window is empty — no capture available.** No watchlist name goes ex-dividend Oct 15–Nov 12. Nearest is MSFT Nov 19 (7 days past the cutoff) at the announced $0.98/qtr (24 consecutive annual increases). AAPL's Q4 dividend is not yet declared; its expected early-Nov ex-date is pattern-based only.
5. **Quant Lab: one TEST candidate with direct premium-desk relevance.** #71 (stale-information IV forecasting, full replication code, scorer 75/TEST) supports the premium desk's IV-as-forecaster read and stale-data discipline. No INTEGRATE-ready candidate; five ARCHIVEs on band discipline.

### Cross-desk resolutions (synthesis, not stapling)

- **MSFT implied move — RESOLVED in part.** The Earnings desk found no current-cycle MSFT implied move in free sources (UNVERIFIED). The Premium desk independently computed a ~5.96% Oct 30-expiry straddle from CBOE delayed mids (15-min delayed). Synthesis: use ~6.0% as the chain-derived straddle breakeven for the earnings expiry, labeled INFERENCE from delayed mids — not a forecast, and not a substitute for a live-chain straddle at the print.
- **TSLA implied move — two figures, different methods.** Earnings desk: ±5.0% reported as options-derived by Magnisto, NOT chain-verified. Premium desk: CBOE-mid straddles (1-day 2.92%, Oct 28 expiry ~8.21%, earnings-loaded). Do not blend: the Magnisto figure is unverified-derived; the CBOE straddles are computed from delayed mids on different expiries. The honest band is "mid-single-digits to ~8% depending on expiry and method."
- **NVDA earnings date — DISPUTED, stays UNVERIFIED.** TipRanks Nov 25 vs MarketBeat Nov 18 (estimated, unconfirmed) vs AltIndex Nov 17. All dates fall outside the 2-week window and beyond the Nov 13 expiry the Premium desk pulled, so no NVDA earnings hump is visible in this package. Earnings desk to resolve against NVIDIA IR next run.
- **Yahoo options chain — access path clarified.** Premium desk hit HTTP 401 on Yahoo `/v7/finance/options/` (crumb/cookie workaround blocked at proxy) and fell back to CBOE delayed quotes (labeled). Parity desk succeeded on the Yahoo chain via the standard cookie/crumb flow. Lesson for next run: try the crumb flow first for Yahoo options before falling back to CBOE.
- **IV-inputs file — usable, with a critical catch.** `2026-10-14-iv-inputs.json`, as_of 2026-10-14T13:54:13−07:00 (~23.5h old) is WITHIN the 26h guard. But its `atm_iv` values are 0DTE artifacts (e.g., TSLA 3.2%) and are NOT comparable to term IVs — only realized_20d, variance-share, and window flags were taken from it. IV levels come from live CBOE delayed quotes.
- **EIA timing correction.** The brief assumed Wed Oct 14 10:30 ET; both EIA releases were delayed to Thu Oct 15 by the Oct 12 Columbus Day holiday. Federal releases remain on schedule — no shutdown/blackout framing applies.

---

## Desk 1 — Earnings Events

**Question:** Which watchlist names report in the next 2 weeks (through ~Oct 29), when, and what does the options market imply?

**Verdict:** Two in-window, both after close: **TSLA Wed Oct 21** and **MSFT Wed Oct 28**. AAPL (Nov 2) and NVDA (mid/late-Nov, disputed) are outside the window. SPY/QQQ have no earnings. See Synthesis for implied-move resolutions. **What would change it:** a live Yahoo/Nasdaq chain straddle for each name, or a company-confirmed date change.

| Ticker | Date | Timing | Period | Consensus EPS | Consensus revenue | Implied move | Hist. avg earnings-day move |
|---|---|---|---|---|---|---|---|
| TSLA | Wed Oct 21, 2026 | After close; webcast 4:30 p.m. CT / 5:30 p.m. ET | Q3 2026 | ~$0.45 — single secondary source, UNVERIFIED vs primary aggregator | ~$27.5–28.3B — reported range, single secondary source | ±5.0% Magnisto-derived, NOT chain-verified | ±7.7% avg abs. next-day, last 8 (Magnisto, with internal label inconsistencies — use with caution); other windows/methods ±5.6% / ±5.2% |
| MSFT | Wed Oct 28, 2026 | After close; call 2:30 p.m. PT / 5:30 p.m. ET | FY27 Q1 | $4.72 (MarketBeat) | $90.61–90.71B (sources differ $0.10B, UNVERIFIED which is current) | UNVERIFIED in free sources; ~5.96% Oct 30 straddle per Premium desk CBOE mids (see Synthesis) | ~4.0% avg actual vs ~5.3% avg implied, last 12 qtrs (Market Chameleon study, undated — historical context, not current) |
| SPY / QQQ | — | — | — | — | — | — | N/A — ETFs, no earnings |
| AAPL | **Outside:** Mon Nov 2, 2026 | After close; call 2:00 p.m. PT | FY26 Q4 | $1.99 (Zacks/TipRanks) | — | Out of scope | — |
| NVDA | **Outside:** disputed (Nov 17 vs 18 vs 25) | After close (per TipRanks) | FY27 Q3 | $2.47 (TipRanks) vs $1.45 (AltIndex) — conflict | — | Out of scope | — |

- **TSLA — FACT (date/timing):** Tesla posts Q3 2026 results after close Wed Oct 21, per its Oct 2 production/deliveries release (Form 8-K Ex. 99.1). Already-known operating figures: Q3 production 464,391; deliveries 486,532 (Model 3/Y 478,237; Other 8,295); storage 13.7 GWh. **INFERENCE:** deliveries beat expectations per secondary coverage, but Tesla states deliveries/storage "should not be relied on as an indicator of quarterly financial results" — do not extrapolate revenue/margin from deliveries alone.
- **MSFT — FACT (date/timing):** Microsoft publishes FY27 Q1 after close Wed Oct 28, per company release Oct 7. Company guide (as reported): fiscal Q1 revenue ~$90.4B, ~45% Azure constant-currency growth. **INFERENCE:** the print matters less than Azure growth + Azure guide + capex/FCF conversion. Prior-quarter context: Azure +43%, Microsoft Cloud $59.3B (+27%), RPO/backlog $678B.
- **MSFT last print (Jul 29) — UNVERIFIED conflict:** Market Chameleon says +15.5% day-after; TradingNews reports a 12.1% gap-up. Do not quote either as settled without reconciling close-to-close definitions. Prior-beat pattern (shares fell 3.01%, 9.80%, 5.00% after three beats before July) is secondary, UNVERIFIED vs primary price history.
- **Value lens (INFERENCE, no trade authorization):** Both in-window prints are guidance events, not history events — TSLA (auto margin ex-credits + Robotaxi/Optimus credibility vs ~197x forward P/E per one secondary source) and MSFT (Azure durability vs AI capex conversion). Margin of safety lives in the guide and cash conversion, not beating consensus EPS by a cent. **SPECULATION:** none offered.
- **CFA read-order (prospective — no release exists yet to tear down):** (1) guidance vs consensus; (2) GAAP statement vs headline adjusted figure; (3) cash-flow statement (OCF vs net income, capex, buybacks vs issuance); (4) segment margins; (5) balance-sheet deltas; (6) call transcript last. No teardown performed — fail closed, do not pre-write it.
- **Gaps:** Nasdaq earnings-calendar API and Yahoo calendar not directly retrievable in this desk's pass; dates rest on company releases (MSFT, TSLA) and IR-page reporting (AAPL) — primary or near-primary for dates.

Sources: MSFT release https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; TSLA 8-K Ex. 99.1 via https://www.morningstar.com/news/business-wire/20261002169209/tesla-third-quarter-2026-production-deliveries-deployments ; TSLA implied/history https://www.magnisto.ai/earnings/TSLA ; MSFT consensus https://www.marketbeat.com/earnings/reports/2026-10-28-microsoft-co-stock/ ; AAPL date https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/ ; NVDA dates https://www.tipranks.com/stocks/nvda/earnings , https://altindex.com/earnings-calendar/nvda

---

## Desk 2 — Dividend Opportunities

**Question:** Which watchlist names go ex-dividend in the next 4 weeks (through ~Nov 12), and are there announced increases, cuts, or specials?

**Verdict:** No watchlist name goes ex-dividend inside the window — the window is empty. Only near-term ex-date is MSFT Nov 19, one week past the cutoff, carrying the already-announced Sep 15 raise to $0.98/qtr. No cuts, no specials. **INFERENCE:** no dividend-capture opportunity in this window, and none manufactured — an ex-date capture is not a mispricing; price adjusts by roughly the distribution amount.

| Symbol | Ex-date in window | Amount | Status |
|---|---|---|---|
| SPY | None | — | Next ex-date Dec 18, 2026 |
| QQQ | None | — | Last ex Sep 21, 2026; next ~Dec, not yet declared |
| AAPL | None | — | Q4 dividend not yet declared as of Oct 15 |
| MSFT | None | — | Next ex-date Nov 19, 2026 — just outside window |
| NVDA | None | — | Last ex Sep 10, 2026; next ~Dec, not yet declared |
| TSLA | None | — | Pays no dividend |

- **Method [FACT]:** Nasdaq dividends calendar API queried day-by-day for every trading day Oct 15–Nov 12 returned zero watchlist hits; cross-checked vs Nasdaq per-symbol histories. Yahoo v10 quoteSummary returned HTTP 401 (not used for forward dates); Yahoo v8 chart `events=div` corroborated historical amounts. SPY is NYSE-listed so Nasdaq's per-symbol endpoint declines it — SPY dates from State Street schedule (labeled fallback).
- **SPY [FACT, State Street]:** Last ex Sep 18, 2026, $1.889/share, payable Oct 30. Next ex Dec 18, 2026, payable Jan 29, 2027; potential Dec 31 excise distribution also scheduled. **INFERENCE:** do not mistake the Oct 30 payment for an opportunity — only holders of record Sep 18 receive it. Consecutive-increase counts do not apply to SPY.
- **QQQ [FACT, Nasdaq]:** Last ex Sep 21, 2026, $0.75143, paid Oct 8. Yield 0.41%, annualized $3.01. Prior 2026: Mar 23 ($0.73282), Jun 22 ($0.81349). Next ~late Dec by pattern (Dec 22, 2025; Dec 23, 2024) — exact date UNVERIFIED, not yet declared.
- **AAPL [FACT, Nasdaq + Zacks]:** Last ex Aug 10, 2026, $0.27, declared Jul 30, paid Aug 13. Yield 0.31%, annualized $1.08. 2026: Feb 9 $0.26, May 11 $0.27 (+3.8% — annual raise, declared Apr 30), Aug 10 $0.27. **No future dividend declared** (Zacks). Third-party estimators project ~Nov 9–10 ex-date at $0.27 — UNVERIFIED estimate, not a declaration. Full consecutive-increase streak UNVERIFIED (standard forbids copying screener counts; Nasdaq history confirms annual May raises 2024–2026 only). *What would change it:* a board declaration, expected around earnings.
- **MSFT [FACT, Nasdaq + count standard]:** Next ex **Nov 19, 2026**, $0.98, declared Sep 15, record Nov 19, payable Dec 10. Increase $0.91 → $0.98/qtr, +7.7% (calculated). Count: **24 consecutive annual increases (incl. Sep 2026 raise)**, per `dividend-count-standard.md` (count increments on announcement; initiated 2003). Staleness trap: Nasdaq header still shows annualized $3.64 (old rate) and yield 0.68%; forward annualized at declared rate = $3.92 (calculated). No cut, no special.
- **NVDA [FACT, Nasdaq + Morningstar]:** Last ex Sep 10, 2026, $0.25, declared Aug 26, paid Oct 1. Yield 0.45%, annualized $1.00. May 2026: raised $0.01 → $0.25 (+2,400%) alongside +$80B buyback authorization; Aug 26 declaration held $0.25. Under the standard, consecutive-increase run = **1 year (2026 only)** — payouts flat at $0.01 through 2024, 2025, Mar 2026 (derived from verified Nasdaq rows). Next ex ~early Dec by pattern — UNVERIFIED. **INFERENCE:** even after a 2,400% raise, yield <1% — a capital-return signal, not an income thesis; buybacks remain dominant (~$26B returned in fiscal Q2 2027, mostly buybacks, per company-reported figures in press coverage).
- **TSLA [FACT, Nasdaq]:** Pays no dividend — ex-date / yield / annualized all N/A.

Sources: Nasdaq calendar API `https://api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD&type=ex-dividend` (per trading day Oct 15–Nov 12); Nasdaq per-symbol dividends API; Yahoo v8 chart `events=div`; State Street SPDR distribution schedule 2026; `~/workspace/hedge-desk-research/dividend-count-standard.md`; Morningstar NVDA hike https://www.morningstar.com/stocks/nvidias-immense-dividend-hike-puts-dividend-growth-stocks-spotlight ; Zacks AAPL https://www.zacks.com/stock/research/AAPL/dividend-history

---

## Desk 3 — Overnight Premium (IV)

**Question:** Where does implied vol sit across the watchlist term structure, and which expiries carry binary-event premium to avoid?

**Verdict:** No symbol gets an "elevated IV rank" call — IV rank is UNVERIFIED (no free IV-history source). On LEVELS: TSLA front vol richest (69% 1-day ATM IV into Oct 21 earnings); MSFT shows the cleanest earnings hump (Oct 30 expiry 36.7% vs 21.8% at Oct 21); AAPL Nov 13 (27.4%) carries Nov 2 earnings. SPY/QQQ flat-to-gently-upward, no event hump. All six show ~30-day IV above (stale) 20-day realized, but 4 of 6 verdicts are WINDOW-CONTINGENT, so none is a clean "IV rich vs realized" call. Premium into a binary event = avoid for MSFT Oct 28, TSLA Oct 21, AAPL Nov 2 expiries.

### Provenance & freshness guard

| Source | As-of | Status |
|---|---|---|
| `nightly/2026-10-14-iv-inputs.json` | 2026-10-14T13:54:13−07:00 (~23.5h old) | ✅ WITHIN 26h guard — usable for realized vol + window flags. STALE for IV levels |
| CBOE delayed quotes `cdn.cboe.com/api/global/delayed_quotes/options/{SYM}.json` | 2026-10-15 ~20:27–20:28 UTC (≈13:27–13:28 PT, 15-min delayed) | ✅ LIVE — IV levels source (labeled fallback) |
| Yahoo chart (spot) | 2026-10-15 20:00 UTC (close) | ✅ LIVE |

**Fallback disclosure [FACT]:** Yahoo options-chain endpoint returned HTTP 401 on both query1/query2 despite the standing UA header; crumb/cookie workaround blocked at proxy (fc.yahoo.com 404; finance.yahoo.com reset). Nasdaq chain API returned rows but carries no IV field. IV levels therefore from CBOE delayed quotes — exchange-direct, 15-min delayed — labeled fallback per source order (Yahoo → Nasdaq → fallback). (See Synthesis: Parity desk succeeded on Yahoo chain via crumb flow — try that first next run.)

**Critical catch on iv-inputs [FACT]:** its `atm_iv` values are **0DTE** (`iv_dte: 0`, expiry 2026-10-14) — e.g., TSLA 3.2% vs 30.9% realized, an end-of-day 0DTE artifact. NOT comparable to term IVs; NOT used as IV levels. Only `realized_20d`, `max_single_day_variance_share`, `window_contingent` taken from it.

### Stale-jump screen (verified from 2026-10-14 file; realized window 2026-09-16 to 2026-10-13 — STALE, ends two sessions ago)

| Symbol | Realized 20d (STALE) | Max single-day variance share | Window-contingent? | Consequence |
|---|---|---|---|---|
| SPY | 9.49% | 0.336 | **YES** | IV-vs-realized verdict WINDOW-CONTINGENT |
| QQQ | 15.64% | 0.424 | **YES** | WINDOW-CONTINGENT |
| AAPL | 17.24% | 0.336 | **YES** | WINDOW-CONTINGENT |
| MSFT | 20.06% | 0.377 | **YES** | WINDOW-CONTINGENT |
| NVDA | 22.78% | 0.227 | No | Clean window — verdict stands on its own terms |
| TSLA | 30.86% | 0.299 | No (just under) | Clean window, borderline — one day away from contingent |

### Live ATM IV term structure (CBOE delayed, ~13:27 PT) — FACT

ATM IV = mean of call/put IV at strike nearest spot. Spot from Yahoo chart at close.

| Symbol | Spot | 1 DTE (10-16) | ~1 wk | ~2 wk | ~29 DTE (11-13) | Shape |
|---|---|---|---|---|---|---|
| SPY | $771.79 | 12.95% | 10.61% (7d) | 12.21% (14d) | 12.84% | Flat-to-gently-upward beyond 1-wk dip |
| QQQ | $728.00 | 22.03% | 18.50% (7d) | 19.78% (14d) | 20.11% | Same pattern as SPY |
| AAPL | $342.00 | 30.74% | 23.19% (6d) | 23.36% (13d) | **27.35%** | Hump at 29d — contains Nov 2 earnings |
| MSFT | $539.44 | 24.86% | 21.79% (6d) | **36.65%** (15d, 10-30) | 31.14% | Large hump at Oct 30 — contains Oct 28 earnings |
| NVDA | $217.23 | 48.53% | 36.89% (6d) | 34.47% (13d) | 34.99% | Downward slope; no hump in window |
| TSLA | $362.44 | **69.12%** | 63.04% (8d) | 54.51% (13d) | 45.67% | Steep backwardation; front loaded with Oct 21 earnings |

**Parity sanity check [FACT]:** ATM call/put IVs agree to ≤0.008 for every expiry except AAPL Oct 28 (call 24.88% vs put 21.85%, gap 0.030) — that expiry is thin (OI 27 calls / 113 puts), so the gap reads as wide/illiquid market, not parity violation. Deterministic put-call parity shows no actionable violation; where quotes are thin, the math is not the problem — the market is.

**Straddle-implied moves (INFERENCE from CBOE mids, 15-min delayed):** 1-day ATM straddle ≈ 0.54% of spot (SPY), 0.93% (QQQ), 1.29% (AAPL), 1.05% (MSFT), 2.04% (NVDA), 2.92% (TSLA). 29-day ≈ 2.93% (SPY), 4.56% (QQQ), 6.18% (AAPL), 7.03% (MSFT), 7.95% (NVDA), 10.28% (TSLA). MSFT Oct 30 ≈ 5.96% (earnings-loaded); TSLA Oct 28 ≈ 8.21% (earnings-loaded). Market-implied breakevens for long premium, not forecasts.

### IV vs realized (indicative only — horizon mismatch + stale realized)

| Symbol | ~29d IV (live) | 20d realized (STALE, ends 10-13) | Read |
|---|---|---|---|
| SPY | 12.84% | 9.49% | IV > realized — **WINDOW-CONTINGENT** |
| QQQ | 20.11% | 15.64% | IV > realized — **WINDOW-CONTINGENT** |
| AAPL | 27.35% | 17.24% | IV > realized — **WINDOW-CONTINGENT**; 29d expiry contains earnings, so elevation is expected, not "rich" |
| MSFT | 31.14% | 20.06% | IV > realized — **WINDOW-CONTINGENT**; 29d expiry contains earnings |
| NVDA | 34.99% | 22.78% | IV > realized, clean window — Nov 13 expiry does NOT contain NVDA earnings, so not earnings-inflated |
| TSLA | 45.67% | 30.86% | IV > realized, clean window (borderline 29.9%); front expiries contain earnings |

**IV rank: UNVERIFIED for all six** — no free source provides IV history (Yahoo options 401; Nasdaq chain has no IV; CBOE delayed quotes are point-in-time). No "elevated IV rank" flag issued. Any rank claim would be a guess.

### Earnings inside the window (FACT unless noted)

| Symbol | Next earnings | In which pulled expiry? | Premium read |
|---|---|---|---|
| SPY / QQQ | None (ETFs) | — | No event premium; flat structures consistent |
| TSLA | **Wed Oct 21, after close** (Tesla IR via BusinessWire) | Oct 23 (8 DTE) and longer | ⚠️ **AVOID premium into this binary event** — front IV 69% event-loaded |
| MSFT | **Wed Oct 28, after close** (Microsoft announcement) | Oct 30 (15 DTE) and Nov 13 | ⚠️ **AVOID** — Oct 30 hump (36.7%) is the event premium |
| AAPL | **Mon Nov 2, after close** (Apple IR via MacRumors/AppleInsider) | Nov 13 (29 DTE) only | ⚠️ **AVOID** for Nov 13 expiry — 27.4% vs 23.4% at 13 DTE is the event hump |
| NVDA | **DISPUTED — UNVERIFIED:** MarketBeat Nov 18 estimated (unconfirmed); TipRanks Nov 25. Both beyond Nov 13 expiry pulled | None pulled | No event premium in pulled expiries; Dec-expiry pull needed to see NVDA hump |

**What would change these verdicts:** an IV-history source (even 1-year) would convert IV rank from UNVERIFIED to a real call; a fresh realized window without single-day dominance would convert the four WINDOW-CONTINGENT verdicts to clean calls; NVDA date resolution + Dec-expiry pull; post-earnings IV crush observations (TSLA Oct 22, MSFT Oct 29).

Sources: iv-inputs file (as_of above); CBOE delayed quotes https://cdn.cboe.com/api/global/delayed_quotes/options/SPY.json (same pattern others); Yahoo chart https://query1.finance.yahoo.com/v8/finance/chart/SPY ; MSFT https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; TSLA https://www.morningstar.com/news/business-wire/20261002169209/tesla-third-quarter-2026-production-deliveries-deployments ; AAPL https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/ ; NVDA (conflicting) https://www.marketbeat.com/stocks/NASDAQ/NVDA/earnings/ vs https://www.tipranks.com/stocks/nvda/earnings

---

## Desk 4 — Open Quant / AI Model Lab

**Question:** What is genuinely new since the 2026-10-14 sweep that the desks can use?

**Verdict:** One strong new TEST candidate (#71, stale-information IV forecasting with full replication code), one new WATCH at the band floor (#73, Bayesian regime detection), five ARCHIVEs on band discipline. No INTEGRATE-ready candidate; scorer max was 75. No disposition changes to existing ledger items.

**Sweep coverage [FACT]:** arXiv q-fin.* submitted 2026-10-13–15 (15 papers, all screened); GitHub created:>2026-10-13 across volatility/options/implied-volatility/earnings-drift/dividend-forecast/purged-walk-forward legs; Semantic Scholar leg returned cleanly but without a date filter surfaces 2024–2025 papers, so arXiv + GitHub carried the new-item sweep. Ledger #1–#70 checked first — nothing below is a re-report.

| # | Candidate | Score / Disp. | Evidence |
|---|---|---|---|
| 71 | **SunnyAlexV/delayed-information-cross-section** — "Breadth, Implied Volatility, and Forecasting with Stale Information" + "Why a Simple Threshold Rule Is Hard to Beat" (working papers + full replication code) — https://github.com/SunnyAlexV/delayed-information-cross-section | **75 / TEST** | MIT LICENSE verified from raw file (GitHub API `NOASSERTION` was a detection quirk). README + 26 labs (lab08_implied_vol, lab04_walkforward, lab16_clark_west_shrinkage) + data/ (MANIFEST.tsv, CONVENTIONS.tsv) + verify_*.py / selftest.py / run_all.py + results_registry.tsv — all read at source. Headline claims (FACT per README, code NOT run): 4,862 OOS days 2007–2026; domestic-only R² 0.499→<0 as delay δ→11wk; +7 foreign closes holds R² at 0.347 (71% [54,83] of loss recovered); VIX+VDAX recover *more* than all of it — 3-weeks-stale + IV beats fully-current domestic-only; given IV, foreign block adds nothing at any delay. Working papers, NOT peer-reviewed → credibility capped at 3. **Relevance:** directly supports premium desk's IV-as-forecaster read and stale-data discipline (complements stale-jump screen). **What would change it:** sandbox run of selftest.py + verify scripts reproducing δ-curve and IV-dominance headline → strengthens toward INTEGRATE-eligibility; failure to reproduce → demote. |
| 72 | **BeTINN** — Structured Conditional Neural Solvers for Parametric SV Pricing (arXiv:2610.19254v1, 14 Oct 2026) — https://arxiv.org/abs/2610.19254 | **42 / ARCHIVE** | Abstract read at source. PINN-style structured conditional solver on Heston PDE; improved joint accuracy on option value + Greeks vs baselines (source-reported, UNVERIFIED). No code link → reproducibility not established. Below 45 WATCH band. |
| 73 | **Regime Detection in Latent Factor Models — A Bayesian Decision-Theoretic Approach** (arXiv:2610.20366v1, 14 Oct 2026) — https://arxiv.org/abs/2610.20366 | **45 / WATCH** | Abstract read at source. Online regime detection as Bayesian decision problem (false alarms vs detection delay vs misclassification); particle-filter + Monte Carlo DP; single-change-point Heston benchmark. No code link → reproducibility not established. At WATCH band floor; Heston-benchmark tie is the desk relevance (vol-regime lane). **What would change it:** code release or journal status. |
| 74 | **Interior smoothness and zero-variance geometry for finite-maturity Heston American puts** (arXiv:2610.20000v1, 14 Oct 2026) — https://arxiv.org/abs/2610.20000 | **33 / ARCHIVE** | Abstract read at source. Pure boundary-regularity theory (smooth fit fails in variance direction at axis; continuation premium O(variance)). No empirical results, no code link. Below band; no desk procedure. |
| 75 | **Common Signals, Spurious Cross-Excitation, and Identification in Multivariate Hawkes Processes** (arXiv:2610.19428v1, 14 Oct 2026) — https://arxiv.org/abs/2610.19428 | **39 / ARCHIVE** | Abstract read at source. Latent common signals generate spurious excitation; second-order non-identification; third-order cumulants identify structure (source-reported). Microstructure-identification theory; no desk data or procedure; no code link. Below band. |
| 76 | **Data-Driven Dynamic Portfolio Selection with Vine Copula Simulation and Reinforcement Learning** (arXiv:2610.20037v1, 14 Oct 2026) — https://arxiv.org/abs/2610.20037 | **28 / ARCHIVE** | Abstract read at source. CRRA + CVaR-penalized dynamic portfolio policy via vine-copula scenarios. Portfolio optimization; no vol/options/earnings/dividend transfer; no code link. |
| 77 | **sdgrrao/options-book-validation** — pricing, hedging, validating a European options book — https://github.com/sdgrrao/options-book-validation | **31 / ARCHIVE** | Scaffold, not a package (verified at source): src/book/ holds only `__init__.py`; tests/test_setup.py is trivial env check (norm.cdf(0)=0.5); notebooks/ holds only .gitkeep; README 2 lines. MIT verified. No evidence of working pricer/hedger/validator. Reopen if built (real pricers + non-trivial tests). |

**Re-checks on existing items (no disposition changes):** License line-stops hold — #1 (ilyamirin harness), #32 (Derivatives-Pricing-Risk-Engine), #20 (Universal-Diffusion-for-IVS), repos untouched since Aug/Sep, still no LICENSE. Code still absent: #4 (M2VN) — GitHub search returned 1 hit, but it is a **name collision**: `Yoontae6719/M2VN-Multi-Modal-Learning-Network-for-Volatility-Forecasting`, a different model, NOLICENSE — not the Oxford/Deutsche Bank narrative-semantics M2VN's code. #35 (VolPaint) — GitHub search 0 hits. #37 (holdout): PyPI `holdout` still v0.3.0 with same collision summary ("Preserve the dissenting reasoning behind contested decisions") — not the author's release. Activity notes only: #54 pushed 2026-10-14, #55 pushed 2026-10-15, #56 pushed 2026-10-15 — no disposition change.

**Triage exclusions (no ledger rows):** All other GitHub hits NOLICENSE (incl. shuyangliu0827/ml-implied-volatility, aidaman01/implied-distribution, Hylex850/Selling_earnings_volatility, JoBi246/earnings-drift, purged-WF NOLICENSE hits); Drallas/Dividend-Compass (AGPL-3.0 retail dividend-fund tax calculator — scope mismatch); dorahborgi/fx-functional-factor-model (MIT but FX MSc thesis — scope mismatch); crypto/live-trading scope (MONEYCAPSLOCK, polymarket-btc-5min bot).

**Follow-ups:** Sandbox #71 (TEST): run selftest.py + verify scripts; reproduce δ-curve + IV-dominance headline on bundled data; port the "stale domestic + current IV" forecaster check to the premium desk's IV screen. Re-check #73 next cycle: code release? journal status?

**Ledger confirmation:** All seven new candidates (#71–#77) appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md`, plus a dated 2026-10-15 Jidoka-log entry recording scoring, triage exclusions, re-checks, and the M2VN name-collision trap. One self-correction: the Jidoka entry initially landed in the older log section; moved to the current Jidoka log and verified in place. No candidate lives only in this daily file.

---

## Desk 5 — Weather / War / Logistics Futures Events

**Question:** What fresh catalysts (USDA, EIA, geopolitical/logistics) hit in the last ~48 hours, and what do the relevant futures curves appear to be pricing?

**Verdict:** This week's two big federal energy releases both landed **today, Thu Oct 15** — not Wed Oct 14 as the brief assumed (Columbus Day holiday delay) — and both surprised toward physical tightness in oil and gas: EIA petroleum showed a large −8.6M bbl crude draw vs a small expected build, and EIA natural gas printed a below-average +67 Bcf injection. Yet crude futures *fell* on the day despite two more vessel sinkings near the Strait of Hormuz — the market is pricing demand destruction and the IEA's weaker demand outlook as outweighing near-term supply disruption (INFERENCE). Grains still digesting the bearish Oct 9 WASDE (record corn crop), harvest running behind average pace. No fresh catalyst maps directly to any single watchlist name today.

### ⚠️ Timing correction (FACT, verified across multiple sources)
- EIA Weekly Petroleum Status Report and EIA Natural Gas Storage Report were **delayed from Wed Oct 14 to Thu Oct 15 by the Oct 12 Columbus Day federal holiday** (FXEmpire pre-release note; DTN confirms the same holiday delayed USDA Crop Progress to Tue Oct 13). The brief's "Wed Oct 14, 10:30 ET" timing was wrong this week. EIA petroleum released Thu ~noon ET (per FXEmpire); gas storage Thu morning ET.
- This does **not** change the standing government-data rule: federal releases remain on schedule, no shutdown/blackout framing applies.

### 1. EIA Weekly Petroleum Status Report — week ended Oct 9, released Thu Oct 15
All figures as reported by WSJ / OilPrice / Seeking Alpha / Barchart from the EIA release (secondary reports; EIA primary PDF not directly pulled — see caveats).

| Item | Reported | vs. expectation |
|---|---|---|
| Commercial crude stocks (ex-SPR) | −8.6M bbl to 415.6M bbl | WSJ survey: +0.1M build; Seeking Alpha consensus: +0.2M build — **large downside surprise** |
| Cushing (WTI delivery hub) | +1.86–1.9M bbl to 26.6M bbl | 5-month high (Barchart) |
| SPR | Unchanged at 283M bbl | — |
| Gasoline stocks | +3.5M bbl to 208.3M bbl | Expected −0.9M draw — **opposite-direction surprise** |
| Distillate stocks | −2.5M bbl | Expected −1.7M — larger draw |
| U.S. crude production | 13.7M bpd, −0.3M bpd w/w | WSJ attributes dip to Gulf platform evacuations ahead of Hurricane Isaias, >70% offshore output shut in by Fri, mostly restored by Wed (single-source attribution) |
| Refinery utilization / inputs | 93.5% (from 92.7%); inputs 16.6M bpd (+0.135M) | WSJ survey had expected runs −0.5 pp |
| Crude imports / exports | Imports 6.0M bpd (−0.79M); exports 4.6M bpd (−0.195M) | — |
| Total products supplied (demand proxy) | 21.1M bpd, 4-wk avg, +2% y/y | OilPrice |
| Gasoline demand | 8.7M bpd (4-wk avg, OilPrice) vs 8.4M bpd, −0.362M (WSJ) | Two sources, different measures — do not blend |
| Distillate demand | 4.0M bpd, 4-wk avg, −0.2% y/y | OilPrice |

**⚠️ Direct conflict, unresolved (UNVERIFIED):** OilPrice reports crude stocks "3% **above** the five-year average"; WSJ reports "about 3% **below** the five-year average." Both cannot be right. OilPrice also reports distillates 12% below the five-year average; WSJ reports gasoline 4% below. Do not cite a five-year-average comparison until the EIA primary text is checked.
**Context [FACT]:** API pre-report estimate (Tue) was an −11.12M bbl crude draw — same direction, larger magnitude. Prior week (ended Oct 2): crude −3.2M bbl to 424.1M (FXEmpire pre-release); −8.6M chains consistently: 424.1 − 8.6 ≈ 415.5 ≈ 415.6 reported.

### 2. EIA Weekly Natural Gas Storage — week ended Oct 9, released Thu Oct 15
| Item | Reported |
|---|---|
| Injection | +67 Bcf |
| vs. expectation / normal | WSJ survey: 75 Bcf; 5-yr avg: 90 Bcf — **below both** |
| Working gas in storage | 3,567 Bcf |
| Surplus vs. 5-yr avg | +45 Bcf (narrowed from +68 Bcf prior week) |
| vs. year-ago | −143 Bcf deficit (widened from −130 Bcf) |
| Front-month futures reaction | Nov settled +1.2% at $3.236/MMBtu (WSJ) |

Supporting facts: LNG feedgas ~19.7 Bcf/d Wed, +9.6% w/w (BNEF via FXEmpire); European gas storage 74% full vs 89% 5-yr seasonal avg (BNEF via FXEmpire); TCO pipeline outage limiting future builds (FXEmpire/NGI). **Conflict (UNVERIFIED):** EIA end-October storage forecast reported as 3,850 Bcf (~2% above norm) by one outlet and 3,985 Bcf (highest in 10 years, 5% above avg) by another — do not cite either until checked against EIA primary. Weather-model split for 6–15 day window (ECMWF much colder than GFS) reported only via Price Group blog — weak single source, UNVERIFIED.

### 3. IEA Oil Market Report — released Wed Oct 14 (FACT, multi-source)
| Item | IEA October report |
|---|---|
| 2026 global oil demand | −2.6M bpd to 102.4M bpd (deepened from −2.5M in Sept) |
| 2027 demand recovery | +2.0M bpd (cut from +2.6M); leaves 2027 ~620k bpd / 0.6% **below** 2025 |
| Diesel share of 2026 drop | ~25% |
| 4Q26 demand | −2.5M bpd y/y |
| Sept global supply | +2.5M bpd m/m to 102.3M bpd (OPEC+ +2.1M, led by Saudi Arabia) |
| Gulf crude exports, Sept | +4.4M bpd to 13.9M bpd, >75% of pre-war levels |
| 2026 supply / 2027 supply | 2026: −5.8M to 100.7M bpd; 2027: +7.7M bpd (recovery "fragile") |
| Observed global inventories | −10M bbl in Sept; −509M bbl vs end-Feb; on-land stocks lowest since at least 2016 |
| Refinery runs | Seasonal low 81.3M bpd in Oct, rebounding to 84.6M bpd by year-end |
| OPEC Oct report (contrast) | 2026: **+0.18M** bpd (vs IEA −2.6M — a ~2.8M bpd gap); 2027: +2.55M bpd |

IEA emergency stocks (single weaker source, Political.org — reported, not confirmed): total release to **exceed** the 400M bbl pledged Mar 11; ~330M bbl tapped so far; ~100M bbl remaining incl. >20M bbl diesel to be delivered "as soon as possible"; members still hold ~1.1B bbl public emergency stocks incl. >200M bbl diesel (as of Oct 7 statement).

### 4. Geopolitics / shipping — Strait of Hormuz and Middle East
- **Two vessels sunk near the Strait of Hormuz within ~24h** (FACT, multi-source): a container ship and a dry-bulk carrier struck by projectiles; WSJ via Morningstar identifies them as two Emirati cargo ships; UKMTO issued warnings on two container ships struck while transiting the Strait. First such sinkings in months (Morningstar/Dow Jones).
- **Houthi missile strike on an Aramco building in Dhahran, eastern Saudi Arabia, late Oct 13** (FACT as reported, single-chain): limited fire, no casualties per Saudi authorities (via The Financial Economy). Iran stated it is adopting new tactics against Strait shipping in response to a U.S. port blockade and tougher September sanctions (via Energy Tribune).
- **≥12 tanker attacks Sep 28–Oct 5** around the Strait (SAAFF/BUSA Cargo Movement Update No. 302, via Africa Ports). War-risk insurance premiums, tanker freight rates, and fuel-price volatility remain elevated (same source).
- **U.S. sanctions-easing under consideration** (reported by two secondary outlets, unconfirmed policy): easing restrictions on certain "shadow fleet" vessels to move more petroleum and cut shipping costs. INFERENCE: the offsetting force markets are weighing against the attacks.
- **Reported U.S. strike plans incl. GBU-43/B ("MOAB") against Iranian energy/nuclear sites** (CNN via Price Group blog): weak second-hand chain — **SPECULATION/UNVERIFIED**. Do not treat as fact; do not trade on it.
- **Market reaction (FACT + INFERENCE):** Brent fell ~1.3–1.8% Thu to ~$104–105; WTI ~$94–97, reversing Wednesday's gains to a three-week high. Falling prices into escalating attacks + a big U.S. crude draw = market pricing demand weakness and the IEA downgrade as dominant over physical disruption risk (INFERENCE). Brent still up >70% YTD per Bloomberg via Moneyweb. What would change this read: a sustained, measured cut in Gulf/Strait throughput (not just higher tanker costs), or a verified U.S. sanctions-easing decision.

### 5. USDA — no new major release today; Oct 9 WASDE still operative
- **Oct 9 WASDE (FACT, multi-source):** Corn yield raised to **181.2 bpa** (+2.7 vs Sept 178.5; trade expected ~177.6); production **16.034B bu**; ending stocks **1.849B bu** (+282M); season-avg price cut $0.10 to **$4.70/bu**. Soybean yield 53.1 bpa (from 52.8); production 4.562B bu; ending stocks 315M bu (from 310M); price unchanged at **$12/bu**. Corn futures fell ~5% on the report (Pro Farmer).
- **Nebraska controversy (FACT that scrutiny exists; cause UNVERIFIED):** USDA raised Nebraska corn yield +11 bpa to 188 bpa; Sept sample reportedly ~90% non-irrigated / 10% irrigated vs typical ~55/45 split in Oct. Farmers/analysts questioning the swing (Pro Farmer). Do not assert sampling error — mechanism alleged, not established.
- **Crop Progress, Tue Oct 13 (delayed from Mon by Columbus Day; week ended Oct 11; FACT via DTN/IndexBox):** Corn harvested **33%** (5-yr avg 39%); soybeans **46%** (avg 50%); winter wheat planted **51%** (7 pts behind avg). Corn maturity 91% (= avg); corn good/excellent 56% (+2 pp w/w); soy good/excellent 57% (unchanged). Iowa lagging hardest: corn 14% (20 pts behind avg), soy 31% (28 pts behind).
- **USDA flash sale (FACT, Dow Jones via Morningstar):** 470,000 MT U.S. soybeans sold to China for 2026/27 delivery — first flash sale to China in ~3 weeks. INFERENCE: Chinese buyers stepping in after the WASDE-driven price drop — consistent with, but not proof of, price-sensitive buying.
- Today: only routine daily reports (e.g., USDA morning hog report) — nothing material to futures.

### 6. Futures snapshot — Yahoo Finance, pulled ~13:30 PT Thu Oct 15 (continuous front-month contracts)
| Contract | Last | 5-session closes (oldest→newest, as reported) | Read |
|---|---|---|---|
| WTI crude CL=F | $96.17 | 93.74, 94.14, 95.09, 96.17 | Up ~2.6% over the window despite Thu dip |
| Brent BZ=F | $105.82 | 106.65, 105.69, 106.06, 105.82 | Flat-to-down; **Brent–WTI spread $9.65** (computed) |
| Nat gas NG=F | $3.237 | 3.17, 3.28, 3.20, 3.24 | Firming into heating season + tight storage print |
| Corn ZC=F | 478.25¢ | 483.00, 482.75, 480.75, 478.25 | Drifting lower post-WASDE — big-crop pressure |
| Wheat ZW=F | 669.25¢ | 672.25, 669.25, 673.25, 669.25 | Flat; slow winter-wheat planting not yet moving price |
| Soybeans ZS=F | 1264.25¢ | 1287.75, 1283.75, 1277.25, 1264.25 | Down ~1.8% over window despite China sale |
| Gold GC=F | $4,191.60 | 4190.60, 4177.30, 4107.90, 4191.60 | Near highs — safe-haven bid intact |
| Silver SI=F | $57.56 | 60.14, 59.16, 55.55, 57.56 | Volatile, off recent highs |
| Copper HG=F | $6.566 | 6.70, 6.68, 6.61, 6.57 | Softening from 52-wk-high area (52-wk high 6.83) |
| Live cattle LE=F | 227.20¢ | 224.75, 224.62, 223.90, 227.20 | Steady; consistent with WASDE's tight beef outlook |
| Lean hogs HE=F | 66.625¢ | 75.60, 75.60, 75.55, **66.62** | ⚠️ Apparent one-day −12% move almost certainly a **contract roll**, NOT a market crash — UNVERIFIED, do not interpret |

**Container shipping (FACT, SAAFF/BUSA via Africa Ports):** Drewry World Container Index $4,434/40ft (−0.8% w/w); Asia–Europe rates down >60% since July despite Asian port congestion; ~200,000 TEU new capacity entered service in Sept; fleet growth outpacing demand in TEU-miles. INFERENCE: container freight is a softening cost input even as tanker/war-risk costs stay elevated — a two-track freight market.

### 7. Watchlist read-through
**None of today's catalysts maps directly to SPY, QQQ, AAPL, MSFT, NVDA, or TSLA as a single-name event.** Transmission is macro: (a) diesel tightness + elevated war-risk freight = persistent logistics/cost pressure; (b) Brent >$100 with demand falling = stagflation-flavored backdrop pressuring growth multiples via higher discount rates and margin squeeze (INFERENCE, consistent with rates desk framing); (c) softening container rates partially offset tanker costs for goods importers (INFERENCE). No earnings, dividend, or single-name catalyst arises from this desk today.

### Verdicts (each with what would change it)
1. **Oil: physically tight, demand-weakening, geopolitically fragile.** EIA draw + IEA inventory data say barrels are scarce; IEA demand cuts say scarcity is destroying consumption. What would change it: EIA primary text resolving the five-year-average conflict; a measured Gulf export cut; verified sanctions-easing decision.
2. **Diesel/distillate is the tightest leg** — EIA distillate draw beat expectations, IEA sees no restocking before 2H27, emergency diesel releases being accelerated. What would change it: sustained distillate build + refinery-run recovery above the 84.6M bpd year-end path.
3. **Grains: big-crop overhang dominates; harvest pace is a secondary watch.** WASDE's corn surprise still sets the tone; slow harvest (esp. Iowa) is timing friction, not yet supply loss. What would change it: harvest falling further behind with adverse weather, or a November WASDE revision to the Nebraska yield.
4. **Nat gas: tightening at the margin into winter, but not a squeeze** — below-average injections narrowing the surplus, LNG pull strong, yet storage remains above the five-year average. What would change it: a cold-verifying NOAA seasonal outlook or a sub-60 Bcf print next week.

### Caveats
- EIA figures from secondary reports (WSJ, OilPrice, Barchart, Seeking Alpha, NGI), **not** the EIA primary release text — five-year-average conflict and end-Oct gas storage forecast conflict (3,850 vs 3,985 Bcf) flagged UNVERIFIED pending primary-source check.
- "Hurricane Isaias" attribution for the Gulf production dip rests on WSJ's report (corroborated only by a trading blog) — single-chain attribution, not independently verified.
- IEA emergency-release totals rest on one weaker outlet (Political.org); IEA demand/supply numbers are multi-source and consistent.
- HE=F's apparent plunge treated as likely contract roll, not a price move — not checked against CME contract specs.

Sources: EIA petroleum https://oilprice.com/Energy/Crude-Oil/EIA-Says-US-Crude-Inventories-Down-Nearly-9-Million-Barrels.html ; https://www.wsj.com/business/energy-oil/u-s-crude-oil-stockpiles-post-large-weekly-drop-0a988c08 ; https://seekingalpha.com/news/4652954-crude-inventory-falls-by-86m-barrels-for-the-week-ended-october-9-eia ; EIA gas https://naturalgasintel.com/news/following-bullish-storage-print-natural-gas-futures-sustain-rally/ ; IEA OMR https://www.ttnews.com/articles/iea-lowers-world-oil-demand ; Hormuz https://www.morningstar.com/news/dow-jones/202610156756/oil-prices-mixed-as-traders-weigh-demand-outlook-hormuz-shipping-risks-2nd-update ; USDA https://www.profarmer.com/news/agriculture-news/nebraska-yield-jump-stirs-controversy-after-usdas-october-wasde-surprise ; https://www.dtnpf.com/agriculture/web/ag/crops/article/2026/10/13/usda-crop-progress-corn-33-harvested ; Futures quotes: Yahoo Finance chart API, UA header, pulled ~13:30 PT Thu Oct 15, 2026.

---

## Desk 6 — Box / Parity Observer

**Question:** Any new index-methodology change or published parity-violation evidence affecting the watchlist?

**Verdict:** Nothing material and new today. No new index-methodology document affecting SPY/QQQ constituents or settlement found; no published parity-violation analysis for the watchlist found. Live SPY put-call/box parity spot-check on the Oct-15 (0DTE) chain shows box parity holding exactly and put-call parity within $0.14 of textbook level across near-ATM strikes — consistent with quote timing/rate/dividend frictions, not a violation. No parity-based edge claimed.

### Index methodology / constituent news

| Item | Status | Relevance |
|---|---|---|
| S&P DJI change to S&P/TSX Canadian indices eligibility (foreign issuers with material Canadian connection; effective Dec 21, 2026) | **FACT** — announced Sept 11–13, 2026, after July consultation; not new today | None to SPY/QQQ/watchlist — Canadian benchmarks only |
| Nasdaq-100 constituent change: Moderna (MRNA) replaced Warner Bros. Discovery (WBD), effective Oct 9, 2026 | **FACT** — routine replacement under existing methodology, already effective | Indirect: QQQ tracks Nasdaq-100; no methodology change, no watchlist name added/removed |
| Nasdaq index terminations effective after close Oct 29, 2026 (NASDAQ OMX Iceland Benchmark Bonds / inflation-linked) | **FACT** — Nasdaq Trader notice | None to watchlist |
| Nasdaq-100 methodology update (Fast Entry, full-market-cap ranking incl. unlisted shares, quarterly rank-based review) | **FACT** — methodology update published ~70 days ago (Aug 2026); not new | Background only: governs how future large listings enter NDX/QQQ; no watchlist impact today |
| Cboe × S&P DJI: exclusive SPX options license extended through 2051 (announced Sept 29, 2026); royalty terms unchanged through 2026, reset in 2027 described as minimal/de minimis | **FACT** — announced Sept 29, 2026; not new today | Background only: SPX options franchise continuity confirmed; no settlement or methodology change announced |

**No new S&P 500 or Nasdaq-100 methodology document published in the last several days.** **[INFERENCE]** Absence in this sweep means no methodology-driven rebalance or settlement change needs pricing into parity work today — a sweep result, not proof no obscure notice exists.

### Published parity-violation analysis
**None found for the watchlist in the current sweep. [FACT — sweep result, as of ~13:35 PT Oct 15, 2026]** Closest recent published parity reference: Summa Money options brief dated Oct 1, 2026, which reported put-call-parity-implied VIX futures forwards within $0.16 of feed values — i.e., no violation, 14 days old; not a watchlist single-name parity study. Retail options-outlook pieces surveyed (Oct 10) discuss skew, put/call ratios, expected moves — none report a put-call or box parity violation.

### Live parity spot-check — SPY Oct-15 (0DTE) chain
**Method (deterministic math outranks models):** Put-call parity: C − P = S − PV(K) − PV(dividends). Box parity: (C₁ − P₁) − (C₂ − P₂) = PV(K₂ − K₁), which cancels S, rates, dividends — the cleaner test.
**Data [FACT]:** Yahoo Finance options chain, fetched with browser UA header + crumb session (first crumb-less attempt returned "Invalid Crumb" — retried via standard cookie/crumb flow and succeeded). Underlying SPY $771.79, Yahoo `regularMarketTime` 2026-10-15T20:00:00Z (= 13:00 PDT, during market hours). Expiry 2026-10-15 (0DTE). Quotes mid bid/ask; spreads $0.01–$0.04 on strikes checked.

| Strike | Call mid (bid/ask) | Put mid (bid/ask) | C − P | S − K | (C−P) − (S−K) |
|---|---|---|---|---|---|
| 771 | $0.74 ($0.74/$0.75) | $0.10 ($0.09/$0.10) | $0.65 | $0.79 | −$0.14 |
| 772 | $0.17 ($0.16/$0.17) | $0.52 ($0.51/$0.52) | −$0.35 | −$0.21 | −$0.14 |
| 773 | $0.04 ($0.03/$0.04) | $1.38 ($1.36/$1.40) | −$1.34 | −$1.21 | −$0.13 |

**Box check (strikes 771/772):** (C₇₇₁ − P₇₇₁) − (C₇₇₂ − P₇₇₂) = $1.00 vs strike width $1.00 → difference **$0.00**. **[FACT — computed from chain above]**
**Interpretation:** Uniform −$0.13/−$0.14 put-call gap across strikes is a level shift, not strike-specific mispricing. **[INFERENCE]** On same-day expiry, PV(K) ≈ K and PV(dividends) ≈ 0, so the residual is most plausibly quote-timing, 0DTE settlement convention, or small rate/dividend term — not an executable violation. Box holding to the penny is decisive: it strips out S, rates, dividends, shows no arbitrage. Per the desk rule, the math wins: no parity violation established. −$0.14 magnitude in line with the Oct-1 published observation (parity-implied forwards within $0.16 of feeds). **[FACT — comparison of two observations]**
**What would change this verdict:** a box deviation materially larger than combined bid/ask spread on simultaneously timestamped live quotes; a published, sourced parity-violation study on a watchlist name; a new S&P/Nasdaq/Cboe methodology or settlement notice.

**Gaps:** Single-name parity (AAPL, MSFT, NVDA, TSLA) was **not** chain-checked this run — SPY only, per light-touch mandate. Single-name parity status is therefore **UNVERIFIED**, not "clean." Methodology sweep covers public web search as of ~13:35 PT Oct 15; an exchange notice published after that time would not be captured (UNVERIFIED beyond sweep timestamp).

**Desk line: Box/Parity Observer: nothing material — no new index-methodology doc, no published parity violation; live SPY box parity holds exactly ($0.00 deviation), put-call gap −$0.14 uniform = friction, not arbitrage. Single-name parity UNVERIFIED (not checked this run).**

Sources: S&P/TSX change https://ktwb.com/2026/09/13/sp-dow-jones-indices-loosens-canadian-index-inclusion-criteria/ ; Moderna/WBD https://newsnationonline.com/news/moderna-nasdaq-100-october-9-warner-bros-discovery/ ; Nasdaq terminations https://www.nasdaqtrader.com/tradernews.aspx?id=fpnews2026-67 ; Nasdaq-100 methodology https://www.nasdaq.com/newsroom/nasdaq100-index-methodology-update-why-now ; Cboe/S&P DJI https://dailymirror.co.za/2026/09/29/cboe-extends-sp-500-options-agreement-through-2051-and-considers-tokenizing-contracts/ ; Summa Money https://summamoney.com/investing/the-daily/the-index-held-the-average-stock-did-not-options-brief-1-october-2026/

---

## Desk 7 — Bonds & Rates

**Question:** What does the current rates environment imply for discount rates, growth multiples, and premium pricing for the watchlist?

**Verdict:** Rates remain elevated and the curve is upward-sloping but has flattened over the 60-day window (bear flattening: front end rose faster than long end). Funding markets show zero stress (SOFR = EFFR). For premium pricing, the directional read is mildly restrictive: a 5.19% 10Y keeps discount rates high, pressuring long-duration growth multiples (NVDA, TSLA, MSFT most exposed), while the flattening curve signals the market pricing less term premium than two months ago — not a recession-inversion signal, but a cooling of the steepening impulse. What would change this verdict: a 10Y move back above ~5.31% (Oct 5 window high) or a 2s10s inversion (slope < 0), flipping the read to outright restrictive / recession-warning respectively.

### Rates snapshot (all values from repo module `hedge_desk.rates_desk.rates_environment()`, mode `REAL_FRED_RATES`)

| Series | Level | As-of (FRED obs.) | Change |
|---|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 2026-10-14 | **+0.25 pp** over 60-day window (module-reported) |
| Treasury 2Y (DGS2) | **4.82%** | 2026-10-14 | +63 bp vs 4.19% on 2026-08-17 (computed from module history) |
| Treasury 10Y (DGS10) | **5.19%** | 2026-10-14 | +47 bp vs 4.72% on 2026-08-17 (computed from module history) |
| 2s10s slope (10Y − 2Y) | **+37 bp** | 2026-10-14 | **Flattened ~16 bp** vs +53 bp on 2026-08-17 (computed from module history) |
| Curve shape (module) | **UPWARD_SLOPING** | 2026-10-14 | — |
| SOFR | **3.88%** | 2026-10-14 | — |
| EFFR | **3.88%** | 2026-10-14 | — |
| OBFR | **3.88%** | 2026-10-14 | — |
| **SOFR − EFFR spread** | **0 bp** | 2026-10-14 | No funding stress |

Module run: Thu 2026-10-15 ~13:30 PT; module `as_of` = 2026-10-15; underlying FRED observations dated 2026-10-14 (latest available). Data source per module: `fred-public-csv-http-200`. Schema: `hedge-desk-rates-desk-1.0.0`. No Yahoo yields substituted; no numbers retyped from memory. Note: module's `curve_slope` field (0.046250) is a normalized ratio, not the bp spread; the +37 bp figure is the module's own `spread_10y_2y_points` and is the one used here.

### Evidence labels
- **FACT:** Fed funds effective 3.88% (2026-10-14), up 0.25 pp over the module's 60-day window — module output.
- **FACT:** 2Y 4.82%, 10Y 5.19% (2026-10-14); 2s10s +37 bp; curve upward-sloping — module output.
- **FACT:** SOFR, EFFR, OBFR all print 3.88% on 2026-10-14 — module output; SOFR−EFFR spread exactly 0 bp.
- **INFERENCE (from module history):** Curve flattened ~16 bp over the window (53 bp → 37 bp) because 2Y rose 63 bp while 10Y rose only 47 bp — bear flattening. Near-term (past week), 10Y eased from its 5.31% window high (Oct 5) to 5.19% while 2Y roughly flat (4.84% → 4.82%) — mild bull flattening at the margin.
- **INFERENCE:** Zero SOFR−EFFR spread = no measurable overnight funding stress; repo and unsecured funding pricing identically. Calm-funding read, not a guarantee — one day's observation.
- **INFERENCE (premium-pricing read):** 5.19% 10Y keeps discount rates elevated → continued pressure on long-duration growth multiples (NVDA, TSLA, MSFT, QQQ more than SPY). Flattening (front end rising faster than long end) argues against paying up for long-dated upside via premium; the curve is not compensating duration risk as richly as in August. Recent 12 bp pullback in 10Y from Oct 5 high is a small offset, not a regime change.
- **SPECULATION:** None offered. No forecast of Fed action, no recession call, no rate-path prediction.
- **UNVERIFIED:** Intraday 2026-10-15 moves — module's latest observations are 2026-10-14 closes; today's live yields not pulled (per desk brief, no Yahoo substitution).

**Disconfirming evidence checked:** Checked for inversion: slope +37 bp, still positive — no inversion. Checked for funding stress: SOFR−EFFR = 0 bp — none visible. Checked 10Y vs window high (5.31%, Oct 5): eased, not broken out. Not checked: intraday 10-15 yields, TIPS/breakevens, credit spreads — outside module output; marked UNVERIFIED rather than inferred.

**What would change the verdict:** 10Y closing back above ~5.31% (window high) → outright restrictive / renewed multiple pressure. 2s10s slope turning negative → inversion regime; growth-multiple and recession framing would change materially. SOFR−EFFR widening beyond ~5–10 bp → funding-stress flag; would override calm-funding read.

**Desk status: COMPLETE — module ran successfully, no fallback used.**

---

## Desk status summary

| Desk | Status | Note |
|---|---|---|
| 1 Earnings | COMPLETE | 2 in-window (TSLA 10/21, MSFT 10/28); NVDA date disputed |
| 2 Dividend | COMPLETE | Window empty; MSFT ex Nov 19 just outside |
| 3 Premium IV | COMPLETE | IV levels via labeled CBOE fallback (Yahoo options 401); IV rank UNVERIFIED; 4/6 WINDOW-CONTINGENT |
| 4 Quant Lab | COMPLETE | #71 TEST, #73 WATCH, 5 ARCHIVE; all appended to ledger |
| 5 Futures Events | COMPLETE | EIA Thu (holiday delay); IEA demand cut; Hormuz sinkings; WASDE still operative |
| 6 Box/Parity | COMPLETE | Nothing material; SPY box holds exactly; single-name parity UNVERIFIED |
| 7 Bonds & Rates | COMPLETE | FRED module ran; no fallback |

No desk FAILED. No desk silently dropped.
