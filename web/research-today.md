# Hedge-Desk Daily Research — Tuesday, 2026-10-06

*Research input only. Paper-only context. No trades, no authorization, no Risk of Ruin math.*
*Compiled ~2:20 PM PT Tue 10/6. US equities closed 1:00 PM PT; desk quotes pulled fresh today (Yahoo with UA header; crumb-auth where needed).*
*Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED per the desk standard. The claim's label is set by its weakest link.*
*Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Lens: value investor — mispricings, intrinsic-value gaps, margin of safety.*
*Standing rules honored: ^TNX = 10Y, ^FVX = 5Y (never labeled 2Y); no federal shutdown — CR through Dec 11; EIA (Wed 10:30 ET) and WASDE (Fri 10/9 12:00 ET) on schedule.*
*Carry-over from 10/5 nightly: SPY $774.83, QQQ $756.20, AAPL $332.89, MSFT $525.18, NVDA $238.90 (record), TSLA $378.73; VIX 15.52; 10Y (^TNX) 5.311%, 5Y (^FVX) 5.066%; WTI ~$89.78 with G-7 100M-bbl release news.*

---

## Synthesis — the 5 most decision-relevant items (contradictions resolved)

1. **TSLA's Oct 21 AMC earnings is the first watchlist binary (15 days out) — options price ~2× the median past reaction; avoid selling premium into it.** Implied move ±8.25% via the Oct 23-expiry ATM straddle ask (31.40 ÷ 380.68, FACT — earnings desk, Yahoo chain 10/6) vs a median ±3.5% historical earnings-day move over the last 4 AMC reports (3.45, 3.56, 14.52, 2.28; mean ±5.95%, inflated by Q2's −14.5% shock). The premium desk independently confirms the hump live in the chain: 17DTE ATM IV 46.6% vs 3DTE 32.5% (FACT, today's pull). Desk-tension note: the IV-implied move (~46.6% × √(17/365) ≈ ±10%) differs from the straddle-ask-implied ±8.25% — different conventions (mean call/put IV vs executable ask) on same-day pulls; the straddle-ask number is the tradeable read. Per the desk's binary-event rule: selling 10/23-expiry premium = short gamma into a scheduled binary. (Date re-verified today: TSLA 8-K filed 10-02, Ex. 99.1 — "after market close on Wednesday, October 21, 2026"; webcast 4:30pm CT. Same release: Q3 deliveries 486,532 vs production 464,391 — FACT, EDGAR 0001628280-26-064366.)
2. **MSFT's Windows/Surface event tomorrow (Wed Oct 7) sits inside its 3DTE expiry window — its 23.6% ATM IV is event-priced, not a clean premium-selling setup.** Earnings desk: MSFT's actual earnings date is still UNVERIFIED (third-party estimates conflict: Oct 27 / Oct 28 / Nov 4; issuer has not announced; no MSFT 8-K in last 24h). Premium desk: MSFT window is also WINDOW-CONTINGENT (39.0% single-day variance share). What would change it: event passing (Oct 7), an issuer-confirmed earnings date.
3. **NVDA is the only clean conditional IV read: 24.3% IV vs 25.5% 20d trailing realized, window clean (25.7%), no catalyst in window — modest cheapness vs realized, capped by the 3DTE-vs-20d tenor mismatch.** QQQ (43.8%), AAPL (36.3%), and MSFT (39.0%) verdicts are all WINDOW-CONTINGENT; SPY is borderline (29.98%) — none support a clean rich/cheap call. IV rank is UNVERIFIABLE from free sources (stated, not faked) — but see item 5: a verified free weekly IV-percentile feed was found today.
4. **Rates: neutral-to-slight headwind for growth-multiple premium names; funding clean; binary rate events this week argue against selling premium into them.** FRED module (`rates_environment()`, exit 0, all series populated; observations dated 2026-10-05): fed funds effective 3.88%, 2Y (DGS2) 4.84%, 10Y (DGS10) 5.31%, SOFR 3.89%, EFFR 3.88% (FACT from module output; 10Y cross-checks the 10/5 nightly ^TNX 5.311% — independent-source agreement). 2s10s slope +47bp, broadly stable over 60d but bear-steepening ~6bp since Sep 30 (41bp → 47bp, driven by the 10Y leg). SOFR–EFFR +1bp = no funding stress. Calendar: $58B 3Y auction today 1pm ET, $39B 10Y + FOMC minutes (Sept 15–16 meeting) Wed 2pm ET, $22B 30Y Thu. INFERENCE: elevated discount rates persist as the drag on long-duration growth multiples (QQQ, NVDA, MSFT); net curve regime is neutral-to-slight-headwind for carry-driven premium sizing.
5. **Oil: EIA Wed 10:30 AM ET (confirmed on schedule via eia.gov) is the binary resolving the two-way tape; the bearish leg strengthened in the last 24h.** FACT: CL curve in steep backwardation (Nov 26 $89.76 → Jun 27 $81.57, ~$8.20/7mo); WTI–Brent ~$10.50 (Brent ~$100.3) prices the Gulf disruption premium as temporary; shipping data shows Middle East exports above pre-war levels 4 of 7 days in late Sep (bearish); Houthi strike claims on Aramco sites/Riyadh airport (Oct 4–5) unconfirmed by Saudi (bullish tail only). API weekly inventory tonight 4:30 PM ET sets expectations for Wednesday. October WASDE Fri Oct 9 12:00 PM ET (confirmed via usda.gov) is the only fresh ag binary; corn harvest pace rebound (drier central US) is the pre-report pressure valve; NG Nov $3.12 (+1.6%) bids into Thursday's storage report; gold Dec $4,191.60 (+0.8%) holds a safe-haven bid.

Adjacent one-liners: no watchlist name goes ex-div inside the 4-week window — only MSFT's raised $0.98 dividend ex-div 11/19/2026 (payable 12/10), streak at 24; AAPL streak verified at 15 years, November dividend not yet declared (FACT: "Apple does not have any future dividends declared" per Zacks crawl 10/6). Quant Lab logged 8 new candidates (#22–#29): the standout is the Option Strategist free weekly IV/HV/IV-percentile feed (score 77, TEST) — the first free verified answer to the premium desk's IV-rank gap; FlashAlpha free options-analytics API (score 70, TEST, free key not yet obtained); purgedcv sklearn purged k-fold package (score 74, TEST). Box/Parity: nothing material (one adjacent item: CBOE's exclusive S&P 500 index-options license extended through 2051, 8-K Sep 29 — guarantees SPX options continuity; per-contract fees update Jan 1, 2027).

---

## 1. Earnings Event desk

| Name | Next earnings date | BMO/AMC | Implied move % | Hist avg earnings-day move | Source |
|---|---|---|---|---|---|
| TSLA | **Wed Oct 21, 2026** (15 days out, outside 2-wk window) — FACT | AMC | **±8.25%** — FACT (Oct 23-expiry ATM straddle ask 31.40 ÷ 380.68, Yahoo chain 10/6) | ±5.95% avg / **±3.5% median** (abs moves: 3.45, 3.56, 14.52, 2.28) | Issuer 8-K filed 10-02 (Ex. 99.1): "after market close on Wednesday, October 21, 2026"; EDGAR 0001628280-26-064366; webcast 4:30pm CT |
| MSFT | Late-Oct cluster — **UNVERIFIED** | AMC (est.) | n/a — date unconfirmed | n/a | trefis & ad-hoc-news: Oct 27; MarketBeat: Oct 28 (est.); Zacks outlier Nov 4. Issuer has NOT announced; no MSFT 8-K in last 24h |
| AAPL | Oct 28/29 — **UNVERIFIED** | AMC (est.) | n/a — date unconfirmed | n/a | Zacks & MarketBeat: Oct 29 (est.); tradingpedia: Oct 28. Issuer has NOT announced; no AAPL 8-K in last 24h (only Form 4/144 insider filings) |
| NVDA | Nothing within 2 weeks — FACT; next expected ~late Nov | — | n/a | n/a | Nasdaq earnings calendar 10/6–10/21 and 10/6–11/10 returned zero watchlist rows; no NVDA 8-K in last 24h |
| SPY | n/a — ETFs don't report earnings | — | — | — | — |
| QQQ | n/a — ETFs don't report earnings | — | — | — | — |

Evidence notes: TSLA Oct 21 AMC date FACT (issuer primary source, re-verified 10/6 via 8-K exhibit on EDGAR). Q3 deliveries beat posted in same release: 486,532 deliveries vs 464,391 production (FACT, same exhibit). INFERENCE: options pricing a larger move than the 4-report average; the average is inflated by Q2's −14.52% day; the median (3.5%) is the cleaner read. What would change it: Q2's −14.5% drop falling out of the 20d variance window, or MSFT/AAPL binary dates firming up and repricing the megacap-vol complex. No 8-K filed by any watchlist name in the last 24h (FACT — EDGAR submissions JSON checked for all four; most recent 8-K was TSLA's 10-02 deliveries release). CFA earnings-release reading order not applied — no watchlist name released a filing in the last 24h.

**Most decision-relevant:** TSLA's Oct 21 AMC report is the first watchlist binary event; options price ±8.25% vs a median ±3.5% historical move — ~2× the median past reaction, an elevated expectation likely lingering from Q2's −14.5% shock. The nearest watchlist attention catalyst is not earnings: MSFT's Windows/Surface event Wed Oct 7 (RTX Spark debut, Huang expected).

Sources: EDGAR submissions API (all four issuers, 10/6); Nasdaq earnings calendar API (ranges 10/6–10/21, 10/6–11/10); Yahoo v7 options chains with crumb-auth + UA header (10/6).

## 2. Dividend Opportunity desk

Package date: 2026-10-06. Window scanned: 4 weeks (through ~Nov 3, 2026).

| Name | Next ex-div | Amount | Pay date | Raise/cut/special flag | Streak count + defining event |
|---|---|---|---|---|---|
| SPY | ~Dec 18, 2026 (not declared; quarterly pattern: Sep 18) — UNVERIFIED | TBD — UNVERIFIED | n/a | None | n/a (ETF) |
| QQQ | ~Dec 21, 2026 (not declared; last ex-div 09/21/2026) — UNVERIFIED | TBD — UNVERIFIED | 10/08/2026 (for the Sep ex-div — a *pay* date, not a capture event) — FACT (Nasdaq) | None | n/a (ETF) |
| AAPL | ~Nov 9–10, 2026 (pattern: 11/10/2025); **not yet declared** — UNVERIFIED | Likely $0.27 (prior rate) — UNVERIFIED | n/a | None | **15 consecutive annual increases** (initiated 2012 = year 1; raises announced each calendar year 2013–2026, latest the May 2026 raise to $0.27/qtr) — INFERENCE from Nasdaq dividend history (each year's rate above the prior year's, splits-adjusted; issuer IR not re-pulled this run) |
| MSFT | **11/19/2026** — FACT (Nasdaq + issuer release) | **$0.98** — FACT | **12/10/2026** — FACT | **+8% raise announced Sep 15, 2026** ($0.91 → $0.98) — FACT | **24 consecutive annual increases** (incl. the Sep 2026 raise to $0.98/qtr; no skipped year per ~/workspace/hedge-desk-research/dividend-count-standard.md). No further 2026 raise announced — FACT (news sweep 10/6) |
| NVDA | ~Early Dec 2026 (pattern: 09/10, 06/04); not declared — UNVERIFIED | TBD — UNVERIFIED | n/a | None in last 7 days. Context: quarterly rate jumped $0.01 → $0.25 with the June 2026 payment (announced earlier, not in this window) | UNVERIFIED per the standard — no clean annual-increase run (years with no announced increase break a streak; the 2026 jump is the first increase in years); not counted, not guessed |
| TSLA | — | — | — | — | Nothing material: pays no dividend — FACT |

Evidence-label ledger: no watchlist name goes ex-div tomorrow (10/7) or this week — FACT (independent Nasdaq calendar + Yahoo actions checks). No announced dividend increases, cuts, or specials for watchlist names in the last ~7 days — FACT (news sweep; MSFT's raise is Sep 15, outside the window). What would change the verdicts: AAPL declaring its November dividend (typically late October alongside earnings week) would convert its ex-div from UNVERIFIED to FACT; SPY/QQQ December declarations likewise.

**Most decision-relevant:** No watchlist name goes ex-div inside the 4-week window; the only scheduled ex-div capture event is MSFT's raised $0.98 dividend going ex-div 11/19/2026 (payable 12/10/2026) — already declared, amount fixed.

Sources: Nasdaq dividends calendar API (scanned 10/06, 10/13, 10/20, 10/27, 11/03 — zero watchlist names on any scanned date); Nasdaq per-symbol dividend history; Yahoo Finance chart API v8 (events=div,split) with UA header; Microsoft Sep 15, 2026 dividend declaration release; Zacks dividend history crawl (10/6).

## 3. Overnight Premium desk

Pull status: all six Yahoo v7 options chains retried fresh today and returned non-degenerate, tradeable quotes (last night's bid=ask=0 failure did not recur). Quote timestamps: 2026-10-06T20:00:01Z (1:00pm PT, mid-session — FACT, from Yahoo quote payloads). Tenor note: nearest expiry was 2–3 DTE; a 2–3DTE ATM IV is not directly comparable to 20d realized vol (tenor mismatch — INFERENCE), so "cheap" reads are capped at conditional.

| Name | Nearest-expiry ATM IV (mean call+put) | DTE | 20d realized | Rich/cheap verdict + window-contingent flag | Notes |
|---|---|---|---|---|---|
| SPY | 8.3% (C 9.17 / P 7.40, exp 2026-10-08, und 779.09) | 2 | 10.5% | IV below realized, but **BORDERLINE window** (29.98%, just under the 30% rule) → no clean "cheap" verdict; realized baseline dominated by one ~30%-share day (INFERENCE) | Spreads 2¢, OI live — quotes not stale |
| QQQ | 12.2% (C 13.20 / P 11.16, exp 2026-10-08, und 759.66) | 2 | 15.4% | IV below realized but **WINDOW-CONTINGENT** (43.8%) → verdict suspended (INFERENCE) | Live-quote quality |
| AAPL | 22.2% (C 23.02 / P 21.36, exp 2026-10-09, und 333.63) | 3 | 20.9% | IV slightly above realized but **WINDOW-CONTINGENT** (36.3%) → no clean "rich" verdict | Earnings ~10/29 UNVERIFIED, not in window; liquid (vol 9656 on call) |
| MSFT | 23.6% (C 24.38 / P 22.80, exp 2026-10-09, und 529.30) | 3 | 21.3% | **WINDOW-CONTINGENT** (39.0%); 3DTE window contains **MSFT's own Windows/Surface event Wed Oct 7** → elevated front IV is expected, not "rich" (INFERENCE) | Premium into a binary event = avoid |
| NVDA | 24.3% (C 24.81 / P 23.79, exp 2026-10-09, und 239.24) | 3 | 25.5% | IV below realized, window **clean** (25.7%) → conditional "slightly cheap" vs trailing realized, tenor-mismatch caveat (INFERENCE) | No catalyst in window; earnings ~11/18 (nightly file). Cleanest read today; 46k/38k call/put volume — very liquid |
| TSLA | 32.5% (C 33.39 / P 31.69, exp 2026-10-09, und 380.68) | 3 | 32.6% | IV ≈ realized, window clean (26.7%) → fair, no mispricing (INFERENCE) | **Term structure (FACT, pulled today): 17DTE (exp 2026-10-23, covers 10/21 AMC earnings) ATM IV 46.6% vs 3DTE 32.5%** — textbook earnings hump. Selling 10/23-expiry premium = short gamma into a scheduled binary; avoid |

IV-rank snapshot: **UNVERIFIED for all six** — no free IV-history source exists to build a real IV rank (FACT per standing desk note), and none is faked. VIX 15.01 at 20:15 UTC today (down from 15.52) — index vol, not a substitute for single-name IV (FACT).

CFA sanity checks applied (`references/derivatives_options.md`): (1) positive and finite — all six pass today; (2) term structure sensible — TSLA 3DTE 32.5% → 17DTE 46.6% with 10/21 earnings in the back window is the module's "earnings inside the window = hump" pattern, confirming interpretation; (3) event inside window — MSFT Oct 7 event; (4) IV vs trailing realized — SPY/QQQ below realized but the 30%+ single-day shares confirm window contamination; no complacency call warranted; (5) stale-quote check — 1:00pm PT session quotes with 2–8¢ spreads and real volume/OI, not stale; parity reconciles (TSLA C−P 0.875 vs S−PV(K) 0.805; SPY's wider diff ≈ dividend PV carry) → no parity violation, math stands.

What would change the verdicts: a published IV-history/IV-rank source; post-event prints (MSFT after Oct 7, TSLA after 10/21 earnings); a 20d window with no >30% single-day dominance for QQQ/AAPL/MSFT.

**Most decision-relevant:** (1) TSLA's 10/21 earnings hump is live (46.6% at 17DTE vs 32.5% at 3DTE) — selling premium into the 10/23 expiry is short gamma into a scheduled binary; avoid. (2) MSFT's nearest window covers tomorrow's event — event-priced, not a clean setup. (3) NVDA is the only clean conditional read (modest cheapness vs realized, tenor caveat). (4) QQQ/AAPL/MSFT verdicts WINDOW-CONTINGENT; SPY borderline — none support a clean rich/cheap call.

Sources: Yahoo v7 options chains (crumb + UA header, 10/6, quote timestamp 2026-10-06T20:00:01Z); 2026-10-05 nightly iv-inputs.json (window-contingent flags, realized 20d); CFA `references/derivatives_options.md`.

## 4. Open Quant/AI Model Lab

Scored with the repo's own `hedge_desk.research_intelligence.assess_source` (0–100; INTEGRATE ≥80, TEST ≥65, WATCH ≥45, ARCHIVE <45). Ledger checked first — no re-adds; candidates #22–#29 appended to ~/workspace/hedge-desk-research/quant-lab-ledger.md (date, URL, score, disposition, follow-up — verified on disk).

| Title | Type | URL | Score | Disp. | Reason |
|---|---|---|---|---|---|
| eslazarev/purged-cross-validation (purgedcv) — sklearn purged k-fold, embargo, walk-forward, CPCV, PSR/DSR/PBO/MinBTL | REPO | https://github.com/eslazarev/purged-cross-validation | 74 | TEST | FACT (GitHub fetched 10/6): MIT license, CI/docs/coverage badges, PyPI + conda-forge, JOSS paper, updated ~9 days ago. Installable — the practical purged-CV testbed; supersedes license-blocked ilyamirin harness (#1) |
| Option Strategist free weekly IV/HV/IV-percentile (McMillan Analysis Corp) | DATA | https://www.optionstrategist.com/calculators/free-volatility-data | 77 | TEST | FACT (source fetched live 10/6): renders real rows — $SPX hv20/50/100 11/11/12, cur_iv 14.60, 594/26%ile; $NDX 191/97%ile. Updated each Saturday, covers all stock/index/futures options. HTML table only (no API) — weekly scrape pipeline needed. **Direct upgrade for the premium desk's IV-rank UNVERIFIED gap** at weekly cadence |
| FlashAlpha options analytics API + MIT Python SDK (surface, GEX/DEX/VEX/CHEX, VRP, vol-carry, earnings analytics) | API | https://github.com/flashalpha-lab/flashalpha-python | 70 | TEST | FACT (README fetched 10/6): free key, no card; Public tier = vol-grid `surface()`, `stock_summary()`; Free+ = gex/dex/exposure levels/greeks/IV solver; `data_as_of` provenance. UNVERIFIED: free-tier quotas (pricing page not read). Next: free-key signup (user decision — not taken) + quota verification |
| Han et al — Diffusion models for dynamic IV surface generation + data-driven hedging | PREPRINT | https://arxiv.org/abs/2609.13402v1 | 48 | WATCH | arXiv:2609.13402v1, v3 17 Sep 2026 (q-fin.CP). UNVERIFIED: code hyperlink renders as malformed text on the abs page — reproducibility not established. Re-check: code link fixed? |
| Adamski & Ślepaczuk — When the Fed Speaks: Dynamics and Forecasts of the Volatility Surface | PREPRINT | arXiv:2608.10693 | 40 | ARCHIVE | Conv2D-LSTM on IV surface; headline is a negative result (edge limited by surface noise). Code unlocated. FOMC-week IV elevation noted as premium-desk context |
| MDPI Risks 14(10): AI/ML framework for PEAD classification | PEER_REV | https://www.mdpi.com/2227-9091/14/10/230 | 39 | ARCHIVE | Peer-reviewed (~Oct 2026) but Saudi Tadawul-only — no US/watchlist transfer |
| stackflow-pead — pre-registered PEAD V2 audit, NSE India | REPO | https://github.com/kanikakataria75-ship-it/stackflow-pead | 37 | ARCHIVE | UNVERIFIED (search snippets only). Indian equities — scope mismatch; process note only |
| project-finmetrica — quant research engine, CPCV backtesting | REPO | https://github.com/swastikk594-hub/project-finmetrica | 37 | ARCHIVE | Student project, license unverified, superseded by #22 for purged-CV utility |

Desk-input upgrades identified: (1) Premium desk — #23 Option Strategist: first verified free IV-percentile feed for all watchlist names; a Saturday scrape would give the desk a real IV-vs-history baseline within a week. (2) Premium + Earnings — #24 FlashAlpha: free-tier vol surface grid, VRP/vol-carry screening, earnings analytics once a key is obtained. (3) Quant lab — #22 purgedcv: pip-installable replacement for the license-blocked #1 harness.

**Most decision-relevant:** the Option Strategist free weekly IV-percentile feed (#23, score 77, TEST) — first free, verified-from-source dataset that directly fills the premium desk's IV-rank data gap.

Standing TEST/WATCH items: no status changes this run; #9 (Buchegger) line-stop unchanged (code repo still down).

## 5. Weather/War/Logistics Futures Event desk

### Catalyst triage

| Catalyst | Date/time | Status | Directional pressure |
|---|---|---|---|
| EIA Weekly Petroleum Status Report | Wed Oct 7, 10:30 AM ET | **CONFIRMED ON SCHEDULE** — eia.gov schedule page lists Wed 10:30 AM ET as standard release (no exception for week ending Oct 2) | Binary — crude build/draw + distillate stocks are the near-term tape catalyst |
| API weekly inventory | Tue Oct 6, 4:30 PM ET | On schedule (tonight, after our package) | Sets expectations for Wednesday's EIA print |
| October WASDE + Crop Production | Fri Oct 9, 12:00 PM ET | **CONFIRMED** — usda.gov: "In 2026 the WASDE report will be released on … Oct. 9" at 12:00 PM ET | Binary for corn/soy/wheat |
| EIA Natural Gas Storage | Thu Oct 8, 10:30 AM ET | On schedule per standing calendar | Near-term binary for NG |
| G-7 100M-barrel reserve release (diesel + crude, over 4 months, no export restrictions) | Agreed Fri Oct 3 | Active — pressured crude Mon (WTI −1.2% to ~$90) | Bearish crude |
| Houthi strikes on Saudi targets (Aramco Riyadh/Khurais; Oct 5 claims added King Khalid airport, Rabigh refinery, Abha airport) | Claimed Oct 4–5 | Ongoing — **unconfirmed by Saudi Arabia** | Bullish crude tail only |
| Saudi/Gulf exports | Week ending Sep 26 | Shipping data: Middle East crude exports **above pre-war levels 4 of 7 days** despite Hormuz vessel attacks | Bearish — physical flow offsetting strike headlines |
| OPEC+ | Held Nov targets steady | Unchanged | Neutral-to-tight — no supply relief |
| US corn harvest weather | Last week + outlook | ~10 days of heavy rain slowed harvest; central US now turning drier, temps near/above normal | Bearish-to-neutral grains into WASDE (faster harvest pace = pressure) |

### Futures curve read (Yahoo quotes, pulled ~1:35 PM PT Tue Oct 6 — FACT quotes; reads are INFERENCE)

- **CL (WTI):** Nov 26 $89.76 → Dec 26 $88.70 → Jan 27 $87.67 → Jun 27 $81.57. **Steep backwardation** (~$8.20 over 7 months). FACT: market pricing prompt tightness + future loosening. INFERENCE: consistent with G-7 reserve release + elevated spot geopolitical premium priced to fade. Front-month −0.7% vs last night.
- **WTI–Brent spread:** WTI ~$89.76 vs Brent ~$100.3 (Reuters) → ~$10.50. INFERENCE: wide spread reflects Middle East logistics dislocation priced into Brent; ICE gasoil +2% Monday confirms diesel/refined-products dislocation continues.
- **NG:** Nov 26 $3.12 (+1.6% d/d) → Jan 27 $3.80 (+2.5%). Winter premium/contango shape; modest bid into Thursday storage report.
- **GC (gold Dec 26):** $4,191.60 (+0.8% d/d). FACT: bid near highs. INFERENCE: safe-haven demand persists alongside Gulf strike risk even as equities rose.
- **ES (Dec 26):** 7,877.25 (+0.65% d/d). **NQ:** 31,499 (+0.58% d/d). FACT: equity futures up overnight. INFERENCE: risk assets treating oil supply headlines as net-benign; China closed (Golden Week through Oct 7) = thin Asia session, direction UNVERIFIED for full-session conviction.
- **ZB (Treasury bond Dec):** 102.38 — roughly flat vs yesterday; no fresh rates signal.

### Facts vs inference — the oil two-way tape

- **FACT (reported):** G-7 released 100M barrels and pledged no export restrictions; Middle East exports above pre-war levels 4 of 7 days in late Sep; Houthi strike claims Oct 4–5 unconfirmed by Saudi; WTI −1.2% Monday to ~$90; Brent ~$100.
- **FACT (quotes):** CL curve in steep backwardation; gasoil +2% Monday; gold up overnight.
- **INFERENCE:** the bearish leg (SPR release + physical export recovery) strengthened in the last 24h; the bullish leg (Houthi/Aramco) is unchanged-to-slightly-active (new claims, zero confirmed damage). Tape bias shifted modestly bearish; the curve prices the geopolitical premium as temporary.
- **UNVERIFIED:** actual Aramco damage; the real G-7 release pace (announced, not yet verified flowing); energy-cost transmission magnitude into watchlist earnings margins.
- **What would change it:** EIA Wednesday 10:30 ET (big draw re-arms the bullish leg; build confirms bearish drift); any confirmed Aramco damage report (flips instantly).

### Crop/weather (into WASDE)

- Heavy rain delayed US corn/soy harvest ~10 days; drier central-US outlook lets farmers catch up — harvest pace = near-term pressure (FACT: ag press; INFERENCE on price effect).
- Sept quarterly stocks pegged corn at 2.095B bu (+173M vs Sept WASDE ending stocks) — bearish baseline already in price (AgWeb: corn $4.95, soybeans $12.75, "waiting on the next card").
- Watch: WASDE yield calls (corn estimates 173–182 bpa), Brazil Oct 25 runoff (real strength = US export competitiveness edge), Mexico buying corn near $5, grain-quality/mold concerns from the wet spell (yield/quality risk = bullish tail).

**Most decision-relevant:** (1) **EIA Wednesday 10:30 AM ET is the single binary resolving the oil two-way tape** — watch the distillate print specifically, given diesel/gasoil dislocation persists even as crude slides. (2) CL backwardation + ~$10.50 WTI–Brent spread prices the Gulf disruption premium as temporary — a mean-reversion lean on Brent basis, but fail-closed on any confirmed Aramco damage. (3) WASDE Friday 12:00 PM ET is the only fresh ag binary; harvest-pace rebound is the pre-report pressure valve.

Sources: eia.gov Weekly Petroleum Status Report schedule; usda.gov WASDE page; Reuters via IndexBox (10/6); American Ag Network (10/5); AgWeb (10/5); Yahoo futures quotes (10/6 ~1:35 PM PT).

## 6. Box/Parity Observer

Nothing material on the desk's core mandate this run: no new CBOE / S&P DJI / Nasdaq index-methodology documents and no fresh published parity-violation analysis (academic, CBOE white paper, or primary-data market-structure blog) dated in the last ~7 days.

Adjacent item (one line): Cboe Global Markets extended its exclusive U.S. S&P 500 index-options license with S&P through 2051, effective Sep 28, 2026 (announced via 8-K Sep 29, 2026) — guarantees SPX options continuity for the premium desk; per-contract license fees update Jan 1, 2027. (FACT — TradingView News: https://www.tradingview.com/news/tradingview:a15474a0a43ff:0-cboe-global-markets-extends-exclusive-s-p-500-index-options-license-with-s-p-through-2051/)

Desk status: nothing material to log this run.

## 7. Bonds & Rates desk

**Source:** repo module `hedge_desk.rates_desk.rates_environment()` (mode `REAL_FRED_RATES`, fred-public-csv-http-200, exit 0, all series populated). **Module as-of: 2026-10-06; latest observations dated 2026-10-05** (FRED daily series are prior-business-day). All numbers below are FACT from the module output unless otherwise labeled.

| Series | Level | As-of date |
|---|---|---|
| Fed funds effective (DFF) | **3.88%** | 2026-10-05 |
| Treasury 2Y (DGS2) | **4.84%** | 2026-10-05 |
| Treasury 10Y (DGS10) | **5.31%** | 2026-10-05 |
| SOFR | **3.89%** | 2026-10-05 |
| EFFR | **3.88%** | 2026-10-05 |
| OBFR | **3.88%** | 2026-10-05 |

**2s10s slope: +47bp, UPWARD_SLOPING** (module-reported `curve_shape`). Direction: the curve is broadly *stable, edging steeper at the margin* — 2Y 4.19% → 4.84% and 10Y 4.65% → 5.31% since Aug 7 (both ≈+66bp, net slope change ≈+1bp), but the last five sessions show mild bear-steepening: Sep 30 slope was 41bp, now 47bp (+6bp in ~3 sessions, driven by the 10Y leg). Cross-check: module's 5.31% 10Y matches the 10/5 nightly Yahoo ^TNX read of 5.311% (FACT — independent-source agreement).

**SOFR–EFFR spread: +1bp (3.89 vs 3.88)** — FACT. One-line read: **no funding stress** — overnight secured and unsecured benchmarks are essentially pinned to each other and to EFFR; nothing here constrains premium-selling capacity or widens financing drag on hedges (INFERENCE).

**Directional read for premium pricing** (INFERENCE, anchored to measured levels): 10Y at 5.31% with a positively sloped curve means discount rates remain elevated — the standing drag on long-duration growth multiples (QQQ, NVDA, MSFT) persists; all else equal, that caps upside multiple expansion and is the headwind to monitor for premium sizing on big-cap growth names. Mild recent bear-steepening is a small tailwind for time-value (longer-dated premium carries higher carry), but the heavy auction slate this week can just as easily richen term premia (bid risk) — SPECULATION on direction from here. Net: no rate-driven reason to lean into premium selling on growth names for carry alone; the curve regime is neutral-to-slightly-headwind, and binary event risk (auctions, FOMC minutes) dominates the next 48 hours — avoid selling into those, consistent with the premium desk's binary-event rule.

**Upcoming rates events** (FACT — desk brief context, times ET): Tue 10/6: **$58B 3Y auction, 1pm ET**; Wed 10/7: **$39B 10Y auction** + **FOMC minutes (Sept 15–16 meeting), 2pm ET**; Thu 10/8: **$22B 30Y auction**; Fri 10/9: October WASDE 12:00 ET; Oct 28 FOMC meeting (Oct-hike odds ~20% per yesterday's brief — secondary, INFERENCE-classified).

**Most decision-relevant:** Fed funds effective 3.88% with a +47bp 2s10s curve that bear-steepened ~6bp since Sep 30 — rates are a neutral-to-slight headwind for growth-multiple premium names (QQQ/NVDA/MSFT), funding markets are clean (SOFR–EFFR +1bp), and today's $58B 3Y (1pm ET) plus Wednesday's FOMC minutes are the rate catalysts that argue against selling premium into binary supply/policy events this week.

---

## Run notes

- All seven desks delivered. No desk failed; no retry was needed. Quant-lab ledger append verified on disk (candidates #22–#29, dated 2026-10-06).
- Desk-agreement check: earnings and premium desks agree TSLA 10/21 is the binary (issuer-confirmed); MSFT/AAPL late-Oct earnings dates remain UNVERIFIED across all sources checked (EDGAR, Nasdaq calendar, web); premium and rates desks agree on the binary-event-avoidance rule for this week's auctions/FOMC minutes/MSFT event.
- IV-rank remains the desk's weakest input; today's Quant Lab find (#23, Option Strategist weekly IV-percentile feed, TEST) is the first verified free fix — a Saturday scrape of the six watchlist symbols would close the gap at weekly cadence.
- No synthetic data anywhere in this package. All numbers carry sources and as-of timestamps above.
