# ADR-0006: Mandatory Yellow Sheet control

## Status

Implemented for the paper pipeline; independent risk-control review is required
before merge or any future live design.

## Decision

Every proposed trade carries exactly one active, immutable `YellowSheet`.
The sheet is canonical and machine-readable, content-addressed by SHA-256, bound
to the candidate and the exact pre-authorization plan hash, and represented in
the existing append-only audit chain by a `YELLOW_SHEET` event. Version 1 has no
predecessor. Every later version names the immediately prior version and gets a
new content hash.

The deterministic gate validates identity, schema and policy versions, required
text, investigated alternatives, timestamped and source-hashed evidence, model
or rule versions, all five action conditions, observable invalidation, complete
cross-market and risk context, canonical input hashes, freshness, and both
candidate and plan bindings. A triggered invalidation is a gate failure.

Any failure yields `NO_TRADE` with stable reason codes. The rejected record may
be retained for review, but it cannot be authorized, filled, or executed. Plan
integrity is rechecked at authorization, fill, open, lifecycle, and close.

## Authority boundary

Research agents may draft, synthesize, or challenge Interest, Hypothesis,
Investigation, Evidence, and narrative rationale. Those statements are inputs,
not authorization. The Yellow Sheet gate performs no RoR calculation and cannot
waive deterministic risk, compliance, audit, or human controls. Human approval
is bound to the exact plan only after every machine gate passes.

## Cross-market reasoning

The schema requires explicit treatment of rates/bonds, curve shape, credit,
equities, volatility, commodities, currencies, and liquidity. A field may state
that a market is not relevant, but it may not be omitted. This turns standard
fixed-income, portfolio, quantitative, and intermarket concepts into reviewable
system inputs without embedding proprietary prose or allowing narrative signals
to calculate authoritative risk.

## Consequences

- Rationale and contradictory evidence become reproducible artifacts.
- A revision cannot silently replace the sheet attached to an approved plan.
- Evidence expiry or thesis invalidation deterministically stops progression.
- Future live adapters must call the same integrity gate and cannot introduce a
  bypass; no live adapter exists today.
