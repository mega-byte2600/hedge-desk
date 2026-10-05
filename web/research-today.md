# Hedge-desk daily research input package — 2026-10-05 (Monday, PDT)

- **Run:** `hedge-desk-daily-research` (scheduled 1:30pm PT; owner goal: `goal_e9225062b8dc`)
- **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA
- **Mandate:** research + input only; paper-only; trace claims to evidence; every number verified, every claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED; value-investor lens (mispricings, intrinsic-value gaps, margin of safety — never risk-seeking framing).
- **Data freshness by desk:** rates FRED via module 2026-10-01/02 · IV snapshot 2026-10-02 close (Friday) · futures quotes 2026-10-05 ~1:40pm PDT · earnings/dividend calendars 2026-10-05.
- **Boundaries honored:** no Risk of Ruin estimated; no trade authorization proposed; no licensed material reproduced; UNVERIFIED marked, never guessed. No git/GitHub operations.

---

## Synthesis — the 5 most decision-relevant items (not a staple)

1. **Clean runway through Oct 19, then a binary cluster.** FACT: no watchlist earnings and no watchlist ex-divs inside the window — short-dated premium written now carries no embedded binary. But the front-30d IV term structure already shows event humps: TSLA (Oct 21 AMC, issuer-confirmed), MSFT (~Oct 27–28, sources disagree on date, unconfirmed), AAPL (Oct 29). Elevated IV into these is event-inflated, NOT rich — do not read it as edge. Desk rule: premium into a binary event = avoid. Only clean front-window names: SPY, QQQ, NVDA — and NVDA's edge is thin (IV/RV 1.15).
2. **Rate regime is the growth-premium headwind.** FACT (repo rates module, FRED): EFFR 3.88% (post Sep 15–16 hike to 3.75–4.00%), 10Y 5.24% (highest in the 60-day window), 2s10s +46 bp and steepening. INFERENCE: higher long rates = higher discount rates = pressure on growth multiples (MSFT/NVDA/AAPL). 2Y at 4.78% sits ~90 bp above EFFR — the market is pricing further hikes, not a pause. October FOMC (Oct 28) + September minutes (~Oct 7) are the policy events to price; Polymarket sentiment leaned ~82% hold (sentiment, not evidence).
3. **Diesel — not crude — is the macro variable, and the curve says the crunch is temporary.** FACT: US retail diesel at a record $6.53/gal; VLCC Middle East→Asia >$1.2M/day (was ~$30k/day in January); freight/insurance ~27% of a delivered barrel (was ~3%). But WTI Dec-27 at $76.22 vs front $89.38 — steep backwardation (INFERENCE: market prices the logistics/refining dislocation resolving in ~12–18 months). Value-relevant: if it persists past November (OPEC+ Dec-levels decision Nov 1), Dec-27 is the mispricing to investigate. Transmission to watchlist is via energy-cost margin squeeze into SPY/QQQ earnings (INFERENCE) — real channel, uncertain magnitude.
4. **Week's binaries sit in energy/ag, not the watchlist:** Wednesday EIA weekly (Oct 7) and Thursday WASDE (Oct 9, 12:00 ET). FACT: corn carryover printed +173M bu surprise (bearish) while spec funds are long corn — asymmetric downside into Thursday. Ag/energy premium sellers face headline risk; same desk rule applies.
5. **Quant lab advanced, not just watched.** Two evidence-gated WATCH→TEST upgrades: #3 Wysocki (Kelly–VIX hybrid put-writing sizing) is now peer-reviewed in *Knowledge-Based Systems* — the first ledger item with a published drawdown-controlled premium-sizing framework; #5 snowjug/trading-bot MIT license declared (methodology modules only, never the live bot). New #18 (volatility-surface-lab, score 75, MIT + CI + benchmark-validated, fail-closed) gives the Premium desk an honest SVI surface + no-arb pipeline from live SPX quotes. #1 still license-blocked; #9 still code-404. Ledger updated in place (21 rows).

**Contradictions resolved:** MSFT earnings date (Trefis/TipRanks 10/27 vs WallStreetHorizon 10/28 unconfirmed) — both outside the window; date UNVERIFIED, collision real either way. TSLA earnings: Nasdaq calendar row says 10/28, but Tesla's own Oct 2 IR release says 10/21 AMC — issuer outranks aggregator; treat 10/21 as confirmed, Nasdaq row as stale (INFERENCE the row is stale, FACT they conflict). AAPL Oct 29 timing: Nasdaq calendar says "time-not-supplied" — AMC pattern is INFERENCE, not fact.

