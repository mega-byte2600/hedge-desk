# Hedge-Desk Daily Research — Wed 2026-11-04

**Run:** 13:30 PT, Wed 2026-11-04. **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Profile:** research + input only — no git push/pull, no PRs, no code changes, no GitHub operations.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; no risk-seeking framing.
**Evidence labels:** FACT / INFERENCE / SPECULATION / UNVERIFIED per the CFA evidence standard.
**Market-data rule:** Yahoo Finance first, Nasdaq second, then fallbacks; Yahoo v7 options/quote via cookie+crumb handshake, v8 chart via browser User-Agent alone.
**Hard boundaries honored:** paper-only; no Risk of Ruin generated or estimated; no trade authorization proposed; no licensed material reproduced; unverifiable numbers marked UNVERIFIED, never guessed.

**All seven desks reported this run. No desk FAILED; none silently dropped.**

## Decision-relevant items (synthesis, not stapling)

1. **NVDA Nov 17 after close is the window's only binary earnings event — and its vol is already earnings-contaminated.** Consensus $2.49 (Nasdaq, Zacks). Options price a ±7–9% move depending on method (see §1); last print moved +8.7%. Premium desk: the 37-DTE NVDA chain (45.08% IV) spans Nov 17 — do not read it as a clean vol level. Premium into a binary event = avoid.
2. **Crude sold off ~7–9% into bullish inventory data — a war-premium unwind, not a glut signal.** EIA's on-schedule report today (10:30 ET) showed crude, gasoline, and distillate all drawing, distillates at a 23-year low — yet Brent broke below $100 and WTI traded ~$88.50–91.80 late. Driver per Reuters coverage: midterm results plus Iran-de-escalation hopes. The "Hormuz reopens within 2 days" claim is single-source and UNVERIFIED; Gulf exports still depressed (17.1M bpd in Oct vs 18.9M in Sep, Vortexa).
3. **Rates still pressure growth multiples: 10Y 4.95%, 2Y 4.61%, 2s10s +34 bp (FRED, as of Nov 3).** Curve still upward-sloping but ~7 bp flatter than 60 days ago; both ends retraced from window highs (10Y peaked 5.31% Oct 5). Funding calm: SOFR–EFFR +9 bp. Directional read: elevated long rates = higher discount rates = margin-of-safety discipline on long-duration growth exposure.
4. **Two dividend events in the window, one of them the raise.** MSFT ex Nov 19 at $0.98/qtr — the Sep 15-announced increase, 24th consecutive annual raise under the desk standard; AAPL ex Nov 12 at $0.27, unchanged. No cuts, no specials announced on the watchlist.
5. **Do not over-trust front-week index vol prints today.** SPY's 20-day realized window is WINDOW-CONTINGENT (one day = 32.5% of variance), so any SPY IV-vs-realized verdict is WINDOW-CONTINGENT, not clean. Front-week SPY/QQQ chains show wide same-strike call/put IV gaps on post-close marks (likely stale quotes, not arbitrage). IV rank is UNVERIFIED for all six names — no rank flag is issued today.

**Cross-desk resolutions:** NVDA Nov 17 confirmed three ways (company release, Nasdaq calendar, Zacks) — stale third-party listings of Nov 18/25 are superseded by the company release. AAPL $0.27 dividend corroborated by both the 8-K and the Nasdaq calendar. The "November WASDE postponed to Nov 14 due to shutdown" aggregator claim is contradicted by USDA's own calendar (Nov 10, 12:00 ET), by the Oct 9 WASDE itself, and by today's on-schedule EIA release — the shutdown/postponement framing is NOT adopted (standing government-data rule).

---

## 1. Earnings Event desk

**Window:** through Nov 18, 2026. **As-of:** ~13:45 PT Nov 4.

| Symbol | Report date | Timing | Consensus EPS | Implied expected move | Last earnings-day reaction (verified) | Historical avg move |
|---|---|---|---|---|---|---|
| NVDA | Tue Nov 17, 2026 | After close — results ~1:20 p.m. PT, call 2:00 p.m. PT / 5:00 p.m. ET | $2.49 | ±9.0% (own Nov 20 straddle); ±7.3% (vendor stripped method, cited not recomputed) | +8.7% (Aug 27, 2026) | ±8.4% 10-yr avg — third-party, NOT independently recomputed |
| AAPL | Reported Mon Nov 2, 2026 (after close) | — | — | — | −1.9% on Nov 3 (first session after print); +5.3% on Nov 4 (price fact only; driver not attributed) | UNVERIFIED (not computed this run) |
| MSFT | None in window; next est. late Jan 2027, unconfirmed | — | — | — | −0.2% on Oct 29 (after Oct 28 print) | UNVERIFIED |
| TSLA | None in window; next est. late Jan 2027, unconfirmed | — | — | — | −3.1% on Oct 22 (after Oct 21 print) | UNVERIFIED |
| SPY | None — ETF, no earnings event | — | — | — | — | — |
| QQQ | None — ETF, no earnings event | — | — | — | — | — |

**NVDA — the window's only event (FACT).** Date/timing verified independently of the Nov 3 IV-inputs file: (1) NVIDIA's own Oct 28, 2026 release — call Tue Nov 17, 2 p.m. PT / 5 p.m. ET, fiscal Q3 2027 ended Oct 25, 2026, CFO written commentary ~1:20 p.m. PT; (2) Nasdaq earnings calendar API pull Nov 4 — NVDA on 2026-11-17, "time-after-hours," EPS forecast $2.49, no other watchlist symbol on any date Nov 4–18; (3) Zacks calendar — Nov 17, confirmed, consensus $2.49 (+91.5% YoY). MarketBeat/TipRanks listings of Nov 18 or Nov 25 are stale/estimated; the company release governs.

**Implied move — method note (FACT computation + INFERENCE caveat):** Yahoo v7 options chain pulled Nov 4 (cookie+crumb), NVDA $200.13. Nov 20, 2026 expiry (first expiry after the print) ATM straddle: $200 call $9.30 + $200 put $8.75 = $18.05 → ±9.0% (mid-price ±9.1%). This straddle spans 16 calendar days, not the earnings day alone, so it overstates the pure earnings-day move. Vendor EarningsWatcher quotes ±7.3% on a stripped method — cited, not independently recomputed; the 7.3% vs 9.0% gap is method, not contradiction.

