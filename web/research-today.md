# Hedge-Desk Daily Research — Thu 2026-11-05

**Run:** daily research, 13:30 PT. **Research and input only** — no git push/pull, no PRs, no code changes, no GitHub operations.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety; never risk-seeking framing.
**Method:** CFA standard — every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED with source and as-of timestamp. Market data: Yahoo first, Nasdaq second, fallbacks after.

## The day in one paragraph (synthesis)

**Thu Nov 5, 2026 was a crash day, and it reprices everything in this package.** SPY closed −4.41%, QQQ −6.49%, NVDA −9.26%, TSLA −10.77% (FACT, Yahoo v8 chart). That single day dominates every 20-day realized-vol window (single-day variance share 46–63% for all six names once it enters the window), so **every IV-vs-realized verdict this run is WINDOW-CONTINGENT — there is no clean "IV rich" edge to claim.** The apparent premium (IV above realized by +8 to +17 pts on the thru-Nov-4 window) compresses to ~0–2 pts once today's returns enter the window. The only binary event in the window is **NVDA earnings Tue Nov 17 after close**, with the implied move widened to ±12.5% — premium into it is premium into a binary event: avoid. Rates offer no offsetting stress signal (2s10s +32 bp, flattening; SOFR–EFFR +6 bp), and crude fell >8% on de-escalation sentiment even as physical distillate hit a 23-year low — a sentiment unwind sitting on top of a tight physical market.

## 1. Earnings Event desk — COMPLETE

**Window:** Nov 5–19, 2026. **As-of:** ~13:30–14:00 PT, Thu Nov 5, 2026 (post-close).

| Symbol | Report date | Timing | Consensus EPS | Implied expected move | Last earnings-day reaction (verified) | Historical avg move |
|---|---|---|---|---|---|---|
| **NVDA** | **Tue Nov 17, 2026** | After close — results ~1:20 p.m. PT, call 2:00 p.m. PT / 5:00 p.m. ET | $2.49 (Nasdaq, 13 ests) | **±12.5%** (own Nov 20 straddle, mid-price) | **+8.7%** (Aug 27, 2026) | ±8.4% 10-yr avg — third-party, NOT independently recomputed |
| AAPL | Reported Mon Nov 2, 2026 (after close) | — | — | — | −1.9% on Nov 3 (first session after print) | UNVERIFIED |
| MSFT | Reported Wed Oct 28, 2026 (after close) | — | — | — | −0.2% on Oct 29 | UNVERIFIED |
| TSLA | Reported Wed Oct 21, 2026 (after close) | — | — | — | −3.1% on Oct 22 | UNVERIFIED |
| SPY / QQQ | None — ETFs, no earnings event | — | — | — | — | — |

- **NVDA is the window's only event (FACT).** Nasdaq earnings calendar API queried for every date Nov 5–19 and parsed in full: the only watchlist hit is NVDA on 2026-11-17, `time-after-hours`, consensus EPS $2.49, 13 estimates, fiscal quarter ending Oct/2026, last-year EPS $1.24. Date re-confirmed against NVIDIA's own Oct 28, 2026 release (call Tue Nov 17, 2 p.m. PT / 5 p.m. ET, fiscal Q3 2027 ended Oct 25, 2026, CFO written commentary ~1:20 p.m. PT). Stale third-party listings of Nov 18/25 are superseded by the company release.
- **Consensus discrepancy flagged (FACT).** Nasdaq shows $2.49 (13 ests); MarketBeat today shows $2.47 on revenue of $108.80B. The $0.02 gap is a vendor-consensus difference, not an error in either. Company revenue guidance is $108.0B ±2% (FACT, from the Aug 26 call, corroborated by multiple sources today).
- **Implied move — widened sharply in one day (FACT, own computation).** Yahoo v7 options chain pulled Nov 5 post-close (cookie+crumb handshake; underlying $181.60, prev close $200.13). Nov 20, 2026 expiry (first expiry after the print), $180-strike ATM straddle: call mid $12.43 + put mid $10.25 = **$22.68 → ±12.5%** of $181.60 (last-price basis $22.85 → ±12.6%). Yesterday the same straddle was $18.05 → ±9.0% at $200.13. Caveat (INFERENCE-grade method note): the straddle spans 15 calendar days, not the earnings day alone, so it overstates the pure earnings-day move. Yesterday's vendor stripped-method figure (±7.3%, EarningsWatcher) was **not** re-pulled today — treat as stale, not current.
- **Why the move widened — the day's selloff (FACT).** NVDA closed today at **$181.60, −$18.53 (−9.26%)** vs Nov 4 close $200.13, corroborated three ways (Yahoo v8 chart, Finnhub, stockanalysis.com; day's range $181.50–$196.24, open $196.07). Finnhub 5-day return −15.68%. Press coverage attributes the drop to a broad tech/AI-infrastructure-spending selloff (Invezz, Nov 5 — driver attribution is press-reported, not verified from primary sources). Per Dow Jones Market Data via Invezz, this would be NVDA's worst daily performance since April 2025 and its second-largest one-day market-cap loss on record — third-party, cited not recomputed. The market is de-risking into the Nov 17 print: the implied move widened ~3.5 points while the stock fell ~9%.
- **History (FACT, own computation, re-verified today from Yahoo v8 closes):** last report Aug 26, 2026 AMC → Aug 27 close $227.98 vs Aug 26 $209.66 = **+8.7%**. The 10-yr average ±8.4% is third-party (EarningsWatcher) and UNVERIFIED by this desk.
- **AAPL / MSFT / TSLA — all reported in late Oct, nothing in the window (FACT, per prior verified releases; no new dates appeared on the Nasdaq calendar Nov 5–19).** AAPL fiscal Q4 2026 (ended Sep 26): revenue $114.5B +12% YoY, EPS $2.10 +14% YoY, per its Nov 2 Form 8-K. Next reports est. late Jan 2027 (third-party, unconfirmed) — outside the window.
- **What would change the verdict:** an NVIDIA pre-announcement or date change, or a sharp repricing of the Nov 20 straddle before Nov 17. The straddle will mechanically cheapen as Nov 20 approaches if no new vol arrives — the ±12.5% is a today-only print.
- **Sources:** Nasdaq earnings calendar API https://api.nasdaq.com/api/calendar/earnings?date=2026-11-17 (and each date Nov 5–19, full-row parse); NVIDIA release https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873 ; Yahoo v7 options NVDA Nov 20 expiry + v8 chart closes (pulled Nov 5 post-close); Finnhub NVDA quote; https://stockanalysis.com/stocks/nvda/ ; MarketBeat NVDA calendar https://www.marketbeat.com/earnings/reports/2026-11-17-nvidia-co-stock/ ; Invezz Nov 5 selloff coverage https://invezz.com/news/2026/11/05/nvidia-stock-plunges-8-as-ai-spending-fears-and-financing-risks-mount/ ; ~/workspace/hedge-desk-research/nightly/2026-11-04-iv-inputs.json (as_of 2026-11-04T14:54:03−07:00).

