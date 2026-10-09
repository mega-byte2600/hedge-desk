# Hedge-desk daily research package — Fri 2026-10-09 (~1:30pm PDT)

Research and input only — paper-only context. All desks covered in full. Labels: **FACT** = verified this run; **INFERENCE** = reasoned from facts; **SPECULATION** = ungrounded extrapolation; **UNVERIFIED** = could not verify, failed closed.

---

## SYNTHESIS — the 5 most decision-relevant items

1. **Earnings-date corrections beat the nightly inputs: TSLA Oct 21 (after hours), MSFT Oct 28 (after hours), AAPL Nov 2 (announced).** Last night's iv-inputs had MSFT ~Nov 4 and AAPL ~Oct 29 — both stale. (FACT, Nasdaq calendar + Apple IR) INFERENCE: all three names now carry earnings *inside* the 28D (Nov 6) option window. TSLA's Oct-23 straddle prices ±7.5%, almost exactly its 8-quarter average absolute reaction (7.8%, fat tails: two >14%) — no edge on pricing alone, and premium-into-a-binary = avoid on all three. (INFERENCE; what would change it: straddle repricing into Oct 21 on fresh news.)
2. **Only one clean IV-vs-realized read on the watchlist: NVDA (unremarkable).** 28D IV 29.8% vs realized 24.5% (+22%), non-contingent window; the 28D→42D slope (29.8%→35.0%) is the Nov-18 earnings premium sitting on the back expiry — calendar, not fear. QQQ's apparent richness is WINDOW-CONTINGENT (38.5% of 20-day variance is one verified AI-rally day); SPY is clean but modestly priced (28D 12.2% vs realized 9.9%). AAPL/MSFT/TSLA verdicts withheld/avoid per the binary-event rule. (FACT numbers; INFERENCE verdicts)
3. **Rates regime is the dominant backdrop: 10Y 5.22%, 2Y 4.75%, 2s10s +47bp (flattened 4bp d/d), EFFR 3.88%, SOFR–EFFR −1bp (no funding stress).** 60-day parallel +50bp shift on both ends; no inversion anywhere in the window. (FACT, FRED via rates_desk module) INFERENCE: elevated absolute yields keep equity risk premia thin — the margin-of-safety bar for new long-duration exposure (NVDA/TSLA/MSFT) stays high. Nothing in rates argues for widening liquidity-risk discounts.
4. **Commodities day: WASDE corn bearish surprise + energy risk elevated into the weekend.** USDA raised corn yield to 181.2 bu/ac vs 177.7 est, ending stocks 1.849B vs 1.67B expected — all three grains >1% lower today. (FACT) Hormuz tanker attacks hit their highest weekly rate since the war began, strait transits at a 2-month low (crude −27% w/w), and Hurricane Isaias makes landfall tonight with ~11.2M bbl of Gulf production at risk. (FACT) INFERENCE: Brent–WTI steep backwardation + this weekend's stack keeps prompt energy risk premium bid — relevant to inflation/margin tail reads, not directly to the watchlist.
5. **Nothing ex-dividend inside the 4-week window; parity desk quiet.** 28-day Nasdaq dividend-calendar sweep (Oct 10–Nov 6): zero watchlist hits. (FACT) Nearest: AAPL ~Nov 10 (undeclared, pattern), MSFT Nov 19 ($0.98 declared, ex just outside window). NVDA's $1.00 annualized raise stands as the dividend catalyst. SPY Oct-16 put-call parity holds within bid/ask (the 0.14 deviation was a 13-minute quote-timing offset, not a break). (FACT)

---

## 1. Earnings Event desk

One watchlist name reports inside the 2-week window (through Fri Oct 23).

| Name | Report date | Timing | Implied move | Historical avg earnings-day move | Source |
|---|---|---|---|---|---|
| TSLA | **Wed 2026-10-21** | After hours (Nasdaq `time-after-hours`) | **≈ ±7.5%** — ATM straddle on Oct-23 expiry: ($14.825 call mid + $13.975 put mid) / $382.70 spot = 7.53% | **7.8% absolute avg** last 8 quarters (signed mean +0.3%; range +21.9% to −14.5%) | Nasdaq calendar; CBOE delayed quotes (bid/ask mids) — **labeled fallback** (Yahoo v7 options returned 401 "Invalid Crumb" in this environment) |
| AAPL | **Mon 2026-11-02** (announced Oct 6) | After hours — release 1:30pm PT, call 2:00pm PT | Outside window — not computed | — | Apple IR via MacRumors |
| MSFT | **Wed 2026-10-28** | After hours (Nasdaq) | Outside 2-wk window — not computed | — | Nasdaq calendar API (fiscal qtr ending Sep/2026; EPS fcst $4.71, 13 ests) |
| NVDA | **2026-11-18** | Timing not supplied by Nasdaq | Outside window — not computed | — | Nasdaq calendar API |
| SPY / QQQ | — | ETFs, no earnings | — | — | definitional (FACT) |

