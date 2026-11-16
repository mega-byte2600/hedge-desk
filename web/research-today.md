# Hedge-Desk Daily Research — Mon 2026-11-16

**Run:** 13:30 PT, Mon 2026-11-16. **Package as-of:** ~13:35 PT Nov 16, 2026 (post-close pulls where noted).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA. **Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety.
**Labels:** FACT = primary source + as-of; INFERENCE = stated logic from FACTs; SPECULATION = open question, no basis asserted; UNVERIFIED = looked, could not confirm.
**Standing:** Research and input only — no git, no PRs, no code changes. Paper-only; never estimate Risk of Ruin; never propose trade authorization.
**Government data:** NO federal shutdown — CR passed 2026-09-01, funding through Dec 11. EIA weekly and USDA releases on schedule (WASDE Nov 10, EIA Nov 12, Crop Progress Nov 16 — all released normally).

## Top 5 decision-relevant items (synthesis)

1. **NVDA reports Tue Nov 17 after close — the only watchlist earnings event, and the highest-stakes one of the quarter.** Options imply ~9.7% (Nov 20 straddle $15.10 / $156.14); the last four reports averaged −2.8% signed (all four down), so the market is pricing ~3.5× the recent realized move. Stock is −31.5% since the last print. First report under interim CEO Colette Kress. (Desk 1, FACT; Desk 3 concurs on the event.)
2. **The Huang resignation claim HOLDS — verified, not stale.** SEC Form 8-K filed Nov 12 (event Nov 11, accession 0001045810-26-000082): Board accepted Jen-Hsun Huang's resignation as President, CEO and director, effective immediately; EVP & CFO Colette M. Kress named interim CEO; Harvey C. Jones named Board Chair. The Nov 12 brief was correct on substance; only its "that day" timing was off by one day (announcement Nov 12, event Nov 11). (Desk 1, FACT — primary source.)
3. **No clean IV-vs-realized verdict is issuable on any name today.** All six symbols are WINDOW-CONTINGENT — the Nov 5 crash day still drives 37–54% of 20-day realized variance — and IV rank is UNVERIFIED across the board (no free IV-history source). Live post-close pull: NVDA Nov 18 expiry IV 116.17% is event vol, not a mispricing to sell into — premium into the binary event = AVOID. (Desk 3.)
4. **Desk 7 unchanged: 25bp hike Dec 9, tally 5 HIKE / 1 CUT / 4 NEUTRAL.** 10Y rose to 5.15% (+17bp since Nov 10; Gordon multiple −13.5% from the Nov 6 anchor — re-anchor to 5.15%). Kalshi 50bp tail halved to $0.06 (was $0.12 Nov 13); markets now agree on ~95% hike. Waller's trigger fired (Oct core CPI +0.296% m/m, at his "around 0.3%" threshold) and the market faded it anyway — the >25bp price fell after the print. (Desk 7.)
5. **Crude sold off ~3% today on the IEA's flip to a Q4 surplus call** (Nov 13 report: ~1.7 mb/d surplus, first since the Iran war began), even as Hormuz tanker attacks continue — WTI $85.39 intraday. The operative tension is crude-loose vs diesel-tight (distillate ~8% below its 5-yr average). WASDE Nov 10 tightened corn/soy ending stocks below trade expectations. Next EIA weekly Wed Nov 18, 10:30 ET. (Desk 5.)

**Cross-desk checks:** NVDA close $156.14 agrees across Desks 1, 2, 3 (FACT). SPY $739.95–96 / QQQ $661.75 agree across Desks 2, 3. No contradictions required resolution. Desk 7's rates read (hike odds ~95%) is consistent with Desk 5's gold slide (−0.6%, lowest since Sept 2025) — same repricing, two lanes.

---

## 1. Earnings Event desk

**As-of:** ~13:30 PT Nov 16. Sources: Nasdaq earnings calendar API, Yahoo v7 options + v8 chart (cookie+crumb), SEC EDGAR Form 8-K.

| Name | Report date | Timing | Consensus EPS | Options-implied move | Hist. avg earnings-day move |
|---|---|---|---|---|---|
| **NVDA** | **Tue Nov 17, 2026** | After close | $2.49 (14 ests) | **~9.7%** (Nov 20 weekly ATM straddle $15.10 / $156.14); 8.4% on Nov 18 expiry | **−2.8% avg signed, 2.8% avg absolute** (last 4 reports) |
| AAPL | None in window | — | — | — | — |
| MSFT | None in window | — | — | — | — |
| TSLA | None in window | — | — | — | — |
| SPY / QQQ | N/A (ETFs, no earnings) | — | — | — | — |

