# Hedge-Desk Daily Research Package — Thu 2026-10-22

**Run:** `hedge-desk-daily-research`, scheduled 13:30 PT. Research and input only — no repo writes, no pushes, no PRs.
**Method:** 7 parallel desk subagents, each given the watchlist (SPY, QQQ, AAPL, MSFT, NVDA, TSLA), the `research` profile (claims traced to evidence; FACT/INFERENCE/SPECULATION/UNVERIFIED), the value-investor lens, and the hard boundaries (paper-only; no RoR; no trade authorization; fail closed on unverifiable numbers).
**Market-data rule:** Yahoo first, Nasdaq second, fallbacks. Yahoo v7 OPTIONS/QUOTE required cookie+crumb handshake (worked today). v8 CHART with UA alone.
**IV baseline:** `~/workspace/hedge-desk-research/nightly/2026-10-21-iv-inputs.json`, `as_of` **2026-10-21T13:54:03-07:00** (~24h old at the 13:30 start — **accepted under the 26h freshness guard**). Yesterday's file had null ATM-IV reads for all names except TSLA; the Premium desk supplemented with a labeled live post-close pull (2026-10-22 ~16:31–16:33 ET). IV *levels* below are live; IV *rank* is UNVERIFIED for all names (no free IV-history source).
**Government-data state:** NO shutdown — CR signed 2026-09-02, funding through Dec 11. EIA weekly (Wed) and USDA export sales (Thu) released ON SCHEDULE.

## Cross-desk synthesis: the 5 most decision-relevant items

1. **Middle-East escalation owns the macro tape today.** Houthi strikes on Saudi targets Wednesday (Dammam airport; Saudi oil field), US ordering diplomats/family out of Saudi, IRGC strikes on vessels in the Persian Gulf and mine collisions west of Hormuz. Brent closed **$112.92 (+3.8%)**, a near-five-month high; the Brent–WTI spread widened to **$13.70** (from $11.67) — the market is pricing waterborne-supply risk specifically, not generic crude risk. INFERENCE: the rally is geopolitical risk premium, not inventory — EIA's third straight crude draw (−3.1 Mb) was already absorbed Wednesday morning when crude was flat-to-down pre-attack. What would change it: a verifiable US/Iran de-escalation signal; or next week's EIA flipping to a build with shipping normalized. (Futures desk)
2. **MSFT earnings Wed 10/28 AMC is the live watchlist binary.** Options-implied ±5.45% (Oct-30 weekly straddle mid $28.38 / $521.08) vs **8.09% four-quarter average reaction** — FACT: the options market is pricing a *tamer* print than history suggests. Separately, the Oct-30 chain carries **44.15% ATM IV vs 21.73%** on the Oct-26 pre-event chain — ~22pp of implied vol sitting in the expiry that straddles the report. Desk rule stands: **premium into a binary event = avoid** (no new short premium into the Oct-30 chain). Consensus EPS $4.71 (14 ests; fiscal Q1 2027). (Earnings + Premium desks, consistent)
3. **TSLA Q3 landed — mixed, mild reaction.** −3.08% session vs 5.95% four-quarter average move; IV crushed 76.76% → 39.50% post-print (FACT). From Exhibit 99.1: GAAP net income $787M vs $1,373M (−42.7%), op margin −322bp, auto revenue −3.0%, opex +39.2% — but OCF $6,263M (flat YoY), FCF $1,531M, cash $45,447M (+$1.9B QoQ), and **services & other record $4,605M (+32.5%) with record $734M services gross profit**. INFERENCE (value lens): the cash engine and balance-sheet margin of safety are intact; the quarter's margin improvement was carried by services mix, not autos. **UNVERIFIED flag:** Nasdaq records actual EPS $0.20 vs $0.22 consensus (−9.09%), but the release's own GAAP diluted EPS is $0.22 — discrepancy flagged, not resolved. (Earnings + Premium desks, consistent)
4. **Rates: front end pinned between hot CPI and a guidance-free Fed.** FRED module (REAL_FRED_RATES, as_of 2026-10-22): fed funds effective **3.88%** (+0.25 over the window — Sept hike pass-through), DGS2 **4.81%**, DGS10 **5.13%**, 2s10s **32 bp** (flattened ~46→32 over the 60-day window; still upward-sloping). SOFR−EFFR−OBFR all print 3.88% → **0 bp funding stress**. Reuters poll (Oct 16–20): 94/100 economists expect hold Oct 27–28 at 3.75–4.00%, **all 100 expect a December hike**; September CPI printed hot at 3.7%. INFERENCE: with the 10Y above 5% the discount-rate drag on long-duration growth multiples persists — structural caution for rich-call writing against growth names on a "rates normalize" thesis, not a signal to add premium. What would change it: an Oct 28 surprise hike/guidance re-introduction, a sub-3.5% CPI unwinding the Dec-hike consensus, or 2s10s inversion. (Rates desk)
5. **AAPL Nov 2 AMC — the reverse tilt.** Implied ±5.05% (Nov-6 weekly straddle mid $17.60 / $348.22) vs **2.86% four-quarter average** — FACT: options are pricing *more* event risk than Apple's usually-calm prints warrant. AAPL was today's sole watchlist advancer (+1.23%). Dividend watch: no November dividend announced yet; AAPL historically declares in the earnings release (Oct 30, 2025 → ex Nov 10, 2025 precedent) — INFERENCE: if declared ~Nov 2, ex-date likely ~Nov 9–10 at the unchanged $0.27. Worth one re-check in the Nov 2–3 runs. (Earnings + Dividend desks)