**Corrections vs last night's iv-inputs (decision-relevant, FACT):** MSFT is Oct 28, not ~Nov 4; AAPL is Nov 2 (announced), not ~Oct 29. INFERENCE: premium desk should use the corrected windows — MSFT's Oct-28 date pulls its event inside the 28D window; AAPL Nov 2 sits inside both 28D and 42D windows. All three verdicts below stand as stated (they assumed ~Nov-4/~Oct-29; the corrected dates are still in-window).
**No watchlist name reported this week (Oct 7–9) — no release to read today.** (FACT)
TSLA detail: quarter ending Sep/2026, consensus EPS $0.23, 11 estimates. Quotes ~15-min delayed; spot $382.70 = Yahoo regular-market price ~1:30pm PDT today. (FACT) The ±7.5% implied move prices almost exactly the 8-quarter average absolute reaction — symmetric, no directional skew embedded. (INFERENCE) What would change it: straddle repricing the morning of Oct 21.

Sources: Nasdaq earnings calendar API (`https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`, checked Oct 7–23 plus Oct 28/29/30, Nov 4/5/18); CBOE delayed quotes `https://cdn.cboe.com/api/global/delayed_quotes/options/TSLA.json` (fetched 2026-10-09 ~1:35pm PDT); Yahoo chart API for TSLA daily bars/spot; https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/

---

## 2. Dividend Opportunity desk

**Headline: no watchlist name has an ex-dividend date inside the 4-week window (Oct 10 – Nov 6, 2026).** (FACT — 28-date Nasdaq dividends-calendar sweep, zero hits.) No increases, cuts, or specials announced in the past 2 weeks (Sep 25 – Oct 9) for any watchlist name. (FACT, news/issuer search)

| Symbol | Next ex-date | Amount | Payment date | Increase/cut/special | Consecutive-increase count |
|---|---|---|---|---|---|
| AAPL | ~Nov 10, 2026 (pattern; not yet declared — UNVERIFIED) | Expected $0.27 — UNVERIFIED until board declaration | ~Nov 13 (est.) — UNVERIFIED | None since Apr 30, 2026 raise to $0.27 (+3.85%) — FACT (Yahoo actions) | 15 consecutive years — INFERENCE (issuer IR not re-pulled this run; known gap) |
| MSFT | **Nov 19, 2026** — FACT (declared Sep 15, 2026) | **$0.98** — FACT (+$0.07/+8% over $0.91) | **Dec 10, 2026** — FACT | INCREASE Sep 15, 2026 board raise $0.91 → $0.98 (+8%) — FACT | **24 consecutive annual increases** — FACT per `dividend-count-standard.md`; do not drift (some screeners show 23 — they undercount per the standard) |
| NVDA | ~early Dec 2026 (pattern; not yet declared) — INFERENCE | Last **$0.25**, paid Oct 1, 2026 (ex Sep 10) — FACT | Next payable ~Dec 31 — INFERENCE | INCREASE: $0.01 → $0.25 (+2,400%), announced with fiscal Q1 FY2027 results — FACT | 1 (2026 raise is the only announced increase in the run) — INFERENCE, issuer IR not verified |
| TSLA | None — no dividend paid or declared — FACT (Yahoo actions, 1y: zero dividend events) | — | — | None | n/a |
| SPY | Dec 2026 (~Dec 18, pattern; not yet declared) — INFERENCE | Last **$1.889**, ex Sep 18, 2026 — FACT | Pay date of Sep distribution UNVERIFIED | No November distribution: quarterly Dec/Mar/Jun/Sep cycle — FACT (1y events: 12/19/25, 3/20/26, 6/18/26, 9/18/26) | n/a (ETF distribution) |
| QQQ | Dec 2026 (~Dec 21, pattern; not yet declared) — INFERENCE | Last **$0.7514**, ex Sep 21, 2026, paid Oct 8 — FACT | Oct 8, 2026 — FACT | Same quarterly cycle — FACT (1y: 12/22/25, 3/23/26, 6/22/26, 9/21/26). Down QoQ ($0.8135 → $0.7514) — FACT, but pass-through constituent variation, not a company "cut" — INFERENCE | n/a (ETF distribution) |

