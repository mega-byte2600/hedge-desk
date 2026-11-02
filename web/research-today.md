# Hedge-Desk Daily Research — Mon 2026-11-02

Research and input only — no git operations, no PRs, no code changes. Paper-only context; no Risk of Ruin estimate; no trade authorization proposed.
Watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA. Lens: value investor — mispricings, intrinsic-value gaps, margin of safety.
Evidence labels: FACT / INFERENCE / SPECULATION / UNVERIFIED. Every verdict states what would change it.

## Decision-relevant items (synthesis, not stapling)

1. **AAPL reports TODAY after the close — the only in-window earnings event, and the premium desk says avoid selling into it.** Options price ~4.6–5.0% implied move vs a 2.46% average first-session absolute move over the last 8 reports (FACT, Earnings desk computation). Front IV 64.4% vs 14.9% trailing realized is event premium, not edge (INFERENCE). A declaration could also accompany tonight's release — re-check AAPL dividend before Tuesday's open (Dividend desk watch item).
2. **SPY's IV-vs-realized verdict is WINDOW-CONTINGENT.** A single day drives 32.23% of its 20-day realized variance (>30% bar), so no clean SPY verdict is offered (FACT, Premium desk stale-jump screen). QQQ sits at 29.8% — one large day from tripping the same bar. Broad single-name vol is elevated vs realized (TSLA/MSFT/NVDA +15–17pp) but event-free and tenor-mixed — a flag, not a sell signal (INFERENCE).
3. **Oil's ~6% front-month fall prices Doha hopes, not a Hormuz reopening.** Brent fell to ~$106.45 (−6.15%), WTI below $100, while Dec-2027 Brent fell only $2.41 — the curve drains a front-month war premium ~3x faster than the deferred premium (FACT, Futures desk). Attacks continued through Nov 2 and no US acceptance of terms was found. Physical tightness survives the headline: EIA crude ~4% below the 5-year average, distillates ~10% below. Next hard catalysts: EIA petroleum Wed Nov 4, 10:30 a.m. ET; USDA WASDE Tue Nov 10, 12:00 p.m. ET; OPEC+ ministerial Sun Nov 29.
4. **Rates: 10Y 4.94%, 2Y 4.56%, 2s10s +38bp, upward-sloping, mildly flattening; SOFR–EFFR +7bp, no funding stress.** (FACT, repo rates module, FRED data dated 2026-10-30.) Long rates near 5% = discount-rate pressure on growth multiples — a value lens demands a wider margin of safety on long-duration growth exposure (INFERENCE). Rho is second-order for short-dated premium vs IV.
5. **One declared dividend in the next 4 weeks: MSFT ex Thu Nov 19 at the raised $0.98/qtr, 24th consecutive annual increase.** Last purchase day Wed Nov 18 (FACT). AAPL's mid-November ex-date is projection only — UNVERIFIED until declared.

Contradictions resolved: (a) NVDA earnings date — Yahoo says Nov 17 after close; some secondary calendars say Nov 18, likely a timezone-label difference; either way it is outside the 2-week window, flagged only because it lands the next day after the cutoff. (b) Premium desk's live 1-DTE/2-DTE prints vs yesterday's file mix tenors for MSFT/NVDA/TSLA (dead 1-DTE vs live 2-DTE) — day-over-day jumps partly reflect tenor, not pure vol change (INFERENCE, disclosed). (c) Futures desk's PortWatch "2 transits Oct 25 vs 85/day" is a secondary summary, not a direct PortWatch pull — carried as UNVERIFIED, not as a verified print.

---

## 1. Earnings Event desk

| Symbol | Earnings date | Timing | Options-implied expected move | Historical avg earnings-day move (verified) |
|---|---|---|---|---|
| AAPL | Mon Nov 2, 2026 | After close; call 5:00 p.m. ET | ~4.6% (Nov 4 expiry ATM straddle) / ~5.0% (Nov 6 weekly ATM straddle) | Mean absolute first-session move 2.46% over last 8 reports; signed mean −1.53%; 2 up / 6 down |
| MSFT | Oct 28, 2026 — already reported | After close | n/a (past event) | Not computed — outside window |
| TSLA | Oct 21, 2026 — already reported | After close | n/a (past event) | Not computed — outside window |
| NVDA | Tue Nov 17, 2026 — OUTSIDE window by 1 day | After close | Not computed — outside window | Not computed — outside window |
| SPY | None | n/a | n/a | n/a |
| QQQ | None | n/a | n/a | n/a |

- FACT: Nasdaq earnings calendar for Nov 2 lists AAPL, time-after-hours, fiscal quarter ending Sep 2026, consensus EPS forecast $1.98 (7 estimates), last year's report Oct 30, 2025 at $1.85. Yahoo quote data agrees: earnings timestamp Nov 2, 2026 21:00 UTC, not flagged as an estimate.
- FACT: Nasdaq calendar checks for Nov 3, 4, 5, 6, 9, 10, 11, 12, 13, and 16 returned no AAPL/MSFT/NVDA/TSLA/SPY/QQQ entries.
- FACT (Yahoo quote snapshot ~13:28 PT, Nov 2): AAPL $338.32 vs prior close $344.63 (−1.83%) heading into the release.
- INFERENCE (calculation, not a market quote): implied move = ATM straddle mid ÷ spot ($338.32). Nov 4 expiry, 337.5 strike: call mid $8.45 + put mid $7.15 = $15.60 → 4.61%. Nov 6 weekly: $9.15 + $7.60 = $16.75 → 4.95%. Bid/ask spreads ~$0.70–$0.80, so approximate (±~0.2pp from spread alone). ATM IVs: Nov 4 call 65.7% / put 61.8%; Nov 6 call 55.4% / put 50.7%.
- FACT (own computation from Yahoo v8 daily closes): first-session returns after AAPL's last 8 after-close reports: Jul 30, 2026 −7.35%; Apr 30, 2026 +3.24%; Jan 29, 2026 +0.46%; Oct 30, 2025 −0.38%; Jul 31, 2025 −2.50%; May 1, 2025 −3.74%; Jan 30, 2025 −0.67%; Oct 31, 2024 −1.33%. Mean absolute 2.46%, signed mean −1.53%. Dates cross-checked against two independent secondary listings, agreeing on all 8 dates. Sensitivity disclosed: excluding the Jul 30, 2026 −7.35% outlier, mean absolute falls to ~1.76%.
- INFERENCE / verdict: the options market prices roughly double the recent average first-session reaction (~4.6–5.0% implied vs 2.46% historical absolute average). That gap is the decision-relevant fact: either tonight's release/guidance is expected to be unusually consequential, or the premium embeds a larger-than-usual cushion. It is NOT evidence the stock will move 5% — implied move is a breakeven, not a forecast.
- What would change this verdict: tonight's actual release (revenue, iPhone/services, holiday-quarter guidance — no release exists yet as of this run, so no statement teardown was possible; the CFA reading-order step applies to the release itself once published), the first-session close Nov 3, and any revision to the Nov 17 NVDA date.
- SPECULATION (labeled, not a claim): holiday guidance is typically the swing factor for a Q4-fiscal AAPL print; no guidance figure is verifiable pre-release, so none is stated.
- SPY / QQQ: index ETFs do not report earnings (FACT by structure).