### Secondary items (kept, not padded)
- **NVDA** (11/18, out of window): cleanest rich-vs-realized read — 33.13% IV vs 23.79% 20d realized on a clean (non-contingent) window — but today was a −4.40% single-name down day, so the richness is **compensation, not mispricing**. (Premium)
- **Window-contingent verdicts:** QQQ (35.4%), AAPL (36.7%), MSFT (34.8%) each have a single day driving >30% of 20-day realized variance — no clean IV-vs-realized verdicts on those names; roll out of the contingent day restores clean reads. (Premium)
- **Income desk:** only MSFT goes ex-dividend in the 4-week window — **11/19/2026, $0.98** (first payment at the raised rate; 24th consecutive year of growth, raise +7.7% declared 9/15). Consecutive-increase counts per standard: MSFT 24, AAPL 15 (re-verified against issuer this run — third-party screeners undercount at 4–5), NVDA 1. NVDA is now ~$24B annualized — 2nd-largest US dividend payer behind MSFT. (Dividend)
- **Grains:** Oct 9 WASDE was decisively bearish (record soy yield 53.1 bu/ac, corn 181.1 bu/ac; corn fell ~5%) vs today's strong USDA export sales (soy 2.84 Mt incl. China 2.18 Mt; corn 1.53 Mt, top of survey). Curves price a demand-vs-supply tug-of-war; soybeans the cleanest demand leg. Next WASDE Nov 10. (Futures)
- **Quant lab:** 4 new candidates scored with the repo's own scorer and appended to the ledger (rows #124–127). Two WATCH: **#124 volforge** (score 52 — offline-first arb-aware pricing/vol lab, MIT, 29 pytest files; next: sandbox suite) and **#125 qqq-volatility-forecaster** (score 55 — free-data QQQ VRP methodology with year-by-year OOS + 21-day leakage gaps; **line-stopped: NOLICENSE**). Two ARCHIVE (Itkin DSINC extension, LLM factor-mining). No candidate reached TEST. Most decision-relevant: #125's methodology is the most premium-desk-applicable find of the week — unblocked only by licensing. Semantic Scholar leg 429'd (transient; arXiv + GitHub legs carried). (Quant)
- **Parity:** nothing material. Standing position re-affirmed: deterministic parity math outranks models; no capturable violation in liquid SPX/SPY/QQQ chains. One tangential in-window note: SEC cleared Cboe to list $1-or-nothing binary options on company KPIs (~7 days ago, market-maker-only) — product-universe watch, not parity math. (Parity)

