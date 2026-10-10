# Hedge-desk daily research package — Sat 2026-10-10 (~1:30pm PDT)

Research and input only — paper-only context. Saturday run: markets closed; all market data is Friday 10-09 close (or FRED 10-08), labeled explicitly throughout. Nothing below is presented as Saturday data. Labels: **FACT** = verified this run; **INFERENCE** = reasoned from facts; **SPECULATION** = ungrounded extrapolation; **UNVERIFIED** = could not verify, failed closed.

---

## SYNTHESIS — the 5 most decision-relevant items

1. **TSLA Oct 21 AMC is the lone earnings event in the window — priced slightly rich on its own base rate, and it's a binary event to avoid.** Oct-23 straddle prices ±7.5% vs. ±6.0% average absolute next-session move over the last 4 quarters; the Jul 2026 −14.5% print dominates the trailing window (window-contingent caveat). Earnings premium isolated in quadrature terms at roughly ±6.2% (pre-earnings Oct-16 straddle only ±4.1%). (FACT: date confirmed by 3 sources — TipRanks "After Close (Confirmed)", signalysis, Capket; Nasdaq sweep of all 11 days in window found no other watchlist hits.) Consensus to use: **$0.45** (TipRanks, 27 analysts) — Nasdaq's $0.23 is stale. Q3 deliveries (486,532) are public; the trade is the guide + AI/robotaxi/Optimus commentary, not the print. (INFERENCE; what would change it: straddle repricing into Oct 21, or a guide that resets the narrative.)
2. **Rates regime: EFFR 3.88% (+25bp over 60 days), 10Y 5.22%, 2Y 4.75%, 2s10s +47bp, SOFR−EFFR −1bp (no funding stress).** Both ends eased off peaks (10Y 5.31 on 10-05 → 5.22) but the 60-day trend is a sustained bear-steepening from 4.7% 10Y in mid-August. (FACT, FRED via rates_desk module, series through 2026-10-08.) INFERENCE: rates are priced higher-for-longer, not a cut cycle — the margin-of-safety bar for long-duration exposure (NVDA/TSLA/QQQ) stays high; overnight markets show no disorderly-liquidity signal into next week.
3. **CPI Wed Oct 14 (8:30am ET) is the named macro catalyst, with headline risk skewed up and core as the policy line.** Futures desk: Brent ~$103, backwardated, with 71.5% of Gulf oil production shut in by Hurricane Isaias (~1.46M bpd) against 100M bbl of strategic releases + a US–Russia diesel waiver — a two-sided energy binary into the print. WASDE (Oct 9) was a bearish grain surprise (corn yield 181.2 bpa, ending stocks 1,849M bu, near limit-down) — food-at-home disinflation for the headline, but policy trades core. Dec-hike pricing repriced 68%→~80% on oil escalation (per the cpi-conditional addendum; the FedWatch re-baseline guard band — 82.3% Oct hold / 81.3% Dec hike — stays staged until the user's manual CME cross-check). Core MoM ≤0.2% unwinds the hawkish repricing; ≥0.3% hard-confirms it.
4. **No actionable IV-vs-realized signal this run.** Five of six 20-day realized windows are WINDOW-CONTINGENT (SPY 32.5%, QQQ 41.9%, AAPL 37.9%, MSFT 36.2%, TSLA 31.0% max-day variance share — all above the 30% line), so no clean cheap/rich verdicts. The only clean window is NVDA (23.8%): 6-DTE IV 29.1% vs 20d realized 25.8% — mild premium, not a mispricing. (FACT values; INFERENCE verdict.) IV rank is UNVERIFIED for all six — no free IV-history source; never guessed. Data provenance: iv-inputs file as_of 2026-10-09T13:59 PT (~23.5h old, outside the 18h guard but the latest market-day pull — labeled Friday-close); Friday's 0DTE chain is purged so exact re-verification was impossible — the proxy term-structure check (smoothly rising curves on the 10-12 and 10-16 expiries) passed.
5. **Quant lab's strongest find: options-lab (#50, 61 WATCH) — an MIT repo running arb audits of SVI vs SSVI/eSSVI on a live SPX chain plus a 1990–present variance-sold-at-VIX history (Sharpe 1.19, skew −6.17).** Direct feed for the premium desk's IV-regime screens; sandbox before Monday's run. Also: Subrahmanyam's PEAD design critique is now a real SSRN paper (drift t=2.18 all-stocks → 1.43 ex-microcaps) — the Earnings desk should treat residual post-earnings drift expectations for large-cap watchlist names with high skepticism. (INFERENCE; full paper not read, per UCLA Anderson Review summary.) No dividend or parity events: MSFT's $0.98 Nov-19 ex-div is confirmed but lands OUTSIDE the 4-week window (correction to the desk's "in window" label — see §2).

