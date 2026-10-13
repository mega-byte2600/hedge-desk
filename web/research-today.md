# Hedge-desk daily research — 2026-10-13

**Run:** Tuesday 2026-10-13, 13:30 PDT (coordinator). **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** 7 parallel desks, synthesized — contradictions resolved, top items kept. Standing rules: Yahoo Finance first (UA header `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; v7 options now needs cookie+crumb flow), Nasdaq second; ^TNX = 10Y, ^FVX = 5Y (never 2Y), 13W bill = front-end anchor; no shutdown framing (CR passed 2026-09-01, funding through Dec 11). Technique: CFA skill; every material claim tagged FACT/INFERENCE/SPECULATION/UNVERIFIED.
Desk detail files: `~/workspace/hedge-desk-research/desks/2026-10-13-{earnings,dividend,premium,quantlab,futures,parity,rates}.md`.

---

## Decision-relevant (5 items, cross-desk)

1. **TSLA Q3 earnings Wed Oct 21 AMC — implied move repriced sharply: ±7.14% today vs ±3.97% yesterday.** Oct-23 expiry straddle mid 26.80 on $375.23 close (FACT, live chain ~16:30 ET, IV ~52%); trailing last-4 avg-absolute 5.95% (re-verified from Yahoo closes; Jul −14.52% is the tail). Premium-desk term structure: 51.5% IV on the earnings expiry vs 30.3% trailing realized — largest implied move on the watchlist. **Desk rule: binary event, avoid selling premium into it.** The swing factor is Q2-style margin/regulatory-credit disappointment (auto gross margin 16.8%, weakest since 2023), not deliveries — the 486,532 Q3 delivery beat was pre-announced Oct 2 and is likely in the price.
2. **CPI Wed Oct 14, 8:30 ET is the week's fulcrum.** Consensus: headline ~3.6–3.7% y/y (energy-driven; retail gasoline $4.35/gal, Brent >$105), core ~2.4% m/m steady. A hot core print reprices Oct-28 hike odds up from ~20%; a soft core reprices December hike odds down from ~70%+. FOMC decision Wed Oct 28 — tracker mirrors cluster ~80–83% hold at 3.75–4.00%.
3. **Iran war is the dominant macro catalyst — crude is a logistics-risk market, not a barrel-shortage market.** 7 vessel incidents in Hormuz Oct 11–13 (UKMTO); Hormuz flows 10.5M b/d, ~38% below prewar 17.1M (Kpler); crude freight $30/bbl vs $4 a year ago; Brent−WTI front spread $11.66. WTI curve in steep backwardation: Dec-26 94.05 → Dec-27 79.76 (−$15.31, −16.1%). Binary: Hormuz reopening or IEA-board G7 release details (Oct 14–15) collapse the front; escalation spikes it. EIA WPSR Thu Oct 15 (Columbus Day delay).
4. **NVDA is the richest clean IV-vs-realized on the board — ~31–33% front IV vs 21.8% 20d realized (+~9pts, ~40% relative), mild week-1 backwardation pricing near-term event risk.** Only non-window-contingent IV-vs-realized read (0.237 single-day variance share). No earnings inside the window (Nov 18). Separately, NVDA's 2,400% dividend raise to $0.25/qtr (May/June 2026, ~$24–25B/yr commitment) is a quality-of-FCF signal, not a yield story (~0.44% yield).
5. **Rates: EFFR 3.88% (+25 bp over 60 days), 2s10s flattened 51→44 bp — cut expectations being unwound, not accelerated.** 10Y 5.24% / 2Y 4.80% (FRED, via repo rates module). SOFR≈EFFR (−1 bp): no funding stress. Directional read: mild headwind for growth-multiple premium selling; nothing supports an imminent inversion or funding shock.

---

## 1. Earnings Event desk

**One in-window event (Oct 13–27).**

| Symbol | Quarter | Date | Timing | Options-implied expected move | Historical avg earnings move |
|---|---|---|---|---|---|
| **TSLA** | Q3 2026 | **Wed 2026-10-21** | **After close** (Nasdaq `time-after-hours`) | **±7.14%** (Oct-23 expiry) | −4.81% signed / **5.95% avg-absolute, last 4** |
| MSFT | FQ1 2027 | Wed 2026-10-28 | After close | n/a — 1 day past window | — |
| AAPL | FQ4 2026 | Mon 2026-11-02 | After close | n/a (outside window) | — |
| NVDA | FQ3 2027 | Wed 2026-11-18 | Not supplied (Nasdaq) | n/a (outside window) | — |

- **Date/timing FACT:** Nasdaq earnings calendar API, every in-window trading day queried individually 2026-10-13. SPY/QQQ are ETFs — no earnings by construction.
- **Implied move FACT:** Oct-23 expiry ATM 375.0 straddle mid 26.80 (call 13.75 / put 13.05 mids) on underlying close $375.23 → 7.142%. Chain ~16:30 ET 2026-10-13, live quotes (call vol 2,082, put vol 2,735), IVs 51–52.5%. Consistency check: ~52% IV over 10 days ≈ 6.9–7.1% — straddle math and chain IVs agree (INFERENCE on agreement).
- **Repricing FACT:** yesterday's run reported ±3.97% (Oct-23 ATM 377.5 straddle mid 15.00 on 378.03). Stock fell only ~0.7% while IV roughly doubled. INFERENCE: the Oct-12 figure (~29% annualized) was anomalously low for TSLA 9 days pre-earnings; today's ~52% sits in the normal pre-earnings band — treat the delta as a data-point correction, not a pure market signal.
- **Historical FACT (Yahoo daily bars, report-day close → next close):** +2.28% (2025-10-22), −3.45% (2026-01-28), −3.56% (2026-04-22), **−14.52% (2026-07-22)**. Signed avg −4.81%; avg-absolute 5.95%. INFERENCE: 3 of 4 recent prints were negative — skew to the downside.
- **Setup (statement-analysis reading order):** no Q3 release exists yet. From the Q2 2026 release (record rev $28.24B but adjusted EPS miss $0.33 vs ~$0.54, auto gross margin 16.8% weakest since 2023, FCF −$1.09B) and Tesla IR's Q3 operating update (486,532 deliveries, +24.5k vs consensus; storage 13.70 GWh, 2.2 below consensus). INFERENCE: the delivery beat was pre-announced 19 days out and is likely in the price — the margin/regulatory-credit line, not the unit count, is the swing factor.
- **Verdict:** implied 7.14% > 5.95% trailing average, but the July −14.52% tail sits well outside the straddle — the market prices an average print, not a repeat of the Q2 margin implosion. What would change it: Q3 auto-gross-margin back above ~19% with stabilized credit revenue (upside surprise); any pre-announcement/8-K before 10-21.
- Sources: Nasdaq calendar API `https://api.nasdaq.com/api/calendar/earnings?date=`; Yahoo v7 options (TSLA) + v8 chart; Tesla IR via trade press. Tool note: Yahoo v7 options now requires cookie+crumb (`fc.yahoo.com` → getcrumb); Nasdaq per-quote earnings endpoints returned empty — use the calendar API with date param.

## 2. Dividend Opportunity desk

**No confirmed ex-dividend event inside the 4-week window (through Nov 10).**

| Symbol | Next ex-div | Amount | Declared? | Increase / cut / special | In window? |
|---|---|---|---|---|---|
| AAPL | **~Mon Nov 9 (expected)** | $0.27/qtr est. | **No** — expected ~Nov 2 with FYQ4 earnings | None expected | **Expected (undeclared)** |
| MSFT | Thu 2026-11-19 | $0.98/qtr | Yes (declared 09/15/2026, payable 12/10) | **INCREASE — 24th consecutive year** (count standard) | No — 9 days past window |
| NVDA | ~Dec 3–4 (pattern) | $0.25/qtr (if unchanged) | No | **2400% raise in May/June 2026** (headline carry) | No |
| SPY | ~Dec 18 (pattern) | ~$1.85–1.99 est. | No | None | No |
| QQQ | ~Dec 21 (pattern) | ~$0.75–0.81 est. | No | None | No |
| TSLA | None — no dividend program | — | — | None | — |

- **AAPL — INFERENCE on timing:** pattern Feb/May/Aug/Nov; last ex 08/10/2026 ($0.27, declared 07/30/2026). Next ex expected Mon Nov 9, $0.27 est. (May 2026 raise $0.26→$0.27) — UNVERIFIED until declared. Zacks: "does not have any future dividends declared" as of 10/13. **Value-lens note:** ex-date lands ~9–10 trading days after the Nov 2 earnings print — a dividend-capture position would cross a binary earnings event; not a clean standalone catalyst. Consecutive-increase count: UNVERIFIED this run (not verified against Apple IR; desk standard forbids copying screener counts — no count stated).
- **MSFT $0.98 — FACT** (Nasdaq dividends API): ex 11/19/2026, declared 09/15/2026, payable 12/10/2026. Count **24** per `~/workspace/hedge-desk-research/dividend-count-standard.md` (announcement-date rule; issuer-verified). Just outside window — carry forward.
- **NVDA 2,400% raise — FACT** (Nasdaq API + Yahoo chart history: paid 06/26/2026 and 10/01/2026 at $0.25; prior at $0.01): quarterly lifted from $0.01 to $0.25 (announced with FQ1 2027 results, May/June 2026). Annualized ~$1.00/share ≈ $24–25B/yr (per Morningstar/Colello context); yield still ~0.44% — the raise is a capital-allocation signal (Nvidia committed to return ≥50% of FCF to shareholders), not a yield thesis. Watch the December declaration: a second hold starts a verifiable streak base.
- **SPY last ex 09/18/2026 ($1.889); QQQ last ex 09/21/2026 ($0.75143)** — FACT (Yahoo chart events=div; Nasdaq ETF endpoint). Dec ex-dates are pattern INFERENCE, not declared. Nasdaq's dividends endpoint returns "Non-Nasdaq symbols is not available" for SPY — source limitation noted.
- **Verdict:** nothing actionable in-window — zero declared ex-dates, all watchlist yields <0.7%. What would change it: AAPL declaring a raise >$0.27 with earnings; NVDA declaring Q4 at a different rate; any declared special/cut.
- Sources: Nasdaq `https://api.nasdaq.com/api/quote/<SYM>/dividends?assetclass=stocks|etf`; Yahoo chart API events=div; Zacks dividend-history pages; Morningstar Colello NVDA coverage; `~/workspace/hedge-desk-research/dividend-count-standard.md`.

## 3. Overnight Premium desk (IV)

**Freshness guard: PASS — FRESH.** File `~/workspace/hedge-desk-research/nightly/2026-10-12-iv-inputs.json`, `as_of` 2026-10-12T13:54:39-07:00 ≈ 23.6h old (within the 26h guard) → FACT. IV levels below from a labeled live Yahoo pull as_of **2026-10-13 13:30 PDT** (post-close). IV rank (1Y): **UNVERIFIED all six symbols** — no free IV-history source; never guessed. Note: the file's `atm_iv` column is 0-DTE end-of-day artifact (e.g. SPY 0.55%) — not usable as an IV level read.

| Symbol | Spot | ~3 DTE (Fri 10/16) | ~6 DTE (Mon 10/19) | ~10 DTE (Fri 10/23) | ~17 DTE (Fri 10/30) | 20d realized (file) | Window-contingent? |
|---|---|---|---|---|---|---|---|
| SPY | 778.01 | 10.09% | 8.80% | — | — | 9.97% | **True (0.318)** |
| QQQ | 743.57 | 16.41% | 14.27% | — | — | 15.46% | **True (0.427)** |
| AAPL | 341.27 | 22.27% | 20.75% | 22.27% | — | 16.85% | **True (0.357)** |
| MSFT | 543.45 | 23.15% | 20.98% | 23.56% | — | 22.38% | **True (0.345)** |
| NVDA | 228.52 | 32.95% | 28.59% | 30.93% | — | 21.84% | **False (0.237)** |
| TSLA | 375.23 | 41.32% | 34.84% | **51.52%** | 46.81% | 30.30% | **True (0.306)** |

- **Stale-jump screen:** 5 of 6 symbols are WINDOW-CONTINGENT (single-day variance share >30%) → no clean IV-vs-realized verdict on those five. Only NVDA admits a clean comparison.
- **NVDA — the only clean read: IV rich to trailing realized (INFERENCE).** Front-week ~29–33% vs realized 21.84% — +~9pts / ~40% relative, widest gap on the board. Mild week-1 backwardation (3 DTE 32.95% > 6 DTE 28.59%) then contango to 30.93% at 10 DTE. INFERENCE: front elevation prices genuine near-term event risk (semis newsflow); the decay into Monday is consistent with a priced event resolving by week-end. SPECULATION: the specific catalyst is unidentified from chain data alone. Value-lens: richness is the market charging for convexity into event risk — not a mispricing claim. No earnings in window (Nov 18). What would change it: identifying the priced catalyst, or the elevation decaying through Friday without one.
- **TSLA — earnings binary: premium into it = avoid.** Oct-23 (earnings) expiry 51.52% vs 3 DTE 41.32% vs realized 30.30% — ~1.7× trailing realized through the print. Largest implied move on the watchlist. Realized is window-contingent (0.306) → no clean rich/cheap verdict vs history.
- **MSFT — earnings Oct 28 (15 days out, in window for the desk):** front IV 23.15% → 23.56% at 10 DTE, mildly elevated into the print vs realized 22.38%; window-contingent (0.345) → no clean verdict. Same binary rule: avoid.
- **SPY/QQQ — calm, roughly fair, no verdict:** SPY 10.09% vs 9.97% realized; QQQ 16.41% vs 15.46% — both window-contingent (QQQ's 0.427 highest single-day share on the board). INFERENCE: calm regime, no premium anomaly.
- **AAPL:** Nov 2 earnings inside the 30-day window — flag for next week: the 10/30 and Nov expiries will begin pricing the print; watch for the earnings hump forming.
- Sanity checks: no negative/zero IVs, monotonic strike grids, no parity/model disagreement observed; OTM skew not measured (UNVERIFIED). 0-DTE near-close IVs collapse toward zero (SPY 1.57%, QQQ 2.16%) — expected time-decay behavior (INFERENCE).
- Sources: Yahoo v7 options (crumb-authenticated, 2026-10-13 13:30 PDT); `~/workspace/hedge-desk-research/nightly/2026-10-12-iv-inputs.json`.

## 4. Open Quant/AI Model Lab

**Sweep:** arXiv API (q-fin PR/ST/MF/RM, title-matched option/volatility/implied/hedge/earnings/dividend, 60 hits, sorted submittedDate desc), GitHub repo search API (3 queries, created>2026-10-09), Semantic Scholar bulk API (27 items, clean). Window Oct 9–13. All scores from the repo's own `hedge_desk.research_intelligence.assess_source` on own evidence; bands TEST ≥ 65 / WATCH ≥ 45 / ARCHIVE < 45. 3 new candidates appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` as #64–66 (deduped vs existing 63; no repeats).

| # | Candidate | Source | Score | Disposition | Reason |
|---|---|---|---|---|---|
| 64 | chawla2255/sabr-vol-surface — SABR IV surface, Hagan formula, β=1, vega-weighted fits (RMSE 0.09–0.34 vol pts), zero calendar/butterfly arb on ±3σ grid; live SPY snapshot 2026-10-12 | GitHub, MIT (FACT via API), 0-star single author | 55 | **WATCH** | Third MIT surface impl. in the premium-desk arb-audit lane (#18/#32/#50). Claims README-reported, UNVERIFIED (tests not run). Next: sandbox pytest; fit fresh SPY chain vs #50's eSSVI. |
| 65 | CaffineDuck67/can-ml-beat-garch — leakage-free walk-forward: EWMA/GARCH(1,1)-t/HAR-RV vs Ridge/RF/LightGBM/LSTM for S&P 500 forward RV; purge/embargo expanding windows; DM tests. Headline: ML wins at 5d (Ridge RMSE 7.57 vs GARCH 8.56, DM p=0.0002) but NOT at 21d (LightGBM significantly *worse* than HAR-RV, p=0.016); no clear economic value. | GitHub, MIT verified | 58 | **WATCH** | Day's strongest catch — a fully documented, leakage-audited purged-WF benchmark that *fails to beat classical models at 21d and admits it*. Strongest purged-WF methodology match in weeks. Next: pip install + pytest; reproduce 5d/21d; port expanding-window+embargo pattern. |
| 66 | Prakash/Ferstler/Pezolano — "FOMO: FLEX Options and Market Outcomes" (arXiv:2610.13044v1, 9 Oct 2026) — matched-control DiD: post-event listed-OI increase β=0.3061 (p=0.0042); FLEX selects high-IV environments; event-day IV−RV spreads predict execution-stressed short-straddle returns. | arXiv, CC BY-NC-SA 4.0, no author code link (FACT, abs page verified) | 37 | **ARCHIVE** | Below the 45 band; microstructure context only, no transferable data/code; findings source-reported, UNVERIFIED. |

- **Re-checks:** #4 M2VN and #35 VolPaint — GitHub search 0 hits, still no code; stay WATCH. No status changes; #1/#20/#32 license line-stops untouched. No TEST/INTEGRATE promotions.
- **Triage exclusions (no ledger rows):** NOLICENSE repos (PulkitTiwari87/neural-volatility-surface, Nitmore/ML-Volatility-forecasting-options-research, nabilely19/orderbook-realized-vol, simbashakib/SPY_Volatility_Forecasting, MadhanJ05/options-lab, faresgit19/Nappe_vol_SP_Bergomi, NightCoderLJ/Option-Valuation-Engine); crypto/MOEX/NSE scope; notebook stubs; arXiv hedging-theory with marginal desk fit.
- Sources: arXiv API; GitHub search/code-search API; Semantic Scholar bulk API; ledger `~/workspace/hedge-desk-research/quant-lab-ledger.md`.

## 5. Futures Event desk (Weather / War / Logistics)

### USDA / Grains — Oct WASDE digested; harvest pace is the live variable
- **FACT (WASDE, Fri Oct 9 12:00 ET):** bearish corn — yield raised 2.7 bpa to **181.2** (trade expected a cut; largest Sept→Oct increase since 2005), production **16.034B bu** (+234M), ending stocks **1.849B bu** (+282M vs 1.677B avg guess). Soy near-neutral: yield 53.1 (+0.3), production 4.562B bu (+27M, record if realized), stocks 315M (+5M). Wheat stocks 740M (+23M); world: corn 280.4 MMT, soy 124.3 MMT, wheat 276.0 MMT.
- **FACT (market response):** Dec corn −20½¢ (−4.1%) to 479¾ on WASDE day (limit-down intraday); soy +4½¢ to 1292. As of Oct 13 close: ZCZ26 **482.75** (−0.05% d/d), ZSX26 **1282.75** (−0.39%), ZWZ26 **668.25** (−0.60%) — corn flatlined near WASDE-day lows.
- **FACT (Crop Progress, wk ended Oct 4, released Mon Oct 12):** corn harvest 23% complete (4 pts behind avg), condition 54% G/E (−3 w/w); soy harvest 25% (8 pts behind avg); winter wheat planting 36% (10 pts behind last year).
- **FACT (COT as of Oct 6):** managed money cut corn net long 60,491 to 377,850; added 10,496 to soy net long (251,660); added 7,873 to CBT wheat net short (29,543).
- **INFERENCE (curve pricing):** full carry, no near-term squeeze — ZCZ26 482.75 → ZCH27 496.75; ZSX26 1282.75 → ZSF27 1298.50. Market accepts 181.2 yield until harvest proves otherwise. What would change it: harvest yields vs 181.2; hard freeze; China soy buying ahead of US-China summit; CONAB **Thu Oct 15**; next WASDE **Tue Nov 10**.

### EIA / Crude — WPSR delayed; curve in steep backwardation
- **FACT (schedule):** WPSR (week ended Oct 9) is **Thu Oct 15, 12:00 ET** — pushed from Wed by Columbus Day (eia.gov schedule page). API weekly bulletin moves to **Wed Oct 14**. Nat Gas Storage Thu Oct 15, 10:30 ET (last print Oct 8: +85 Bcf vs 79 expected; stocks 3,500 Bcf, +68 vs 5-yr avg).
- **FACT (last EIA print, wk ended ~Oct 2):** crude drew 3.186M bbl vs +1.722M expected (API had flagged −2.09M crude, −1.37M gasoline).
- **FACT (Oct 13 closes):** CL=F **95.07** (+1.42% d/d); BZ=F **106.73** (+0.08%); **Brent−WTI front spread $11.66**, unusually wide. NG=F **3.32** (+4.77% d/d, +14.6% 1mo).
- **FACT (WTI term structure):** Dec-26 94.05 → … → **Dec-27 79.76**: front-to-Dec27 **−$15.31 (−16.1%) over ~14 months**, ~$1.00/month front backwardation.
- **INFERENCE:** acute near-term physical tightness with expected normalization through 2027 — textbook war-risk backwardation, not structural shortage. The $11.66 Brent−WTI spread says US domestic barrels are insulated; the dislocation is in seaborne/freight-exposed barrels. Nat gas Nov 3.32 → Jan 4.02 (+21%) is normal winter contango tempered by the +68 Bcf storage surplus. What would change it: IEA-board G7 release details (Oct 14–15); Hormuz reopening (front collapses toward deferreds); escalation (front spikes).

### Geopolitics / Logistics (last ~72h) — Iran war is the dominant macro catalyst
- **FACT (Hormuz, UKMTO/Kpler via press):** ≥7 vessel incidents Oct 11–13 — crude tanker struck by unknown projectile in outbound Hormuz transit (fire aboard), UAV hit near Oman's Sohar anchorage, third vessel struck Oct 11; one damaged tanker diverted to Fujairah. ~14 vessels attempted Hormuz transit Oct 12; 6 ran dark. Hormuz flows averaged **10.5M b/d** (7 days through Oct 10), **~38% below prewar 17.1M b/d** (Kpler).
- **FACT (weekend escalation):** Houthis struck Riyadh's King Khalid airport (≥13 killed, 300+ wounded); CENTCOM disabled Panama-flagged *M/V Ocean Molica* Oct 10 for running the naval blockade. Aramco CEO: supply pressure intensifies until Hormuz fully reopens; Saudi output ~**8.4M b/d** (highest since conflict began), Iraq 4.4M b/d via alternative routes.
- **FACT (freight dislocation, Goldman via DJ/Morningstar Oct 13):** avg global crude freight **$30/bbl vs $4 a year ago**; Middle East routes $35. Murban-over-Basrah **$43/bbl vs $2 in February**. Dated Brent **+$40/bbl to WTI**, +$24 to Dubai in physical markets.
- **FACT (market reaction):** Brent rallied to $106.63 (+1.8%) and WTI $93.39 (+1.7%) Mon Oct 12; Brent held >$105 Oct 13. European low-sulphur gasoil ~**$1,412/MT ≈ $190/bbl** Nov delivery.
- **UNVERIFIED (do not trade on):** Trump's Sunday claim of a Russia–Ukraine "energy ceasefire" effective immediately — Zelenskyy says awaiting details; a similar truce last month had no confirmed effect. European diesel futures fell up to 8.3% Monday on reports Russia may ship 500,000 tons of diesel after lifting a partial export ban (fraction of last year's 28.6M tons) — Bloomberg/Moneyweb.
- **INFERENCE:** physical flows are resilient (rerouting) but the *cost* of moving oil has exploded — the market prices logistics risk, not just barrel risk. What would change it: confirmed Hormuz reopening/ceasefire → freight normalizes, Brent−WTI compresses; verified escalation (energy infrastructure hit — none yet per ING) → front spikes, gold bids.
- Sources: UKMTO/Kpler via engine.online and Morningstar/DJ; Goldman via DJ Newswires/Morningstar; EIA schedule page; investinglive; WSJ; Reuters (IEA Oct 14–15); Bloomberg/Moneyweb.

### Equity-index futures — quiet tape
- **FACT (Oct 13 closes):** ES=F **7853.00 (−0.06%)**; NQ=F **30770.25 (−0.41%)**. Cash: Dow −0.35% to 51,670.10; S&P 500 −0.02% to 7,805.45 (46.56 pts below early-Oct ATH 7,844.67); Nasdaq −0.15% to 27,204.38.
- **FACT (drivers):** Q3 bank earnings — JPM missed ($5.57 vs $5.90 consensus), Citi −5.5%, JNJ −6%, CAT −3.5%; memory-chip selloff on China's CXMT production-breakthrough news (MU −4.45%, SOXX −0.2%, KOSPI −5.46% overnight); Anthropic Q3 due **Wed Oct 14**. Breadth narrow: ~35% of S&P above 50-day.
- **INFERENCE:** holding pattern under ATHs, event-risk coiled not dissipated — awaiting CPI Wed 8:30 ET and Anthropic. What would change it: CPI surprise either way; Anthropic capex/AI-hardware guidance shock.

### Calendar through end of October
| Date | Event | Status |
|---|---|---|
| Wed Oct 14, 8:30 ET | **CPI (Sep)** — consensus headline +0.6% m/m, 3.6–3.7% y/y; core +0.2% m/m, 2.4–2.5% y/y (Cleveland Fed nowcast 3.6%/2.4%). Last major print before FOMC. | FACT (BLS schedule via CNBC/Polymarket previews) |
| Wed Oct 14 | API weekly petroleum bulletin (holiday-shifted); Anthropic Q3 | FACT (reported) |
| Wed–Thu Oct 14–15 | IEA board — details of G7 **100M-barrel** diesel+crude emergency release | FACT (Reuters Oct 6) |
| Thu Oct 15, 10:30 ET | EIA Natural Gas Storage (wk ended Oct 9) | FACT |
| Thu Oct 15, 12:00 ET | **EIA WPSR** (wk ended Oct 9) — Columbus Day delay | FACT (eia.gov schedule page) |
| Thu Oct 15 | PPI (Sep) — secondary-source reported; CONAB Brazil crop estimates | Reported-not-primary-verified (PPI) |
| Tue–Wed Oct 27–28 | **FOMC decision Wed Oct 28** — tracker mirrors: **~80–83% hold** at 3.75–4.00%, ~17–22% hike; Dec hike odds 67–88% across trackers | FACT that trackers report these; exact live CME number UNVERIFIED |
| Tue Nov 10 | Next WASDE | FACT |

- INFERENCE (market mechanics): a hot *core* CPI reprices Oct-28 hike odds up from ~20%; a soft core reprices December down from ~70%+.

## 6. Box/Parity Observer

**Verdict: nothing material.** No new index-methodology documents or published put-call/box parity-violation analyses found in the Oct 1–13, 2026 window (two independent web searches 2026-10-13). One search hit ("CBOE to enhance VIX index methodology by including SPX Weeklys," hedgeweek.com) is stale recycled content quoting former CEO Edward Tilly — not a new change. Parity studies returned only a 2005 box-spread article, an April 2026 NYU MFE homework, and amateur GitHub notebooks (one extracting forwards from live SPX quotes via put-call-parity regression reported no arbitrage violations). The "nothing material" verdict is FACT; the absence claim beyond search is UNVERIFIED (CBOE can publish without a search-indexable announcement).
Source: https://hedgeweek.com/news/cboe-enhance-vix-index-methodology-including-spx-weeklys-option-series

## 7. Bonds & Rates desk

Source: repo module `hedge_desk.rates_desk.rates_environment()` (mode REAL_FRED_RATES, as_of 2026-10-13). Every number below FACT from module output — never retyped from memory.

| Metric | Value | Observation date |
|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-12 |
| Fed funds change over window | +0.25 pts (60-day lookback) | 2026-08-14 → 2026-10-12 |
| Treasury 2Y (DGS2) | 4.80% | 2026-10-09 |
| Treasury 10Y (DGS10) | 5.24% | 2026-10-09 |
| 2s10s spread | 44.00 bp | 2026-10-09 |
| Curve slope | 0.055000 (UPWARD_SLOPING) | 2026-10-09 |
| SOFR | 3.87% | 2026-10-09 |
| EFFR | 3.88% | 2026-10-09 |
| OBFR | 3.88% | 2026-10-09 |
| SOFR − EFFR spread | −1 bp | 2026-10-09 |

- **Direction of change (INFERENCE on FACT observations):** 2s10s narrowed 51 bp (2026-08-14) → 44 bp — mild flattening, not steepening. Both legs rose: 2Y 4.17→4.80 (+63 bp), 10Y 4.68→5.24 (+56 bp); front end rose slightly faster, consistent with the +25 bp EFFR rise — policy repricing, not a term-premium-only move. No inversion on 2s10s. SOFR−EFFR ≈ 0 → no overnight funding stress.
- **Directional read for premium pricing (INFERENCE):** higher long rates = higher discount rates = pressure on growth multiples (NVDA, MSFT, TSLA where this bites hardest). Rate-cut expectations being unwound, not accelerated. No forced-deleveraging bid in vol from the funding channel.
- **Thesis:** rates elevated, curve gently flattening on front-end repricing; neutral-to-slightly-negative for growth-multiple premium strategies, no acute funding stress. What would change it: 2s10s through zero (inversion), SOFR−EFFR widening beyond ~10 bp sustained, or 10Y breaking materially above 5.5%. Note: FRED daily series lag one business day; Treasury levels as of Fri 2026-10-09.