---

## Desk 1 — Earnings Event

| Name | Report date | Timing | Consensus EPS | Implied move | 4-Q avg |move| | Source |
|---|---|---|---|---|---|---|
| MSFT | Wed 2026-10-28 | AMC (Nasdaq "time-after-hours") | $4.71 (14 ests; fiscal Q1 2027; last yr $4.13) | **±5.45%** (ATM 520 straddle $15.18+$13.20=$28.38 / $521.08, Oct-30 wkly) | **8.09%** (−2.92, −9.99, −3.93, +15.51) | Nasdaq calendar; Yahoo v7 options |
| AAPL | Mon 2026-11-02 | AMC (Nasdaq "time-after-hours") | $2.00 (8 ests; fiscal Q4 2026; last yr $1.85) | **±5.05%** (ATM 350 straddle $8.20+$9.40=$17.60 / $348.22, Nov-6 wkly) | **2.86%** (−0.38, +0.46, +3.24, −7.35) | Nasdaq calendar; Yahoo v7 options |
| TSLA | **Reported Wed 2026-10-21** | AMC (established pattern; 10-Q filed 10/22) | Nasdaq recorded $0.20 vs $0.22 = **−9.09% surprise** | n/a (print out) | Realized reaction: **−3.08%** (vs 5.95% 4-Q avg) | Nasdaq calendar; SEC EDGAR 8-K/Ex. 99.1 |
| NVDA | ~2026-11-18 | n/a (outside window) | $2.49 forecast | — | — | iv-inputs file scan (not re-verified today) |
| SPY / QQQ | n/a | n/a | n/a | n/a | n/a | ETFs have no earnings |

**TSLA Q3 read from the release itself (Exhibit 99.1, 8-K filed 2026-10-21) — statement-analysis order:**
- Guidance vs consensus: qualitative outlook only, no quarterly revenue/EPS guide (FACT). Nasdaq $0.22 consensus; Nasdaq actual $0.20 → −9.09%. **UNVERIFIED nuance:** release states GAAP diluted EPS **$0.22** — equals consensus; conflicts with Nasdaq's recorded $0.20. Flagged, not resolved.
- GAAP vs headline: net income $787M vs $1,373M Q3-2025 (−42.7%); non-GAAP EPS $0.48 vs $0.50 (−4.1%). Operating income $718M vs $1,624M (−55.8%); op margin −322bp.
- Cash flow: OCF $6,263M (vs $6,238M, flat); capex $4,732M (vs $2,248M, >2×); FCF $1,531M (vs $3,990M YoY; vs −$1,092M in Q2). Net income $787M << OCF $6,263M — no receivables-quality red flag (INFERENCE).
- Segment margins: gross profit $5,494M (+8.7%), margin +160bp. Auto revenue $20,560M (−3.0%). Energy gen/storage $2,881M (−15.6%). **Services & other $4,605M (+32.5%) — record; services gross profit record $734M.** INFERENCE: margin improvement carried by services mix, not autos.
- Balance sheet: cash & investments $45,447M (+$1.9B QoQ). Opex $4,776M vs $3,430M (+39.2%) — spend front-running revenue (INFERENCE).
- Operations: deliveries 486,532 (−2.1%); production 464,391 (+3.8%); cumulative 10.2M. FSD subscriptions 1.74M (record). Energy storage 13.7 GWh (vs 12.5). Cybercab into Austin Robotaxi fleet Sep 3; ~2M unsupervised Robotaxi miles (8× QoQ); largest passenger-vehicle backlog in 4 years. Tesla Semi volume production (Nevada); Next Gen Roadster unveiled Oct 15; Optimus production (Fremont); Megafactory Texas began (50 GWh planned).
- Value-lens read (INFERENCE): cash engine intact, P&L compressed — margin of safety sits in the balance sheet, not this quarter's earnings. The −3.08% reaction reads "mixed, not bad."
- Access note: SEC Archives blocked curl (403 bot-check); the release was read via browser text fetch, not a press summary. Tesla IR blocked curl as well.
- Sources: `https://api.nasdaq.com/api/calendar/earnings?date=2026-10-28` (and 11-02, 11-18, historical dates), `https://www.sec.gov/Archives/edgar/data/1318605/000162828026066738/exhibit9914.htm`, Yahoo v7 options / v8 chart.

