# Hedge-desk daily research package — Wed 2026-09-30

**Run:** hedge-desk-daily-research, 1:30pm PT. Six desks fanned out in parallel; this is the synthesized package (not a stapling). Research-only — no git ops, no trade authorization. Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED. Full desk reports: `~/workspace/goals/hedge-desk-daily-research/hidden_files/desk{1..6}_*_2026-09-30.md`.

## The 4 most decision-relevant items

1. **TSLA Q3 deliveries, Friday Oct 2 (pre-market) — the only watchlist binary event inside the 2-week window.** FACT (date): widely and independently reported; Tesla IR posted its own company-compiled consensus of **461,974** vehicles. Street spread is unusually wide: 421,758 (Cantor) to 482,000 (JPMorgan), ~13% range; Q3-2025 comp (497,099) was tax-credit-inflated. Premium-desk rule: avoid selling Oct TSLA premium into this; the 30D TSLA curve already shows the event hump (30D IV 45.7%). Would change: Tesla IR postponement or pre-announcement. (Earnings + Premium desks agree.)
2. **MSFT is the most event-inflated premium name on the board.** 30D IV 34.1% vs 24.2% realized (+9.9pp spread, clean window) with earnings estimated ~10/27–28 — INFERENCE only: MSFT's date is **not** on Nasdaq's calendar and is unconfirmed by the company; treat the timing as UNVERIFIED. AAPL 10/29 and TSLA 10/28 are confirmed (Nasdaq calendar). All three 30D curves show the binary-event hump; selling 30D premium here is selling into a binary event — avoid. Would change: post-earnings IV-crush, or MSFT confirming a date outside the 30D window. (Premium desk; date-status reconciled with Earnings desk.)
3. **Product-market squeeze, not crude surplus.** Today's EIA report: crude +922k bbl (build) vs distillates **−2.251M bbl, 14% below the 5-yr average**; heating oil +4.2%, RBOB +3.0%, retail diesel at a record **$6.53/gal**; ANZ flags a U.S. diesel export ban as an explicit risk. WTI $90.7 (+1.5% today) in steep backwardation ($90.5 → ~$77.6 down the strip). INFERENCE: today's rally on a crude build means the geopolitical premium — not inventories — is the marginal driver; the binding constraint is refined product, not crude. FACT context: a tanker was struck in the Strait of Hormuz today; U.S.-Iran talks stalled (Trump rejected a 7-day ceasefire offer); Saudi exports at 5.8M bpd, ~98% of pre-war. Watch: distillate draws into winter, the export-ban tail, and any Hormuz reopening framework (would deflate the front-month premium fast). (Futures desk.)
4. **Strongest quant-lab week in recent runs: Fed tree-SHAR IV-forecasting paper → INTEGRATE (83).** Kim & Oh, FEDS 2026.049 (July 2026): boosted tree-SHAR cuts 1-month S&P 500 IV RMSE 13% vs benchmark SHAR, stress-period robust, interpretable, reproducible materials bundle — the premium desk's next vol-input upgrade candidate. Complement: MDPI weekly-VIX HAR framework → TEST (67), a free FRED-only benchmark design with the honest negative result (persistence/HAR beats 8 ML models) — any lab ML forecaster must clear that bar first. WATCH additions: 24.6M-row free SPY chain dataset (freshness/IV-methodology/license UNVERIFIED — potential free-IV-history backup), l3a0's proxy-vs-real sign-flip measurement (+$270k on proxy-IV flips to −$184k on real chains — validates the desk's no-proxy-IV rule), options-scanner IV-excess pattern. (Quant Lab.)

**Honorable mentions:** SPX box-spread financing at record ~$146B outstanding per Cboe-cited reports, box-implied yield ~70 bps over SOFR — a live SPY Oct-30 box enforces within bid/ask, so this is segmented funding demand, not an arb (Parity desk). MSFT dividend raised to $0.98 (+7.7%, Sep 15); ex-div Nov 19 sits one day before Nov 20 monthly expiry — deep-ITM short-call early-exercise consideration (Dividend desk). SPY's +3.0pp IV−RV spread on a clean window is the only non-contingent, non-event premium observation today (Premium desk).

---

## 1. Earnings Event desk

**Window verdict: no watchlist earnings Oct 1–14, 2026.** Verified across 10 Nasdaq calendar-API dates (zero watchlist hits; as-of 13:35–13:45 PDT 9/30).

| Symbol | Next report | Status |
|---|---|---|
| TSLA | Wed Oct 28 | FACT — Nasdaq calendar |
| AAPL | Thu Oct 29 | FACT — Nasdaq calendar (IR timing details unconfirmed) |
| MSFT | ~late Oct (~10/27–28 per MarketBeat estimate) | **UNVERIFIED** — not on Nasdaq calendar; INFERENCE from FY2025 pattern |
| NVDA | ~Nov 17–25 | **UNVERIFIED** — TipRanks "TBA (Not Confirmed)" |
| SPY/QQQ | n/a | FACT — ETFs don't report |

**In-window adjacent event:** TSLA Q3 deliveries, expected Fri Oct 2 (pre-market; timing INFERENCE from pattern). Consensus 461,974 (Tesla IR-compiled, FACT as reported); Street 421.8k–482k; Q3-2025 comp 497,099 was credit-inflated. **No recent prints require a statement teardown** (latest: NVDA Aug 26). Yahoo quoteSummary 403s from this VM (known-blocked); Nasdaq API worked cleanly.

## 2. Dividend Opportunity desk

**No watchlist ex-divs in the 4-week window** (through Oct 28; Nasdaq dividends-calendar weekly snapshots, FACT as of 13:33 PDT 9/30).

- **MSFT: raised $0.91 → $0.98 (+7.7%) on Sep 15, 23rd consecutive increase.** Ex-div 2026-11-19 (one day before Nov 20 monthly expiry), payable 2026-12-10. INFERENCE: Nov-cycle deep-ITM short calls face the usual dividend-capture early-exercise pull. Yield ~0.76% — value-lens read: FCF-strength signal, not income.
- **NVDA: new $0.25 quarterly rate (2,400% raise in June) pays out tomorrow, Oct 1** (ex-div was Sep 10). Yield ~0.4%; ~$46B buybacks YTD dominate the return program. INFERENCE: immaterial for option pricing.
- AAPL: no declaration yet — INFERENCE: Nov dividend declared with late-Oct Q4 earnings (ex-div itself ~Nov 9–10, outside window). SPY ($1.889 last) and QQQ ($0.751 last) both went ex-div in September; nothing before December. TSLA: no dividend.

**October monthly cycle is free of dividend-driven exercise noise.** (FACT+INFERENCE)

## 3. Overnight Premium (IV) desk

As-of: 9/30 US close. IVs from CBOE delayed quotes (20:27–20:45 UTC); realized from Yahoo closes; Yahoo options API 401'd (known intermittent block), CBOE used as fallback. **IV-rank UNVERIFIED for all six** (no free IV-history source).

| Ticker | 30D ATM IV | 20D RV | Spread | Earnings in window | Term shape | ± move |
|---|---|---|---|---|---|---|
| SPY | 13.81% | 10.78% | +3.0pp | No | normal upward | 3.96% |
| QQQ | 19.60% | 15.11% | +4.5pp ⚠ | No | normal upward | 5.62% |
| AAPL | 26.47% | 22.80% | +3.7pp | Yes (10/29) | hump at 30D | 7.59% |
| MSFT | 34.07% | 24.15% | **+9.9pp** | Yes (~10/27–28, est.) | hump at 30D | 9.77% |
| NVDA | 31.32% | 27.17% | +4.2pp | No (Nov print) | far leg elevated | 8.98% |
| TSLA | 45.72% | 40.22% | +5.5pp ⚠ | Yes (10/28) | hump at 30D | 13.11% |

- ⚠ **WINDOW-CONTINGENT: QQQ** (9/21 +2.74% day = 36.8% of 20D variance) and **TSLA** (9/4 −6.10% day = 30.4% of variance) — their IV−RV spreads are invalid as stated; exclude the stale day or let the window roll.
- Sanity checks: all implied moves positive; put-call parity holds within bid/ask on all six (SPY +0.62 vs 0.31 width = 8bp of spot on post-close delayed quotes — INFERENCE: quote artifact, not an arb). Humps at 30D = binary-event signature, not inversion.
- **Desk verdict:** avoid selling 30D premium into MSFT/AAPL/TSLA (earnings-inflated); NVDA is the only clean-window, no-in-window-earnings name but +4.2pp spread isn't an actionable mispricing; SPY +3.0pp on a clean window is the only pure premium observation.

## 4. Open Quant/AI Model Lab

Scored read-only with the repo's `assess_source` rubric. Full file: `hidden_files/desk4_quantlab_2026-09-30.md`.

| Candidate | Score | Disposition |
|---|---|---|
| Kim & Oh, FEDS 2026.049 — tree-based SHAR for IV forecasting | 83 | **INTEGRATE** |
| MDPI Mathematics — weekly VIX forecasting on FRED (13 models, DM tests) | 67 | **TEST** |
| danielevansmith/options-dataset-hist — SPY chains 2008–2025, ~24.6M rows | 64 | WATCH |
| l3a0/trading-strategies — proxy-IV backtest +$270k → −$184k on real chains | 61 | WATCH |
| medloh/stockpile options-scanner — surface-relative IV excess column | 55 | WATCH |
| arXiv:2609.22893 — universal diffusion models for IV surfaces | 49 | WATCH |
| arXiv:2609.04569 — quantum circuit learning for Bitcoin RV | 25 | ARCHIVE |

Caveats: paper headline claims are FACTs-of-the-abstract (not verified by us); the options dataset's freshness/IV-method/license are UNVERIFIED. Gaps persist in dividend forecasting and options microstructure.

## 5. Futures Event desk (catalysts)

Facts (all as of 9/30 unless noted):
- **EIA Weekly Petroleum Status (10:30 AM ET today):** crude +922k bbl to 427.3M bbl (Reuters poll expected −264k); gasoline −1.684M bbl; **distillates −2.251M bbl, 14% below 5-yr avg**; Cushing +555k bbl; implied demand 20.8M bpd (+2.1% y/y).
- **USDA Grain Stocks (noon ET today):** corn 2.095B bu vs 1.924B est (bearish, −2.5% post); soy 315M vs 323M est (+0.6%); wheat 1.846B bu vs 1.849B est (−1.6%); 2026 all-wheat 1.534B bu (−23% y/y).
- **Hormuz:** tanker struck by unknown projectile (UKMTO/WSJ); Trump rejected Iran's 7-day ceasefire proposal; FlyDubai emergency landing in Saudi after reported stabbing; emergency Netanyahu meeting.
- **Saudi recovery:** East-West pipeline ~3.5M bpd vs ~4M pre-attack; Saudi exports 5.8M bpd (highest since Feb 2026); Gulf flows ~98% of pre-war levels (figures vary slightly by source).
- **OPEC+ Sunday (Oct 4):** expected to roll November quotas (Reuters); actual output ~5M bpd below pre-war levels.
- **SPR:** DOE offering up to 40M bbl exchange (bids due Oct 6); SPR ~284–287M bbl, lowest since 1982.
- Retail diesel at record $6.53/gal; ANZ flags U.S. diesel export ban risk; Russia extending its diesel export ban. LNG Canada Phase 2 approved by Shell; U.S. LNG feedgas at record ~18 bcfd. Nor'easter developing; above-normal temps in South-Central U.S. through Oct 6.

Curves: WTI front ~$90.55–90.76 in steep backwardation down to ~$77.6 (FACT — quoted strip); nat gas $2.99/MMBtu in deep contango (Dec 2027 ~$4.19, ~41% carry). Brent-WTI ~$12.29, widest in four months.

Inferences: (a) refined-product tightness is the binding constraint, not crude; (b) today's WTI rally on a crude build = geopolitics is the marginal price driver; (c) Brent-WTI spread reflects Hormuz risk on Brent vs U.S. supply access on WTI.

**Watchlist transmission (INFERENCE):** $90+ oil + record diesel = logistics/energy-cost headwind for TSLA deliveries, AAPL supply chain, MSFT/NVDA datacenters; 30Y at a 24-year high (~5.60%) tightens valuation math on long-duration growth names. No single equity-moving catalyst from this desk — macro, not idiosyncratic.

## 6. Box/Parity Observer

- **Record SPX box-spread financing wave:** ~$146B outstanding notional per Cboe Derivatives Market Intelligence (cited via cryptobriefing/tokenpost); box-implied yield ~69 bps over SOFR (avg 32 bps this year). INFERENCE: segmented funding demand (margin-loan alternative, BOXX-style tax treatment), not a textbook parity failure. Cboe-primary figures UNVERIFIED.
- **Cboe + S&P DJI extended exclusive SPX options licensing through 2051** (announced Sep 29) — franchise news, no methodology or parity implication.
- **No new index-methodology changes; no new published parity-violation analysis.** Background: arXiv 2605.12250 argues parity holds as terminal identity, deviations via funding costs.
- **Live SPY box check (10/30 expiry, Yahoo delayed chain, ~13:30 PDT):** put-call residuals ±$0.05 across strikes 760–765; box 760/770 mid $10.050 vs PV $9.968 (+8¢ mid-rich); crossing the spread PV sits inside bid/ask → **no executable arbitrage; parity holds within transaction costs.** INFERENCE: the mid-price richness matches the market-wide box-vs-SOFR premium — friction, not an arb.

## 7. Macro driver check (oil + bonds)

Source: Yahoo Finance, 9/30 session close (pulled 13:26 PT).

| Driver | Level | Day move | Read (INFERENCE where causal) |
|---|---|---|---|
| WTI (CL=F) | 90.52 | +1.28% | $90+ oil = energy-cost pressure on watchlist margins (TSLA freight/deliveries, AAPL supply chain, datacenter power). Directional headwind, not idiosyncratic. |
| Nat gas (NG=F) | 3.02 | +0.2% | Flat; no margin signal today. |
| 10Y (^TNX) | 5.29% | +0.03pp | Rates grinding higher; raises valuation discount rates and erodes premium-buying power. 30Y at ~5.60%, a 24-year high per futures-desk sources. |
| 2Y (^FVX) | 5.09% | +0.03pp | Front-end firm; term premium positive. |

**One-line verdicts:** Oil — up on geopolitics, not inventories; margin headwind intensifies for logistics/power-heavy names. Bonds — yields firming at multi-decade highs; directional pressure on long-duration multiples and on option time-value financing.

## Cross-desk resolution notes

- MSFT earnings timing: Premium desk used a MarketBeat estimate (~10/27–28); Earnings desk confirms MSFT has **not** announced and isn't on Nasdaq's calendar. Treated as INFERENCE/UNVERIFIED everywhere in this package.
- TSLA Oct 2 deliveries timing "pre-market": INFERENCE from Tesla's past pattern; the date itself is FACT (multi-source).
- QQQ/TSLA IV−RV spreads: Premium desk flagged both WINDOW-CONTINGENT; no desk action implied until recomputed ex-stale-day or the window rolls.
- Nat gas $2.99 (WSJ/EBW, ~09:46 ET) vs $3.02 (Yahoo close) — both cited with as-of; consistent within a flat session.