---

## 1. Earnings Event desk

One watchlist name reports inside the 2-week window (through Fri Oct 23).

| Name | Report date | Timing | Implied move | Historical avg earnings-day move | Source |
|---|---|---|---|---|---|
| TSLA | **Wed 2026-10-21** | After hours (confirmed: TipRanks, signalysis, Capket) | **≈ ±7.5%** — Oct-23 expiry ATM straddle mid $28.80 (call $14.83 + put $13.98) ÷ $382.70 spot | **−4.8% signed / ±6.0% absolute** next-session close-to-close over last 4 quarters | Nasdaq earnings calendar API (all 11 days swept); Nasdaq options chain; Yahoo chart (spot/history). as_of Fri 2026-10-09 close |
| AAPL | Nov 2 (announced) | AMC | Outside window — not computed | — | Apple IR / prior packages |
| MSFT | Oct 28 | AMC | Outside window — not computed | — | Nasdaq calendar API |
| NVDA | Nov 18 | — | Outside window — not computed | — | Nasdaq calendar API |
| SPY / QQQ | — | — | — | ETFs — no earnings (FACT) | definitional |

**TSLA history (last 4, next-session):** Oct 22 2025 +2.3% ($0.50 vs $0.56 miss); Jan 28 2026 −3.5% ($0.50 vs $0.46 beat); Apr 22 2026 −3.6% ($0.41 vs $0.35 beat); Jul 22 2026 −14.5% ($0.33 vs $0.53 miss). (FACT: Yahoo chart closes; beat/miss vs TipRanks consensus history.) The Jul −14.5% print is window-contingent on a miss, not a clean quarter — the verdict that ±7.5% is rich-vs-base-rate changes if that outlier is judged unrepresentative.

**Consensus correction:** use **$0.45** (TipRanks, 27 analysts, updated ~Oct 10; fiscal.ai agrees), not Nasdaq's stale $0.23. Q3 deliveries 486,532 units are public (Oct 2 operating update — FACT). No release to read yet; when it prints, read in order: guidance vs consensus → GAAP net income vs headline adjusted → cash flow (OCF vs net income) → automotive gross margin ex-regulatory-credits → energy revenue vs 13.7 GWh deployments → balance-sheet deltas.

**Premium-desk note:** Oct-16 (pre-earnings weekly) straddle implies ±4.1% — no binary-event premium in the front week; the jump to ±7.5% on Oct 23 isolates the earnings premium at roughly ±6.2% in quadrature.

---

## 2. Dividend Opportunity desk

**Headline: no watchlist name has an ex-dividend date inside the 4-week window (Oct 10 – Nov 7, 2026).** (FACT — 28-date Nasdaq dividends-calendar sweep, zero hits.) **Correction to the desk's draft:** the desk labeled MSFT's Nov 19 ex-div "(in window)" — Nov 19 is 12 days past the window edge. Confirmed facts stand; only the window label is corrected here. No increases, cuts, or specials announced this week on any watchlist name.