**Desk verdict:** MSFT implied 5.45% < 8.09% history (tamer print priced); AAPL implied 5.05% > 2.86% history (more event risk priced); TSLA print sealed (mixed, mild). What would change it: an Azure/AI-capex guide-down or services-margin re-rating for MSFT; an iPhone-cycle or China-demand surprise for AAPL.

## Desk 2 — Dividend Opportunity

Window 2026-10-22 → ~2026-11-19.

| Name | Ex-date | Record | Payable | Amount | Status |
|---|---|---|---|---|---|
| **MSFT** | **Thu 11/19/2026** | 11/19/2026 | 12/10/2026 | **$0.98/qtr** | FACT — declared 09/15/2026 (Nasdaq history); first payment at raised rate |
| AAPL | — | — | — | $0.27 last paid (ex 08/10/2026) | No November announced; declaration expected ~Nov 2 earnings → ex ~Nov 9–10 at $0.27 (INFERENCE) |
| NVDA | — | — | — | $0.25 last paid (ex 09/10/2026) | Next declaration at late-Nov FYQ3 earnings; ex ~Dec, out of window (INFERENCE) |
| SPY | — | — | — | $1.889 last paid (ex 09/18/2026) | Next expected ~12/18, out of window (INFERENCE from quarterly third-Friday pattern) |
| QQQ | — | — | — | $0.75143 last paid (ex 09/21/2026) | Next expected mid-Dec, out of window (INFERENCE) |
| TSLA | — | — | — | — | FACT: non-payer (0 dividend rows, yield N/A — Nasdaq) |

- **MSFT increase (FACT):** board raised +7.7% to $0.98 on Sep 15, 2026 — 24th consecutive year of growth. Nasdaq history confirms $0.91 → $0.98. No cuts, no specials among watchlist names.
- **NVDA context (FACT):** raised $0.01 → $0.25 on May 20, 2026 — now ~$24B annualized, 2nd-largest US dividend payer behind MSFT (~0.43% yield at $230). Out of window but reframes NVDA as an index income contributor.
- **AAPL raise cadence (FACT):** raises land with the May payment ($0.26 → $0.27 declared April 30, 2026, issuer IR history); no November raise expected.
- **Consecutive-increase counts (per dividend-count-standard.md, no drift):** MSFT **24** · AAPL **15** (re-verified against investor.apple.com this run: increases every calendar year 2013–2026; third-party screeners quote 4–5 — undercount) · NVDA **1** (streak starts 2026) · SPY/QQQ n/a (variable ETF distributions) · TSLA none.
- Sources: api.nasdaq.com (per-symbol histories, upcoming-dividends calendar); investor.apple.com dividend history (fetched 2026-10-22); Yahoo v8 chart events=div (SPY); quiverquant.com, capitalsnitch.com, stockinvest.us, lighthorse.io.

**Desk verdict:** only MSFT ex 11/19 ($0.98, first at raised rate) in window; AAPL's November dividend is the single open variable. What would change it: an AAPL declaration ~Nov 2 with ex-date ≤ Nov 19; any unscheduled special; earlier-than-usual December SPY/QQQ declarations (not expected).

## Desk 3 — Overnight Premium (IV)

IV-inputs baseline `as_of` 2026-10-21T13:54:03-07:00, accepted under the 26h guard. **All IV levels below are LIVE** (Yahoo v7 options, cookie+crumb, 2026-10-22 ~16:31–16:33 ET, post-close); IV rank UNVERIFIED across all names.

Market context today (FACT, Yahoo v8 close-to-close): broad risk-off. SPY −1.18% (763.96), QQQ −2.86% (704.47), AAPL +1.23% (348.22, sole advancer), MSFT −2.23% (521.08), NVDA −4.40% (212.21), TSLA −3.08% (374.58).

