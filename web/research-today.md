# Hedge-Desk Daily Research — Sun 2026-10-18 (~13:30 PT)

**Run:** `hedge-desk-daily-research` · paper-only, research + input only (no git, no PRs, no code changes).
**Market state:** US equities and bonds CLOSED (Sunday). Futures reopen ~15:00 PT today. All price/quote as-ofs are Fri Oct 16 close unless noted.
**Standing rules applied:** Yahoo-first with `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; ^TNX=10Y, ^FVX=5Y (never 2Y), 13W=front-end anchor (never "2Y"); no shutdown framing (CR through Dec 11); MSFT dividend streak = 24 (incl. Sep 2026 raise); every material claim labeled FACT / INFERENCE / SPECULATION / UNVERIFIED.
**IV inputs:** `nightly/2026-10-17-iv-inputs.json`, `as_of` 2026-10-17T13:54:25-07:00 — ~23.5h old at run start, INSIDE the 26h guard → usable baseline. Supplemented by a labeled live Yahoo pull (Sun 13:35 PT, quotes Fri 16:00 ET).

---

## Desk 1 — Earnings Event desk

**Question:** What are the confirmed earnings dates, timings, and options-implied expected moves for the watchlist through Nov 1, and what changed since yesterday?

| Symbol | Date | Timing | Implied move (as of Fri Oct 16 close) | Historical earnings-day move | Status |
|---|---|---|---|---|---|
| TSLA | Wed Oct 21, 2026 | AMC — FACT (Nasdaq `time-after-hours`; corroborated Zacks, TipRanks, Tesla IR) | **7.41%** — FACT (Oct 23-expiry straddle $26.27 ÷ $354.72; unchanged, markets closed) | Mean \|move\| 7.77%, median 4.46% — FACT (8 qtrs, yesterday's series, unchanged) | In-window, 2 trading days out |
| MSFT | Wed Oct 28, 2026 | AMC — FACT (Nasdaq `time-after-hours`) | **6.04%** — FACT (Oct 30-expiry straddle $31.95 ÷ $529.05; unchanged) | Mean \|move\| 7.02%, median 6.12% — FACT (unchanged) | In-window |
| AAPL | **Mon Nov 2, 2026** | AMC — **issuer-confirmed** FACT (Apple IR page, reported Oct 6; release 1:30 PM PT, call 2:00 PM PT) | UNVERIFIED this run (no chain pull; markets closed) | UNVERIFIED this run (carry yesterday's ~1.9% only as yesterday's number — do not quote) | 1 day outside 2-wk window; in weekly expiries |
| NVDA | Nov 18, 2026 | UNVERIFIED (Nasdaq `time-not-supplied`; one secondary says Nov 17) | n/a (no in-window expiry) | n/a | Outside window |
| SPY/QQQ | — | No earnings — FACT (ETFs) | — | — | — |

**New/changed vs yesterday (all FACT unless noted):**
1. **AAPL Nov 2 upgraded to issuer-confirmed** — resolves yesterday's "Monday placement is atypical, re-verify" caveat. INFERENCE: Monday coincides with new-CEO optics — first call for **John Ternus**, who succeeded Tim Cook Sep 1, 2026 (corroborated by multiple secondaries) — a communication-risk variable not priced in prior quarters.
2. **AAPL July guidance surfaced** (per same IR coverage): FQ4 revenue +9–11% y/y on $102.47B → **$111.69–113.74B** (recomputed 102.47×1.09=111.69, ×1.11=113.74 ✓); gross-margin guide **47–48%** (vs 50.1% in June, which carried ~2pp tariff-refund benefit); iPhone mid-teens growth; supply constraints + surging memory pricing cited. MarketBeat consensus EPS $1.99 / revenue $113.38B (matches Nasdaq EPS $1.99 exactly); 8-of-8 beat streak (MarketBeat, basis UNVERIFIED).
3. **TSLA primary check:** SEC EDGAR 8-K (filed Oct 2, read directly) confirms Q3 deliveries **486,532** (+5.3% vs Tesla-compiled consensus 461,974; −2.1% y/y vs record 497,099 — both recomputed, signs check) but does NOT announce the earnings date; Oct 21 AMC rests on Nasdaq + Zacks/TipRanks/IR corroboration. Nasdaq EPS $0.21 vs Zacks/TipRanks $0.44–0.45 = **different bases; do not mix** — basis UNVERIFIED. Webcast 5:30 PM ET secondary-reported, corroborated, not primary-verified.
4. **NVDA date disagreement persists:** Nasdaq Nov 18 vs one secondary Nov 17 — UNVERIFIED, unchanged.
5. No reschedulings; Nasdaq calendar swept Oct 19 → Nov 2 day-by-day: only TSLA Oct 21 and MSFT Oct 28 AMC on watchlist names.

**Premium-relevant reads:** TSLA implied 7.41% ≈ hist mean 7.77% (well above median 4.46%) — market pricing the fat-tail history (INFERENCE) → premium into this binary = avoid. MSFT implied 6.04% ≈ hist median 6.12% — roughly in line (INFERENCE). AAPL Nov 2 sits one day outside the stated window but inside weekly option expiries — flagged for the Premium desk.

**Sources:** Nasdaq earnings calendar API (swept 2026-10-19 → 2026-11-02, 2026-11-18); SEC EDGAR `https://www.sec.gov/Archives/edgar/data/1318605/000162828026064366/tsla-20261002.htm`; Apple IR coverage via MacRumors/9to5Mac Oct 6; MarketBeat; Zacks (Oct 13); TipRanks.