## 2. Dividend Opportunity desk — COMPLETE

**As-of:** Thu 2026-11-05, ~13:40 PT (post-close). Prices are Nov 5, 2026 closes from Yahoo Finance v8 chart. Ex-dates from Nasdaq dividends calendar API (full sweep Nov 5–Dec 3, 2026) cross-checked against Nasdaq per-symbol dividend history and Yahoo v7 quote (cookie+crumb). Yields computed as annualized declared rate ÷ Nov 5 close, unless noted.

| Symbol | Ex-date | Pay date | Amount | Annualized | Yield* | Status |
|---|---|---|---|---|---|---|
| AAPL | Thu Nov 12, 2026 | Nov 16, 2026 | $0.27/qtr | $1.08 | 0.31% | Regular quarterly — **not** a raise (same $0.27 as May & Aug 2026) |
| MSFT | Thu Nov 19, 2026 | Dec 10, 2026 | $0.98/qtr | $3.92 | 0.73% fwd | **Raised rate** — first payment at the new $0.98 level (raise declared Sep 15, 2026) |
| SPY | — none in window | — | — | — | ~1.0% | Next distribution ex-date not in window (see below) |
| QQQ | — none in window | — | — | — | ~0.45–0.48% | Next distribution ex-date not in window (see below) |
| NVDA | — none in window | — | — | $1.00 | 0.55% | Next dividend not yet declared (see below) |
| TSLA | — none | — | — | — | 0.0% | Pays no dividend |

\* Yahoo's quoted yields differ slightly (MSFT 0.71%, NVDA 0.50%, QQQ 0.45%, AAPL 0.31%, SPY 1.0%) — likely a different reference price. Nov 5 was a sharp broad selloff (SPY −4.4%, QQQ −6.5% per Yahoo), which mechanically lifts all yields vs Nov 4.

- **MSFT — increase in effect (FACT).** Quarterly rate $0.91 → $0.98 (+7.7%), declared Sep 15, 2026; the Nov 19 ex-date is the first at the raised rate. **24 consecutive annual increases** (incl. the Sep 2026 raise; initiated 2003) per the standing count standard (`dividend-count-standard.md`); Nasdaq history confirms annual increases 2013–2026 and the 2026 raise. No raise has been announced since Sep 15, 2026, and the next raise is not due until ~Sep 2027 (INFERENCE from the annual September pattern).
- **AAPL — 2026 raise already banked (FACT).** $0.26 → $0.27 (+3.8%), declared Apr 30, 2026, first paid May 14, 2026. The Nov 12 dividend is the third payment at $0.27 — no new raise. **14 consecutive calendar years of increases, 2013–2026** — verified from Nasdaq's full dividend history (each year's maximum quarterly rate exceeded the prior year's, split-adjusted: 2014 $3.29 pre-split = $0.47 post-split < 2015 $0.52; 2020 $0.82 pre-split = $0.205 post-split < 2021 $0.22). No raise has been announced in 2026 beyond the April one; the next raise is not due until ~Apr/May 2027 (INFERENCE from the annual spring pattern).
- **NVDA — the desk's notable item: a 25× raise in May 2026 (FACT, Nasdaq history + corroborated by TokenPost, Oct 11, 2026).** Quarterly rate $0.01 → $0.25, declared May 20, 2026, first paid Jun 26, 2026; $0.25 confirmed again for the Sep 10, 2026 ex-date (paid Oct 1, 2026). Annualized $1.00 = 0.55% yield at the Nov 5 close — a cash-generation signal, not a yield story (INFERENCE). NVDA has raised in 2026, so no further raise is expected this year (INFERENCE).
- **Cuts / specials: none.** No watchlist name announced a cut, suspension, or special dividend in the window (FACT — Nasdaq calendar sweep + history show only the regular quarterly amounts above).

**Just beyond the window (context, not in the 4-week scope):**
- **SPY — next ex-date ~Fri Dec 18, 2026 (INFERENCE, not declared).** Third Friday of December per the fund's pattern; Wall Street Horizon, TipRanks, and DividendMax all point to Dec 18, 2026 (pay ~Jan 29, 2027). Q3 2026 distribution was $1.888834 (ex Sep 18, 2026, paid Oct 30, 2026). TTM distributions ~$7.58/share (FinanceCharts) → ~1.03% at the Nov 5 close. Nasdaq's calendar does not list SPY at all (NYSE Arca-listed) — amount and date remain UNVERIFIED until State Street declares.
- **QQQ — next ex-date ~Dec 21–22, 2026 (INFERENCE, not declared).** Prior 2026 ex-dates Mar 23, Jun 22, Sep 21; Dec 2025 ex-date was Dec 22. TTM distributions $3.09/share (0.75143 + 0.81349 + 0.73282 + 0.79408) → 0.48% trailing at the Nov 5 close. Not yet in Nasdaq's calendar (sweep through Dec 23 returned no QQQ row).
- **NVDA — next ex-date NOT YET DECLARED as of Nov 5 (FACT).** Nasdaq calendar sweep Dec 4–23 shows no NVDA row; TokenPost (Oct 11), HeyGoTrade, and Finbold all confirm no declaration yet. Pattern points to early December (prior Dec ex-dates: Dec 5, 2024; Dec 4, 2025); expected $0.25 if the rate holds (INFERENCE). **Conflict flagged:** DivTrkr lists "Dec 10, 2026 — Confirmed," contradicting Nasdaq's calendar and the other sources — treat Dec 10 as UNVERIFIED.

**What would change this:** AAPL: a new raise would be declared ~Apr 30, 2027 (spring pattern); the Nov 12 ex-date is fixed and confirmed. MSFT: the Nov 19 ex-date / Dec 10 payment at $0.98 is declared and fixed; next raise ~Sep 2027. NVDA/SPY/QQQ: any December declaration — watch Nasdaq calendar and issuer IR; the December dates above are pattern-based estimates, not declarations.

