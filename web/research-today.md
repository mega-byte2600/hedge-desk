# Hedge-Desk Daily Research Package — Wed 2026-10-07
Run: 1:30pm PT (4:30pm ET), post-close. Paper-only. Research & input only — no git, no pushes, no PRs, no code changes.

Standing rules honored this run: Yahoo-with-UA market data order; ^TNX = 10Y, ^FVX = 5Y (never 2Y); no federal "data blackout" framing (CR through Dec 11; EIA on schedule); MSFT dividend streak per the 2026-10-05 count standard (24); all material claims labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.

## Synthesis — the 5 most decision-relevant items (contradictions resolved)

1. **TSLA earnings Oct 21 is the week's watchlist binary.** Confirmed live on Nasdaq calendar today — this corrects the 10/28 date sitting in the 10/05–10/06 nightly files (PREMIUM FACT). Front-earnings-expiry implied move ±8.2% vs 6.0% mean-absolute realized reaction over the last four prints; the July −14.5% reaction shows tail skew. Premium not obviously cheap into the binary; 30DTE IV (43.6%) vs front weekly (30.9%) shows the classic earnings hump. Avoid selling the hump (PREMIUM INFERENCE; EARNINGS FACT on dates/move).
2. **The distillate deficit is the real energy tight spot.** EIA weekly released on schedule today 10:30 ET: crude −3.2M bbl to 424.1M (1% above 5-yr avg), but distillates flat at **12% below the 5-yr avg** into heating season; WSJ notes diesel near record highs. G7's 100M-bbl emergency release (incl. diesel) is the direct offset. What would change it: a distillate build next week or confirmed diesel SPR hitting the market (FUTURES FACT/INFERENCE).
3. **Rates: 10Y at 5.27% (+55bp in two months) keeps growth multiples under pressure.** Whole-curve parallel bear move; 2s10s flat at 48bp; SOFR–EFFR 2bp — funding calm. Read-across: QQQ/NVDA/TSLA/MSFT/AAPL carry the most duration exposure; long-dated growth-call premium should be treated as expensive until the 10Y confirms a top (back under ~5.00%). (RATES FACT/INFERENCE)
4. **Brent-WTI at $11.95 is historically wide — the geopolitical premium lives in seaborne Brent.** WTI $89.14, backwardation ~1%/mo; ME exports exceeded pre-war levels 4 of the last 7 Sept days while Aramco cut Asia OSPs by $3 — physical market less tight than Brent's $100+ handle implies. COT: WTI spec length washed out near the 10th percentile. VIX 15.08: premium is siloed in energy, no equity-vol spillover. (FUTURES FACT/INFERENCE)
5. **Premium desk: nothing elevated (no symbol above 55%ile IV-rank); NVDA at 0%ile is historically cheap but offers no seller's edge.** MSFT richest vs realized (33.2% vs 20.0%) but 55%ile is event-driven (earnings 11/4 in window), not a sell signal. AAPL/MSFT/TSLA verdicts are WINDOW-CONTINGENT (single day >30% of realized variance) + earnings inside the window = avoid. NVDA clean verdict: modestly rich vs realized at a 0%ile level. (PREMIUM FACT/INFERENCE)

---

## 1. Earnings Event desk

| Symbol | Report date | Timing | Implied move % (front-earnings expiry ATM straddle) | Historical avg earnings-day move | Sources |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21, 2026 | After market close; Q&A webcast 5:30pm ET | ±8.2% (Oct 23 expiry; K=375 straddle 30.80/377.81 = 8.15%; K=380 → 8.21%; avg 8.18%) | 6.0% mean absolute (last 4, reaction session; signed mean −4.81%) | Nasdaq calendar API; Yahoo options chain; Tesla IR guidance via metricshour; stocktwits/Goldman |
| AAPL | — (not in window) | — | — | — | Nasdaq calendar API 10-07→10-21: zero rows |
| MSFT | — (not in window) | — | — | — | Nasdaq calendar API 10-07→10-21: zero rows |
| NVDA | — (not in window) | — | — | — | Nasdaq calendar API 10-07→10-21: zero rows |
| SPY / QQQ | N/A — ETFs do not report earnings | — | — | — | structural fact |

