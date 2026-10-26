# Hedge-Desk Daily Research Package — Monday 2026-10-26

**Run:** 13:30 PT (16:30 ET). Premium-desk live quotes are today's 16:00 ET close; rates figures are FRED prints through Fri Oct 23 (normal weekend publication lag).
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Standing:** paper-only research. No Risk of Ruin work, no trade authorization, no synthetic data. Every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**Desk status:** all 7 desks delivered. No desk FAILED. Two cross-desk items are resolved or flagged below — MSFT implied move RESOLVED; NVDA earnings date remains UNRESOLVED (three-way tracker split).

---

## 5 most decision-relevant items (synthesized, not stapled)

1. **[FACT] Wednesday Oct 28 is a stacked binary session — FOMC decision 2:00 p.m. ET + MSFT earnings after close.** MSFT's ±5.26% implied move is a joint macro+earnings price, not a pure earnings read. Premium into MSFT's front expiry is event premium — avoid per the Premium desk's standing rule.
2. **[FACT, RESOLVED] MSFT implied move settles at ~5.3%.** Today's fresh own-calculation (±5.26%, Oct 30-expiry ATM straddle $28.00 ÷ $532.60) matches the Oct 23 own-calculation (5.28%). The stale 7.57% secondary read from Oct 18 is retired. Yesterday's package left this UNRESOLVED; it is resolved today.
3. **[FACT] Rates: 10Y at 5.00%, 2Y at 4.69%, 2s10s +31bp — bear-flattening.** The curve compressed 16bp over 60 days (47bp on Aug 27 → 31bp on Oct 23) because the 2Y rose more (+49bp) than the 10Y (+33bp). Funding stress: none visible (SOFR−EFFR +4bp). Elevated long rates keep the discount-rate headwind on growth multiples in place into Wednesday's FOMC.
4. **[FACT] Energy shock is the live macro channel to SPY/QQQ.** Brent held ~$115 Monday after Friday's $116.72 settle; Hormuz transit readings are sharply reduced but methodology-conflicted (see Futures desk — reported as a range, not resolved). Distillates remain the tight spot (9% below the 5-year average) into heating season. Next EIA print is also Wednesday, 10:30 a.m. ET.
5. **[FACT] Only one declared dividend event in the 4-week window: MSFT, ex Nov 19, $0.98 (raised).** AAPL is the live watch: a Nov 2 earnings declaration would likely create a second in-window ex-date — re-check Nov 3. NVDA's earnings date is UNVERIFIED (see conflict note); do not use Nov 17, 18, or 25 as confirmed.

---

## 1. Earnings Event desk

| Ticker | Event | Timing | Options-implied expected move | Historical avg earnings-day move (own calc, last 8 qtrs) |
|---|---|---|---|---|
| MSFT — Q1 FY27 | Wed, Oct 28, 2026 | After close; webcast 5:30 p.m. ET | **±5.26%** — Oct 30-expiry ATM straddle (532.5 strike) mid $28.00 ÷ $532.60 | **4.04% avg / 3.44% median** (absolute, next-session close vs release-day close) |
| AAPL — Q4 FY26 | Mon, Nov 2, 2026 | After close; call 5:00 p.m. ET | **±4.26%** (Nov 4 expiry) / **±4.73%** (Nov 6 expiry) — 345-strike ATM straddles $14.65 / $16.27 ÷ $343.91 | **1.98% avg / 1.01% median** (absolute, same method) |
| TSLA | Already reported — Wed, Oct 21, 2026, after close | — | — | — |
| NVDA | Outside window — date NOT company-confirmed | After close (expected) | — | — |
| SPY, QQQ | No earnings — ETFs, by structure | — | — | — |

**Evidence / labels:**
- MSFT date + after-close timing: FACT — Nasdaq earnings-calendar API, `?date=2026-10-28` (time-after-hours, consensus EPS $4.71, 14 estimates, vs $4.13 last year), corroborated by Microsoft's own Oct 7, 2026 release.
- AAPL date + after-close timing: FACT — Nasdaq API, `?date=2026-11-02` (time-after-hours, consensus EPS $2.00, 8 estimates, vs $1.85 last year), corroborated by Apple's IR calendar via secondary reports.
- MSFT implied move: FACT (own calculation, this run) — 5.26%, effectively identical to Oct 23's 5.28%. The 7.57% Oct 18 secondary read is superseded (stale chain and/or different strike/expiry selection). What would reopen it: a fresh chain recomputation diverging materially.
- MSFT caveat — INFERENCE: the Oct 30 straddle embeds BOTH the Oct 28 FOMC decision (2:00 p.m. ET, same day, pre-earnings) AND earnings. Do not attribute the full 5.26% to earnings alone, nor the Oct 29 session move to earnings alone.
- Historical moves: FACT (own calculation, method stated) — Yahoo v8 chart unadjusted closes; move = next trading session's close ÷ release-day close − 1, for after-close releases. MSFT 8 quarters: −2.92%, +3.95%, +7.63%, −6.18%, −6.05%, −1.08%, +1.82%, −2.69%. AAPL 8 quarters: −0.38%, −2.50%, −3.74%, −0.67%, −1.33%, +0.69%, +5.98%, −0.54%. Limitation: close-to-close only, small sample — a baseline, not a prediction. This replaces yesterday's UNVERIFIED marks for both names.
- Reading for both names — INFERENCE: options price more event vol than recent realized earnings moves (MSFT 5.26% implied vs 4.04% historical avg; AAPL ~4.3–4.7% implied vs 1.98% historical avg), with the small-sample caveat.
- NVDA date: FACT that it is unconfirmed; UNVERIFIED as to which tracker date is right — see conflict note below. Company guidance cited secondhand (revenue $108.0B ±2%, gross margin 74.0% ±50bp) is UNVERIFIED as company guidance — not read from an Nvidia release.
- TSLA: FACT — reported Wed Oct 21, 2026, after close (Tesla IR table). Next date outside window, UNVERIFIED.

