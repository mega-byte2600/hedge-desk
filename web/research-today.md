# Hedge-desk daily research — 2026-10-11

**Run:** hedge-desk-daily-research, Sun 2026-10-11, 13:30 PT. Research + input only — paper-only context, no trade authorization, no Risk of Ruin.
**Data clock:** US equities closed (weekend); all equity/options data = Friday 2026-10-09 close. Futures reopen Sun ~3pm PT. Rates data = FRED through 2026-10-08.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA. **Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety.
**Standing labels:** every material claim marked FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it.

## Cross-desk synthesis — the 5 decision-relevant items

1. **TSLA earnings Wed Oct 21 (AMC) is the only binary event in the 2-week window — and both desks say don't sell premium into it.** Options-implied ±7.5% (Oct-23 ATM straddle, live-computed at TSLA $382.70) vs ~5% realized average over the last 4 reports (Barron's Apr 2026; DailyIQ 5.2%). Term structure independently confirms: Oct-16 expiry 37.35 → Oct-23 (captures earnings) **48.07** → Oct-30 44.80 — the textbook binary-event hump. INFERENCE: the market is pricing elevated uncertainty; selling TSLA premium into 10/21 buys the binary, not edge. The opportunity side is the post-10/21 IV crush. Context (FACT, Tesla IR Oct 2): Q3 deliveries 486,532 beat company-compiled consensus by ~5.3%, but energy-storage deployments 13.7 GWh missed 15.9 GWh consensus. INFERENCE: the 10/21 print will trade on auto gross margin and FCF conversion more than the delivery beat. What would change the verdict: the release itself (apply release-reading order: guidance vs consensus → GAAP net income → cash flow → segment margins).
2. **Rates support elevated baseline IV in growth names; no funding stress.** 10Y 5.22%, 2Y 4.75% (FRED, 10/8), 2s10s 47bp steady upward-sloping, DFF 3.88%, SOFR−EFFR −1bp (no wholesale funding stress). INFERENCE: high discount-rate regime = structural pressure on long-duration multiples (NVDA, MSFT, TSLA) and typically supports elevated baseline IV in growth names. Cross-check from the parity desk: SPX box-spread implied premium over SOFR averaged ~32bp in 2026, recently rising to **~69bp** — synthetic borrowing via boxes getting more expensive, consistent with marginally tighter funding. No parity violation reported.
3. **Sunday-night futures reopen carries gap risk in both directions.** Friday's October WASDE was genuinely bearish for corn: yield raised 2.7 bpa to **181.2** (trade expected a cut to ~177.6), ending stocks 1.849B bu (+282M vs Sept); Dec corn **−4% to $4.80½** (nearly −6% intraday; lowest close since Aug 13). Funds entered net long 377,850 corn contracts → forced liquidation; the market now treats 181.2 bpa as the base case into the Nov 10 report. Energy whipsawed: Brent $104.72 (+44¢), WTI $91.85 (+36¢) — Friday fell on Iran de-escalation headlines (no pre-midterm strikes, Hormuz-reopening proposal, Russian diesel license through Apr 7, 2027) then closed higher on the hurricane. Concrete tightness: Hurricane Isaias (Cat 2, landfall near Destin, FL Friday night) shut in **71.5% of Gulf oil production (1.46M bpd)**; VLCC rates Persian Gulf→East Asia **>$1.4M/day** (record, +40% first week of Oct); distillates flat at 12% under the 5-yr average. INFERENCE: Friday closed pricing physical disruption over political talk. SPECULATION: whether the Russian diesel license lands physical barrels by November.
4. **Only NVDA offers a clean IV-vs-realized read; everything else is WINDOW-CONTINGENT.** NVDA iv30 29.59 vs RV20 22.37 on a non-contaminated window (single-day share 23.7%), front expiries clean of the Nov 17 event — paper-seller-friendly, though part of the 7.2-pt gap is event bid. SPY / QQQ / AAPL / MSFT / TSLA all carry single-day variance shares of **30.6–40.9%** (above the 30% threshold) — no clean rich/cheap verdicts; treating AAPL (26.4 vs 16.4) or MSFT (31.3 vs 22.3) gaps as seller opportunities would trade on contaminated denominators. **Methodology change with standing implications:** Yahoo's v7 options API is now fully crumb-gated from this host (401 "Invalid Crumb" on query1/query2); the CBOE delayed-quotes feed (`cdn.cboe.com`, unauthenticated, exchange-computed iv30) is the new standing fallback. IV-rank (1Y percentile) remains **UNVERIFIED** — no free IV-history source; the quant desk's #56 (volrec, daily IV recorder) is the candidate that attacks this gap.
5. **Quant lab: two actionable candidates this week (ledger #54–58, Jidoka triage appended).** **#54 landtml/finlab-ml (TEST):** complete AFML toolkit — combinatorial purged CV + embargo, triple-barrier labels, DSR/PBO, HRP, numba — green CI this morning, MIT. Sandbox shootout vs #22 (purgedcv) decides the purged-CV testbed for the whole desk. **#56 gabrielmitton-cloud/volrec (WATCH):** daily 30d ATM call IV + 5 Greeks for 109 tickers (full watchlist incl.) via GH Actions 14:30 NY since Sep 4 — the first candidate attacking the premium desk's chronic IV-history gap from the data side. SPECULATION until the Alpaca indicative feed cross-checks against Yahoo IV. Also: #55 volsurface (WATCH, IV-surface pricing lib), #57 AlphaPADI (WATCH, alpha discovery — no code), #58 UVM error bounds (ARCHIVE, European-only theory). No new free options-data APIs surfaced this week.

**Contradictions resolved:** (a) AAPL timing — earnings desk confirms **Mon Nov 2, 2026 (AMC)**; the dividend desk's early-Nov ex-div estimate was built on the 2025 pattern (ex-div 11/10/2025) and assumed an Oct-29 declaration. Kept as SPECULATION — if the earnings date shifted a weekend, the declaration/ex-div schedule may shift with it. (b) NVDA earnings — earnings desk: **Tue Nov 17, 2026 (AMC)**, announced on the Aug 26 call; the premium desk's "11-18" was carried from the stale iv-inputs file. Nov 17 is the confirmed date. Otherwise desks corroborate (TSLA hump vs earnings date; rates-tightening vs box-implied premium; quiet parity desk vs no parity flags in IV chains).
---

## 1. Earnings Event desk

*Window: Oct 12–25, 2026. No watchlist-name earnings releases issued in the last 7 days (TSLA's Q3 deliveries release was Oct 2 — outside the window), so no fresh release teardown this run.*

| Name | Report date | BMO / AMC | Implied move % | Historical avg move | Verdict |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21, 2026 | AMC (webcast 5:30 p.m. ET) | **±7.5%** (front expiry bracketing earnings, live-computed) | ~5% avg over 4 most recent quarters (Barron's, Apr 2026; DailyIQ 5.2% / median −3.4% / largest −9.6%) | Only in-window event; implied exceeds recent realized — binary-event risk into 10/21 |
| AAPL | Mon Nov 2, 2026 | AMC | n/a — outside window | — | Out of window |
| MSFT | Wed Oct 28, 2026 | AMC (call 2:30 p.m. PT; confirmed by Microsoft press release, Oct 7) | n/a — outside window | — | Out of window |
| NVDA | Tue Nov 17, 2026 | AMC (announced on Aug 26 earnings call) | n/a — outside window | — | Out of window |
| SPY / QQQ | — | — | — | — | ETFs; no earnings |

**TSLA detail (the one event in window):**
- Report date/timing FACT — after market close Wed Oct 21, 2026; Q&A webcast 4:30 p.m. CT / 5:30 p.m. ET, per Tesla's own IR announcement (Morningstar/Business Wire, 20261002169209). TipRanks independently confirms Oct 21, After Close (Confirmed).
- Implied move FACT (computed live 2026-10-11 ~13:30 PDT, TSLA $382.70) — Oct 23, 2026 expiry ATM straddle (strike 380) mid = $28.80 → **±7.53%** (strike-385 straddle identical). Oct 16 expiry pre-dates the event, so Oct 23 is the earnings-capturing expiry. Yahoo pulls used the UA header; the v7 options endpoint required the crumb flow, which succeeded for the earnings desk (note: the premium desk's parallel attempt hit 401s — host-route-dependent; see §3).
- Historical avg move FACT with recency caveat — Barron's (Apr 2026, around Q1 print): ~5% average in either direction after each of the four most recent quarterly reports (2 up, 2 down). DailyIQ (crawled Oct 11): 5.2% average session-after move across its last 3 dated reports. Both are secondary aggregators, not issuer data.
- Consensus estimates UNVERIFIED — TipRanks Q3 consensus EPS $1.78 vs Barchart $0.23 diluted (down 37.8% YoY) vs fiscal.ai ~$0.45 on $27.9B revenue; the sources disagree on basis definition and cannot be reconciled.
- Pre-earnings context FACT — Tesla's Oct 2 IR release: Q3 deliveries 486,532 vs 461,974 company-compiled consensus (beat ~5.3%); production 464,391; energy-storage deployments 13.7 GWh vs 15.9 GWh consensus (miss). Tesla cautions deliveries are "only two measures of the Company's financial performance." INFERENCE: the 10/21 print trades on auto gross margin and FCF conversion more than the delivery beat.

**Verdict:** One event in window — TSLA Oct 21 AMC, implied ±7.5% above the recent realized average of ~5%. INFERENCE: the market prices elevated uncertainty; premium-selling into 10/21 carries above-baseline tail risk and premium-buying is expensive vs history. What would change it: a fresher published historical-move average (through Q2 2026) or the actual Oct 21 release.

---

## 2. Dividend Opportunity desk

*Window: Oct 11 → ~Nov 8, 2026. Prices = Friday Oct 9 closes (Yahoo Finance, FACT).*

| Name | Next ex-div | Amount | Pay date | Yield | Count / status | Notes |
|---|---|---|---|---|---|---|
| SPY | ~mid-Dec 2026 (est. Dec 18–19) | ~$1.89 (last: $1.889, Sep 18) | ~Dec 21, 2026 | 0.97% | Quarterly dist.; no increase/cut announced | Outside window; date is INFERENCE from 2023–2026 pattern; last payment FACT |
| QQQ | ~mid-Dec 2026 (est. Dec 22) | ~$0.75 (last: $0.751, Sep 21) | ~Dec 23, 2026 | 0.40% | Quarterly dist.; no increase/cut announced | Outside window; date INFERENCE; last payment FACT |
| AAPL | **Not yet declared**; expected ~Nov 9–10 | $0.27 (declared Apr 30, 2026) | ~Nov 12, 2026 | 0.32% | 14 consecutive annual raises, calendar years 2013–2026, off 2012 initiation base (FACT per issuer/MarketBeat) | At/just beyond the 4-week edge — undeclared until earnings (now confirmed **Nov 2** by earnings desk, not the Oct-29 pattern the desk assumed). Treat as SPECULATION |
| MSFT | **Thu Nov 19, 2026** (record Nov 19) | **$0.98** | Thu Dec 10, 2026 | 0.73% | **24 consecutive annual increases** (incl. Sep 15, 2026 board raise; anchor per dividend-count-standard.md) (FACT) | +$0.07/+8% over prior $0.91; declared Sep 15, 2026 (FACT). Outside window but declared — first ex-div at the new rate |
| NVDA | Not yet declared; expected ~early Dec 2026 | $0.25 ($1.00 annualized) | ~Jan 2027 | 0.44% | May 18, 2026 raise $0.01 → $0.25 (+2,400%) is the defining increase; payout ratio ~14–17.5% (FACT) | No future dividends declared per Zacks (FACT). Raised-then-frozen posture; management prefers buybacks per 2026 coverage (INFERENCE) |
| TSLA | None | $0 | — | 0% | Pays no dividend (FACT — zero dividend events in Yahoo history) | — |

Sources: Yahoo Finance chart API (events=div, UA header) for payout history and Oct 9 closes; Zacks NVDA/AAPL dividend histories; MarketBeat AAPL history; MSFT declaration reporting (ad-hoc-news.de); NVDA raise coverage. **Gap:** Nasdaq dividends-calendar API returned zero rows on all tested dates (2026-10-12 through 2026-11-09) — flagged as a source gap; declared facts corroborated via Yahoo + issuer-adjacent reporting, not Nasdaq alone.

Decision-relevant bullets:
1. **No dividend-capture play inside the 4-week window.** Nothing has a *declared* ex-div through ~Nov 8. AAPL's early-November date is the only candidate and is undeclared — SPECULATION, not tradeable.
2. **MSFT Nov 19 is the first ex-div at $0.98 — the anchor-rate event.** Fully declared: record Nov 19, pay Dec 10, 24th consecutive annual increase. Value lens: 0.73% entry yield with ~20–24% payout ratio is conservative, not a red flag.
3. **NVDA's $1.00 annualized dividend is a reset, not a yield story.** 0.44% yield, ~14–17.5% payout ratio — zero income mispricing for a value lens; no December declaration yet.

**Desk verdict:** no announced increases/cuts/specials in-window; all streaks intact; nothing material for dividend-capture through Nov 8.

---

## 3. Overnight Premium (IV) desk

**Data-status declaration:** The nightly `2026-10-10-iv-inputs.json` is **STALE** — `as_of` 2026-10-10T13:55:03−07:00, ~23.5h before this run, exceeding the 18-hour freshness guard. Its IV values are not used as today's numbers. **Yahoo fallback also failed**: `v7/finance/options` returns HTTP 401 on query1 and query2 (Invalid Crumb; crumb flow broken from this host; finance.yahoo.com unreachable), and Nasdaq's option-chain API returned `400 "Symbol not exists"`. **This section uses the CBOE delayed-options feed** (`cdn.cboe.com/api/global/delayed_quotes/options/{SYM}.json`) — per-contract IVs plus exchange-computed 30-day `iv30` — as of Friday Oct 9 close. All CBOE figures labeled **FALLBACK**. The stale-jump screen was re-run live on Yahoo v8 daily closes (HTTP 200) for 2026-09-14 → 2026-10-09. IV *rank* (1Y percentile) is **UNVERIFIED** — no free IV-history source available from this host; level-vs-realized reported instead.

| Symbol | IV read (FALLBACK, Fri 10/9 close) | Front-week ATM IV | Term-structure note | Earnings in window? | Verdict |
|---|---|---|---|---|---|
| SPY (778.57) | iv30 **11.85** vs RV20 9.93 | 8.96 (DTE 4) | Flat 8.8–9.4 across DTE 4–9; no hump | None | WINDOW-CONTINGENT — single day drives 31.8% of 20d variance; no clean rich/cheap call |
| QQQ (751.38) | iv30 **17.81** vs RV20 15.58 | 13.97 (DTE 4) | Flat 13.8–14.7; no hump | None | WINDOW-CONTINGENT — 40.9% single-day share |
| AAPL (336.08) | iv30 **26.37** vs RV20 16.42 | 22.22 (DTE 5) | 20.6–22.3, flat-ish DTE 5–12 | Nov 2 in iv30 window | WINDOW-CONTINGENT — gap inflated by contaminated realized window + earnings bid; not cleanly "rich" |
| MSFT (535.00) | iv30 **31.30** vs RV20 22.30 | 22.54 (DTE 5) | Mild upward slope 20.9 → 23.0 into DTE 12 | Oct 28 in iv30 window; front expiries only partially capture it | WINDOW-CONTINGENT — upward slope into the 10-28 event; premium prices the binary, not free alpha |
| NVDA (229.33) | iv30 **29.59** vs RV20 22.37 | 28.78 (DTE 5) | 26.5–28.8, flat DTE 5–12 | Nov 17 in iv30 window; front window clean | Cleanest read: IV ~7.2 vol pts above realized on a NON-contingent window — seller-friendly on paper; changes if the gap compresses after 11-17 clears |
| TSLA (382.73) | iv30 **42.41** vs RV20 29.97 | 37.35 (DTE 5) | **Earnings hump confirmed:** 10-16 37.35 → 10-23 **48.07** (straddles 10-21 earnings) → 10-30 44.80 | Oct 21 inside front window | WINDOW-CONTINGENT — hump is unambiguous: premium INTO the binary event = **avoid selling**; the 48.07 vs 37.35 differential is priced-in IV-crush protection, not edge |

**Live re-verification of the stale-jump screen** (Yahoo v8, window 2026-09-14 → 2026-10-09, FACT — values match the stale file's shares to 0.001): window_contingent = SPY 0.318, QQQ 0.409, AAPL 0.357, MSFT 0.345, TSLA 0.306 — all above 30% (flags persist); NVDA 0.237, clean.

Bullets:
- Term structure independently confirms TSLA's 10-21 earnings is priced. Per desk stance we are premium sellers by default, but selling TSLA premium into that hump is buying the binary, not selling edge — **avoid**; the opportunity side is the post-10-21 crush, after the event clears (INFERENCE on the hump-to-earnings mapping; changes if the company moves the date).
- No put-call parity red flags: ATM call/put IVs print equal (e.g., SPY 10-15: 8.96/8.96) — the math wins; the IV numbers pass the sanity screen (positive, finite, front > back only where an event sits).
- The IV > realized gaps for AAPL (26.4 vs 16.4) and MSFT (31.3 vs 22.3) look "rich" but are not actionable: both realized windows are WINDOW-CONTINGENT (35.7% / 34.5%) and both iv30 windows contain earnings — marked UNVERIFIED-as-opportunity.
- NVDA is the only clean IV-vs-realized verdict: 29.59 vs 22.37 on a non-contingent window, front expiries clean. Even there the iv30 window contains Nov-17 earnings, so part of the gap is event bid — a seller-side read holds only if the gap persists after the event clears.
- **Methodology note:** Yahoo's v7 options API is now fully crumb-gated from this host (both query endpoints → 401; legacy crumb endpoint 404s; finance.yahoo.com HTML unreachable). The CBOE delayed feed worked unauthenticated and includes exchange-computed iv30 — viable standing fallback, and the freshest available data on a Sunday (Fri 10/9 close). IV-rank history remains the unresolved gap; labeling stays UNVERIFIED.

---
## 4. Open Quant/AI Model Lab

*Sweep window: 2026-10-04 → 2026-10-11. Sources: arXiv API (q-fin.CP/PR/ST + keyword legs), GitHub API (repos created since 10-04), HuggingFace datasets API, web search for new free APIs/datasets. All candidates scored with the repo's own scorer (`hedge_desk.research_intelligence.assess_source`, 0–5 input scale). Ledger confirmed appended: rows #54–#58 plus a 2026-10-11 Jidoka triage entry (9 exclusions: 5 NOLICENSE, 2 scope-mismatches, 1 IBKR-gated, 1 out-of-window, 3 marginal arXiv theory papers). No candidates copied from the ledger without this week's re-verification.*

| # | Candidate | Type | Desk relevance | Score | Disp. | Reason |
|---|---|---|---|---|---|---|
| 54 | landtml/finlab-ml — AFML toolkit (CombinatorialPurgedCV + embargo, triple-barrier labels, DSR/PBO, HRP, numba, no sklearn dep; v0.1.4; NOTICE_purgedcv_LICENSE.txt acknowledging #22) | GitHub, created **today** 2026-10-11, MIT | Purged walk-forward / backtest validation | 66 | **TEST** | CI verified green 2026-10-11 via Actions API (FACT); MIT license file present (FACT). README test/purity claims UNVERIFIED (code not run) — sandbox, not integrate. Direct benchmark vs #22 (purgedcv) to pick the purged-CV testbed |
| 55 | coreyjpritchard/volsurface — modular pricing library: yfinance + IBKR chain backends, IV surfaces, one-interface BS/Heston/SABR/rough Bergomi; committed SPY chain snapshots (parquet); pytest; marimo sessions | GitHub, created 2026-10-08, MIT | IV surface screening / SV calibration | 64 | **WATCH** | One point under the TEST band — band discipline; README claims (SPY ATM-skew power law) read at source, not run. Yfinance backend fail-softs to last-session trade prices (quote-quality caveat). TEST opens on sandbox evidence |
| 56 | gabrielmitton-cloud/volrec — daily IV recorder: GH Actions 14:30 NY, 30d ATM call IV + 5 Greeks for 109 tickers (SPY/QQQ/NVDA/TSLA incl.) via Alpaca free indicative feed; `data/iv_history.csv` appended since 2026-09-04; live working-paper page | GitHub, MIT, pushed 2026-10-10 | IV percentile history / VRP | 64 | **WATCH** | Directly addresses premium desk's IV-rank UNVERIFIED gap at daily granularity (complements #23's weekly index scrape). CAVEATS: only ~5 weeks of history; Alpaca feed is indicative/IEX-based, not OPRA — quality UNVERIFIED. Scorer 64 = one point under TEST band; sandbox + cross-check opens it |
| 57 | AlphaPADI (Jin et al) — formulaic alpha discovery via pool-aware hierarchical discrete diffusion | arXiv:2610.04959v2, 4 Oct 2026 (preprint) | Factor-mining methodology (frozen-referee lane) | 45 | **WATCH** | At the WATCH band floor; no author code link on arXiv abs page (verified at source) → reproducibility not established; equity cross-section scope, not options |
| 58 | Abbas-Turki et al — a posteriori error bounds for the Uncertain Volatility Model | arXiv:2610.06495v1, 5 Oct 2026 (preprint) | None operational | 44 | **ARCHIVE** | Below the 45 band; pricing theory for European options (watchlist is American → no desk transfer); no code link |

**Highest-value finds:**
- **#54 finlab-ml (TEST)** — a complete AFML methodology stack with green CI as of this morning, built chapter-by-chapter with explicit proof-note discipline ("proved here / checked by test / measured / claimed from book only" — the evidence-labeling this desk demands). The sandbox shootout vs #22 (purgedcv) decides the purged-CV testbed for the whole desk.
- **#56 volrec (WATCH)** — the first candidate attacking the premium desk's chronic IV-history gap from the data side: daily 30d ATM IV snapshots across the full watchlist, MIT-licensed, machine-collecting since Sep 4. If the Alpaca indicative feed cross-checks cleanly against Yahoo IV on overlapping days, this becomes the daily IV-percentile series the premium desk has never had in-house. SPECULATION until the cross-check is run.

**No new free options-data APIs surfaced this week** (HuggingFace datasets API returned zero options/IV datasets created since 10-04; web sweep found only prior-window items).

---

## 5. Futures Event desk (catalysts)

*Window: Fri Oct 9 – Sun Oct 11, 2026. Futures reopen this evening (~3pm PT); all price "reactions" below are Friday closes.*

### 5a. October WASDE (released Fri Oct 9, 12:00 ET — on schedule)

- FACT: USDA released the October WASDE/Crop Production reports on schedule; next report November 10.
- FACT: Corn was the shock. National yield raised **2.7 bpa to 181.2 bpa** (Sept: 178.5; trade avg: 177.6 — the trade expected a cut). Production **16.034B bu**; 2026/27 ending stocks **1.849B bu** (+282M from Sept's 1.567B; trade avg 1.677B). Release-window move: ZC −72 ticks (HAAWKS).
- FACT: Soybeans: yield **53.1 bpa (record)** (Sept 52.8; trade 52.9), production 4.562B bu, ending stocks 315M bu (+5M from Sept). Exports raised 10M bu on Chinese buying. ZS −76 ticks at release (HAAWKS).
- FACT: Wheat: ending stocks +23M bu to 740M bu on a 25M-bu cut to U.S. export projections. Russian wheat exports cut 3 MMT to 40 MMT. Season-average farm prices cut: corn $4.70 (was $4.80), wheat $6.30 (was $6.40); soybeans held at $12.00.
- FACT (Friday futures reaction, CBOT via Morningstar/DJN): Dec corn **−4% to $4.80½** (nearly −6% intraday before paring; $4.79¾ lowest close since Aug 13); Dec Chicago wheat −1.8% to $6.70¾; Nov soybeans **+0.4% to $12.92¼** (recovered from the release-window drop and closed higher).
- FACT (positioning): CFTC COT showed funds net **long 377,850 corn contracts** entering the report — Friday was forced long liquidation. The Sept 30 Grain Stocks report had already flagged corn at 2.095B bu (+35% YoY, above every trade estimate).
- INFERENCE: The grain curve repriced from a bullish posture to pricing **near-record U.S. supply through year-end**: Dec corn at ~$4.80 sits at the bottom of the $4.80–$5.00 zone — the market treats 181.2 bpa as the working base case, not a headline to fade. INFERENCE: soybeans diverging (+0.4%) while corn/wheat sold signals the curve prices **demand elasticity (China buying) offsetting beans' smaller yield surprise** — beans' problem is comparatively resolved, corn's is not.
- What would change it: the Nov 10 Crop Production report (harvest delays mean USDA data is still incoming); a break in Chinese buying would unwind soybean resilience.

### 5b. EIA weekly petroleum status (released Wed Oct 7, 10:30 ET — on schedule)

- FACT: Week ending Oct 2: commercial crude **−3.2M bbl to 424.1M** (API: −2.09M; surveys expected roughly a +1.7–1.9M build — genuine surprise draw); gasoline +0.4M to ~204.7M (expected ~1.7M draw); distillates roughly flat at 105.1M (expected −2.1M draw) and **12% below the 5-year average**; Cushing +444K to ~24.3–24.7M. Refinery inputs 16.5M bpd at 92.7% utilization; crude exports 4.765M bpd; U.S. production ~14M bpd.
- FACT: Front-month reaction Wednesday: Brent +$1.21 (+1.2%) to $101.79; WTI +$0.48 (+0.5%) to $89.92 — a modest up-move despite mixed product data.
- FACT: EIA's Oct 6 STEO: world stocks drew **1.9M bpd in Q3 (~175M bbl)**, a further 0.7M bpd draw forecast in Q4. The U.S. announced **40M bbl in SPR exchanges (Sept 29)**; G7 announced further supply measures Oct 2. The reports ahead are pre-hurricane (see 5c).
- INFERENCE: The curve read the report as **crude-draw positive but product-data negative** — the surprise was in the wrong contract for a rally (distillate tightness is the bullish channel, and it showed no relief). INFERENCE: with global stocks still falling ~1.9M bpd, the curve's prompt-strength structure is intact absent resolution of the Middle East shipping crisis.
- What would change it: the next two EIA reports (hurricane distortions cut both ways); a material SPR release schedule; concrete diesel flows from the Russia deal.

### 5c. Geopolitics / logistics — last 72 hours

- FACT: **Hurricane Isaias** made landfall Friday night as a **Category 2 near Destin, FL** (had reached Cat 3, 120 mph, Friday morning). As of Friday 11am, **71.5% of Gulf oil production shut in (1.46M bpd)** and 58.8% of gas; 129 of 371 manned platforms evacuated. Saturday: 834,000 customers without power across FL/AL/GA. ~500K bpd of refining capacity at risk.
- FACT: Friday crude settle: **Brent $104.72** (+44¢), **WTI $91.85** (+36¢); Brent **+2.41% on the week**, WTI a slight weekly decline.
- FACT: Thursday Oct 8: Trump posted on Truth Social that the U.S. has "productive discussions" with Iran and will **not attack before the Nov 3 midterms**; kept the port blockade "in full force." Oil fell Friday morning on the news (Brent −1.3% to $102.91, WTI −1.2% to $90.40 early Friday GMT) before recovering on the hurricane. Treasury simultaneously sanctioned 17 more "shadow fleet" vessels. Iran's FM said Tehran is reviewing the U.S. response to a proposal to **reopen the Strait of Hormuz within seven days**.
- FACT: Friday Oct 9: after a Trump–Putin call, U.S. Treasury issued a **temporary license for Russian diesel transactions through April 7, 2027**; Russia on Oct 10 **partially lifted its diesel export ban** (initially permitting 500K tons; Trump announced 300K+ tons immediately, 500K in Nov, 1M thereafter, up to 3M tons total). Analysts skeptical on actual volumes given refinery damage.
- FACT (shipping crisis): VLCC rates Persian Gulf→East Asia **exceeded $1.4M/day** in early October (+40% in the first week — a record); U.S. Gulf→China charters at $76–80M vs $7–10M pre-war. Ship-to-ship transfers off the Gulf of Oman are tying up the fleet; the crunch has spread to Aframax/Suezmax. Hormuz effectively closed since Feb 28 (~20% of world oil/gas flowed through pre-war); 12 attacks/incidents in the strait Sept 28–Oct 5, the worst week since the war began.
- FACT: Thursday: Houthi cruise missiles **struck King Khalid International Airport in Riyadh** (a passenger jet destroyed, pilot killed), with the group threatening Saudi energy plants — tightening Red Sea/Saudi-route options.
- FACT (grain corridor): Black Sea shipping attacks escalated: Turkish bulker *Royad Mammadov* sank off Romania (2 crew killed); bulker *Alfa Watan* sank off Bulgaria; *Able* ablaze with evacuations — hitting commercial grain vessels in NATO economic zones, spiking insurance premiums.
- INFERENCE: The energy complex is pricing **two offsetting premium structures**: the bear case on Iran (no pre-midterm strikes + Hormuz-reopening proposal + Russian diesel) versus the immediate, concrete supply hit (Isaias shut-ins, the shipping crisis adding ~$40/bbl to some delivered-cost routes, Houthi escalation). INFERENCE: Friday's price action — falling on the Trump post, then closing higher on the hurricane — says the curve discounts **political headlines faster than physical disruptions**.
- SPECULATION: Whether the Russia diesel deal actually lands physical barrels by November — Treasury's license is administrative, Russian refineries are damaged, the 500K-ton authorization is small, no delivery schedule confirmed. Treat diesel-price-relief as SPECULATION until tanker fixtures print.

**Bottom-line read:** Friday was the run's heaviest catalyst day — a genuinely bearish WASDE (corn curve pricing near-record supply with liquidation overhang into Nov 10) and an energy market torn between de-escalation headlines and concrete physical tightness. Net: the ag curve repriced lower and decisively; the energy curve whipsawed and closed **pricing physical disruption over political talk**. Futures reopen this evening — Sunday-night reopens after these dual shocks are worth watching for gap risk in both directions.

---

## 6. Box/Parity Observer

No new S&P, Nasdaq, or CBOE index-methodology documents affecting US index-option pricing appeared in the last week (FACT — searches covered methodology announcements and parity analyses; all recent hits are older consultations or product news). Two parity-adjacent items worth a note, neither changing how we read index-option pricing:

- **IRS Notice 2026-62 targets box-spread ETFs (BOXX)** — describes box-spread ETFs converting T-bill-like box returns into deferred capital gains via in-kind redemptions; explicitly limits its reach ("does not address other transactions involving box spreads"), so direct box positions (our implied-rate gauge) are outside it (FACT). INFERENCE: could eventually compress or widen box-spread financing flows through ETFs, but does not alter the parity math or SPX box-implied rates for a paper desk. WATCH only.
- **SPX box-spread loan volume hit a record ~$1.7B notional in 2026**, with the implied yield premium over SOFR averaging ~32bp and recently rising to ~69bp — synthetic borrowing via boxes getting more expensive relative to the front end (FACT). INFERENCE: consistent with tighter funding conditions; cross-check for the Rates desk's funding read. No parity violation reported.

Net: nothing material to change the premium desk's read; desk status green, one-line watch on the IRS notice.

---

## 7. Bonds & Rates desk

*Source: the repo's own `rates_desk.rates_environment()` module, run live this run against FRED daily series. All numbers below come from the module output — none retyped from memory. Latest observations dated 2026-10-08.*

| Metric | Level | Change / direction | Source |
|---|---|---|---|
| Fed funds effective (DFF) | 3.88% (as of 2026-10-08) | −0.25 over 60-day window (measured fact, not forecast) | FRED DFF via rates_desk |
| 2Y Treasury (DGS2) | 4.75% (2026-10-08) | Fell from 4.84% (10/05) → 4.75% (10/08); up from 4.20% (08/12) | FRED DGS2 via rates_desk |
| 10Y Treasury (DGS10) | 5.22% (2026-10-08) | Fell from 5.31% (10/05) → 5.22% (10/08); up from 4.68% (08/12) | FRED DGS10 via rates_desk |
| 2s10s slope (10Y−2Y) | 47 bp | Roughly flat: 47 bp on both 10/05 and 10/08 — curve steady | computed by module |
| Curve shape | UPWARD_SLOPING | No inversion anywhere on the 2s–10s segment | rates_desk classifier |
| SOFR | 3.87% (2026-10-08) | — | FRED via rates_desk |
| EFFR | 3.88% (2026-10-08) | — | FRED via rates_desk |
| OBFR | 3.88% (2026-10-08) | — | FRED via rates_desk |
| SOFR − EFFR | −1 bp | Zero material funding stress | computed |

Labels: every figure above is FACT (FRED daily series, latest observations 2026-10-08). Reads below are INFERENCE unless stated.

- **Curve-shape read (INFERENCE):** upward-sloping and steady — not signaling recession via the 2s10s segment. The −25bp decline in EFFR over the 60-day window is a factual observation consistent with a Fed cut since mid-August (the "cut" attribution is INFERENCE — the module does not provide the target range). What would change it: a re-inversion (10Y−2Y < 0) or sharp bear-steepening.
- **Funding-stress read (FACT-based):** SOFR − EFFR ≈ −1 bp and OBFR = EFFR — no wholesale funding stress in secured or unsecured overnight markets.
- **Premium-pricing implication (INFERENCE):** 10Y at 5.22% is a high discount-rate regime — structurally negative for long-duration growth multiples (NVDA, MSFT, TSLA on the watchlist); high discount rates compress the equity risk premium, which typically supports elevated baseline IV in growth names. The intra-week drift lower (10Y 5.31 → 5.22) is modest relief, not a regime change. What would change it: a sustained 10Y break below ~5.0% or above ~5.4%.

Rates desk: OK (module succeeded; all numbers from FRED module output, no substitutions).

---

## Run notes & methodology changes

1. **All seven desks reported.** Dividend desk's handoff payload dropped in transit; its section was recovered verbatim from the agent's session transcript (no re-dispatch needed; content verified against the transcript).
2. **Premium desk data-source change (standing implication):** nightly `2026-10-10-iv-inputs.json` was STALE (as_of 2026-10-10T13:55 PDT, ~23.5h old > 18h guard) and is not used as today's numbers; Yahoo's v7 options API is now fully crumb-gated from this host (HTTP 401 "Invalid Crumb" on both query endpoints). The **CBOE delayed-quotes feed** (unauthenticated, includes exchange-computed iv30) is the new standing fallback. IV-rank (1Y percentile) remains UNVERIFIED — no free IV-history source; quant candidate #56 (volrec) is the active lead on closing that gap.
3. **AAPL date tension resolved:** earnings desk confirms Mon Nov 2, 2026 (AMC); dividend desk's early-Nov ex-div estimate was built on the 2025 pattern — kept as SPECULATION with possible shift. NVDA earnings confirmed Tue Nov 17, 2026 (AMC) per the Aug 26 call (premium desk's "11-18" was carried from the stale file).
4. **Government-data rule re-verified in practice:** October WASDE (Fri Oct 9, 12:00 ET) and EIA weekly (Wed Oct 7, 10:30 ET) both released on schedule; no shutdown framing anywhere. The stale `brief-correction-2026-10-05.md` premise remains retired.
5. **Yield labeling:** FRED DGS2/DGS10 via the module (authoritative 2Y/10Y); no ^FVX-as-2Y mislabeling.