| Symbol | Realized 20d (file) | Window-contingent? (max single-day share) | Live 1DTE (Oct 23) ATM IV | Term structure (live) | IV-vs-realized verdict |
|---|---|---|---|---|---|
| SPY | 8.89% | No (21.9%) | 12.70% | 4DTE 11.73%, 5DTE 12.58%, 6DTE 14.18% | **CLEAN**: +3.8pp over trailing realized — modest premium, consistent with −1.18% day |
| QQQ | 15.68% | **Yes (35.4%)** | 24.53% | 4DTE 22.73%, 5DTE 24.30%, 6DTE 26.28% | **WINDOW-CONTINGENT** — realized is one-day-driven; no clean richness signal |
| AAPL | 16.63% | **Yes (36.7%)** | 19.46% | 4DTE 19.40%, 6DTE 22.46%, 8DTE 23.25% | **WINDOW-CONTINGENT**; gentle back-end ramp = early Nov-2 earnings positioning |
| MSFT | 22.20% | **Yes (34.8%)** | 22.79% | 4DTE 21.73%, **8DTE 44.15%**, 15DTE 38.46% | **WINDOW-CONTINGENT** on 1DTE; 8DTE read is the story — IV nearly **doubles** into the Oct 28 report (~22pp earnings hump) |
| NVDA | 23.79% | No (25.0%) | 33.13% | 4DTE 32.01%, 6DTE 36.64%, 8DTE 38.34% | **CLEAN**: +9.3pp over realized — compensation for a −4.40% day, not mispricing |
| TSLA | 33.63% | No (25.6%) | 39.50% | 4DTE 37.13%, 6DTE 41.65%, 8DTE 41.42% | **CLEAN**: post-earnings IV crush confirmed — 76.76% @ 2DTE yesterday → 39.50% @ 1DTE; now only mildly rich vs realized |

Earnings in/near window: **TSLA reported Oct 21 AMC (FACT)** — non-GAAP EPS $0.48 vs $0.44 expected (Zacks/Quiver, Oct 21–22); binary over, crush confirmed. **MSFT Oct 28 AMC, 6 calendar days out (FACT — issuer press release Oct 7)** — ⚠️ premium-into-binary: Oct 30 chain 44.15% vs 21.73% on the Oct 26 pre-event chain → **no premium-selling into that binary**. **AAPL Nov 2 (FACT — Apple IR via MacRumors/AppleInsider, Oct 6)** — Oct 30 (8DTE) chain does NOT contain the event; 23.25% is pre-positioning, not binary premium; first call under new CEO John Ternus. NVDA ~Nov 18 (per iv-inputs file; not re-verified today) — no binary inside pulled expiries; 6DTE→8DTE slope is normal term structure.
Sanity checks (derivatives_options.md): front > back only where an event sits (MSFT hump passes); no inverted term structure anywhere; all ATM IVs positive and sane; 0DTE dead-contract marks failed closed (not quoted); TSLA 1DTE call 41.2% vs put 37.8% upside skew into a −3% day — INFERENCE: dealer/call-demand after the beat-and-down day (UNVERIFIED from positioning data).
Scripts: `/tmp/iv_pull_20261022.py`, `/tmp/iv_pull_term_1022.py`; raw JSON retained in /tmp for this run.

**Desk verdict:** Post-TSLA crush as expected; the only live binary is **MSFT Oct 28**, fully priced — no premium-selling into it; NVDA cleanest rich-vs-realized but that's compensation. What would change it: (a) QQQ/AAPL/MSFT windows rolling out of the contingent day (max_single_day_variance_share < 0.30); (b) MSFT Oct-30 IV collapsing post-report Oct 29; (c) a tomorrow pre-close re-pull replacing post-close marks.

## Desk 4 — Open Quant/AI Model Lab

Sweep: 60 recent arXiv q-fin items (4 in-window abstracts read at source); 22 new GitHub repos (3 deep-checked via API); Semantic Scholar 429'd (transient — arXiv + GitHub legs carried). Re-checks on prior candidates below.