**CFA note:** neither in-window release exists yet, so no statement teardown is possible today. At release time, apply the reading order: guidance vs. consensus first, then GAAP income statement (vs. headline adjusted figure), cash flow (OCF vs. net income, capex, buybacks vs. issuance), segment margins, balance-sheet deltas, call transcript last.

**Sources:** Nasdaq earnings-calendar API (`api.nasdaq.com/api/calendar/earnings?date=2026-10-28` and `?date=2026-11-02`, pulled this run); https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/ ; Yahoo Finance v7 options chains and v8 charts (cookie+crumb, pulled this run); https://www.cmelitegroup.com/knowledge-hub/nvidia-earnings-date/ ; https://www.marketbeat.com/stocks/NASDAQ/NVDA/earnings/ ; https://www.tipranks.com/stocks/ch:nvda/earnings

**What would change it:** a company-issued date change (MSFT/AAPL/NVDA); a fresh chain recomputation diverging from 5.26% / 4.26–4.73%; an Nvidia company announcement settling its date.

---

## 2. Dividend Opportunity desk

| Symbol | Ex-date | Amount | Pay date | Status |
|---|---|---|---|---|
| MSFT | **2026-11-19** | **$0.98/qtr** | 2026-12-10 | FACT — declared, INCREASE |
| AAPL | None declared in window | — | — | WATCH — Nov 2 declaration could create one |
| NVDA | None in window | — | — | Next ex expected early Dec (UNVERIFIED) |
| SPY | None in window | — | — | Next ex expected ~Dec 18 (UNVERIFIED) |
| QQQ | None in window | — | — | Next ex expected ~Dec 21 (UNVERIFIED) |
| TSLA | None — pays no dividend | — | — | FACT |

**Evidence / labels:**
- MSFT: FACT — Nasdaq dividends calendar + per-symbol history, pulled Oct 26. Declared Sep 15, 2026; $0.91 → $0.98 (+7.7%, recomputed: 0.07 ÷ 0.91 = 7.69%). Consecutive-increase count: **24 consecutive annual increases (incl. the Sep 2026 raise)**, per the standing standard in `~/workspace/hedge-desk-research/dividend-count-standard.md` (count increments on announcement date). No cut, no special. Note: the desk reported a record date of Nov 19; yesterday's package carried only ex-date and pay-date, and the parent's Nasdaq re-check this run did not corroborate a record date — the package asserts ex-date and pay-date only, and the record date is NOT carried as verified.
- AAPL: FACT — no declared ex-date in the window (Nasdaq calendar scan Oct 26–Nov 23; last ex Aug 10, 2026, $0.27, declared Jul 30, 2026, paid Aug 13, 2026). Watch trigger: AAPL reports Nov 2 after close and historically declares its quarterly dividend with earnings (2025 pattern: declaration Oct 30 → ex Nov 10). INFERENCE: if declared Nov 2, the ex-date will likely land inside this window (early–mid Nov) — but date and amount are UNVERIFIED until declared. Last raise was declared Apr 30, 2026 ($0.26 → $0.27, ex May 11), so a November raise would break Apple's spring-raise pattern — no increase expected, but that is INFERENCE, not fact. Re-check the Nasdaq calendar the morning of Nov 3.
- NVDA: FACT — no declared ex-date in the window (last ex Sep 10, 2026, $0.25, paid Oct 1, 2026). Prior increase: board raised the quarterly dividend $0.01 → $0.25 on May 20, 2026 (GlobeNewswire release) — FACT. The 25× headline is a post-split artifact: pre-10:1-split (Jun 2024) the payout was $0.10/share, so the raise roughly restores the pre-split level — INFERENCE from split arithmetic, stated so the desk does not misread NVDA as a 25× dividend-growth story. INFERENCE: next declaration expected with NVDA's earnings (~mid/late Nov), ex-date likely early December — outside this window, UNVERIFIED until declared. A third-party "estimated Dec 25 payment" circulating online is an unconfirmed estimate — not used.
- SPY: FACT — no declared ex-date in the window. Last ex Sep 18, 2026, $1.8888, payable Oct 30, 2026 (a payment date, not an ex-date — no dividend event remains in the window). INFERENCE: next quarterly ex expected in December (~Dec 18 area) — not yet declared, UNVERIFIED.
- QQQ: FACT — no declared ex-date in the window. Last ex Sep 21, 2026, $0.75143, paid Oct 8, 2026; prior quarters Jun 22 ($0.81349), Mar 23 ($0.73282). ETF distributions vary quarter to quarter; no "increase/cut" framing applies. INFERENCE: next quarterly ex expected December (~Dec 21 area) — not declared, UNVERIFIED.
- TSLA: FACT — pays no dividend (Nasdaq: ex-date/yield/annualized all N/A, zero dividend rows).
- Cuts / specials: none announced for any watchlist name in the sources checked — a checked-negative, not an issuer filing review.

