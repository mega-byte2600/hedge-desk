# Emporion Pitch Deck Blueprint (grounded in what is actually built)

Purpose: map the standard seed-stage deck structure to Emporion's real, verified
state. Every number here is either measured by a command or explicitly labeled a
gap. No fabricated traction — the GP's own rule: "can't raise money with bs."

Source basis: seed-deck guidance (Antler pre-seed, Qubit seed guide, Waveup
traction 2026, SVB) + docs/PRODUCT_POSITIONING_AND_MEASUREMENT.md.

## The 12-slide structure investors expect (seed)

1. Problem
2. Solution
3. Market (TAM/SAM/SOM)
4. Product / demo
5. Traction (the slide VCs spend 3x longer on)
6. Business model / revenue
7. Competition
8. Go-to-market
9. Team
10. Financials
11. Use of funds
12. Ask

## Emporion's honest fill for each

### 1. Problem
Retail investors have screeners, charts, feeds, filings, and broker tools — but
no decision discipline. Fragmentation, not information scarcity. The GP's
framing: retail gets what is normally behind back-office doors. A compass, not a
boat.

### 2. Solution
Emporion is open investment research and decision infrastructure. Bring your
watchlist; research it your way. The differentiator is the SOUL.md multi-agent
desk — six specialist identities (QUANT, ENGINEER, RESEARCH, DATA, RISK,
ORCHESTRATOR), each on its own model, forced to disagree, with an independent
RISK veto. That is the engine, not decoration.

### 3. Market
TAM/SAM/SOM must be researched and cited — NOT invented here. This is a gap to
fill with real market data (retail options volume, fintech TAM). Do not fabricate.

### 4. Product / demo
The true-MVP demo: real EOD batch in → overnight premium-desk run → AM candidate
list. VERIFIED live:
- Real EOD ingestion (Yahoo public chart API), non-synthetic, batch
  READY_FOR_RESEARCH.
- Premium-desk candidate economics: cash-secured put, covered call, vertical
  credit spread, with real collateral/margin requirements.
- Nightly orchestrator writes a content-addressed AM report.
- Web console serves real candidates via /api/eod-candidates; iOS app scaffold
  exists.
- 672 unit tests green.

### 5. Traction (honest)
What is real and measurable today:
- 672 deterministic unit tests passing (measured).
- Live EOD pipeline producing real candidates (measured, 2026-09-19).
- A working web console + iOS app scaffold.
- 6+ years of iterative personal research practice (continuity, not performance).

What is NOT traction yet (state plainly, do not fake):
- No paying members, no revenue, no ARR.
- No live option-chain premium income (needs licensed/BYO data).
- No Schwab auto-execution (adapter is read-only).
- No real users beyond the GP.

The traction slide must lead with the honest hero metric that exists — e.g.
"real EOD → AM candidates, fully automated, 672 tests green" — and stack the
product proofs, then name the revenue gap as the next milestone.

### 6. Business model
The funnel (already designed, from the repo):
- GUEST: open 31-day test drive on synthetic research (funnel top).
- MEMBER: self-serve subscription, real data + read-only broker link (REVENUE).
- LP: actual LLC investor, GP-invited, capped at 99, never pays.
A paid Member is a converted Guest. This is the revenue path.

### 7. Competition
Robo-advisors (passive, no options), options screeners (no decision
discipline), broker apps (execution, not research). Emporion's point of
difference: Risk of Ruin is an independent constraint on every decision, and the
multi-agent desk is the differentiator. Needs a real competitive matrix — gap to
fill with cited research.

### 8. Go-to-market
Open-source-first: the public repo IS the marketing. GUEST funnel → MEMBER
conversion. iPhone app as the consumer surface. Needs a real GTM plan — gap.

### 9. Team
The GP (mbolton) + the SOUL.md multi-agent desk. Honest: the desk is the
differentiator; the human is the decision-maker. Do not claim credentials not
held (e.g. no FINRA Series 4 claim).

### 10. Financials
Gap — must be built from the MEMBER pricing model, not invented. State the
funnel math (Guest→Member conversion) as a model, not a promise.

### 11. Use of funds
Standard: data licensing (option chains), engineering, compliance counsel,
marketing. Needs real numbers — gap.

### 12. Ask
To be defined by the GP. Not fabricated here.

## What must be true before this deck is pitchable (the honest checklist)

- [ ] Real option-chain premium income shown (licensed or BYO data) — the #1 gap.
- [ ] Schwab risk-gated auto execution behind the deterministic risk gate + kill
      switch (the GP's chosen mode).
- [ ] At least one real MEMBER (converted Guest) — first revenue proof.
- [ ] TAM/SAM/SOM with cited sources.
- [ ] Competitive matrix with cited sources.
- [ ] Financial model from the MEMBER price, not invented.
- [ ] Compliance counsel review of the fund structure and any auto-execution.

## Verified status of this record

- VERIFIED: the product claims above are backed by the 672-test suite and the
  live EOD→premium pipeline (measured 2026-09-19).
- VALIDATED: matches the GP's stated product shape (premium desk centerpiece,
  EOD batch → overnight → AM candidates, risk-gated Schwab auto, web + iOS).
- NOT YET: revenue, real users, option-chain income, auto-execution, market
  sizing, financials. These are labeled gaps, not hidden.