**History (FACT, own computation from Yahoo v8 closes):** last report Aug 26, 2026 AMC → Aug 27 close $227.98 vs Aug 26 $209.66 = +8.7%, against a ±5.9% move options had priced (third-party figure). The 10-yr average ±8.4% is third-party (EarningsWatcher) and UNVERIFIED by this desk.

**AAPL — reported this week, still market-moving (FACT, from the release itself).** Apple's own Nov 2, 2026 Form 8-K (Exhibit 99.1), not a summary: fiscal Q4 2026 (ended Sep 26, 2026) revenue $114.5B, +12% YoY; gross margin 47.9%, including ~1 point from tariff refunds; diluted EPS $2.10, +14% YoY, including $0.05 from tariff refunds; fiscal 2026 revenue a record $479B; dividend $0.27 declared, payable Nov 16 to holders of record Nov 12. First-session reaction (Yahoo v8 closes): Nov 3 close $331.90 vs Nov 2 $338.32 = −1.9%; Nov 4 close $349.51 (+5.3% on the day). December-quarter gross-margin guidance of 45–46% is INFERENCE-grade (call coverage, not in the release itself; the release contains no guidance). Next report est. Jan 28, 2027 (third-party, unconfirmed) — outside the window.

**MSFT (FACT):** reported fiscal Q1 2027 Oct 28, 2026 after close (company announcement Oct 7, 2026). Reaction: Oct 29 $530.14 vs Oct 28 $531.01 = −0.2%. Next est. late Jan 2027 (Jan 26–28 across vendors, unconfirmed).

**TSLA (FACT):** reported Q3 2026 Oct 21, 2026 after close (Tesla IR events page). Reaction: Oct 22 $374.58 vs Oct 21 $386.47 = −3.1%. Next est. late Jan 2027 (Jan 27 across vendors, unconfirmed).

**What would change the verdict:** an NVIDIA pre-announcement or date change, or a sharp repricing of the Nov 20 straddle before Nov 17.

**Sources:** NVIDIA release https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx ; Nasdaq earnings calendar API https://api.nasdaq.com/api/calendar/earnings?date=2026-11-17 (queried each date Nov 4–18); Zacks NVDA calendar https://www.zacks.com/stock/research/NVDA/earnings-calendar ; Yahoo v7 options + v8 chart closes Nov 4; Apple Q4 2026 8-K https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/5061d9d7-3617-4eac-b3b1-a95c6fd839f1.pdf and Apple Newsroom https://www.apple.com/sg/newsroom/2026/11/apple-reports-fourth-quarter-results/ ; Microsoft release-date announcement https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; Tesla IR https://ir.tesla.com/ ; third-party context (labeled, not recomputed): https://earnings-watcher.com/wiki/nvda-implied-move , https://www.tipranks.com/stocks/msft/earnings , https://www.zacks.com/stock/research/TSLA/earnings-calendar

---

## 2. Dividend Opportunity desk

**Window:** through Dec 2, 2026. **As-of:** ~13:40 PT Nov 4. Count standard: ~/workspace/hedge-desk-research/dividend-count-standard.md.

| Symbol | Ex-date | Amount | Record | Pay date | Declared | Change vs prior | Label |
|---|---|---|---|---|---|---|---|
| AAPL | Thu Nov 12, 2026 | $0.27/qtr | Nov 12, 2026 | Mon Nov 16, 2026 | Nov 2, 2026 | None — unchanged from Aug 2026 ($0.27) | FACT |
| MSFT | Thu Nov 19, 2026 | $0.98/qtr | Nov 19, 2026 | Thu Dec 10, 2026 | Sep 15, 2026 | INCREASE — from $0.91 (+$0.07, +7.7%); first payment at the new rate | FACT |

**MSFT — the window's only increase (FACT, issuer release + Nasdaq calendar).** Board declared $0.98/qtr Sep 15, 2026, payable Dec 10 to holders of record Nov 19; ex-date Nov 19. Per the standardized count, this is the **24th consecutive annual increase** (count increments on announcement date; specials never count). No new raise announced since Sep 15. Quirk flagged: Nasdaq's "indicated annual dividend" field for MSFT still shows $3.64 (pre-raise $0.91 × 4 basis) — the $0.98 quarterly rate is authoritative; annualized at the new rate is $3.92.

**AAPL — steady, no increase (FACT).** $0.27 declared Nov 2, 2026 (alongside fiscal Q4 results), ex Nov 12, pay Nov 16 — identical to the Aug 10, 2026 payment. No increase, cut, or special announced. AAPL's last raise was to $0.27 earlier in 2026 (Feb 2026 ex-date was $0.26; May 2026 onward $0.27 per Yahoo events). No AAPL streak count stated — not verified against the issuer under the desk standard.

**NVDA — nothing declared in window (FACT).** Last ex-date Sep 10, 2026, $0.25, paid Oct 1, 2026. Next dividend not yet declared as of Nov 4. On past cadence (Dec ex-dates Dec 5, 2024 and Dec 4, 2025) the next ex-date would fall in early December — just outside this window — but that is pattern, not a declaration (INFERENCE, do not treat as dated). The May 2026 step-up ($0.01 → $0.25) is old news, already paid twice. No NVDA streak count stated: third-party screeners conflict (1 yr vs 3 yrs), none verified against the issuer (UNVERIFIED — count withheld, not guessed).

**SPY — next ex-date outside window.** Last ex Sep 18, 2026 ($1.889) (FACT, Yahoo events). Next distribution ex-date estimated Dec 18, 2026, pay Jan 29, 2027 (ESTIMATE per Wall Street Horizon ETF calendar / TipRanks — not yet declared, outside the window in any case).