**Source failures (classified):** Yahoo v8 chart `events=div` returned 0 dividend events for all six symbols despite valid price metadata — classified as a DEGRADED route, not a data absence; Nasdaq calendar + per-symbol endpoints succeeded, so no coverage gap. Nasdaq SPY dividends endpoint returns empty rows (SPY is NYSE-listed) — a DEAD END for that route, covered by the calendar scan plus secondary history sites for the last ex-date.

**Sources:** Nasdaq dividends calendar API, day-by-day scan Oct 26–Nov 23, 2026 (`api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD` — only hit: MSFT Nov 19); Nasdaq per-symbol dividends (`api.nasdaq.com/api/quote/{AAPL,MSFT,NVDA,QQQ}/dividends`); `~/workspace/hedge-desk-research/dividend-count-standard.md`; https://www.digrin.com/stocks/detail/SPY/ ; https://www.macrumors.com/2026/10/06/apple-q4-2026-earnings-nov-2/

**What would change it:** AAPL's Nov 2 declaration (could add an in-window ex-date at $0.27 or, unexpectedly, a new amount); NVDA's earnings declaration; any Nasdaq calendar row appearing for SPY/QQQ before Nov 23.

---

## 3. Overnight Premium desk (IV)

**Freshness guard: PASS (with label).** IV-inputs file `~/workspace/hedge-desk-research/nightly/2026-10-25-iv-inputs.json`, `as_of` **2026-10-25T13:54:03−07:00** — age ~23.6h at run time, inside the 26h guard. It is a Friday-close snapshot (realized window ends Fri Oct 23), NOT today's data — levels below are superseded by today's live pull where they differ. The file's own `_failover` entry notes the repo's options failover was unavailable and a legacy Yahoo-only pull was used.