Sources: Nasdaq earnings calendar API, https://api.nasdaq.com/api/calendar/earnings?date=2026-11-02 (and Nov 3–16 dates, same pattern); Yahoo Finance v7 quote (cookie+crumb handshake) and v7 options chain; Yahoo v8 chart for AAPL daily closes; cross-checks https://www.simianx.ai/stories/magnificent-7-earnings-dates-results-tracker and https://www.trefis.com/stock/aapl/articles/621479/apple-earnings-ahead-what-past-reactions-say-about-the-stock/2026-10-30; prior iv-inputs reference ~/workspace/hedge-desk-research/nightly/2026-11-01-iv-inputs.json (as_of 2026-11-01T14:54 PT; AAPL next_earnings 2026-11-02).

## 2. Dividend Opportunity desk

Window Nov 2–30, 2026 (next 4 weeks). Sources pulled Mon Nov 2 ~13:35–13:50 PT: Nasdaq dividends calendar API (every trading day Nov 2–30 checked individually), Nasdaq per-symbol histories (AAPL, MSFT, NVDA), Yahoo v8 chart dividend events.

| Symbol | Ex-date | Amount | Declared | Record / Payable | Flag |
|---|---|---|---|---|---|
| MSFT | Thu Nov 19, 2026 | $0.98/qtr | Sep 15, 2026 | Record Nov 19 / Payable Dec 10, 2026 | INCREASE — up from $0.91 (+7.7%); 24 consecutive annual increases per the desk count standard (count increments on announcement date; includes the Sep 2026 raise) |
| AAPL | — none declared — | — | — | — | Last ex Aug 10, 2026 ($0.27, declared Jul 30, 2026). Mid-November ex-date is pattern-plausible (2026 cadence Feb 9, May 11, Aug 10, all Mondays → Mon Nov 9) but UNVERIFIED until declared |
| SPY | — none — | — | — | — | Last distribution ex Sep 18, 2026 ($1.889, Yahoo v8). Next quarterly ex expected mid-December, outside window — INFERENCE from quarterly cadence, not a declaration |
| QQQ | — none — | — | — | — | Last distribution ex Sep 21, 2026 ($0.751, Yahoo v8). Next quarterly ex expected mid-December, outside window — INFERENCE |
| NVDA | — none — | — | — | — | Last ex Sep 10, 2026 ($0.25, declared Aug 26, 2026). Next declaration normally accompanies earnings (Nov 17), with an early-December ex-date — outside window (INFERENCE on timing). NVDA's 2026 rate already reflects an announced increase ($0.01 → $0.25, declared May 20, 2026) — past and ex'd, not a new in-window event |
| TSLA | — none; pays no dividend — | — | — | — | No dividend program (FACT — no dividend events in Yahoo history, none in Nasdaq calendar) |

- FACT: announced increases in window: MSFT only. Cuts: none. Specials: none (Nasdaq calendar sweep + per-symbol histories, cross-checked against Yahoo v8 events).
- FACT (options-relevant mechanic): MSFT's ex-date is Thu Nov 19, so the last purchase day for entitlement is Wed Nov 18, 2026.
- FACT (data quirk carried forward): Nasdaq's MSFT calendar row still shows indicated annual dividend $3.64 (4 × old $0.91); forward annualized at $0.98 is $3.92 by arithmetic. Do not quote $3.64 as the forward rate.
- INFERENCE (capture note): MSFT Nov 19 is the only actionable capture date in the window, but the $0.98 has been public since Sep 15 — no information edge attaches to the ex-date itself.
- Third-party "Nov 9/10" AAPL dates are projections, not declarations: StockLrn, DividendMax, and TalkMarkets all show a Nov 9–10 AAPL ex-date explicitly labeled estimated/forecast, while Nasdaq's per-symbol history still ends at Aug 10, 2026. Do not treat any Nov AAPL date as declared until Apple's board announces it.
- Coverage gaps, labeled honestly: Nasdaq's calendar API returned `rows: []` for Wed Nov 11, 2026 again (second consecutive run); the Nov 11 "none" rests on that empty response plus AAPL/MSFT histories — source-evidenced, not independently confirmed. Yahoo v8 dividend events live under the `dividends` key, not `dividend` — an initial wrong-key parse was corrected before any conclusion. Nasdaq's per-symbol dividends endpoint returned null data for SPY/QQQ (ETF coverage gap, covered by the calendar sweep + Yahoo fallback). Nov 26 (Thanksgiving, market closed) was not swept; no ex-date can fall on a market holiday.
- What would change this section: an AAPL board declaration — most likely with tonight's Nov 2 earnings release (re-check before Tuesday's open); an NVDA declaration pulling its ex-date into late November (cadence does not suggest it); any SPY/QQQ special distribution announcement (none indicated).

Sources: https://api.nasdaq.com/api/calendar/dividends?date=2026-11-19 (and each trading day Nov 2–30, 2026); https://api.nasdaq.com/api/quote/MSFT/dividends?assetclass=stocks, https://api.nasdaq.com/api/quote/AAPL/dividends?assetclass=stocks, https://api.nasdaq.com/api/quote/NVDA/dividends?assetclass=stocks; Yahoo v8 chart https://query1.finance.yahoo.com/v8/finance/chart/{SPY,QQQ,AAPL,MSFT,NVDA,TSLA}?range=2y&interval=1d&events=div; count standard ~/workspace/hedge-desk-research/dividend-count-standard.md; AAPL projection cross-check https://stocklrn.com/stock/AAPL/dividend, https://www.dividendmax.com/united-states/nasdaq/technology-hardware-and-equipment/apple-inc/dividends, https://www.strasmore.com/blog/aapl-dividend-2026.