| # | Candidate | Score | Disp. | Why |
|---|---|---|---|---|
| 124 | gunhoo1124-arch/volforge — offline-first arb-aware pricing/vol lab; BSM/Bachelier, analytic Greeks, Brent IV inversion, deterministic chains, fail-closed Heston boundaries, parity/quote/bound/staleness diagnostics | 52 | **WATCH** | MIT verified via API (FACT); tests/ has 29 pytest files, CI + CodeQL (FACT); code not run, 0 stars, single author. Next: sandbox pytest + fail-closed IV inversion check on live SPY chain; TEST only on passing suite |
| 125 | AleemS7/qqq-volatility-forecaster — QQQ 1-month vol forecasting, year-by-year OOS (21-day leakage gaps), options-overpricing measurement | 55 | **WATCH** (MONITOR_FOR_EVIDENCE, LICENSE_REVIEW_REQUIRED) | Claims source-reported UNVERIFIED (22.6% over naive; options overpriced realized in 80.4% of months). **Line-stopped: NOLICENSE → all-rights-reserved.** Next: license resolution, then sandbox reproduction of results/summary.json |
| 126 | Itkin, "DSINC beyond Heston" (arXiv 2610.28847) — damped-sinc American pricing to 3/2, SABR, GARCH | 33 | **ARCHIVE** | No code; methodologically relevant (watchlist options are American) but not desk-operational |
| 127 | Liu et al, "Lineage-Aware Search Control for LLM-Based Evolutionary Factor Mining" (arXiv 2610.29663) | 22 | **ARCHIVE** | Crowded LLM-factor lane already covered by #34/#57/#83; preprint, no code |