**Sources:** Nasdaq dividends calendar API, daily sweep Nov 5–Dec 3, 2026 (and Dec 4–23 for beyond-window check): `api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD`; Nasdaq per-symbol dividend history: `api.nasdaq.com/api/quote/{AAPL,MSFT,NVDA}/dividends?assetclass=stocks`; QQQ `assetclass=etf` (SPY history returns no rows — NYSE Arca-listed); Yahoo Finance v8 chart (Nov 5, 2026 closes) and v7 quote with cookie+crumb handshake; web cross-checks (Nov 5): wallstreethorizon.com SPY calendar; tipranks.com SPY dividends; dividendmax.com SPY/NVDA; tokenpost.com (NVDA raise, Oct 11, 2026); heygotrade.com; finbold.com; financecharts.com (SPY TTM $7.58); count standard: `~/workspace/hedge-desk-research/dividend-count-standard.md`.

## 3. Overnight Premium (IV) desk — COMPLETE

**As-of:** live Yahoo pull ~13:27–13:35 PT 2026-11-05 (post-close; 16:27+ ET). Stale-file realized vols as-of 2026-11-04T14:54 PT.

**Headline context first: 2026-11-05 was a sharp selloff day** — verified closes (Yahoo v8 chart, FACT): SPY 733.00 (−4.41% vs Nov 4 close 766.81), QQQ 647.05 (−6.49%), NVDA 181.60 (−9.26%), TSLA 343.69 (−10.77%), MSFT 535.93 (−3.57%), AAPL 344.17 (−1.53%). Every IV and realized-vol reading below is a post-crash print; treat accordingly.

**IV-inputs file status:** `~/workspace/hedge-desk-research/nightly/2026-11-04-iv-inputs.json`, as_of 2026-11-04T14:54:03−07:00 — within the 26h freshness guard, usable but **STALE-labeled** (yesterday's post-close data). Its `atm_iv` is null for all six symbols, so IV levels below come from a **labeled live Yahoo pull**, not the stale file.

### IV levels — LIVE Yahoo options chain (cookie+crumb), all six symbols fetched OK

Nearest unexpired expiry is **Fri 2026-11-06 (1 DTE)** — today's expiry was already dead at pull time (options die 16:00 ET), so the desk rolled to the next live expiry and labels the tenor. Second tenor is **Fri 2026-12-04 (29 DTE)**. ATM IV = mean of Yahoo-published call/put `impliedVolatility` at the strike nearest spot; all ATM quotes had live two-sided markets (no degenerate zero-bid marks).

| Symbol | Spot (Nov 5 close) | 1-DTE ATM IV, exp 2026-11-06 (call / put) | 29-DTE ATM IV, exp 2026-12-04 (call / put) |
|---|---|---|---|
| SPY | 733.00 | **17.9% — UNRELIABLE, see parity flag** (25.4% / 10.4%) | 21.5% (22.5% / 20.6%) |
| QQQ | 647.05 | **29.2% — UNRELIABLE, see parity flag** (44.0% / 14.5%) | 33.9% (35.5% / 32.4%) |
| AAPL | 344.17 | 32.1% (33.1% / 31.1%) | 28.2% (29.9% / 26.6%) |
| MSFT | 535.93 | 37.2% (37.5% / 37.0%) | 33.0% (34.0% / 32.0%) |
| NVDA | 181.60 | 69.9% (72.7% / 67.1%) | 63.0% (65.1% / 60.9%) |
| TSLA | 343.69 | 66.7% (68.7% / 64.7%) | 56.1% (57.7% / 54.5%) |

**Parity flag — SPY/QQQ 1-DTE (FACT, verified twice):** at the same ATM strike, call-minus-put mid is $3.21 for SPY (strike 733) vs put-call parity $0.12, and $7.30 for QQQ (strike 645) vs parity $2.15. The desk re-solved Black-Scholes IVs from the mids using the chart-verified close as spot (T = 1/252, r = 4%) and reproduced the split (SPY call IV 29.2% vs put 12.4%; QQQ 49.5% vs 17.3%), so this is not a Yahoo-solver quirk — the quoted marks themselves violate parity. **INFERENCE:** the 1-DTE index quotes are asynchronous/stale closing marks from a fast late-day selloff (they imply an underlying ~0.4% above the close for SPY, ~0.8% for QQQ). Per the CFA standard, deterministic parity outranks model output: **do not use the SPY/QQQ 1-DTE mean ATM IV as a clean level**; the 29-DTE prints (call-put gaps 2–3 pts, normal) are the usable tenor. Single-name 1-DTE call-put gaps (2–6 pts) are within normal skew/solver noise; their means are usable with that caution.

**Term structure (INFERENCE):** single names show an elevated front end on the crash day (1-DTE above 29-DTE: NVDA 69.9 vs 63.0, TSLA 66.7 vs 56.1, MSFT 37.2 vs 33.0, AAPL 32.1 vs 28.2). SPY/QQQ show the reverse only because their 1-DTE means are parity-distorted — no clean term-structure read there at 1 DTE.

### Realized vol — three vintages, labeled

| Symbol | STALE file (thru 2026-11-03, as-of Nov 4 14:54 PT) | FRESH recompute, convention (thru 2026-11-04 close) | PREVIEW incl. today's closed bar (thru 2026-11-05) |
|---|---|---|---|
| SPY | 11.5%, max-share 32.4% → CONTINGENT | 13.2%, max-share 25.8% → not contingent (biggest day Oct 30, −1.79%) | **20.7%, max-share 62.8% → CONTINGENT** (today −4.51% log) |
| QQQ | 23.3%, 28.4% → not contingent | 23.6%, 29.0% → not contingent (Oct 30, −3.54%) | **32.6%, 51.2% → CONTINGENT** (today −6.71% log) |
| AAPL | 17.8%, 16.2% → not contingent | 25.9%, 55.5% → **CONTINGENT** (Nov 4, +5.17%) | **26.2%, 54.3% → CONTINGENT** (Nov 4 +5.17% still dominates) |
| MSFT | 24.7%, 18.8% → not contingent | 33.9%, 49.9% → **CONTINGENT** (Nov 4, +6.47%) | **35.8%, 45.7% → CONTINGENT** (Nov 4 +6.47%) |
| NVDA | 33.5%, 22.4% → not contingent | 33.7%, 22.1% → not contingent (Oct 22, −4.50%) | **46.9%, 50.8% → CONTINGENT** (today −9.72% log) |
| TSLA | 37.3%, 25.6% → not contingent | 39.5%, 23.1% → not contingent (Oct 26, +5.08%) | **57.0%, 54.7% → CONTINGENT** (today −11.40% log) |

Notes: the stale file's SPY CONTINGENT flag is superseded on the fresh thru-Nov-4 window (25.8%, below the 30% screen) — but the preview window flips SPY back to CONTINGENT. The preview is labeled as such: the standing nightly convention excludes today's bar, so the Nov 6 file will show these preview values, not today's package. AAPL/MSFT's Nov 4 jumps (+5.17%/+6.47%) are reported as FACT with no causal claim attached.

### IV-vs-realized verdicts — all WINDOW-CONTINGENT, no clean verdict anywhere

- On the **convention window (thru Nov 4)**, 29-DTE IV exceeds realized for SPY (+8.4 pts), QQQ (+10.3), AAPL (+2.4), NVDA (+29.3), TSLA (+16.6); MSFT is flat (−0.8).
- On the **preview window (incl. today)**, those gaps nearly vanish: SPY +0.9, QQQ +1.3, AAPL +2.0, MSFT −2.8, TSLA −0.9. Only NVDA keeps a wide gap (+16.1) — and NVDA has earnings inside the window (below).
- **Verdict (INFERENCE): the apparent "IV rich" premium is a crash artifact — today's returns had not yet entered the realized window at pull time. Once they do (tomorrow's file), IV ≈ realized for five of six names. Do not read the thru-Nov-4 gap as a clean edge.** Every verdict is marked WINDOW-CONTINGENT on the preview basis (single-day variance share 46–63% for all six).

