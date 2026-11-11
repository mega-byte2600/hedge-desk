# Hedge-desk daily research — Wed 2026-11-11

**Run:** 13:30 PT, Wed Nov 11, 2026. **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety. Paper-only; no Risk of Ruin, no trade authorization.
**IV inputs file:** `~/workspace/hedge-desk-research/nightly/2026-11-10-iv-inputs.json`, `as_of` **2026-11-10T14:54:30-07:00** — ~22.5h old at run start, **within the 26h freshness guard (usable) but labeled STALE** (yesterday's post-close data, not today's).

## Synthesis — the 5 most decision-relevant items

1. **NVDA earnings Tue Nov 17 after close is the only watchlist print in the window** — options pricing **±9.3%** (own Yahoo-chain calc, Nov 18 expiry) vs ~5.6% average actual move over the last 12 reports. Premium is elevated into a binary event; standing desk rule = **avoid selling NVDA premium into the print**. (Desks 1 + 3 agree.)
2. **Every IV-vs-realized verdict this run is WINDOW-CONTINGENT.** The Nov 5 crash day drives 42–54% of the 20-day realized variance for every symbol. Live front IV is low in absolute terms (SPY 9.86%, QQQ 17.99%, 1 DTE) but that is **not** a clean "IV cheap" signal. IV rank is **UNVERIFIED** for all six names — no free IV-history source.
3. **Rates (FRED, as of Nov 9):** EFFR 3.88%, 2Y 4.56%, 10Y 4.88%, 2s10s **+32 bp, flattening** (front end +10 bp w/w vs long end +4 bp). SOFR–EFFR **0 bp** — no funding stress. Long rates near 4.9% keep a discount-rate headwind on growth multiples (NVDA, TSLA, MSFT).
4. **Hormuz risk premium is alive but shrinking.** Attacks continue (tanker struck Nov 10; 37 ships attacked in Oct, ≥10 in the first 10 days of Nov) even as Brent slid ~20% off late-Oct highs to $91.49 (Nov 10 close), rebounding ~1–2% today. EIA's Nov STEO sees Brent near $100 through year-end vs futures ~$92–93 — the market prices faster normalization than EIA. **EIA weekly petroleum report delayed to Thu Nov 12, 12:00 ET** (Veterans Day); the API preview is contradictory across secondary reports → **UNVERIFIED**.
5. **Dividends:** AAPL goes ex-div **tomorrow, Nov 12** ($0.27, rate held); MSFT goes ex-div **Nov 19 at the new $0.98 rate** (first payment at the raised level, +7.7%); NVDA's Q4 dividend is undeclared, declaration expected ~Nov 19–20, ex-date likely early December. **Quant Lab:** no TEST / no INTEGRATE this run; standout WATCH is #255, point-in-time earnings-call encoders (score 59).