All four appended to `quant-lab-ledger.md` (rows #124–127). Triage exclusions: 12 NOLICENSE repos (code unusable); 3 out-of-scope (India, BTC, EU index); 1 live platform; 1 already logged (#115); marginal: MIT plotting plugin, single-script Bayesian SV research, 2 non-lane arXiv items.
Re-checks: #4 M2VN stays WATCH (name-collision repo only, no code); #35 VolPaint stays WATCH (no code); #37 holdout stays WATCH (PyPI still the v0.3.0 name collision); #7 merged 0DTE paper stays WATCH (SSRN 5641974 last revised 17 Jul 2026, no new RFS decision).
**Desk verdict:** no candidate cleared TEST; the two WATCH items merit weekly follow-up. #125 is the most decision-relevant find — a free-data QQQ VRP methodology with honest OOS discipline — but line-stopped on licensing. What would change it: volforge's suite passing in sandbox, or the QQQ forecaster gaining a license.
Process note: the ledger file holds candidate rows fragmented across sections and the Jidoka/Kaizen logs in triplicate — worth a one-time consolidation.

## Desk 5 — Futures Event (catalysts)

48–72h window, facts from primary sources; inference labeled.

1. **Escalating Middle-East conflict (Wed 10/21 → Thu 10/22).** FACT: Houthi strikes on Saudi targets — 1 killed, 8 wounded at Dammam civilian airport; 2 killed in drone attack on a Saudi oil field (Reuters). US ordered some diplomats/family out of Saudi missions, withdrawing family from additional regional missions (Reuters). IRGC Navy: 4 vessels in "illegal oil transfers" hit in northern Persian Gulf Thursday, 3 more collided with mines west of Hormuz; warned of wider response against US regional bases (Reuters). Kpler: ≥18 vessel attacks in 2 weeks; LSEG: Iran targeting tankers beyond Hormuz into the Gulf of Oman. INFERENCE: live supply-disruption risk on ~20% of global crude flow via Hormuz; the market is pricing a non-trivial escalation probability, not headline noise.
2. **EIA Weekly Petroleum Status (released Wed 10/21, 10:30 ET; week ending Oct 16).** FACT: crude −3.1 Mb to 412.5 Mb (3% below 5Y avg; 3rd straight draw; prior week −8.6 Mb). Gulf Coast −5.04 Mb to 229.32 Mb (lowest since Jan 2025). Gasoline −3.0 Mb (5% below avg); distillates +1.7 Mb but still 9% below avg; refinery inputs 16.6 Mb/d at 93.4% capacity. Products supplied 21.1 Mb/d (+3.2% y/y); gasoline 8.7, distillates 3.9 Mb/d (−2.4% y/y). API private print (Tue): deeper −4.93 Mb crude draw. INFERENCE: fundamentally supportive, but crude was *down* Wednesday morning ($97.69 WTI) — the inventory story was absorbed; the Oct-22 rally is geopolitical premium, not inventory repricing.
3. **EIA natural gas storage (released Thu 10/22, 10:30 ET; week ended Oct 16).** FACT: +77 Bcf; working gas 3,644 Bcf; −152 Bcf y/y (−4.0%), +35 Bcf above 5Y avg (+1.0%); 10th consecutive below-average injection. South Central 1,125 Bcf (−10% y/y, −3.4% vs avg) — the regional tight spot. Nymex front-month settled +0.2% at $2.796/mmBtu; 2-month low pre-report on warm forecasts. INFERENCE: muted/bullish-leaning but low-conviction; injection season ending just above the 5Y average leaves winter upside exposure on any cold snap; mild weather into early November is the nearer-dated headwind.
4. **USDA Weekly Export Sales (released Thu 10/22, 8:30 ET; week ended Oct 15).** FACT: soy net sales 2.84 Mt (vs 0.575 Mt prior; survey 1.1–3.0 Mt; China top buyer 2.18 Mt). Corn +36% w/w to 1.53 Mt (top of 0.8–1.5 Mt survey; Mexico 477.7 kt). Wheat −25% w/w to 239.6 kt (below 250–550 kt survey). Context — Oct 9 WASDE was decisively bearish: record soy yield 53.1 bu/ac (4.562 Bbu), corn 181.1 bu/ac (16.034 Bbu), ending stocks raised; corn fell ~5%. Next WASDE Nov 10. INFERENCE: strong demand data running against record-supply overhang — grain curves price a tug-of-war; soy has the cleanest demand-driven support.
Futures price check (Yahoo v8 chart, front-month, verified ~13:30 PT): WTI $97.15→**$99.22** (+2.1%); Brent $108.82→**$112.92** (+3.8%); natgas $2.79→$2.78 (flat); corn 463.25¢→460.25¢ (−0.6%); soy 1245.25¢→1253.50¢ (+0.7%); wheat 628.25¢→624.75¢ (−0.6%). FACT (computed): **Brent–WTI spread widened to $13.70** (from $11.67) — the premium sits in waterborne barrels. Brent touched a near-5-month high intraday ($111.64 at 0626 GMT Thursday, Reuters).
Sources: EIA via oilprice.com / tradingview (Reuters, DJN, dpa_afx) / oilvoice.com / xtb.com; Reuters via northlandnewsradio.com and angelone.in; EIA natgas via oilandgas360.com / el7.ai / WSJ; USDA via morningstar.com (Dow Jones Newswires); WASDE context via global-agriculture.com, rfdtv.com; Yahoo Finance v8 chart.

**Desk verdict:** geopolitical risk, not fundamentals, owns the energy curve — Brent near a 5-month high with the widest Brent–WTI spread in the 5-day window, while natgas balances into winter just above its 5Y average; grains are a separate book (record supply vs strong export sales). What would change it: a verifiable US/Iran de-escalation signal compressing the crude risk premium; or next week's EIA flipping to a crude build with shipping normalized. SPECULATION: whether Gulf shipping attacks broaden into a Hormuz chokepoint disruption — no confirmed interdiction of commercial crude flows as of writing; the premium could compress fast on a de-escalation signal.

## Desk 6 — Box/Parity Observer

**One line: nothing material on parity mechanics this week.**
Screened: optionscout.ai "Put-Call Parity" explainer (published 2026-10-17 — retail education, no new analysis); SPX box-spread financing coverage (~28 days old, outside window — ~$1.7B daily notional record; box-implied yield premium over SOFR averaged ~32 bps, recently ~69 bps — INFERENCE, single secondary source, UNVERIFIED against Cboe primary: boxes trading as financing instruments, not arbitrage; keep on the Bonds & Rates funding-stress watchlist as a passive indicator, not a trigger).
Tangential in-window product note (not parity methodology): SEC cleared Cboe to list $1-or-nothing binary options on company KPIs (~7 days ago; market-maker-only exemption; Cboe Clear US; disclosure doc pending SEC review) — new options product class settled on earnings-filing KPIs; watch on the product-universe side, not a parity-math change.
Standing desk position (re-affirmed): deterministic parity math (C − P = e^(−rT)(F − K); box = strike-width payoff) outranks any model output; observed deviations in liquid SPX/SPY/QQQ chains remain explainable by spreads, borrow costs, and early-exercise terms. No change to any parity screen or implied-rate calibration.

## Desk 7 — Bonds & Rates

Module: `hedge_desk.rates_desk.rates_environment()`, mode **REAL_FRED_RATES**, `as_of` **2026-10-22**, data source `fred-public-csv-http-200`. **RAN SUCCESSFULLY.** All numbers from module output — nothing retyped from memory.

| Series | Level | Latest obs. | Note |
|---|---|---|---|
| Fed funds effective rate (DFF) | **3.88%** | 2026-10-21 | change over window +0.25 (Sept hike passing through) |
| FRED DGS2 (2Y) | **4.81%** | 2026-10-21 | 60-day history in module output |
| FRED DGS10 (10Y) | **5.13%** | 2026-10-21 | 60-day history in module output |
| 2s10s spread | **32 bp** | 2026-10-21 | slope +0.04, shape UPWARD_SLOPING |

Funding-stress gauge: SOFR 3.88% = EFFR 3.88% = OBFR 3.88% (2026-10-21) → **SOFR−EFFR 0 bp** — no measurable funding stress; year-end funding markets orderly.
Curve read (60-day lookback, FACT): 2Y rose ~57 bp (4.24→4.81); 10Y rose ~43 bp (4.70→5.13); 2s10s **compressed ~46→32 bp — flattened ~14 bp**, still upward-sloping, not inverted. Both ends retreated from early-October highs: 10Y touched 5.31 on Oct 5 (−18 bp since); 2Y topped 4.92 on Sep 28. Past week modest rebound (10Y 5.09→5.13; 2Y 4.74→4.81).
Directional read for premium pricing: INFERENCE — with the 10Y still above 5%, discount-rate drag on long-duration equity multiples persists; structural headwind for writing rich calls against growth names on a "rates normalize" thesis. That rates support premium pricing is caution about carry-style risk in long-growth positioning, not a signal to add premium. Curve flattening reduces the term-premium bid for long-dated (LEAPS-type) positioning at the margin. Short-end carry backdrop neutral (0 bp SOFR−EFFR).
Fresh events (labeled): FACT — Reuters poll (Oct 16–20, published Oct 20): **94 of 100 economists expect the FOMC to hold Oct 27–28 at 3.75–4.00%; all 100 expect a December hike**. September CPI printed hot at **3.7%**; fed funds futures briefly priced an October hike ~50% before falling back toward ~20%; current CME-type reads put October hold ~83–87%. FOMC raised 25 bp in September; Chair Warsh has issued no forward guidance. Next decision **Oct 28, 2:00 pm ET**. INFERENCE: the front end is caught between a hot CPI and a quiet, guidance-free Fed — rates vol into next Wednesday's decision is the premium-relevant risk, not the hold itself.
Sources: FRED module output (JSON in run state); Kitco/Reuters Oct 20; RealClearMarkets Oct 22.

**Desk verdict:** rates elevated, curve flattened-but-upward, zero funding stress — no new premium mispricing signal from the desk today. What would change it: (a) Oct 28 surprise hike or guidance re-introduction (re-steepening/rate-vol repricing); (b) sub-3.5% CPI unwinding the December-hike consensus (front-end rally, re-steepening); (c) 2s10s flipping negative (inversion = regime change).