---

## Desk 2 — Dividend Opportunity desk

**Question:** Do any watchlist names go ex-dividend in the next 4 weeks (through Nov 15), and has anything changed — increases, cuts, specials — since yesterday?

**Verdict: Nothing goes ex-dividend in the window. No new increases, cuts, or specials since yesterday.**

| Symbol | Ex-div in window? | Next ex-div | Amount | Pay date | Change vs prior | Streak count (per standing standard) |
|---|---|---|---|---|---|---|
| SPY | None — FACT | ~mid-Dec 2026, UNVERIFIED (pattern) | Last: $1.889 (ex Sep 18, 2026) — FACT | — | None — FACT | N/A (variable ETF distribution) |
| QQQ | None — FACT | ~mid-Dec 2026, UNVERIFIED (pattern) | Last: $0.7514 (ex Sep 21, 2026) — FACT | — | **Framing correction:** secondaries calling $0.8135→$0.7514 a "cut" is misleading — variable ETF-distribution noise, not a corporate cut (amounts FACT; cause INFERENCE) | N/A |
| AAPL | None — FACT (not yet declared) | ~Nov 9–10, UNVERIFIED (pattern; declaration expected with Nov 2 earnings) | Last: $0.27 (ex Aug 10, 2026) — FACT | — | None — FACT | **15** (2012 initiation + 2013–2026) |
| MSFT | None — FACT | **Nov 19, 2026** — FACT | **$0.98** — FACT | Dec 10, 2026 — FACT | Sep 15, 2026 raise $0.91→$0.98 (+7.7%/8%) — FACT | **24** (incl. Sep 2026 raise; initiated 2003) — per standing standard |
| NVDA | None — FACT | ~early Dec 2026, UNVERIFIED (not yet declared) | Last: $0.25 (ex Sep 10, paid Oct 1) — FACT | — | None — FACT ($150B buyback authorized Sep 28 = separate capital-return channel, not a dividend change — FACT) | **1** (2026 only; flat $0.01 in 2024–25 broke any earlier run) |
| TSLA | None — FACT | None expected — INFERENCE | $0 — FACT | — | None — FACT | 0 (non-payer) |

**New vs yesterday:** effectively nothing material. (1) MSFT ex-date **re-verified against Microsoft's own Sep 15, 2026 press release** — ex Nov 19, 2026; record Nov 19 (same-day under T+1); pay Dec 10; annual meeting Dec 8 (FACT, non-decision-relevant). Yesterday's "ex Nov 19" was correct. (2) Nasdaq dividend-calendar sweep Oct 19–Nov 17 returned zero watchlist rows — FACT. (3) QQQ "cut" reframing (above).