---

## Desk 1 — Earnings Event

**Verdict: no watchlist name reports inside the 2-week window (through 2026-10-19). All six OUT.**

| Name | Report date | Timing | Status | Source |
|---|---|---|---|---|
| SPY | — | ETF; no earnings | OUT | FACT |
| QQQ | — | ETF; no earnings | OUT | FACT |
| TSLA | 2026-10-21 | AMC (webcast 5:30 PM ET) — confirmed by Tesla IR release, Oct 2 | OUT (2 days past window) | FACT |
| MSFT | 2026-10-27 (Trefis, TipRanks) / 10/28 (WallStreetHorizon, UNCONFIRMED) | after market (pattern) | OUT; date UNVERIFIED — company unconfirmed | FACT of disagreement |
| AAPL | 2026-10-29 | Nasdaq: "time-not-supplied"; AMC is pattern (INFERENCE) | OUT | FACT (Nasdaq API row) |
| NVDA | 2026-11-17 | AMC — confirmed on fiscal Q2 2027 call | OUT | FACT |

**Relevant tape (FACT):** Tesla Q3 deliveries (Oct 2, 8-K): 486,532 delivered (+5.3% above company-compiled consensus; −2.1% YoY), 464,391 produced, 13.7 GWh storage (missed 15.9 GWh consensus). Stock closed +4.7% at $370.59 Oct 2. The Oct 21 release must convert the delivery beat into revenue/margin/EPS. NVDA street knowledge already priced: FY27 revenue guide $108B ±2%, gross margin guide low-end 73.5%, last print moved +8.74% (Aug 27 session).

**Implied expected moves / historical averages:** not computed — no name has earnings inside the window, so options-implied expected move per-name is not defined against an earnings expiry; historical multi-quarter averages UNVERIFIED (would require a clean price series keyed to report dates; not assembled). Fail closed.

**Takeaways:** (1) Clean runway through 10/19 — the single most decision-relevant fact of the run. (2) TSLA Oct 21 AMC is the first landmine — delivery beat + storage miss = genuine two-way setup on revenue/ASP/margin. (3) Oct 27/28–29 cluster (MSFT, AAPL) is the second wave — no premium across that week without naming the binary.

*Source notes: Nasdaq earnings-calendar API (`api.nasdaq.com/api/calendar/earnings?date=...`, queried 10/05–10/19 + 10/20–10/30, real row counts — empty watchlist rows are genuine absences, not fetch errors). Yahoo quoteSummary v10 calendarEvents 401'd on all four individual names (classified access-blocked, not transient; issuer/third-party confirmations answered the desk's question).*

---

## Desk 2 — Dividend Opportunity

**Verdict: zero watchlist ex-divs inside the 4-week window (through ~2026-11-02).**

| Name | Next ex-div | Amount | Status |
|---|---|---|---|
| MSFT | **2026-11-19** (payable 12/10) | $0.98 (raised 09/15/2026 from $0.91) | OUT of window by ~2.5 wks — flag now |
| AAPL | ≈ mid-Nov (expected w/ FY Q4 earnings late Oct) | $0.27/qtr current; declaration pending | OUT; declaration watch |
| NVDA | ≈ mid-Dec (last ex 09/10, paid 10/01) | $0.25/qtr | OUT |
| TSLA | none — pays no cash dividend (Nasdaq API rCode 200, all fields N/A) | — | FACT |
| SPY | ≈12/18/2026 (last 09/18, $1.889) | — | OUT |
| QQQ | ≈12/21/2026 (last 09/21, $0.751) | — | OUT |

**Consecutive-increase counts (per `~/workspace/hedge-desk-research/dividend-count-standard.md` — read this run):** MSFT **24 consecutive annual increases (incl. the Sep 2026 raise to $0.98/qtr)** — FACT, anchored; do not drift. AAPL and NVDA streak counts UNVERIFIED against issuer IR (raises visible in Nasdaq data: AAPL $0.25→$0.26 in 2025, $0.26→$0.27 on 04/30/2026; NVDA $0.01→$0.25, +2,400%, announced 05/20/2026). No increases, cuts, or specials announced inside the window.