- **FACT:** Nasdaq calendar sweep of all 10 trading dates Nov 16–30 returned no watchlist name other than NVDA on Nov 17 (sanity check: Nov 20 calendar returned 22 rows, none watchlist). NVDA fiscal Q3 ending Oct 2026; last year's report Nov 19, 2025, EPS $1.24.
- **FACT — NVDA implied move:** Yahoo options chain, pulled this session. Underlying $156.14 (Nov 16 close). Nov 20 expiry, 155 strike: call mid $8.55 / put mid $6.55, straddle $15.10 → 9.67%; Nov 18 expiry straddle $13.05 → 8.36%. ATM IV ~103–117% annualized. Cross-strike straddles (152.5–160) all imply 8.4–8.6% on Nov 18 — not a single-strike artifact.
- **FACT — NVDA historical earnings-day moves** (Yahoo v8 daily chart, close-to-close, report day → next trading day; includes the following session's whole market move, not a pure earnings reaction): Aug 27, 2026 −4.57%; May 28, 2026 −1.45%; Feb 26, 2026 −4.16%; Nov 20, 2025 −0.97%. Mean signed −2.79%, mean absolute 2.79% — all four down. 1-year chart range limits this to 4 observations; earlier quarters UNVERIFIED from this pull.
- **FACT — NVDA price context:** $156.14 at Nov 16 close vs $227.98 close on Aug 27, 2026 → −31.5% since the last report.
- **UNVERIFIED:** AAPL/MSFT/TSLA next report dates — Nasdaq quote/earnings endpoint and Yahoo v7 multi-symbol quote both returned non-JSON ("Not Found") on retry; not guessed.

**NVDA leadership verification — the Nov 12 claim HOLDS (FACT, primary source):** SEC Form 8-K, filed Nov 12, 2026, accession 0001045810-26-000082, event date Nov 11, 2026 (https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm): "On November 11, 2026, the Board of Directors… accepted the resignation of Jen-Hsun Huang, as NVIDIA's President, Chief Executive Officer and member of the Board, effective immediately." Board appointed EVP & CFO Colette M. Kress interim CEO (continuing as CFO) and Harvey C. Jones as Chair of the Board. Corroborated by USA Today, NYT, Motley Fool, The Register. The Nov 12 brief was correct on substance; the brief's "that day" (Nov 12) is off by one day on timing only.

**Verdict:** NVDA's Nov 17 report is the only watchlist earnings event in the window, and the highest-stakes one of the quarter: first report under interim CEO Kress, with options pricing a ~9.7% move — roughly 3.5× the average realized move of the last four reports (2.8%, all negative) — against a stock already down 31.5% since the last print. **INFERENCE:** the market is pricing leadership uncertainty on top of the print, not just the print; a clean beat with a steady hand from Kress would compress that premium fast, while any guidance wobble or succession vacuum has room to run to the full implied move. **What would change it:** the actual Nov 17 release (read the release itself, not summaries) plus Kress's tone on the call on guidance and succession timeline; any 8-K naming a permanent CEO before the print would reprice the leadership premium first.

---

## 2. Dividend Opportunity desk

**As-of:** ~13:30 PT Nov 16. Sources: Nasdaq dividends calendar API (every date Nov 16–Dec 14, 2026, plus spot-checks Dec 18/21); Yahoo v8 chart dividend events + regular-market prices. Count standard: ~/workspace/hedge-desk-research/dividend-count-standard.md (announcement-date counting).

| Name | Next ex-div (in window?) | Amount | Yield* | Consecutive-increase count (desk standard) | Increase / cut / special |
|---|---|---|---|---|---|
| **MSFT** | **Thu Nov 19, 2026 — IN WINDOW** (pay Dec 10, 2026; announced Sep 15, 2026) | $0.98/qtr ($3.92/yr) | ~0.76% fwd | **24** — incl. Sep 15, 2026 raise to $0.98; initiated 2003, no skipped year | **Raise — Sep 15, 2026, $0.91 → $0.98 (+7.7%). This Nov 19 ex-date is the first ex at the new rate.** No cut/special. |
| **AAPL** | None in window. Last ex Nov 12, 2026 ($0.27), **paid today, Nov 16, 2026**. Next ~Feb 2027 (not declared — third-party estimate Feb 11, 2027, UNVERIFIED as a declared date). | $0.27/qtr ($1.08/yr) | ~0.31% fwd | **15** — initiation 2012 as year 1, announced increase every year 2013–2026; latest May 11, 2026, $0.26 → $0.27 (+3.8%). Note: screeners counting increase-years only report 14; complete-calendar-year conventions report 12–13. | Raise — May 2026. No cut/special. |
| **NVDA** | None in window; **not yet declared**. Past two Decembers ex'd Dec 5, 2024 / Dec 4, 2025, so a December declaration is plausible but INFERENCE, not a date. | $0.25/qtr ($1.00/yr indicated) | ~0.64% fwd; ~0.33% TTM ($0.52 paid last 4 qtrs) | **1** — 2026 is the only year in the current run with an announced increase; 2025 had no increase ($0.01 held), breaking any prior run. Defining event: May 18, 2026 announcement, $0.01 → $0.25. The Jun 2024 split rebase ($0.04 → $0.01 post-split) is not counted as an increase. | **Raise — May 18, 2026, 25× step $0.01 → $0.25/qtr** (per NVIDIA Q1 FY2027 release / 10-Q; first payment at new rate Jun 26, 2026, record Jun 4; latest ex Sep 10, 2026, paid Oct 1). No cut/special. No second raise announced — do not front-run one. |
| **SPY** | None in window; Dec distribution **not yet declared** (Nasdaq calendar Dec 18/21 shows no SPY). Pattern (Mar 20 / Jun 18 / Sep 18, 2026) points to ~Dec 18 — INFERENCE, outside window. | Last: $1.889 (Sep 18, 2026); TTM $7.58 | ~1.02% TTM | N/A — variable quarterly ETF distribution, no increase streak | None. |
| **QQQ** | None in window; Dec distribution **not yet declared** (Nasdaq calendar Dec 18/21 shows no QQQ). Pattern points to ~Dec 21 — INFERENCE, outside window. | Last: $0.751 (Sep 21, 2026); TTM $3.09 | ~0.47% TTM | N/A — variable quarterly ETF distribution, no increase streak | None. |
| **TSLA** | None — pays no dividend (FACT, Yahoo events: zero dividend events in 2-yr window; price $379.74). | — | — | N/A | None. |

\* Yields computed from Yahoo regular-market prices at pull time Nov 16, 2026 ~13:30 PT: SPY $739.95, QQQ $661.75, AAPL $352.78, MSFT $517.99, NVDA $156.14. Forward yield = indicated annual rate ÷ price; TTM where noted. All FACT, arithmetic recomputed.

**Coverage caveats (fail-closed):** Nasdaq calendar returned no rows for Dec 9, 2026 on two pulls (other dates return rows normally). Coverage for Dec 9 is UNVERIFIED, not "nothing happens" — though Yahoo history shows no watchlist name with an ex-div pattern near Dec 9. Nov 26 no-rows is explained: Thanksgiving, market closed. SPY/QQQ December dates are pattern-based INFERENCE only; neither is declared as of this pull.

**Verdict:** The only in-window event is **MSFT ex-div Thu Nov 19 ($0.98, first ex at the raised rate; own by Nov 18 close to capture it)** — a 24-year streak, 0.76% forward yield; income is trivial vs. price, the signal is the streak's durability, not the cash. **NVDA's 25× May 2026 raise ($0.01 → $0.25) is the desk's material dividend story of the year, but it is old news for this window** — no December date declared yet; watch for the declaration, and a second raise would be a new signal, not an expected one. Nothing else in the next 4 weeks: AAPL just paid today, SPY/QQQ December distributions are undeclared and fall outside the window, TSLA pays nothing. No cuts or specials anywhere on the watchlist.

---

## 3. Overnight Premium desk (IV)

**IV inputs file:** ~/workspace/hedge-desk-research/nightly/2026-11-16-iv-inputs.json, **as_of 2026-11-16T07:55:32-07:00** (pre-market pull; within the 26h guard — FRESH, not stale). All ATM IVs below are **0-DTE** (iv_expiry 2026-11-16, DTE=0). Realized window 2026-10-19 to 2026-11-13 (last 20 fully-closed closes). **All six symbols WINDOW-CONTINGENT** — the Nov 5 crash day drives >30% of 20-day realized variance in every name, so no clean IV-vs-realized verdict is issuable for any symbol today.

### IV table (morning file — pre-market 0-DTE)

| Symbol | ATM IV (0-DTE) | Realized 20d | Max 1-day var share | Window-contingent | IV rank |
|---|---|---|---|---|---|
| SPY | 17.95% | 22.83% | 54.4% | YES | UNVERIFIED |
| QQQ | 28.09% | 36.50% | 46.5% | YES | UNVERIFIED |
| AAPL | 19.59% | 28.24% | 46.3% | YES | UNVERIFIED |
| MSFT | 29.27% | 37.35% | 41.9% | YES | UNVERIFIED |
| NVDA | 62.79% | 54.48% | 36.9% | YES | UNVERIFIED |
| TSLA | 49.04% | 61.48% | 47.8% | YES | UNVERIFIED |

- **FACT:** IV < realized for SPY, QQQ, AAPL, MSFT, TSLA; IV > realized only for NVDA — but every comparison is **WINDOW-CONTINGENT**, so none of these is a clean "IV cheap/rich" verdict. The realized leg is inflated by the Nov 5 jump in all six names.
- **UNVERIFIED:** IV rank for all six — no free IV-history source available in this run; never guessed. Do not quote a rank.
- File note: `_failover` failure recorded — repo `hedge_desk.data.options_failover` unavailable (clone on a branch without it); legacy Yahoo-only options pull used.

### LIVE supplement — Yahoo v7 options pull, labeled live (as_of 2026-11-16 13:28 PT / 16:28 ET, post-close; cookie+crumb handshake, all six chains returned, zero failures)

Underlyings at pull: SPY 739.96, QQQ 661.75, AAPL 352.78, MSFT 517.99, NVDA 156.14, TSLA 379.74.

| Symbol | ATM IV 1-DTE | ATM IV 2-DTE | ATM IV 4-DTE | Term-structure read |
|---|---|---|---|---|
| SPY | 17.43% (Nov 17) | 20.27% (Nov 18) | — | Upward-sloping; 1-DTE ≈ morning 0-DTE 17.95% |
| QQQ | 28.13% (Nov 17) | 34.00% (Nov 18) | — | Upward-sloping; 1-DTE ≈ morning 0-DTE 28.09% |
| AAPL | — | 23.51% (Nov 18) | 26.72% (Nov 20) | Upward-sloping; above morning 0-DTE 19.59% |
| MSFT | — | 37.23% (Nov 18) | 40.12% (Nov 20) | Upward-sloping; above morning 0-DTE 29.27% |
| NVDA | — | **116.17%** (Nov 18) | 103.81% (Nov 20) | Earnings spike: Nov 18 expiry captures the event; 4-DTE lower as event dilutes |
| TSLA | — | 50.22% (Nov 18) | 55.61% (Nov 20) | Upward-sloping; ≈ morning 0-DTE 49.04% |

- **FACT (live, do NOT use as a vol-collapse signal):** the live 0-DTE ATM IVs printed 2.26% (SPY) to 10.30% (NVDA) — these are post-expiry artifacts. The 0-DTE contracts expired at the 16:00 ET close; post-close Yahoo IV on expired contracts is not a market print. The 1–4 DTE chains above are the usable live levels.
- **INFERENCE:** NVDA's Nov 18 (2-DTE) IV of 116.17% implies a ~8.6% two-day move (116.17% × √(2/365)) — the earnings jump is fully priced into that expiry, while today's 0-DTE print (62.79% morning) never contained the event. Arithmetic shown; the 116.17% print itself is FACT from the live chain.

**Earnings-in-window flags:** NVDA — earnings Tue Nov 17 after close (FACT, Nasdaq calendar scan in the IV-inputs file). Premium into this binary event = **AVOID** — the Nov 18 expiry's 116% IV is event vol, not a mispricing to sell into. No other watchlist name has earnings in the next 45 days (FACT, same scan).

**Verdict:** No clean IV-vs-realized call is issuable today: all six windows are WINDOW-CONTINGENT on the Nov 5 crash day, and IV rank is UNVERIFIED across the board. Live term structure is upward-sloping everywhere and broadly consistent with the morning levels — no dislocation outside NVDA's earnings spike. **What would change it:** the Nov 5 jump aging out of the 20-day window (after ~Nov 27 closes) restores clean realized comparisons; a verifiable IV-history source would restore IV-rank calls; NVDA's post-earnings IV crush (or lack of it) on Nov 18–19 reprices the event-vol read.

---

## 4. Open Quant/AI Model Lab

**Sweep window:** arXiv q-fin submissions of Fri 13 Nov 2026 (announced Mon 16 Nov) — 6 new v1 items, 0 weekend submissions (API submittedDate-range query + no-filter control agree; newest is 2611.18531, 2026-11-13T18:43:24Z). GitHub leg skipped per the run brief's ban on GitHub operations — no repo discovery, re-checks, or license verification. All scores run through the repo scorer (`hedge_desk.research_intelligence.assess_source`), never hand-scored. All abstract claims labeled UNVERIFIED unless noted (abstract-only reads).

### New candidates (3 scored, all appended to the ledger)

| # | Candidate | Venue/Date | Score | Disp. | Why |
|---|---|---|---|---|---|
| 289 | Bayer / Belomestny / Hager / Schoenmakers, "Local Stochastic Volatility Iterations" — arXiv:2611.18214v1 (q-fin.CP) | arXiv, Nov 13 2026 | 56 | **WATCH** | Fixed-point iteration calibrating the LSV leverage factor; recalibrated to S&P 500 index options on a rate-announcement day; 63- and 143-coefficient factors reproduce the fitted IV surface within a few bps (source-reported, UNVERIFIED). No code link in arXiv record. Inputs: signal 4 / data 3 / impl 2 / risk 3 / cred 4, reproducible False. Reasons: MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED, LICENSE_REVIEW_REQUIRED. Monitor code release / peer-review; sandbox the iteration on a live SPX chain vs #18/#31 if code appears. |
| 290 | Silva Prado et al, "DECODE: Decomposable Environments for COntrolled Sequential-Decision Evaluation" — arXiv:2611.18367v1 (cs.LG/q-fin.RM/stat.ML) | arXiv, Nov 13 2026 | 48 | **WATCH** (band floor) | Benchmark for controlled experiments on sequential-decision systems; planning 1→6 months lifts two gradient-boosted solvers 15–17pp of exact optimum (source-reported, UNVERIFIED). Code linked in arXiv comment (github.com/alpha-synthesis/decode-arxiv + Zenodo 10.5281/zenodo.24200270) but NOT verified — GitHub leg banned; license UNVERIFIED. Eval-design transfer to purged walk-forward methodology only; verify repo contents + license via a permitted leg before any use. |
| 291 | Chassagneux / Crépey / Loeper / Ruelland, "Well-Posedness of Semimartingale Optimal Transport with Partial Marginal Constraints for Model Calibration" — arXiv:2611.17902v1 (q-fin.MF) | arXiv, Nov 13 2026 | 41 | **ARCHIVE** | Pure theory (duality/existence/uniqueness for OT-based model calibration to finitely many option prices). No code, no data, no desk-ready method. Reopen if a calibration implementation appears. |

**Triage exclusions (no ledger rows):** 2611.18531 "Alignment by Socialization" (Lo et al.) — AI-agent alignment, q-fin.GN cross-list only; 2611.18150 "Who Should Be on the Panel?" (FinPanel LLM trading-agent personas) — LLM-agent lane, out of scope; 2611.17942 "Mapping NGFS Climate Pathways to GICS Sectors" — portfolio decarbonization, out of scope. Replacements 2408.03134v3 (incomplete-market CAPM equilibria, theory) and 2606.13880v2 (health-state neural network) — both out of scope.

**Re-checks (arXiv API id_list, 11 items):** #4 (2510.20699 v1), #9 (2608.22478 v2, 2026-10-19), #13 (2609.00332 v1), #14 (2509.11928 v3), #15 (2509.05911 v1), #20 (2609.22893 v2), #21 (2608.00616 v3), #25 (2609.13402 v4, 2026-11-10), #30 (2607.08500 v3), #31 (2511.07571 v3), #257 (2611.13616 v2, 2026-11-12) — **no version movement on any; all stay WATCH.** No TEST/INTEGRATE movement.

**Ledger:** candidates #289–#291 appended to ~/workspace/hedge-desk-research/quant-lab-ledger.md (ledger now ends at #291); Jidoka log entry added. No other file written by this desk.

**Verdict:** Thin but real window: 3 new candidates ledgered, run max 56 — nothing TEST- or INTEGRATE-ready. The one item worth the Premium desk's attention is #289 (LSV calibration to SPX options within a few bps), gated on a code release that does not yet exist.

---

## 5. Weather/War/Logistics Futures Event desk

**As-of for prices:** Yahoo v8 chart pull 13:24 PT (21:24 UTC) Nov 16. Front-month futures; intraday levels, not settlements.

### Catalyst triage

**FRESH (today / this weekend):**
- **Crude sell-off accelerates intraday, Mon Nov 16 — FACT.** Reuters: Brent $95.15 (−0.7%) / WTI $88.19 (−0.4%) at 09:19 GMT; by 17:52 GMT Brent $93.08 (−2.9%) / WTI $86.15 (−2.7%). Live Yahoo pull at 13:24 PT shows the slide continuing: WTI $85.39, Brent $92.19 (intraday, not settlement). Driver named by Reuters/IEA: recovering Gulf exports + IEA surplus call. [Sources: Reuters via ktwb.com / mymixfm.com, Nov 16; fxnews.ai, Nov 16; Yahoo Finance v8 chart, this session]
- **USDA Crop Progress, released today Mon Nov 16 (~4:00 pm ET / 1:00 pm PT) — FACT.** Corn harvest 88% complete vs 92% five-year average; soybeans 96% vs 95% average, harvest essentially wrapping up; winter wheat 53% good-to-excellent, +4 pts on the week and +8 pts on the year, 92% planted / 82% emerged, both near five-year averages. [Source: Brownfield Ag News, Nov 16, 21:09 UTC]
- **Jones Act waiver extension took effect today, Mon Nov 16, 00:00 ET — FACT.** Announced Fri Nov 13: 90-day extension (third), no gap in coverage, covered cargo must load before 11:59 pm ET Feb 14, 2027. Case-by-case vessel-availability review (since August) unchanged; covered products include gasoline, jet fuel, crude, naphtha, LNG, soy oil, fertilizers. White House: ~90M bbl of petroleum moved between US ports under the waiver since March (27M gasoline, 26M crude). Longest waiver in the law's history. [Sources: Reuters, Nov 13; Bloomberg via gCaptain, Nov 14; CBP guidance Nov 13]
- **Fresh Hormuz tanker incidents still occurring — FACT.** Reuters Nov 16: "fresh tanker incidents underscored risks to Middle East exports" even as flows recover. Tankers struck mines as late as Nov 8; at least 11 ships attacked in the first week of November (Geopolitical Intelligence Group, Nov 10–12). Houthis attacked a Saudi East-West pipeline pumping station and a Yanbu facility on Nov 13 (Reuters, via DiscoveryAlert). [Sources: Reuters Nov 16; geopoliticalrisks.global; discoveryalert.com]

**FRESH (last week — still price-relevant):**
- **IEA November Oil Market Report, Fri Nov 13 — FACT.** Global oil market returns to surplus in Q4 2026 — first since the Iran war began in late Feb. Q4 supply ~105 mb/d, ~1.7 mb/d above forecast demand (reversal from a Q4 deficit forecast a month earlier); October supply 105.4 mb/d, +2.3 mb/d m/m (+5.3 mb/d since August); Q4 supply estimate raised 3.3 mb/d. 2026 demand −2.7 mb/d to 102.3 mb/d; 2027 supply +6.6 mb/d to 108.1 mb/d. IEA caveat, verbatim substance: "downside risks to the forecast persist, as attacks on shipping undermine maritime security" and "the severe tightness in product supply, especially for diesel, remains the overriding concern." North Sea Dated peaked $136/bbl early Oct, ~$93 by mid-Nov (−32%). [Source: iea.org, Oil Market Report November 2026, Nov 13]
- **EIA Weekly Petroleum Status Report, released Thu Nov 12 (delayed from Wed Nov 11, Veterans Day) — FACT.** Week ending Nov 6: commercial crude **+4.657 Mbbl to 414.4 Mbbl** vs a Reuters-polled expected −1.1 Mbbl draw — ended five straight weekly draws; stocks ~3.1% below a year earlier (YCharts: 414.42M vs 421.17M a year ago, −1.6%). Distillate **+4.1 Mbbl to 103.3 Mbbl, ~8% below its five-year average**. SPR ~279.5 Mbbl, lowest since Oct 1982, ~39% of capacity. **Next release: Wed Nov 18, 10:30 ET (week ending Nov 13).** [Sources: EIA via global-energy-flow.com / ycharts.com / thebullticker.com, Nov 12]
- **EIA November Short-Term Energy Outlook, Tue Nov 10 — FACT.** EIA expects Brent spot ~$100/bbl in Nov–Dec (reported as $104 Nov / $99 Dec). US crude production 13.86 mb/d avg 2026. Next STEO: Dec 8. [Sources: eia.gov STEO tables; kagels-trading.com; coinpaper.com, Nov 16]
- **USDA November WASDE + Crop Production, Tue Nov 10, 12:00 ET — FACT.** Last full US harvest update of the season; next WASDE Dec 10. Corn: yield cut 1.6 bu to **179.6 bu/acre**, production −141M bu to **15.893 bn bu**, ending stocks **1.758 bn bu** (Oct: 1.849 bn; Dow Jones survey expected 1.826 bn — notably tighter than expected). Soybeans: yield raised to record **53.3 bu/acre**, production 4.574 bn bu (+12M), but exports raised 25M bu to 1.720 bn, so ending stocks **300M bu** (Oct: 315M; survey expected a rise to 336M). Wheat ending stocks 743M bu, +slightly, still −19% y/y. Livestock: 2026 beef production cut 40M lb to 24.830 bn lb; pork raised 35M lb to 27.672 bn lb. Season-average price forecasts: corn $4.60/bu (−$0.10), soybeans $12.10/bu (+$0.10). November is the last corn/soy/rice yield estimate until the January annual summary. [Sources: usda.gov WASDE-677; efeedlink.com; rfdtv.com; dtnpf.com, Nov 10–11]
- **EIA natural gas storage (prior week) — FACT.** +61 bcf w/w build to 3,862 bcf; inventories ~2% lower y/y and ~2% above the five-year average. **Next storage report: Thu Nov 19, 10:30 ET.** [Source: EIA via SP Angel, Nov 16; Topstep weekly kickoff, Nov 16]

**STALE / BACKGROUND (no new development today):**
- **Strait of Hormuz restricted, not freely open — FACT (as of Nov 9–16).** Open only to Iran-authorised vessels since Feb 28; transits ~65–90% below pre-crisis baseline by measure; Hormuz crude flows recovered to ~10.3 mb/d in Oct (Reuters/Kpler, ex-Iran) from 4.9 mb/d in Q2 2026 vs 21.6 mb/d in Q4 2025. Bypass routes carry the difference: Saudi East-West pipeline to Yanbu (~4.3 mb/d loadings in June vs ~0.75 pre-war), UAE Fujairah, Bab el-Mandeb flows up 5.4 → 8.1 mb/d. Suez recovering: 1,490 transits in Oct for $724M tolls, best revenue month since 2023, transits +32% y/y. [Sources: ryanshook.org, Nov 9; straitinsider.com; discoveryalert.com; geopoliticalrisks.global, Nov 10–12]
- **OPEC+ meeting Nov 29 — FACT (calendar).** Seven producers meet Nov 29 (with ministerial + JMMC); Nov 1 decision held September output levels. Goldman sees a "sizable" 2027 surplus building. [Sources: thebullticker.com; morningstar.com, Nov 16]
- **Abu Dhabi talks (Russia–Ukraine–US) wrapped Nov 11 — FACT.** Prisoner exchange agreed; no announcement on Black Sea shipping. [Source: pgi.klarenbach.ca, Nov 11]
- **No federal shutdown — FACT, confirmed by releases on schedule.** WASDE released Nov 10, EIA weekly Nov 12, Crop Progress today Nov 16. No "data blackout" framing applies.

### Futures levels — verified this session

| Contract (Yahoo) | Level | Context |
|---|---|---|
| WTI crude CL=F (NYM) | **$85.39/bbl** | Reuters 17:52 GMT: $86.15, −2.7% on the day; Fri Nov 13 close reported as $88.56 (nabdmal/Yahoo-sourced) but $88.92 elsewhere (Kagels) — Fri-close basis CONFLICTING, so no computed day-change vs Friday. Down through the session from $88.19 at 09:19 GMT. |
| Brent BZ=F (NYM/ICE) | **$92.19/bbl** | Reuters 17:52 GMT: $93.08, −2.9%; Fri Nov 13 close $95.84 (multiple sources agree) → intraday $92.19 is −3.8% vs that close (arithmetic on stated figures, INFERENCE). |
| Natgas NG=F (NYM) | **$3.132/MMBtu** | MineralPulse 1:57 pm EST: $3.1350, −2.94%; Morningstar 09:49 ET: $3.163, −2.1% on rising production into the first cold spell. Dec gas (NGZ26) was +8.0% last week at $3.247 before giving back. |
| Gold GC=F (CMX) | **$3,853.50/oz** | Morningstar mid-morning: Dec gold $3,862.20, −0.6%, lowest since Sept 2025; SP Angel: $3,852 vs $3,884 prior. Down ~4.9–6% on the week. Reported driver: Fed hike bets building (Dec hike "close to a done deal" per Topstep) — Desk 7's lane for the rates read. |
| Corn ZC=F (CBT) | **448.50 ¢/bu** | Post-WASDE: tighter-than-expected stocks (1.758 bn bu) but futures reaction not verified in this run — see UNVERIFIED note. |
| Soybeans ZS=F (CBT) | **1,226.75 ¢/bu** | Same caveat as corn. |
| Wheat ZW=F (CBT) | **601.75 ¢/bu** | Same caveat as corn. |

**Facts vs inference:** FACT — IEA flipped to a Q4 surplus call (Nov 13); crude fell hard today; Hormuz flows are recovering while attacks continue; distillate/diesel remains tight even as crude loosens; WASDE Nov 10 tightened corn and soybean ending stocks vs expectations; EIA crude built 4.657 Mbbl w/e Nov 6 vs an expected draw. INFERENCE — the market is pricing the IEA surplus + recovering Gulf flows as dominant over shipping-attack risk *today*; the crude-vs-diesel split (loose crude, tight products) is the operative tension: a headline crude surplus does not equal cheap delivered fuel. Gold's slide with rising hike odds is consistent with Desk 7's Dec-hike read, not a Desk 5 call. SPECULATION — none offered. UNVERIFIED — post-WASDE CBOT futures reaction (no verified settlement-to-settlement move pulled this session — levels above are intraday snapshots only); WTI's exact Fri Nov 13 close ($88.56 vs $88.92 across sources); any API weekly estimate ahead of Wed's EIA release (not pulled — private estimate, not a substitute for EIA).

**Watchlist relevance:** No direct watchlist catalyst today. Indirect: falling crude/natgas is a modest input-cost / disinflation tailwind for AAPL/MSFT/NVDA/TSLA demand backdrop; gold's slide tracks the same hike repricing Desk 7 is watching; energy-price moves do not change any watchlist earnings date. NVDA reports Tue Nov 17 after close — not a Desk 5 item.

**Verdict:** The fresh news is bearish crude, tight diesel, and a tighter-than-expected US grain balance: IEA's Nov 13 flip to a 1.7 mb/d Q4 surplus plus recovering Hormuz flows is driving Brent/WTI down ~3% today even as tanker attacks continue, while distillate sits ~8% below its five-year average and WASDE cut corn/soybean ending stocks below trade expectations. **What would change it:** Wed Nov 18 EIA weekly (a second consecutive crude build vs a draw would confirm the surplus narrative; a draw + tight distillate would revive the product-squeeze story); any Hormuz/Bab el-Mandeb incident that actually stops flows rather than just raising insurance; OPEC+ on Nov 29.

---

## 6. Box/Parity Observer

**Bottom line:** No new index-methodology doc and no new published parity-violation analysis since yesterday (Nov 15 run). Nothing material for the watchlist.

**Checked since yesterday (FACT, sources as noted):**
- **No new S&P/Nasdaq methodology doc.** The standing item remains S&P Dow Jones Indices' growth/value reclassification (announced Oct 28, 2026; effective before the open Mon Dec 21, 2026; preliminary files from Fri Dec 4): momentum dropped from growth, free-cash-flow-to-price added to value. Not new today — no update since Oct 28 (sources: TradingView/Benzinga, Oct 28; EL7.AI, Oct 28).
- **No new parity-violation analysis.** Search surfaced no Saxo Options Brief parity line for Nov 13/16, no new boxtrades.com / Cboe Box Rate index print, and no equity-index parity break. The Optionly crypto cross-venue scan (Nov 16) reports calls/puts in line on every expiry checked — crypto venues only, not watchlist-relevant.
- **Standing (unchanged):** Current SPX box rate remains **UNVERIFIED** — latest direct dated print is still Tulan Capital, Oct 20, 2026 (Dec 2026 SPX boxes ~4.3–4.4% vs ~4.1% 1-mo Treasury); the Nov 6 Alaska Wealth 1-yr ~4.90% figure is an adviser's estimate, not a tradeable print. Saxo parity checks Nov 4–11 (17.73 vs 17.74; 24.55; 19.82) all held; Nov 12–13 briefs' parity lines still UNVERIFIED. SPXO first expiry Wed Nov 18 (stops trading Tue Nov 17) remains the structural watch item.
- No parity violation is asserted; no box rate is asserted.

---

## 7. Bonds & Rates desk (Desk 7 — consolidated deliverable)

**Module status:** `rates_desk.rates_environment()` ran clean this session (mode `REAL_FRED_RATES`, as-of 2026-11-16, source `fred-public-csv-http-200`). Note: the function returns the rates block only — the 10 core indicators were pulled this session through the same module's `fred_series_rows` FRED transport, so every number below is from a pull run this session. No indicator series printed new data since the Nov 13 snapshot except the daily reads (breakevens, HY OAS) and October core CPI (not a kept indicator — reported as context because Governor Waller named it as his test). Source doc: ~/workspace/hedge-desk-research/desk7-core-indicators.md (2026-11-13 snapshot).

### 1. Rates table (FACT — FRED via rates_desk, latest obs Fri 2026-11-13)

| Series | Latest | Prior (Nov 12) | Change |
|---|---|---|---|
| Fed funds effective (DFF/EFFR) | 3.88% | 3.88% | 0.00 |
| 2Y Treasury (DGS2) | 4.88% | 4.86% | +2bp |
| 10Y Treasury (DGS10) | 5.15% | 5.10% | +5bp |
| 2s10s slope | +27bp | +24bp | +3bp, widening |
| Curve shape | UPWARD_SLOPING | — | — |
| SOFR | 3.90% | — | — |
| OBFR | 3.88% | — | — |
| **SOFR − EFFR funding spread** | **+2bp** | — | Funding calm; no stress signal |

Direction of change: yields still rising — 10Y 4.86% (Nov 6) → 4.98% (Nov 10) → 5.15% (Nov 13), +29bp in five sessions; the move is concentrated at the long end (2Y only +2bp since Nov 12), so the curve is steepening, not bear-flattening. (FACT from the module's 60-day history.)

### 2. Core-indicator table (FACT — FRED pulls this session; no new prints since Nov 13 except daily series)

| Indicator | Trigger rule | Today's read | Signal | Broker POV (discount rate / margin of safety) |
|---|---|---|---|---|
| Core PCE y/y (PCEPILFE) | HIKE if y/y > 2.5% or m/m > +0.25% | y/y **+3.121%** (130.902 ÷ 126.94 Sep-25), m/m +0.317% (Sep 2026, latest) | **HIKE** | Anchor the discount rate to the higher regime. Next print (Oct PCE, Nov 25, provisional) is the re-anchor date — nothing before then moves the decision variable. |
| Breakevens 5Y/10Y (T5YIE/T10YIE) | HIKE if > 2.75% | **2.30% / 2.24%** (Nov 13; was 2.31%/2.24% Nov 12) | **NEUTRAL** | Expectations anchored: room for 25bp, not a forced 50bp. Tripwire is a break above 2.75%. |
| Michigan expectations (MICH) | HIKE if yr-ahead > 3.5% | **4.3%** yr-ahead, Nov prelim (rel. Nov 6); FRED MICH still shows Sep 4.6% — FRED lags ~2 months, U-M read is the live one | **HIKE** | Do not average with breakevens: 4.3% vs 2.24% is a credibility gap the Fed reads as pressure to act. |
| Payrolls 3-mo avg (PAYEMS) | HIKE if > +150k; CUT if < +50k | **+137k** (Aug +186k, Sep +60k, Oct +165k; verified arithmetically this session) | **NEUTRAL** | Apply the rule as written. The +165k October print alone does not override the average. |
| Initial claims 4-wk avg (ICSA) | CUT if > 300k | **195,250** (w/e Nov 7: 200k; last 4 wks 195k/195k/191k/200k — verified this session) | **NEUTRAL** | No action. Check every Thursday; a 4-wk avg above 300k flips labor to CUT before payrolls confirm. Next print Thu Nov 19. |
| Job openings (JTSJOL) | HIKE if 3-mo change positive | **7,523k**, Sep 2026 (Jul 7,335k, Aug 7,190k) | **HIKE** | Demand has not rolled over — rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1) | HIKE if > 2.5% ann. | **Q3 +3.37% annualized** (verified arithmetically this session: 24,611.077 ÷ 24,408.011) | **HIKE** | Above-trend growth removes the "restraint is biting" objection. Backdrop, not trigger. |
| Housing starts (HOUST) | CUT if −5% over 3 mo | **1,221k**; −10.8% Jul→Sep | **CUT** | The hold case's best evidence — report it, don't bury it. It is why the call is 25bp, not 50bp. |
| HY OAS (BAMLH0A0HYM2) | CUT if > 5.00% | **3.23%** (Nov 13; was 3.20% Nov 12) | **NEUTRAL** | No credit stress; the market is neither doing the Fed's tightening work nor forcing easing. Watch a break above 5.00%. |
| FOMC vote & guidance | HIKE if dissents favor tightening | Oct 28: held 3.75–4.00%, **10–2**, Cook + Hammack dissenting for +25bp; "Inflation remains elevated." | **HIKE** | Weight the vote above any single print. Nov 18 minutes are the check on whether 10–2 understates division. |

**Tally unchanged: 5 HIKE / 1 CUT / 4 NEUTRAL.**

### 3. Market pricing vs the indicator read (FACT — direct Kalshi API pull ~13:35 PT Nov 16; FedWatch secondhand)

**Kalshi Dec-2026 (KXFEDDECISION-26DEC), direct API:** 25bp hike **$0.90** (bid/ask 0.90/0.91, prev 0.88) · more than 25bp **$0.06** (0.05/0.06, prev 0.11) · hold **$0.05** (0.04/0.05, prev 0.03) · cuts $0.01 each. Five lasts sum to **$1.03** (3-cent over-round, down from $1.05). **Total hike $0.96** (down from $1.00). 24h volume: H25 $67.5k, H26 $267.2k, H0 $385.6k — active book. (Caveat: the API's `updated_time` field reads 2026-10-27 on all five markets and is not maintained; prices demonstrably moved since Nov 13, so the pull is live — the timestamp field is UNVERIFIED, not the prices.)

**CME FedWatch, secondhand Nov 16 (no public text API):** 91–94% for 25bp, 6–9% for 50bp (BigGo, intraday Nov 16); 91.3% for 25bp (growbeansprout, as of Nov 16); futures-implied 92.9% 25bp / 7.1% 50bp (predictionmarketspicks FedWatch-method read, Nov 16 12:30 PM ET). A Nov 15 Jin10 read had 95% / 5%.

**Disagreements, named:**
1. **The 50bp tail repriced down by half** — Kalshi $0.12 (Nov 13) → $0.06 — and now sits *inside* the FedWatch range (~5–9%), closing the Nov 13 disagreement where Kalshi's tail sat below FedWatch. Markets now agree on direction (hike ~95%) and tail (~6%).
2. **Waller's trigger fired; the market faded it anyway.** Governor Waller (Nov 10, London) said he would consider 50bp if October core CPI came in "around 0.3% or higher." October core CPI printed **+0.296% m/m** (CPILFESL 339.900 vs 338.896, FRED pull this session) — at the threshold. Yet the >25bp price fell from $0.11 to $0.06 after that print. (INFERENCE: the market reads "consider" as not a commitment, or weighs other officials and the coming minutes more heavily. The indicator set cannot adjudicate size — no rule distinguishes 25bp from 50bp.)
3. **Indicators vs markets on size, unchanged:** the indicator set votes direction (hike), not size. The tail is a market judgment, not a data judgment.

### 4. Verdict — thesis / evidence / what would change it

**Thesis (INFERENCE):** 25bp hike on Dec 9. Unchanged from Nov 13. Direction is high-confidence — indicators (5/1/4) and markets (~95% hike) agree; size is the open question, with the 50bp tail now ~6% on both venues.

**Evidence (FACT):** Core PCE 3.121% y/y vs a 2% target; Michigan 4.3% vs breakevens 2.24% (credibility gap); labor intact on every kept read (payrolls +137k avg, claims 195,250, openings 7,523k); growth +3.37%; a 10–2 vote with two hawkish dissents; Kalshi total hike $0.96, FedWatch ~91–95% for 25bp. Counter-evidence carried in full: housing starts −10.8% over three months (the CUT vote) and breakevens anchored at 2.30%/2.24% (no credibility crisis forcing 50bp).

**What would change it:**
- October core PCE (Nov 25, provisional): m/m at or below +0.15% with a downward September revision — the target variable softening.
- Initial claims 4-week average above 300k — the fast labor signal turning.
- November 18 minutes, or a named speaker arguing for a hold — guidance shifting against the hike. (Also on the calendar: Fed Chair Kevin Warsh speaks later today, per press; November jobs Dec 4; November CPI Dec 10, the day *after* the decision, so it cannot change December.)

### 5. Graham lens (arithmetic from FACTs above)

10Y 4.98% (Nov 10) → **5.15%** (Nov 13). At assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) falls 50.51x → **46.51x, −7.9%**; from 4.86% (Nov 6, 53.76x) the fall is **−13.5%**. Duration ≈ 8 puts the +17bp move since Nov 10 at about **−1.36%** on a 10-year position (approximation; ignores convexity). The margin of safety is thinner at the same prices: any intrinsic-value estimate carried at the old 4.86% anchor overstates value by ~13% on this sensitivity. Re-anchor to 5.15%. Earnings-yield vs bond-yield spread: **UNVERIFIED** — bond side verified (5.15%); earnings side unverified from any primary source this session. No live spread is asserted. The defensive read: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price — a wider required discount, not a chase for yield.

**Desk status: COMPLETE. No desk failure. No new data print moves the call; the only moves since Nov 13 are the 10Y (+17bp), the steepening 2s10s (24→27bp), and the halving of the 50bp tail.**

---

## Sources (session pulls)

- Nasdaq earnings calendar API; Yahoo Finance v7 options / v8 chart (cookie+crumb); SEC EDGAR (NVDA 8-K, accession 0001045810-26-000082).
- Nasdaq dividends calendar API; Yahoo dividend events.
- ~/workspace/hedge-desk-research/nightly/2026-11-16-iv-inputs.json (as_of 2026-11-16T07:55:32-07:00); live Yahoo options pull 13:28 PT.
- arXiv q-fin API (submittedDate-range + id_list re-checks); repo scorer `hedge_desk.research_intelligence.assess_source`.
- Reuters (Nov 16 crude/Hormuz); IEA Oil Market Report Nov 2026 (Nov 13); EIA Weekly Petroleum Status Report (Nov 12) + STEO (Nov 10); USDA WASDE-677 + Crop Progress (Nov 10 / Nov 16); Brownfield Ag News (Nov 16).
- FRED via `rates_desk.rates_environment()` + `fred_series_rows` (REAL_FRED_RATES, 2026-11-16); Kalshi API direct (KXFEDDECISION-26DEC, ~13:35 PT); CME FedWatch secondhand (BigGo, growbeansprout, predictionmarketspicks, Jin10).
- Desk standards: ~/workspace/hedge-desk-research/desk7-core-indicators.md; ~/workspace/hedge-desk-research/dividend-count-standard.md; ~/workspace/hedge-desk-research/quant-lab-ledger.md (now ends at #291).

## Desk status

All seven desks reported. No desk FAILED. No retry required. One coverage caveat: Nasdaq dividends calendar returned no rows for Dec 9, 2026 (UNVERIFIED, not "nothing happens"); AAPL/MSFT/TSLA next report dates UNVERIFIED (endpoint failures, not guessed); IV rank UNVERIFIED for all six names; SPX box rate UNVERIFIED (latest dated print Oct 20).
