# Sentry Red-Team Baseline — 2026-W39

**Date:** 2026-09-25 (one-off baseline; weekly cron starts Mon 2026-09-28) · **Scope:** this week's research output (`~/workspace/hedge-desk-research/`: daily packages 09-22 → 09-25, parts/, two competitive notes) + strategy autopsy of `hedge_desk/premium_candidates.py` · **Method:** read-only · **Lens:** value investor · **Note:** no nightly briefs exist yet (first run tonight 20:54 PT).

---

## Part 1 — Pipeline audit: catches

### CATCH 1 (material): NVDA/MSFT earnings dates upgraded to "(confirmed)" with no new evidence — and NVDA's date moved 8 days unexplained
- `2026-09-25.md:15,17` — table lists MSFT "Oct 27/28 … (confirmed)" and NVDA "Nov 25 … (confirmed)".
- Track record: `2026-09-22.md:11,21` and `2026-09-23.md:13,21` had NVDA Nov 17 "company-confirmed via its Q2 FY2027 call transcript." `2026-09-24.md:26` silently downgraded it to "~11-17, estimated (Yahoo only)" with no explanation. `2026-09-25.md:17` then moved the date to Nov 25 and re-upgraded to "(confirmed)" — no named source for either the move or the confirmation. MSFT went from "provider estimates" (`2026-09-24.md:10`) to "(confirmed)" (`2026-09-25.md:15`) with no new evidence cited.
- **Correct label:** the 09-25 "(confirmed)" tags are UNVERIFIED as stated. A confirmation with no confirmer fails the desk's own bar. Either cite what confirmed the new dates or carry the conflict forward explicitly.

### CATCH 2 (material): 09-24 Futures section carries hard numbers with zero source traceability in the consolidated package
- `2026-09-24.md:58` — "IEA 9-2: global supply −4.3M bpd in 2026, demand −1.6M bpd"; "US diesel at record highs ($6.28/gal nat'l avg 9-14, +78% since late Feb)"; "3 commodity vessels transited Tuesday, 80% below 10-day avg"; "Trump diesel export ban proposal spiking European diesel."
- The 09-24 consolidated package has **no Sources line** for the Futures section (09-25 does). A reader of the consolidated package cannot verify any of these numbers.
- **Correct:** every hard number in the consolidated package needs its source inline or a Sources line. Traceability that lives only in a part file the reader wasn't pointed to is not traceability.

### CATCH 3: 09-22 Futures section — same traceability gap
- `2026-09-22.md:38` — "China–US East Coast spot $10,948/FEU near the COVID record; bunker fuel $901.50/mt vs. $543.50 pre-war." No Sources line in the consolidated package.
- **Correct:** add source traceability (same fix as Catch 2).

### CATCH 4: 09-25 VIX "corroboration" is two sources disagreeing
- `2026-09-25.md:45` — "VIX closed ~14.8–15.2 on Sep 25: sigmanomics 14.80 (−4.76% day), haruspex 15.20", presented under "What is verifiable (FACT, third-party corroboration)."
- A 0.4-pt spread between two same-day closes means at least one source is stale or wrong — that is not corroboration. Same line: "S&P 500 closed 7,704.13" appears with **no source at all**.
- **Correct:** note the inter-source disagreement (or pick the primary: Cboe), and mark the S&P close UNVERIFIED as stated.

### CATCH 5: 09-24 "six-month backwardation" is a seven-month spread
- `2026-09-24.md:8` and `:59` — "WTI $95.37 Nov26, ~$79.40 Jun27 → −16.7% backwardation" labeled "six-month." Nov→Jun is 7 months. The −16.7% math itself checks ((95.37−79.40)/95.37).
- **Correct:** "seven-month" (or recompute on an actual six-month pair).

### CATCH 6: 09-24 IV table asserts causation without a label
- `2026-09-24.md:47` — Shape column: "Nov hump = 10-29 earnings." `2026-09-24.md:10` — "its Nov IV hump is earnings premium" stated as fact.
- The hump is real (28.29% vs 24.05% Oct); the *cause* is inference. The same package properly hedges MSFT/NVDA as "probable binary events."
- **Correct:** INFERENCE.