- **TSLA (FACT on dates/move; INFERENCE on verdict):** Only watchlist name reporting in window. Implied ±8.2% prices the event at or above the recent 6.0% average realized reaction — premium not obviously cheap into this binary. Context: Q3 deliveries 486,532 beat company-compiled consensus (secondary, via metricshour); Goldman Neutral $360 PT says robotaxi/FSD/Optimus commentary matters more than the print (secondary). Value lens: at ~343x trailing earnings with consensus EPS still sliding, no margin of safety on the equity itself; the desk's contribution is the calendar fact and the measured premium. *What would change it: a pre-announcement/8-K before Oct 21 compressing IV; a verified consensus revision; the chain re-priced on Oct 21 itself.*
- **Date correction recorded:** the 2026-10-05/06 nightly iv-inputs files listed TSLA 10/28 — superseded by today's live Nasdaq API confirmation of Oct 21. AAPL 10/29, MSFT 11/4, NVDA 11/18 re-confirmed live by the premium desk.

## 2. Dividend Opportunity desk

| Symbol | Ex-date in window (Oct 7–Nov 4) | Pay date | Amount | Yield (ann., Oct 6 close) | Streak + defining event | Flags |
|---|---|---|---|---|---|---|
| SPY | None | — | TTM $7.583 | 0.98% ($7.583 / $777.22) | N/A (pass-through ETF) | None |
| QQQ | None | — | TTM $3.091 | 0.41% ($3.091 / $757.73) | N/A (pass-through ETF) | None |
| AAPL | None | — | $0.27/qtr ($1.08 ann.) | 0.32% | 15 consecutive years (initiation 2012; increases every year 2013–2026; latest Apr 2026 raise) | Watch: Nov declaration expected ~late Oct, ex ~Nov 7–10 — just outside window (INFERENCE) |
| MSFT | None | — | $0.98/qtr ($3.92 ann.) | 0.74% | 24 consecutive years (anchor per count standard; Sep 15, 2026 raise; ex 11/19, payable 12/10) | None in window — ex 11/19 is 15 days past window end |
| NVDA | None | — | $0.25/qtr ($1.00 ann.) | 0.42% | Not a dividend-growth name; nominal quarterly | None |
| TSLA | None | — | $0 | 0% | No dividend ever paid | None |

- **Bottom line (FACT):** zero watchlist ex-dividend dates in the window — verified via Nasdaq dividends calendar API scanned date-by-date across all 29 days. **No increases/cuts/specials announced in-window.**
- Cross-desk note (FACT): AAPL's ~Nov 7–10 ex-date falls inside typical November covered-call expiry windows — ex-div drag is small (0.32% yield) but real.

## 3. Overnight Premium desk

Stale-jump screen vs 2026-10-05 file: QQQ/AAPL/MSFT still WINDOW-CONTINGENT; **TSLA flipped clean → borderline-contingent (30.50%, just over the line)**; SPY clean (28.93%, just under); NVDA clean.

| Sym | Front ATM IV (Oct 8 expiry, DTE 1.1) | 20d realized | Window-contingent? | 30DTE anchor IV (Nov 6, DTE 29.1) | IV percentile (McMillan, 10/02 vintage) | Earnings in 30d? |
|---|---|---|---|---|---|---|
| SPY | 8.59% | 10.04% | No (28.93%) | 12.73% | 18%ile | none |
| QQQ | 12.16% | 14.73% | **Yes (39.87%)** | 18.51% | 26%ile | none |
| AAPL | 21.48% | 19.77% | **Yes (36.92%)** | 27.74% | 15%ile | **10/29 — INSIDE** |
| MSFT | 22.69% | 19.95% | **Yes (37.67%)** | 33.21% | 55%ile (highest rank) | **11/4 — INSIDE** |
| NVDA | 24.85% | 23.59% | No (25.38%) | 30.19% | **0%ile — cheapest in ~2.4yr** | 11/18 — outside (42d) |
| TSLA | 30.92% | 29.16% | **Yes, borderline (30.50%)** | 43.63% | 2%ile | **10/21 — INSIDE** |

- **Verdicts (INFERENCE, horizon-matched 30DTE IV vs 20d realized):** SPY modestly rich (+2.7pp), clean read; historically cheap level (18%ile). QQQ — WINDOW-CONTINGENT, no clean call. AAPL/MSFT — rich but event-priced, WINDOW-CONTINGENT; avoid. MSFT's 55%ile rank is the board high but event-driven, not a sell signal. NVDA — clean verdict, modestly rich vs realized at a 0%ile level; cheap level, no seller's edge. TSLA — rich with earnings inside the anchor window; avoid selling the hump.
- Term structure upward-sloping across all six; TSLA/AAPL/MSFT slopes embed earnings humps. Premium-into-binary-event = avoid applies to AAPL, MSFT, TSLA.
- Method (FACT): front IV = mean(call ATM IV, put ATM IV), arithmetic shown in raw pull JSON at `~/workspace/goals/hedge-desk-daily-research/hidden_files/iv-desk-raw-2026-10-07.json`. McMillan feed re-pulled live today; page updates Saturdays only (stale-by-construction, date-stamped).