**What would change it:** AAPL — Nov 2 earnings declaration sets November ex-date/amount (UNVERIFIED until then; a $0.27 hold keeps the 15-streak). NVDA — Nov 18 earnings declaration sets December ex-date (amount UNVERIFIED). MSFT — only a board reversal (no signal).

**Sources:** Nasdaq dividends calendar API (swept 2026-10-19 → 2026-11-17); Nasdaq MSFT dividend history endpoint; Microsoft press release (primary issuer source); Yahoo chart API v8 (UA header); `dividend-count-standard.md`.

---

## Desk 3 — Overnight Premium (IV) desk

**Question:** With Friday-close quotes and Monday's expiry 1 DTE away, is watchlist option premium rich or cheap versus trailing realized vol, and which names are distorted by binary events or stale single-day jumps?

**Inputs:** baseline `nightly/2026-10-17-iv-inputs.json` (as_of 2026-10-17T13:54:25-07:00, ~23.5h old, inside 26h guard — USABLE); live Yahoo options pull Sun 13:35 PT (quotes Fri 16:00 ET). Front expiry Mon Oct 19 (1 DTE); back expiry Nov 12 (25 DTE). Note: Yahoo now 401s without session cookie + crumb — recovered via cookie-crumb flow (poka-yoke: bake this into future runs).

| Sym | Baseline ATM IV (Oct 19) | Live ATM IV (Oct 19) | Live IV (Nov 12) | Realized 20d (9/21–10/16) | IV−RV (live) | Verdict | Binary-event note |
|---|---|---|---|---|---|---|---|
| SPY | 0.1135 | 0.1390 | 0.1508 | 0.0900 | +0.049 | **RICH — clean** (not contingent) | none |
| QQQ | 0.1932 | 0.2366 | 0.2335 | 0.1543 | +0.082 | **WINDOW-CONTINGENT** (0.3559) | none |
| AAPL | 0.2053 | 0.2514 | 0.2948 | 0.1646 | +0.087 | **WINDOW-CONTINGENT** (0.3737) | earnings 11-02 in Nov-12 window |
| MSFT | 0.1987 | 0.2434 | 0.3512 | 0.2234 | +0.020 | **WINDOW-CONTINGENT** (0.3485) | earnings 10-28 in Nov-12 window |
| NVDA | 0.3014 | 0.3691 | 0.3682 | 0.2368 | +0.132 | **RICH — clean** (not contingent) | earnings 11-18 outside both windows |
| TSLA | 0.3544 | 0.4340 | 0.4932 | 0.3001 | +0.134 | **WINDOW-CONTINGENT** (0.3136) | **earnings 10-21 in-window → AVOID** |

**Term structure (live, Fri-close quotes):** SPY 0.139→0.151 (normal upward slope, no event hump — FACT, no SPY earnings); QQQ 0.237→0.234 (flat/slightly inverted front); AAPL 0.251→0.295 and MSFT 0.243→0.351 (earnings humps in Nov-12 expiry — expected, not "rich," per sanity check: event inside window); NVDA 0.369→0.368 (flat — consistent with Nov-18 earnings *outside* both expiries); TSLA 0.434→0.493 (earnings hump + elevated front).

**Decision-relevant items:**
1. **TSLA Oct-21 earnings in-window: premium into a binary event = avoid.** Elevated IV is event-expected, not edge (FACT: date; INFERENCE: elevation is event-driven).
2. **NVDA is the cleanest rich-premium read on the board:** live IV +13.2pp over trailing realized, NOT window-contingent, no earnings inside either pulled expiry — elevation without an event (FACT: spread + flat structure; INFERENCE: unjustified by events).
3. **SPY clean-rich too (+4.9pp over realized, not contingent).** Baseline→live gap on the same expiry (0.1135→0.1390, same Friday quotes) is mechanically consistent with unchanged dollar prices and shrinking time to expiry — INFERENCE from the math, not a regime read. All four single-name earnings are excluded from the front Oct-19 expiries.