| Symbol | Next ex-date | Amount | Payment | Change | Consecutive-increase count | Source + as_of |
|---|---|---|---|---|---|---|
| MSFT | **Thu Nov 19, 2026** (declared Sep 15, 2026) | **$0.98** (+7.7% over $0.91) | Dec 10, 2026 | First payment at raised level | **24 consecutive annual increases** (per dividend-count-standard.md; do not drift to 23) | Nasdaq dividends API, fetched 2026-10-10; as_of Fri 10-09 |
| AAPL | Not yet declared (Nov ex-div expected ~2nd week, with late-Oct earnings declaration) | Last $0.27 (ex 08-10-26) | — | None since Apr 30, 2026 raise to $0.27 | UNVERIFIED (issuer IR not re-pulled; not claimed) | Nasdaq + Zacks; as_of 10-09 |
| SPY | Nothing in window; next ~Dec 2026 (quarterly) | Last $1.889 (ex 09-18-26) | — | None | n/a (ETF) | Yahoo actions (UA header); as_of 10-09 |
| QQQ | Nothing in window; next ~Dec 2026 | Last $0.75143 (ex 09-21-26, paid 10-08) | 10-08-26 | None | n/a (ETF) | Nasdaq dividends API; as_of 10-09 |
| NVDA | Nothing in window; next ~Dec 2026 | Last $0.25 (ex 09-10-26) | — | $0.01 → $0.25 raise stands as standing catalyst (FACT per Nasdaq) | n/a for decision purposes | Nasdaq dividends API; as_of 10-09 |
| TSLA | None — pays no dividend (FACT) | — | — | None | n/a | Nasdaq dividends API |

**Premium-desk flag (INFERENCE):** MSFT's Nov 19 ex-div falls one day before Nov-20 monthly expiry — standard dividend-capture / early-exercise timing risk for ITM Nov calls. AAPL's November ex-div is UNVERIFIED timing — declaration comes with earnings (~late Oct).

---

## 3. Overnight Premium (IV) desk

**Data provenance (explicit).** iv-inputs file as_of 2026-10-09T13:59 PT (~23.5h old) — OUTSIDE the 18h freshness guard, but the latest market-day pull (markets closed Saturday), so it stands as **Friday-close data**, labeled as such in every row. Spot-verification: Friday's 0DTE (10-09) chain is purged post-expiry, so exact re-verification of the file's 0DTE IVs is impossible. Proxy check via live Yahoo options pull (crumb flow + UA header): the 10-12 (2 DTE) and 10-16 (6 DTE) expiries show smoothly rising term structure in every name, with the file's 0DTE readings sitting plausibly at the 0-DTE end of each curve → **PROXY-CONSISTENT, not exact-match verified**. IV rank: **UNVERIFIED** for all six — no free IV-history source; never guessed.

### Snapshot (all Friday-close; as_of 2026-10-09T13:59 PT)

| Symbol | Front ATM IV (0DTE, file) | 20d realized | Window-contingent? | IV-vs-realized verdict + label | Earnings inside window? |
|---|---|---|---|---|---|
| SPY | 1.04% | 10.02% | YES (32.5%) | No clean verdict — WINDOW-CONTINGENT; 0DTE-vs-20d is a DTE artifact | None |
| QQQ | 1.50% | 15.96% | YES (41.9%) | No clean verdict — WINDOW-CONTINGENT; 0DTE artifact | None |
| AAPL | 6.51% | 16.24% | YES (37.9%) | No clean verdict — WINDOW-CONTINGENT | Nov 2 (inside ≥11-02 expiries, not front week) |
| MSFT | 3.49% | 21.91% | YES (36.2%) | No clean verdict — WINDOW-CONTINGENT | Oct 28 (inside ≥10-28 expiries) |
| NVDA | 2.15% | 25.80% | NO (23.8% — clean) | Mild premium: 6-DTE live IV 29.1% vs 20d 25.8% — INFERENCE, not a mispricing | Nov 18 (back-month; no front-week hump) |
| TSLA | 3.36% | 30.50% | YES (31.0% — just over the line) | No clean verdict — WINDOW-CONTINGENT; 0DTE artifact | **Oct 21 — inside any expiry ≥ 10-21. Premium into this binary = avoid** |

### Live Friday-quote term-structure anchors (Yahoo, UA header, served Saturday)

| Symbol | 10-12 (2 DTE) ATM IV | 10-16 (6 DTE) ATM IV | Underlying (Fri close) |
|---|---|---|---|
| SPY | 5.70% | 9.71% | 778.57 |
| QQQ | 8.73% | 14.77% | 751.27 |
| AAPL | 16.16% | 22.83% | 336.64 |
| MSFT | 18.62% | 23.77% | 535.07 |
| NVDA | 19.31% | 29.08% | 229.28 |
| TSLA | 23.48% | 37.73% | 382.70 |