## 4. Open Quant/AI Model Lab

Ledger now holds **34 candidates** (`~/workspace/hedge-desk-research/quant-lab-ledger.md`); this run added #30–34 and one verified status change.

| # | Candidate | Source | Score | Disposition | Next action |
|---|---|---|---|---|---|
| 30 | Shiraya/Yamakami/Yamazaki — option-implied time-varying-volatility-scaled SDF → equity premium forecast | arXiv:2607.08500 | 57 | WATCH | Advance to TEST only if code/data released and OOS claim replicated on US data |
| 31 | Jin/Agarwal — conditional DDPM for arbitrage-free IV surface generation | arXiv:2511.07571v1 | 46 | WATCH | Code not linked; watch for repo release |
| 32 | yassineerraji/Derivatives-Pricing-Risk-Engine (fail-closed SVI arb checks) | GitHub | 70 | TEST | BLOCKER: no LICENSE (all-rights-reserved); resolve with author, then sandbox SVI calibration on SPY chain vs #18 |
| 33 | ArturSepp/VanillaOptionPricers (numba BSM + Bachelier pricers, IV fitters) | GitHub | 77 | TEST | pip install; benchmark IV inversion speed/accuracy vs desk's solver |
| 34 | Qu/Chen/Wang — "Propose, Don't Judge" frozen betting-based referee for LLM factor mining | arXiv:2609.27051v1 | 57 | WATCH | Re-check code release; repo's own 2026-09-25 sweep scored 66/TEST — rescored independently, scores never inherited |

- **Status change (FACT):** #4 M2VN — peer review confirmed (proceedings of ACM ICAIF'25); rescored 62→59, stays WATCH (no code).
- Line stops re-verified: #9 Buchegger & Gonon still no author code link (stays WATCH/BLOCKED); #20 Yang et al code hyperlink still malformed (stays WATCH).
- Kaizen: never import scores from the repo's own docs — verify via primary source (arXiv abs) and rescore independently.

## 5. Weather/War/Logistics Futures Event desk