**Value-lens observations:** MSFT is one more raise (expected ~Sep 2027) from the 25-year Dividend Aristocrat threshold (INFERENCE re: index mechanics). NVDA now pays ~$25B/yr on a ~6% payout ratio — FCF durability signal far beyond the sub-0.5% headline yield (INFERENCE).

**Takeaways:** (1) Clean October — no early-assignment dividend-capture risk this month. (2) MSFT assignment window opens 11/19 ($0.98): deep-ITM call writers plan early-exercise economics now. (3) AAPL declaration watch: board action with late-Oct earnings; note whether the $0.27/qtr rate is raised again.

---

## Desk 3 — Overnight Premium / IV

**Data date: Friday 2026-10-02 close** (Monday session UNVERIFIED). IV = AlphaQuery 30/60/90d IV mean (avg of put/call). RV20 = 20-day log-return vol × √252 from Yahoo closes (desk-computed). **IV rank = UNVERIFIED for all names** — no free IV-history source; AlphaQuery 52-week rank paywalled. Never guessed.

**Macro backdrop:** VIX 15.52, VIX9D 12.85, VIX3M 18.00 — FACT (Yahoo). Term proxies in normal contango. Low-vol regime; absolute index premium thin (INFERENCE).

| Name | Spot | RV20 | IV30 | IV60 | IV90 | IV30/RV20 | Curve | Event in 30d window? |
|---|---|---|---|---|---|---|---|---|
| SPY | 774.83 | 10.50 | 12.89 | 13.65 | 14.28 | 1.23 | contango | no |
| QQQ | 756.20 | 15.39 | 18.90 | 19.74 | 20.52 | 1.23 | contango | no |
| AAPL | 332.89 | 20.91 | 25.70 | 25.30 | 25.11 | 1.23 | mild backwardation | YES — 10/29 |
| MSFT | 525.18 | 21.26 | 32.49 | 30.43 | 29.05 | 1.53 | backwardation | YES — ~10/27–28 |
| NVDA | 238.90 | 25.52 | 29.33 | 34.41 | 34.30 | 1.15 | front contango, 60d hump | no (11/17 in 60d) |
| TSLA | 378.73 | 32.56 | 43.20 | 41.27 | 40.90 | 1.33 | backwardation | YES — 10/21 confirmed |

**Event-hump verdicts (INFERENCE, with what would change them):** MSFT IV30 32.5 vs realized ~21 — widest gap on the board, but backwardated curve = classic event signature; event-inflated, not mispriced. TSLA IV30 43.2 ≈ 30d HV — fairly priced given realized + event; note **flat skew (~0) into Oct 21 earnings** — flattening into an event can signal upside-chase positioning (INFERENCE; watch for skew steepening as a positioning tell). NVDA is the cleanest read: 1.15x, no 30d event, contango — but the edge is thin, not a fat pitch.

**Parity sanity:** ATM put/call IV ratios 0.98–1.01 across all six — no parity anomalies visible at ATM level (FACT about this data; not a full chain audit).

**Takeaways:** (1) TSLA, MSFT, AAPL front IV is event-inflated — avoid premium into those binaries. (2) Best IV-vs-realized setup is NVDA (1.15x, no event) but modest. (3) Index premium is thin; single names carry the game. (4) TSLA skew flat into earnings = positioning tell to watch.

*Methodology/failures: Yahoo v7 options endpoint 401'd on all names even with the mandated UA header (classified genuine dead end for unauthenticated pulls; AlphaQuery free IV pages used as fallback). CBOE delayed quotes 403; Nasdaq option-chain API returned headers only; MarketChameleon JS-shell. IV rank UNVERIFIED per standing rule.*

---

## Desk 4 — Open Quant/AI Model Lab