All six curves rise with DTE (FACT) — normal term structure, no inversion; TSLA's elevated front IV is consistent with Oct-21 earnings proximity, not "richness" (INFERENCE). What would change the verdicts: a Monday pull with a live non-zero-DTE front expiry, re-screened 20d windows, and Earnings-desk confirmation (cross-checked: TSLA Oct 21 confirmed — see §1).

---

## 4. Open Quant/AI Model Lab

Scored with the repo's own `assess_source`; band discipline held (nothing inflated into TEST on interest alone).

### New candidates (ledger rows #49–53 appended to ~/workspace/hedge-desk-research/quant-lab-ledger.md — verified on disk)

| # | Candidate | Score | Disp. | Why |
|---|---|---|---|---|
| 49 | Schneider/Looser/Garin/Liu/Kuhn — WRAP: adversarial training for deep hedging in nonstationary markets (DRO), arXiv:2610.07162v1 | 36 | ARCHIVE | Preprint; no author code link on arXiv abs page (verified at source); hedging-policy learning — marginal desk fit |
| 50 | emiliensabathier/options-lab — arb-free SVI/SSVI/eSSVI fitted to a real SPX chain (2026-10-05, 7,425 OTM quotes, grid arb audit) + variance risk premium history since 1990, GitHub, MIT | 61 | WATCH | README verified at source: eSSVI zero-arb on 238 archived sessions (source-reported); VRP: selling 30d variance at VIX since 1990, Sharpe 1.19, skew −6.17, COVID worst window ≈ 3 years of avg gains (source-reported, UNVERIFIED — read, not run). Sandbox next |
| 51 | FaiyazEnayet/deep-hedging-lab — from-scratch deep hedging (Buehler et al. 2019): NN hedgers under transaction costs/stoch vol/jumps, GitHub, MIT | 52 | WATCH | README verified at source (GBM/Heston/Merton simulators, CVaR/entropic objectives — source-reported, UNVERIFIED). Sandbox: run test suite, hedge-error vs BS delta |
| 52 | blaquebaux/bight — 25-delta risk-reversal skew mean-reversion stub | 22 | ARCHIVE | STUB/DATA-BLOCKED — no code, no backtest; honest null stated. Reopen if built |
| 53 | blaquebaux/broaching — post-event vol-bleed stub (short-dated straddles after earnings/FDA) | 22 | ARCHIVE | Same stub state. Reopen if built |

Triage exclusions (no ledger rows; recorded in the Jidoka log): 8 GitHub repos rejected on NOLICENSE/crypto/IBKR-dependency/bot-framing grounds; arXiv 2610.11691 (market impact, no options relevance); 2610.09613 (residual asset pricing, no vol/options relevance).

### Re-check outcomes (remaining items without 10-10 notes)
- **#10 Subrahmanyam (PEAD design critique):** full paper located — SSRN 5930255. Per UCLA Anderson Review summary: PEAD t=2.18 all-stocks vs 1.43 excluding microcaps (INFERENCE from secondary summary — full paper not read). Working paper, not peer-reviewed. Stays WATCH.
- **#12 Dong (dividend-growth state-space):** full paper located — Hang Dong (UGA), FMA Taipei 2026 program paper 206; Kalman extraction of dividend-growth expectations from dividend futures (source-reported, UNVERIFIED). Requires proprietary OTC dividend futures — not replicable on desk data. Stays WATCH.
- **#37 DaniyalMlk/holdout:** PyPI `holdout` still v0.3.0 with the same collision summary ("Preserve the dissenting reasoning behind contested decisions") — not the author's release; repo unchanged (pushed 2026-10-05). Stays WATCH.
- **#39 QuantOracle:** repo README read in full at source — MIT confirmed; 63 deterministic calculators + 10 composites, zero market-data dependencies (math-only); free tier 1,000 calls/IP/day no-key confirmed. Rescored 63→WATCH (band unchanged). **Decision-relevant correction:** it is a pure-math calculator API, not a data API — useful as a parity/Greeks reference calculator only; it does NOT fill the IV-rank data gap.

---

## 5. Futures Event desk (catalysts)