**QQQ — next ex-date outside window.** Last ex Sep 21, 2026 ($0.7514), paid Oct 8, 2026 (FACT). Next ex-date projected Dec 21, 2026 (PROJECTION from cadence, AlgovestIQ/TipRanks, not an announcement). Note, not a verdict: the Sep distribution ($0.7514) was 7.6% below the prior quarter's $0.8135. Whether that is a cut or one-off ETF distribution variability is UNVERIFIED — it is not a declared cut, and QQQ distributions vary quarter to quarter by construction. No cut is flagged.

**TSLA — no dividend, nothing to flag (FACT).** Tesla has never paid a common-stock dividend and none is declared.

**Increases / cuts / specials summary:** Increases: 1 (MSFT). Cuts: none announced. Specials: none announced.

**What would change these verdicts:** an NVDA declaration (typically alongside quarterly results) could add an early-December ex-date; SPY/QQQ December declarations, when issued, replace current estimates/projections; any new AAPL/MSFT board action supersedes the declared figures (none pending as of Nov 4).

**Sources:** Nasdaq dividends calendar API https://api.nasdaq.com/api/calendar/dividends?date=2026-11-19 and ?date=2026-11-12 (queried Nov 4); Yahoo v8 chart dividend events (query1.finance.yahoo.com/v8/finance/chart/{symbol}?events=div, Nov 4); Microsoft issuer release https://news.microsoft.com/source/2026/09/15/microsoft-announces-quarterly-dividend-increase-7/ ; AAPL corroboration https://www.zacks.com/stock/research/AAPL/dividend-history , https://ycharts.com/companies/AAPL/dividend , https://stockanalysis.com/stocks/aapl/dividend/ ; MSFT https://stockanalysis.com/stocks/msft/dividend/ ; NVDA https://www.heygotrade.com/en/market-outlook/nvidia-dividend-2/ , https://www.lighthorse.io/tickers/nvda/dividends ; SPY https://www.wallstreethorizon.com/spy-dividend-calendar , https://www.tipranks.com/etf/spy/dividends ; QQQ https://www.algovestiq.com/etf/qqq/dividends , https://www.tipranks.com/etf/qqq/dividends ; TSLA https://www.zacks.com/stock/research/TSLA/dividend-history ; count standard ~/workspace/hedge-desk-research/dividend-count-standard.md

---

## 3. Overnight Premium desk (IV)

**IV-inputs file:** ~/workspace/hedge-desk-research/nightly/2026-11-03-iv-inputs.json, `as_of` **2026-11-03T14:54:06−07:00** (Nov 3 post-close). **Guard status: WITHIN the 26h freshness guard** (~22.6h old at this run's 13:30 PT start) — usable, but it is **YESTERDAY's data, labeled STALE below; never read as today's.** Live supplement pulled today via Yahoo v7 options chain (cookie+crumb handshake, UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`), ~13:27–13:35 PT Nov 4 (post-close marks, 16:27+ ET).

**Method note (FACT):** today's Nov 4 expiries expired at 16:00 ET before this pull, so the default Yahoo chain for every name returns solver residuals on dead contracts (e.g. SPY Nov 4 put IV printed as 0.00001) — failed closed and excluded, exactly as the Nov 3 pull did for SPY/QQQ. All live levels below use the **next live expiry** onward. ATM IV = mean of nearest-strike call and put IV at the closing spot. Expected move ≈ ATM IV × √(DTE/365). Source: https://query1.finance.yahoo.com/v7/finance/options/{SYM}.

### Yesterday's post-close snapshot (STALE — as of Nov 3 post-close, from the iv-inputs file)

| Symbol | ATM IV (Nov 3 close) | Expiry / DTE then | Realized 20d | Max single-day var. share | Window-contingent? |
|---|---|---|---|---|---|
| SPY | NULL (failed closed, expiry expired) | — | 11.35% | **0.3246** | **YES** |
| QQQ | NULL (failed closed, expiry expired) | — | 22.87% | 0.2865 | No |
| AAPL | 27.31% | Nov 4, 1 DTE | 16.60% | 0.1726 | No |
| MSFT | 31.12% | Nov 4, 1 DTE | 22.33% | 0.2260 | No |
| NVDA | 40.45% | Nov 4, 1 DTE | 31.44% | 0.2361 | No |
| TSLA | 48.16% | Nov 4, 1 DTE | 37.02% | 0.2589 | No |

**SPY WINDOW-CONTINGENT (FACT, from the file):** a single day drives 32.5% of SPY's 20-day realized variance (window Oct 6 – Nov 2). Any IV-vs-realized verdict for SPY built on this window is **WINDOW-CONTINGENT, not clean** — the verdict flips if that one day rolls out. No other watchlist name breaches the 30% threshold.

### Live term structure — Nov 4 close (FACT, Yahoo options chain)

Spots at pull: SPY 766.82, QQQ 691.95, AAPL 349.51, MSFT 555.80, NVDA 200.13, TSLA 385.19.

| Symbol | Nov 5 (1 DTE) | Nov 6 (2 DTE) | Nov 9 (5 DTE) | Nov 11 (7 DTE) | Dec 11 (37 DTE) | Expected move, nearest live expiry |
|---|---|---|---|---|---|---|
| SPY | 11.12% | 12.47% | 11.71% | — | — | ~0.6% (1 DTE) |
| QQQ | 19.87% | 23.18% | 20.68% | — | — | ~1.0% (1 DTE) |
| AAPL | — | 25.45% | 22.76% | 26.61% | — | ~1.9% (2 DTE) |
| MSFT | — | 28.95% | 25.45% | 29.50% | 27.56% | ~2.1% (2 DTE) |
| NVDA | — | 44.57% | 39.09% | 42.32% | 45.08% | ~3.3% (2 DTE) |
| TSLA | — | 46.86% | 40.87% | 43.75% | 43.46% | ~3.5% (2 DTE) |

("—" = no weekly expiry that date for that name, or not pulled; not a zero.)

**Desk notes:**

1. **Term structure essentially flat-to-mildly-upward across the board (FACT from the table; INFERENCE: no front-week vol event priced beyond the ordinary weekly pattern).** No name shows a sharp front-week IV spike vs. its own 5–7 DTE level. What would change this: a front-expiry ATM IV jumping >5 points above the 7 DTE level on the next pull.
2. **Single-name IV sits well above index IV (FACT):** NVDA ~39–45% and TSLA ~41–47% vs. SPY ~11–12% and QQQ ~20–23%. Against yesterday's STALE realized-20d baselines, NVDA's live IV (~40–45%) runs above its 31.4% realized and TSLA's (~41–47%) above its 37.0% realized — consistent with a standing single-name premium, not a new spike (INFERENCE; realized baselines are yesterday's, so treat the gap as indicative only).
3. **NVDA earnings inside the window — premium into a binary event = avoid (FACT: next earnings 2026-11-17 per the Nov 3 iv-inputs file, independently confirmed in §1).** The Dec 11 (37 DTE) NVDA chain at 45.08% spans the Nov 17 earnings date; its elevation vs. the Nov 6–11 chains is consistent with earnings premium already embedded (INFERENCE). Do not read NVDA's 37 DTE IV as a clean vol level — it is an earnings-contaminated quote. What would change this: the earnings desk confirming a different date, or the event passing.
4. **IV sanity flag — wide same-strike call/put IV gaps in front-week index chains (FACT, observed in the pull):** SPY Nov 5 call IV 13.6% vs. put IV 8.7% at the same 765 strike; QQQ Nov 5 call 22.6% vs. put 17.2% at 690. Put-call parity says same-strike, same-expiry IVs should nearly match; a gap this wide on post-close marks most likely reflects stale/wide closing quotes rather than a real arbitrage (INFERENCE). Per the desk standard the math outranks the model: do not trade off these prints — re-check on live intraday marks before trusting any front-week index IV to better than ±3 points. What would change this: a live-market pull showing the gap closed.
5. **IV rank: UNVERIFIED for all six names.** No free IV-history source was available in this run to compute a percentile rank, and none is guessed. Yesterday's STALE ATM levels vs. today's live next-expiry levels show no overnight regime shift by eyeball (INFERENCE, not a rank), but that is not a substitute for a rank. What would change this: a verifiable IV-history feed (e.g. a 52-week IV series) becoming available.
6. **No elevated-IV-rank flag is issued today** — with rank UNVERIFIED, the desk flags only the NVDA earnings-contaminated chain (note 3) and the SPY WINDOW-CONTINGENT verdict (above), not a rank call.