**Live pull (labeled supplement):** Yahoo Finance v7 options, cookie+crumb handshake (curl-seeded jar → query1 `/v1/test/getcrumb` → `?crumb=`; UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`). Succeeded for all 6 symbols; no fallback needed. Note: `fc.yahoo.com` returned HTTP 404 on the seed request but the crumb still issued and all chain pulls returned 200 — classified as a non-blocking quirk, not a failure. Quote time for all six: **2026-10-26 16:00 ET (today's close)**.

**IV snapshot — live (today's close) vs Friday file:**

| Symbol | Live price (close) | Live next expiry / ATM IV (call / put) | Fri file ATM IV (1-DTE Oct 26 exp.) | 20d realized (file, thru Oct 23) | IV − realized, live basis |
|---|---|---|---|---|---|
| SPY | 765.37 | Oct 27: 8.2% / 9.1% | 13.57% | 9.70% | ≈ −1.0pp (avg 8.7% vs 9.7%) |
| QQQ | 712.20 | Oct 27: 15.4% / 15.0% | 23.91% | 18.78% | ≈ −3.6pp |
| AAPL | 343.91 | Oct 28: 21.9% / 20.6% | 20.09% | 16.56% | ≈ +4.7pp |
| MSFT | 532.60 | Oct 30: **56.9% / 55.7%** | 22.71% | 19.50% | ≈ +36.7pp — earnings-inflated, see below |
| NVDA | 216.00 | Oct 28: 33.0% / 31.8% | 36.24% | 29.38% | ≈ +3.0pp |
| TSLA | 391.62 | Oct 28: 35.5% / 35.6% | 36.36% | 34.00% | ≈ +1.5pp |

**0-DTE handling (INFERENCE, desk sanity check):** Oct 26-expiry quotes are discarded as vol points — expiry-day IVs collapse to artifacts (e.g., SPY ATM call IV 0.001% vs put 2.28%). The call/put divergence there is expiry-day quote decay, NOT a put-call parity violation. Term structure above uses the next expiry instead, where ATM call/put IVs agree within ~1–2pp, consistent with parity sanity (FACT on the checked points).

**Elevated-IV flags:**
- **MSFT — ELEVATED, event-driven (FACT: 56–57% ATM IV on the Oct 30 expiry; INFERENCE: elevation is the earnings premium, not a mispricing).** Oct 28 earnings sit inside the Oct 30 expiry window, so front IV is inflated by construction. Per the standing rule: **premium into this binary = avoid.** Do not read 56% as "rich" vs the 19.5% realized — the two are not comparable across an earnings event.
- **No other clean elevated flag.** AAPL (+4.7pp) and NVDA (+3.0pp) sit modestly above realized, but both are WINDOW-CONTINGENT (below), so no clean "elevated" verdict is issued for them. SPY, QQQ, TSLA are at or below realized on the live basis.

**Window-contingent flags (stale-jump screen, from the file — FACT):**

| Symbol | Max single-day variance share | Window-contingent? | Effect on verdict |
|---|---|---|---|
| SPY | 20.9% | No | IV-vs-realized verdict stands as clean on its window |
| QQQ | 32.0% | **Yes** | Live "IV below realized" verdict is WINDOW-CONTINGENT |
| AAPL | 36.4% | **Yes** | Live "IV above realized" verdict is WINDOW-CONTINGENT |
| MSFT | 20.1% | No | Clean window — but live IV is earnings-dominated, see above |
| NVDA | 31.0% | **Yes** | Live "IV modestly above realized" verdict is WINDOW-CONTINGENT |
| TSLA | 24.8% | No | "IV roughly in line with realized" stands as clean |

Friday-file-basis verdicts (for the record, superseded by live): SPY +3.9pp, QQQ +5.1pp (contingent), AAPL +3.5pp (contingent), MSFT +3.2pp, NVDA +6.9pp (contingent), TSLA +2.4pp — all IV above realized on Friday's close, a pattern today's live pull did NOT repeat for SPY/QQQ (INFERENCE: weekend/overnight vol compression, or Friday's 1-DTE expiry effect; either way the Friday premium is gone).

**Earnings inside the window (FACT unless noted):**
- MSFT — Wed Oct 28, after close. Confirmed by BOTH the iv-inputs file and the live Yahoo quote timestamp. Inside the Oct 30 expiry and every front window. **Avoid premium into this binary.**
- AAPL — Mon Nov 2. File and live Yahoo agree. Outside the Oct 28/30 front expiries; inside the November monthly window — front-week IV is NOT earnings-inflated.
- NVDA — DATE CONFLICT, UNVERIFIED. Live Yahoo quote timestamp says Nov 17; the iv-inputs file says Nov 18; the Earnings desk's tracker sweep adds Nov 25. See conflict note below. Either way outside the front window (Oct 28 expiry IV ~32% is non-event vol).
- TSLA — no upcoming date in the file; last earnings Oct 21 (past, per live Yahoo timestamp). No earnings inside the front window (next date UNVERIFIED — no source in hand gives it; not guessed).
- SPY/QQQ: no earnings (index ETFs), as expected.

**IV rank: UNVERIFIED.** No IV-rank percentile is reported for any symbol. Reason (FACT): no free source in hand provides the IV history needed to compute a rank; the spreads above are IV-vs-realized comparisons, not ranks, and must not be presented as ranks. What would change this: a sourced IV-history series the desk can cite.

**Verdicts + what would change them:**
1. MSFT front premium is event premium, not alpha (INFERENCE, high confidence on the mechanism). Would change if: Oct 29 post-earnings IV does not crush toward the ~20% realized zone, or the Oct 28 date moves.
2. Index/single-name vol is not broadly elevated today (INFERENCE). SPY/QQQ/TSLA at or below realized; AAPL/NVDA modestly above but window-contingent. Would change if: tomorrow's session reprices front IV back above Friday's levels, or the contingent windows roll clean and the spreads persist.
3. No parity violation detected at ATM on live quotes (FACT on the checked points). Would change if: a live, non-expiry-day chain shows a call/put IV or price break beyond bid/ask width — the 0-DTE artifacts do not count.

**Sources:** `https://query1.finance.yahoo.com/v7/finance/options/{SPY,QQQ,AAPL,MSFT,NVDA,TSLA}` (cookie+crumb required); `~/workspace/hedge-desk-research/nightly/2026-10-25-iv-inputs.json`

---

## 4. Open Quant/AI Model Lab

**Sweep coverage (FACT, as of 2026-10-26 ~13:30 PT):** arXiv q-fin API, newest-first control: 60 items back to 2026-10-15; in-window (Oct 22–23, since ledger #151) items triaged against the ledger — all previously logged items (#137–#151) confirmed already present, no duplicates added. GitHub search (created >2026-10-24, volatility-in-name): 22 repos returned; 21 NOLICENSE → triage exclusions, no rows (per standing NOLICENSE rule); 1 MIT repo examined in full below.

**New candidates — all scored with the repo's own `hedge_desk.research_intelligence.assess_source` (run, not hand-computed), abstracts/README read at source, claims labeled. All five appended as rows #152–156 in `~/workspace/hedge-desk-research/quant-lab-ledger.md`, verified by re-read. No candidate lives only in this daily file.**

| # | Candidate | Score / Disposition | Reason |
|---|---|---|---|
| 152 | "On the continuity of conditional distributions and stratification for derivative pricing" — arXiv:2610.32970v1, 23 Oct 2026 | 36 / **ARCHIVE** | Neural stratification factors for MC variance reduction (source-reported, UNVERIFIED). No author code link on abs page → reproducibility not established. Pricing-numerics theory, no desk procedure. |
| 153 | "Optimal Size in Market Making under State-Dependent Hawkes Process" — arXiv:2610.31903v1, 22 Oct 2026 | 39 / **ARCHIVE** | Prony/Hawkes executed-volume model, retrospective LOB evaluation (source-reported, UNVERIFIED). No code link. Market-making sizing, not a desk lane. |
| 154 | "Mimicking Volatilities under Marginal Constraints via q_x-Bass Martingales" — arXiv:2610.31825v1, 22 Oct 2026 | 36 / **ARCHIVE** | Martingale-optimal-transport calibration theory (source-reported, UNVERIFIED). No code link. Pure theory, no desk procedure. |
| 155 | "Financial Context-Rich Strategy for Actor-Critic based Agents" (DRL stock trading) — arXiv:2610.32237v1, 23 Oct 2026 | 22 / **ARCHIVE** | Autonomous-execution framing = paper-only boundary mismatch (no human-approval framing). No code link. Lowest score of the sweep. |
| 156 | Anindya-nub/Options-Market-Making-Volatility-Trading-Dynamic-Hedging — GitHub, created 2026-10-26, MIT, 0 stars | 43 / **ARCHIVE** | README verified at source via GitHub API: BS + 5 Greeks, vectorised IV inversion, SVI fit with calendar/butterfly checks, hedging simulator, Avellaneda-Stoikov MM book, P&L attribution — all source-reported, code NOT run. No tests/ dir, no CI in tree → reproducibility not established. Strongest of today's GitHub batch and the only MIT one, but 43 falls below the 45 WATCH band and the SVI/hedging lane is crowded (#18/#128/#146, #106). Archived on band discipline, not interest — reopen if tests/CI land. |

**Desk verdict: no TEST, no INTEGRATE this run.**

**Source failures (classified):** GitHub search API returned empty body / HTTP 000 twice (transient, proxy-level — same signature as 2026-10-17). Fallback worked: /rate_limit and /repos/ endpoints stayed healthy, and the search leg recovered on retry with a URL-encoded query. No data lost; the 22-repo result set was obtained after recovery. arXiv API leg healthy throughout.

**What would change the verdicts:** code release for #152/#154 (reopen), tests + CI for #156 (re-score toward WATCH), nothing for #153/#155 (lane mismatch regardless of code).

---

## 5. Weather/War/Logistics Futures Event desk (catalysts)

**Government-data rule applied:** no shutdown framing used — federal releases are demonstrably on schedule (EIA releases Oct 21–22, USDA WASDE Oct 9, Crop Progress weekly), consistent with the standing rule. The 2026-10-05 brief-correction premise was NOT applied.

### 1. Middle East energy shock dominates — Monday pullback is relief, not resolution
- FACT: Brent and WTI fell ~2% Monday morning Oct 26 from near six-month highs, after Friday's ~$3 surge. Snapshots differ by timestamp — Reuters 0018 GMT: WTI $101.67 (−1.55%), Brent $115.16 (−1.34%); Grafa 0426 GMT: WTI $101.04 (−2.16%), Brent $114.51 (−1.89%); DTN 9:27 AM CDT: Dec WTI $101.82, Brent $115.95. Friday settles: Brent $116.72, WTI $103.27. Week to Friday: Brent +6%, WTI +2.3%.
- FACT: Houthis claimed attacks on a Saudi airport and oil facilities Sat Oct 24–25; Saudi Arabia said it intercepted more missiles/drones Sunday and partly restarted its main airport. Qatari mediators went to Tehran Sunday; Saudi, Pakistani and Turkish officials prepared to meet in Tehran Monday; President Trump said Sunday he was still deciding between an Iran agreement or action.
- FACT (transit, conflicting methodologies — reported as range, not resolved): DTN vessel tracking: 8 vessels through Hormuz in the last 24h vs ~60/day average. IMF PortWatch via straits.live: 4 transits Oct 18 vs 85/day pre-crisis baseline. Kpler (Oct 6): 7 vessels, crude crossing 10.1 mmbpd, 27% below the wartime high, 74% of pre-war. ~492–500 vessels waiting outside the strait. October is the worst month on record for Hormuz shipping attacks (28+ attacks in October, 113 since February; 11 VLCCs damaged in October).
- FACT: DOE authorized an emergency exchange of up to 400,000 bbl from the SPR (West Hackberry site) for Phillips 66's 264,000 bpd Lake Charles refinery after a crude-delivery disruption (announced Friday).
- FACT: IEA Executive Director Fatih Birol warned energy markets may not return to pre-war conditions in 2027, with Hormuz and Bab el-Mandeb disruptions ongoing.
- INFERENCE — what curves appear to be pricing: a persistent disruption premium, not a one-day spike: Brent held above $114 after a 6% weekly gain, and Monday's dip retraced only ~22% of Brent's $7.17 four-session run from $109.55 (Oct 19) to $116.72 (Friday) — arithmetic from reported settles. Brent–WTI spread ≈ $13.49 (115.16 − 101.67, same-timestamp Reuters snapshot), a wide seaborne-risk premium. ULSD/RBOB diverged Monday (DTN: Nov ULSD +$0.0130 to $4.9972/gal, RBOB +$0.0369 to $3.2485/gal while crude fell) — product tightness outlasting the crude pullback.
- UNVERIFIED: full dated futures-curve shape (backwardation/contango by tenor) — no free dated curve snapshot retrieved in this sweep; do not treat the front-month read above as a term-structure claim.
- What would change it: verified Hormuz transit normalization (sustained daily transits back toward baseline), a confirmed Iran deal/ceasefire, or confirmed Saudi facility outage volumes. Opposite direction: a confirmed strike on export infrastructure or a Hormuz closure event.

### 2. Stacked catalyst Wednesday Oct 28 — EIA petroleum + FOMC same day
- FACT: FOMC meets Oct 27–28; decision Wed Oct 28, 2:00 p.m. ET, press conference 2:30 p.m. ET, no Summary of Economic Projections/dot plot at this meeting. Current target range 3.75–4.00% (Sep 16 hike). Market odds of a hold ~83–90% per Oct 26 secondary reporting; an Oct 9-vintage source put October-hike odds at 16–18% (stale — do not use as current).
- FACT: next EIA Weekly Petroleum Status Report due Wed Oct 28, 10:30 a.m. ET (weekly cadence; most recent release was Wed Oct 21).
- INFERENCE: Wednesday is a double-barreled session for energy and rates-sensitive futures: the morning inventory print lands hours before the FOMC statement. (Rates-desk overlap flagged; detail belongs to Desk 7.)

### 3. U.S. oil inventories: third straight draw, distillates the tight spot
- FACT (EIA via OilPrice/Morningstar/CME summaries — EIA primary page not directly fetched this run; figures cross-checked across three secondaries and consistent): week ending Oct 16 (released Oct 21): crude −3.1 mmbbl to 412.5 mmbbl, ~3% below the 5-yr average; gasoline −3.0 to 205.3 mmbbl (~5% below avg); distillates +1.7 to 104.3 mmbbl (~9% below avg). Third consecutive weekly crude draw; analysts expected only −0.3 mmbbl. Refinery runs 93.4%; U.S. production 13.3 mmbpd, −410,000 bpd w/w, still affected by Hurricane Isaias Gulf shut-ins (landfall Oct 9). Prior week (ending Oct 9): crude −8.6 mmbbl to 415.6 mmbbl.
- INFERENCE: into heating season, distillate tightness (9–12% below average across the last two reports) is the structural support under product cracks even when crude dips — consistent with Monday's ULSD/RBOB firmness against falling crude.
- What would change it: the Oct 28 EIA print showing crude/distillate builds, or restored Gulf production.

### 4. Natural gas: storage essentially balanced, winter setup neutral-to-firm
- FACT (EIA via Oil & Gas 360/TokenPost): week ending Oct 16 (released Thu Oct 22, 10:30 a.m. ET): working gas +77 Bcf to 3,644 Bcf — 152 Bcf (−4%) below year-ago, 35 Bcf (+1%) above the 5-yr average (3,609 Bcf), within the 5-yr range. Prior week: +67 Bcf to 3,567 Bcf. Next report expected Thu Oct 29 (weekly cadence).
- FACT (single secondary source — treat forecast miss as reported, not primary-confirmed): the 77 Bcf build came in below an ~80 Bcf consensus forecast.
- INFERENCE: storage enters withdrawal season roughly at average — no scarcity premium from inventories alone; any winter gas upside must come from weather or LNG feedgas, not a storage deficit. EIA's October STEO (via secondary) forecasts $3.48 average for 2026, $3.16 for 2027, and heating-oil homes facing prices >30% higher than last winter.
- What would change it: a cold snap driving early withdrawals, or the Oct 29 storage print missing consensus by a wide margin.

### 5. Grains: Oct 9 WASDE shock fully digested; harvest pace + China buying are the live variables
- FACT (Oct 9 WASDE, 17 days old): corn yield raised to 181.2 bu/acre (+2.7 vs September), production 16.034 bn bu, ending stocks 1.849 bn bu (+282 mm); soybeans record 53.1 bu/acre, production 4.562 bn bu, stocks 315 mm; wheat production 1.534 bn bu (smallest since 1970), stocks 740 mm (+23 mm). Day-one futures reaction: corn ~−5%, soy ~−2%, wheat ~−3%; tick moves ZC −72, ZS −76, ZW −52.
- FACT (Crop Progress, week ending Oct 18): corn harvested 44% (5-yr avg 52%); soybeans 64% (avg 65%); Iowa corn just 26% vs 50% average; winter wheat planting 63%, 6 pts behind last year. Dec corn fell 2.89% on the week to $4.60/bu by Oct 22. NOAA dry window through Tue Oct 27 favors catch-up.
- FACT (CFTC, week ending Oct 20): managed money cut corn net long 84,620 contracts to 146,257; added 18,096 to CBT wheat net short (51,134); cut soy net long 30,555 to 206,936.
- FACT with conflict (range, not resolved): China has bought "over 60%" (TradingEconomics, Oct 23) to "near 70%" (Fastmarkets headline) of its 25 mmt U.S. soybean target — report as 60–70%, not a point estimate.
- INFERENCE — what grain curves appear to be pricing: ample supply plus harvest pressure: the post-WASDE selloff has held, funds are trimming longs, and the market is treating the large crop as the base case. Next WASDE Nov 10 is the next scheduled repricing event.
- What would change it: Nov 10 WASDE revision, a Brazil planting disruption, or a stall in Chinese buying.

**Watchlist relevance — INFERENCE only:** no fresh futures catalyst names a watchlist company directly. Transmission to SPY/QQQ is via the energy channel — crude near six-month highs raises transport/input costs and headline inflation pressure into Wednesday's FOMC decision, while product tightness (distillates, ULSD) raises logistics costs. No single-name futures read is warranted from this desk today.

**Gaps:** today's Crop Progress report (normally Mon 4:00 p.m. ET) was NOT captured — searches surfaced only the Oct 18 report. Do not carry the Oct 18 figures forward as current without that check. EIA primary pages (eia.gov) were not directly fetched; EIA figures above rest on three mutually consistent secondary summaries, with no contradiction found. Futures term-structure (beyond front-month spreads) and today's intraday curve moves are UNVERIFIED for lack of a free dated source, not estimated.

**Sources:** https://www.thehindubusinessline.com/markets/commodities/crude-oil-price-slips-from-six-month-highs-despite-supply-concerns/article71625467.ece ; https://grafa.com/en/news/united-states/oil-prices-fall-iran-diplomacy-saudi-supply-risks ; https://www.dtnpf.com/agriculture/web/ag/news/world-policy/article/2026/10/26/wti-brent-crude-fall-mideast-talks ; https://straits.live/briefs/2026-10-24 ; https://logisticswall.com/category/blog/strait-of-hormuz-under-pressure-record-ship-attacks-and-nearly-500-vessels-disrupted ; https://oilprice.com/Energy/Crude-Oil/EIA-Says-US-Crude-Inventories-Sink-Further.html ; https://www.morningstar.com/news/dow-jones/202610216600/us-crude-oil-stockpiles-fall-more-than-expected ; https://www.oilandgas360.com/weekly-gas-storage-10-16/ ; https://www.rfdtv.com/wasde-recap-usda-raises-grain-supplies-as-futures-fall-sharply ; https://blog.pricegroup.com/2026/10/26/a-red-october-ag-marketing-report-10-26-2026/ ; https://df.media/federal-reserve-october-2026-meeting-investors-guide/

---

## 6. Box/Parity Observer — light touch

**One new methodology item (material, watchlist-adjacent):**
- FACT (corroborated secondary reporting; S&P DJI primary release NOT directly retrieved): S&P Dow Jones Indices will revise its growth/value scoring methodology, effective before the open on **December 21, 2026**, implemented at the annual index reconstitution. Changes: **remove 12-month price momentum** from growth scoring; **add free cash flow, forward earnings, and intangible assets** to the value assessment; retain the three-year sales-per-share growth rate as a growth factor. Reported Oct 23–24, 2026, citing an S&P statement following a consultation.
- INFERENCE: a style-index reshuffle at reconstitution could shift growth/value index weights for large-cap watchlist names (AAPL, MSFT, NVDA, TSLA are all style-index constituents in principle). Per-name weight changes are UNVERIFIED — no constituent-level reshuffle list was published in the sources read.
- Analyst estimate, not a FACT: Bloomberg Intelligence's James Seyffart put passive funds tied to the affected benchmarks at "no less than $375 billion" — treat as an estimate, not an S&P figure.
- Parity read: no parity implication — this is a benchmark-classification change, not an options-pricing deviation. Deterministic put-call/box parity is unaffected by it.

**WATCH — FTSE Russell consultation (secondary, single-source item):** FTSE Russell is separately consulting on revising its benchmarks' 50/50 growth-value allocation in response to technology giants' market dominance; consultation closes **December 11, 2026**. No outcome yet — watch item only.

**Parity violations: nothing material found.** Explicit line: no new published parity-violation or box-spread arbitrage analysis for SPY, QQQ, or any watchlist name was found in this sweep. What surfaced was evergreen educational material only (e.g., optionscout.ai put-call parity explainer, updated 2026-10-17; Investopedia conversion/reversal explainer), with the standard point that market makers arbitrage away actionable deviations within seconds/minutes.
- Adjacent, not a violation: Saxo's Oct 26 options brief reports implied correlation at its highest since June with dispersion at its median — i.e., the options market is pricing index-level rather than single-name moves into this week's Fed decision. That is a correlation/dispersion observation, NOT a put-call parity violation, and Saxo's Oct 20 brief explicitly centres its straddle reads on put-call parity (parity holding as the reference frame).
- Scope note: this desk did not run a live options-chain parity check (that is the Premium desk's live-pull lane); this verdict covers published analysis and methodology docs only. No live deviation is claimed or denied.

**Already-effective context (not new — do not treat as this run's news):** Nasdaq-100: Moderna joined Oct 9, 2026, replacing Warner Bros. Discovery (deal-driven removal). Relevant to QQQ composition in principle, but effective over two weeks ago and neither name is on the watchlist.

**Gap, not a failure:** the S&P DJI primary press release / methodology document itself was not located via search, so the Dec 21 revision is reported as corroborated secondary reporting (two independent aggregators agreeing, both citing S&P/Bloomberg) rather than primary-verified.

**Sources:** https://bursakl.com/news/s-and-p-changes-rules-for-classifying-growth-and-value-stocks/n751 ; https://www.briefs.co/news/s-p-dow-jones-revamps-growth-and-value-playbooks-ahead-of-de/ ; https://www.home.saxo/content/articles/options/paying-for-the-index-not-the-names---options-brief---26-october-2026-26102026

---

## 7. Bonds & Rates desk (FRED module — authoritative for this desk)

**Module run: SUCCESS (exit 0, no retries).** Command: `cd ~/workspace/github/hedge-desk && python3 -c "from hedge_desk import rates_desk; import json; print(json.dumps(rates_desk.rates_environment(), default=str))"`. Schema `hedge-desk-rates-desk-1.0.0`, mode `REAL_FRED_RATES`, `as_of` 2026-10-26, source `fred-public-csv-http-200`, lookback 60 days. No Yahoo yields were substituted, and no ^FVX/2Y labeling issue arises since all figures are FRED DGS2/DGS10.

| Series | Level | Latest date |
|---|---|---|
| Fed funds effective rate (DFF) | **3.88%** (change over window +0.25pp) | 2026-10-23 |
| Treasury 2Y (DGS2) | **4.69%** | 2026-10-23 |
| Treasury 10Y (DGS10) | **5.00%** | 2026-10-23 |
| 2s10s spread (10Y − 2Y) | **+31bp** | 2026-10-23 |
| SOFR | **3.92%** | 2026-10-23 |
| EFFR | **3.88%** | 2026-10-23 |
| OBFR | **3.88%** | 2026-10-23 |
| **SOFR − EFFR spread** | **+4bp** (3.92 − 3.88, arithmetic from module outputs) | 2026-10-23 |

All levels above are FACT (FRED via module). Data-currency note: latest FRED observations are Friday 2026-10-23; this is the normal weekend publication lag, not staleness — the module's `as_of` is today (2026-10-26).

**Slope direction (sign-reconciled): FLATTENING over the 60-day window.** Window start (2026-08-27): 10Y 4.67% − 2Y 4.20% = 47bp. Latest (2026-10-23): 5.00% − 4.69% = 31bp. Change: 31 − 47 = **−16bp → flattening**. Both legs rose over the window (10Y +33bp, 2Y +49bp); the 2Y rose more, which is what compressed the spread. Short-run: essentially flat — Oct 21: 32bp, Oct 22: 31bp, Oct 23: 31bp. Curve shape: **UPWARD_SLOPING** at +31bp — no inversion signal.

**Directional read for premium pricing:**
- Funding stress: none visible. SOFR sits just 4bp over EFFR and OBFR equals EFFR — no funding-stress signal in the overnight complex [FACT levels; "no stress" is INFERENCE from the narrow spread].
- Growth-multiple pressure persists. The 10Y at 5.00% keeps discount rates elevated versus the window start (4.67%) [FACT]; higher long rates = higher discount rates = pressure on growth multiples [INFERENCE] — most relevant to the long-duration watchlist names (NVDA, TSLA, MSFT, AAPL, and QQQ as a whole). This is a headwind to multiple expansion, not a claim about any single name's valuation — no name-level valuation was computed here.
- The flattening is a bear-flattening pattern (front end rising faster), consistent with a fed funds rate that rose 25bp over the window rather than with recession pricing [INFERENCE].
- Value-investor lens: elevated long rates raise the bar for paying up for growth; margin of safety matters more at a 5% 10Y than at a sub-4.5% one [INFERENCE, framing only — no trade proposed].

**What would change the read:** a move in the 2s10s spread back above ~45bp (re-steepening) or below zero (inversion) would flip the flattening call; a SOFR−EFFR spread widening well beyond the current 4bp would signal funding stress. Next catalyst: the FOMC announcement Wednesday Oct 28 (2:00 p.m. ET) — new policy guidance and the next FRED prints would supersede these levels. Module note: observations are measured facts, not a forecast and not advice; `trade_authorized`: false.

---

## Cross-desk conflicts — resolved / flagged (synthesis, not stapling)

1. **MSFT implied move — RESOLVED.** Yesterday's package left 5.3% (own Oct 23 calc) vs 7.57% (MetisTrades Oct 18 secondary read) unresolved. Today's fresh own recomputation lands at 5.26%, effectively identical to Oct 23's 5.28% — two consecutive fresh calculations vs one stale secondary read. **5.3% stands; the 7.6% read is retired.** Cross-check (INFERENCE/arithmetic, different measures, not a second FACT): MSFT's live Oct 30-expiry ATM IV of ~56% annualized over ~4 days implies roughly 56% × √(4/365) ≈ 5.9% — directionally consistent with the 5.26% straddle, not a contradiction.
2. **NVDA earnings date — UNRESOLVED, three-way split, do not pick one.** Premium desk: live Yahoo quote timestamp Nov 17 vs iv-inputs file Nov 18. Earnings desk: trackers split Nov 18 (MarketBeat, estimate) vs Nov 25 (TipRanks, labeled "Confirmed" but caveated as estimated from past schedules — an internal contradiction). Yesterday's package already flagged the Nov 17/18/25 split. Company has NOT confirmed a date (CMEG, ~20h old). All three dates fall outside the 2-week earnings window regardless, and outside the front IV window — so no front-window verdict depends on it. What settles it: an Nvidia company announcement.
3. **MSFT dividend record date — NOT carried.** The Dividend desk reported record Nov 19 alongside ex Nov 19; yesterday's package carried only ex-date and pay-date, and the parent's Nasdaq re-check this run did not corroborate a record date. The package asserts ex-date Nov 19 and pay-date Dec 10 only.
4. **Hormuz transit readings — UNRESOLVED range, not a point estimate.** DTN (~8/day vs ~60/day average), IMF PortWatch via straits.live (4 on Oct 18 vs 85/day baseline), and Kpler (7 vessels, Oct 6) use different methodologies and windows — reported as a range, not averaged or resolved.
5. **China soybean purchases — range, not a point estimate.** "Over 60%" (TradingEconomics, Oct 23) to "near 70%" (Fastmarkets headline) of the 25 mmt target — reported as 60–70%.
6. **FOMC hold odds — secondary only.** The 83–90% hold figure is Oct 26 secondary reporting (Futures desk), not a primary market source; an Oct 9-vintage 16–18% hike-odds figure is stale and was not used.

## What to watch next

- **Wed Oct 28, 10:30 a.m. ET:** EIA Weekly Petroleum Status Report. **Wed Oct 28, 2:00 p.m. ET:** FOMC decision + 2:30 p.m. press conference, then MSFT earnings after close — do not attribute the Oct 29 session move to either event alone.
- **Mon Nov 2, after close:** AAPL earnings + possible dividend declaration — re-check the Nasdaq dividend calendar the morning of Nov 3.
- **Thu Oct 29, 10:30 a.m. ET:** EIA natural gas storage. **Tue Nov 10:** next WASDE.
- **Dec 11, 2026:** FTSE Russell consultation closes. **Dec 21, 2026:** S&P DJI growth/value scoring revision effective at reconstitution.
- **Open items carried forward:** NVDA earnings date (UNVERIFIED, three-way split); today's Crop Progress report (not captured — pull directly, do not carry Oct 18 figures forward as current); IV rank for all symbols (UNVERIFIED — no free IV-history source); futures term-structure beyond front-month spreads (UNVERIFIED).
