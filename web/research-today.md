# Hedge-desk daily research — Sat 2026-11-21

**Run:** Sat 2026-11-21, ~13:30 PT. **Profile:** research / input only — no git, no PRs, no code changes, no GitHub operations.
**Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA.
**Method:** 7 parallel desks; every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED with source + as-of. Market data: Yahoo Finance first (v8 chart UA-only; v7 options/quote cookie+crumb), Nasdaq second, then fallbacks. Yield labeling: ^TNX = 10Y, ^FVX = 5Y (never 2Y); 13W bill is the front-end anchor. Federal data releases on schedule (CR funding through Dec 11 — no shutdown framing).
**IV inputs:** `nightly/2026-11-21-iv-inputs.json`, as_of 2026-11-21T07:55:37-07:00 — **FRESH** (inside the 26h guard). Live Yahoo pull 13:28 PT reproduced the file's nearest-expiry ATM IVs exactly on all six symbols.

---

## Synthesis — the 5 decision-relevant items

1. **Friday Nov 20 was a crash day, and it changes the realized-vol baseline, not just the tape.** S&P 500 −3.70% (7th straight down day), Nasdaq −5.28%, VIX closed 35.89 (+86% on the week, highest in 19 months). NVDA −14.01% to $125.53 on the reported SEC accounting probe — three sessions after a 103%-growth earnings beat that already faded −2.9% on Nov 18. [FACT — Yahoo v8 closes; CNN/Reuters, Nov 20–21]
2. **All six IV windows are now WINDOW-CONTINGENT — and the standing "Nov 5 crash day" framing is corrected.** Recomputation this session: Nov 5 drives only SPY/QQQ/TSLA; AAPL and MSFT are driven by a Nov 4 **up**-day (+5.17% / +6.47% log), and NVDA is driven by **Nov 20 itself** (−15.09% log). The 20-day window now carries **two** crash days. No clean IV-vs-realized verdict is available on any name; IV rank is UNVERIFIED (no free IV-history source). Front IV is elevated (SPY 33.9% → NVDA 107.4% at 2 DTE) but that is not a rich-premium call. [FACT — Desk 3, live pull + recomputation]
3. **Desk 7 unchanged: 5 HIKE / 0 CUT / 5 NEUTRAL; Dec 9 25bp hike call holds.** No new data prints on any indicator line (data lull until Nov 25: Oct core PCE). Goolsbee (Nov 20) added a credibility argument for hiking — second named voice in two days against a hold. Kalshi Dec total hike $0.92 unchanged; 25bp $0.89, hold $0.09. FedWatch secondhand converged ~90–98% 25bp. The 10Y reportedly rallied to 4.95% Friday — secondhand only; the Graham lens stays anchored to FRED-verified 5.04% (Nov 19). [FACT — Desk 7, FRED module + Kalshi direct pull]
4. **Oil is pricing a surplus while war escalates around Hormuz — the week's central tension.** Brent $92.57 (−3.41% w/w), WTI $83.98 (−5.17% w/w), third straight weekly loss, ~20% down in November. IEA flipped Q4 to a 1.7M b/d surplus (forecast, not observed fact). A tanker was struck exiting Hormuz Nov 20, yet shipments run at roughly pre-war levels. **OPEC+ full meeting Sun Nov 29** — the highest-consequence scheduled catalyst in the window: retaining ~2M b/d of cuts into 2027 would invalidate the IEA surplus arithmetic. [FACT — Desk 5, EIA/IEA/Reuters]
5. **Nothing on the earnings calendar for two weeks; one dividend date in four weeks.** No watchlist name reports Nov 23–Dec 5 (Nasdaq calendar sweep, 0 rows). Next reports cluster late Jan–early Feb 2027, all estimates. NVDA Dec 2 ex-date ($0.25, unchanged) is the only in-window dividend; MSFT's $0.98 ex-date passed Nov 19. Quant Lab's one find: Piterbarg & Van der Helm on term premia and bond convexity (#325, WATCH 59) — Desk 7 adjacent. [FACT — Desks 1, 2, 4]

**What would change the picture:** Oct core PCE on Nov 25 (the last print that can move December; a hot m/m ≥ +0.3% strengthens the 50bp tail); OPEC+ on Nov 29; any Hormuz flow interruption; the Nov 5 and Nov 20 jumps aging out of the 20-day window (~Dec 4 and ~Dec 21) restoring a clean realized-vol baseline.

---

## Desk 1 — Earnings Event

**As of:** Sat 2026-11-21, ~13:30 PT. Window: Mon 2026-11-23 → Fri 2026-12-05.
**Headline: No watchlist name reports earnings in the next two weeks.** [FACT — Nasdaq earnings-calendar API, swept 2026-11-23 → 2026-12-05, 11 dates, 0 watchlist rows; retrieved 2026-11-21 13:27 PT] No options-implied earnings move to report; no binary-event premium to avoid. Thanksgiving Nov 26 (market closed); Nov 27 short session, 4 reporters, none on watchlist.

### Forward calendar (next report per name — all estimates, none issuer-confirmed)

| Name | Next report | Timing | Status | Source |
|---|---|---|---|---|
| AAPL | ~Feb 4, 2027 | After close (est.) | ESTIMATED | MarketBeat; range Jan 21–Feb 4 per SmartCalendars |
| MSFT | ~Jan 27, 2027 | After close (est.) | ESTIMATED | MarketBeat; SummitCapNews lists Jan 26 — dates disagree by one day |
| NVDA | ~Feb 23, 2027 | After close (est.) | ESTIMATED | SummitCapNews |
| TSLA | ~Jan 27, 2027 | After close (est.) | ESTIMATED | MarketBeat; SummitCapNews lists Jan 26 — dates disagree by one day |
| SPY / QQQ | n/a | n/a | ETFs — no earnings | — |

Yahoo quoteSummary `calendarEvents.earningsDate` returned null for all four names on 2026-11-21 — Yahoo currently carries no next earnings date for any of them. [FACT — Yahoo v10 quoteSummary, cookie+crumb pull, 13:28 PT]

### Just-reported: NVDA Q3 FY2027 (Tue Nov 17, after close) — read from the release itself

- Revenue **$115.8B**, +20% Q/Q, **+103% Y/Y**; Data Center **$107.6B** (+110% Y/Y, ~93% of total). [FACT — NVIDIA Q3 FY27 release, Nov 17, 2026; same text filed as SEC 8-K exhibit]
- Non-GAAP diluted EPS **$2.68** (+111% Y/Y); GAAP EPS $2.70. Q4 FY27 outlook: revenue **$130.0B ±3%** (14-week quarter). [FACT — same release]
- Consensus (Zacks): EPS beat $2.50 consensus by ~7%; revenue beat $108.19B by ~7%. [FACT — Zacks, Nov 18; second-hand consensus figure]
- Price reaction: $155.46 (Nov 17) → **$150.96 (Nov 18, −2.9%)** → $145.98 (Nov 19, −3.3%) → $125.53 (Nov 20, −14.0%, SEC-probe report). [FACT — Yahoo v8 closes]
- **Value-lens read [INFERENCE]:** a 103%-growth print with a $130B guide that still sells off is a reminder that the margin of safety lives in the price paid, not the quarter's growth rate.

### Last-print reactions (single observations, not historical averages)

| Name | Reported | Result (verified) | Next-session move |
|---|---|---|---|
| AAPL | Mon Nov 2, after close | Revenue $114.5B +12% Y/Y; EPS $2.10 +14% Y/Y (incl. +$0.05 tariff-refund benefit) | **−1.9%** ($338.32 → $331.90, Nov 3) |
| MSFT | Wed Oct 28, after close | EPS $4.89 vs $4.72 est.; revenue $92.28B vs $90.62B est. (MarketBeat) | **−0.2%** ($531.01 → $530.14, Oct 29) |
| TSLA | Wed Oct 21, after close | Figures not re-verified this session | **−3.1%** ($386.47 → $374.58, Oct 22) |
| NVDA | Tue Nov 17, after close | See above | **−2.9%** ($155.46 → $150.96, Nov 18) |

**Pattern note [INFERENCE]:** all four names fell the session after their latest print despite beats (AAPL, MSFT, NVDA all beat consensus; TSLA figures unverified). Four single observations do not establish a "beats sell off" rule — that would be speculation — but the uniformity is decision-relevant context for the next cycle.

**Verdict:** nothing on the earnings calendar for two weeks — no binary event to trade around, no earnings premium to harvest or avoid. **What would change it:** an issuer-confirmed earnings date inside the window; a surprise pre-announcement; a rescheduled date moving a name into December.
**Gaps / UNVERIFIED:** multi-quarter historical average earnings-day move per name — not computable from free sources this session, not estimated. TSLA Q3 headline figures — date and move verified, figures not re-checked. MSFT figures rest on MarketBeat, not the issuer release (second-hand).

**Sources:** Nasdaq earnings calendar API (swept 2026-11-23 → 2026-12-05); Yahoo v10 quoteSummary + v8 chart closes; NVIDIA Q3 FY27 release (nvidianews.nvidia.com) + SEC 8-K exhibit (sec.gov, CIK 1045810); Apple Q4 FY26 release + SEC 8-K exhibit (CIK 320193); MarketBeat compare pages; SmartCalendars Magnificent 7 calendar; CapitalMEG; Zacks NVDA recap.

---

## Desk 2 — Dividend Opportunity

**As of:** Sat 2026-11-21, 13:30 PT. Prices = Fri Nov 20 close (Yahoo v8 timestamped closes). Window: ex-dates Nov 21 – Dec 19, 2026.

| Symbol | Ex-date | Amount | Pay date | Change vs prior | Yield* | Source |
|---|---|---|---|---|---|---|
| NVDA | **Dec 2, 2026** | $0.25/qtr | Dec 23, 2026 | Unchanged (same as Sep 10) | 0.80% | Nasdaq dividends calendar 2026-12-02 (announced 11/17/2026); NVIDIA Q3 FY27 release |
| MSFT | Nov 19, 2026 (passed) | $0.98/qtr | Dec 10, 2026 | **+7.7% vs $0.91** (Sep 15 board raise) | 0.81% | Nasdaq calendar 2026-11-19; desk standard (dividend-count-standard.md) |
| AAPL | Nov 12, 2026 (passed) | $0.27/qtr | Nov 16, 2026 | Unchanged | 0.32% | Nasdaq calendar 2026-11-12; Apple IR history |
| SPY | None declared in window | — | — | — | 1.10% trailing | Yahoo chart events (last ex Sep 18, $1.889); Nasdaq Dec 18/21 queries: no SPY row |
| QQQ | None declared in window | — | — | — | 0.51% trailing | Yahoo chart events (last ex Sep 21, $0.751); Nasdaq Dec 18/21 queries: no QQQ row |
| TSLA | None — pays no dividend | — | — | — | 0.00% | Yahoo chart events, 1-yr history: zero dividends |

\* Yield = annualized rate ÷ Nov 20 close (AAPL $342.56, MSFT $484.52, NVDA $125.53); SPY/QQQ use trailing-12-mo distributions ($7.583 / $3.091) ÷ close (SPY $689.81, QQQ $608.45). Computed by this desk from the two named inputs.

### Observations

1. **NVDA's Dec 2 ex-date is the only in-window ex-date — now declared, closing last week's open item.** [FACT — Nasdaq calendar 2026-12-02; corroborated by NVIDIA's Q3 FY27 release.] Rate unchanged — no raise, no cut, no special. The 0.80% forward yield at the Nov 20 close of $125.53 (up from 0.60% at the Nov 12 close of $166.19) is entirely mechanical — price fell ~24% in the week, rate unchanged — not a dividend improvement. [FACT — arithmetic; Yahoo timestamped closes Nov 12–20]
2. **MSFT's $0.98 payment lands Dec 10; ex-date passed Nov 19, capture window closed.** Still the **24th consecutive annual increase** under the desk standard. Two third-party write-ups this week say "25-year streak" — a different counting methodology, not a new fact; the desk does not drift. Forward yield 0.81% at $484.52 — highest single-name yield on the watchlist, also mechanically lifted by the week's decline. [FACT]
3. **AAPL's Nov 12 ex-date is past; next is February 2027.** $0.27 unchanged; no raise since May 2026 (+3.8% from $0.26). Full consecutive-increase streak remains **UNVERIFIED**: screeners disagree (12 vs 14 vs 15 years). [FACT]
4. **SPY/QQQ December ex-dates still undeclared — do not assume the usual third-Friday date.** [UNVERIFIED — Nasdaq calendar queries Dec 14–18 and Dec 21 returned no SPY/QQQ rows.] Pattern only: SPY Dec 2025 ex was Dec 19, QQQ Dec 22 — mid/late-December dates plausible but unconfirmed. [INFERENCE — cadence pattern only]
5. **No cuts, suspensions, specials, or new increases** anywhere on the watchlist this week. [FACT — Nasdaq calendars Nov 23–27, Dec 1–4, Dec 7–11, Dec 14–18, Dec 21; Yahoo histories; news sweep Nov 21]

**Verdict (value lens):** no dividend-capture opportunity of note — the single in-window ex-date pays $0.25 on a price-drop-inflated yield, and watchlist yields (0.32–1.10%) are too thin to drive a margin-of-safety case on income alone. MSFT's 24-year raise streak is the only durable dividend-quality signal, and its capture window has closed for this quarter. **What would change it:** a declared SPY/QQQ December ex-date; any new raise/cut/special; an NVDA or AAPL raise declaration (next expected: AAPL May 2027, MSFT Sep 2027).

**Source notes:** Yahoo v8 chart (UA-only) returned full 1-yr histories; Yahoo meta `chartPreviousClose` values are stale (e.g., NVDA $223.47 vs Nov 19 close $145.98) — all prices use timestamped daily closes. Nasdaq calendar returned rows for every queried trading day; only watchlist row in the window was NVDA Dec 2. Nov 26 returned 0 rows (Thanksgiving).

---

## Desk 3 — Overnight Premium (IV)

**Freshness guard — FRESH (verified this session).** IV inputs `as_of` **2026-11-21T07:55:37-07:00** (~5.5h old, inside 26h guard). Live Yahoo pull 13:28 PT (cookie+crumb) reproduced the nightly file's nearest-expiry ATM IVs **exactly to 4 decimals on all six symbols**. Levels below are Friday-close chains (markets closed Saturday), not today's live quotes. Raw live pull: `parts/2026-11-21-desk3-live-iv.json`. [FACT]

### Context — Friday Nov 20 was a crash day

S&P 500 −3.70% (7th straight down day), Nasdaq Composite −5.28%, VIX closed 35.89 (+86% on the week, highest in 19 months). NVDA −14.01% to $125.53 on the reported SEC accounting probe. [FACT — Yahoo v8 closes + CNN/Reuters/Investopedia, Nov 20–21]

Friday simple moves, recomputed from Yahoo v8 daily closes: SPY −3.64% (715.87 → 689.81), QQQ −5.67% (645.04 → 608.45), AAPL −1.90% (349.21 → 342.56), MSFT −2.77% (498.30 → 484.52), NVDA −14.01% (145.98 → 125.53), TSLA −7.64% (374.41 → 345.82). [FACT]

### IV snapshot — nearest expiry Mon Nov 23 (2 DTE) vs Dec 18 (~27 DTE)

ATM IV = mean of ATM call/put `impliedVolatility`; realized 20d = sample stdev of 19 log returns × √252 over closes Oct 26–Nov 20. All IV levels **FACT** (live Yahoo pull + nightly file agreement); realized and variance shares **FACT** (nightly file, independently recomputed — 5 of 6 realized vols reproduced exactly, MSFT within 0.10pp).

| Symbol | Spot (Fri close) | ATM IV Nov 23 | ATM IV Dec 18 | Term slope (front−back) | Realized 20d | IV − realized | Max-day var. share | Driver day |
|---|---|---|---|---|---|---|---|---|
| SPY | 689.81 | 33.88% | 31.31% | +2.57pp | 26.89% | +6.99pp | 0.355 | Nov 5 (−4.51% log) |
| QQQ | 608.45 | 47.65% | 41.60% | +6.05pp | 40.99% | +6.66pp | 0.338 | Nov 5 (−6.71% log) |
| AAPL | 342.56 | 35.51% | 32.02% | +3.49pp | 28.47% | +7.04pp | 0.462 | **Nov 4 (+5.17% log)** |
| MSFT | 484.52 | 51.61% | 44.09% | +7.52pp | 38.36% | +13.25pp | 0.382 | **Nov 4 (+6.47% log)** |
| NVDA | 125.53 | 107.40% | 80.21% | +27.19pp | 68.33% | +39.07pp | 0.466 | **Nov 20 (−15.09% log)** |
| TSLA | 345.82 | 64.90% | 64.27% | +0.63pp | 63.89% | +1.01pp | 0.434 | Nov 5 (−11.40% log) |

### Stale-jump screen — ALL SIX WINDOW-CONTINGENT

Every symbol's max single-day variance share exceeds the 0.30 threshold, so **every IV-vs-realized verdict is WINDOW-CONTINGENT, not a clean verdict**. [FACT]
- **Correction to the standing "Nov 5 crash day" framing:** Nov 5 is the driver only for SPY, QQQ, and TSLA. AAPL and MSFT are driven by a Nov 4 **up**-day, and NVDA by **yesterday, Nov 20**. Second-largest shares: SPY Nov 20 (0.240), QQQ Nov 20 (0.256), TSLA Nov 20 (0.211) — the window now carries **two** crash days. [FACT — recomputed from Yahoo v8 closes this session]
- Consequence: the 20-day realized vols are inflated by one-to-two jump days, and the IV-minus-realized spreads (+1 to +39pp) cannot be read as "premium is rich" — the denominator is jump-polluted. [INFERENCE]

### Term structure — front-loaded everywhere, no earnings hump

Front (Nov 23) IV exceeds Dec 18 IV on all six names; NVDA's slope (+27.19pp) is by far the steepest, MSFT next (+7.52pp). [FACT] The shape is a crash-regime front elevation, not an earnings hump: no watchlist name reports inside either expiry window. [INFERENCE] TSLA is the exception in shape: near-flat term structure (64.90% vs 64.27%) and IV ≈ realized (+1.01pp) — its vol is high across the curve, not front-loaded. [FACT levels / INFERENCE shape read]

### Skew observation — calls richer than puts at ATM (flag, not a verdict)

Near-expiry ATM call IV vs put IV: SPY 40.78% / 26.99% (+13.79pp), QQQ 56.78% / 38.52% (+18.26pp), AAPL 40.92% / 30.10% (+10.82pp), NVDA 112.84% / 101.95% (+10.89pp), TSLA 68.32% / 61.47% (+6.85pp); MSFT the exception at 50.98% / 52.23% (−1.25pp). [FACT — live pull] Calls-richer-than-puts at ATM inverts normal equity skew and is **flagged as an observation only**: Saturday quotes on 2-DTE contracts with wide markets (e.g., SPY Nov 23 ATM call bid/ask 3.85/5.10, ~28% of mid), so the split may be quote noise / stale marks. A full put-call parity check was **not** run (no rate/dividend inputs pulled) — no parity verdict claimed. [INFERENCE noise hypothesis / UNVERIFIED parity] What would change it: Monday live quotes with tight two-sided markets.

### IV rank — UNVERIFIED

No free source for IV history / 52-week IV percentile was available this session, so **IV rank is UNVERIFIED for all six names** — no "elevated IV rank" flag can be issued. Levels (front IV 34–107%) are high in absolute terms, but without a history baseline that is not an IV-rank claim. [UNVERIFIED — never guessed]

### Earnings inside the window — NONE

NVDA reported Tue Nov 17 (past). Next estimated reports (MSFT/TSLA ~Jan 27, AAPL ~Feb 4, 2027) are well outside the IV window. No premium-into-binary-event avoidance flag applies this week.

**Verdict:** Front-month IV is elevated across the board after a two-crash-day week, but no clean rich/cheap premium verdict is available — every window is jump-contaminated. **What would change it:** (1) the Nov 5 and Nov 20 jumps aging out of the 20-day window (~Dec 4 and ~Dec 21) restoring a clean realized baseline; (2) a verifiable IV-history source establishing IV rank; (3) Monday tight-market quotes confirming or killing the call-rich skew split. **Value-investor read:** no margin-of-safety signal here — elevated IV in a crash regime with a contaminated realized baseline is not evidence of mispriced premium in either direction. Premium into Monday's 2-DTE expiry is weekend paper, not an opportunity set.

**Sources:** `nightly/2026-11-21-iv-inputs.json` (as_of 2026-11-21T07:55:37-07:00); live Yahoo v7 options chains, cookie+crumb pull 13:28 PT, raw JSON at `parts/2026-11-21-desk3-live-iv.json`; Yahoo v8 chart daily closes; Nov 20 selloff: CNN, Reuters, Investopedia, Motley Fool; next-earnings estimates: MarketBeat, Zacks, Market Chameleon.

---

## Desk 4 — Open Quant/AI Model Lab

**Question:** anything new in papers, preprints, open datasets, or free APIs that changes how the desks work? Scored with the repo's own scorer (`hedge_desk.research_intelligence.assess_source`, run as a module, never hand-scored). Full register: `~/workspace/hedge-desk-research/quant-lab-ledger.md` (rows #324–#325 appended this run; ledger now ends at #325).

**Coverage note [FACT]:** Saturday — arXiv issued no new announcement. The q-fin listing still tops at Fri 20 Nov (20 entries, all accounted for in the 2026-11-20 run); arXiv API `submittedDate` range Nov 19–21 returns only the same 13 Nov-19 items — zero Nov-20 q-fin submissions at sweep time. Nov 20–22 submissions announce Mon 23 Nov; next run re-covers that window. GitHub leg skipped per the run brief's ban on GitHub operations.

### New candidates (2)

**#325 — Piterbarg & Van der Helm, "Term Premia and Bond Convexity" — score 59 → WATCH (run's top score)**
- Venue: SSRN 7687582, posted 13 Nov 2026, revised 16 Nov 2026; 76 pp. Abstract read at source: papers.ssrn.com/sol3/papers.cfm?abstract_id=7687582
- What it claims (source-reported, **UNVERIFIED** — abstract only, full paper not read): the bond yield decomposes exactly into expectation-hypothesis yield + term premium + lifetime convexity value, with the term premium defined as the expected profit of a continuously rebalanced bond position funded at the short rate. A "sliding curve" condition fixes the market price of rate risk without unobservable parameters. In a multi-factor quasi-Gaussian model with local + stochastic vol, skew/smile materially change the value of convexity vs an ATM-vol-only correction.
- Desk relevance [INFERENCE]: Desk 7 adjacent — a term-premium/convexity decomposition bears directly on the discount-rate input and the margin-of-safety read. The authors' own warning — convexity built from ATM vol alone is not the right correction — is the doctrine point to carry.
- Scorer (module): signal 4 / data 3 / implementation 2 / risk 4 / credibility 4, reproducible False → 59, WATCH (`MONITOR_FOR_EVIDENCE`, `REPRODUCIBILITY_NOT_ESTABLISHED`, `LICENSE_REVIEW_REQUIRED`). No code; data model-based plus a referenced swaps/swaptions empirical estimate, not open.
- Follow-up: full-paper read; code release? Re-check on the WATCH cadence.

**#324 — Pimentel, "Model Predictions of Gamma-Risk Evolution in Mid-Cap Options Chains" — score 34 → ARCHIVE**
- Venue: SSRN 6006035, posted 26 Jan 2026, revised 9 Nov 2026; 13 pp. Abstract read at source: papers.ssrn.com/sol3/papers.cfm?abstract_id=6006035
- What it claims (source-reported, **UNVERIFIED** — abstract only): extends gamma-risk analysis around earnings into mid-cap equities, testing five widely used option-pricing models on predicting Gamma-risk evolution over short horizons. Headline result is a null — no correlation established between liquidity and predictions of Gamma risk.
- Why archived [INFERENCE]: single author, no affiliation stated, 13 pp unreviewed working paper, no code/data; watchlist is large-cap so mid-cap-only transfer is thin; an honest null, but too thin to carry. Band discipline: 34 < 45.
- Scorer (module): signal 2 / data 2 / implementation 1 / risk 3 / credibility 2, reproducible False → 34, ARCHIVE.

### Triage exclusions (no ledger rows)

- Pozzetti/Natividade, "Breaking Even with FX Volatility" (SSRN 7683321, Oct 2026) — FX options break-even vol; no desk lane covers FX. Out of scope.
- Li/Wang 2608.26115 (option-implied crash risk) and Boucher WP7 — already ledgered (#206, #284); no new row.

### Re-checks (no movement)

arXiv API `id_list` re-check, 2026-11-21: core set #4 (v1), #9 (v2), #13 (v1), #14 (v3), #15 (v1), #20 (v2), #21 (v3), #25 (v4, 2026-11-10), #30 (v3), #31 (v3), #257 (v2, 2026-11-12); recent set #312–#323 (all v1). No version movement — all stay WATCH/ARCHIVE as recorded. (API query did not return `arxiv:comment` elements this run, so comment fields were not re-verified; no conclusion drawn from their absence.)

**Verdict:** quiet Saturday sweep — one genuinely new, Desk-7-relevant paper; nothing that changes a desk workflow today. **What would change it:** a code release or full-paper read on #325; the Mon 23 Nov arXiv announcement covering the Nov 20–22 window. No TEST/INTEGRATE movement this run (run max 59).

---

## Desk 5 — Weather / War / Logistics Futures Events

**As of:** Sat 2026-11-21, ~13:30 PT. All prices are Friday 20 Nov 2026 settlements unless noted.

### 1. Oil — surplus pricing vs. live war risk

**Prices and curve [FACT]:** Brent Jan 2027 settled Fri 20 Nov at **$92.57/bbl**, +$0.59 (+0.64%) on the day, **−3.41% on the week** (from $95.84), third straight weekly loss. WTI Dec 2026 settled **$83.98**, +$0.77 (+0.93%) on the day, **−5.17% on the week** (from $88.56); more-active Jan WTI $83.41. November month-to-date: both benchmarks down ~20%. Brent–WTI spread at settlement: $8.59/bbl. (Reuters via EnergyNow / TBS News, 21 Nov 2026.) Curve: WTI cash $87.99 vs futures (+$4.58); Brent cash $95.72 (+$5.78) — prompt physical tightness coexists with a falling flat price; the market is pricing a *future* surplus, not a *current* glut. [INFERENCE; single-source curve read, magnitude indicative only]

**EIA Weekly Petroleum Status Report — Wed 18 Nov, week ending 13 Nov [FACT, EIA via Morningstar / OilPriceAPI]:** commercial crude **+3.38M bbl to 417.8M bbl**, second straight weekly build; ~3% below the five-year average. Consensus had been ~+1.0M bbl (Morningstar survey) / +0.058M bbl (Reuters poll) — either way a clear upside surprise. Gasoline **+5.19M bbl to 215.9M bbl** (vs ~+1.4M expected); distillate **+1.57M bbl to 104.9M bbl**, still 7% below five-year average. Total commercial petroleum stocks +9.2M bbl to 1,224.9M bbl. Cushing **−1.21M bbl to 26.1M bbl** — the one tightening line. SPR −3.17M bbl to 276.4M bbl. Refinery utilization 95.7% (+0.5 pts); crude inputs 16.92M b/d (−129k b/d); U.S. crude production ~14.0M b/d (+19k b/d). Market reaction: WTI fell as much as $1.94 intraday post-release and settled Wed 18 Nov down $3.68 (−4.28%) at $82.34; Brent down $3.99 (−4.28%) at $89.15. [INFERENCE]: an across-the-barrel build with refineries at 95.7% reads as demand-side softness plus recovering supply, not a refinery outage. Next WPSR: **Wed 25 Nov, 10:30 ET**.

**IEA November Oil Market Report — Fri 13 Nov [FACT, IEA via Reuters/Oilprice]:** IEA flipped its Q4 2026 balance from a **1.8M b/d deficit to a 1.7M b/d surplus** — a 3.5M b/d swing in one month, driven by a +3.3M b/d upward revision to Q4 supply as Gulf exports recover. Global supply 105.4M b/d in October (+2.3M b/d m/m); observed inventories rose 52M bbl (1.7M b/d) in October. 2027: supply rising 6.6M b/d to 108.1M b/d and a surplus of ~3.8M b/d. Demand: −2.7M b/d in 2026 to 102.3M b/d, rebounding +2.0M b/d in 2027. [INFERENCE]: the IEA revision is the single biggest fundamental driver of the week's −3% to −5% price move. **Caveat:** a forecast revision of this magnitude is not the same as corroborated physical supply; no comparable revision from other major forecasters was found — treat the surplus as the IEA's forecast, not an observed fact. EIA's October STEO had Brent falling from $104.69 (Q4 2026) to $73.94 (Q4 2027) — directionally consistent.

**OPEC+ — the 29 Nov decision point [FACT]:** full 21-member ministerial meeting **Sun 29 Nov 2026** to set the **2027 output framework and new production baselines**. Group-wide production level currently runs only to 31 Dec 2026. On 1 Nov the seven core members kept December targets at September levels — third straight monthly pause; ~2M b/d of cuts remain in force through end-2026. [INFERENCE]: 29 Nov is the highest-consequence scheduled catalyst in this desk's window. Options range from extending the pause (bullish for price) to a dated unwind (bearish). **What would change the surplus thesis:** OPEC+ retaining the ~2M b/d cuts into 2027, or a Hormuz closure — either would invalidate the IEA's 2027 surplus arithmetic.

**Strait of Hormuz / Red Sea — escalation is real, flows are not (yet) disrupted [FACT]:** **20 Nov:** UKMTO reported an oil tanker exiting the Strait of Hormuz struck by an unidentified projectile, fire onboard, no injuries; a second tanker reportedly struck near Oman's Musandam Peninsula. Houthis fired missiles at Riyadh on Thu 19 Nov (intercepted); on Fri 20 Nov the Houthis warned workers/shipping near Saudi Red Sea ports (Jeddah) to evacuate, threatening to target Saudi ports if the Saudi-led coalition strikes Hodeidah. U.S. Central Command denied new strikes on Iran's Qeshm Island. Trump said he is "not rushing" Iran decisions; Iran's foreign minister said Tehran still wants a diplomatic end. **Despite all of the above, crude shipments through Hormuz have returned to roughly pre-war levels** (Reuters via TBS News, 21 Nov). [INFERENCE]: the market is pricing the *flow* (intact) over the *headline risk* (escalating) — hence three straight weekly declines during an active shooting war around the world's key oil chokepoint. Any actual flow interruption reprices violently the other way. **What would change it:** a Hormuz transit halt, a second tanker hit with casualties, or a Saudi–Houthi strike on port infrastructure. Russian supply side [FACT]: Ukrainian drone attacks have cut Russian refineries' combined crude processing by **45% since late October** — a partial offset to the Gulf surplus story, not yet visible in weekly EIA numbers.

**Ukraine / Europe escalation [FACT, 20–21 Nov]:** Russia launched a large overnight attack on Ukraine 20 Nov: 84 cruise missiles + 404 attack drones per Ukraine's Air Force; ≥9 killed; three Kyiv Dnipro bridges damaged; blackouts in ten regions. 21 Nov: ballistic missile struck Kryvyi Rih, 2 killed, 60 wounded. 20 Nov: two Russian missiles and a suspected drone came down in eastern Poland during NATO drills; NATO's Mark Rutte said the alliance would defend every inch of Polish territory. 21 Nov: drones hit Russian cargo ship *Sparta II* in the Gulf of Finland; ship caught fire, crew evacuated. [INFERENCE]: escalation is broadening geographically but no energy-infrastructure or shipping-lane closure has resulted yet. No direct futures-market impact beyond the general risk-off tone.

### 2. Natural gas — ample storage, soft winter outlook

**EIA Weekly Natural Gas Storage Report — Thu 19 Nov, week ending 13 Nov [FACT, EIA via TradingNews / MarketReview]:** injection **+20 Bcf to 3,882 Bcf**, vs 25 Bcf consensus and 15 Bcf five-year-average injection; 80 Bcf above the five-year average (3,802 Bcf), 66 Bcf below a year ago. Dec Henry Hub (NGZ26) $3.339 after the release (−3.3 cents on the day); front-month ~$3.41/MMBtu as of 21 Nov. Injection season ended at **3,810 Bcf, ~2% above the five-year average**. EIA Nov STEO [FACT]: Henry Hub forecast to average **$2.87/MMBtu Nov–Mar** (16% below the October forecast, on mild November weather), **$3.37 average for 2026 and $2.88 for 2027**. [INFERENCE]: Dec futures at $3.34 sit ~16% above EIA's winter-average forecast — the market is pricing more winter risk than the EIA's mild-weather base case. A cold snap is the obvious repricing trigger; January 2026 showed the tail (Henry Hub spot averaged $7.72 that month). Next storage report: **Wed 25 Nov, noon ET** (Thanksgiving shift). Next STEO: 8 Dec.

### 3. Agriculture — WASDE digested, harvest nearly done

**November WASDE — Tue 10 Nov [FACT, USDA via Grain Journal / Ag Optimus]:** corn yield cut to **179.6 bu/acre** (from 181.2); production 15.893B bu (−141M); ending stocks **1.758B bu** (−91M m/m, 68M below trade survey); stocks-to-use 10.8%; season-average farm price cut 10¢ to **$4.60**. Soybeans: record yield **53.3 bu/acre**; production 4.574B bu (+12M); exports raised 25M bu to 1.72B bu; ending stocks **300M bu** (−15M m/m, 36M below trade); price +10¢ to **$12.10**. World soybean stocks 123.50M tonnes — below the lowest trade estimate. Wheat: ending stocks **743M bu** (+3M); price −10¢ to $6.20. World wheat stocks 280.82M tonnes — above the highest estimate. Market reaction: corn +10¢ to $4.48, soybeans +43¢ to $12.26 on release day. [INFERENCE]: modestly bullish report, now 11 days old and digested; no fresh price signal this week.

**Crop Progress — Mon 16 Nov, week ending 15 Nov [FACT, USDA NASS via DTN / Farm Progress]:** corn harvest **88%** (90% last year, 92% five-year avg); soybean harvest **96%** — effectively done. Winter wheat: planting 92%; good-to-excellent **53%**, +4 pts w/w. [INFERENCE]: harvest is a non-event now; winter wheat improving is mildly bearish for wheat but the crop is months from harvest. Next USDA catalyst: **December WASDE** (expected quiet) and the **12 Jan** annual production summary + winter wheat seedings + quarterly Grain Stocks. Note: USDA is using an AI tool it built to double-check data in monthly crop production reports after September corn-data errors [FACT, Reuters via Pro Farmer, 9 Nov] — a data-reliability footnote, not a market mover.

### 4. Other / logistics

Thanksgiving week: U.S. markets closed Thu 26 Nov; thin liquidity Wed–Fri expected. No new index-methodology or parity items in this desk's scope; no fresh USDA/EIA schedule changes. Federal data releases are on schedule (CR funding through 11 Dec; no shutdown framing applies).
**UNVERIFIED / not found in this sweep:** full WTI/Brent term-structure strip beyond front month; current PortWatch Hormuz tonnage figure for this week (last verified baseline 2,911,941 t/day in the Love&Peace lane — not re-verified here, do not cite as current); gold/metals and softs moves.

**Verdict:** Energy futures are pricing a 2027 supply surplus (IEA flip + EIA builds + OPEC+ unwind arithmetic) while a live war around Hormuz and escalating Russia–Ukraine strikes have not yet touched physical flows. **What would change it:** (1) OPEC+ on 29 Nov retaining the ~2M b/d cuts into 2027; (2) any Hormuz transit interruption or port-infrastructure strike; (3) a cold snap repricing Henry Hub above the $2.87 winter-average forecast; (4) EIA WPSR on 25 Nov showing a draw instead of a third straight build. **Decision-relevance for the watchlist:** no direct earnings/IV catalyst from this desk this week; falling crude and a surplus narrative are a mild tailwind for equities' energy-cost line, while the Hormuz tail risk is the one asymmetric upside shock to oil and to broad risk sentiment. Nothing here justifies a risk-seeking posture; the margin-of-safety read is that the surplus is a forecast, not a fact, and the war discount is thin.

**Sources:** EIA WPSR 18 Nov (Morningstar / OilPriceAPI / GoldSquawk); oil settles 20 Nov (TBS News / EnergyNow); IEA Nov Oil Market Report (Oilprice / Rigzone); OPEC+ 29 Nov (Admiral Markets / FinanceFeeds); Hormuz / Red Sea / Ukraine (KimKJ / One Turn / Open Chronicle); EIA nat gas storage 19 Nov (TradingNews / MarketReview / OilMonster); USDA WASDE 10 Nov (Ag Optimus / Grain Journal); USDA Crop Progress 16 Nov (DTN / Farm Progress).

---

## Desk 6 — Box / Parity Observer

**Verdict: no new parity violation and no new core index-methodology document since yesterday.** Two items worth one line each: (1) the first SPXO (AM-settled SPX weekly) expiry on Nov 18 passed with no settlement-disruption report surfacing; (2) a genuinely new arXiv paper (Nov 17) on no-arbitrage shape violations in American options finds SPY violations under 1% for calls and under 2% for puts — parity-adjacent, not a violation finding.

- **Parity / box spreads — standing measurement carried [FACT, Solvinc blog, measurement run Nov 12]:** SPX box-implied financing 3.86% at 15 days rising to 5.16% at 435 days — parity holding, long end ≈ SOFR + ~120bp, retail-margin edge erased by execution costs. No updated scan published since. Source: blog.solvinc.io/posts/box-spread-financing-spx-rate-scanner/
- **Third Shin carry-gap paper surfaced [FACT, not new — dated May 26, 2026]:** "Tuning in to Frequencies: How Global Assets Align with U.S. Put-Call Parity Residuals" (arXiv:2604.19605). Adding IEFA, IGOV and IAU improves carry-gap fit (SPX in-sample R² 0.312 → 0.402; leave-one-year-out 0.221 → 0.379). Same conclusion as the other two: a funding/implementation wedge, not a payoff-level parity failure.
- **New paper [FACT, published Nov 17, 2026]:** Glasserman, Li & Pirjol, "Total Positivity Properties of American Options" (arXiv:2611.23495) — establishes TP2 conditions for American options under log-concave return densities; empirically violations are infrequent, typically small, and reverse quickly; for SPY, overall violation rates are less than 1% for calls and less than 2% for puts. A no-arbitrage shape constraint on American-style options, not a put-call parity violation. [INFERENCE]: consistent with the standing desk view — deterministic no-arbitrage relations in liquid US options hold within transaction-cost bounds; apparent violations are microstructure noise, not tradeable breaks. What would change it: a published, reproducible scan showing a same-day SPX/SPY/QQQ parity or box residual exceeding transaction costs.
- **No published SPY/QQQ/single-name US equity parity-violation analysis from the last day surfaced in this sweep.** [FACT]

**Index methodology / settlement mechanics:**
- **SPXO first expiry passed [FACT, Cboe]:** first SPXO expiry — Wednesday Nov 18, 2026, aligned to the monthly VIX settlement — occurred as scheduled; SPXO options settle to the SPX opening settlement price. No settlement-disruption report surfaced. Second SPXO expiry is Dec 16, 2026. SPXO uses price-time allocation in single-leg and complex books while SPX remains pro-rata; SPXW mixed with SPX/SPXO cannot leg into single-leg books — a spread-risk item for anyone holding SPXO against SPXW, not a parity break.
- **SEC notice [FACT, Federal Register, published Nov 18, 2026; Release No. 34-106897]:** SPXO fee-schedule change notice — publication of the filing already covered Nov 20; no new substance, fees only.
- **CME Globex [FACT, technology roadmap, as of Nov 21]:** three production items land Nov 22, 2026 — implied functionality extension for calendar and butterfly spreads, strike-price listing change for S&P 500 month-end options, reference-data warehouse enhancements; E-mini Nasdaq/S&P weekly options listing-cycle expansion follows Dec 6. Exchange infrastructure, not index methodology or parity; watchlist impact nil unless a listing change alters available expiries.
- **Carried [FACT, announced Oct 23, 2026, not new]:** S&P U.S. Style Indices methodology changes take effect before market open **Dec 21, 2026**; pro-forma files reach clients **Dec 4, 2026**. SPY tracks the S&P 500, not the style sub-indices, so no direct SPY composition change. Next check date: Dec 4 pro-forma files.

**Failures / gaps:** none. All searches returned; no source failure. **UNVERIFIED:** Solvinc box-curve numbers remain a single blog measurement on a delayed feed (Nov 12), not independently reproduced. The "$375B+ in passive funds tied to the affected style gauges" figure (Bloomberg Intelligence estimate relayed by secondary sources) remains unconfirmed against a primary source. Glasserman et al. SPY violation rates are as reported via the paper's abstract/secondary card; the full paper text was not re-read in this run.

---

## Desk 7 — Bonds & Rates

**Desk status: RAN CLEAN.** Rates module `rates_environment()` returned `REAL_FRED_RATES`, as_of 2026-11-21, latest obs Nov 19 (no Nov 20 daily obs published yet for DGS2/DGS10/SOFR/EFFR — the rates table is therefore unchanged from Nov 20 and is restated, not re-pulled). All 10 core indicators re-pulled from FRED this session. Kalshi pulled direct from API this session (~13:35 PT). **No new data prints on any indicator line; no indicator changed call. Tally unchanged: 5 HIKE / 0 CUT / 5 NEUTRAL. Call holds: 25bp hike Dec 9.** Baseline: `~/workspace/hedge-desk-research/desk7-core-indicators.md` (Nov 13 snapshot).

### Most decision-relevant items

1. **No new prints, no call changes — the quietest session of the cycle.** Every indicator's latest vintage is the one already carried: core PCE still Sep (Oct print Nov 25), payrolls still Oct, claims still w/e Nov 14, JOLTS still Sep, GDP still Q3, starts still Oct. The desk is in a data lull until Nov 25. [FACT, FRED pulls this session]
2. **Goolsbee added a credibility argument for hiking — Friday, Nov 20.** Chicago Fed President Austan Goolsbee said the Fed risks losing credibility if it does not act, after "multiple months in a row of borderline disturbingly high inflation rates." He declined to rule out a bigger move. He becomes a voter in January. Second named voice in two days leaning against a hold, after Waller's 50bp case. [FACT as reported, CoinCentral/Barron's]
3. **Kalshi total hike unchanged at $0.92; hold eased $0.11 → $0.09; tail ticked up $0.02 → $0.03.** Dec 25bp $0.89 (was $0.90); >25bp $0.03 (was $0.02, 24h vol $200k — the day's heaviest Dec contract after hold); hold $0.09 (was $0.11, 24h vol $471k). January 25bp $0.46 (was $0.48) vs hold $0.50 — still a coin flip. [FACT, Kalshi direct pull]
4. **Breakevens edged down a third straight session — 2.18% / 2.15% (Nov 20) vs 2.22% / 2.16% (Nov 19).** The Michigan-vs-breakevens credibility gap is now 3.7% vs 2.15% = 1.55pp, essentially flat vs yesterday's 1.54pp. Expectations stay anchored; no tripwire crossed. [FACT, FRED T5YIE/T10YIE]
5. **The 10Y reportedly rallied through 5% on Friday — secondhand only, not FRED-verified.** One report has the 10Y falling more than 10bp to 4.95% Friday as investors bought bonds into the equity selloff. FRED has not yet published a Nov 20 DGS10 obs, so the Graham lens below stays anchored to the verified 5.04% (Nov 19). [SECONDHAND, single basis; FRED verification pending]

### Rates table (module pull, FRED, as_of 2026-11-21; latest obs Nov 19 — unchanged from Nov 20)

| Series | Nov 19 | Nov 18 | Change since Nov 18 |
|---|---|---|---|
| EFFR (fed funds effective) | 3.88% | 3.88% | 0.00 (60-day window change 0.00) |
| 2Y Treasury (DGS2) | 4.76% | 4.80% | −4bp |
| 10Y Treasury (DGS10) | 5.04% | 5.07% | −3bp |
| **2s10s slope** | **+28.0bp** | +27bp | **+1bp steepening** (Nov 13: +27bp; Nov 10: +25bp) |
| SOFR | 3.91% | 3.90% | +1bp |
| OBFR | 3.88% | 3.88% | 0bp |
| **SOFR − EFFR funding spread** | **+3bp** | +2bp | Funding calm |

Curve shape: UPWARD_SLOPING. [FACT, module output]

### Core-indicator table — today's reads vs Nov 20

| Indicator | Trigger rule | Today's read | Call | Change | Broker POV |
|---|---|---|---|---|---|
| Core PCE (PCEPILFE, BEA via FRED) | HIKE if y/y >2.5% or m/m >+0.25% | **No new print.** Sep y/y +3.121%, m/m +0.317% (130.902) — still latest in FRED | HIKE | — | Anchor the discount rate to the higher regime. Oct PCE (Nov 25) is the re-anchor date and the last print that can move December. |
| Breakevens (T5YIE/T10YIE, FRED) | HIKE >2.75%; CUT <1.75% | **2.18% / 2.15% (Nov 20)** vs 2.22%/2.16% (Nov 19) — third straight downtick | NEUTRAL | — | Anchored; no credibility crisis. Tripwire remains a break above 2.75%. |
| Michigan expectations (MICH, U-M) | HIKE if yr-ahead >3.5% | **No new print.** Final: yr-ahead **3.7%** (prelim 4.3%, Oct 4.7%); 5-yr 3.3%; sentiment 51.5. Rel. Nov 20, 10:00 ET. FRED MICH still shows only Oct 4.7% (lags ~2 months — do not use as current) | HIKE | — | Gap vs breakevens now 1.55pp (3.7% vs 2.15%) — still the pressure to act. Margin above the trigger is only 20bp; the December prelim (early Dec) is the next read on this line. |
| Payrolls 3-mo avg (PAYEMS, BLS via FRED) | HIKE >+150k; CUT <+50k | **No new print.** Aug +186k, Sep +60k, Oct +165k = **+137k avg**, confirmed | NEUTRAL | — | Rule as written: NEUTRAL. Do not cherry-pick the +165k print. |
| Initial claims 4-wk avg (ICSA, DOL via FRED) | CUT if >300k; NEUTRAL <250k | **No new print.** Latest w/e Nov 14, 203k. 4-wk avg **197,750** (195+191+202+203)/4 — unchanged | NEUTRAL | — | No action on this read. It turns first — a 4-wk avg above 300k flips labor to CUT before payrolls confirm. Next release is the Thanksgiving-week print. |
| Job openings (JTSJOL, BLS via FRED) | HIKE if 3-mo change positive | **No new print.** Sep 7,523k (Jul 7,335k, Aug 7,190k) | HIKE | — | Demand has not rolled over; rules out the "labor is cracking" case for a hold. |
| Real GDP (GDPC1, BEA via FRED) | HIKE >2.5% ann.; CUT <1.0% | **No new print.** Q3 +3.37% annualized confirmed (24,611.077) | HIKE | — | Above-trend growth removes the "restraint is biting" objection. |
| Housing starts (HOUST, Census via FRED) | CUT if −5% over 3 mo; HIKE if rising through high rates | **No new print.** Oct 1,309k; Jul→Oct −4.4% | NEUTRAL | — | One month is not "rising through high rates" — NEUTRAL, not HIKE. Nov starts is the confirmation print. |
| High-yield OAS (BAMLH0A0HYM2, ICE BofA via FRED) | CUT >5.00%; NEUTRAL <4.00% | **3.52% (Nov 19)** — no Nov 20 obs in FRED yet; 3.20% Nov 12 → 3.52% is +32bp over the last 5 published sessions | NEUTRAL | — | No stress yet, but the direction is one-way and the minutes corroborate it (HY spreads "widened notably," esp. data-center construction debt). Watch is a break above 4.00%; 48bp away. |
| FOMC vote & guidance (federalreserve.gov) | HIKE if dissents favor tightening / language turns hawkish | **New voice:** Goolsbee (Nov 20) — Fed risks losing credibility if it does not act; "everything's always on the table." Standing: Oct 28 held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; minutes (Nov 18) "almost all" see further hikes as likely appropriate; "a couple" said >25bp could warrant consideration; Waller (Nov 18) for 50bp unless January is clearly signaled; Williams (Nov 18) against dramatic action; Musalem for up to a full point by spring 2027; Jefferson (Nov 19) deliberate, monitoring both sides; Schmid (early week) for strong action; Bessent (Nov 20, not a voter) urged against 50bp | HIKE | — (Goolsbee strengthens the direction case, not the size case) | Weight the Committee above any print — and above the Treasury Secretary, who does not vote. Goolsbee is the second named voice in two days against a hold; no new voice has argued for a hold. |

**Tally: 5 HIKE / 0 CUT / 5 NEUTRAL** (unchanged from Nov 20; Nov 13 was 5/1/4). No indicator changed call today.

### Market pricing vs indicator read

**Kalshi, direct API pull Nov 21 ~13:35 PT, Dec-2026 meeting (`KXFEDDECISION-26DEC-*`):** 25bp hike **$0.89** (bid 0.89 / ask 0.90, prev 0.89; 24h vol $26,548); more than 25bp **$0.03** (bid 0.02 / ask 0.03, prev 0.02; 24h vol $200,128); hold **$0.09** (bid 0.08 / ask 0.09, prev 0.11; 24h vol $471,458); 25bp cut $0.01; >25bp cut $0.01. **Total hike $0.92** (unchanged from Nov 20); sum of lasts $1.03 (3-cent over-round). vs Nov 20: 25bp $0.90→$0.89, >25bp $0.02→$0.03, hold $0.11→$0.09. [FACT]

**Kalshi further out (same pull):** Jan 2027 25bp hike **$0.46** (prev $0.48) / hold $0.50 (prev $0.49); Mar 2027 25bp **$0.50** (prev $0.54) / hold $0.40 (prev $0.38). The hiking-sequence case weakened again in step with December — January remains a coin flip, March's 25bp case fell 4 cents. [FACT]

**CME FedWatch — secondhand only, could not be read directly (embedded app, no public text API):** frenzycap FedWatch replication (Nov 20, 5:00 PM ET): 93% 25bp / 7% hold / 0% >25bp, +23bp expected. predictionmarketspicks (Nov 21, 3:00 PM ET): futures-implied 90.2% 25bp / 9.8% hold; Kalshi 89.5% 25bp / 8.5% hold on their read. Barron's (Nov 20): ~98% 25bp per CME FedWatch. Motley Fool (Nov 20): 96% 25bp / 4% 50bp. Converged range: ~90–98% 25bp, ~7–10% hold, ~0–4% 50bp. [FACT as secondhand reports; direct CME read UNVERIFIED.]

**Agreement/disagreement:** The venues have converged. Kalshi hold ($0.09) now sits inside the futures-implied hold range (7–10%), and the tail is $0.03 on Kalshi vs 0–4% on FedWatch — the cross-venue disagreement that opened Nov 20 has closed. The remaining disagreement is between the markets and the indicators: the indicator set votes direction (hike), not size, and no rule in it distinguishes 25bp from 50bp. One new tension: Waller's "25bp + clear January signal" path depends on forward guidance, and Barron's reports Chair Warsh has retreated from forward guidance — if the Committee will not signal January, the 50bp path gains relative plausibility. [FACT on prices; INFERENCE on the guidance tension.]

### Verdict — Desk 7

- **Thesis:** 25bp hike on Dec 9. The decision variable (core PCE, 3.12% y/y) is 112bp above target with no softening print since Nov 13; labor shows no deterioration on any kept read (claims 197,750 avg); the Committee's own minutes say "almost all" see further hikes as likely appropriate; Goolsbee added a credibility argument for acting; markets price a hike at ~92–98% depending on venue. [INFERENCE from FACTs above]
- **Evidence:** 5 HIKE / 0 CUT / 5 NEUTRAL (unchanged); Michigan final 3.7% yr-ahead (still >3.5% trigger); minutes' "almost all" + ">25bp could warrant consideration"; Kalshi total hike $0.92, 25bp $0.89; FedWatch ~90–98% 25bp; 2s10s +28bp; SOFR–EFFR +3bp (funding calm — no market-functioning objection to hiking).
- **What would change it:** (a) **Direction (to hold):** effectively nothing on the data calendar — would require Oct core PCE collapsing (Nov 25) or a market-functioning event; Nov CPI lands Dec 10, after the decision, and cannot change December. No kept indicator supports a hold, and no Committee voice has argued for one. (b) **Size (25bp → 50bp):** a hot Oct core PCE on Nov 25 (m/m ≥ +0.3% range, the Waller threshold) plus Waller gaining a second voice on the Committee; Bessent's pushback now works against this path, while Warsh's retreat from forward guidance works for it. (c) **Size (25bp → 25bp + January signal):** a soft Oct PCE would keep 25bp but strengthen the January-hike case — though Kalshi now prices January as a coin flip ($0.46/$0.50), so the street's sequence case has weakened further. (d) Claims 4-wk avg above 300k would flip labor to CUT — no sign of it (197,750). (e) Michigan is settled for November (3.7% final); the next read on this line is the December prelim (early Dec).

### Graham lens (update to §5 of the Nov 13 doc)

10Y 5.04% (Nov 19, FRED) — unchanged from yesterday's read, since no Nov 20 obs is published yet: at assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) is 49.02x, unchanged vs yesterday and **−2.95%** vs the Nov 10 anchor 4.98% (50.51x). Duration ≈ 8 puts the same move at about −0.96% on a 10-year position vs the anchor (approximation; ignores convexity). Re-anchor to 5.04%. The margin of safety is thinner by ~3% on this sensitivity vs the Nov 10 anchor: any intrinsic-value estimate carried at 4.98% overstates value by ~3%. Earnings-yield vs bond-yield spread: UNVERIFIED (no S&P earnings-yield figure from a primary source this session). The defensive read stands: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price. [FACT on yields; INFERENCE on the valuation read]

Note (secondhand, not in the lens): one report has the 10Y at 4.95% live on Friday. If FRED confirms ~4.95% when the Nov 20 obs publishes, the Gordon multiple would be 1 ÷ (0.0495 − 0.03) = 51.28x — a +4.6% re-rating vs the 5.04% anchor. That number is NOT used until FRED publishes it.

**Sources + as-of (all pulled this session unless noted):** Rates + all 10 indicators: FRED via repo module `hedge_desk.rates_desk` (rates_environment + fred_series_rows), run Nov 21 ~13:28–13:35 PT; latest obs Nov 19 for daily rates series, Nov 20 for breakevens, monthly/quarterly vintages as named per line. Michigan final: U-M Surveys of Consumers release Nov 20, 10:00 ET, carried from Nov 20 session. Kalshi: api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXFEDDECISION, direct pull Nov 21 ~13:35 PT. FedWatch: secondhand only (frenzycap Nov 20; predictionmarketspicks Nov 21; Barron's Nov 20; Motley Fool Nov 20). Direct CME read UNVERIFIED. Speakers: Goolsbee Nov 20 (CoinCentral, Barron's); Waller/Williams/Musalem/Schmid/Jefferson/Bessent carried from Nov 18–20 sessions. Friday 10Y 4.95%: single-basis secondhand. No source failures this session.

**UNVERIFIED items:** Direct CME FedWatch read (secondhand range only). Friday 10Y 4.95% live quote (single basis; FRED Nov 20 obs not yet published). No other UNVERIFIED items — every indicator read comes from a FRED pull or the U-M release this session.

---

## Cross-desk contradictions resolved

- **"Nov 5 crash day" vs Desk 3 recomputation:** the standing framing said Nov 5 drives the 20-day realized-vol window. Desk 3 recomputed from Yahoo v8 closes and showed Nov 5 drives only SPY/QQQ/TSLA; AAPL/MSFT are driven by a Nov 4 up-day, NVDA by Nov 20 itself. The package carries the recomputed attribution; the standing framing is corrected, not carried. [FACT — Desk 3]
- **NVDA's Friday −14.01% vs its Nov 17 earnings beat:** Desk 1 (release) and Desk 3 (news) agree — the Friday move is on the SEC-probe report, not on earnings. No contradiction; the beat faded first (−2.9% Nov 18, −3.3% Nov 19) and the probe report drove the crash leg. [FACT]
- **SPY/QQQ December ex-dates:** Desk 2 found no declaration; no desk asserts a date. Pattern-only inference is labeled as such. [UNVERIFIED]
- **FedWatch vs Kalshi:** converged this session (~90–98% 25bp vs Kalshi $0.89); the Nov 20 cross-venue disagreement is closed. [FACT — Desk 7]
- **Oil surplus vs war risk:** Desk 5 keeps the two separate — the surplus is an IEA forecast, the war risk is observed escalation with intact flows. No desk claims the surplus is observed fact. [FACT + INFERENCE]

## Desk status

| Desk | Status |
|---|---|
| 1 Earnings | Complete — no watchlist earnings in 2 weeks |
| 2 Dividend | Complete — NVDA Dec 2 only in-window ex-date |
| 3 Premium (IV) | Complete — FRESH inputs; all six windows WINDOW-CONTINGENT |
| 4 Quant Lab | Complete — 2 new candidates (#324 ARCHIVE, #325 WATCH); ledger updated |
| 5 Futures Events | Complete — oil surplus vs Hormuz risk; OPEC+ Nov 29 |
| 6 Parity Observer | Complete — no new violation; SPXO first expiry passed clean |
| 7 Bonds & Rates | Complete — 5 HIKE / 0 CUT / 5 NEUTRAL; Dec 9 25bp hike call holds |

No desk failed. No desk produced no output. All seven sections present above.