**Sources:** Yahoo Finance v7 options chains, pulled 2026-11-04 ~13:27–13:35 PT (https://query1.finance.yahoo.com/v7/finance/options/{SPY,QQQ,AAPL,MSFT,NVDA,TSLA}); ~/workspace/hedge-desk-research/nightly/2026-11-03-iv-inputs.json (as_of 2026-11-03T14:54:06−07:00). No number in this section is estimated or carried from memory.

---

## 4. Open Quant/AI Model Lab

**Headline: no brand-new candidate, but one reopened item — #9 comes out of ARCHIVE.** No TEST, no INTEGRATE movement. GitHub leg skipped per the run brief's ban on GitHub operations (same as the Nov 1–3 runs), so no new-repo discovery, no repo re-checks, and no repo contents/license verification this run.

| # | Candidate | Venue / date | Scorer score | Disposition + reason |
|---|---|---|---|---|
| 9 (reopened) | Buchegger & Gonon — "Arbitrage-Aware Probabilistic Multi-Step Forecasting of Implied Volatility Surfaces" (latent-diffusion joint IVS + return trajectories) | arXiv:2608.22478v2, ICAIF'26 proceedings, DOI 10.1145/3858063.3858845 | 56 | **WATCH (ARCHIVE → WATCH)** — code link now present in the paper itself, the exact trigger the 2026-10-10 archive decision named; peer-reviewed proceedings + persistence-beating multi-step design lift it back into the WATCH band, but repo contents, license, and licensed-data replication are all still unverified, so it cannot reach TEST |

Scorer result (run via `hedge_desk.research_intelligence.assess_source` from ~/workspace/github/hedge-desk, read-only — no repo writes): score **56**, decision **WATCH**, reasons MONITOR_FOR_EVIDENCE, REPRODUCIBILITY_NOT_ESTABLISHED, LICENSE_REVIEW_REQUIRED. Inputs: PEER_REVIEWED, signal 4 / data 2 / implementation 3 / risk 3 / credibility 4, reproducible False.

**FACT** (abstract + introduction + methodology read at source, 2026-11-04 ~13:30–14:00 PT): the ICAIF'26 version states "Code is available on GitHub" linking github.com/DomBBB/implied-volatility-trajectories/tree/main/ICAIF26, and provides a transparent dataset-construction protocol from OptionMetrics IvyDB US via WRDS (licensed data, not open) plus a pretrained smoothing-operator checkpoint link. The model is a two-stage conditional latent diffusion: an arbitrage-regularized autoencoder compresses daily SPX surfaces, and diffusion generates joint 30-step surface + return trajectories in one non-autoregressive pass.

**UNVERIFIED** (source-reported, full paper not read beyond abstract/intro/methodology): predictive mean beats persistence from approximately weekly horizons onward, while persistence remains superior at 1 day; generated trajectories improve probabilistic scores over persistence at medium/longer horizons with negligible detected static-arbitrage violations; main limitation is underdispersion (predictive intervals too narrow).

**INFERENCE:** the transferable item is the persistence-baseline discipline (a model that merely copies today's surface can look good without learning anything) plus the arb-regularized latent representation as a scenario generator for the premium desk — not a one-day point forecaster, and not a tradable signal.

**What would change the verdict:** verification of the repo's contents + license via a permitted leg (→ sandbox the arb-check/autoencoder pieces on a live SPY chain against #18/#31); a licensed-data replication or an open-data port (→ TEST). What would close it again: repo contents failing to match the paper, or a non-permissive license.

**Source:** https://arxiv.org/html/2608.22478v2

**Coverage gaps, stated plainly:** The Nov 2–3 arXiv announcement window is still not directly verifiable via search-indexed results (same leg gap as Nov 3). One 2611 ID surfaced (2611.03592, TSFM uncertainty calibration) — general forecasting methodology, marginal desk relevance, not scored as a candidate. Search legs covered vol-surface, earnings/dividend, and purged walk-forward angles with no other new primary-source items. Mir/Shrestha "Quantifying Backtest Overfitting from Information Leakage" (July 2026 preprint) is again NOT ledgered: still claimed only by a secondary AICopse roundup, no arXiv ID or primary source located — fail-closed as UNVERIFIED, not scored (same as Nov 1). Triage exclusions (no ledger rows): #31 Jin/Agarwal v3 PDF internal date Oct 26, 2026 — a PDF date is not an arXiv version record, so no version movement claimed; #157 Bastola re-surfaced, already ledgered; Turbine/Nvestiq/AICopse backtest-overfitting blogs (secondary explainers of published AFML work, no new release); analyst-estimate wires and earnings-week vendor pieces (broker commentary, not research releases).

**Ledger confirmation:** row #9 in ~/workspace/hedge-desk-research/quant-lab-ledger.md updated in place (disposition ARCHIVE → WATCH, score 57 → 56, 2026-11-04 reopen note with scorer inputs), plus a 2026-11-04 run note in the Kaizen log. No new row was created because #9 is a reopen, not a new candidate — no candidate lives only in a daily file.

**Bottom line for synthesis:** the premium desk's IV-surface forecasting lane regains a peer-reviewed, code-linked candidate (#9) whose honest headline — beats persistence only beyond ~weekly horizons, still loses at 1 day, intervals too narrow — is itself a useful guard against overclaiming surface forecasts.

---

## 5. Weather/War/Logistics Futures Event desk (catalysts)

**As-of:** 13:30 PT, Wed 2026-11-04. Futures quotes pulled 13:18 PT via Yahoo v8 chart (UA-only, working). Facts kept separate from inference throughout.

| # | Catalyst | Fresh? | What happened | Label / source | What would change the verdict |
|---|---|---|---|---|---|
| 1 | **EIA Weekly Petroleum Status Report — week ending Oct 30, released today 10:30 ET** | YES — today | Crude −865k bbl to 409.8M bbl (5th straight weekly draw); gasoline −222k to 209.0M; distillates −3.565M to 99.3M — lowest since May 2003, ~13% below 5-yr avg; Cushing +280k; refinery utilization 94.5% (+1.7pp), runs +199k bpd to 16.7M bpd; U.S. crude production record 14.003M bpd; SPR −399k to 282.2M; total commercial petroleum −8.2M bbl; 4-wk products supplied 21.2M bpd, +4.2% YoY | FACT (EIA release as reported by Reuters via Morningstar/BOE Report, 2026-11-04) — https://www.morningstar.com/news/dow-jones/2026110410540/us-crude-oil-stockpiles-post-fifth-straight-weekly-drop ; https://boereport.com/2026/11/04/us-crude-stocks-gasoline-and-distillate-inventories-fall-eia-2/ . Note: eia.gov weekly page returned HTTP 200 at pull time but headline figures were not extracted from it directly, so figures are carried as EIA-via-Reuters, not EIA-page-verified | A correction in next week's EIA release or a revised Reuters poll consensus |
| 2 | **API vs EIA divergence (Tue → Wed)** | YES — today | API (Tue): crude −5.267M bbl, gasoline +1.427M, distillates −270k — far larger crude draw than EIA's −865k; gasoline sign flipped (API build vs EIA draw) | FACT (API via market sources, Reuters) — same BOE/Morningstar links; https://investinglive.com/news/eia-weekly-us-crude-oil-inventories-k-vs-877k-expected/ | Nothing — divergence is observed; it cautions against trading on API alone |
| 3 | **Crude price collapse on de-escalation hopes — midterms + Iran talks** | YES — today | Brent whipsawed: +0.7% to $104.36 early (07:30 GMT), then broke below $100 intraday (low ~$98.67) and traded ~$94–95 late; WTI ~$88.5–91.8 late. Yahoo front-month at 13:18 PT: WTI (CL=F) $88.56, Brent (BZ=F) $95.07, vs prior closes $96.09 / $103.60 — i.e. the selloff, not the morning rally, is the day's story so far | FACT for price levels at stated times (Reuters/BusinessDay/Invezz + Yahoo pull) — https://www.businessday.co.za/markets/2026-11-04-oil-prices-plunge-as-trumps-midterm-defeat-raises-hopes-of-peace/ ; https://invezz.com/news/2026/11/04/brent-crude-price-falls-below-100-iran-deal-hopes-eia-draw/ ; https://ktwb.com/2026/11/03/oil-edges-down-as-investors-await-us-midterm-election-results/ . Late-day levels differ by timestamp (16:02 GMT $98.90 vs 16:58 GMT $94.29); do not quote a single settlement — settlement UNVERIFIED at desk time | NYMEX/ICE settlement prints; any signed deal or renewed strike |
| 4 | **U.S.–Iran war / Hormuz: diplomacy vs "far from a deal"** | YES — fresh statements Tue–Wed | Democrats swept Congress in Tue midterms (both houses, per Reuters); Trump told the FT Tue he has "no immediate plans" to strike Iran; Qatar mediating; U.S. carried out "defensive" strikes on Qeshm Island Tue; senior Iranian official told Reuters Tue the sides remain "far from a deal"; Iran reportedly signalled Hormuz could reopen within 2 days if sanctions/frozen-asset demands are met (single-source report, unconfirmed) | FACT for midterms outcome, Trump quote, Qatar mediation, Qeshm strikes, "far from a deal" (Reuters) — BusinessDay/KTWB links above. UNVERIFIED for the 2-day Hormuz-reopening claim (Invezz only, no second source) | A signed agreement, Hormuz transit data (PortWatch/Vortexa), or renewed strikes |
| 5 | **Gulf crude exports still depressed** | Fresh data point (Oct totals) | Gulf crude/condensate/refined exports ex-LPG averaged 17.1M bpd in Oct vs 18.9M in Sep, ~three-quarters of pre-war levels (Vortexa ship-tracking via BusinessDay) | FACT (Vortexa via BusinessDay, link above) | November Vortexa/PortWatch transit data |
| 6 | **Black Sea grain corridor proposals** | Fresh (Sat Nov 1, still live Wed) | Sec. Rubio (G20, Atlanta, Sat): India and Türkiye have proposed ideas to move grain through the Black Sea; several countries considering guarantor/facilitator roles; Hormuz passage "more challenging" with limited allied cooperation. No agreement signed — proposals only | FACT (Rubio statements) — https://shippingtelegraph.com/shipping-reports/black-sea-grain-shipments-several-countries-consider-roles-as-guarantors/ ; https://www.thehindubusinessline.com/news/india-and-turkey-propose-plans-to-move-grain-shipments-through-black-sea-says-rubio/article71651939.ece/ | A signed corridor/guarantor agreement or a vessel transit under it |
| 7 | **BIMCO dry-bulk outlook: Hormuz closure = largest uncertainty** | Context, Oct 30 (not new today) | Effective Hormuz closure remains top uncertainty; ~4% of dry-bulk demand sails via Hormuz; Black Sea attacks add risk; "SoH closed" scenario: 2027 ship demand +0.5–2.5% vs supply +3–4%; if blocked 2026 RU/UA grain stays blocked, grain shipment growth up to 4pp weaker in 2027 | FACT (BIMCO, Oct 30) — https://www.hellenicshippingnews.com/dry-bulk-shipping-escalating-attacks-on-ships-heighten-uncertainty/ | BIMCO update or Hormuz reopening |
| 8 | **Grains: fresh lows + flash export sales** | YES — Tue Nov 3 | CBOT corn 4-month low ($4.42¼), soy 2½-month low ($12.12¾), wheat $5.99 (Reuters, Nov 3). USDA flash sales: corn 1.7M mt to Mexico (Mon) + 315k mt Mexico, 136k mt South Korea (Tue); soy 136k mt China (Mon), 134k mt unknown (Tue). Yahoo at 13:18 PT today: corn (ZC=F) $4.4575, wheat (ZW=F) $5.9925, soy (ZS=F) $12.0375 — consistent with the weak tape | FACT (Reuters Nov 3 via trade press; Yahoo quotes) — https://urallnews.com/trading-update-corn-futures-hit-four-month-low-on-big-us-crop-export-worries-what-it-means/ ; https://www.admis.com.sg/ag-market-view-for-nov-2-2026/ | Nov 10 WASDE (see #10) |
| 9 | **Natural gas: storage comfortable; next report Thu Nov 5** | Scheduled, not yet released | Last report (week ending Oct 23, released Oct 29): +80 Bcf to 3,724 Bcf, +38 Bcf (+1%) vs 5-yr avg, −147 Bcf vs year ago. Next WNGSR Thu Nov 5, 10:30 ET (week ending Oct 30; ~70 Bcf 5-yr-avg injection cited as reference). EU storage 75% full vs 90% 5-yr avg (GIE via EIA supplement) — U.S. comfortable, Europe tight. Yahoo NG=F $2.95 at 13:18 PT | FACT (EIA via supplement/press) — https://www.eia.gov/naturalgas/weekly/supplement/#naturalgas ; https://www.fxempire.com/forecasts/article/natural-gas-tests-2-80-support-as-warm-forecast-limits-optimism-1642541 | Thu Nov 5 storage print |
| 10 | **November WASDE — still scheduled Nov 10, 12:00 ET** | Calendar item — NOT released | USDA's own 2026 calendar lists WASDE Nov 10 (and Dec 10), 12:00 ET; Oct 9 WASDE (WASDE-676) is the latest. Contradicted claim flagged: Glance aggregator stories claim Nov WASDE "postponed to Nov 14 due to shutdown" and "first update since Sept 12" — both contradicted by USDA's calendar and by the Oct 9 WASDE itself, and inconsistent with today's on-schedule EIA release. Per the standing government-data rule, the shutdown/postponement framing is NOT adopted; the Glance claim is treated as UNVERIFIED/contradicted, not as fact | FACT for Nov 10 date (USDA primary) — https://www.usda.gov/oce/commodity/wasde ; https://agsist.com/usda-calendar . UNVERIFIED for Nov 14 postponement (Glance only) — https://trends.glance.com/story/articles/Auto/US/en/rapid-read/s-c06640630b-f25471bc-d041-5dd4-b507-5aa8d84787cc | A USDA calendar change on usda.gov |

**What the curves appear to be pricing (INFERENCE, separated from fact):**

- **Crude: war-premium unwind, not a supply glut.** The EIA draw (crude, gasoline, distillate all down; distillates at a 23-year low) is tight on its face, yet Brent/WTI fell 7–9% on the day. The market sold into bullish inventory data, which points to geopolitics — midterm-driven de-escalation hopes and Hormuz-reopening talk — overwhelming the inventory signal today. **What would change it:** a signed U.S.–Iran deal or Hormuz transit resumption (confirms the unwind, further downside) vs. renewed strikes or a failed mediation (re-prices the premium violently upward). The distillate tightness vs. crude selloff divergence is worth watching: product cracks, not flat crude, may carry the tightness story.
- **Grains: big-crop / weak-export-demand discount.** Four-month corn lows and 2½-month soy lows alongside large flash sales to Mexico/China read as a market that has supply and doubts demand pace — the Nov 10 WASDE is the next repricing event, not today's tape.
- **Nat gas: comfortable U.S. winter, tight Europe.** U.S. storage back above the 5-yr average with NG ~$2.95 argues the U.S. curve is pricing a non-scarce winter; EU at 75% vs 90% average keeps LNG-pull upside as the tail, not the base case.

**Discrepancies and gaps (fail-closed notes):**

- **EIA consensus figures conflict across summaries:** BOE/Morningstar cite a Reuters poll expecting a +877k bbl crude *build*; SeekingAlpha/Barchart cite a −1.7M bbl *draw* expectation. The direction of the "surprise" therefore depends on which consensus is used — the desk reports the EIA actuals (−865k) as fact and the surprise interpretation as **UNVERIFIED** until a single Reuters poll figure is confirmed.
- **No futures-curve (contango/backwardation) term-structure read is offered:** front-month quotes only were pulled; deferred-contract spreads were not verified from a free source today — marked **UNVERIFIED**, not estimated.
- **No new USDA Crop Progress details claimed:** the Mon Nov 2 report was not independently verified in this sweep; harvest percentages in the Nov 2 ADMIS note (corn ~74% expected, soy ~90% expected) are expectations, not the USDA release itself.

**Bottom line for the package:** Fresh and material today: (1) EIA petroleum report landed on schedule — crude/gasoline/distillate all drew, distillates at a 23-year low — yet crude sold off ~7–9% as midterm results and Iran-de-escalation hopes unwound the war premium; (2) Hormuz/Black Sea shipping diplomacy is active but unsigned (India/Türkiye Black Sea proposals, Qatar mediating on Iran); (3) grains at multi-month lows into the Nov 10 WASDE; (4) next catalyst is Thu Nov 5 EIA gas storage, then Nov 10 WASDE.

---

## 6. Box/Parity Observer

**As-of:** 2026-11-04, search sweep during the 13:30 PT run. **No new published SPY/QQQ put-call parity violation found.** One index constituent change takes effect today; one pending methodology change is flagged as a watch item only.

**1. Index change effective today — Okta joins the S&P 500 (SPY-relevant constituent change, not a methodology change).** S&P Dow Jones Indices announced on Oct 30, 2026 that Okta (OKTA) would replace Kenvue (KVUE) in the S&P 500, effective before the market open on Wed Nov 4, 2026, following Kimberly-Clark's pending acquisition of Kenvue. Glaukos, McGrath RentCorp, and Loar Holdings move into new roles across the S&P MidCap 400 / SmallCap 600 in the same reshuffle. Sources (secondary, citing the S&P DJI Oct 30 announcement; primary S&P DJI release not directly re-fetched — verify against spglobal.com/spdji before treating the effective-date detail as primary-sourced): https://www.finnsign.com/articles/okta-to-join-sandp-500-as-indexes-shuffle-post-manda-glaukos-mcgrath-loar-move-up ; https://southbaychronicle.com/2026/11/02/okta-joins-sp-500-replaces-kenvue-kimberly-clark-november-4/ . INFERENCE: mechanical, M&A-driven constituent replacement for index trackers, not a parity signal. It changes what SPY holds, not whether SPY options obey put-call parity. No parity verdict follows. Parity note (CFA rule applied): deterministic parity (C + PV(K) = P + S, box payoff = strike width) is unaffected by a constituent swap; when any model output disagrees with that identity, the math wins.

**2. Watch only — S&P U.S. Style index methodology revision (announced Oct 23–28, NOT effective yet, NOT a headline S&P 500 change).** S&P Dow Jones Indices will revise its growth/value classification rules, effective before the open on Mon Dec 21, 2026, with preliminary files from Fri Dec 4, 2026. Growth drops 12-month price momentum (retaining 3-year EPS and sales measures); value adds intangibles-adjusted book-to-price, averages trailing and 1-year forward earnings-to-price, keeps sales-to-price, and adds free-cash-flow-to-price (excluded for real estate, banks, insurers, and some financials). Scope is the S&P U.S. Style Indices (including Pure Style) built on the S&P 500, MidCap 400, SmallCap 600, Composite 1500, S&P 900, and S&P 1000. Source: https://www.tradingview.com/news/benzinga:b353d12e7094b:0-s-p-changes-the-rules-here-s-new-value-vs-growth/ . INFERENCE: this does not change headline S&P 500 membership tracked by SPY; it reclassifies stocks *within* style indices. Relevance is indirect (style-ETF rebalancing into Dec 21), not a SPY/QQQ parity event. Re-check when Dec 4 pro-forma files appear.

**3. Parity scan — no violation found.** A Nov 2, 2026 Saxo options brief reported a put-call parity check on 18 November options at the Oct 30 close returning 20.16, described as close to the November VIX futures settlement, i.e. consistent rather than a violation. This is a VIX-futures consistency check, not an SPY/QQQ equity parity measurement. Source: https://www.home.saxo/en-mena/content/articles/options/a-day-priced-like-a-month---options-brief---2-november-2026-02112026 . The Optionly cross-venue arbitrage scan retrieved Nov 4 showed no quote pairs passing its fee/size/edge filters and stated its scan is incomplete; its box-rate table covers crypto venues (Deribit/Derive) only, not SPY/QQQ. Not evidence for or against equity parity. Source: https://www.optionly.com/arb . UNVERIFIED: no live SPY/QQQ box-spread implied-rate or put-call parity deviation was independently computed in this desk's sweep (no options-chain pull was run for this desk); any current deviation is therefore UNVERIFIED, not zero. October box-spread explainers/guides found in the sweep are educational material, not new violation findings.

**Checked, not new:** the Nasdaq-100 methodology update (Fast Entry, quarterly rank reviews, float-based weight cap) took effect May 1, 2026 — prior, not new — and no new Nasdaq-100 methodology document for November was found. Source for the May update: https://www.nasdaq.com/newsroom/nasdaq100-index-methodology-update-why-now

**Bottom line:** nothing material on parity violations today. The only dated item is today's mechanical S&P 500 constituent swap (OKTA in, KVUE out); the Dec 21 S&P style reclassification is a watch item, not a parity event.

---

## 7. Bonds & Rates desk

**Module run:** `cd ~/workspace/github/hedge-desk && python3 -c "from hedge_desk import rates_desk; import json; print(json.dumps(rates_desk.rates_environment(), default=str))"` — executed 2026-11-04 ~13:28 PT; module `as_of` 2026-11-04; all series observations dated 2026-11-03 (latest FRED daily print available at run time). Data source: `fred-public-csv-http-200`. Mode: `REAL_FRED_RATES`. No Yahoo fallback used; no numbers from memory. Note: no live 2026-11-04 FRED observation yet — today's print is UNVERIFIED until FRED publishes it.

| Metric | Value | As-of | Label |
|---|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-11-03 | FACT (FRED via rates_desk) |
| Fed funds change over 60-day window | +0.25 pp | 2026-09-08 → 2026-11-03 | FACT (module output) |
| Treasury 2Y (DGS2) | 4.61% | 2026-11-03 | FACT (FRED via rates_desk) |
| Treasury 10Y (DGS10) | 4.95% | 2026-11-03 | FACT (FRED via rates_desk) |
| 2s10s spread | +34 bp (0.0425 slope) | 2026-11-03 | FACT (module-computed) |
| Curve shape | UPWARD_SLOPING | 2026-11-03 | FACT (module classification) |
| SOFR | 3.97% | 2026-11-03 | FACT (FRED via rates_desk) |
| EFFR | 3.88% | 2026-11-03 | FACT (FRED via rates_desk) |
| OBFR | 3.88% | 2026-11-03 | FACT (FRED via rates_desk) |
| SOFR − EFFR spread | +9 bp | 2026-11-03 | FACT (arithmetic on module output) |

**2s10s direction of change (FACT, computed from the module's own 60-day histories):** window start 2026-09-08: 10Y 4.80 − 2Y 4.39 = +41 bp. Latest 2026-11-03: 4.95 − 4.61 = +34 bp. → **Net flattening of ~7 bp over the 60-day window**, with both ends higher in level (2Y +22 bp, 10Y +15 bp over the window). Day-over-day, the spread ticked up 2 bp (32 bp on 2026-11-02 → 34 bp on 2026-11-03) after falling from 38 bp on 2026-10-30 — a small bounce within the flattening trend, not a reversal. The 10Y peaked at 5.31% (2026-10-05) and has since eased to 4.95%; the 2Y peaked at 4.92% (2026-09-28) and sits at 4.61%. Both ends have retraced from their window highs.

**Funding stress gauge (FACT + INFERENCE):** SOFR (3.97%) sits 9 bp above EFFR (3.88%), with OBFR equal to EFFR at 3.88%. A single-digit SOFR–EFFR gap is consistent with orderly overnight funding, not stress (INFERENCE). *What would change it:* a SOFR–EFFR widening into the 20+ bp range or a sustained multi-day drift would signal funding pressure and would flip this read.

**Directional read for premium pricing (INFERENCE, grounded in the FACTs above):** the curve remains upward-sloping but flatter than 60 days ago, and absolute long yields remain elevated (10Y 4.95%, near the top of its recent range despite the pullback from 5.31%). Higher long rates = higher discount rates = continued pressure on growth multiples — the value-investor lens favors margin of safety here; elevated discount rates argue against paying up for long-duration growth exposure. Flattening (bear-flattening in level terms, since both ends rose but the 2Y rose more) historically compresses term premium and argues for caution on duration-heavy premium-selling theses that assume a steep curve; the day-over-day +2 bp steepening is too small to change that read. *What would change it:* a 10Y break back above 5.31% (window high) would strengthen the discount-rate pressure case; a 2s10s inversion (spread < 0) would flip the curve-shape verdict to inverted and materially change the macro read; a decisive 10Y drop below ~4.80% (window-start level) would soften the pressure case.

**Yield-labeling note:** ^TNX is the 10Y, ^FVX is the 5Y — never labeled as 2Y here; the 2Y above is FRED DGS2 from the module, not a Yahoo ticker. No Yahoo yields substituted (per brief); ^TNX/^FVX not used as the rates source. Fed funds change (+0.25 pp) is the module's 60-day window figure, not a claim about any single FOMC move. All verdicts rest on the 2026-11-03 FRED prints; today's (2026-11-04) prints are UNVERIFIED pending publication.

**Raw module output (quoted verbatim):** `{"schema_version": "hedge-desk-rates-desk-1.0.0", "mode": "REAL_FRED_RATES", "as_of": "2026-11-04", "fed_funds_effective_rate": "3.88", "fed_funds_latest_date": "2026-11-03", "fed_funds_change_over_window": "0.25", "treasury_2y": "4.61", "treasury_2y_date": "2026-11-03", "treasury_10y": "4.95", "treasury_10y_date": "2026-11-03", "spread_10y_2y_points": "34.00", "curve_slope": "0.042500", "curve_shape": "UPWARD_SLOPING", "lookback_days": 60, "sofr": "3.97", "sofr_date": "2026-11-03", "effr": "3.88", "effr_date": "2026-11-03", "obfr": "3.88", "obfr_date": "2026-11-03", "data_source": "fred-public-csv-http-200", "trade_authorized": false, "note": "Observations of official FRED daily series. Fed funds/src curve change is a measured fact, not a forecast and not advice. No order placed."}`

**Decision-relevant summary for synthesis:** curve still upward-sloping at +34 bp but ~7 bp flatter than 60 days ago; 10Y at 4.95% keeps discount-rate pressure on growth multiples; funding calm (SOFR–EFFR +9 bp).

---

## Desk status

| Desk | Status |
|---|---|
| 1. Earnings Event | Reported — NVDA Nov 17 only event in window |
| 2. Dividend Opportunity | Reported — AAPL ex Nov 12, MSFT ex Nov 19 |
| 3. Overnight Premium (IV) | Reported — IV-inputs within 26h guard, labeled STALE; live pull supplemented; IV rank UNVERIFIED |
| 4. Open Quant/AI Model Lab | Reported — no new candidate; #9 ARCHIVE → WATCH, ledger updated |
| 5. Futures Event (catalysts) | Reported — EIA on schedule, crude selloff, WASDE Nov 10 confirmed |
| 6. Box/Parity Observer | Reported — no violation; OKTA/KVUE swap effective today |
| 7. Bonds & Rates | Reported — REAL_FRED_RATES, as of Nov 3 prints |

No desk produced no output. No section invented. Research and input only — no git operations, no PRs, no code changes performed in this run.
