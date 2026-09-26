# Macro Transmission Map — WTI & Treasury Yields → Watchlist
**Date:** 2026-09-25 (post-close, Friday) · **Watchlist:** SPY, QQQ, AAPL, MSFT, NVDA, TSLA
**Purpose:** reference doc for the daily macro-driver check — how oil and bond moves transmit, with evidence labels. RESEARCH ONLY.

## Current snapshot (FACT — sourced, timestamped)

| Input | Level | Move | Source |
|---|---|---|---|
| WTI front-month (CL=F, Nov 26) | 92.44 | −2.29% / 5d | Yahoo Finance, 2026-09-25 |
| WTI spot (DCOILWTICO) | 96.41 | 101.44 → 96.41 since 9-18 | FRED/EIA, 2026-09-22 |
| Brent (BZ=F) | 97.47 | −8.56% / 5d | Yahoo Finance, 2026-09-25 |
| 10Y Treasury (^TNX / DGS10) | 5.18% | 4.96 → 5.18 this week (+22bp) | Yahoo / FRED, 2026-09-24 |
| 2Y Treasury (DGS2) | 4.87% | 4.71 → 4.87 this week | FRED, 2026-09-24 |
| 2s10s spread (T10Y2Y) | +36bp | steepening (+26bp → +36bp) | FRED, 2026-09-25 |
| Fed funds target upper (DFEDTARU) | 4.00% | unchanged | FRED, 2026-09-25 |
| US Dollar Index (DX-Y.NYB) | 101.04 | −0.25% / 5d | Yahoo Finance, 2026-09-25 |
| VIX | 14.87 | −5.11% / 5d | Yahoo Finance, 2026-09-25 |
| SPY / QQQ | 771.35 / 744.50 | +0.54% / +0.46% / 5d | Yahoo Finance, 2026-09-25 |

**Read of the week (INFERENCE):** oil fell while yields rose — the +22bp move in the 10Y is NOT oil-driven this week. Something else (growth expectations, supply, term premium — UNVERIFIED which) is pushing long yields up into falling energy prices.

## Channel 1 — Discount rate / duration: yields → valuation (sharpest)
**Direction: FACT (DCF arithmetic, no model needed). Magnitude per name: UNVERIFIED.**
- A higher discount rate mechanically lowers present value; the hit scales with cash-flow duration. NVDA, MSFT, TSLA, AAPL skew long-duration (growth priced on outer years) — they take the biggest mark from a +22bp week. SPY/QQQ inherit it through their mega-cap weights.
- Deterministic illustration (pure math, FACT): $1 of year-10 cash flow is worth $0.616 at 4.96% and $0.604 at 5.18% — roughly a 2% PV haircut per 22bp at 10-year duration. The sign is certain; any specific price target for a name is UNVERIFIED without a real DCF.
- Value-lens read: rising yields don't change intrinsic cash flows, they change what you should pay for them — margin of safety must be re-measured against the new rate, not the old one.

## Channel 2 — Rho / cost of carry: yields → options premium pricing (sharpest)
**Direction: FACT (Black-Scholes math). Magnitude per contract: verifiable from the chain, not assumed.**
- Higher risk-free rate → calls richer, puts cheaper (rho), all else equal. For the premium desk this is directional and certain.
- Direct consequence: cash-secured-put premium **compresses** as rates rise — the same strike put pays less. Screen CSP candidates against the current rate regime; a put that looked attractive at 4.5% may not clear the bar at 5.18%.
- Higher carry also raises the forward price, which mechanically supports call-side premium. Check the chain; don't assert a number you didn't pull.

## Channel 3 — Oil → CPI → Fed path → yields (the indirect oil channel)
**Mechanism: INFERENCE (standard macro, timing/magnitude UNVERIFIED). Inputs: FACT.**
- Energy is a direct CPI component, so a sustained oil move pushes inflation prints, which push Fed-funds expectations, which push 2Y/10Y. Fed target upper is 4.00% (FACT, FRED).
- For THIS watchlist this is the main oil channel — none of the six names is an oil producer/refiner (FACT), so oil reaches them through inflation expectations and the rate path, not through revenue.
- Discipline: one week's oil move (−2% to −9%) does not move the Fed. Only sustained moves that show up in CPI/PCE prints matter — verify against the prints, not the futures screen.

## Channel 4 — Direct energy/input-cost: oil → margins (weak for this watchlist — honest finding)
- TSLA: gasoline prices ↔ EV demand economics — high pump prices support the EV value proposition. **INFERENCE; demand elasticity UNVERIFIED.**
- NVDA / MSFT: datacenter electricity is a real cost line that rises with energy prices. **INFERENCE; magnitude UNVERIFIED — not broken out in a way that moves the thesis.**
- AAPL: freight and supply-chain energy costs — minor at Apple's scale. **INFERENCE.**
- Bottom line: do not force an oil-cost story onto names where it doesn't bind. For these six, Channel 3 dominates Channel 4.

## Channel 5 — Dollar translation: DXY → non-US revenue (one line)
**Direction: FACT (accounting). Magnitude: UNVERIFIED.**
- DXY at 101.04. A stronger dollar is a translation headwind on AAPL/MSFT/NVDA non-US revenue when reported in USD. Note the direction; don't quantify without segment FX disclosure.

## Channel 6 — Equity risk premium: 10Y vs earnings yield (watch, don't assert)
**INFERENCE; index trailing EPS not pulled — UNVERIFIED.**
- 10Y at 5.18% raises the bar every equity competes against. Relative-valuation pressure on high-multiple names is real in direction; quantifying it needs the index earnings yield, which the daily check should pull before claiming compression.

## How the daily macro check should reason (template)
1. Pull: CL=F, ^TNX, ^FVX (Yahoo); DGS10/DGS2 if FRED is reachable. Record level + 5d move. FACT.
2. State the yield move's discount-rate implication for long-duration names (Channel 1) and the rho implication for any open premium screens (Channel 2). Direction FACT, magnitude UNVERIFIED.
3. Ask: is the yield move oil-driven? Compare oil's week vs yields' week. This week: no (oil down, yields up). FACT on data, INFERENCE on attribution.
4. Only if oil moved a lot AND sustainably: trace Channel 3 (CPI → Fed → yields) and Channel 4 (name-level cost). Mark every step INFERENCE unless verified against prints/filings.
5. Never invent a causal claim. "Yields rose 22bp; long-duration names reprice lower, all else equal" is enough.

## Sources
- Prices/yields: Yahoo Finance chart API (query1.finance.yahoo.com), 2026-09-25 post-close.
- Official series: FRED fredgraph.csv — DGS10, DGS2, T10Y2Y, DFEDTARU, DCOILWTICO (EIA).
- Math: DCF present-value arithmetic; Black-Scholes rho sign — deterministic, no source needed beyond the formulas.