**Decision-relevant:** (1) no dividend-capture or assignment-risk events to plan around through Nov 6; (2) NVDA's 2,400% raise to $1.00 annualized (≈$24–25B/year, one of the largest US payouts; "second only to Microsoft by some estimates" is the sources' phrasing) is the standing dividend catalyst — SPECULATION: continued payout growth is not guaranteed; next declaration expected with late-Nov earnings; (3) AAPL (~Nov 10) and MSFT (Nov 19) ex-dates land just past the window — flag for the next run.

Sources: Nasdaq dividends calendar API (28 dates swept); Yahoo Finance actions `chart/{sym}?interval=1d&range=1y&events=div,split` (UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`); MSFT raise: ad-hoc-news, tipranks; NVDA raise: fool.com 2026-09-25, global.morningstar.com; AAPL pattern: dividendhistory.org, dividend.com, stockevents.app; QQQ/NVDA declared: marketbeat.com; count standard: `~/workspace/hedge-desk-research/dividend-count-standard.md`.

---

## 3. Overnight Premium (IV) desk

**Data provenance (explicit).** Today's IV is a **live Yahoo v7 options-chain pull** (cookie+crumb), ~1:33–1:40pm PDT Fri Oct 9, post-session close. Realized-window stats, variance shares, and window-contingent flags are **carried from 2026-10-08-iv-inputs.json** (as_of 2026-10-08T21:54 PDT, ~15.5h old — WITHIN the 18h freshness guard). Last night's `atm_iv` fields were all None (failed closed on degenerate bid/ask=0/0 quotes) and were **not used as today's IV**. ATM IV computed by Black-Scholes Newton solve on non-degenerate mids, call/put averaged; cross-checked against Yahoo's published per-contract IV (within 1–2pp) and the Brenner-Subrahmanyam straddle approximation (matches). Funding rate assumed r = 4% (INFERENCE-level input, stated). IV-rank history unavailable from free sources → "elevated IV rank" claims are vs the 20-day realized base only, labeled UNVERIFIED vs history.

### IV / realized snapshot (live IV vs carried realized base)

| Symbol | Spot (Oct 9 close) | 7D IV (10/16 exp) | **28D IV (11/6 exp)** | 42D IV (11/20 exp) | Realized 20d* | 28D IV vs realized | Term-structure shape |
|---|---|---|---|---|---|---|---|
| SPY | 778.57 | 9.5% | **12.2%** | 12.9% | 9.9% | +2.3pp (~+23%) | gentle contango |
| QQQ | 751.27 | 14.8% | **18.1%** | 18.7% | 15.1% | +3.0pp (~+20%), WINDOW-CONTINGENT | contango |
| AAPL | 336.64 | 22.2% | **26.8%** | 25.6% | 16.4% | +10.4pp (~+64%), WINDOW-CONTINGENT | hump at 28D, inverted 28D→42D |
| MSFT | 535.07 | 23.0% | **32.0%** | 30.5% | 20.8% | +11.2pp (~+54%), WINDOW-CONTINGENT | spike 7D→28D, slight inversion after |
| NVDA | 229.28 | 28.9% | **29.8%** | 35.0% | 24.5% | +5.3pp (~+22%), clean window | steep contango 28D→42D |
| TSLA | 382.70 | 37.5% | **43.1%** | 41.4% | 29.0% | +14.1pp (~+49%), WINDOW-CONTINGENT | inversion peak at 28D |

\* Realized = ann. 20d log-return std × √252, window 2026-09-11 → 2026-10-08 (carried, desk-recomputed within ~1pp).

### Stale-jump screen (standing rule 2026-09-28)
- **SPY — NOT contingent (0.296).** Driver: 2026-09-21 +1.54% (29.6% of window variance) — verified cause: broad AI/chip rally (Brent −3.1% ahead of Pezeshkian UNGA, 10Y −2bp, Meta +11.4% on Muse AI-agent demand, Trump–Xi summit set for Sep 24). (FACT)
- **QQQ — WINDOW-CONTINGENT (0.385).** Driver: 2026-09-21 **+2.74%** (38.5%) — same verified AI rally. Second: 9/17 +1.72%; third: 10/08 −1.35%.
- **AAPL — WINDOW-CONTINGENT (0.328).** Driver: 2026-09-29 **−2.70%** (32.8%) — verified Apple-specific: new CEO John Ternus (succeeded Tim Cook 9/1) weighing cuts to middle management/engineering program-manager roles and scrapping the fixed spring/fall launch calendar; BofA flagged Meta's Muse AI shopping agent as an e-commerce threat; 37.8× trailing vs 5y median 31×. (FACT)
- **MSFT — WINDOW-CONTINGENT (0.358).** Driver: 2026-09-25 **+3.60%** (35.8%) — verified: Copilot revamp announcement + Stifel upgrade to Buy, $575 target. (FACT)
- **NVDA — NOT contingent (0.238).** Drivers diffuse: 9/14 −3.42% (23.8%), 10/08 −2.99% (18.2%), 9/17 +2.51% (12.8%) — no single day dominates.
- **TSLA — WINDOW-CONTINGENT (0.309).** Driver: 2026-10-02 **+4.55%** (30.9%) — verified: Q3 deliveries 486,532 vs ~461k consensus (+5.5%). Second: 9/28 −4.02% (24.1%) — cause UNVERIFIED.

### Earnings-in-window flags (premium into a binary event = avoid)
- **TSLA — Oct 21 after close**, inside the 28D window. 28D IV 43.1% = event pricing (FACT of term shape + calendar). Note: earnings-date source triangulation — Nasdaq calendar says Oct 21; one secondary source said Oct 20; Earnings desk verified Oct 21 after hours (Nasdaq). 
- **AAPL — Nov 2**, inside both 28D and 42D windows. 28D IV 26.8% vs 42D 25.6% hump = earnings priced in the 11/6 expiry (FACT).
- **MSFT — Oct 28 after close** (corrected today), inside the 28D window (11/6 expiry). The 7D→28D IV jump (23.0%→32.0%) is largely this event premium (INFERENCE from term shape + calendar).
- **NVDA — Nov 18**, inside the 42D window (11/20 expiry) but OUTSIDE the 28D window — the 28D→42D slope (29.8%→35.0%) is the earnings premium on the back expiry (FACT).
- **SPY, QQQ — no earnings.**

### Desk verdicts (each states what would change it)
1. **NVDA — the only clean IV-vs-realized read, and it's unremarkable.** 28D 29.8% vs realized 24.5%; premium mechanically explained by Nov-18 earnings on the back expiry. No mispricing signal. **What would change it:** realized running above ~30% would validate the premium as cheap; an IV spike without catalyst would flag fear pricing.
2. **SPY — modest premium, clean window.** 28D 12.2% vs realized 9.9%; front 7D at 9.5% sits *below* realized — normal contango, no elevation worth chasing. **What would change it:** front-end IV collapsing through 8% on no news, or realized breaking above 12%.
3. **QQQ — WINDOW-CONTINGENT; verdict withheld.** Ex-the-9/21-jump, realized is ~11.8% (computed, FACT math) — so the apparent "+20%" IV premium is likely materially understated; IV looks genuinely rich ex-jump (INFERENCE). Per the standing rule, no clean verdict. **What would change it:** a refreshed 20-day window excluding 9/21, or front-month IV compressing toward 15%.
4. **AAPL, MSFT, TSLA — AVOID per the binary-event rule (three for three).** All three carry in-window earnings; all three are WINDOW-CONTINGENT with verified single-name causes; their elevated 28D IVs (26.8% / 32.0% / 43.1%) are event premium + jump-contaminated realized bases — not a mispricing. **What would change it:** earnings pass-through with IV crush, then re-screen on a clean window.
5. **Elevated-IV flags (vs realized base only; IV history UNVERIFIED):** MSFT 28D 32.0% and TSLA 28D 43.1% are the most elevated reads, but both sit on in-window earnings — elevation expected, not an edge. AAPL's 28D→42D inversion (26.8%→25.6%) and TSLA's (43.1%→41.4%) confirm event concentration on the front expiry (FACT); NVDA's steep 28D→42D rise confirms the market paying for earnings further out (FACT).

Working detail: /tmp/iv_snapshot.json (ephemeral; full per-expiry BS solves). Sources: Yahoo Finance v7 options chains (cookie+crumb, UA header), carried 2026-10-08 iv-inputs; cause-verification links in desk working notes.

---

## 4. Open Quant/AI Model Lab

**Sweep scope:** arXiv q-fin.PR/CP/ST/RM + keyword sweeps (implied volatility, options microstructure, vol forecasting, PEAD, dividend forecasting) since 2026-10-02, plus GitHub/PyPI/awesome-quant API leg. All candidates scored with the repo's `assess_source`; all score inputs recomputed per candidate. Nothing INTEGRATE-ready (max score 66). Evidence labels: FACT = verified this run (arXiv API, abs page, GitHub API, PyPI API); INFERENCE = reasoning from verified facts; source-reported claims = UNVERIFIED unless independently checked. All candidates appended to `quant-lab-ledger.md` (#39–#48; ledger now at 48 rows); five existing-row dispositions updated; Jidoka + Kaizen entries recorded (Jidoka: no INTEGRATE-ready candidates, TEST advance on verified evidence only, no moves on unlicensed code; Kaizen: PyPI name-collision poka-yoke — PyPI `holdout` v0.3.0 is a different package, name collision — plus arXiv API `sortBy=submittedDate` fix).

| # | Candidate | Score | Disposition | Reason |
|---|---|---|---|---|
| 39 | QuantOracle (github.com/QuantOracledev/quantoracle) — free quant API, 63 deterministic endpoints, options pricing + Greeks, no key, MIT, updated 2026-10-03 | 61 | WATCH | FACT: MIT, updated 10-03 (12 stars). Deterministic calculators = potential premium-desk parity/reference tools. Endpoint/Greeks/no-key claims UNVERIFIED (README not read this run). Follow-up: sandbox fail-closed + determinism vs desk solver |
| 40 | SOTA: Stock Options Trading Agents Guided by Option-Implied Return Distributions (arXiv 2610.10407, 7 Oct) | 42 | ARCHIVE | LLM trading-agent framing = paper-only boundary mismatch; no code on abs page |
| 41 | HAN-Mamba: Hierarchical Selective State Space Networks for Multi-Scale Financial Volatility Forecasting (arXiv 2610.10323, 7 Oct) | 45 | WATCH | Multi-scale RV forecasting; Optiver benchmark claim UNVERIFIED; no code |
| 42 | Scale or speed? When do path signatures improve volatility-regime forecasts? (arXiv 2610.06690, 5 Oct) | 51 | WATCH | +2.7pp balanced accuracy on US next-month vol terciles after multiple-testing correction (source-reported, UNVERIFIED); honest null outside US; replicable from free Yahoo daily data. Sandbox candidate: HAR + signature features on SPY 20-day RV |
| 43 | Beneath the VIX: Probability, Severity, and Uncertainty Shocks (arXiv 2610.03849, 2 Oct) | 45 | WATCH | Downside Protection Premium tracks VIX; strike slope separates shortfall probability vs severity (UNVERIFIED). Vol-regime context, not tradable input |
| 44 | Shapley-based Structural Analysis of Neural Calibration for SV Models (arXiv 2610.03076, 2 Oct) | 42 | ARCHIVE | Calibration intuition only (preprint, no code; source-reported) |
| 45 | josephouyang/machine_learning_for_implied_volatility_forecasting — CMU replication of Jiang/Lazar/Marra (2026) JFM peer-reviewed "Improving IV Forecasts for American Options Using Neural Networks"; MIT, updated 2026-08-19 | 63 | WATCH | FACT: MIT; FACT: JFM 46:1137–1153 peer-reviewed. Gap-NN (market-IV − model-IV) idea directly applicable to American-exercise watchlist options. Data proprietary (OptionMetrics/WRDS) → replicate on Yahoo chain instead |
| 46 | danielevansmith/options-dataset-hist — historic options dataset SPY/IWM/QQQ Jan 2008–Dec 2025 (IV, Greeks, volume, OI); MIT, updated 2026-06-29 | 61 | WATCH | FACT: MIT, description.pdf summary stats read. Fills premium desk's free IV-history gap IF provenance checks out — currently UNVERIFIED. Follow-up: verify provenance + format, cross-check vs Yahoo chain |
| 47 | Latent Continuum of Regimes in Limit Order Book Dynamics (arXiv 2610.05740, 5 Oct) | 42 | ARCHIVE | EURO STOXX futures LOB; zero watchlist options transfer; no code |
| 48 | Event History Over Scale: MBOFormer LOB forecasting (arXiv 2610.02917, 2 Oct) | 42 | ARCHIVE | Level-3 message data not desk-accessible; UNVERIFIED; no code |

**Disposition changes on existing rows:** #25 Han et al (diffusion IV surface) **WATCH→TEST** — code verified (yinbinhan/volatility-surface-simulation, MIT, updated 2026-10-02, 26 files incl. sanity_check.py); rescored 48→**66** TEST; sandbox: run sanity_check, verify arb-violation claim on SPY chain. #20 Yang et al stays WATCH — code link found but **no LICENSE → all-rights-reserved, unusable until licensed**. #37 DaniyalMlk/holdout stays WATCH — PyPI `holdout` is a different package (name collision). #9 Buchegger & Gonon stays WATCH/BLOCKED — no author code. #34 stays WATCH — no code link.

**Null results (explicit, not dropped):** earnings-drift lane — no new PEAD papers in-window; dividend-forecasting lane — nothing new (#12 Dong unchanged); purged walk-forward lane — no new candidates (#22 purgedcv, #37, #1 unchanged); 8 new preprints — zero author code links (reproducibility not established for any).

Ledger: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (48 rows, ~30.6KB).

---

## 5. Weather/War/Logistics Futures Event desk

### EIA Weekly Petroleum Status (released Wed Oct 7, 10:30 ET; week ended Oct 2) — FACT
- **Crude: −3.2M bbl to 424.1M** vs Reuters poll expecting a +1.7M build — bullish surprise. Still 1% above the 5-yr seasonal average. Cushing +444K bbl.
- **Gasoline: +0.4M bbl to 204.7M** vs −1.7M draw expected — bearish surprise vs expectations.
- **Distillates: ~105.1M** vs −2.1M draw expected — but still **12% below the 5-yr average**, the tight leg.
- Refinery runs +223K bpd; utilization 92.7% (+0.2pp). US crude production hit a **record 13.979M bpd**. Net crude imports −53K bpd.
- Products supplied (4-wk avg): 21.1M bpd, +0.7% YoY; gasoline 8.8M bpd; distillates 3.8M bpd (−1.6% YoY).
- Price reaction Wed morning: Brent +1.2% to ~$101.79, WTI +0.54% to ~$89.92 — crude drew, but product builds capped the bid.
- Sources: Reuters Oct 7; OilPrice Oct 7.

### USDA October WASDE (released today, 12:00 ET) — FACT unless noted
- **Corn (bearish surprise):** yield raised to **181.2 bu/ac** vs 178.5 prior and 177.7 average trade estimate — reversed two months of cuts. Production ≈16.034B bu (+234M m/m). Ending stocks **1.849B bu vs 1.67B avg trade**. Futures traded lower post-report.
- **Soybeans (near expectations):** yield 53.1 vs 52.8 prior, slightly above avg trade. Ending stocks **315M bu** vs 305M avg, +5M vs Sep. Futures modestly lower.
- **Wheat:** October headline specifics UNVERIFIED in this sweep (pre-report: US ending stocks 717M bu est. per DTN analyst poll). Reported post-report: wheat, corn, soybean futures all **>1% lower today** on fund/technical selling after the report. Dec wheat had already fallen 2.6% Wed ($6.86) on a strong-dollar record-yield trade.
- Pre-report positioning (Oct 7–8): Dec corn $5.02 (2-sided), Nov beans ~$12.94-1/2; export sales (wk ended Oct 1) low-end of forecasts for corn (769.5K MT) and soy (549.4K MT), high-end for wheat (451.6K MT).
- INFERENCE: the corn yield surprise removes rationing urgency and likely caps December corn's upside until South American weather risk re-enters; part of the move was front-run by Thursday's risk-off selloff.
- Sources: RFD-TV WASDE recap; DTN pre-report estimates; XTB post-report price action.

### Hurricane Isaias — Gulf energy/logistics disruption this weekend — FACT
- Now **Category 2**; NHC briefly forecast Cat 3 early Friday before shear weakens it ahead of landfall **late tonight/early Saturday** along a 130-mile stretch from Gautier, MS to Miramar Beach, FL. Tropical-storm winds reach the coast by midday Friday; dangerous surge; 10" isolated rainfall; tracks inland to TN/KY as post-tropical depression Sunday.
- **~11.2M bbl of Gulf oil production at risk** through the storm (Earth Science Associates model via Reuters) — up from 7.1M for July's Tropical Storm Bertha. Track crosses significant offshore production and onshore refining corridors.
- INFERENCE: short-lived but real prompt-weekend premium for Gulf crude and products; damage updates Saturday–Monday move RBOB/distillates first, not just crude. Watch distillate cracks, already elevated.
- Sources: USA Today live updates; Reuters Oct 7.

### Strait of Hormuz / US–Iran war — FRESH (last 48h) — FACT
- Tanker attacks at the highest weekly rate since the war began Feb 28: ≥12 attacks/attempts Sep 28–Oct 5 (IMO collated 9). IRGC drone overflights/VHF hails persist.
- Hormuz transits at lowest since July 23: 7 commodity vessels Tuesday Oct 6; crude through the strait **−27% w/w to ~10.1M bpd (74% of pre-war)**. Offset: Gulf of Oman/Red Sea exports rose 2x pre-war, keeping total Middle East exports near pre-war.
- Today: Trump said the US would not attack Iran before November midterms citing "productive discussions"; the US naval blockade of Iranian ports stays; NYT reports Pentagon drew up 3-day strike plans. Iran's Fars claimed mine strikes on tankers late Thursday (UNVERIFIED/unconfirmed); Iran claims control of the strait, Sec. Rubio disputes.
- Market reaction: Brent shed ~1% to ~$103.25 after Thursday's 4%+ surge. Freight/insurance rates remain elevated. OPEC+ kept November quotas unchanged (Sunday Oct 4). China's refined-product export suspension for October reported to continue. IEA (Sep 11): high prices + restricted supply → biggest demand drop since Covid, but 2026 global deficit estimate raised to 1.7M bpd; return of surplus pushed to 2027.
- Sources: Reuters tanker-attacks Oct 7; Reuters Hormuz-transits Oct 8; Moneyweb/Bloomberg Oct 9.

### Futures-curve read — FACT + INFERENCE
- Both benchmarks in **steep backwardation**: WTI Nov 26 front ~$89–91, Brent Dec 26 ~$101–103; Brent–WTI front spread ~$10–11. Prompt barrels commanding the premium.
- Trump's remarks today trimmed the geopolitical premium (Brent −1%), but backwardation persisting through the war escalation says near-term physical tightness is real, not just paper fear.
- Distillates are the tight leg (12% below 5-yr avg; diesel cracks outpacing crude). INFERENCE: if Isaias shutters Gulf refining or damages offshore supply, the crack complex reprices first.

### Government-data status — FACT
No shutdown; EIA weekly and October WASDE both released on schedule. No correction needed. (User-verified: CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11.) Brief-correction-2026-10-05.md NOT applied per standing rule.

---

## 6. Box/Parity Observer

**Desk verdict: quiet. No parity violations; no methodology changes; OCC memos all single-name, none touching the watchlist.**

- **Index methodology scan (last ~7 days):** No new published put-call/box-parity violation studies found. One search hit (Hedgeweek, "CBOE to enhance VIX index methodology by including SPX Weeklys … From 6 October") is a **stale recrawl** of a 2014-era article (quotes ex-CEO Edward Tilly) — flagged so it isn't misread as fresh. Cboe's 25-year exclusive SPX licensing extension through 2051 (reported Oct 8; Goldman Sell→Neutral $300, TD Cowen upgrade to Buy $334) is index-*franchise* news, not a methodology change — no parity implication. Cboe exploring perpetual futures on VIX (Bloomberg via CoinDesk, Oct 2) is early exploration only — no specs, no filing, VIX index methodology unchanged. (FACT; article-age call is INFERENCE from CEO attribution)
- **OCC corporate-action memos Oct 7–9 (#59920–#59932):** all single-name (ACVA tender, MSGK1 distribution, RGEN1/ETHA1/FMX4/FMX5 cash-in-lieu, NXH1 warrants, QNCX1→IRLA1 rename) — none affect SPY/QQQ/AAPL/MSFT/NVDA/TSLA. (FACT, theocc.com)
- **SPY put-call parity spot-check (live Yahoo quotes ~1:33pm PDT Oct 9, UA header):** expiry Oct 16, 2026 (weekly), T = 7/365 = 0.01918 yr; rate proxy ^IRX 13W T-bill 4.057% (Oct 9 close — labeled 13W, not 2Y); S = 778.57 (4:00pm ET close print). K=779: C mid 4.12, P mid 4.085 → observed C−P = 0.035 vs theoretical 0.176 (deviation −0.141). K=778: C mid 4.69, P mid 3.64 → observed C−P = 1.050 vs theoretical 1.175 (deviation −0.125). Both strikes imply the same spot — 778.43 and 778.44, agreeing to 0.016, ~0.13 below the 4:00pm ET stock print. (FACT) Option quotes timestamped 4:13pm ET vs stock 4:00pm ET — the deviation is fully explained by the ~13-minute quote-timing mismatch, not a parity break. (INFERENCE) Combined leg spreads 0.02 wide; cross-strike consistency inside 0.02 — **parity holds within bid/ask; no violation flagged.** (INFERENCE from FACT arithmetic) Quotes liquid, non-degenerate (no 0/0 bids/asks; OI in the thousands). Dividend assumption: no SPY ex-div between Oct 9 and Oct 16 (next ~mid-Dec), so no dividend term needed. (INFERENCE)
- **Carry-forward:** the Yahoo v7 options endpoint now requires the crumb flow ("Invalid Crumb" on bare calls) — working sequence: fc.yahoo.com → cookie → v1/test/getcrumb → ?crumb= on every API call.

---

## 7. Bonds & Rates desk

**Desk status: OPERATIONAL — `rates_desk.rates_environment()` ran clean** (`REAL_FRED_RATES` mode, HTTP 200 from FRED public CSV, observations dated 2026-10-08; FRED daily series publish T+1 business day, so 10-08 is latest available — FACT). No substitutions made; no numbers from memory.

| Metric | Value | Date |
|---|---|---|
| Fed funds effective rate (DFF/EFFR) | 3.88% | 2026-10-08 |
| Fed funds change over 60-day window | +0.25% (+25bp) | module-computed |
| Treasury 2Y (DGS2) | 4.75% | 2026-10-08 |
| Treasury 10Y (DGS10) | 5.22% | 2026-10-08 |
| 2s10s spread | +47bp | computed |
| Curve shape | UPWARD_SLOPING | module-computed |
| SOFR | 3.87% | 2026-10-08 |
| OBFR | 3.88% | 2026-10-08 |

**Curve read (FACT, from 60-day histories):** on 10-07, 2Y 4.77% / 10Y 5.28% → spread 51bp. On 10-08, 2Y fell 2bp (→4.75%) and 10Y fell 6bp (→5.22%) → spread 47bp. Long end led the decline; **mild flattening day-over-day** (spread −4bp), curve still positively sloped. 60-day: 2Y 4.25%→4.75% (+50bp), 10Y 4.72%→5.22% (+50bp) — roughly parallel; spread identical at both ends (47bp). Peak 10Y in window: 5.31% on 10-05. 2s10s touched 32bp on 9-28, back to 47bp now.
**Rate-level context (INFERENCE):** 5.22% 10Y / 4.75% 2Y are historically elevated; curve positive but not steep. EFFR at 3.88% sits ~87bp below the 2Y, consistent with the market pricing the policy path near its resting level rather than expecting aggressive cuts — a forward-rate implication, not a forecast.
**Funding stress (FACT→INFERENCE):** SOFR 3.87% vs EFFR 3.88% = −1bp; OBFR 3.88% — all three overnight measures within 1bp. **No funding stress** (stress would show as tens-of-bp SOFR–EFFR widening). No inversion anywhere in the observed window — **no recession-flag signal from 2s10s.** (FACT)
**Directional read for premium pricing (INFERENCE):** higher long rates = higher discount rates = pressure on long-duration growth multiples (NVDA, TSLA, MSFT carry the most duration risk) — standard present-value mechanics. Elevated yields raise the carry component in options via put-call parity (higher forward → richer calls, cheaper puts, all else equal) — small vs vol, but systematically biases premium capture toward covered-call writing in this regime. The mild long-end-led decline eases discount-rate pressure marginally vs yesterday (6bp is noise-level but directionally favorable). What would change the posture: a sustained 10Y break below ~5.00% in the module's prints.

---

## Cross-desk consistency notes

- **Earnings dates now corrected (Earnings desk verified live today):** TSLA Oct 21 (after hours), MSFT Oct 28 (after hours), AAPL Nov 2 (announced). The Premium desk's section was built on the nightly job's ~Oct 21/~Nov 4/~Oct 29 estimates; the corrected dates keep all three names in-window — verdicts stand, but MSFT's window is now *shorter* (19 days, inside the 28D expiry) and the desk's "MSFT earnings inside 28D window" read is confirmed rather than calendar-inferred. No contradictions remain unresolved.
- **Dividend MSFT ex-date (Nov 19) sits inside the MSFT Oct-28 earnings → Nov-19 ex-div sequence:** no assignment-risk event inside this run's window, but the next run should check that Nov-19 ex-div against short-call positioning. (INFERENCE from two desks' FACT dates)
- **No government-data contradictions:** EIA and USDA released on schedule; the no-shutdown standing rule held again.
- All source URLs are in per-desk sections above. Every material number is labeled. No desk failed; no desk was silently dropped.

*Run metadata: 7/7 desks reported. Market-data rule followed (Yahoo UA header; Yahoo v7 options crumb flow working — Premium desk; CBOE fallback labeled on Earnings desk). IV-inputs freshness guard: file present, as_of 2026-10-08T21:54 PDT, ~15.5h old at run start — within 18h guard; ATM IVs failed closed last night and were NOT used as today's IV.*