### WASDE Oct 9, 2026 (released 12:00 ET, confirmed on usda.gov release page)
FACT (figures via five-source post-release consensus — DTN, HAAWKS structured feed, ADMIS, Brownfield, Teucrium; raw USDA PDF fetch failed, not line-verified):
- **Corn — bearish surprise.** Yield 181.2 bpa (+2.7 vs Sep; trade expected a cut), 2nd highest ever. Production 16,034M bu (+234M; ~315M above survey avg). 2026/27 ending stocks **1,849M bu** (+282M vs Sep; +172M above survey avg). Avg farm price cut $0.10 → $4.70. Corn traded near its $0.30 daily limit on release. INFERENCE (ADMIS): "prices must fall to stimulate demand in a hurry."
- **Soybeans — neutral.** Yield 53.1 bpa (record, +0.3). Ending stocks 315M bu (+5M). Farm price $12.00, unchanged. Exports raised 10M on Chinese buying.
- **Wheat — neutral-to-bearish.** Ending stocks 740M bu (+23M); exports cut 25M. Farm price $6.30 (−$0.10). Global: corn 280.4 mmt (+8.3), soy 124.3 mmt (+0.3), wheat 276.0 mmt (−0.3). Next WASDE: Nov 10.

### Curve read (as_of Sat Oct 10; futures closed, quotes = Friday Oct 9 closes unless noted)
- **Crude:** WTI Nov ~$90–93, Brent Dec ~$103–105 as_of Oct 10 (tape conflicts across sources — precise level UNVERIFIED). Term structure backwardated (Brent Dec ~$102.8 vs Jan-27 ~$98.25, Oct 8 — INFERENCE: prompt tightness still priced). **EIA weekly (Oct 7 report, week ending Oct 2):** commercial crude −3.2M to 424.1M bbl (1% above 5-yr avg); Cushing +444k to 24.7M; gasoline +400k; distillates ~flat, 12% below 5-yr avg; refinery util 92.7%; US production ~14M bpd. Pre-hurricane data — next two prints will be Isaias-distorted.
- **Nat gas:** November ~$3.20 (+3% on Gulf shut-ins, Oct 8). INFERENCE: psychology/timing, not structural — Gulf gas is a small slice of Lower-48 supply.
- **Metals:** Gold spot ~$4,182 (late Fri NY); Dec COMEX $4,212.20 — ~$30 spot-to-Dec carry = normal contango at 4% policy rates. Gold ETFs at record 4,256t after 67t Sept inflows; China central bank +740k oz Sept (largest in 3 yrs). ~25% below the January $5,595 record, inside a $159 band since Sept 28 — a bounce inside a downtrend, bought by ETFs/official sector (INFERENCE). Silver ~$60.13 (Oct 7, Kitco — stale).

### Weekend geopolitical triage (verified only — FACT, multi-sourced or primary-attributed)
Hurricane Isaias has shut **71.51% of US Gulf of Mexico oil production (~1.46M bpd)** (Marine Minerals Administration, Sat Oct 10). IEA/G7: 100M bbl strategic release over 4 months (G7 agreement Oct 2; US 40M bbl SPR exchanges Sept 29) — part of the earlier 400M bbl IEA program, not new commitments. Trump announced Oct 9 a US–Russia diesel deal with Treasury waiver through Apr 7, 2027 (Reuters via Atlas News); Zelenskyy criticized. Houthis claimed strikes on Riyadh's King Khalid airport (smoke reported on a stationary aircraft); earlier Riyadh/Abha attacks killed 3 (Oct 8). UKMTO: tanker struck by projectiles north of Qatar mid-week. Ukraine hit a fourth Russian refinery this week. Iran FM Araghchi: talks ongoing via mediators, response in days; Trump ruled out Iran strikes before Nov 3 midterms; blockade + fresh tanker sanctions stay. OPEC+ core: November output held. Aramco CEO Nasser: stockpiles "scarily thin," ~3bn bbl regional supply lost, >1bn bbl drawn from reserves.

INFERENCE: near-term energy is a two-sided binary — physical tightness (Isaias, Hormuz risk, thin distillates) vs policy barrels (IEA/G7, Russian diesel, SPR exchanges). SPECULATION: whether Isaias-driven Gulf tightness persists into the next EIA print; whether the diesel waiver loosens US distillate spreads before winter.

**No federal-data blackout:** USDA/EIA releases on schedule (WASDE Oct 9, EIA Oct 7 both landed). Retail-gas/diesel figures cited by one low-quality source — UNVERIFIED, not leaned on.

