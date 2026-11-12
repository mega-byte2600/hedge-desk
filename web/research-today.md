# Hedge-desk daily research — Thu 2026-11-12 (13:30 PT)

**Run:** daily research, 13:30 PT. **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; never risk-seeking framing.
**Method:** CFA skill (`local-cfa-financial-analysis`); every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED with source + as-of.
**Status:** all 7 desks delivered. No desk FAILED. Paper-only; no Risk of Ruin touched; no trade authorization.

## Synthesis — the 5 decision-relevant items

1. **NVDA earnings Tue Nov 17 (after close) is the week's event — and premium into it is a avoid.** FACT: options price ±10.4–10.8% (three independent reads: desk's own Yahoo straddle calc ±10.38% on the Nov 20 expiry; EarningsWatcher ±10.8%; OANDA ±10.6%), vs a 10-yr average earnings-day move of ±7.8%. FACT: NVDA ATM IV ~88–92% on both the Nov 13 and Nov 20 expiries (live Yahoo pull, 13:28 PT), ~1.7× its 20d realized (51.9%), with a flat-to-inverted term structure — the front expiry is as rich as the earnings expiry, so the elevation is not purely earnings-driven. INFERENCE: the Nov 9 governance overhang (board investigation involving CEO Jensen Huang; stock −4.3% that day, ~$190B market cap) is a live non-earnings vol source stacked on the event. Desk rule: premium into a binary event = avoid; the event is the trade, not the backdrop.
2. **No clean IV-vs-realized verdict exists for any watchlist name — all six windows are WINDOW-CONTINGENT.** FACT (IV-inputs file `nightly/2026-11-11-iv-inputs.json`, as_of 2026-11-11T14:54 PT, ~22.5h old, within the 26h guard): a single day (the Nov 5 jump) drives 41–55% of 20-day realized variance for every symbol, above the 30% threshold. At 8 DTE, IV sits below trailing realized on 5 of 6 names — but that gap is most plausibly the jump inflating realized, NOT cheap premium. Do not read it as a buying signal. IV rank is UNVERIFIED (no free IV-history source). SPY/QQQ closing marks fail put-call parity (+$0.86 / +$1.45), so those IV levels are indicative, not precise.
3. **The curve flattened 10 bp in two sessions while the long end nears 5%.** FACT (repo `rates_desk`, REAL_FRED_RATES, FRED daily): 2s10s +25 bp on Nov 10 (10Y 4.98%, 2Y 4.73%), down from +35 bp Nov 6 — 2Y rose 17 bp vs 10Y +10 bp in a day. EFFR 3.88% (Nov 11); SOFR–EFFR +1 bp, no funding stress. INFERENCE: front-end repricing (fewer expected cuts) + ~5% long rates = discount-rate pressure on growth multiples, most on the watchlist's long-duration names (NVDA, TSLA, MSFT). What would change it: 2Y back below ~4.60% (one-day move) or 10Y sustained above 5.00% (more pressure).
4. **Oil rallied ~2% into the most bearish EIA print in weeks — geopolitics, not fundamentals, is pricing crude.** FACT: EIA Weekly Petroleum Status Report (Thu Nov 12, ~12:00 ET, Veterans Day-delayed) showed commercial crude +4.657M bbl to 414.4M vs a draw expected (~−0.7M to −1.5M), ending five straight weekly draws; gasoline +1.799M, distillate +4.071M. FACT: WTI Dec +$1.96 (+2.27%) to $88.49 in the Thu US session after Trump posted the US is "no longer interested in any deal with Iran." INFERENCE: futures are pricing Strait-constraint risk premium, not the inventory surplus. Durable physical story is distillate tightness (8% below 5-yr avg; Gulf refined flows ~60% of pre-war; ~30% of Russian refining offline). Current live oil level at 13:30 PT is UNVERIFIED — no single-timestamp quote was pulled.
5. **Dividends: AAPL goes ex today, MSFT's raise goes ex Nov 19; no cuts anywhere.** FACT: AAPL ex-dividend today Nov 12, $0.27/qtr, unchanged, payable Nov 16. FACT: MSFT ex Nov 19, $0.98/qtr (+7.7% vs $0.91, Sep 15 board raise), 24th consecutive annual increase per the desk standard; forward yield 0.75% at $523.00, highest among single-name watchlist. NVDA's next dividend is undeclared (last ex Sep 10, $0.25); a December ex-date is plausible from cadence but UNVERIFIED. SPY/QQQ December ex-dates unconfirmed (UNVERIFIED).

---

## Desk 1 — Earnings Event

**Question:** Which watchlist names report in the next 2 weeks (Nov 12–26), and what is the options market pricing?