### Earnings in window — AVOID flag

- **NVDA reports 2026-11-17, after hours — VERIFIED via Nasdaq earnings calendar API** (EPS forecast $2.49, 13 estimates), confirming the stale file's date. It sits **inside the 29-DTE window** (12 days out) and inside any ~30-day premium horizon: premium sold into it is premium into a binary event — **avoid**. Its 63.0% 29-DTE IV is event-driven, not a clean richness signal.
- **No other watchlist name has earnings in the next 21 days** (Nasdaq calendar sweep 2026-11-05 → 2026-11-25, FACT). AAPL/MSFT/TSLA/SPY/QQQ: none.

### Elevated-IV flags

- **NVDA (69.9% 1-DTE / 63.0% 29-DTE) and TSLA (66.7% / 56.1%)** are elevated in absolute terms and vs realized — but both are post-crash prints on a −9%/−11% day, and NVDA's is earnings-loaded. No clean "sell premium" read; both are event/vol-regime prints.
- **SPY/QQQ:** 29-DTE IVs of 21.5%/33.9% are elevated vs their thru-Nov-4 realized (13.2%/23.6%) but, per the preview, roughly in line with realized once today enters the window. No elevated-IV flag survives the window-contingent screen.

### IV rank — UNVERIFIED

No free source of IV history was available to this desk, so **IV rank / IV percentile cannot be computed — UNVERIFIED, never guessed.** (The stale file carries no IV history either; its `atm_iv` is null for all six symbols.)

**What would change the verdicts:** tomorrow's IV-inputs file (realized incl. Nov 5) confirming the preview numbers; a second consecutive large down day would keep all six windows contingent and push realized above current IVs; NVDA's Nov 17 print resolving the earnings premium; a clean SPY/QQQ 1-DTE chain (call-put IVs within ~2 pts) would restore the front-end read.

**Method/sources:** live Yahoo v7 options (cookie+crumb via curl-seeded jar; crumb fetched 13:27 PT) + v8 chart closes; Nasdaq calendar API for earnings; stale file `~/workspace/hedge-desk-research/nightly/2026-11-04-iv-inputs.json` (as_of 2026-11-04T14:54:03-07:00, within the 26h guard, STALE-labeled, `atm_iv` null — supplemented by the live pull above).

## 4. Open Quant/AI Model Lab — COMPLETE

**Sweep window:** arXiv submissions Nov 2–4, 2026 (q-fin.PR/ST/RM/CP/MF/PM + keyword leg for "implied volatility / volatility forecasting / post-earnings drift / dividend forecast"). Ledger read first — last entry #206 (Li/Wang, seen Nov 3). **GitHub leg SKIPPED** per this run's ban on GitHub operations — no new-repo discovery, no repo re-checks, no repo contents/license verification. SSRN leg: no new in-window paper surfaced (only a 2014 IV-around-earnings paper and education/blog pieces).