**CPI conditional (Wed Oct 14, 8:30am ET):** Dec-hike odds repriced 68% → ~80% on oil escalation alone (cpi-conditional addendum); the FedWatch re-baseline guard band (82.3% Oct hold / 81.3% Dec hike) stays staged until the user's manual CME cross-check. Asymmetry: core MoM ≤0.2% unwinds two days of hawkish repricing (10Y backs off, vol stays crushed); core ≥0.3% hard-confirms the hot branch.

---

## 6. Box/Parity Observer

No index-methodology changes and no new parity-violation analysis this week (CBOE/CFE notices + VIX-methodology news, Oct 5–10 sweep — FACT). The "VIX Weeklys inclusion" story in search results is a recycled old announcement; Cboe's new Futures-Options Order Type for VIX options/futures (effective Dec 14, 2026) is execution infrastructure, not a methodology change.

**One box-spread-relevant item (FACT, verified across KPMG Tax News Flash, Debevoise alert, JD Supra):** IRS Notice 2026-62 (late Sept 2026) with Rev. Rul. 2026-20 names "box-spread funds" among strategies the Treasury/IRS says may be inconsistent with the purpose of §852(b)(6). Targeted mechanism: ETFs (e.g., Alpha Architect's BOXX, ~$14.5B, now holding almost entirely long SPY boxes) that generate a Treasury-like return via non-§1256 box spreads and distribute appreciated option legs in-kind before expiry, asserting fund-level nonrecognition. The notice requests comments and signals possible further guidance (regulations, transaction-of-interest/listed-transaction designation, possibly retroactive); it expressly does not address other box-spread transactions (direct borrowing via boxes, holding boxes outright). INFERENCE: if regulatory action dents demand for box-spread ETFs, it alters the flow structure around SPY box spreads — worth the Premium desk's awareness when interpreting implied rates from box quotes, not a pricing dislocation itself. Watch for BOXX outflows or structure changes in coming weeks.

---

## 7. Bonds & Rates desk

**Status: OK** — module ran via real FRED; all numbers from module output, none from memory.

**Module output (verbatim, REAL_FRED_RATES, as_of 2026-10-10, underlying series through 2026-10-08):**
```json
{"schema_version": "hedge-desk-rates-desk-1.0.0", "mode": "REAL_FRED_RATES", "as_of": "2026-10-10", "fed_funds_effective_rate": "3.88", "fed_funds_latest_date": "2026-10-08", "fed_funds_change_over_window": "0.25", "treasury_2y": "4.75", "treasury_2y_date": "2026-10-08", "treasury_10y": "5.22", "treasury_10y_date": "2026-10-08", "spread_10y_2y_points": "47.00", "curve_slope": "0.058750", "curve_shape": "UPWARD_SLOPING", "lookback_days": 60, "sofr": "3.87", "sofr_date": "2026-10-08", "effr": "3.88", "effr_date": "2026-10-08", "obfr": "3.88", "obfr_date": "2026-10-08", "data_source": "fred-public-csv-http-200", "trade_authorized": false}
```

**Read:** fed funds effective 3.88%, up 25bp over the 60-day window; 2Y 4.75%; 10Y 5.22%; 2s10s +47bp, UPWARD_SLOPING. SOFR 3.87 vs EFFR 3.88 — spread −1bp, no funding stress. (FACT, FRED series through 2026-10-08.) Both ends eased off late-Sept/early-Oct peaks (2Y 4.92 on 9-28 → 4.75; 10Y 5.31 on 10-05 → 5.22), but the 60-day trend is a sustained bear-steepening from 4.7% 10Y in mid-August. INFERENCE: 5.2%+ 10Y keeps discount rates elevated — a structural headwind for long-duration growth multiples (NVDA/TSLA/QQQ); the −9bp pullback off the peak is relief, not a turn — the verdict changes if 10Y breaks and holds below ~5.0%. Nothing in overnight markets argues for disorderly liquidity heading into next week. Value lens: favor names whose cash flows hold up at 5%+ discount rates (MSFT, AAPL) over duration-long stories.

---

*No desk dropped. All seven sections delivered with sources and as_of labels. Paper-only; no Risk of Ruin generated or touched.*