| # | Event | Timing | Reported FACT | Inference | Source |
|---|---|---|---|---|---|
| 1 | EIA Weekly Petroleum Status | Released today 10:30am ET — ON SCHEDULE | Crude −3.2M bbl to 424.1M (1% above 5-yr avg); gasoline +0.4M; distillates ~unchanged at **12% below 5-yr avg**; products supplied 21.1M bpd (+0.7% y/y). API Tue had shown −2.09M. | Neutral-to-soft crude balance, but distillate deficit into heating season is the tight spot — matches WSJ "diesel near record highs." *Changes: distillate build next week or confirmed G7 diesel SPR hitting market.* | eia.gov dnav (primary, direct fetch) |
| 2 | EIA Natural Gas Storage | Thu Oct 8, 10:30am ET (upcoming) | WSJ survey: +79 Bcf expected vs 5-yr avg ~96 Bcf; 8th straight surplus-shrink week if so. Tropical Storm Isaias approaching Gulf, forecast hurricane landfall Friday. | A print at/under 79 Bcf tightens winter setup (EIA's Oct-31 3,969 Bcf target likely unachievable → October STEO likely revised down). Storm output disruption (~10 Bcf/day, Tradition Energy) partly offset by LNG shut-ins/demand destruction — net UNVERIFIED until landfall. | WSJ; tradingnews |
| 3 | October WASDE | Fri Oct 9, 12:00pm ET (upcoming) | StoneX: soy yield 54.1 bpa / 4.65B bu (record, above USDA Sep); corn 182.1 bpa / 16.12B bu (2nd-largest ever, vs USDA Sep 178.5). Brazil runoff Oct 25. | Grains pricing big-crop confirmation; surprise risk skews to USDA printing *below* StoneX (bullish surprise). *Changes: Friday's USDA figures.* | tradingview/DJN; American Ag Network |
| 4 | US-Iran conflict / Hormuz (8th month) | Ongoing; OPEC+ held Nov targets Sun Oct 4 | OPEC+ seven core members held Nov output steady; G7 Oct 2: 100M-bbl crude+diesel emergency release over ~4 months; Trump ruled out US diesel export ban; ME exports exceeded pre-war levels 4 of last 7 Sept days (Reuters shipping data); Saudi Aramco cut Nov Arab Light OSP for Asia by $3 to $5/bbl discount. | Market prices both sides: Brent $100+ on disruption risk while recovering flows + G7 release + OSP cut cap upside. Aramco CEO's "dangerously thin inventories / ~3B bbl removed" is a company claim (UNVERIFIED) — tension with observed export recovery. *Changes: Hormuz reopening progress (bearish) or confirmed major attack (bullish).* | Reuters; WSJ |
| 5 | Houthi claims vs Saudi | Mon Oct 5 | Houthi claimed attacks on Saudi sites (Riyadh airport, Rabigh refinery, Abha airport). **No Saudi confirmation — UNVERIFIED.** | Headline risk only; Monday oil price action (fell) suggests the market discounted it. | Reuters |
| 6 | CFTC COT | Released Fri Oct 2 (as of Sep 29); next Fri Oct 9 | WTI non-commercial net long ≈109.5K, near 10th percentile; price fell >5% to ~$89. | Washed-out positioning = limited forced-selling overhang; a genuine bullish catalyst could re-leverage fast. *Changes: Friday's COT.* | fxstreet (secondary of CFTC; direct pull not performed) |

**Futures-curve read (FACT quotes, INFERENCE read):** WTI Nov $89.14 → Dec $88.25 → Jan 27 $87.43 → Feb $86.50 — steady ~1%/mo backwardation: curve wants barrels now despite US stocks 1% above avg. Brent $101.09 vs WTI $89.14 = **$11.95 spread** (widened from $8.41 Oct 1) — the geopolitical premium is almost entirely in seaborne Brent. Nat gas winter hump: Nov $3.21 → Jan $3.91 (+22%) → Mar $2.77. Corn 502¢, soy 1295.75¢, wheat 686¢ (wheat −2.6% today) — no fear premium into WASDE, which is itself the tell. VIX 15.08: geopolitical premium siloed in energy, not transmitting to equity risk-off.

## 6. Box/Parity Observer

Nothing material since the 2026-10-06 run. The only index-methodology items found are stale (S&P/TSX Canadian eligibility change announced 2026-09-13, effective Dec 21, irrelevant to the US watchlist; TXSE eligible-exchange addition from June; VIX weeklies inclusion predates the run window). No published put-call/box-parity violation analysis appeared — the closest reference (Summa Money's Oct-1 options brief) shows VIX-futures put-call parity holding within ~0.16, i.e., no dislocation. Deterministic parity math remains unchallenged.

## 7. Bonds & Rates desk

Module run OK, no failures. All FACT from `rates_desk.rates_environment()`, REAL_FRED_RATES mode, as-of 2026-10-06.

| Series | Value | As-of | Direction of change |
|---|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-06 | +25bp over the module's 60-day window |
| 2Y Treasury (DGS2) | 4.79% | 2026-10-06 | −5bp day-over-day; up from 4.25% at window start (2026-08-10) |
| 10Y Treasury (DGS10) | 5.27% | 2026-10-06 | −4bp day-over-day; up from 4.72% at window start (+55bp over window) |
| 2s10s slope | 48bp (UPWARD_SLOPING) | 2026-10-06 | Flat — 47bp at start, 48bp at end; parallel bear move, not a steepening/flattening episode |
| SOFR | 3.90% | 2026-10-06 | — |
| EFFR | 3.88% | 2026-10-06 | — |
| OBFR | 3.88% | 2026-10-06 | — |

- **SOFR–EFFR spread: 2bp (FACT)** — calm; no funding stress. Overnight rates cluster tightly with EFFR.
- **Premium-pricing read (INFERENCE):** higher long rates raise discount rates → growth multiple compression; QQQ/NVDA/TSLA/MSFT/AAPL carry the most duration exposure; treat long-dated growth-call premium as expensive until the 10Y confirms a top. Stable curve shape means no fresh recession-signal or term-premium regime shift to price into vol structure. *What would change it: 10Y back under ~5.00%; a ±15bp weekly move in the 2s10s slope.*

## Run notes

- All seven desks returned output; none FAILED. No desk section missing. Verification: file re-read from disk after write.
- Yield labeling rule held (^TNX = 10Y; ^FVX = 5Y; no 2Y claim). No federal "data blackout" framing applied; brief-correction-2026-10-05.md not applied per standing rule.
- Hard boundaries honored: no Risk of Ruin work, no trade authorization, no licensed material reproduced, no GitHub operations of any kind.
- Paper-only context throughout. Verdicts are research inputs for the downstream brief-publish job, not trading instructions.