Standing note (carried from this morning's premarket sweep, ~07:00 PT Nov 11): the Nov 10 20:54 PT batch refresh failed closed (gate 2/4, `data_freshness.is_current=false`); the live dashboard is still the Nov 8 report on the Nov 6 close — now 2 trading days stale. Not re-verified by this run's desks.

---

## 1. Earnings Event desk

**Headline: NVDA is the only watchlist name reporting in the next two weeks (through Nov 25).** AAPL, MSFT and TSLA all reported in the last three weeks; their next prints are late January 2027 (estimates only, unconfirmed). SPY and QQQ are ETFs — no earnings.

| Ticker | Report date | Timing | Quarter | Consensus EPS | Implied expected move | Historical avg earnings-day move |
|---|---|---|---|---|---|---|
| NVDA | **Tue Nov 17, 2026** | After close — results ~1:20 p.m. PT, call 2:00 p.m. PT / 5:00 p.m. ET | Q3 FY2027 (ended Oct 25, 2026) | $2.49 (Nasdaq, 13 ests); $2.47 per other aggregators | **±9.3%** (own Yahoo calc, Nov 18 expiry); third-party range ±6.5% to ±10.6% by method | Mean 5.6% (last 12, ApexVol) to ±7.8% (10-yr, n=39, EarningsWatcher); median 4.36% (last 16, Finviro) |
| AAPL / MSFT / TSLA | none in window | — | — | — | — | — |
| SPY / QQQ | n/a (ETFs) | — | — | — | — | — |

**NVDA — detail (FACT unless labeled):**
- **Date/timing — company-confirmed, independently verified:** NVIDIA's Oct 28, 2026 press release sets the Q3 FY2027 call for Tue Nov 17 at 2 p.m. PT, results ~1:20 p.m. PT, CFO written commentary posted with the release. Nasdaq earnings-calendar API independently lists NVDA on 2026-11-17, `time-after-hours`, fiscal quarter ending Oct/2026, consensus EPS $2.49 (13 estimates), last-year EPS $1.24 (report date 11/19/2025). First full session on the news: Wed Nov 18.
  - Sources: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx ; Nasdaq API `https://api.nasdaq.com/api/calendar/earnings?date=2026-11-17` (queried live 2026-11-11).
- **Guidance / bar:** revenue $108.0bn ±2%, GAAP and non-GAAP gross margin 74.0% ±50bp, no Data Center compute revenue from China assumed (company guidance, Aug 26 Q2 release, as reported). Consensus revenue ~$108.8–109.2bn (secondary aggregators — INFERENCE-level, not company-stated). Q4 margin guided to trough at 71–72% (CFO commentary on Aug call, as reported).
- **Options-implied expected move — FACT (own calculation from live Yahoo options chain, cookie+crumb handshake, Nov 11 ~16:00 ET close, NVDA $173.73):** Nov 18 expiry (first expiry after the print — cleanest earnings-only read): ATM 172.5 straddle mid $16.12 = **±9.28%**, ATM IV ~77–80%. Nov 20 expiry: ATM 175 straddle mid $17.05 = **±9.81%** (includes two extra sessions of ordinary movement, so it overstates the pure print move). Third-party cross-checks: EarningsWatcher ±9.5% as of Nov 11 (±10.6% as of Nov 10); ApexVol earnings-only ±6.5% with Nov 20 straddle ±10.9% (priced Nov 10); Finviro ±7.89% nearest expiry. One outlier, Tradestie ±4.5% (Nov 10), is inconsistent with the live chain — **UNVERIFIED, do not use**.
  - **Desk read (INFERENCE):** the market is pricing a move roughly double NVDA's recent average actual move — premium is elevated into a binary event, which under the desk's standing rule is an avoid, not an opportunity, for premium sellers.
- **Historical moves — FACT (third-party histories, definitions differ — do not blend):** last 12 reports average 5.6% (ApexVol); 10-year average ±7.8%, n=39, 2-year ±5.7% (EarningsWatcher); median 4.36% over last 16 (Finviro). Last report Aug 26, 2026: **+8.7%** vs ±5.9% priced in (EarningsWatcher). EPS beat in 12 of last 12 reports (ApexVol).
- **Context — FACT (secondary):** NVDA closed $178.67 on Nov 9, ~21.9% off its Oct 13 high of $228.64 (Tradestie, Nov 10). No earnings release exists to read yet — the release itself lands Nov 17; the CFA read-the-release rule applies on the day, not today.
- **What would change this:** NVDA's date is company-confirmed, so a change would require a company notice; the implied move reprices daily and must be re-pulled before the print.

**Just-reported names (outside window — one line each, for the record):**
- **AAPL — FACT:** reported Mon Nov 2, 2026 after close (Q4 FY26); EPS $2.10 vs $1.98 consensus; fell 1.9% on Nov 3. Next print estimated Jan 28 (Seeking Alpha) to Feb 4, 2027 (TipRanks/Zacks) — **UNVERIFIED, sources disagree, company has not confirmed**.
- **MSFT — FACT:** reported Wed Oct 28, 2026 after close (Q1 FY27); EPS $4.89 vs $4.72 consensus. Next print estimated Jan 26–27, 2027 — **UNVERIFIED, unconfirmed**.
- **TSLA — FACT:** reported Wed Oct 21, 2026 after close (Q3 2026); EPS $0.48 vs ~$0.45–0.46 consensus. Next print estimated Jan 27, 2027 — **UNVERIFIED, unconfirmed** (Tesla confirms Q4 dates via its early-January deliveries release).
- **SPY / QQQ — FACT:** index ETFs; no earnings reports.

**UNVERIFIED items:** all Jan-2027 dates for AAPL/MSFT/TSLA (estimates only); Tradestie's ±4.5% NVDA implied move (discordant with live chain).
Sources: NVIDIA Investor Relations press release Oct 28, 2026; Nasdaq earnings-calendar API (live query); Yahoo Finance v7 options chain for NVDA (own straddle calculation); ApexVol https://apexvol.com/earnings/nvda ; EarningsWatcher https://earnings-watcher.com/wiki/nvda-implied-move ; Finviro earnings page; SimianX Mag-7 tracker https://www.simianx.ai/stories/magnificent-7-earnings-dates-results-tracker .

---

## 2. Dividend Opportunity desk

**As of:** Wed Nov 11, 2026, ~13:27 PT. **Window:** ex-dates Nov 12 – Dec 9, 2026.

### In-window ex-dividend dates (watchlist)

| Ticker | Ex-date | Amount | Record | Pay date | Declared | Change vs prior qtr |
|---|---|---|---|---|---|---|
| AAPL | **Thu Nov 12, 2026** | $0.27 | Nov 12 | Nov 16, 2026 | Nov 2, 2026 | None — held at $0.27 |
| MSFT | **Thu Nov 19, 2026** | $0.98 | Nov 19 | Dec 10, 2026 | Sep 15, 2026 | **+7.7% — first payment at raised rate** |
| NVDA | Expected early Dec (undeclared) | ~$0.25 expected | — | ~Dec 25–26, 2026 est. | Not yet declared | None expected |
| SPY | None in window | — | — | — | — | — |
| QQQ | None in window | — | — | — | — | — |
| TSLA | None — pays no dividend | — | — | — | — | — |

### Per-name detail

**AAPL — ex-date TOMORROW, Nov 12, 2026 (FACT).** $0.27/share, declared Nov 2, 2026, record Nov 12, payable Nov 16, 2026. Confirmed by Nasdaq dividends calendar for 2026-11-12 and Nasdaq quote dividends endpoint; Yahoo v8 chart history corroborates the $0.27 rate (ex-dates Feb 9 / May 11 / Aug 10, 2026). No increase in this declaration — the rate is unchanged from the prior two quarters. Annualized $1.08; yield 0.30% at $355.63 (FACT, Nasdaq yield 0.31%; computed 1.08/355.63 = 0.30%).
- **Consecutive-increase count: 15 years per the desk standard (FACT, derived from Nasdaq history).** Initiation 2012 = year 1; increases announced every calendar year 2013–2026 (latest Apr 30, 2026, $0.26→$0.27, +3.8%). No skipped year in the run. A raise has been announced in calendar 2026, so the count is current.

**MSFT — ex-date Nov 19, 2026 (FACT).** $0.98/share, declared Sep 15, 2026, record Nov 19, payable Dec 10, 2026. Confirmed by Nasdaq dividends calendar for 2026-11-19 and quote dividends endpoint. This is the first ex-date at the raised rate (+7.7% vs $0.91). Annualized at new rate $3.92; forward yield 0.75% at $521.13 (computed; Nasdaq's header still shows stale $3.64 / 0.68% based on the old $0.91 rate — do not use that figure).
- **Consecutive-increase count: 24 years (FACT, desk-standard anchor).** Includes the Sep 15, 2026 raise to $0.98/qtr; initiated 2003, no skipped year. A raise has been announced in calendar 2026, so the count is current.

**NVDA — no declared dividend in window; declaration expected ~Nov 19–20 (INFERENCE).** Last ex-date Sep 10, 2026, $0.25, paid Oct 1, 2026 (FACT, Nasdaq + Yahoo agree). No Q4 declaration exists yet in Nasdaq data as of this writing (FACT). Pattern-based expectation: 2025 declaration came Nov 19, 2025 with ex-date Dec 4, 2025 and payment Dec 26, 2025; third-party estimates point to a ~Dec 25–26, 2026 payment at $0.25 if the rate holds, implying an ex-date in early December — inside this window — but the ex-date is **UNVERIFIED** until declared. Multiple secondary sources (Finbold, TokenPost, Snowball) agree the payment is not yet declared; treat any specific ex-date (e.g. ~Dec 10 per one estimator) as SPECULATION.
- **2026 raise (FACT):** $0.01 → $0.25/qtr (+2,400%), declared May 20, 2026, first paid Jun 26, 2026; corroborated by Nasdaq history and Motley Fool (Sep 15, 2026). NVDA has paid $0.51/share YTD in 2026 vs $0.04 total in 2025.
- **Consecutive-increase count: 1 year per the desk standard (FACT, derived from Nasdaq history).** 2024 had an announced increase (May 2024, to $0.01 post-split, +150% split-adjusted), 2025 had NO announced increase (flat $0.01 all four quarters — streak reset), 2026 has the $0.25 raise. Note: some third-party screeners claim "3 consecutive years" for NVDA; that is inconsistent with the issuer/Nasdaq payment record and is NOT used — per the standard, screeners are never copied without issuer verification.

**SPY — no ex-date in window (FACT).** Last four quarterly distributions (Yahoo v8 chart): Dec 19, 2025 $1.993; Mar 20, 2026 $1.797; Jun 18, 2026 $1.904; Sep 18, 2026 $1.889. Trailing 12-mo total $7.583; trailing yield ~1.00% at $759.84 (computed from Yahoo events). Next distribution expected Fri Dec 18, 2026 (third Friday of December, matching the 2024/2025 pattern) — **INFERENCE, outside the window**; amount unknown until State Street declares it (typically mid-December). Nasdaq's Dec 18 calendar currently lists no SPY distribution, which is expected pre-declaration, not evidence against the date. Nasdaq's SPY ETF dividends endpoint returned null data on two attempts — SPY figures here rest on Yahoo only.

**QQQ — no ex-date in window (FACT).** Last four quarterly distributions (Nasdaq ETF endpoint + Yahoo agree): Dec 22, 2025 $0.794; Mar 23, 2026 $0.733; Jun 22, 2026 $0.813; Sep 21, 2026 $0.751. Trailing total $3.091; trailing yield 0.45% at $690.38 (Nasdaq: 0.45%). Next distribution expected ~Mon Dec 21, 2026 (pattern: Dec 22, 2025; Dec 23, 2024) — **INFERENCE, outside the window**.

**TSLA — pays no dividend (FACT).** Nasdaq quote endpoint: ex-dividend date N/A, yield N/A; Yahoo v8 chart shows zero dividend events in the trailing year. No increase/cut/special to flag.

### Increases / cuts / specials
- **Increases:** MSFT +7.7% (Sep 15, 2026, to $0.98 — first payment at new rate Dec 10); NVDA +2,400% (May 20, 2026, to $0.25); AAPL +3.8% (Apr 30, 2026, to $0.27). No new increase announced in the past week.
- **Cuts:** none in watchlist. **Specials:** none in watchlist.

### Desk read (labeled)
- The only imminent capture event is AAPL going ex-div tomorrow (Nov 12) at $0.27 — ~0.08% of the share price, mechanically trivial against daily volatility (INFERENCE). No dividend-driven mispricing signal in the watchlist: yields are 0.30–1.00% and all in-window amounts were declared weeks ago and are fully known (INFERENCE).
- The one live watch item is NVDA's undeclared Q4 dividend: declaration expected ~Nov 19–20 per the 2025 pattern; if declared at $0.25, the ex-date likely lands in early December, inside the window (INFERENCE). A hold at $0.25 would make 2026 NVDA's first full year at the new rate (~$1.00 annualized, ~0.58% at $173.73).
- What would change this section: an NVDA board declaration (expected late Nov) or any new increase/cut announcement.

Prices used for yields are Yahoo v8 chart regularMarketPrice as of the pull (~13:27 PT Nov 11, 2026): SPY $759.84, QQQ $690.38, AAPL $355.63, MSFT $521.13, NVDA $173.73, TSLA $390.84.
Sources: Nasdaq dividends calendar API https://api.nasdaq.com/api/calendar/dividends?date=2026-11-12 , ?date=2026-11-19 , ?date=2026-12-18 (queried Nov 11, 2026); Nasdaq quote dividends endpoints (AAPL/MSFT/NVDA/TSLA stocks, QQQ ETF; SPY ETF endpoint returned null twice); Yahoo Finance v8 chart dividend events (query1.finance.yahoo.com/v8/finance/chart/{SPY,QQQ,AAPL,MSFT,NVDA,TSLA}?range=1y&events=div), UA-only, pulled Nov 11, 2026 ~13:27 PT; desk standard ~/workspace/hedge-desk-research/dividend-count-standard.md; NVDA raise corroboration https://www.fool.com/investing/2026/09/15/3-stocks-that-declared-dividend-raises-2026/ ; undeclared-Q4 reporting https://finbold.com/nvidia-to-pay-2026s-last-dividend-on-this-date-heres-how-much-100-nvda-shares-will-earn/ and https://www.tokenpost.com/news/investing/29771 .

---

## 3. Overnight Premium (IV) desk

**Sources & as-of:** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-11-10-iv-inputs.json`, `as_of` **2026-11-10T14:54:30-07:00** — ~22.5h old at run start, **within the 26h freshness guard (usable) but labeled STALE**. Live supplement pulled 2026-11-11T13:28:37-08:00 via Yahoo Finance v7 options (cookie+crumb handshake, `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`), source URLs `https://query1.finance.yahoo.com/v7/finance/options/SPY?date=1794441600` and `.../QQQ?date=1794441600`.

### Stale-jump screen (standing rule, 2026-09-28) — FACT
**Every symbol is WINDOW-CONTINGENT.** Max single-day variance share of the 20-day realized window (2026-10-13 to 2026-11-09): SPY **0.536**, QQQ **0.444**, AAPL **0.498**, MSFT **0.425**, NVDA **0.450**, TSLA **0.461** — all >0.30. The Nov 5 crash day drives the trailing realized-vol window for the whole board. **Any IV-vs-realized verdict below is WINDOW-CONTINGENT, not a clean verdict.** The Nov 5 day ages out of the 20-day window around Dec 3.

### Live ATM IV — SPY / QQQ (LIVE, verified 2026-11-11 13:28 PT) — FACT
Nearest **live** expiry is 2026-11-12 (DTE 1); today's 2026-11-11 expiry died 16:00 ET (13:00 PT) and is excluded. Quotes are healthy (non-zero, tight bid/ask — not solver residuals).

| Symbol | Spot | Expiry | DTE | ATM strike | Call IV | Put IV | **ATM IV (mean)** |
|---|---|---|---|---|---|---|---|
| SPY | 759.84 | 2026-11-12 | 1 | 760.0 | 0.1100 | 0.0873 | **0.0986 (9.86%)** |
| QQQ | 690.38 | 2026-11-12 | 1 | 690.0 | 0.1740 | 0.1858 | **0.1799 (17.99%)** |

- SPY call IV (11.0%) sits notably above put IV (8.7%) at the ATM strike — upside skew on the 1-DTE tenor (FACT from the chain; interpretation is INFERENCE, see below). QQQ is near-balanced, slightly put-heavy (17.4% call / 18.6% put).
- Note: the first two live-pull attempts returned empty chains because the parser read `calls`/`puts` at the wrong payload level; the chain lives under `result[0].options[0]`. Corrected and re-verified — the prints above come from the corrected parse with the expiry-epoch assertion passing.

### STALE single-name ATM IV (from the 2026-11-10 file — DO NOT present as today's) — FACT, STALE
Tenor was 1 DTE, expiry **2026-11-11 — which has now itself expired** (died 13:00 PT today). These prints were live at pull time yesterday; they are expired-tenor now and are carried for context only, not as tradeable IV.

| Symbol | ATM IV (STALE, exp 2026-11-11) | Realized 20d (STALE window) | IV vs realized |
|---|---|---|---|
| AAPL | 0.1901 (19.01%) | 0.2731 (27.31%) | IV below realized — WINDOW-CONTINGENT |
| MSFT | 0.2568 (25.68%) | 0.3712 (37.12%) | IV below realized — WINDOW-CONTINGENT |
| NVDA | 0.5657 (56.57%) | 0.4990 (49.90%) | IV above realized — WINDOW-CONTINGENT |
| TSLA | 0.3386 (33.86%) | 0.6281 (62.81%) | IV well below realized — WINDOW-CONTINGENT |

Realized 20d (STALE window 2026-10-13 to 2026-11-09): SPY 0.2287 (22.87%), QQQ 0.3685 (36.85%).

### IV-vs-realized read — WINDOW-CONTINGENT (INFERENCE, not a clean verdict)
- **SPY live 1-DTE IV 9.86% vs trailing realized 22.87%; QQQ 17.99% vs 36.85%.** On the face of it, front-tenor IV prices a far calmer forward regime than the crash-inflated trailing window. That gap is **not** a clean "IV cheap" signal: the realized leg is dominated by a single Nov 5 jump (53.6% of SPY's 20-day variance), so the comparison is WINDOW-CONTINGENT. What would change it: the realized window rolling past Nov 5 (~Dec 3) or a fresh vol event repricing front IV.
- **NVDA is the only name with IV above trailing realized (56.6% vs 49.9%, STALE tenor)** — consistent with earnings premium building into its Nov 17 print, but the tenor is expired so this is context only, not a live quote.
- SPY's call-over-put ATM skew (INFERENCE): upside-chasing flow or call-side hedging demand into the 1-DTE tenor; alternatively a transient quote artifact — a single-tenor snapshot cannot distinguish the two (UNVERIFIED which).

### IV rank — UNVERIFIED for all six names
No IV history is available from free sources in this run, so no IV rank can be computed. **Never guessed.** Flag on absolute level only: NVDA's 56.6% (STALE) is by far the highest absolute IV on the board; SPY's 9.9% live 1-DTE IV is low in absolute terms, but without rank history that is not an "IV cheap" call.

### Term structure — UNVERIFIED / not observable
Only the nearest-expiry (1 DTE) tenor was pulled for each name. A term-structure curve needs ≥2 tenors; none was observed. No steepening/flattening claim can be made from this run.

### Earnings inside the window — FACT (from the file's 45-day Nasdaq sweep)
- **NVDA reports 2026-11-17 (6 days out).** Premium into a binary event = avoid: do not sell NVDA premium across the Nov 17 print without pricing the binary. Note the 1-DTE IV prints above do **not** embed NVDA earnings premium (earnings is 6 days out, beyond the 1-DTE tenor); any longer-dated NVDA premium quote would.
- No earnings found in-window for SPY, QQQ, AAPL, MSFT, TSLA in the file's sweep.

### Desk verdicts (decision-relevant)
1. **SPY/QQQ front IV is live and low in absolute terms (9.9% / 18.0%, 1 DTE), but the IV-vs-realized "cheap" read is WINDOW-CONTINGENT** — the trailing realized window is crash-inflated by Nov 5. No clean premium-selling signal from this comparison.
2. **NVDA earnings Nov 17 — avoid selling NVDA premium into the print.** Highest absolute IV on the board (56.6% STALE) is earnings-driven; confirm with a live pull before any action.
3. **IV rank and term structure are UNVERIFIED this run** — no free IV-history source, single-tenor snapshot only. Do not act on rank or curve-shape claims today.
4. **No elevated-IV-rank flag can be issued** (rank UNVERIFIED); the only flag is NVDA's absolute-IV + earnings combination.

### What would change these verdicts
- Realized window rolling past Nov 5 (~Dec 3) would un-contaminate the IV-vs-realized comparison.
- A live IV-history source would enable a real IV-rank read.
- A multi-tenor pull (e.g. 1 DTE + 7 DTE + 30 DTE) would make term structure observable.

### Failures / gaps (nothing silently dropped)
- SPY/QQQ `atm_iv` null in the 2026-11-10 file (nearest expiry 2026-11-10 already expired at pull time; post-expiry solver residuals failed closed per the no-invent rule) — **recovered by the live pull above** (nearest live expiry 2026-11-12, healthy quotes).
- Single-name ATM IVs in the file are STALE and their 2026-11-11 tenor has now expired; no live single-name pull was attempted this run (brief scope was SPY/QQQ supplement) — live single-name IV is UNVERIFIED as of 13:28 PT.
- Repo failover module (`hedge_desk.data.options_failover`) unavailable in the clone; legacy Yahoo-only pull used (recorded in the file's `failures`).

---

## 4. Open Quant/AI Model Lab

**Sweep window:** arXiv q-fin.*, submitted Nov 10–11, 2026. 7 new items, all submitted Nov 10 (Nov 11 submissions announce Nov 12 00:00 UTC — next sweep's window). All scores run through the repo scorer (`hedge_desk.research_intelligence.assess_source`), not hand-computed. All claims below are source-reported from abstracts only and labeled UNVERIFIED unless stated FACT. Full-paper reads: none this run. **No new candidate reached TEST; no INTEGRATE.**

### New candidates

| # | Candidate | Score | Disp. | Why |
|---|---|---|---|---|
| 254 | Tabular Foundation Models in Financial Predictions — TabFM for next-year earnings-change forecasting | 48 | **WATCH** | Google Research's TabFM (pretrained on synthetic tabular data, no post-release tuning) reportedly beats a fine-tuned open-weight LLM and all tree baselines on earnings-change prediction; authors' own caveat: single benchmark task. Earnings-lane relevant; synthetic pretraining avoids look-ahead from memorized outcomes. No code link in API record → reproducibility not established. [arXiv:2611.13550](https://arxiv.org/abs/2611.13550) |
| 255 | Brini et al — "Point-in-Time Encoders for Earnings Calls" | 59 | **WATCH** | 412,248 calls, yearly vintages 2010–2024, each reading only text dated on/before its cutoff; 33.8M-param call-only vintages beat general retrievers every test quarter; vectors raise by ~half the rank correlation between next-day returns and return/size forecasts; 2024 vintage forecasts earnings surprises better (interval includes zero on unseen calls); returns no better. Accepted at 3rd IEEE Workshop on LLMs for Finance (IEEE BigData 2026). Code link in arXiv comment: github.com/Alessiobrini/point-in-time-encoders-for-earnings-calls — **contents and LICENSE NOT verified this run (GitHub leg banned per run brief)**, so reproducibility not established. Highest score of the sweep. [arXiv:2611.14325](https://arxiv.org/abs/2611.14325) |
| 256 | Fine-Tuning an Order-Flow Foundation Model for Sub-Second Forecasting | 39 | ARCHIVE | 300M-param model on crypto Level-3 order flow; beats GBM baselines sub-second, but authors' own bound: predicted moves < spread + fees, application is execution/market-making. Crypto-only, no desk lane. [arXiv:2611.14117](https://arxiv.org/abs/2611.14117) |
| 257 | Optimal Trading Speed on Blockchain | 33 | ARCHIVE | Block-speed/priority-fee equilibrium; Base Flashblocks evidence. Crypto market-structure only. [arXiv:2611.13616](https://arxiv.org/abs/2611.13616) |
| 258 | Nonzero-Sum Stochastic Exit Games with Singular Belief Dynamics | 30 | ARCHIVE | Pure exit-game theory, no empirical evaluation, no desk procedure. [arXiv:2611.13841](https://arxiv.org/abs/2611.13841) |
| 259 | Deceleration without identification: testing a power-law trend in Bitcoin prices under persistent noise | 39 | ARCHIVE | Pre-registered test (OSF protocol + Zenodo replication package, not read); constant drift rejected at 5% under the declared family, but rejection fails under stronger persistence; Gompertz fits about as well. Crypto-only. Pre-registration discipline noted as process practice only. [arXiv:2611.13962](https://arxiv.org/abs/2611.13962) |
| 260 | Deep Learning for Operator Maps in Optimal Liquidation | 39 | ARCHIVE | Neural-net approximation of optimal-liquidation strategy map under transient impact. Execution theory; desk never does execution. [arXiv:2611.14245](https://arxiv.org/abs/2611.14245) |

### Re-checks (WATCH items, arXiv API id_list)
No version movement on any of the 10 version-triggered WATCH items since the 2026-11-10 sweep — all stay WATCH: #4 M2VN (2510.20699 v1), #9 Buchegger/Gonon (2608.22478 v2), #13 (2609.00332 v1), #14 (2509.11928 v3), #15 (2509.05911 v1), #20 (2609.22893 v2), #21 (2608.00616 v3, ICAIF'26 accepted), #25 (2609.13402 v3), #30 (2607.08500 v3), #31 (2511.07571 v3). Caveat: GitHub leg skipped per the run brief's ban, so #20's license block and #9's code-link claim remain unverified by a permitted leg.

### Ledger
All 7 new candidates appended as #254–#260 to ~/workspace/hedge-desk-research/quant-lab-ledger.md, with a re-check line added to the Jidoka log. No candidate lives only in a daily file.

### Decision-relevant takeaway
One item worth attention: **#255 point-in-time earnings-call encoders** — it is the first candidate to operationalize the desk's own look-ahead discipline (vintaged encoders, each blind to future text) and it quantifies the payoff (retrieval gains real, return-forecast gains nil). Follow-up for a permitted leg: verify the repo's license/contents, then sandbox a vintage encoder on a watchlist earnings-call window.

---

## 5. Weather / War / Logistics Futures Event desk

**As of: Wed 2026-11-11 ~13:30 PT (16:30 ET).**

### Headline triage — the 3 items that matter
1. **Hormuz attacks continue even as peace hopes pull crude ~20% off late-October highs — Brent rebounded ~1–1.5% today from two-month lows.** [FACT + INFERENCE]
2. **November WASDE (Tue Nov 10) was bullish for corn and soybeans vs. expectations — both ending stocks came in below trade averages; Dec corn +9¾¢, Jan soybeans +39¾¢ on the day.** [FACT]
3. **EIA weekly petroleum report did NOT land today — Veterans Day moved it to Thu Nov 12, 12:00 ET. The API preview is contradictory across secondary reports; treat it as UNVERIFIED until EIA publishes.** [FACT]

### 1. Energy — Hormuz / US–Iran war

| Item | Detail | Label |
|---|---|---|
| Brent / WTI, Tue Nov 10 close | Brent (Jan) settled $91.49, −1.17%; WTI (Dec) $86.04, −0.93%. Both two-month lows; Brent down from ~$117.6 in late Oct. | FACT — EIA STEO coverage via [OGJ](https://www.ogj.com/general-interest/economics-markets/news/55418180/eia-sees-brent-near-100-bbl-through-yearend-2026-as-middle-east-supply-constraints-persist), [Quantisnow](https://www.quantisnow.com/insight/eia-sees-brent-near-100-for-the-rest-of-the-6785180) |
| Brent / WTI, Wed Nov 11 intraday | Rebounded off the lows: Brent ~$92.8 (+1.4%, 13:14 GMT) to $93.64 (+2.35%, 12:04 ET); WTI ~$87.1–$87.7. Still down ~21% (Brent) / ~17% (WTI) since Nov 1. | FACT — [Reuters via JournalArta](https://journalarta.com/en/2026/11/11/oil-rises-iran-nuclear-material-standoff/), [TheGlobuzz](https://theglobuzz.com/2026/11/11/oil-prices-iran-enriched-nuclear-material/) |
| Fresh tanker attacks, Tue Nov 10 | UKMTO: a tanker struck northeast of Lima, Oman. Iran's Revolutionary Guards Navy separately said two tankers caught fire after hitting naval mines on an "unauthorised route" through the strait. UKMTO Wed reported another incident in the strait. | FACT — [Reuters via KWSN](https://kwsn.com/2026/11/10/oil-rises-from-two-month-low-as-hormuz-shipping-attacks-offset-iran-truce-hopes/), [MarineLink](https://www.marinelink.com/news/hopes-peace-continue-despite-ongoing-544301) |
| Attack tempo | 37 ships attacked in October — highest monthly total since the war began (Washington Institute for Near East Policy data via Reuters). At least 10 ships hit in the first 10 days of November. IMO: 130–133 incidents in the region since the conflict began Feb 28, at least 25 seafarers killed. | FACT — [HeadlinesXtra](https://headlinesxtra.com/2026/11/11/oil-rebounds-hormuz-shipping-attacks-iran-deal-november-11-2026/), [MarineLink](https://www.marinelink.com/news/hopes-peace-continue-despite-ongoing-544301) |
| Hormuz still closed; diplomacy stalled | Iran denies US peace talks are underway; security official Mohsen Rezaei said Tehran awaits a US response to seven conditions; Iran insists Hormuz stays closed until conditions are met. Foreign Minister Araghchi indicated it could reopen within two days if conditions were satisfied. Iran's security chief said Tehran will not allow enriched nuclear material to leave the country. | FACT — [TradersUnion](https://tradersunion.com/news/geopolitics-trade/show/4194191-iran-keeps-hormuz-closed/), [TheGlobuzz](https://theglobuzz.com/2026/11/11/oil-prices-iran-enriched-nuclear-material/) |
| Flows recovering despite attacks | Hormuz crude flows averaged 10.5 mb/d since Oct 1 (Kpler); total Gulf crude exports incl. bypass routes 16.7 mb/d, just shy of pre-war 17 mb/d. EIA estimate: Hormuz flows were 4.9 mb/d in Q2 2026 vs 21.6 mb/d in Q4 2025. Freight/insurance costs ~10× pre-war levels. | FACT — [DevDiscourse/Reuters](https://www.devdiscourse.com/article/international/4005006-roi-trumps-iran-war-pause-is-as-costly-as-new-strikes-bousso?amp) |
| Saudi East-West pipeline struck Nov 9 | Saudi state media: pipeline struck in Medina region Nov 9; limited fire extinguished, no reported casualties or disruption. | FACT — [HeadlinesXtra](https://headlinesxtra.com/2026/11/11/oil-rebounds-hormuz-shipping-attacks-iran-deal-november-11-2026/) |
| Russian refining hit | Russian refining capacity down ~30% since late October after renewed Ukrainian drone attacks; a drone attack caused a fire in the port area of Ust-Luga (Baltic) on Wed Nov 11, injuring three workers. | FACT — [KWSN/Reuters](https://kwsn.com/2026/11/10/oil-rises-from-two-month-low-as-hormuz-shipping-attacks-offset-iran-truce-hopes/) |
| What futures appear to be pricing | The ~$26/bbl Brent slide from ~$117.6 (late Oct) to ~$91.50 (Nov 10) prices a high probability of de-escalation / Hormuz reopening; today's ~1–2% rebound prices the counter-evidence that attacks have NOT stopped. The curve is caught between diplomacy hope and live maritime risk — a binary, headline-driven tape, not a smooth supply/demand read. | INFERENCE — price levels FACT (sources above); interpretation is inference |
| EIA Nov STEO (Tue Nov 10) vs. market | EIA: Brent near $100/bbl through year-end 2026, avg $97 in 2026, $86 in 2027, $77 by Q4 2027; Middle East production outages 2.5 mb/d in Oct vs 10.9 mb/d May peak; global inventories to start rebuilding in Q4. Futures (~$92–93) sit ~$7–8 BELOW EIA's near-term view — the market is pricing faster supply normalization than EIA. EIA inputs were finalised Nov 5 and do not reflect post-Nov-5 events. | FACT (EIA figures) + INFERENCE (market-vs-forecast gap) — [OGJ](https://www.ogj.com/general-interest/economics-markets/news/55418180/eia-sees-brent-near-100-bbl-through-yearend-2026-as-middle-east-supply-constraints-persist), [Fuels&Lubes](https://www.fuelsandlubes.com/eia-sees-brent-crude-near-usd-100-per-barrel-through-2026/) |

### 2. EIA weekly petroleum — DELAYED, not missing

| Item | Detail | Label |
|---|---|---|
| Weekly Petroleum Status Report (week ending Nov 6) | **Delayed by Veterans Day to Thu Nov 12, 12:00 ET** (normal slot Wed 10:30 ET). This is a scheduled holiday shift on EIA's published release calendar — NOT a data blackout or shutdown issue. No federal shutdown: CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11. | FACT — [FXEmpire](https://www.fxempire.com/forecasts/article/wti-crude-oil-tests-support-as-u-s-distillate-stocks-tighten-1643659), [PetroEyes](https://petroeyes.com/deep-dives/eia-report-release-schedule-explained/), [InvestingLive](https://investinglive.com/commodities/private-oil-inventory-survey-shows-huge-headline-build-vs-draw-expected/) |
| Last official EIA weekly (Nov 4, week ending Oct 30) | Commercial crude 409.8 mmbbl, −0.9 mmbbl w/w; distillates drew 3.6 mmbbl. End-Oct commercial crude ~410 mmbbl — lowest end-October level since 2014. US production record 14.003 mb/d (week ending Oct 30). | FACT — [FXEmpire](https://www.fxempire.com/forecasts/article/crude-oil-outlook-tight-us-fuel-stocks-clash-with-supply-recovery-1643330), [Goodman Macro](https://www.goodman-macro.com/en/articles/20261111-oil/) |
| API weekly (Tue Nov 10, week ending Nov 6) | **CONFLICTING secondary reports — UNVERIFIED.** IndexBox reports API showed a **+9.0 mmbbl crude build** (vs ~−0.6 mmbbl expected), gasoline ~flat (+4k bbl), distillates +1.5 mmbbl, Cushing +182k bbl, SPR −2.7 mmbbl to 279.5 mmbbl. The Hindu BusinessLine, citing the same API release, reports a **−9.8 mmbbl crude decline**. The two cannot both be right; do not use either figure as fact until EIA publishes Thu. | UNVERIFIED (conflict) — [IndexBox](https://www.indexbox.io/blog/us-crude-inventories-post-sharp-build-as-spr-continues-to-drain/), [Hindu BusinessLine](https://www.thehindubusinessline.com/markets/commodities/crude-oil-futures-rise-as-us-industry-data-shows-decline-in-inventories/article71688277.ece) |
| EIA STEO US outlook | US crude production forecast record 14.3 mb/d in 2027 (13.9 mb/d avg 2026); commercial inventories to stay below the 5-yr average until mid-2027, then rebuild toward ~444 mmbbl by year-end 2027. | FACT — [OGJ](https://www.ogj.com/general-interest/economics-markets/news/55418180/eia-sees-brent-near-100-bbl-through-yearend-2026-as-middle-east-supply-constraints-persist) |

### 3. OPEC Monthly Oil Market Report — released today (Wed Nov 11)

| Item | Detail | Label |
|---|---|---|
| Demand forecasts unchanged | Global oil demand growth +0.2 mb/d in 2026 and +2.6 mb/d in 2027, unchanged from October's assessment (after six straight months of cuts). 2026 global growth revised slightly up to 3.1%. Demand for DoC crude unchanged at 42.1 mb/d (2026) and 43.9 mb/d (2027). | FACT — [OPEC MOMR](https://publications.opec.org/momr), [SourceFirstNews](https://sourcefirstnews.com/opec-november-2026-report-saudi-oil-output-october) |
| Supply rebound | DoC crude production +2.04 mb/d m/m to 41.23 mb/d in October (secondary sources). Saudi Arabia told OPEC it pumped 10.563 mb/d in October, up from 8.372 mb/d in September; OPEC's secondary-source estimate puts Saudi at 9.194 mb/d. OECD commercial inventories −14.6 mmbbl m/m to 2,811 mmbbl (preliminary Sep data). | FACT — [OPEC MOMR](https://publications.opec.org/momr), [SourceFirstNews](https://sourcefirstnews.com/opec-november-2026-report-saudi-oil-output-october), [Maritime Professional](https://www.maritimeprofessional.com/news/opec-production-rises-october-nearing-424257) |
| Read | OPEC's flat demand call after six cuts, plus a 2 mb/d production jump, keeps its balance near neutral — no new tightening signal from Vienna today. The Saudi self-reported vs secondary-source gap (~1.37 mb/d) is a data-quality flag, not a market mover on its own. | INFERENCE |

### 4. USDA — November WASDE landed Tue Nov 10 (12:00 ET)

| Item | Detail | Label |
|---|---|---|
| Corn — bullish vs expectations | Yield cut 1.6 bu to 179.6 bu/acre (trade avg 180.6); production 15.893 bn bu, −141 mmbu vs Oct. Ending stocks 1.758 bn bu vs 1.846 bn trade avg (−91 mmbu vs Oct). Season-avg price forecast cut $0.10 to $4.60/bu. World ending stocks 281.94 mmt (+1.5 mmt). | FACT — [American Ag Network](https://www.americanagnetwork.com/2026/11/10/usda-trims-corn-yield-stocks-in-november-wasde/), [Teucrium](https://teucrium.substack.com/p/november-wasde-recap) |
| Soybeans — bullish vs expectations | Yield 53.3 bu/acre (from 53.1); production 4.574 bn bu (+12 mmbu). Exports raised 25 mmbu to 1.720 bn; ending stocks 300 mmbu vs 332 mmbu trade avg (−15 mmbu vs Oct), = 6.5% of use — tight by historical standards. Price forecast +$0.10 to $12.10/bu. World ending stocks 123.5 mmt. Brazil crop cut to 186.0 mmt (from 188.0). | FACT — [American Ag Network](https://www.americanagnetwork.com/2026/11/10/usda-trims-corn-yield-stocks-in-november-wasde/), [Klarenbach/PGI](https://pgi.klarenbach.ca/p/wasde-stocks-canola-gains-and-abu-dhabi-talks-nov-11-2026) |
| Wheat — neutral | US ending stocks 743 mmbu (+3 mmbu vs Oct), still 19% below last year. World ending stocks +4.8 mmt to 280.8 mmt (Argentina, Australia larger). | FACT — [Klarenbach/PGI](https://pgi.klarenbach.ca/p/wasde-stocks-canola-gains-and-abu-dhabi-talks-nov-11-2026) |
| Market reaction (Tue Nov 10) | Dec corn settled +9¾¢ at $4.49/bu; Jan soybeans +39¾¢ at $12.28/bu. Pre-report corn was +1¢, soybeans flat — the move was a report reaction. | FACT — [Klarenbach/PGI](https://pgi.klarenbach.ca/p/wasde-stocks-canola-gains-and-abu-dhabi-talks-nov-11-2026), [Ohio Ag Net](https://ocj.com/2026/11/november-wasde-bullish-corn-and-soybeans/) |
| Next USDA dates | Next WASDE Thu Dec 10, 12:00 ET. Final 2026 corn/soy production estimates Jan 12, 2027. Weekly Export Sales Fri Nov 13, 8:30 ET. Next Cattle on Feed Fri Nov 20. | FACT — [USDA WASDE](https://www.usda.gov/oce/commodity/wasde), [Teucrium](https://teucrium.substack.com/p/november-wasde-recap) |

### 5. Natural gas

| Item | Detail | Label |
|---|---|---|
| Storage (latest, week ending Oct 30) | Working gas 3,801 Bcf after +77 Bcf injection; −109 Bcf (−2.8%) vs year-ago, +54 Bcf (+1.4%) vs 5-yr average. | FACT — [FXEmpire](https://www.fxempire.com/forecasts/article/natural-gas-eyes-breakout-as-mixed-weather-dominates-fundamentals-1643930) |
| Next storage report | **Fri Nov 13** (delayed by Veterans Day; covers week ending Nov 6). Consensus cited for the week ended Nov 4 is +65 Bcf — treat as a survey estimate, not EIA data. | FACT (date) / UNVERIFIED (consensus figure) — [FXEmpire](https://www.fxempire.com/forecasts/article/natural-gas-eyes-breakout-as-mixed-weather-dominates-fundamentals-1643930), [Barchart](https://www.barchart.com/story/news/8787082/nat-gas-price-fall-on-forecasts-for-return-of-normal-us-temps) |
| Price action Wed Nov 11 | Dec NYMEX nat gas settled $3.215/MMBtu, −2.46% (−8.1¢), snapping a 3-session rally, after forecasts called for a return to seasonal temperatures (below-avg temps Nov 16–20 in the East, then normal). Front-month had traded near $3.10–$3.20 early in the week; intraday high ~$3.36. | FACT — [WSJ](https://www.wsj.com/finance/commodities-futures/european-ttf-gas-rises-as-storage-withdrawals-accelerate-569c8aab), [Barchart](https://www.barchart.com/story/news/8787082/nat-gas-price-fall-on-forecasts-for-return-of-normal-us-temps) |
| EIA Nov STEO gas cut | Winter Henry Hub forecast cut 16% to $2.87/MMBtu (Nov–Mar), citing mild weather, higher storage, production growth outpacing demand; 2026 avg $3.37, 2027 $2.88. Futures (~$3.22) sit above the winter forecast. US LNG exports forecast to rise from ~15 Bcf/d (2025) to 19 Bcf/d (2027). European storage 72% full vs 89% 5-yr avg — a separate winter-risk flag. | FACT — [AIAgentUpdate](https://aiagentupdate.com/post/eia-gas-forecast-2026-11-11), [FXEmpire](https://www.fxempire.com/forecasts/article/natural-gas-eyes-breakout-as-mixed-weather-dominates-fundamentals-1643930), [Barchart](https://www.barchart.com/story/news/8787082/nat-gas-price-fall-on-forecasts-for-return-of-normal-us-temps) |

### 6. Calendar — what is still to come this week

| Date / time (ET) | Event | Label |
|---|---|---|
| Thu Nov 12, 12:00 | EIA Weekly Petroleum Status Report (week ending Nov 6) — delayed from Wed | FACT |
| Fri Nov 13, 10:30 | EIA Weekly Natural Gas Storage Report (week ending Nov 6) — delayed from Thu | FACT |
| Fri Nov 13, 08:30 | USDA Weekly Export Sales | FACT |
| Thu Dec 10, 12:00 | Next WASDE | FACT |

### Desk verdict
- **Decision-relevant items:** (1) Hormuz risk premium is alive but shrinking — crude's ~20% November slide prices de-escalation, yet attacks continue daily; any single incident can re-price the front month by dollars, so energy-adjacent premium is headline-binary this week. (2) WASDE tightened corn/soybean balances vs expectations — grain futures repriced higher Tue; the Dec 10 WASDE is the next scheduled grain catalyst. (3) No EIA petroleum data today — the Thu noon release is the next hard energy data point; the API preview is unusable due to conflicting secondary reports.
- **Nothing material found on:** new logistics/supply-chain disruptions outside energy (no fresh port/rail/weather event surfaced today); no new USDA report beyond the Nov 10 WASDE.
- **What would change this read:** EIA Thu noon showing a large crude draw/build vs the (conflicting) API signals; a Hormuz reopening announcement or a major new attack/closure escalation; a cold-snap revision to US weather forecasts ahead of Fri gas storage.

Sources: EIA (via OGJ, FXEmpire, Goodman Macro, Fuels&Lubes); USDA WASDE page; OPEC MOMR; Reuters via KWSN/MarineLink/JournalArta; American Ag Network; Teucrium; Barchart; WSJ. All accessed Wed 2026-11-11, ~13:30–13:45 PT.

---

## 6. Box / Parity Observer

**Verdict: Nothing material new today — one line: no new SPY/QQQ parity-violation report or index-methodology change published in the last 24 hours; one standing item carried forward below.**

- **Index methodology — FACT:** S&P Dow Jones Indices announced 2026-10-28 a revision to its U.S. growth/value classification rules, effective before the open on **2026-12-21**, with preliminary files from **2026-12-04**: 12-month price momentum removed from growth rankings; value adds free-cash-flow-to-price and an intangibles-adjusted book-to-price. Scope includes the S&P 500 style indices; Bloomberg Intelligence estimates ≥$375B in passive funds follow the affected indices. **INFERENCE:** This is a style-classification change, not a change to S&P 500 membership/weighting itself, so no direct SPY/QQQ basket or parity implication — monitor the Dec 4 pro-forma files only for style-ETF flows. Sources: https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing ; https://www.kucoin.com/news/flash/s-p-to-revise-growth-and-value-stock-classification-rules
- **Parity violations — FACT:** No new published SPY/QQQ box-spread or put-call parity violation analysis found in today's sweep (searches 2026-11-11). The most recent relevant paper remains Shin, "The Cost of a Free Lunch: Evidence from U.S. Derivatives Markets" (arXiv, 2026-08-24): using minute-level NBBO on SPX/RUT options, quoted put-call parity residuals vs traded futures are near zero in price space, but option-implied discount factors sit systematically above the OIS curve — median annualised carry gap ≈37bp, >98% positive. **INFERENCE:** The gap is a carry/funding wedge and path/margin cost of enforcing parity, not an unclosed price-space arbitrage — consistent with deterministic parity holding after costs. Disposition: WATCH, no desk action. Source: https://arxiv.org/html/2604.19604
- **Standing rule restated:** Deterministic put-call/box parity outranks any model output — when they disagree, the math wins. No SPY/QQQ parity break was found today that would trigger that rule.

*As-of: Wed 2026-11-11 ~13:27 PT. No numbers estimated; no Risk of Ruin, no trade authorisation.*

---

## 7. Bonds & Rates desk

**Status: PASS.** Module `hedge_desk.rates_desk.rates_environment()` ran clean (exit 0), mode `REAL_FRED_RATES`, source `fred-public-csv-http-200`. All figures below are from that module output. As-of: **2026-11-09** (latest FRED daily observation; Nov 11 is Veterans Day, a bond-market holiday — INFERENCE for why no Nov 10–11 observations exist).

### Levels (FACT — FRED via rates_desk, as of 2026-11-09)

| Series | Level | Date |
|---|---|---|
| Fed funds effective rate (DFF) | **3.88%** | 2026-11-09 |
| 2Y Treasury (DGS2) | **4.56%** | 2026-11-09 |
| 10Y Treasury (DGS10) | **4.88%** | 2026-11-09 |
| SOFR | **3.88%** | 2026-11-09 |
| EFFR | **3.88%** | 2026-11-09 |
| OBFR | **3.88%** | 2026-11-09 |

### Curve shape and direction of change (FACT — computed from module history)
- **2s10s slope: +32 bp, curve UPWARD_SLOPING.** (10Y 4.88% − 2Y 4.56%.)
- **Direction: flattening.** Slope was 47 bp on 2026-10-05, 38 bp on 2026-10-30 and 2026-11-05, 35 bp on 2026-11-06, 32 bp on 2026-11-09. Over the past week the front end did the flattening: 2Y rose 10 bp (4.46% → 4.56%, Nov 5 → Nov 9) while 10Y rose only 4 bp (4.84% → 4.88%).
- **Both ends down over the 60-day window:** 2Y −9 bp (4.65% → 4.56%) and 10Y −9 bp (4.97% → 4.88%) since 2026-09-14 — the slope is unchanged vs 60 days ago (32 bp then, 32 bp now); the flattening is a move off the early-October peak, not a 60-day trend.
- **Fed funds change over window: +0.25 pp** (module-reported, 60-day lookback).

### Funding stress (FACT)
- **SOFR − EFFR spread: 0 bp** (both 3.88%). OBFR also 3.88%. No funding stress signal — all three overnight benchmarks coincide exactly.

### Directional read for premium pricing (INFERENCE)
- Long rates near 4.9% keep discount rates elevated — a headwind for growth-multiple valuations on the watchlist (notably NVDA, TSLA, MSFT), which argues against paying up for long-dated upside premium on valuation grounds alone; it does not by itself make premium cheap or expensive.
- The flattening (front end rising faster than the long end) implies the market is pricing less near-term easing, not a growth scare: the long end is essentially flat on the week (+4 bp). A flattening driven by the front end typically compresses the term premium embedded in longer-dated options less than a long-end selloff would.
- No funding-stress read-through: a 0 bp SOFR–EFFR spread gives no reason to expect forced-selling or liquidity-driven vol spikes from the funding channel.

### What would change this read
- A 2s10s move back above ~45 bp (re-steepening) or below 0 bp (inversion) would change the curve call; a SOFR–EFFR spread widening beyond ~5 bp would flag funding stress; a fresh FRED observation (next business day, Nov 12) supersedes the Nov 9 levels.

**Sources:** FRED daily series DFF, DGS2, DGS10, SOFR, EFFR, OBFR via `hedge_desk.rates_desk.rates_environment()` (schema `hedge-desk-rates-desk-1.0.0`), run 2026-11-11 ~13:27 PT. No Yahoo yields used; no ^FVX/13W substitution needed — the module supplies a real 2Y.

---

## Cross-desk reconciliation

- **NVDA earnings (Desks 1 + 3): agree.** Nov 17 after close, company-confirmed; options pricing ±9.3% vs ~5.6% average actual move; both desks flag premium into the binary event as avoid. No contradiction.
- **IV vs realized (Desk 3 alone):** all six symbols WINDOW-CONTINGENT; no desk issued a clean "IV cheap/rich" verdict. No contradiction with any other desk.
- **Rates vs futures (Desks 5 + 7):** no contradiction — Desk 7's Nov 9 FRED 10Y (4.88%) is the latest official observation; no desk in this run verified an intraday 10Y level, so none is asserted here.
- **No desk failed.** All seven desks produced output. Gaps, labeled in place: IV rank UNVERIFIED (all names); term structure UNVERIFIED (single-tenor snapshot); live single-name IV UNVERIFIED (STALE file tenor expired); NVDA Q4 ex-date UNVERIFIED until declared; Jan-2027 earnings dates for AAPL/MSFT/TSLA UNVERIFIED (estimates only); API crude-inventory preview UNVERIFIED (conflicting secondary reports).

## Method notes
- Market data: Yahoo Finance first, Nasdaq second, then fallbacks. Yahoo v8 chart UA-only; v7 options/quote via cookie+crumb handshake.
- Yield labeling: ^TNX = 10Y, ^FVX = 5Y (never 2Y); 13W bill is the front-end anchor when no real 2Y is available. Desk 7 used the module's real DGS2 2Y.
- Government data: no federal shutdown — CR passed 2026-09-01, signed 2026-09-02, funding through Dec 11. EIA/USDA releases on schedule except the Veterans Day holiday shift noted above.
- Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED throughout, per the CFA evidence standard. No number was guessed; no Risk of Ruin was estimated; no trade was authorized.