### CATCH 7 (minor): 09-22 realized-vol figures have no stated methodology
- `parts/2026-09-22-iv.md:16` — "IV below 20-day realized vol on NVDA (30.4 vs 46) and TSLA (41.1 vs 50)." The 46 and 50 appear only in the prose takeaway; the table has no realized-vol column and no calculation method. (09-23 later documents the method: own calc, log returns, sqrt(252) — `parts/2026-09-23-iv.md:3`.)
- **Correct:** backfill the method or mark the 09-22 figures' basis UNVERIFIED.

### Non-catches (pipeline defended — checked, held up)
- The 09-23 "+18% dividend" error was self-caught and corrected in-package (`2026-09-23.md:13`) — the pipeline working as designed.
- NVDA dividend timeline coheres once the part file is read correctly: ex 09-10, payment lands 10-01 (`parts/2026-09-22-dividend.md:14,23`); the consolidated "9/10 ($0.25)" is loose ex-vs-pay phrasing, not a contradiction.
- Yahoo options 401 → all IV ranks fail-closed to UNVERIFIED (`2026-09-25.md` Desk 3) — correct behavior, and the standing preference/persistence is documented in Session notes.
- Bracket22 and High-Flyer notes are properly labeled throughout (claims marked as reported/unaudited; inference separated).

---

## Part 2 — Strategy autopsy: `hedge_desk/premium_candidates.py`

**Verdict: KEEP (conditional) — do not kill.** The module's honesty boundary is its load-bearing strength: it computes only collateral/margin from real EOD closes, never fabricates option prices, IV, probability, or RoR, and `trade_authorized` is always False. Decimal money, versioned policy, reason codes, reproducible, fail-closed on bad closes, zero-credit margin = maximum capital at risk. The failure modes below are sins of omission, not commission. There is no fabricated edge to kill.

### Hit 1 — Vol-blind strike offsets (regime fragility; the main hit)
`CASH_SECURED_PUT_STRIKE_OFFSET = 0.90`, `COVERED_CALL_STRIKE_OFFSET = 1.10`, `CREDIT_SPREAD_WIDTH = $5.00` are fixed policy constants (`premium_candidates.py:36-40`). On TSLA (IV ~44%) a 10%-OTM put is roughly 0.2σ; on SPY (IV ~12%) it's roughly 0.8σ — the "same" structure carries ~4x different moneyness across the watchlist, and the module cannot see it. No earnings-proximity check either: it will emit a 10%-OTM put straight into a binary event. The constants are honestly labeled as policy, not data — but the candidate set's risk profile drifts silently with regime.
**Fix:** consume the in-repo earnings calendar to flag event-proximity; consider vol-scaled offsets once a real IV source exists.

### Hit 2 — No freshness check on the close (staleness)
The EOD row dict carries `last_day` (date) — `eod_ingest.py:284` — but `build_premium_candidates` never reads it. Strikes compute off whatever the last bar was. A weekend/holiday run, or a failed pull served from cache, silently yields stale strikes.
**Fix:** reject or flag when `last_day` is older than N trading days.

### Hit 3 — Silent symbol dropout (selection-bias analog)
Non-PASS rows are `continue`d with no record (`premium_candidates.py:86-87`). Downstream cannot distinguish "no opportunity" from "data failed."
**Fix:** emit a `skipped` list with reason codes.

### Hit 4 — Covered-call ownership unverified (logic gap)
`covered_call_requirement` (`options/requirements.py:106-127`) honestly prices the full share capital — but nothing checks the paper portfolio actually holds the shares. A "covered" call on unheld shares is economically a naked call.
**Fix:** ownership check at plan assembly, or make the held-shares assumption explicit in the candidate record.

### Hit 5 — No cost model
Commissions, bid/ask, assignment fees absent. Out of scope by design (no premium is modeled), but any downstream "candidate economics" use is incomplete without it. Note, don't necessarily fix here.

### Explicitly checked, low risk
- **Overfit: LOW** — no fitted parameters, no ML; constants are arbitrary but not data-fit.
- **Lookahead: LOW** — point-in-time EOD close; minor Yahoo split/dividend-revision caveat only.
- **Survivorship: LOW** for a 6-name watchlist; Hit 3 is the live variant.

---

## Bottom line
7 pipeline catches (2 material: earnings-date confirmation upgrades with no evidence; hard futures numbers with no source traceability). Autopsy: **KEEP** `premium_candidates.py` — 5 additive fixes, none touching risk/ruin math. No kills this run.