**7 new candidates (#207–213), all scored with the repo scorer (run, not hand-computed). No TEST, no INTEGRATE — scorer max 57.** Appended to `~/workspace/hedge-desk-research/quant-lab-ledger.md` (standard work).

| # | Candidate | Venue/Date | Score | Disp. | First seen | Note |
|---|---|---|---|---|---|---|
| 207 | Zhang et al — "Hard to Fool: A Bounded LLM Research Loop for Quantitative Finance, and What Two Dozen Campaigns Found" (Autonomous Quant Researcher) | arXiv:2611.06607v1, 4 Nov 2026 (q-fin.CP/TR), abstract + abs page read at source | 57 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** LLM proposes, trusted code decides: strict declarative-JSON proposals, immutable chronological stores (discovery/validation/holdout opened exactly once), acceptance = conjunction of absolute gates (net P&L after costs, weekly-cluster bootstrap lower bound, elevated-cost survival, per-year stability, sample floors), hash-chained append-only ledger. Campaigns incl. 0DTE options from traded option bars, overnight SPX verticals, earnings options. Findings (source-reported, UNVERIFIED — full paper not read): most hypotheses fail; headline failure — an LLM survivor at Sharpe ~3 in discovery/validation fell to 0.26 on its single holdout use. **Code link on abs page: github.com/henryzhangpku/autonomous-quant-researcher (FACT — link present); repo contents + license NOT verified (GitHub leg banned) → reproducibility not established.** Directly relevant to the purged-WF / frozen-referee lane (#34, #69, #208). Scorer (run): 57 → WATCH. |
| 208 | "Can We Stop the Backtest Yet? Anytime-Valid Promotion Tests for Adaptive Financial Research Agents" (PROMOTE) | arXiv:2611.03384v1, 2 Nov 2026 (cs.AI/q-fin.ST), abstract read at source | 54 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** E-process / Ville-argument promotion protocol: each candidate gets predictable testing wealth at birth; cost-aware e-process from subsequent returns only; permits dependent candidates, adaptive births, indefinite monitoring. Claims (source-reported, UNVERIFIED — full paper not read): unadjusted tests cross in 94.5% of null paths vs 0.0% for PROMOTE (24 panel-rule hypotheses, 3,000 shared-sign null paths); 70.1% target power at a 15bp perturbation; market replay produces zero promotions after costs. **No author code link on abs page → reproducibility not established.** Complements #34 (frozen referee) and #69 (validation-time cost) — the desk's adaptive-research admission rule. Scorer (run): 54 → WATCH. |
| 209 | "Are LLM Research Agents Reliable Judges of Predictability? Evidence from Planted-Signal Worlds" | arXiv:2611.04070v1, 2 Nov 2026 (q-fin.ST), abstract read at source | 48 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** Agents scored as statistical tests in planted-signal worlds (3 frontier + 1 open-weight model). Findings (source-reported, UNVERIFIED): agents detect weak signals more often than pre-specified OOS tests mainly by accepting weaker evidence; claim predictability too often with no signal; miscalibrated probabilities; verdicts shift after a sentence about prior research. Prescription matches #34's frozen-referee theme: neutral brief, decision rule fixed outside the agent, sealed holdout. **No author code link on abs page → reproducibility not established.** Scorer (run): 48 → WATCH. |
| 210 | "Aggregate Calibration Can Mask Stress-State Undercoverage: Bounded-Memory Forecast Intervals under Recurrent Financial Stress" | arXiv:2611.04223v1, 3 Nov 2026 (stat.ME/q-fin.ST), abstract read at source | 48 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** Next-day financial range forecasting; recent-only FIFO calibration is near-nominal in aggregate but undercovers substantially during high-volatility states (ETF development panel + fixed stock panel); state-structured "Rare replay" yields lower high-VIX interval scores than matched Recent-n/Hybrid-n controls. **No author code link on abs page → reproducibility not established.** Premium-desk relevance: interval-calibration discipline for vol-regime reads — aggregate IV-vs-realized verdicts can conceal stress-state failure, same failure mode as the stale-jump screen's window-contingency. Scorer (run): 48 → WATCH. |
| 211 | "How market volatility responds to a preceding price trend: a lag-resolved measurement in cryptocurrencies and equities" | arXiv:2611.04533v1, 3 Nov 2026 (q-fin.ST), abstract read at source | 45 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** Minute-resolution vol response to preceding trend, 2020–2026: BTC/ETH asymmetry positive (leverage-effect sign), greatest at first measurable lag (20 min), decays to half by ~1.5h; T-odd (arrow-of-time) part detected for BTC/ETH. **Equities: NO detectable T-odd part at 20 min in the straight-line fit (FACT per abstract) — honest negative for the watchlist;** the S&P 500 ETF's return-variance correlation does display an arrow of time. Crypto-heavy sample; equities portion is 3 large US stocks + SPY. **No author code link on abs page → reproducibility not established.** Scorer (run): 45 → WATCH, band floor. |
| 212 | "Multidimensional Views Behind Target-Price Revisions: An LLM-Based Representation of Analyst Outlooks" | arXiv:2611.04119v1, 3 Nov 2026 (q-fin.CP), abstract read at source | 42 | ARCHIVE | 2026-11-05 | **New 2026-11-05 sweep.** LLM question-based outlook scores extracted from analyst research reports (earnings, valuation, industry dimensions); walk-forward: scores improve prediction of subsequent target-price revisions beyond revision momentum + sector; beat dictionary/FinBERT sentiment (source-reported, UNVERIFIED). Analyst reports are licensed data, not open → not replicable on desk data. **No author code link on abs page → reproducibility not established.** Scorer (run): 42 → ARCHIVE, below the 45 WATCH band. Read noted: structured-analyst-sentiment idea only. |
| 213 | CosmosAlpha: Multi-Relational Graph Search with Pareto-Guided Exploration for LLM-Driven Alpha Mining | arXiv:2611.04555v1, 3 Nov 2026 (q-fin.CP/cs.AI/cs.LG), abstract read at source | 45 | WATCH | 2026-11-05 | **New 2026-11-05 sweep.** Graph-based LLM factor mining: factors as multi-relational graph (lineage, expression similarity, exposure correlation); Graph Flow propagates search utilities; Pareto-guided selection over quality/fertility/diversity. Claims (source-reported, UNVERIFIED): best mean rank over 7 predictive/portfolio metrics on CSI 300 and CSI 500, beats its MCTS counterpart on every metric. **Code link in abstract: github.com/wzhmtldswz/CosmosAlpha (FACT — stated in abstract); repo contents + license NOT verified (GitHub leg banned).** China A-shares scope (CSI 300/500) — no US/watchlist transfer; complements #34/#57 factor-mining theme. Scorer (run): 45 → WATCH, band floor. |

**Triage exclusions (no ledger rows):** 2611.03592 (TSFM uncertainty calibration, Nov 2) — general time-series forecasting, marginal desk relevance; noted by the Nov 3 run, not scored (same call). 2611.06459 (explicit quantile representations, Nov 4), 2611.06126 (insurance reserving), 2611.06495 (pension management), 2611.05310 (sector rotation), 2611.05218 (wallet-identity order flow, crypto), 2611.04826 (portfolio learning from untrusted predictions) — theory, insurance/pension, or out-of-lane scope. Keyword leg surfaced no new in-window items: 2610.39636, 2610.33438, 2610.25671, 2610.25468 all already ledgered.

**Re-checks / follow-ups:** none done this run — GitHub leg banned, so no repo re-checks (incl. #9's newly linked code repo, still unverified) and no new-repo discovery. #9 follow-up stands: verify DomBBB/implied-volatility-trajectories contents + license via a permitted leg.

**Strongest lead:** #207 (Hard to Fool) — the only candidate with an author code link AND direct desk-lane fit (0DTE + earnings-options campaigns, holdout-once discipline). Sandbox the loop's gate logic on desk data once the repo is verifiable; its headline failure (Sharpe ~3 → 0.26 on holdout) is the desk's own overfitting caution in one number.

**Methodology cluster:** #207 + #208 + #209 form a coherent Nov 2–4 cluster with #34/#69: frozen referees, anytime-valid promotion, and agent-verdict reliability — the purged-WF lane's admission-control theme. Worth one combined read when a code release lands for any of them.

**Evidence labels:** all findings above are source-reported from arXiv abstracts/abs pages read at source unless marked FACT (link presence, scorer outputs, ledger state). No number is presented as verified beyond the scorer runs and the abstract text itself.

## 5. Weather / War / Logistics Futures Event desk — COMPLETE

**As-of:** Thu 2026-11-05, ~13:30 PT. **Sources checked:** EIA, USDA NASS/FAS, Reuters via wire carriers, Brownfield, Barchart, WSJ Market Talk, Baltic Exchange via Reuters.

### Catalyst triage

**A. Crude oil — war-risk premium unwinding into a physical distillate squeeze (dominant catalyst)**
- **FACT** — EIA Weekly Petroleum Status Report, released Wed Nov 4, 10:30 ET (week ended Oct 30): commercial crude drew 0.865 Mbbl to 409.8 Mbbl — a fifth straight weekly draw — vs. a Reuters poll expecting a +0.877 Mbbl build. Crude is 4% below its 5-yr seasonal average. Gasoline drew 0.222 Mbbl to 209.0 Mbbl (2% below avg); distillate drew 3.6 Mbbl to 99.3 Mbbl, its lowest since May 2003 and 13% below its 5-yr average. Total commercial petroleum drew 8.2 Mbbl. Refinery utilization rose 1.7 pp to 94.5%; Cushing +0.28 Mbbl to 27.3 Mbbl; SPR −0.399 Mbbl to 282.2 Mbbl; production 14.003 Mb/d; 4-wk product supplied 21.2 Mb/d, +4.2% y/y. Sources: EIA via Morningstar/Dow Jones, OilPrice, Reuters.
- **FACT** — Wed Nov 4 settle: Brent −8.7% to $94.62/bbl; WTI −8.3% to $88.12/bbl, lowest since Aug 31. Thu Nov 5 intraday snapshots conflict by timestamp (volatile, whipsawing): early Asia ~$93.8 Brent / ~$86.9 WTI (down ~1%); 06:30 ET $96.15 / $88.83 (up ~1.6% / 0.8%); 09:00 GMT $95.40 / $88.23. No verified Thu settle in hand at desk time — **UNVERIFIED** for the Thu close.
- **FACT** — Reported driver of the selloff: US midterm results (Democratic sweep) read as raising the odds of a diplomatic end to the US–Israeli war on Iran; JPMorgan estimated the global oil market returned to surplus in September, with more supply in October. Sources: Reuters via multiple carriers.
- **FACT (reported, single-source claims)** — IRGC Operational Statement No. 21 (Nov 5, via Fars/Anadolu) claims five oil tankers and a tugboat struck naval mines and caught fire in/near the Strait of Hormuz; UKMTO reported a tanker struck by two projectiles ~50 nm north of Qatar on Wed Nov 4, 23:20 GMT; a Qatari LNG carrier (Al Mayeda) was hit Oct 30. No vessel names or casualty figures released. **These are Iranian-state-media claims, not independently verified — treat the incident count as UNVERIFIED, the UKMTO projectile report as FACT (UKMTO is the reporting authority).** UKMTO recorded 35+ Hormuz incidents in October, the highest monthly volume since the conflict began in February.
- **FACT** — Eurasia Group (via Cornerstone Futures, Nov 5, 06:30 ET): cut odds of renewed US strikes on Iran to 60% (from 65%) **but also cut odds of a deal to 10% (from 20%)**, raising a continued standoff as the base case; says escalation would put Brent in a $110–125 band.
- **INFERENCE** — The market is pricing de-escalation hopes and a returning surplus faster than it is pricing physical Hormuz disruption: crude fell >8% on the same day tanker-attack claims escalated. That is a sentiment-driven premium unwind, not a fundamentals-clearing move — and it sits in tension with the tightest physical signal in the same EIA release (distillate at a 23-year low). What would change it: a confirmed Hormuz closure/suspension by a major shipper or insurer, or a verified US strike resumption.
- **FACT** — IEA, IEF and OPEC held an emergency meeting Nov 5 on maritime energy flows (Ports Europe, single source — **not independently corroborated**). OPEC SG Al Ghais reportedly said shipping + marine insurance now exceed 33% of the underlying value of crude in 2026.

**B. Russian diesel / refinery war — distillate-relevant**
- **FACT** — Ukraine hit the Ryazan refinery overnight Nov 4–5 (Reuters video analysis; second refinery hit this week after Yaroslavl on Mon), breaking a pause in strikes; Moscow has enforced fuel export bans since April. At least six Russian diesel cargoes signal US Atlantic coast voyages (Kpler/LSEG data); first US-bound arrival expected New York this weekend, but discharge is not guaranteed on sanctions/regulatory grounds. Source: Reuters, Nov 5.
- **INFERENCE** — If Russian diesel reaches the US Atlantic coast it would relieve the distillate tightness flagged above; if discharge is blocked, the 13%-below-average distillate deficit persists into heating season. Binary, watch the weekend arrival.

**C. Natural gas — storage build beats seasonal norm, price soft**
- **FACT** — EIA Natural Gas Storage Report, Thu Nov 5, 10:30 ET (week ended Oct 30): +77 Bcf injection to 3,801 Bcf, vs. WSJ survey +81 Bcf and 5-yr avg +61 Bcf. Storage is +54 Bcf (+1.4%) vs. 5-yr avg and −109 Bcf (−2.9%) y/y. Dec NYMEX natgas settled $2.947/MMBtu, −0.4% on the day. Sources: EIA via WSJ Market Talk, Barchart.
- **FACT** — European gas storage 74% full as of Nov 3 vs. 90% 5-yr seasonal average (Barchart). US Lower-48 dry gas production 112.5 Bcf/d Thu, +2.4% y/y (BNEF via Barchart).
- **INFERENCE** — Futures are pricing adequate US supply into winter (small surplus vs. 5-yr avg) with mild early-November weather extending the injection season; the European deficit is the offsetting upside risk. Next EIA STEO Tue Nov 10.

**D. Grains — harvest pressure into the Nov 10 WASDE**
- **FACT** — CBOT closes Thu Nov 5 (Brownfield): Dec corn $4.40, −4¼¢; Jan soybeans $11.88¼, −14¢ (2½-month low); Dec Chicago wheat $5.99¼, +¾¢; Dec meal $317.20, −$1.40; Dec soyoil 62.24, −129 pts. Wed closes were corn $4.44¼, soy $12.02¼, wheat $5.98½.
- **FACT** — USDA Crop Progress, released Mon Nov 2 (week ended Nov 1): corn 74% harvested (60% prior week; 77% 5-yr avg); soybeans 88% (79%; 84% avg); winter wheat 83% planted (84% avg), 65% emerged. Source: USDA NASS via DTN/Farm Progress.
- **FACT** — USDA Weekly Export Sales, released Thu Nov 5 (week ended Oct 29): corn 1.295 MMT (−1% w/w, +10% vs. 4-wk avg; YTD commitments 976m bu vs. 1.471B last year, −34%); soybeans 1.456 MMT (−44% w/w, −11% vs. avg; China 873.9k t; YTD 1.111B bu vs. 631.9m, +76%); wheat 538k t (−37% w/w, +16% vs. avg; YTD 443m bu vs. 617.5m). Flash sales: 1.73 MMT corn to Mexico (Nov 2); 167k t soybeans to Spain (Nov 4). Sources: USDA via Brownfield/Pro Farmer.
- **FACT** — Pre-WASDE positioning: StoneX (Nov 5) raised US corn to 16.203B bu / 183.1 bpa and soybeans to 4.725B bu / 55.0 bpa, vs. USDA Oct at 16.03B / 181.2 and 4.56B / 53.1. Reuters poll average points the other way on corn (15.961B bu, −73m vs. Oct USDA) and mildly higher on soy (4.597B bu). Next WASDE + Crop Production: **Tue Nov 10, 12:00 ET** (USDA schedule).
- **INFERENCE** — Grains are pricing a large, fast-harvested crop with soft cash basis; the Nov 10 WASDE is the clearing event — StoneX vs. Reuters-poll disagreement on corn direction (±~240m bu spread) means a two-sided surprise risk, not a one-way lean.

**E. Freight — dry bulk firming on large vessels, not broad-based**
- **FACT** — Baltic Dry Index Thu Nov 5: 2,740, +1.7% (+46 pts), highest since Oct 13; Capesize 4,191 (+2.3%, ~$34,510/day); Panamax 1,956 (+3.3%, $17,603/day); Supramax 1,824 (−0.6%, lowest since Oct 12). Wed: BDI 2,694 (+4.0%). Sources: Baltic Exchange via Reuters/Baird Maritime. Iron ore rose a second straight session to a one-month high on Chinese equities/steel margins.
- **INFERENCE** — The BDI move is an iron-ore/China restocking story in large vessels, not a broad freight or grain-shipping signal — Panamax (grain/coal) firming is the only leg directly relevant to ag logistics, and Supramax weakness argues against reading the headline as general tightness.

### Futures-curve read (what curves appear to be pricing)
- **FACT** — Brent–WTI spread at Wed settle: ~$6.50/bbl ($94.62 vs. $88.12).
- **INFERENCE** — Energy: the curve is pricing war-premium removal + surplus, with physical tightness confined to the distillate leg — crude soft, distillate scarce. Natgas: pricing ample US winter supply. Grains: pricing harvest glut ahead of Nov 10 WASDE.
- **UNVERIFIED** — Full term-structure shape (contango/backwardation) for crude, natgas, and grains: no verified curve data retrieved this run; not asserted.

### Watchlist relevance (value lens)
- **INFERENCE** — A sustained crude break below ~$90 WTI / ~$95 Brent is a disinflationary input-cost tailwind for the broad market (SPY/QQQ) and a margin tailwind for transport-heavy names, but the driver is geopolitical sentiment, not durable supply growth — treat as fragile, reversible on one verified Hormuz escalation. No direct watchlist earnings/exposure channel identified today; TSLA energy exposure is second-order. Grain softness is a food-input cost tailwind, immaterial to watchlist names.
- **Nothing material** on USDA/EIA schedule disruption: both agencies released on schedule this week (EIA petroleum Nov 4, EIA natgas Nov 5, USDA Crop Progress Nov 2, Export Sales Nov 5) — consistent with the standing no-shutdown rule; no "data blackout" framing applies.

### Calendar — next catalysts
| Date | Event |
|---|---|
| Tue Nov 10, 12:00 ET | USDA WASDE + Crop Production (Nov) |
| Tue Nov 10 | EIA Short-Term Energy Outlook (Nov) |
| Wed Nov 11, 10:30 ET | EIA Weekly Petroleum Status Report (w/e Nov 6) |
| Thu Nov 12, 10:30 ET | EIA Natural Gas Storage (weekly) |
| Weekend Nov 7–8 | First Russian diesel cargo due New York — discharge yes/no |
| Sun Nov 29 | OPEC+ meeting (output held unchanged Nov 1) |

**Sources:** EIA via Morningstar/Dow Jones Nov 4, OilPrice Nov 4, Reuters/BOE Report Nov 4, WSJ Market Talk Nov 5, Barchart Nov 5, Brownfield Ag News Nov 5, USDA NASS via DTN/Farm Progress Nov 2, USDA FAS via Brownfield/Pro Farmer Nov 5, StoneX via Precision Feed Nov 5, Reuters via KTWB Nov 5, Cornerstone Futures Nov 5, Baltic Exchange via Baird Maritime/Reuters Nov 5, Ports Europe Nov 5, UKMTO via Al Jazeera/Occasional Digest Nov 5.

**Desk open verifications:** Thu crude settle (UNVERIFIED at desk time); IRGC Hormuz tanker count (UNVERIFIED — single-source state-media claim); IEA/IEF/OPEC meeting details (single source).

## 6. Box / Parity Observer — COMPLETE

**One material item — index methodology (not a parity violation):**

- **FACT:** S&P Dow Jones Indices announced on Oct 23, 2026 a revision to its U.S. growth/value classification rules, effective at the annual reconstitution before the open on **Dec 21, 2026**; pro-forma files from Dec 4. Growth drops 12-month price momentum (keeps 3-yr EPS-change and sales-per-share growth); value replaces book-to-price with an intangibles-adjusted measure, blends trailing + forward earnings-to-price, and adds free-cash-flow-to-price (excluded for real estate, banks, insurers and certain financials). Applies to S&P 500 / MidCap 400 / SmallCap 600 / Composite 1500 style indices. Sources: S&P DJI release Oct 23 via CNBC-TV18 / Bloomberg, https://www.tradingview.com/news/cnbctv:efc13bb28094b:0/ and https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/
- **INFERENCE:** No change to SPX level calculation or to put-call/box parity math — this is a style-classification change, not a pricing-identity change. Watchlist relevance is indirect only: growth-heavy AAPL / MSFT / NVDA could see style-index weight shifts at the Dec 21 reconstitution. **UNVERIFIED (secondary figure):** Bloomberg Intelligence's James Seyffart estimated ≥$375bn in passive funds tied to the affected gauges — reported by Bloomberg/briefs.co, not verified against a primary S&P DJI or Bloomberg source.
- **FACT:** FTSE Russell is separately consulting on its growth/value 50/50 split, consultation closing Dec 11, 2026 (per Bloomberg summary, https://headlinesbriefing.com/market/bloomberg-markets/sp-overhauls-growth-and-value-stock-rules-c93396af). No outcome yet.

**Parity / box spreads — nothing new in the window:**
- **FACT:** No new published put-call parity violation or box-spread arbitrage analysis for U.S. watchlist underlyings in the last ~2 weeks. The recent papers surfacing in search are older: Shin, "The P behind Q" (May 26, 2026, SPX/RUT carry-gap wedge, https://arxiv.org/pdf/2605.12250v5.pdf) and Jarrow–Kwok, "Measuring Bubbles via Put-Call Disparity" (May 2026, https://clubgestionriesgos.org/wp-content/uploads/Jarrow-Kwok-2026.pdf). A Nov 2026 Nifty parity blog is Indian-market educational content, not a U.S. study. No new CBOE SPX methodology change in the window (the Buffer IC consultation result is Feb 2026).
- **FACT (context, outside window):** CBOE's record SPX box-spread outstanding notional of $146bn (mid-Sep 2026, reported Sep 24) and the Oct 2026 IBKR/Cboe box-spread webinar are background only — no new violation or pricing dislocation reported from them. Deterministic put-call/box parity stands unchallenged for the watchlist this run: no actionable mispricing identified.

**Bottom line:** No parity violation to act on. One watch item: S&P style-index reconstitution Dec 21 (pro-forma Dec 4) — check watchlist growth/value weights then.

## 7. Bonds & Rates desk — COMPLETE

**Status: OK — REAL_FRED_RATES mode.** Source: repo module `hedge_desk.rates_desk.rates_environment()`, FRED public CSV (HTTP 200). Module run 2026-11-05 ~13:27 PT; latest observations dated **2026-11-04**. All figures below are FACT from that module output.

### Levels (as of 2026-11-04)
| Series | Level | Date |
|---|---|---|
| Fed funds effective rate (DFF / EFFR) | **3.88%** | 2026-11-04 |
| 2Y Treasury (DGS2) | **4.58%** | 2026-11-04 |
| 10Y Treasury (DGS10) | **4.90%** | 2026-11-04 |
| SOFR | **3.94%** | 2026-11-04 |
| OBFR | **3.88%** | 2026-11-04 |

### Curve: 2s10s slope = +32 bp, upward sloping
- **FACT:** 10Y − 2Y = 4.90 − 4.58 = **+32 bp** (module `spread_10y_2y_points: 32.00`, `curve_shape: UPWARD_SLOPING`).
- **FACT (direction):** The slope has **flattened** over the 60-day window — 41 bp on 2026-09-08 → 47 bp peak early Oct (5.31 − 4.84 on 2026-10-05) → 38 bp on 2026-10-30 → **32 bp on 2026-11-04**. Both ends fell over the last month, but the 10Y fell more (5.31% → 4.90%, −41 bp) than the 2Y (4.84% → 4.58%, −26 bp). Day-over-day Nov 3 → Nov 4: 2Y 4.61 → 4.58, 10Y 4.95 → 4.90 — flattening continued into the latest print.
- **FACT:** Fed funds effective rate changed 0.25 pp over the 60-day window per the module (magnitude as reported; module does not sign the change).

### Funding stress: none evident
- **FACT:** SOFR − EFFR = 3.94 − 3.88 = **+6 bp**; OBFR = EFFR (3.88%).
- **INFERENCE:** A 6 bp SOFR–EFFR spread is narrow — no funding-stress signal. Overnight funding is functioning normally; nothing here argues for a stress premium in short-dated options.

### Premium-pricing read (INFERENCE)
- Long rates have eased meaningfully from the early-October peak (10Y −41 bp since Oct 5), which modestly relieves discount-rate pressure on growth multiples — a mild tailwind for the growth-heavy watchlist names (NVDA, TSLA, MSFT, QQQ) versus a month ago.
- But the absolute level still bites: a 4.90% 10Y is a high discount rate, so premium on long-dated growth exposure should still be priced with a margin-of-safety lens — no case here for paying up for duration.
- The flattening 2s10s (+32 bp and narrowing) says the market is pricing less term premium, not a growth re-acceleration; nothing in the curve argues for chasing upside vol on the watchlist.
- **What would change this read:** a 10Y break back above ~5.25% (early-Oct highs) would re-tighten the discount-rate headwind; a 2s10s inversion would flip the read to recession-risk pricing.

**What would change the desk's verdicts:** any FRED revision to the Nov 4 prints, or a fresh FOMC/statement move shifting the front end.

## Desk status summary

| Desk | Status |
|---|---|
| 1. Earnings Event | COMPLETE — NVDA Nov 17 only event; implied ±12.5% |
| 2. Dividend Opportunity | COMPLETE — AAPL ex Nov 12, MSFT ex Nov 19 at raised $0.98 |
| 3. Overnight Premium (IV) | COMPLETE — all verdicts WINDOW-CONTINGENT; IV rank UNVERIFIED |
| 4. Open Quant/AI Model Lab | COMPLETE — 7 new candidates #207–213 appended to ledger |
| 5. Futures Event | COMPLETE — crude unwind vs distillate squeeze; WASDE Nov 10 |
| 6. Box/Parity Observer | COMPLETE — no violation; S&P style revision Dec 21 watch item |
| 7. Bonds & Rates | COMPLETE — REAL_FRED_RATES; 2s10s +32 bp flattening |

No desk failed. No desk produced no output. IV-inputs file `2026-11-04-iv-inputs.json` (as_of 2026-11-04T14:54:03−07:00) was within the 26h guard; `atm_iv` null for all symbols, supplemented by a labeled live Yahoo pull. No GitHub operations performed.

## 3–5 most decision-relevant items

1. **Crash day reprices everything — no clean IV edge.** SPY −4.41%, QQQ −6.49%, NVDA −9.26%, TSLA −10.77% on Nov 5. Once today's returns enter the 20-day realized window, realized vol jumps to ~21% (SPY) / ~33% (QQQ) / ~47% (NVDA) / ~57% (TSLA) and every IV-vs-realized verdict is WINDOW-CONTINGENT. The thru-Nov-4 "IV rich" gap (+8 to +17 pts) compresses to ~0–2 pts — it was the crash not yet being in the window.
2. **NVDA earnings Tue Nov 17 after close — the window's only binary event.** Consensus EPS $2.49; implied move ±12.5% (Nov 20 straddle, up from ±9.0% yesterday as the stock fell 9.26% to $181.60). Premium into it is premium into a binary event: avoid. Its 63.0% 29-DTE IV is event premium, not a richness signal.
3. **Crude fell >8% on de-escalation sentiment while distillate hit a 23-year low.** EIA Nov 4: crude drew 0.865 Mbbl (vs +0.877 expected build), distillate 99.3 Mbbl — lowest since May 2003, 13% below 5-yr avg. Sentiment unwind, not a fundamentals-clearing move; fragile and reversible on one verified Hormuz escalation (IRGC tanker claims UNVERIFIED). Next clearing events: WASDE + EIA STEO Tue Nov 10.
4. **Rates: no stress, mild relief, still high.** EFFR 3.88%, 10Y 4.90%, 2Y 4.58%, 2s10s +32 bp and flattening from a 47 bp early-Oct peak; SOFR–EFFR +6 bp (no funding stress). Long rates −41 bp since Oct 5 modestly relieves discount-rate pressure on growth names, but 4.90% is still a high discount rate — no case for paying up for duration.
5. **Dividends: AAPL ex-div Thu Nov 12 ($0.27, no raise); MSFT ex-div Thu Nov 19 at the raised $0.98 (24th consecutive annual increase).** NVDA's next ex-date not yet declared (DivTrkr's "Dec 10 — Confirmed" contradicts Nasdaq's calendar; treat as UNVERIFIED). SPY/QQQ December distributions are pattern-based estimates, not declarations.