| Symbol | Report date | Timing | Implied move % | Historical avg earnings-day move | Source |
|---|---|---|---|---|---|
| NVDA | Tue Nov 17, 2026 | After close; call 5:00 p.m. ET | ±10.4% (desk's Yahoo straddle calc, Nov 20 expiry, 13:30 PT); ±10.8% EarningsWatcher (Nov 12); ±10.6% OANDA (Nov 10) | ±7.8% (10-yr avg peak earnings-day move) | NVIDIA Oct 28 notice via jorgai.com; EarningsWatcher; OANDA; Yahoo Finance options chain |
| AAPL | — (reported Mon Nov 2, after close) | n/a | n/a | n/a | SimianX Mag 7 tracker, updated Nov 3 |
| MSFT | — (reported Wed Oct 28, after close) | n/a | n/a | n/a | SimianX Mag 7 tracker, updated Nov 3 |
| TSLA | — (reported Wed Oct 21, after close) | n/a | n/a | n/a | SimianX Mag 7 tracker, updated Nov 3 |
| SPY / QQQ | — | n/a | n/a | n/a | ETFs — no earnings by construction |

**NVDA is the only watchlist earnings event in the window.** Next AAPL/MSFT/TSLA reports fall in late Jan 2027 (unconfirmed estimates, outside window).

- **FACT:** NVDA options pricing a bigger-than-usual move — three independent reads in a 10.4–10.8% band, all above the ±7.8% 10-yr average. Caveat (INFERENCE): the Nov 20 straddle also prices Nov 18–20 non-event days, so it slightly overstates the pure event move; direction (elevated vs history) is robust.
- **INFERENCE, grounded in FACT:** the print is not the main variable; the Q4 guide is. Company guidance from the Aug 26 release: Q3 FY27 revenue $108.0B ±2%, gross margin 74.0% (FACT, NVIDIA). Consensus compiled by Schwab as of Nov 4: ~$109.2B revenue, EPS ~$2.47 (FACT, via OANDA/Binance). OANDA notes the reaction will likely hinge more on the Q4 FY27 revenue outlook than the Q3 print.
- **FACT:** governance overhang landed days before the print — NVDA fell 4.3% on Mon Nov 9 (~$190B market cap) after Reuters reported (Nov 8–9) the board launched an independent investigation involving CEO Jensen Huang (via OANDA citing Reuters). INFERENCE: the elevated premium is not purely earnings-driven.
- **Evidence notes:** NVDA date verified independently by four sources incl. the company's own notice and the IV-inputs file (`next_earnings: 2026-11-17`). No Nasdaq earnings-calendar API pull attempted — corroboration was sufficient. No release teardown: no pending release to tear down. AAPL first-session reaction after its Nov 2 print: −1.9% on Nov 3 (FACT, SimianX). MSFT/TSLA first-session reactions UNVERIFIED, omitted rather than guessed.
- Desk status: DELIVERED.

## Desk 2 — Dividend Opportunity

**As of:** Thu 2026-11-12, 13:30 PT (prices = Nov 12 close, Yahoo v8 chart, marketTime 21:00 UTC). Window: ex-dates Nov 12 – Dec 10, 2026.

| Symbol | Ex-date | Amount | Pay date | Change vs prior | Yield* | Source |
|---|---|---|---|---|---|---|
| AAPL | **Nov 12, 2026 (today)** | $0.27/qtr | Nov 16, 2026 | Unchanged (same as Aug 10, 2026) | 0.30% | Nasdaq dividends calendar 2026-11-12; Apple IR dividend history |
| MSFT | **Nov 19, 2026** | $0.98/qtr | Dec 10, 2026 | **+7.7% vs $0.91** (Sep 15, 2026 board raise) | 0.75% | Nasdaq dividends calendar 2026-11-19; desk standard `dividend-count-standard.md` |
| NVDA | Not yet declared | $0.25/qtr (last declared rate) | — | Unchanged at last declared rate | 0.60% | Yahoo chart events (last ex Sep 10, 2026); NVIDIA Q1 FY27 release |
| SPY | None in window | — | — | — | 1.00% trailing | Yahoo chart events (last ex Sep 18, 2026, $1.889) |
| QQQ | None in window | — | — | — | 0.45% trailing | Yahoo chart events (last ex Sep 21, 2026, $0.751) |
| TSLA | None — pays no dividend | — | — | — | 0.00% | Yahoo chart events, 2-yr history: zero dividends |

\* Yield = annualized rate ÷ Nov 12 close (AAPL $354.88, MSFT $523.00, NVDA $166.19); SPY/QQQ use trailing-12-mo distributions ($7.583 / $3.091) ÷ close (SPY $757.12, QQQ $688.17). All yields computed by this desk from the two named inputs — FACT per sources cited.

- **FACT:** AAPL goes ex today — the Nov 16 payment is already locked out for new buyers. $0.27 unchanged from the prior two quarters; last raise to $0.27 in May 2026 (from $0.26, +3.8%). AAPL's full consecutive-increase streak is UNVERIFIED: third-party screeners disagree by methodology (12 vs 14 vs 15 years); the issuer's own history confirms only the annual May raise pattern 2021–2026.
- **FACT:** MSFT's $0.98 ex-date is Nov 19 — the only in-window raise, and the 24th consecutive annual increase (per the standing desk standard, anchored to the Sep 15, 2026 board raise; no raise announced since, count stays 24). No cut, special, or suspension anywhere on the watchlist.
- **FACT:** NVDA's next dividend is undeclared — watch the Nov 19 earnings release. Prior two December ex-dates fell Dec 5, 2024 and Dec 4, 2025, so a December ex-date inside this window is plausible but UNVERIFIED (pattern, not a declaration). Context: NVDA raised its quarterly rate 25-fold, $0.01 → $0.25, on May 20, 2026 (Q1 FY27 release), first paid Jun 26, 2026.
- **UNVERIFIED:** SPY/QQQ December ex-dates — Nasdaq calendar queries for Dec 18 and Dec 21, 2026 returned no SPY/QQQ rows; treat any mid/late-December date as UNVERIFIED until declared.
- Source failures: none material. Yahoo v8 chart returned full 2-yr dividend histories for all six names; Nasdaq dividends calendar API returned rows for Nov 12, Nov 19, Nov 20, Dec 10, Dec 18, Dec 21.
- Desk status: DELIVERED.

## Desk 3 — Overnight Premium (IV)

**Question:** Where does implied vol sit vs trailing realized vol, is any IV rank elevated, and is any premium priced into a binary event?

**Sources and as-of:**
- **IV-inputs file (STALE-labeled, within 26h guard):** `~/workspace/hedge-desk-research/nightly/2026-11-11-iv-inputs.json`, as_of 2026-11-11T14:54:30-07:00 (~22.5h old at run time). ATM IV **NULL for all six symbols** — nearest expiry had already expired at pull time; the pull failed closed rather than report solver residuals on dead contracts. [FACT — file]
- **Live Yahoo options-chain pull (supplement, labeled LIVE):** succeeded via cookie+crumb handshake, pulled 13:28 PT / 16:28 ET — **after the 16:00 ET close, so these are closing marks, not live tradable quotes**. Two expiries: Fri 2026-11-13 (0.98 DTE) and Fri 2026-11-20 (7.98 DTE). ATM IV by Black-Scholes inversion on bid/ask mids, r = 4%, T to 16:00 ET expiry. First-pass IVs discarded: Yahoo's expiry timestamp is midnight UTC, which understated T ~9× and inflated IV ~3× (e.g. NVDA 280%); recomputed with correct T. [FACT — desk pull]
- **IV rank: UNVERIFIED** — no free IV-history source available; no elevated-IV-rank flag can be issued.

| Symbol | ATM IV 11-13 (0.98d) call/put | ATM IV 11-20 (7.98d) call/put | Realized 20d* | Max 1-day var share* | Verdict |
|---|---|---|---|---|---|
| SPY | 20.9% / 15.5% ⚠️ | 16.6% / 14.9% ⚠️ | 22.6% | 55.1% | WINDOW-CONTINGENT |
| QQQ | 37.5% / 27.3% ⚠️ | 29.7% / 26.6% ⚠️ | 36.4% | 46.0% | WINDOW-CONTINGENT |
| AAPL | 24.4% / 24.1% | 22.6% / 22.3% | 27.4% | 49.7% | WINDOW-CONTINGENT |
| MSFT | 40.9% / 40.3% | 30.6% / 33.7% ⚠️ | 37.4% | 41.8% | WINDOW-CONTINGENT |
| NVDA | 91.7% / 90.5% | 88.3% / 88.2% | 51.9% | 40.8% | WINDOW-CONTINGENT |
| TSLA | 58.8% / 56.2% | 47.7% / 47.4% | 62.2% | 46.9% | WINDOW-CONTINGENT |

\* Realized 20d and variance share from the STALE 2026-11-11 file, window 2026-10-14 to 2026-11-10. [FACT — file]

⚠️ = put-call parity violation on Yahoo closing marks (C−P vs S−PV(K)): SPY +$0.86 (11-13) / +$0.73 (11-20); QQQ +$1.45 / +$1.28; MSFT −$0.98 (11-20 only). Per the parity rule the math wins over the marks: these quotes are internally inconsistent (stale underlying vs option marks after the close), so SPY/QQQ IV levels — and MSFT's 11-20 legs — are **indicative, not precise**. AAPL, NVDA, TSLA parity diffs ≤ $0.22, clean. [FACT — desk computation; INFERENCE that the cause is stale post-close marks]

**Earnings in window:** NVDA earnings 2026-11-17 falls **inside the 2026-11-20 expiry window** — premium into a binary event: **avoid**. [FACT — file; confirmed by Desk 1] No other watchlist earnings inside either expiry window.

**Observations:**
1. **No clean IV-vs-realized verdict exists for any symbol.** All six 20d windows are WINDOW-CONTINGENT — a single day (the Nov 5 jump) drives 41–55% of realized variance. At 8 DTE, IV sits below trailing realized on 5 of 6 names, but that gap is most plausibly the jump inflating realized, **not cheap premium**. Do not read it as a buying signal. [INFERENCE from FACTs above; what would change it: a fresh 20d window with the jump aged out, or a clean IV-rank series]
2. **NVDA is the standout: ~88–92% IV across both expiries, ~1.7× its 20d realized (51.9%).** The front expiry (Nov 13, no earnings inside) is as rich as the earnings expiry (Nov 20) — term structure is flat-to-inverted, not the usual earnings hump. [FACT — desk pull] The elevation is therefore not purely earnings-driven; it reflects the recent realized regime plus the Nov 17 event. Either way, premium into NVDA earnings = avoid. [INFERENCE]
3. **Live-pull mechanics note:** Yahoo options auth worked today (cookie+crumb returned 200s); the failure mode is timing, not access — the 13:54 PT nightly pull lands after the weekly expiry dies, and any 13:30 PT research pull lands after the close on closing marks. A pre-close IV pull (before 13:00 PT / 16:00 ET) would give tradable quotes and a live front expiry; as run, 1-DTE IVs are noise-sensitive (a $0.05 quote error moves IV several points) and SPY/QQQ marks fail parity. [FACT — pull outcome; INFERENCE on the fix]
- Desk status: DELIVERED with caveats — IV levels obtained live (not from the NULL file), IV rank UNVERIFIED, all verdicts WINDOW-CONTINGENT, SPY/QQQ/MSFT-11-20 levels parity-flagged.

## Desk 4 — Open Quant/AI Model Lab

**Sweep complete. 7 new candidates, all scored with the repo scorer (run, never hand-computed), all WATCH. No TEST, no INTEGRATE (run max 59). All 7 appended to the ledger (#261–267).**

| # | Candidate | Source / date | Scorer | Disposition + reason |
|---|---|---|---|---|
| 261 | Kratsios/Limmer/Buehler/Horvath/Saqur — "AFNO: Universal Certifiably-Arbitrage-Free Operator Learning Framework for European Call-Price Surfaces" | arXiv:2611.12899v1, submitted 13 Oct 2026, abstract read at source | 59 — PREPRINT, signal 4 / data 3 / impl 2 / risk 4 / cred 4, reproducible False | **WATCH** — run's top score, 6 under TEST. Certifiably arb-free neural operator; key doctrine point (source-reported, UNVERIFIED): a nearest arb-free correction of an unconstrained surface need not exist, so post-processing cannot restore no-arbitrage — supports the desk's arb-check-first stance. No author code link → reproducibility not established. |
| 262 | Lerner — "Making sense of rule 605" | arXiv:2611.13365v1, submitted 9 Nov 2026, abstract read at source | 48 — PREPRINT, 3/3/2/3/3, reproducible False | **WATCH** — late catch (announced 11 Nov, missed by Nov 11 sweep). Rule 605 reports (Virtu/SoHo, Jan 2021–Mar 2024); LR+LSTM poor at predicting order-probability laws but month-to-month correlations highly stable/predictable (source-reported, UNVERIFIED). No code link. |
| 263 | Tiwari/Majumdar — "Asian option valuation under price impact" + AsianOption R package | arXiv:2512.07154v3, revised 10 Nov 2026; CRAN AsianOption v0.2.0, GPL ≥ 3 | 45 — PREPRINT, 2/2/3/3/3, reproducible False | **WATCH** (band floor) — version trigger. Dealer bid/ask via utility indifference; package implements the framework (verified at CRAN-mirror level only, not run). No watchlist lane (LME-metals context); transferable item is the impact-aware pricing pattern only. |
| 264 | Aboussalah et al — "FINN: Finance-Informed Neural Network" | arXiv:2412.12213v2, revised 11 Mar 2026, abstract read at source | 54 — PREPRINT, 4/3/2/4/3, reproducible False | **WATCH** — late catch (Dec 2024 paper). Replication-objective pricing; put-call parity emerges endogenously; IV-surface reconstruction closer to market IVs than Heston calibrations (source-reported, UNVERIFIED). No code link. |
| 265 | Feng et al — "FI-DeepONet" (Finance-Informed Operator Learning) | arXiv:2609.33213v2, revised 5 Oct 2026, abstract read at source | 45 — PREPRINT, 3/2/2/3/3, reproducible False | **WATCH** (band floor) — late catch (math.NA, outside q-fin sweep categories). BS-carrier + admissibility layer enforces no-arb bounds; index-option test: accurate without retraining but does NOT beat the same-input analytic formula (author-honest bound). No code link. |
| 266 | Lundquist/Eck — "Volatility Forecasting Using Similarity-based Parameter Correction and Aggregated Shock Information" | arXiv:2406.08738v3, 24 Aug 2026, abstract + intro read at source | 48 — PREPRINT, 3/3/2/3/3, reproducible False | **WATCH** — late catch via SSRN/vol search. Donor-pool shock aggregation adjusts h-step GARCH forecasts with no post-shock data needed; real-data example is 2016 US election vol (source-reported, UNVERIFIED). No code link in full text (searched "github" = 0 hits). |
| 267 | EODHD — Options Explorer (+ 6 more MIT apps) | Medium announcement by EODHD COO, 6 Nov 2026, read at source | 48 — REPOSITORY, 3/2/3/3/3, reproducible False | **WATCH** — vendor release. GEX-by-strike + gamma flip + IV surface explorer. **Data gate (vendor-stated): the chain is a PAID add-on (~40–70 calls per large chain); free plan (20 calls/day) covers quote only — free value is the code pattern, not data.** MIT claim + repo contents UNVERIFIED (GitHub leg banned). |

All claim labels are FACT only where read at source (dates, versions, license icons); paper findings are labeled source-reported / UNVERIFIED (abstract-only reads, full papers not read). No Risk of Ruin touched; no trade authorization; no licensed material reproduced.

**Ledger:** all 7 rows appended once to the latest table in `quant-lab-ledger.md` (#261–267; verified on disk: 7 rows). Run log entry added to the Jidoka log. No candidate lives only in a daily file.

**Re-checks (no movement):** #9 still v2 (2026-10-19), #20 still v2 (2026-09-25), #21 still v3 (2026-10-16), #25 still v3 (2026-09-17), #31 still v3 (2026-10-22) — abs pages read at source, all stay WATCH. #4/#13/#14/#15/#30 carried from the 2026-11-11 re-check (no movement, no trigger). #245 Strasmore page live with 2026-11-10 IV-leaders data; #24 FlashAlpha site live with a new sell-window endpoint — free-key email signup still a user decision, TEST blocker unchanged.

**Gaps / failures (explicit):**
- **Nov 11 submission window is provisional, not confirmed empty.** No Nov 11-submitted q-fin item was visible in any leg at sweep time (~13:30 PT): academ.us feed tops out at 2611.14325 (submitted Nov 10); TR new listing shows only Nov 9–10 submissions. Per the 2026-11-09 lag lesson, next run must re-cover the Nov 11 window — announcement lag has bitten twice before.
- **GitHub leg skipped** per the run brief's ban — #267's MIT claim and #261/#264/#265 code absence rest on arXiv-page evidence only.
- **academ.us article links 403'd** (two attempts); recovered by opening the arXiv abs pages directly. No external state changed.
- **Not ledgered:** 2606.29290 (Yılkı supply-chain LLM embeddings) — its v2 (10 Nov 2026) is a **withdrawal** by the author, not a revision; fail-closed, no score.
- Desk status: DELIVERED.

## Desk 5 — Weather / War / Logistics Futures Events

**Question:** What fresh catalysts (USDA, EIA, geopolitics/logistics) hit in the last ~48h, and what do the relevant futures curves appear to be pricing?

| # | Event | Date/time | What happened — FACT | What futures appear to be pricing — INFERENCE | Source |
|---|---|---|---|---|---|
| 1 | EIA Weekly Petroleum Status Report, w/e Nov 6 | Released Thu Nov 12, ~12:00 ET (delayed one day by Veterans Day holiday, Nov 11) | Commercial crude +4.657M bbl to 414.4M bbl vs ~−0.7M to −1.5M expected (WSJ survey −0.7M; InvestingLive consensus −1.109M) — a ~5.8M bbl upside surprise, ending five straight weekly draws. Gasoline +1.799M to 210.8M (+1% vs 5-yr avg). Distillate +4.071M to 103.3M vs −1.2M expected (8% below 5-yr avg). Cushing +0.106M. SPR −2.6M to 279.5M. US production ~14.0M bpd (+10k bpd w/w). Higher imports + lower exports drove the build. | Bearish inventory print on its face, but the market rallied anyway — futures are pricing the geopolitical risk premium (rows 3–4), not the inventory surplus. A build of this size with prices up says supply-risk, not demand, is the marginal price driver right now. | Morningstar/Dow Jones, Nov 12 12:47 ET, citing EIA; corroborated by XTB and InvestingLive on all four headline numbers. EIA landing page confirmed live (crawled 21:27 UTC) but its tables did not render in text fetch, so figures rest on the three agreeing secondaries. |
| 2 | USDA November WASDE (WASDE-677) | Released Tue Nov 10, 12:00 ET | Corn: yield cut 181.2 → 179.6 bu/acre; production −141M bu to 15.893B; ending stocks 1.758B bu vs 1.846B expected; farm price cut $4.70 → $4.60/bu. Soybeans: yield 53.1 → 53.3; production 4.574B; ending stocks 300M bu vs 332M expected. Wheat ending stocks +3M to 743M. Sugar stocks-to-use 13.87% (from 14.90%). Beef production cut; pork raised; broilers cut. World grain production +5.24M tonnes, ending stocks +9.02M tonnes. | Tighter-than-expected US corn/soy balances, but USDA itself cut the corn price forecast — the market read it as modestly supportive, not a shock. Dec corn settled +9¾¢ to $4.49 and Jan soybeans +39¾¢ to $12.28 on Nov 10. No food-inflation shock signal: the cut is supply-side and partly offset by lower feed/export use. | USDA WASDE-677 via Protein Pulse, Block2Learn, COT-Trader, PGI/Klarenbach (all agree on figures); futures settles via Brownfield as carried by PGI. Analyst read (Allendale's Rich Nelson): "largely routine," November WASDE rarely produces big shocks. |
| 3 | US–Iran: Trump ends deal track; IRGC tanker-mine claims in Hormuz | Thu Nov 12 (Trump message) / late Wed Nov 11 (IRGC claim) | Trump posted via Truth Social that the US is "no longer interested in any deal with Iran" after days of waiting for an agreement — dashing expectations of an early Strait reopening. IRGC Navy claimed two supertankers were disabled by naval mines late Wed Nov 11 while transiting an "unauthorized route" under US escort (Iranian state media). Washington has dismissed related IRGC tanker claims. CENTCOM maintains convoy lanes are swept of ordnance. | WTI Dec futures +$1.96 (+2.27%) to $88.49 and Brent up ~2% in the Thu US session — the market is pricing a higher probability that the Strait stays constrained and no Iranian barrels return. This is a risk-premium move, not a physical-supply move: physical flows are recovering (row 4). | TradingView/dpa-AFX, Nov 12 19:52 UTC; XTB, Nov 12; Region Alert Hormuz intel, refreshed Nov 12 09:00 UTC. IRGC claim is single-source (Iranian state media) — treat the strike itself as UNVERIFIED; the Trump message and the price move are FACT. |
| 4 | Hormuz / Middle East physical flows — underlying balance improving | Week of Nov 10–12 | Middle East crude exports ex-Iran have recovered to >90% of pre-war levels via Hormuz + bypass routes; global supply is ample and the world is no longer drawing inventories weekly. Physical grades trade at deep discounts to Brent/WTI (e.g., Canadian crude below $60). Refined-product flows from the Gulf are only ~60% of pre-war; diesel/jet still elevated, ~⅓ of the diesel-price rise attributed to Ukrainian strikes on Russian refineries. 37 vessel attacks in Oct 2026 — highest monthly total since the conflict began Feb 28 (Washington Institute data). Kpler: disrupted Middle East crude/condensate ~3.8M bpd, falling. Saudi/Iraqi production back to pre-conflict levels. | Brent ~$91–93 is a stalemate price: no imminent third round of fighting is priced, but no deal dividend either. If a US–Iran deal were reached, oil would trade "significantly cheaper" than ~$90. The curve is pricing limbo, with a fat downside tail on a deal and upside tail on escalation. | Bloomberg Opinion (Javier Blas), Nov 12; Reuters via StockBiz, Nov 12; Kpler via StockBiz. |
| 5 | Russia–Ukraine Abu Dhabi talks | Nov 10–11 (two days) | Ended with NO ceasefire or peace agreement; territory remains the blocking issue. Agreed in principle: a large-scale POW exchange (1,000-for-1,000 or 1,500-for-1,500 discussed), ICRC-facilitated, no date or confirmed list yet. US envoys Kushner/Witkoff travel to Moscow Thu Nov 12. Russia launched 163 drones + cruise missiles overnight Nov 11 at Ukrainian energy/transport/fuel infrastructure. Ukrainian drone attacks have cut ~30% of Russian refining capacity since late Oct (industry sources). | No energy-market relief priced from the talks: no ceasefire, no change to the Russian-refinery outage or the diesel tightness it feeds. The POW deal is humanitarian, not a supply event. | BusinessDay/Reuters, Nov 11; First Move Daily, Nov 11; The Leadsman, Nov 12; StockBiz/Reuters for refinery figure. |
| 6 | EIA November Short-Term Energy Outlook + natural gas | STEO released Tue Nov 10 | EIA cut its Henry Hub winter forecast to $2.87/MMBtu (Nov–Mar), −16% vs last month's forecast; 2026 avg $3.37, 2027 $2.88. End-Nov storage forecast raised 67 Bcf to 3,840 Bcf on a warm start to November (13% fewer heating degree days vs 10-yr avg). Latest storage print (Nov 5, w/e Oct 30): working gas 3,801 Bcf, +77 Bcf injection, −2.8% y/y, +1.4% vs 5-yr avg. Next storage report Fri Nov 13, 10:30 ET (delayed by Veterans Day). | Gas futures are pricing a mild winter and production growth outpacing demand — a soft gas tape into winter, the opposite of the oil risk premium. No weather-driven gas catalyst on the board. | EIA STEO Nov 2026 (eia.gov); FXEmpire, Nov 12; NGI via aiagentupdate, Nov 11. |
| 7 | OPEC Monthly Oil Market Report | Released Wed Nov 11 | OPEC+ pumped ~41.23M bpd, up ~2.04M bpd in September (per dpa-AFX summary). OPEC left global demand-growth forecasts unchanged; no change to 2027 outlook. | Neutral for the curve: no OPEC demand downgrade to offset the inventory build, no new supply restraint signal either. | TradingView/dpa-AFX, Nov 12, citing OPEC report. |

**Price tape (FACT, with timestamps — levels moved materially intraday):**
- Wed Nov 11 close: Brent +$1.27 (+1.39%) to $92.76; WTI +$0.49 (+0.57%) to $86.53 (Reuters via StockBiz).
- Thu Nov 12 Asian session: Brent −1.58% to $91.29; WTI −1.43% to $85.29 (Region Alert).
- Thu Nov 12 US session: WTI Dec +2.27% to $88.49; Brent up ~2% (TradingView/dpa; XTB). **Current live level at 13:30 PT is UNVERIFIED** — no single-timestamp quote was pulled; do not quote a "current" price from the above.

**Observations:**
1. **Oil is pricing geopolitics, not fundamentals, today.** The EIA build was the largest bearish surprise in weeks (+4.7M vs a draw expected, ending five straight draws) and prices rose ~2% anyway on the Trump/Iran headline. For premium/IV purposes: energy-linked vol is event-driven and headline-sensitive, not inventory-driven — any IV-vs-realized read on energy names this week is headline-contingent. (INFERENCE from FACTs in rows 1 and 3.)
2. **The diesel/distillate tightness is the durable physical story, not crude.** Distillates are 8% below the 5-yr average despite this week's +4.1M build, Gulf refined-product flows are only ~60% of pre-war, and ~30% of Russian refining capacity is offline from Ukrainian drone strikes. If a logistics desk watches one spread, it is diesel/crack, not flat crude. (INFERENCE from FACTs in rows 1, 4, 5.)
3. **No USDA/EIA calendar shock ahead this week.** December WASDE is expected to be quiet (routine demand adjustments; the next big date is the Jan 12 annual production summary + Grain Stocks). Next EIA petroleum report Wed Nov 18, 10:30 ET; next gas storage Fri Nov 13, 10:30 ET. (FACT per EIA schedule pages and Allendale via Oklahoma Farm Report.)

**Failures / gaps (explicit):** EIA's own weekly petroleum page was fetched live but its data tables did not render as text, so EIA figures are sourced from three agreeing secondaries (Morningstar/Dow Jones, XTB, InvestingLive) rather than the primary PDF — figures agree to the decimal across all three, but flagged as secondarily-sourced. IRGC mine-strike claim on two supertankers (Nov 11) is single-source Iranian state media and partially denied/dismissed by Washington — the strike itself is UNVERIFIED; only the claim and the market reaction are FACT. Houthi drone attack on Saudi East-West pipeline Pumping Station 11 (Region Alert, Nov 12) is single-source — UNVERIFIED, not included in the table above. No live futures quote was pulled at a single timestamp; intraday price levels above carry their session timestamps and the current level is UNVERIFIED. No material fresh catalyst found for watchlist names from this desk's lens — nothing in rows 1–7 is a direct watchlist-name event; the read-through is macro/vol only.

No government "data blackout" framing used; EIA and USDA releases are on schedule (EIA petroleum delayed one day only by the Veterans Day holiday, per EIA's published schedule).
- Desk status: DELIVERED.

## Desk 6 — Box / Parity Observer

**Verdict: no new parity violation and no new index-methodology document today. One standing item carried forward (announced Oct 23, next dated milestone Dec 4).**

**Parity — no violation found:**
- **FACT** (Saxo Options Brief, Nov 4–5, 2026): put-call parity on the 18 Nov options implied 19.96 vs the 19.90 settlement (Nov 4) and 17.73 vs 17.74 (Nov 5) — parity holding within ~0.06 index points, i.e. no exploitable break. Sources: https://www.home.saxo/content/articles/options/blue-wave-meets-a-one-day-premium---options-brief---4-november-2026-04112026 and https://www.home.saxo/en-gb/content/articles/options/vote-premium-drains-from-the-front---options-brief---5-november-2026-05112026
- **FACT** (independent Derivatives Lab analysis of 2,565 CBOE SPX quotes, snapshot Oct 16, 2026): put-call parity regression "essentially exact"; a single small calendar violation of 4.9×10⁻⁴ in total variance between the 2M and 3M slices — far below any exploitable threshold after costs. Source: https://www.deyirviel.com/portfolio/derivatives-lab/
- **FACT:** the only parity breaks surfaced in today's sweep were on crypto venues (Derive vs Deribit, e.g. BTC/HYPE reversals) — not watchlist-relevant; no SPY/QQQ/single-name US equity parity-violation analysis published. Source: https://www.optionly.com/arb
- **INFERENCE:** deterministic parity (C − P = D(F − K)) continues to hold in listed US index options; nothing in today's check overrides a model output on parity grounds. What would change it: a published same-day SPX/SPY/QQQ parity residual exceeding transaction costs.

**Index methodology — one standing item, not new today:**
- **FACT** (S&P DJI consultation results, announced Oct 23, 2026; corroborated by Bloomberg via multiple secondary reports): S&P U.S. Style Indices methodology changes take effect before market open **Dec 21, 2026**; pro-forma files reach clients **Dec 4, 2026**. Growth drops 12-month price momentum (retains 3-yr EPS-change/price and 3-yr sales-per-share growth); value adds intangibles-adjusted book-to-price, free cash flow-to-price (excluded for banks, insurers, real estate and some financials), and a trailing/forward earnings-to-price average. Applies to S&P 500 / Composite 1500 / MidCap 400 / SmallCap 600 / S&P 900 / S&P 1000 style indices. Sources: https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing ; https://www.xponance.com/style-wars-inside-ftse-russells-proposal-to-redraw-the-line-between-growth-and-value/
- **INFERENCE:** watchlist relevance is indirect — SPY tracks the S&P 500, not the style sub-indices, so no direct SPY composition change; the Dec 21 reconstitution may move growth/value ETF holdings (notably AAPL/MSFT/NVDA style weightings). Next check date: Dec 4 pro-forma files.
- **UNVERIFIED:** the "$375B+ in passive funds tied to the affected gauges" figure is a Bloomberg Intelligence analyst estimate relayed by secondary sources; not confirmed against a primary S&P DJI or Bloomberg release.
- **FACT:** FTSE Russell's separate style consultation (50/50 growth-value split) remains open, comments due **Dec 11, 2026**, any change effective at the June 2027 reconstitution — undecided, watch only. Source: same Xponance link above.
- **FACT:** S&P DJI's MegaCap consultation concluded with **no changes** to S&P 500/MidCap 400/SmallCap 600 eligibility (financial viability, seasoning, IWF screens unchanged). Source: https://pr.mysugarhousejournal.com/article/SandampP-Dow-Jones-Indices-Consultation-on-Treatment-of-MegaCap-Companies-Results/6a21f639e80eb70d15dfa517
- **FACT:** Nasdaq-100 December reconstitution follows the standing calendar (rank Nov 30, announce after close Dec 11, effective open Dec 21); no new Nasdaq notice found as of this check. Source: https://pacifictape.com/explainers/sp500-nasdaq-100-inclusion-rules/

**Failures / gaps:** none. All searches returned. No primary spglobal.com press-release URL was returned by search, so the S&P item rests on corroborated secondary reporting of the S&P DJI results document, not the primary document itself — flagged above rather than asserted as primary-sourced.
- Desk status: DELIVERED.

**One-line version:** No new parity violation or index-methodology document today; parity checks (Nov 4–5) show SPX put-call parity holding within ~0.06 pts, and the standing S&P style-methodology change takes effect Dec 21 with pro-forma files Dec 4.

## Desk 7 — Bonds & Rates

**Question:** What does the current rates environment imply for premium pricing and growth-multiple pressure?

**Source:** repo module `hedge_desk.rates_desk.rates_environment()`, mode `REAL_FRED_RATES`, FRED public CSV (HTTP 200). Run executed 13:27 PT, 2026-11-12. All numbers below are verbatim from module output — none retyped from memory.

| Series | Level | As of |
|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-11-11 |
| Treasury 2Y (DGS2) | 4.73% | 2026-11-10 |
| Treasury 10Y (DGS10) | 4.98% | 2026-11-10 |
| 2s10s slope (10Y − 2Y) | +25 bp | 2026-11-10 |
| SOFR | 3.89% | 2026-11-10 |
| EFFR | 3.88% | 2026-11-10 |
| OBFR | 3.88% | 2026-11-10 |
| SOFR − EFFR spread | **+1 bp** | 2026-11-10 |
| Fed funds change over 60-day window | +0.25 pp | — |

Module-reported curve shape: **UPWARD_SLOPING** (curve_slope 0.031250, lookback 60 days).

**Slope direction — FLATTENING (FACT, recomputed from module history):**
- 2026-11-06: 10Y 4.86 − 2Y 4.51 = **+35 bp**
- 2026-11-09: 10Y 4.88 − 2Y 4.56 = **+32 bp**
- 2026-11-10: 10Y 4.98 − 2Y 4.73 = **+25 bp**

The curve flattened **7 bp in one day** and **10 bp over two sessions**, driven by the front end: 2Y rose 17 bp (4.56 → 4.73) while 10Y rose 10 bp (4.88 → 4.98). For context, the slope was ~47 bp on 2026-10-05 (5.31 − 4.84) — the flattening from ~47 bp to 25 bp over five weeks is a sustained move, not a one-day print.

**Funding stress — NONE (FACT):** SOFR 3.89% vs EFFR 3.88% = **+1 bp**; OBFR also 3.88%. All three overnight benchmarks are within 1 bp of each other. No sign of funding stress.

**Directional read for premium pricing (INFERENCE — rests on the FACTs above):**
- **Long rates near 5% (10Y 4.98%)** = elevated discount rates, which pressure growth multiples most — the watchlist's long-duration names (NVDA, TSLA, MSFT) carry the most multiple risk from this level.
- **Front-end rising faster than the long end (2Y +17 bp vs 10Y +10 bp in a day)** = the market is repricing near-term policy expectations upward, or at least removing expected cuts. A flattening curve at a ~5% long end argues against chasing premium-selling on growth names purely for yield — the carry is not being paid by a steep curve.
- **No funding stress (+1 bp SOFR–EFFR)** removes one tail risk for premium sellers: no dislocation in overnight funding that would force unwinds.
- **What would change this read:** a 2Y reversal back below ~4.60% (restoring the 35 bp slope) would signal the front-end repricing was a one-day move; a 10Y break above 5.00% sustained would add further multiple pressure. (FACT thresholds stated as triggers, not forecasts)
- Desk status: COMPLETE — no failures. Module ran clean on first attempt; no fallback to Yahoo yields was needed or used.

---

## Cross-desk reconciliation

- **NVDA Nov 17 earnings** — confirmed by three legs: Desk 1 (company notice + EarningsWatcher + OANDA), Desk 3 (IV-inputs file `next_earnings`), Desk 2 (Nov 19 earnings release as the likely next-dividend declaration trigger). No conflict. Implied move ±10.4–10.8% (Desk 1) vs IV ~88–92% (Desk 3) are consistent reads of the same elevated premium.
- **IV vs realized** — Desk 3's WINDOW-CONTINGENT verdicts and Desk 7's rates read agree on direction: no clean "cheap premium" signal anywhere; the apparent IV-below-realized gap is a jump artifact, and the flattening curve at ~5% long rates argues against yield-chasing premium sales on growth names.
- **Oil vs rates** — Desk 5's geopolitics-priced crude (+2% into a bearish EIA build) and Desk 7's no-funding-stress read are independent: no cross-desk contradiction; energy vol is headline-contingent, funding is calm.
- **Parity** — Desk 6 (published checks: parity holding) vs Desk 3 (Yahoo closing marks fail parity on SPY/QQQ): no contradiction — Desk 3's flags are about stale post-close marks, not market parity; deterministic parity stands.
- **Quant lab top item (#261 AFNO, score 59)** reinforces the desk's standing doctrine: no-arbitrage cannot be restored by post-processing a learned surface — consistent with Desk 3/Desk 6's parity-first stance.

## Sources (desk-level)

- Earnings: NVIDIA Oct 28 notice (via jorgai.com); EarningsWatcher; OANDA; Yahoo Finance options chain (cookie+crumb pull, 13:30 PT); SimianX Mag 7 tracker (Nov 3).
- Dividends: Nasdaq dividends calendar API (Nov 12, Nov 19, Nov 20, Dec 10, Dec 18, Dec 21); Apple IR dividend history; Yahoo v8 chart events; NVIDIA Q1 FY27 release; `dividend-count-standard.md`.
- Premium: `nightly/2026-11-11-iv-inputs.json` (as_of 2026-11-11T14:54:30-07:00); live Yahoo options-chain pull 13:28 PT (cookie+crumb, Black-Scholes inversion on bid/ask mids, r = 4%).
- Quant: arXiv abs pages (2611.12899, 2611.13365, 2512.07154, 2412.12213, 2609.33213, 2406.08738); EODHD Medium announcement 6 Nov 2026; repo scorer `hedge_desk.research_intelligence`; ledger `quant-lab-ledger.md` (#261–267).
- Futures: Morningstar/Dow Jones Nov 12 12:47 ET (citing EIA); XTB; InvestingLive; TradingView/dpa-AFX Nov 12 19:52 UTC; Bloomberg Opinion (Javier Blas) Nov 12; USDA WASDE-677 via Protein Pulse et al.; EIA STEO Nov 2026 (eia.gov); BusinessDay/Reuters Nov 11. EIA figures secondarily sourced (EIA tables did not render in text fetch) — see Desk 5 gaps.
- Parity: Saxo Options Brief Nov 4–5, 2026; Derivatives Lab (2,565 CBOE SPX quotes, Oct 16); S&P DJI consultation results (Oct 23, via secondaries); Xponance; S&P DJI MegaCap consultation results.
- Rates: repo module `hedge_desk.rates_desk.rates_environment()`, REAL_FRED_RATES, FRED public CSV (run 13:27 PT).

## Run notes

- IV-inputs freshness guard: file exists, as_of 2026-11-11T14:54:30-07:00, ~22.5h old — within the 26h guard (STALE-labeled, usable). ATM IV null for all six symbols (structural Yahoo timing failure persists); supplemented by a labeled live Yahoo pull.
- No government "data blackout" framing used anywhere; EIA/USDA releases on schedule (EIA delayed one day only by Veterans Day).
- Desk part files: `~/workspace/hedge-desk-research/parts/desk{1..7}_*.md` (recovered from agent session records).
- No git operations, no PRs, no code changes performed in this run.