## 3. Overnight Premium desk (IV)

### IV-inputs freshness — FRESH under the 26h guard, but yesterday's data
- File: ~/workspace/hedge-desk-research/nightly/2026-11-01-iv-inputs.json, as_of 2026-11-01T14:54:04−07:00 (yesterday's post-close pull), age ~22.5 hours at this run — inside the 26h guard, so accepted per the 2026-10-12 rule. It is NOT today's data: every level from that file below is labeled yesterday's post-close; today's levels come from the labeled live pull.
- FACT (data-quality note): the file's `failures` entry records the repo failover chain was unavailable (clone on a branch without it) — the file's IVs are a legacy Yahoo-only pull, not the Yahoo→CBOE failover print.

### Live Yahoo supplement — labeled live pull, 2026-11-02 13:28 PT (post-close)
Cookie+crumb handshake via curl-seeded jar worked on first attempt. Nov 2 expiries had already died at 13:00 PT, so the pull rolled to the nearest unexpired expiry per symbol and labels tenor explicitly. All ATM quotes had tight, non-degenerate bid/ask, passing the desk's stale-quote check (FACT).

| Symbol | Spot (close) | Live ATM IV | Tenor | Yesterday's file ATM IV (tenor) | 20-day realized (window Oct 5–30) | IV − realized |
|---|---|---|---|---|---|---|
| SPY | 752.15 | 15.0% | 1 DTE, exp 11-03 | 15.4% (1 DTE, exp 11-02, now dead) | 11.6% | +3.8 pp |
| QQQ | 681.09 | 26.6% | 1 DTE, exp 11-03 | 25.5% (1 DTE, exp 11-02, now dead) | 22.9% | +3.6 pp |
| AAPL | 338.32 | 64.4% | 2 DTE, exp 11-04 | 51.7% (3 DTE, exp 11-04) | 14.9% | +49.5 pp |
| MSFT | 507.12 | 37.2% | 2 DTE, exp 11-04 | 28.5% (1 DTE, exp 11-02, now dead) | 20.1% | +17.1 pp |
| NVDA | 202.06 | 46.8% | 2 DTE, exp 11-04 | 38.9% (1 DTE, exp 11-02, now dead) | 31.6% | +15.1 pp |
| TSLA | 403.82 | 53.0% | 2 DTE, exp 11-04 | 40.9% (1 DTE, exp 11-02, now dead) | 36.9% | +16.0 pp |

Tenor caution (INFERENCE): yesterday-vs-today comparisons for MSFT/NVDA/TSLA mix 1-DTE (dead) with 2-DTE prints, so day-over-day jumps partly reflect tenor, not pure vol change.

### Term structure (live, 2026-11-02 13:28 PT)
| Symbol | Front | ~7 DTE (exp 11-09) | ~25 DTE (exp 11-27) | Shape read |
|---|---|---|---|---|
| SPY | 15.2% (1 DTE) | 18.4% | 17.2% | Mild hump at 7 DTE; no event in window (INFERENCE) |
| QQQ | 26.9% (1 DTE) | 31.0% | 28.1% | Same mild 7-DTE hump (INFERENCE) |
| AAPL | 63.8% (2 DTE) | 46.0% | 31.5% | Steep downward slope — textbook earnings hump (FACT pattern; earnings today) |
| MSFT | 37.2% (2 DTE) | 36.0% | 31.1% | Gently downward; no event inside the window |
| NVDA | 46.8% (2 DTE) | 43.3% | 49.8% | 25-DTE print ABOVE front — consistent with Nov 17 earnings inside the 11-27 expiry but outside the 7-DTE window (INFERENCE) |
| TSLA | 53.0% (2 DTE) | 48.6% | 44.7% | Downward slope; no earnings in the window |

### Elevated-IV flags
1. AAPL — ELEVATED, EVENT-DRIVEN, AVOID for premium selling into the event. Front IV 64.4% vs 14.9% realized is a binary-event premium, not a mispricing (INFERENCE). Post-earnings IV crush is the expected vega collection; no "rich premium" verdict is offered on an earnings straddle.
2. TSLA, MSFT, NVDA — ELEVATED vs trailing realized (+15 to +17 pp on live front prints). No earnings inside their front windows, so this is broad vol elevation, not an event hump — but front prints are 2-DTE, and short-dated IV runs hot into weekly expiry mechanics, so the elevation is a flag, not a sell signal (INFERENCE).
3. SPY, QQQ — MILDLY ELEVATED (+3–4 pp over realized). Not a flag on its own.

### Earnings inside the window (verified against Nasdaq calendar API, 22-day sweep today)
- AAPL: TODAY, Mon 2026-11-02, after-hours (FACT). Premium into tonight's print = avoid per desk rule. This fully explains AAPL's front-IV spike (INFERENCE).
- NVDA: Tue 2026-11-17, after-hours (FACT). Inside the 25-DTE window only — explains NVDA's upward-tilting back end, not its front print.
- SPY, QQQ, MSFT, TSLA: no earnings in the next 21 days on the Nasdaq calendar (FACT). Their elevated front IVs are not earnings-driven.

### Window-contingent marks (stale-jump screen, from the 2026-11-01 file)
- SPY: WINDOW-CONTINGENT. max_single_day_variance_share = 32.23% (>30% threshold) — a single day drives nearly a third of the 20-day realized variance. Any SPY IV-vs-realized verdict built on this window is WINDOW-CONTINGENT, not clean. What would change it: the window rolling past the jump day, or a recomputation on a longer window.
- QQQ 29.8%, AAPL 13.1%, MSFT 19.2%, NVDA 24.1%, TSLA 26.1% — all below threshold, not window-contingent (FACT). QQQ at 29.8% is within a hair of the bar — treat its verdict as fragile; one more large day tips it over.

### Skew / parity observations
- FACT: call IV > put IV at the ATM strike for SPY (17.4% vs 13.1%) and QQQ (32.0% vs 21.7%) on the live 1-DTE chains. This is the reverse of typical equity skew. Read as upside-chase positioning OR post-close mark staleness (INFERENCE) — no arbitrage claim is made: quotes are post-close marks on American-style options, and a naive European parity check on them shows a gap that American exercise/dividend terms and stale marks can explain. What would change it: live intraday quotes tomorrow showing the gap persisting or collapsing.
- FACT: AAPL/MSFT/NVDA/TSLA call-put IV gaps are small (≤3 pp) — no skew signal.
- No model output in this section contradicts parity math; all IVs are Yahoo-solver prints from quoted bid/ask, not model estimates.

### IV rank — UNVERIFIED
True IV rank (percentile vs 1-year IV history) cannot be computed from free sources available to this desk — no IV-history series was retrieved. Do NOT read "elevated vs realized" above as "high IV rank." What would change it: a sourced IV-history series (e.g., a vendor or exchange history pull) for any name.

Sources: Yahoo Finance v7 options chains, query1.finance.yahoo.com, cookie+crumb auth, pulled 2026-11-02 13:28 PT; ~/workspace/hedge-desk-research/nightly/2026-11-01-iv-inputs.json, as_of 2026-11-01T14:54:04−07:00; Nasdaq earnings calendar API, swept 2026-11-02 through 2026-11-23; technique ~/workspace/custom-skills/local-cfa-financial-analysis/references/derivatives_options.md.

## 4. Open Quant/AI Model Lab

Coverage note (FACT — this run's own logs): arXiv leg covered Oct 30–Nov 2, 2026. Filtered query returned 5 items, all dated 2026-10-30; the no-filter control confirmed the newest q-fin items are 2026-10-30 (weekend submissions announce later). GitHub leg SKIPPED per the run brief's ban on GitHub operations (same as the 2026-11-01 run) — no new-repo discovery and no repo re-checks this run. Re-check leg for #9/#21/#31 FAILED transient-exhausted: arXiv API returned 503 then "Rate exceeded" on retry — no disposition changes claimed for those items; re-checks deferred to the next run. Open-dataset/API web leg surfaced only secondary vendor roundups (quantvps, Volar crypto-Deribit, MarketXLS, GEX Levels) — no new open release, all triage-excluded.

Headline: quiet sweep — 5 new candidates, all scored with the repo's own hedge_desk.research_intelligence.assess_source (run, not hand-computed). One WATCH, four ARCHIVE. No TEST, no INTEGRATE movement.

| # | Candidate | Venue / date | Scorer score | Disposition + reason |
|---|---|---|---|---|
| 201 | Lopez-Piqueres/Acharya/Sun/Kumar — Functional Tensor Trains for High-Order Greeks and Exposure Tails of Multi-Asset Structured Products | arXiv:2610.42119v1, 30 Oct 2026 | 36 | ARCHIVE — exotic structured-product machinery, not watchlist vanilla options; no author code link, reproducibility not established; third-order-Greek cost advantage is a method note only |
| 202 | Wu — "When is the deepest drawdown also the longest?" | arXiv:2610.41990v1, 30 Oct 2026 | 30 | ARCHIVE — pure drawdown probability theory, no desk lane, no code |
| 203 | Hatemi-J/Mustafa — GAUSS software component for dynamic contagion tests | arXiv:2610.41740v1, 30 Oct 2026 | 22 | ARCHIVE — crisis-contagion econometrics in commercial GAUSS software, no desk lane, no open code |
| 204 | Bai/Bian — QBX: A Compiler for Well-Formed, Auditable Alpha Programs | arXiv:2610.41689v1, 30 Oct 2026; accepted ICAIF 2026 (Milan, Nov 14–17, 2026) per arXiv comment | 50 | WATCH — availability-effect / point-in-time discipline + evidence-carrying-IR audit pattern transfers to the purged walk-forward lane (#1/#22/#54/#199); no code released yet, so reproducibility not established |
| 205 | Aichele/Cialenco/Jelito/Pitera — Expected shortfall estimation and capital coverage under overlapping scenarios | arXiv:2610.41624v1, 30 Oct 2026 | 36 | ARCHIVE — FRTB risk-capital measurement, not a desk lane (desk never touches the risk engine); overlap-bias lesson already embedded in purge/embargo discipline |

- FACT: #204 is accepted at ICAIF 2026 (arXiv comment on arXiv:2610.41689v1, read at source 2026-11-02). Its compiler rejects contract-visible look-ahead while admitting legal point-in-time forecasts (abstract, read at source).
- UNVERIFIED (source-reported, full papers not read): #204's validity rates (26.8% free strings / 36.4% grammar-only → 97.7% typed programs), 7.5× faster incremental evaluation at numerical parity, and zero contract violations across 23,342 candidates; #201's cost claims (MC >10× cheaper for deltas at 1% accuracy; hp-FTT cheaper for every third-order Greek by up to 100×; hp-FTT cheaper for every Greek at 0.1%); #205's finding that overlapping sampling roughly doubles the median covered-confidence level on market data.
- INFERENCE: #204's transferable item is its availability-checker discipline, not its A-share alpha results — the paper itself states its results concern validity/reuse/search efficiency, "not an increase in the information available from the market panel" (abstract, read at source).
- SPECULATION: none offered as a conclusion. What would change a verdict: code release for #204 (→ sandbox the availability checker in miniature on one desk backtest); any code release for #201/#205 (→ re-score, though lane fit still limits both).
- Triage exclusions (no ledger rows): quantvps / Volar / MarketXLS / GEX Levels roundups — secondary vendor summaries, no new open release; Volar is crypto-Deribit, out of scope. TipRanks / SpotGamma / Seeking Alpha earnings-week pieces — broker/vendor commentary, not research releases.
- Ledger: all five candidates appended once to the latest table (rows #201–#205) plus a run note in the Kaizen log in ~/workspace/hedge-desk-research/quant-lab-ledger.md, verified from disk by the desk agent.
- Decision-relevant takeaway: only #204 QBX is worth attention — a peer-accepted (ICAIF 2026) pattern for making look-ahead violations structurally unrepresentable in a backtest pipeline, the same failure class the desk's purged-WF lane exists to prevent. It stays WATCH until code appears; no action for the other desks this run.

## 5. Weather/War/Logistics Futures Event desk

Headline verdict: the dominant fresh catalyst is a two-sided oil shock — a ~6% intraday collapse in front-month crude on Hormuz-diplomacy hopes, against a still-tight physical inventory backdrop. The curve is pricing a negotiation, not a settlement — and that distinction is the whole trade-relevant point. Nothing here is a trade recommendation; this is catalyst triage only.

### Strait of Hormuz / Iran — diplomacy advances, attacks continue (FACT + UNVERIFIED split)
- FACT: US–Iran indirect talks via Qatar in Doha entered a third day on Nov 1–2, centred on a 48-hour plan to reopen the Strait of Hormuz. Iran's foreign minister is reported to have compressed a 5–7-day sequence to 48 hours; Tehran's stated preconditions include sanctions relief, lifting the naval blockade/interdictions, restored oil-export waivers, and release of frozen assets reported at $6–24bn.
- FACT: UK Maritime Trade Operations (UKMTO) issued notices 185–191 between Oct 29 and Nov 1 — seven notices in four days, five involving vessels struck by unknown projectiles or on fire (Oct 29 outbound tanker; Oct 29 vessel on fire 25 nm NE of Khasab; Oct 30 vessel 40 nm south of Lavan Island; Oct 30 crude tanker leaving the strait; Nov 1 Mayday inside the strait). A Nov 2 UKMTO report cited a tanker struck 72 nm east of Ras al-Khafji, Saudi Arabia, crew safe, no reported spill.
- FACT: on Oct 30, projectiles struck the Qatar-owned LNG tanker Al Mayeda near the strait, hours after Iranian authorities had granted it safe-passage clearance; the vessel reversed course.
- UNVERIFIED: the IRGC claim (Nov 1, via Iranian state media) that two tankers struck naval mines on unapproved routes, and footage of a burning supertanker, are not independently verified by maritime agencies in the sources found. Treat as regime-position reporting, not confirmed sinkings.
- UNVERIFIED / second-hand: IMF PortWatch via the Nov 1 Straits brief recorded 2 transits on Oct 25 against a pre-crisis baseline of 85/day. Directionally consistent with an effectively closed strait, but this is a single secondary summary, not a direct PortWatch pull — do not quote as a verified PortWatch print.
- INFERENCE: diplomacy and hostilities are running in parallel, not in sequence. A reopening deal that requires verifiable US sanctions relief on day one cannot be priced as done until Washington accepts terms — no source found shows US acceptance.
- What would change it: a US acceptance statement, a UKMTO-confirmed resumption of commercial transits, or conversely a confirmed strike on a laden VLCC / closure extension — any of these would flip the sign of the front-month move.

### What the oil curve is pricing — front-month premium draining, deferred curve resisting (FACT + INFERENCE)
Intraday Nov 2 readings vary by timestamp — do not compare them as if they were one close:
- FACT (Asian session): Brent ~$111.84 (−1.40%), WTI ~$102.56 (−1.50%).
- FACT (morning, ~09:42 IST / later morning): January Brent ~$109.69 (−3.30%), December WTI ~$100.60 (−3.38%).
- FACT (later session, Oilprice board via FinanceFeeds): Brent fell $6.98 (−6.15%) to $106.45, after opening at $111.69 and trading $105.86–$112.41; WTI fell 6.44% to $97.41, breaking below $100. Friday's Brent settlement was $113.43 (+2.37% on the session).
- FACT (curve shape, same board): January 2027 Brent −$6.98, but December 2027 only −$2.41, December 2028 −$0.85, December 2029 −$0.42.
- FACT: Goldman Sachs on Nov 2 raised its December Brent forecast to $105/bbl from $90, and its 2027 average to $88 from $80, citing Middle East supply risk.
- INFERENCE: the curve is draining a front-month war premium roughly three times faster than the Dec-2027 premium — i.e., the market is pricing near-term de-escalation while keeping a material risk premium in 2027. Brent at ~$106 sits within $1.45 of Goldman's new December forecast, so the "cheap oil" move has already converged on one bank's revised view, not overshot it.
- INFERENCE (watchlist link): falling oil coincided with a rebound in US equity futures after Friday's tech-led selloff (S&P futures ~+0.5% near 7,654 vs Friday cash close 7,580.07, −1.8%). That is correlation in the same session, not proof oil caused the rebound.
- What would change it: a signed reopening (front premium collapses further toward deferred levels) or a breakdown in Doha / new confirmed attack (front re-prices violently upward; the $105.86–$112.41 intraday range shows how fast that repricing runs).

### OPEC+ — December held, the real decision is Nov 29 (FACT)
- On Sun Nov 1, seven OPEC+ producers (Saudi Arabia, Russia, Iraq, Kuwait, Kazakhstan, Algeria, Oman) agreed to hold December 2026 required production at September 2026 levels — the third consecutive monthly hold (Oct, Nov, Dec). Combined required level ~31.01–31.0 million b/d (Saudi 10.478, Russia 9.949, Iraq 4.431, Kuwait 2.676, Kazakhstan 1.628, Algeria 1.007, Oman 0.841 million b/d).
- The seven completed the phased rollback of a 1.65 million b/d voluntary cut in September; a separate ~2 million b/d layer of cuts remains through end-2026. The full 21-country group meets Nov 29 to decide the 2027 framework, after a Q4 production-capacity review.
- FACT / INFERENCE boundary: required production is a policy benchmark, NOT verified physical output — multiple sources note Gulf producers remain below targets because of conflict-related export disruption, and Saudi Arabia is reported to be using its Red Sea Yanbu terminal to bypass Hormuz. Do not read the hold as "supply unchanged."
- What would change it: the Nov 29 ministerial decision on 2027 baselines/quotas, or verified output data showing Gulf exports recovering (or falling further) independent of targets.

### EIA petroleum — tight crude/distillate, loose gasoline, one data caveat (FACT)
Weekly Petroleum Status Report, released Wed Oct 28, week ending Oct 23:
- Commercial crude −1.9 million bbl to 410.6 million bbl, vs a Reuters-poll expectation of a +15,000 bbl build — the second straight weekly draw (prior week −3.2 million). Crude is ~4% below the five-year average. Cushing −624,000 bbl; Gulf Coast crude at its lowest since December 2024.
- Gasoline +3.9 million bbl to 209.2 million bbl (vs an expected ~0.9 million draw), ~2% below the five-year average. Distillates −1.5 million bbl to 102.8 million bbl (vs an expected ~0.9 million draw), ~10% below the five-year average.
- Refinery utilisation 92.8% (from 93.4%); refinery crude runs −123,000 b/d. Net crude imports −796,000 b/d; crude exports +1.4 million b/d to 4.85 million b/d. Four-week total products supplied averaged 20.8 million b/d (+0.2% y/y); the single-week figure was 20.21 million b/d (−1.022 million b/d w/w), with distillate demand +475,000 b/d to 4.21 million and gasoline demand −622,000 b/d to 8.358 million.
- CAVEAT — FACT (discrepancy reported): Kpler's lead oil analyst is reported as saying observed crude loadings were ~1 million b/d below EIA's reported export figure, raising questions about how much of the draw exports explain. This does NOT invalidate the EIA print, but it means the export-driven explanation of the draw is contested.
- INFERENCE: the physical backdrop into today's diplomacy-driven selloff was tightening, not loosening — distillate tightness into heating season is the most durable fundamental here, and it is not resolved by a Hormuz headline.
- What would change it: Wednesday's next EIA petroleum report (Wed Nov 4, 10:30 a.m. ET): a third straight crude/distillate draw confirms tightness; a build, or a downward export revision, weakens it.

### EIA natural gas — storage rebuilding, but still below last year (FACT)
Weekly Natural Gas Storage Report, released Oct 29, week ending Oct 23:
- Working gas +80 Bcf to 3,724 Bcf — above the ~70–75 Bcf consensus and above the ~77 Bcf seasonal average build, the first above-average injection since early August. Stocks are 147 Bcf (−3.8%) below last year but 38 Bcf (+1.0%) above the five-year average (3,686 Bcf).
- South Central accounted for +43 Bcf of the build (incl. 23 Bcf into salt), yet South Central remains 2.3% below its five-year average and salt storage ~11.6% below average — a regional imbalance inside a nationally adequate headline.
- EIA's October outlook forecast end-October stocks at 3,850 Bcf; the Oct 23 print (3,724 Bcf) leaves that target requiring a further ~126 Bcf in the final week. Natural gas traded ~$2.96/MMBtu on Oct 30 (−~2.4%), below $3.04–3.05 support.
- INFERENCE: gas is the mirror image of oil/distillates — adequate on the national average, tight in the salt caverns that matter for winter deliverability. A cold snap, not the average, is the risk.
- What would change it: Thursday's storage report and any sustained cold-weather forecast; a below-average build would re-tighten the winter narrative fast.

### USDA / agriculture — harvest nearly done, Nov 10 WASDE is the next hard catalyst (FACT + INFERENCE)
- FACT (official, week ending Oct 25 Crop Progress): US corn harvest 60% complete (6 points behind the five-year average); soybeans 79% (2 points ahead); winter wheat planted 76% (1 point behind last year), 53% emerged; cotton 52% (4 points ahead of normal). Final condition ratings: corn 56% good/excellent.
- FACT (Nov 2 analyst expectations, not official): ADM/Archer desks look for corn ~74–75% and soybeans ~90% as of Nov 1; today's Crop Progress report is due Monday afternoon (4 p.m. ET) and was not yet incorporated in the sources found at desk time — do not treat the 74%/90% figures as USDA prints.
- FACT: Brazil planting is ahead of pace — Mato Grosso soybeans 89% (vs 76% year-ago, 78.5% five-year average); Brazil first-crop corn 63% (vs 59% year-ago), total Brazil soybean planting 53% (vs 47% year-ago). USDA flash sales Nov 2: 1.730 million tonnes corn to Mexico (45m bu 26/27, 23m bu 27/28) and 136,000 tonnes soybeans to China. US corn export inspections (35m bu) are tracking well below the pace needed for the USDA forecast (YTD −13% y/y vs forecast −4%); soybean inspections (90m bu) are ahead (YTD +56% vs forecast +12%).
- FACT (positioning): managed money cut corn net longs by 90,314 contracts to 55,943 (smallest in 4 months) and soybean-complex longs by ~70,000 to 411,500 (lowest in 2 months) as of Oct 27 CFTC.
- FACT (calendar): USDA's 2026 calendar lists the next WASDE + Crop Production at Tue Nov 10, 12:00 p.m. ET. The October WASDE was released Oct 9 (WASDE-676) on schedule.
- Government-data note — FACT per standing rule, applied: no shutdown/blackout framing is used. Stale 2025 shutdown stories (Nov 2025 WASDE postponement to Nov 14) appeared in search results and were disregarded — they describe the 2025 episode, not 2026, and the standing user-verified rule (CR passed Sep 1, signed Sep 2, funding through Dec 11; September jobs released normally) plus USDA's own 2026 calendar govern. The desk did not apply brief-correction-2026-10-05.md.
- INFERENCE: grains enter the Nov 10 WASDE with a soft fundamental tape (corn at a 4-month low near $4.51 Dec-26, funds exiting longs, corn export pace lagging) — the WASDE is therefore a clearing event with more downside air than upside, but that is positioning inference, not a USDA forecast.
- What would change it: the Nov 10 WASDE yield/ending-stocks revisions; today's Crop Progress (if corn closes the 6-point gap, the lag narrative weakens); a weather shift — widespread midsection showers this week are expected to slow remaining harvest, with week 2 above-normal temperatures / below-normal precipitation.

### Logistics / freight — container rates easing, not a Hormuz proxy (FACT)
- Drewry World Container Index fell 3% to $4,429 per 40-ft container on Oct 29, driven by Transpacific: Shanghai–Los Angeles −6% to $7,514, Shanghai–New York −5% to $9,631; Shanghai–Rotterdam +1% to $3,686, Shanghai–Genoa flat at $4,151. Carriers announced six Transpacific blank sailings next week (vs five this week); NRF forecasts US ocean imports −11% in November vs October.
- INFERENCE: container easing is a demand/Transpacific story, not evidence that Gulf energy logistics are easing — the two freight markets are pricing different things. Do not use Drewry as a Hormuz reopening signal.
- FACT (energy logistics cost): ADNOC's CEO said Nov 2 at ADIPEC that shipping/logistics costs have risen from below 5% to over 30% of the cost of a barrel, and that ~1 billion barrels have been drained from global inventories since the Hormuz disruption; diesel stocks in some markets are at their lowest seasonal levels in 35 years, with a 600 Bcf LNG supply gap cited. These are executive claims at a conference, not independently audited inventory figures — label the 1-billion-barrel figure as a cited claim, not a verified stock count.

### Calendar — what to watch this week
| Date | Event | Why it matters |
|---|---|---|
| Mon Nov 2, 4 p.m. ET | USDA Crop Progress | Confirms/denies the 74%/90% harvest expectations |
| Tue Nov 3 | US midterm elections | Cited by oil desks as a background support for crude prices; outcome UNVERIFIED at desk time |
| Wed Nov 4, 10:30 a.m. ET | EIA Weekly Petroleum Status Report | Tests whether crude/distillate tightness extends to a third week |
| Thu (weekly) | EIA Natural Gas Storage Report | Tests winter-deliverability (salt) vs national-average adequacy |
| Tue Nov 10, 12:00 p.m. ET | USDA WASDE + Crop Production | First post-harvest supply/demand reset; grain clearing event |
| Sun Nov 29 | OPEC+ full ministerial | 2027 production framework and baselines |

Sources: EIA petroleum (Oct 28, week ending Oct 23): https://1027wbow.com/2026/10/28/us-crude-and-distillate-inventories-fall-gasoline-stocks-rise-eia-says/, https://skn-finance.com/skn-us-crude-and-distillate-inventories-fall-as-oil-exports-rise-eia-reports/, https://www.fxempire.com/forecasts/article/crude-oil-weekly-price-forecast-oil-continues-to-see-dip-buying-1641644; oil Nov 2 intraday / curve / Goldman: https://financefeeds.com/oil-prices-fall-6-brent-106-wti-breaks-100/, https://www.thehindubusinessline.com/markets/commodities/crude-oil-futures-fall-as-diplomatic-efforts-to-end-iran-us-war-continue/article71655302.ece, https://www.fxempire.com/forecasts/article/natural-gas-and-oil-forecast-iran-talks-drag-on-and-opec-holds-steady-can-wti-hold-99-61-1641842, https://www.samuelandcotrading.com/us-open-market-brief-2-november-2026-cheaper-oil-buys-a-breather/; Hormuz / UKMTO / Doha talks: https://www.novusdata.news/briefings/briefing-2026-11-02, https://geopolitics.pibrief.com/editions/2026-11-02, https://straits.live/briefs/2026-11-01, https://regionalert.com/blog/hormuz-strait-oil-shipping-intelligence-2026.html, https://oilprice.com/Latest-Energy-News/World-News/ADNOC-Chief-Says-World-Has-Eroded-Its-Supply-Buffers.amp.html; OPEC+ Nov 1: https://katcountry989.com/2026/11/01/opec-set-to-keep-oil-output-targets-steady-sources-say/, https://www.tradingview.com/news/seekingalpha:f67204693094b:0-opec-producers-hold-december-oil-output-steady-amid-market-uncertainty/; EIA natural gas (Oct 29, week ending Oct 23): https://www.oilandgas360.com/weekly-gas-storage-10-23/, https://tradersunion.com/news/commodities/show/4034194-natural-gas-slides-below-3-00-as-eia-inventory-surprise-deepens-bearish-pressure/; USDA / grains Nov 2: https://www.admis.com/ag-market-view-for-nov-2-2026/, https://blog.pricegroup.com/2026/11/02/spooked-ag-marketing-report-11-02-2026/, https://www.archerfinancials.com/feed-grains-up-soybean-complex-mixed/, https://agsist.com/usda-calendar, https://www.usda.gov/oce/commodity/wasde; freight: https://www.novusdata.news/briefings/briefing-2026-11-02 (Drewry section).

## 6. Box/Parity Observer

Bottom line: no new exploitable put-call/box parity violation found today. One material index-methodology item carried forward: the S&P style overhaul effective Dec 21, 2026, with pro-forma files Dec 4. One directly box-relevant paper is timely for year-end expiries.

### Index methodology — S&P style indices (FACT, via secondary reporting of S&P Dow Jones Indices announcement)
- S&P Dow Jones Indices adopted revised growth/value classification rules, effective before market open Mon Dec 21, 2026, at the annual reconstitution; preliminary/pro-forma files from Fri Dec 4, 2026. Consultation ran Sep 4–25, 2026.
- Growth: 12-month price momentum removed; ranking now on 3-year EPS-change-to-price and 3-year sales-per-share growth.
- Value: traditional book-to-price replaced by an intangibles-adjusted measure; trailing earnings-to-price averaged with 1-year forward earnings-to-price; sales-to-price retained; free-cash-flow-to-price added (excluded for real estate, banks, insurers, mortgage REITs and certain financials).
- Scope: S&P 500, Composite 1500, MidCap 400, S&P 900, SmallCap 600 and S&P 1000 style and Pure Style indices.
- Reported estimate: Bloomberg Intelligence's James Seyffart put at least $375B in passive funds tied to the affected gauges — INFERENCE/UNVERIFIED as a primary figure: reported via secondary sources, not verified against the S&P release itself.
- Sources: https://www.tradingview.com/news/benzinga:b353d12e7094b:0-s-p-changes-the-rules-here-s-new-value-vs-growth/, https://el7.ai/en/news/2026-10-28-sp-dow-jones-updates-growth-and-value-criteria-triggering-major-etf-rebalancing
- Desk read (INFERENCE): this is a style-classification change, not a stated change to S&P 500 membership itself — so do not read it as a direct SPY constituent change. The reshuffle pressure falls on style trackers (e.g. IVW/SPYG/IVE, cited at ~$77B/$57B/$50B in the same secondary reporting). Watch Dec 4 pro-forma files for watchlist-name style migration (notably AAPL/MSFT/NVDA classification shifts), not for a parity signal.
- Also noted, not watchlist-direct: FTSE Russell is separately consulting on its 50/50 growth-value split, closing Dec 11, 2026 (FACT, secondary reporting).

### Parity / box — no new violation; year-end box caveat (FACT from paper abstracts)
- No new published, exploitable parity-violation analysis for SPY/QQQ or watchlist names was found in today's sweep. Recent 2026 items found were educational explainers only (put-call parity formula, SpotGamma box-spread guide), not new empirical violation evidence: https://spotgamma.com/box-spread-strategy/
- Relevant to December boxes: Useong Shin, "The Year-End Toll: Frictions Embedded in Option-Implied Rates" (Sep 18, 2026), using SPX and RUT options 2012–2025, finds a 2–3 bp unannualized increase in the option funding basis when maturity first crosses Dec 31, behaving as a fixed price wedge (FACT from abstract). The paper's point is that a riskless box payoff does NOT by itself prove the option-implied rate is frictionless: https://arxiv.org/pdf/2609.20224v1
- Desk read (INFERENCE): do not interpret a small year-end box-rate premium over Treasuries/OIS around the Dec 21 reconstitution / Dec 31 crossing as a clean arbitrage or as a pure convenience-yield signal without allowing for this funding/balance-sheet wedge. Deterministic parity still governs: C + PV(K) = P + S for European options (SPX-style); when a model disagrees with that identity, the math wins — the wedge above is a friction to explain, not a violation to trade. No trade is proposed (paper-only desk).

### Nothing else material
- No new Nasdaq-100 methodology announcement found today; the May 1, 2026 Nasdaq-100 fast-entry / 3x-float-cap change is prior background, not new.
- No new published parity-violation study specific to SPY, QQQ, AAPL, MSFT, NVDA or TSLA found today — marked UNVERIFIED if claimed otherwise, not assumed.

## 7. Bonds & Rates desk

Status: COMPLETE — module ran successfully (mode: REAL_FRED_RATES, source: fred-public-csv-http-200). No Yahoo yields substituted.

### Module output (verbatim numbers)
| Series | Level | Latest date |
|---|---|---|
| Fed funds effective rate (DFF) | 3.88% | 2026-10-30 |
| Treasury 2Y (DGS2) | 4.56% | 2026-10-30 |
| Treasury 10Y (DGS10) | 4.94% | 2026-10-30 |
| SOFR | 3.95% | 2026-10-30 |
| EFFR | 3.88% | 2026-10-30 |
| OBFR | 3.88% | 2026-10-30 |
| 2s10s spread | 38 bp (module: spread_10y_2y_points 38.00; curve_slope 0.047500) | — |
| Curve shape | UPWARD_SLOPING | — |
| Fed funds change over 60-day window | 0.25 (as reported by module; sign convention not stated in output) | — |

Module as_of: 2026-11-02; all series observations dated 2026-10-30 (Friday's close — the latest trading day before this Monday run, so this is current, not stale). (FACT — module output.)

### Slope and direction of change
- 2s10s = +38 bp, upward-sloping, no inversion. (FACT — computed from module levels: 4.94 − 4.56 = 0.38)
- Direction: mild flattening over the 60-day window. On 2026-09-03 the module's history gives 10Y 4.77% − 2Y 4.34% = 43 bp; by 2026-10-30 that gap narrowed to 38 bp (−5 bp). (FACT — computed from module history)
- Both ends fell over the last month: 10Y from its window peak of 5.29% (2026-09-30) to 4.94% (−35 bp); 2Y from 4.92% (2026-09-28) to 4.56% (−36 bp). The curve moved down roughly in parallel, hence the near-stable slope. (FACT — module history)
- Note on labeling: the 2Y here is FRED DGS2, not a Yahoo ticker. Per standing rule, ^FVX is the 5Y and is never labeled 2Y; no Yahoo yield is used in this desk section. (FACT)

### Funding stress gauge: SOFR vs EFFR
- SOFR − EFFR = +7 bp (3.95% − 3.88%). OBFR equals EFFR at 3.88%. (FACT — computed from module levels)
- Read: a 7 bp SOFR premium over EFFR is a modest, unremarkable funding spread — no sign of funding stress in this snapshot. (INFERENCE — spread is small and positive, not spiking; no stress threshold is defined in the module output, so this is a judgment, not a module verdict)

### Directional read for premium pricing (watchlist: SPY, QQQ, AAPL, MSFT, NVDA, TSLA)
- Long rates remain elevated in absolute terms (10Y 4.94%, 2Y 4.56%) even after the October decline. (FACT)
- Higher long rates = higher discount rates = pressure on growth multiples. (INFERENCE — standard valuation mechanics) The duration-sensitive watchlist names (NVDA, TSLA, MSFT, and QQQ broadly) carry the most multiple risk from this level; a value lens favors demanding a wider margin of safety on long-duration growth exposure while the 10Y sits near 5%. (INFERENCE)
- Curve shape implications: an upward-sloping, non-inverted curve gives no recession signal from 2s10s, and the mild flattening (not steepening) argues against a fresh term-premium blowout story. (INFERENCE)
- For premium specifically: rates are a second-order input (rho) versus implied vol for short-dated premium; the rates backdrop matters here mainly through the multiple/discount-rate channel above, not as a direct premium signal. (INFERENCE)
- What would change this read: a 10Y break back above ~5.3% (window peak) or a 2s10s inversion would flip the read to rate-pressure intensifying / recession-signal territory; a sustained 10Y drop below ~4.75% would ease the multiple-pressure case. (SPECULATION — stated thresholds are judgment anchors, not forecasts)

All levels, dates, and history points above are FACT per the repo's own rates module (FRED public CSV, HTTP 200). Slope arithmetic is computed directly from those module outputs. Multiple-pressure and funding-stress interpretations are labeled INFERENCE. No numbers are UNVERIFIED and none are guessed; no Risk of Ruin estimate is made and no trade is proposed.

---

## Desk coverage statement
All seven desks produced output this run: Earnings, Dividend, Premium IV, Quant Lab, Futures Catalysts, Parity, Bonds & Rates. No desk was silently dropped. Partial gaps, labeled in-desk: Quant Lab GitHub leg skipped per the no-GitHub-operations ban and its #9/#21/#31 re-checks deferred after transient arXiv 503/rate-limit errors; Premium IV rank UNVERIFIED (no free IV-history series); Futures PortWatch transit count carried as secondary-summary UNVERIFIED; Dividend Nasdaq Nov 11 calendar response empty (second consecutive run).