**New candidates (all appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` — standard work; ledger verified on disk: 21 rows, #18–#21 new):**

| # | Candidate | Score | Disp. | Reason |
|---|---|---|---|---|
| 18 | elmarfarajov/volatility-surface-lab — SVI surface + Heston calibration + delta-hedging lab (GitHub, 9/16) | 75 | TEST | MIT, CI green, 107 tests/98% coverage, 16 numerical checks vs published benchmarks, fail-closed IV inversion; serves Premium desk directly |
| 19 | diegoperezsoto/ssvi_volatility_visualizer | 34 | ARCHIVE | live-trading bot framing — paper-only mismatch |
| 20 | Yang et al. — Universal Diffusion Models for IV Surfaces (arXiv:2609.22893v1, Sep 2026) | 48 | WATCH | transfers to unseen stocks w/o retraining; beats VolGAN on arb violations; no code link — reproducibility not established |
| 21 | Bajalica/Brooks — Latent Flow Matching for arb-aware IV generation (Paris Dauphine; arXiv:2608.00616 mirror) | 45 | WATCH | found via third-party mirror; canonical arXiv record UNVERIFIED |

**Follow-ups on existing items:** #1 sp500-walkforward-harness — BLOCK UNCHANGED (still no LICENSE, all-rights-reserved). #2 cme-fedwatch — condition 1/4 met; INTEGRATE needs builder-side conditions (pin 0.2.1, exception wrap, ≤5d history). **#3 Wysocki — WATCH→TEST (63→74): now peer-reviewed (*Knowledge-Based Systems*, DOI 10.1016/j.knosys.2026.116331); first ledger item with a published drawdown-controlled premium-sizing framework.** **#5 snowjug/trading-bot — WATCH→TEST (61→69): MIT license declared; sandbox the CPCV/PBO/DSR modules only, never the NSE-India live bot.** #9 Buchegger & Gonon — BLOCK UNCHANGED (code repo still 404). #4, #7, #8, #13, #14, #15, #11, #6: no new advancement; #13 relevance confirmed (cited by new #20).

**Desk-wide signal:** the diffusion-IV cluster is converging — three arXiv items (#9, #20, #21) attack arbitrage-aware generative IV surfaces and #20 cites #13 (latent no-arb geometry). Worth one integrated read when #9's code lands. Negative-result methodology keeps compounding (#1: SPY buy-and-hold beats 1,510 configs; #5: DSR deflates nominal Sharpes; #8: IC≈0 across 6 paradigms × 3 markets) — the falsification standard: deflated-Sharpe + purged-CV proof before any strategy earns a hearing.

*All dispositions from the repo's own `hedge_desk.research_intelligence.assess_source`, run live. No GitHub operations (read-only fetches).*

---

## Desk 5 — Futures Event (weather/war/logistics catalysts)

**Fresh catalysts (FACT, sourced):**

- **Yemen/Bab el-Mandeb escalation (today):** Saudi-backed Yemeni forces claim seized positions on the Bab el-Mandeb Strait (Reuters 10-05); Kpler: Persian Gulf crude exports averaged 18.3M bpd end-Sept (above ~18M pre-war rate, Saudi pipeline diversion); 7 attacks past week in Hormuz/Gulf of Aden (UKMTO). US reportedly sending a third carrier group; Trump told Axios/Fox he is "considering a massive attack. Bigger than ever before" on Iran (TradingEconomics 10-04). War began late Feb 2026; Brent rose from ~$73 pre-war to above $100 (TBS News 10-04).
- **OPEC+ (Oct 4):** seven core members held November quotas unchanged (pause on increases extended); pumped ~25M bpd in Aug — up 630k m/m but still ~5M bpd below pre-war Feb. Next meeting Nov 1 (Dec levels); full OPEC+ Nov 29 (2027 policy).
- **G7 (Oct 2):** agreed 100M-bbl crude+diesel reserve release over four months; pledged no energy export restrictions among G7.
- **Logistics is the binding constraint (Reuters column 10-05):** freight/insurance ~27% of a delivered barrel (was ~3%); VLCC Middle East→Asia >$1.2M/day (from ~$30k/day January, Poten & Partners); Middle East/Russia refining losses compounding, especially diesel.
- **Diesel at records:** US avg $6.529/gal (DOE/EIA), +$1.90 since early July, vs ~$3.76 pre-war; European diesel highest since 2005 (GLN 10-05).
- **EIA weekly (released ~Sep 30; next Wed Oct 7):** crude +0.9M to 427.3M; gasoline −1.7M; distillates −2.3M; refinery utilization 92.5% (−1.5pp); Cushing +0.55M.
- **Nat gas: US isolated:** Henry Hub storage 3,351 Bcf (~95 Bcf above 5-yr avg); EIA projects 3,969 Bcf by Oct 31 — highest end-Oct in a decade; LNG feedgas record 18.1 Bcfd but terminals at capacity; TTF €74.06 (+135% YoY); ~19% of global LNG historically transited Hormuz.
- **Metals:** gold ~$4,216 (10/2), up ~1% Friday after weak payrolls (+29k vs ~88–90k expected; unemployment 4.2%) cut October Fed-hike odds to mid-teens; touched ~$4,689 early October (Jan peak ~$5,608). Silver ~$61.75.
- **Ag calendar: WASDE Thursday Oct 9 (12:00 ET):** Sep 30 grain stocks — corn carryover +173M bu surprise (bearish); soybeans as expected; wheat modestly supportive. China keeps 10% soybean tariff; Brazil/Argentina priced $40–50/ton below US offers.

**Curve snapshot (Yahoo, 2026-10-05 ~1:40pm PDT; FACT quotes, INFERENCE reads):** WTI Nov $89.38, Dec $88.14, Mar-27 $84.72, Dec-27 $76.22 — steep backwardation (INFERENCE: pricing near-term scarcity + normalization ahead; what changes it: Hormuz resolution/escalation, OPEC+ Nov 29 2027 signaling). Brent front $100.42 (prev close 103.53, −3.0%); Brent–WTI spread ~$11 = localized tightness pricing, not global shortage. Nat gas Nov $3.07 (Henry Hub isolated from $29.56 Asian LNG — ~10x gap, liquefaction capped). Gold Dec $4,166.30 / silver Dec $61.40 — consolidating, not panicking. Corn Dec 497.5¢ with spec funds long into the +173M carryover surprise = asymmetric downside into Thursday WASDE (FLAG).

**Transmission to watchlist (real channels only):** energy-cost channel (record diesel/freight → margin squeeze, macro headwind for SPY/QQQ earnings — INFERENCE); geopolitical risk premium stays fat (INFERENCE); supply chain (port congestion, German port strikes, Rhine restrictions, Red Sea rerouting — TSLA Berlin exposure previously reported, INFERENCE on current magnitude).

---

## Desk 6 — Box/Parity Observer

Quiet day. **FACT (fresh):** Cboe and S&P DJI announced 2026-09-29 an extension of the exclusive S&P 500 index-options licensing pact through 2051 (previously through 2032/2033), with tokenized options named as exploratory — no filing, venue, or settlement design disclosed. SPX settlement conventions unchanged: standard SPX AM-settled; SPXW/XSP PM-settled (IBKR reference). The widely re-crawled Hedgeweek "PM-settled XSP launch" piece is STALE (describes the completed 2024 AM→PM migration) — do not treat as news. No new index-methodology docs or institutional parity-violation analyses surfaced. **INFERENCE:** the 2051 extension reduces tail risk of SPX-options fragmentation; no effect on box pricing math; tokenized language is exploratory only.

---

## Desk 7 — Bonds & Rates

**Module status: SUCCESS** — `rates_desk.rates_environment()` exit 0, schema `hedge-desk-rates-desk-1.0.0`, mode `REAL_FRED_RATES`. All numbers FACT, sourced to the module's FRED pull; none retyped from memory.

| Item | Level | Series date |
|---|---|---|
| Fed funds effective rate (EFFR) | **3.88%** | 2026-10-01 |
| 10Y Treasury (DGS10) | **5.24%** | 2026-10-01 |
| 2Y Treasury (DGS2) | **4.78%** | 2026-10-01 |
| 2s10s slope | **+46 bp**, UPWARD_SLOPING | 2026-10-01 |
| Fed funds change, 60-day window | **+25 bp** (Sep 15–16 meeting: range → 3.75–4.00%) | measured |
| SOFR / EFFR / OBFR | 3.88% / 3.88% / 3.88% | 2026-10-02 |
| SOFR−EFFR spread | **0 bp** — no funding stress | — |

**Direction:** steepening — 2s10s widened from ~32 bp (9/28) to +46 bp (10/01); 10Y rose 4.69→5.24 (+55 bp) and 2Y ~4.25→4.78 (+53 bp) over 60 days (parallel-ish bear shift). 2Y sits ~90 bp above EFFR — the market prices further hikes, not a pause. **Next FOMC: Oct 27–28** (verified federalreserve.gov); September minutes expected ~Oct 7.

**Directional read for premium pricing (INFERENCE):** higher long rates = higher discount rates = downward pressure on growth multiples (MSFT/NVDA/AAPL premium faces a rate headwind; IV appetite for high-multiple names compresses as the equity risk premium narrows). Orderly overnight markets (0 bp spread) imply no box/parity dislocation signal. **What would change it:** cooling CPI/PCE, dovish October FOMC, or 2s10s flattening back to the low-30s.

---

## Data gaps / UNVERIFIED list (fail-closed, by name)

1. IV rank — all six names (no free IV-history source; AlphaQuery 52-week rank paywalled).
2. Historical average earnings-day moves — all names (requires multi-quarter price series keyed to report dates; not assembled).
3. AAPL full consecutive-dividend-increase streak (issuer IR not checked).
4. NVDA full consecutive-dividend-increase streak (third-party "three years" claim unverified against issuer IR).
5. MSFT earnings date confirmation (~10/27 vs 10/28; company unconfirmed).
6. AAPL earnings timing (Nasdaq "time-not-supplied"; AMC is pattern inference).
7. TSLA Nasdaq calendar row (10/28) vs issuer IR (10/21 AMC) — conflict resolved in favor of issuer.
8. VIX futures curve (no accessible Yahoo ticker; CBOE 403); VIX9D/VIX3M proxies used.
9. Canonical arXiv record for new candidate #21 (found via third-party mirror).
10. Flugum et al. full SSRN paper (not located).

## Desk status ledger

| Desk | Status |
|---|---|
| 1 Earnings Event | DONE |
| 2 Dividend Opportunity | DONE |
| 3 Overnight Premium / IV | DONE (with source-failure fallbacks classified) |
| 4 Open Quant/AI Model Lab | DONE (ledger updated: rows #18–#21 added, #1/#2/#3/#5/#6/#7/#8/#9/#11/#13/#14/#15 status notes) |
| 5 Futures Event | DONE |
| 6 Box/Parity Observer | DONE |
| 7 Bonds & Rates | DONE (FRED module succeeded; no substitution) |

No desk produced nothing; no desk was silently dropped.

---

## Source index (verbatim URLs per desk)

- Earnings: `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD` (10/05–10/30 sweep); Tesla IR via https://www.morningstar.com/news/business-wire/20261002169209/tesla-third-quarter-2026-production-deliveries-deployments; trefis.com (MSFT 10-01, NVDA 09-27); wallstreethorizon.com; MarketBeat.com NVDA call transcript; stocktitan.net (NVDA +8.74%).
- Dividend: `https://api.nasdaq.com/api/quote/{MSFT,AAPL,NVDA,TSLA}/dividends?assetclass=stocks`; `https://api.nasdaq.com/api/calendar/dividends?date=...`; Yahoo chart events=div; dividend-count-standard.md; unite.ai; global.morningstar.com (NVDA hike); finbold; zacks.com AAPL history.
- IV: AlphaQuery free volatility pages (all six names, 2026-10-02 close); Yahoo chart API (VIX 15.52, VIX9D 12.85, VIX3M 18.00; spot + RV20).
- Quant lab: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (21 rows); repo scorer `hedge_desk.research_intelligence.assess_source`; arXiv:2609.22893v1; GitHub volatility-surface-lab repo page.
- Futures: Reuters 10-05 (Bab el-Mandeb; oil logistics column); CNN 10-04 (Yemen); NY Post 10-05 (Gulf exports); TradingEconomics 10-04/10-05 (crude news); TBS News 10-04 (OPEC); TradingView/Seeking Alpha 10-04 (OPEC quotas); SKN Finance; HAAWKS (EIA 09-30); TradingNews Oct-01/Sep-2026 (nat gas); IndexBox/Kitco 10-02 (gold/payrolls); TS2.tech; farmdoc Illinois WILLAg Week 40; Barchart cmdty WASDE preview; commodity-board.com; africaports.co.za; blog.globalialogisticsnetwork.com.
- Box/parity: crypto.news 09-29 (Cboe–S&P 2051 extension); thecoinrepublic.com 09-30; interactivebrokers.com.hk CBOE page (settlement conventions).
- Rates: repo `hedge_desk.rates_desk` (FRED DFF/DGS10/DGS2/SOFR/EFFR/OBFR); federalreserve.gov (FOMC calendar).