**Fail-closed notes:** IV-rank claims = **UNVERIFIED for all names** — no free IV-history source; richness judged only on IV-minus-realized proxy, labeled as such. Contingent names (QQQ/AAPL/MSFT/TSLA) get clean verdicts only after the jump-day rolls out of the 20-day window. No trade framing (paper-only).

**Sources:** baseline file (above); Yahoo Finance options API (Sun 13:35 PT pull); Nasdaq quote-info cross-check (Fri closes: SPY 763.25, QQQ 709.80, AAPL 343.46, MSFT 529.05, NVDA 214.13, TSLA 354.72).

---

## Desk 4 — Open Quant/AI Model Lab

**Question:** What new papers, repos, datasets, and free APIs relevant to the desks appeared since the 2026-10-17 sweep, and which are worth testing or watching?

**Sweep result: quiet weekend.** arXiv leg EMPTY (INFERENCE from control: no-filter query showed newest q-fin items dated Oct 15 — arXiv announces weekdays only; the date-filtered leg 500'd, classified transient, control stands). GitHub leg: 6 queries over repos created Oct 17→18; 9 excluded at triage (all NOLICENSE — unusable per precedent; 3 more out of scope). Six MIT-licensed candidates verified at source via GitHub API, READMEs read, scored with the repo's `assess_source`.

| # | Candidate | Desk | Score / Disposition | Reason |
|---|---|---|---|---|
| 104 | spx-vol-surface-forecasting (manidmt) | Premium | 37 / ARCHIVE | Master's thesis; notebooks-only, no results yet; data Bloomberg-proprietary, irreproducible from repo |
| 105 | options-engine (oscarschjelderup-sketch) | Premium/Parity | 61 / WATCH | BSM/CRR/MC pricers agree; Greeks 3 ways; SVI per-expiry w/ butterfly+calendar checks; QuantLib cross-checks; CI+tests. 0 stars, created 10-17 → credibility capped. Follow-up: sandbox pytest vs #33 |
| 106 | options-backtester (Scott-Switzer) | Premium | 61 / WATCH | 8 pricing models + blender; arb-rejecting IV solver; backtester crosses spread + commissions; synthetic data explicitly labeled synthetic (fail-closed framing). Follow-up: blender vs #18/#32/#33/#105 |
| 107 | regime-aware-option-pricing (apimaezekiel-arch) | Premium | 49 / WATCH | Honest in-progress MSc: regime-conditional OOS protocol, "not empirical findings" caveat. At WATCH floor; re-check empirical phase |
| 108 | options-pricing (Yleo-Aubry) | Parity | 43 / ARCHIVE | Clean C++17 FD BS-PDE solver, but European-BS-only course project; lanes covered by #33/#22/#105 |
| 109 | options-strategy-backtester (SriharshaPotta) | Premium/Earnings | 55 / WATCH | CUDA MC engine (benchmarks source-reported UNVERIFIED) + strategy ranker on live chains; React dashboard. Follow-up: verify benchmarks; ranker on watchlist earnings names |

**Nothing reached TEST (max 61) or INTEGRATE — band discipline held** (TEST opens only on sandbox evidence, not interest). Re-checks: license blocks on #1/#20/#32/#86 unchanged (repos untouched); #87 conformalForecast still live on CRAN; #35 VolPaint still no code.

**Ledger:** 6 rows (#104–#109) + 2026-10-18 jidoka/kaizen entries appended to `quant-lab-ledger.md` (grep-verified). Standard work — no candidate lives only in this daily file.

**What would change dispositions:** sandbox pytest evidence (#105/#106/#109); empirical phase results (#107); license release on blocked repos; completed thesis with reproducible data (#104).

---

## Desk 5 — Futures Event desk (Weather/War/Logistics)

**Question:** What changed in futures-relevant catalysts since yesterday's run, and what does the Sunday picture imply for the week ahead?

### REPORTED FACTS (markets closed Sunday — last session Fri Oct 16; futures reopen ~15:00 PT today)

**A. Hormuz escalation — the weekend's dominant catalyst (NEW since yesterday)**
- Iran's Revolutionary Guards Navy said Saturday that **two oil tankers caught fire after striking naval mines** while crossing the Strait of Hormuz, each carrying ~2M bbl (~4M bbl total). No independent confirmation. IRNA said the vessels had switched off positioning/radar and used an "unauthorised route" (Reuters, Sat Oct 17).
- Iranian FM Araqchi said Sunday that Iran's offer to **reopen Hormuz within seven days is still on the table**; Tehran's conditions include lifting the US blockade/sanctions and ending regional hostilities; Washington insists on addressing the nuclear program first; negotiations stalled last week (Reuters, Sun Oct 18).
- US/CENTCOM (via Hindu Business Line, Sun Oct 18): **97% of ships transit safely**; ~400 commercial vessels moved ~100M bbl through the strait under naval escort in the week ending Oct 17.
- Friday's settles corroborated by CNBC citation: Brent **$109.86** (+3.7%, touched $110 intraday, highest since May) and WTI **$101.41** (+3.5%) (blog citing CNBC, Oct 18).

**B. Saudi/Houthi front widens (NEW)**
- Saudi MoD confirmed interception of **two ballistic missiles and a UAV launched by Houthis** (globalarabnetwork, Sun Oct 18).
- Conflict Armament Research report (secondary): Houthis building a Kheibar Shekan-derived missile from Chinese-supplied components, ~1,200-mile range (QNC News, Oct 18; production status unclear).

**C. Natural gas — Europe tightens, US stays supplied (NEW texture)**
- European gas hit a **3.75-year high Friday**; EU storage 74% full (Oct 14) vs 89% seasonal average. US LNG flows 20.5 Bcf/d (+6.2% w/w); Lower-48 production 113.9 Bcf/d (+5% y/y, BNEF); TCO/Columbia outage expected resolved Saturday (FXEmpire, Oct 18).
- AGA (Oct 16, primary industry source): EIA STEO projects winter-entry storage ~**2% above** the 5-year average; Nov Henry Hub settled **$3.24** Oct 15; US production on pace for a new annual record.
- ⚠️ PROVIDER CONFLICT (reported, not resolved): FXEmpire says EIA sees end-Oct storage at **3,985 Bcf** (+5% vs avg); TradingNews/AGA cite **3,850 Bcf** (+2%). Both cite EIA. Not reconciled — do not quote either as settled.

**D. Grains — Chinese buying returns (NEW to this desk)**
- USDA confirmed its first flash soybean sale to China in ~3 weeks: **470,000 MT** for 2026/27 delivery (Dow Jones via Morningstar, Oct 14).
- Week recap (Texas Hedge Risk, Oct 16): Dec corn **$4.74¼** (post-WASDE slide continues), Nov soybeans **$12.61¼**, Dec Chicago wheat **$6.59¾**, KC wheat **$7.04**; winter-wheat planting 51% vs 58% avg; Midwest rain slowed harvest.
- No new Crop Progress until **Mon Oct 19 ~4pm ET**.

**E. Unverified / single-source (labeled, not folded into verdicts):** Trump waiving Graham Act energy-buyer penalties (Substack only); DOE 17M-bbl SPR exchange RFP Fri Oct 16 (FinanceFeeds, no second source); IRGC declaring Hormuz "closed" Saturday (regionalert/financialports only); EU postponing Oct 24 Gulf summit (arc-codex only); AAA diesel $6.33/gal (blog-only citation).

**F. Curve state (UNCHANGED — no new session):** WTI backwardated Nov $101.41 → Mar $93.53 (−7.8%); Brent Dec $109.86 (Brent–WTI Dec +$10.84); nat gas contango to Jan $3.759 peak then collapsing to Apr $2.564; corn/soy/wheat all in carry. Next price read: futures reopen ~15:00 PT today.

### INFERENCE (separated)
1. The mine strikes mark a **tactical escalation** from projectile attacks to area-denial (mines), even if the IRGC claim is unconfirmed — higher war-risk premiums and slower non-escorted transits regardless of exact hull count. *Changes if:* wire-confirmed damage reports (UKMTO/owners) or sustained escorted-throughput data contradicting disruption.
2. Iran's still-on-the-table 7-day offer vs US nuclear-first stance = **diplomacy is a floor under resolution, not a priceable event** — preconditions incompatible as stated; crude's ~$8 fade by March remains the market's priced "disruption half-life," with wider two-sided tail risk. *Changes if:* verifiable acceptance terms, ceasefire, or confirmed multi-week attack halt.
3. Nat gas divergence widens: Europe (74% vs 89% storage, 3.75-yr-high price) is the real tightness story; US (production records, mild weather, TCO restored) is capped. *Changes if:* Thursday's EIA build vs ~87 Bcf seasonal norm, or a 10–15-day model flip to sustained cold.
4. Soybean China sale vs record harvest = "China vs the harvest" balance — a marginal bid under a glut, not trend reversal. *Changes if:* second consecutive week of large flash sales, or wet Midwest forecast stalling harvest into November.

**Week ahead:** Mon — USDA Crop Progress (~4pm ET); Tue — API inventories; **Wed — EIA Weekly Petroleum Status 10:30 ET** (watch whether the −8.6M bbl crude draw repeats after hurricane shut-ins recover); Thu — EIA Nat Gas Storage 10:30 ET, USDA Export Sales 8:30 ET; Tue Nov 10 — WASDE + Crop Production 12:00 ET. Ongoing unscheduled: Hormuz/Red Sea attacks, Houthi campaign, Russian refinery strikes, ceasefire diplomacy.

---

## Desk 6 — Box/Parity Observer

**Question:** Any new index-methodology docs or published parity-violation analysis since yesterday?

**One line:** Nothing new since yesterday — no new methodology documents or published parity-violation analysis found; yesterday's parity verdict (holds — single-name diffs ≈$0, SPY/QQQ diffs explained by omitted dividends) and the BOX20X26 box-rate index (effective Oct 7, already noted yesterday) stand unchanged.

Supporting notes: CBOE feed update C2026090301 (BuyWrite methodology changes, effective Oct 15/16) was announced Sep 3 — not new, not watchlist-relevant (BXTB/BXHB/BXLB/BXVBW/BXWBW only). No parity-violation analysis (boxes, conversions/reversals, put-call breaks) in the ~48h window across academic/exchange/practitioner sources — INFERENCE from bounded search (absence-of-evidence). What would change it: a new CBOE/S&P DJI/Nasdaq release note dated Oct 17–18, or a published parity-break analysis for SPX/SPY/QQQ.

---

## Desk 7 — Bonds & Rates desk

**Question:** What is the current rates environment from the repo's own rates module, and what is the directional read for premium pricing?

**Module result (verbatim):** schema `hedge-desk-rates-desk-1.0.0`, mode `REAL_FRED_RATES`, source `fred-public-csv-http-200`, `trade_authorized: false`. Module `as_of` = 2026-10-18; **latest actual observation in every FRED series = 2026-10-15 (Thursday)** — bond markets closed Sunday; Friday Oct 16 observations not yet in the pull. **Identical observation set to yesterday's package** (as-of advanced 10-17 → 10-18, no new data).

| Item | Value |
|---|---|
| Fed funds effective rate | **3.88%** (DFF, 2026-10-15); +0.25 pp over 60d window — FACT |
| 10Y / 2Y | **10Y 5.10%**, **2Y 4.77%** (2026-10-15) — FACT |
| 2s10s slope | **+33 bp**, upward-sloping — **Δ vs yesterday: zero** (same observations). 60d context: flattened 52→33 bp; front end pinned ~4.77%, long end eased 21 bp from Oct 5 peak of 5.31% — FACT |
| SOFR–EFFR spread | **+1 bp** (3.89 vs 3.88); SOFR/EFFR/OBFR 3.88–3.89 — FACT. Funding-stress read: **orderly, no stress signal** — INFERENCE |
| Premium-pricing implication | Long rates still elevated in absolute terms (10Y 5.10%) → discount-rate headwind on growth multiples persists but is not intensifying; −21 bp from Oct 5 peak is mild relief, not regime change. Flattening curve + pinned front end = higher-for-longer pricing, no inversion signal. No rates-driven reason to avoid premium collection; +1 bp SOFR–EFFR = no liquidity-distortion argument. Duration-heavy names (NVDA, TSLA) most exposed — INFERENCE |

**What would change it:** Monday's pull covering Fri Oct 16; 10Y resuming above 5.31% or 2Y breaking ~4.90%; 2s10s toward zero/inversion (flips read to slowdown warning); SOFR–EFFR widening past ~5–10 bp (funding stress); FOMC action or sharp front-end move.

Desk status: COMPLETE — module succeeded, no failure, no Yahoo substitution. Yield labeling per standing rule (^TNX=10Y, ^FVX=5Y, 13W=front anchor).

---

## Synthesis — the 5 decision-relevant items

1. **Hormuz escalated AND a diplomatic floor arrived the same weekend.** Mine strikes on two tankers (~4M bbl, IRGC claim unconfirmed) mark a tactical escalation from projectile attacks to area-denial; Iran's 7-day reopening offer is on the table but preconditions are incompatible (lift blockade vs nuclear-first) — so it is a floor under resolution, not a priceable event. Brent $109.86 / WTI $101.41 at Friday's close; **Sunday ~15:00 PT futures reopening is the first price read on both.** (Futures — FACTs + labeled INFERENCE)
2. **TSLA earnings Oct 21 AMC is the week's binary-event watch — premium into it = avoid.** Implied 7.41% ≈ historical mean 7.77% (median 4.46%) — the market is pricing fat-tail history, not edge. Q3 deliveries 486,532 (+5.3% vs Tesla-compiled consensus) are EDGAR-confirmed; the EPS basis ($0.21 Nasdaq vs $0.44–0.45 adjusted) remains UNVERIFIED — do not mix. (Earnings + Premium)
3. **NVDA is the cleanest rich-premium read on the board.** Live IV +13.2pp over trailing 20d realized, NOT window-contingent, no earnings inside either pulled expiry (Nov 18 sits outside) — elevation without an event. SPY also clean-rich (+4.9pp). QQQ/AAPL/MSFT/TSLA verdicts stay WINDOW-CONTINGENT (single days driving 31–37% of realized variance). IV-rank proper = UNVERIFIED for all (no free history source). (Premium)
4. **Rates: no new information, headwind persists but is not intensifying.** EFFR 3.88%; 10Y 5.10% / 2Y 4.77% (Oct 15 observations, unchanged set vs yesterday); 2s10s +33 bp; SOFR–EFFR +1 bp (orderly). Front end pinned, long end easing −21 bp from Oct 5 peak = mild relief, not regime change. Duration-heavy names (NVDA, TSLA) most exposed to the 5.10% 10Y. Monday's pull (covering Fri Oct 16) is the next data point. (Bonds & Rates)
5. **AAPL Nov 2 confirmed by issuer; Ternus's first call.** Removes the Monday-placement doubt; makes Nov-12-expiry earnings hump a confirmed input (Premium). FQ4 guide: revenue $111.69–113.74B (+9–11%), gross margin 47–48% (ex-tariff-refund), iPhone mid-teens. Communication risk on the new CEO's first call is a variable prior quarters did not have (INFERENCE). Wed 10:30 ET EIA report is the week's data watch alongside Monday's Crop Progress. (Earnings + Futures)

**Quiet lanes:** Dividends (nothing ex-div in window; MSFT Nov 19 reconfirmed; QQQ "cut" = ETF noise). Quant lab (6 new repos, all WATCH/ARCHIVE, none at TEST/INTEGRATE; ledger updated). Parity (no new methodology or violation analysis).

---

## Verification

- [x] File written: `~/workspace/hedge-desk-research/2026-10-18.md`
- [x] All seven desk sections present (Earnings, Dividend, Premium IV, Quant Lab, Futures Events, Box/Parity, Bonds & Rates)
- [x] IV-inputs provenance reported (as_of 2026-10-17T13:54:25-07:00, inside 26h guard)
- [x] No desk silently dropped; UNVERIFIED/failed items named explicitly
- [x] Output verification: re-read from disk, confirmed >2KB
