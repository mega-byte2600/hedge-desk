# BIG Handoff Assessment and Implementation Plan

Date: 2026-08-21

## Scope and safety boundary

This document maps the BIG Agentic Financial Research & Trade Desk handoff onto
the existing `hedge_desk` MVP. It is an implementation plan, not approval to
trade. The repository remains paper-only. No broker adapter or live execution
path exists.

The locked design constraints are accepted as architectural invariants:

- quantitative finance and risk values are produced only by deterministic,
  version-controlled code;
- risk management remains independent of alpha generation;
- no execution path may bypass deterministic risk evaluation and explicit human
  authorization;
- every decision must retain point-in-time evidence and enough inputs, versions,
  parameters, and intermediate values to reproduce its result;
- risk-control changes require reference cases and independent review.

### Risk of Ruin trust boundary

The authoritative RoR number is outside the agentic calculation boundary. It is
produced only by a deterministic risk-engine component built with conventional
software engineering and independent verification and validation (V&V).

Agents and agentic orchestration may not:

- calculate, estimate, infer, interpolate, or replace RoR;
- create authoritative RoR inputs from prose or model judgment;
- modify the engine result, threshold, version, parameters, or intermediates;
- treat an unavailable, invalid, stale, or unverifiable result as a pass.

Agents may read an immutable, versioned calculation artifact after its inputs
have passed non-agentic validation, explain the artifact, and route its existing
`PASS`, `REDUCE`, or `REJECT` status. The system fails closed when the risk
engine or its validation evidence is unavailable.

### Research and validation basis

Portfolio-risk policy and reference models will be grounded in exact primary
sources, including applicable work by David P. Swensen and Robert J. Shiller,
plus a user-supplied validation corpus. Attribution alone is not a model
specification: every implemented rule or formula must identify the exact source,
the interpretation adopted, assumptions, units, applicability limits, and
locked numerical reference cases. Independent V&V is required before a model
can affect a risk gate.

The repository is intended to be public open source. Source documents may be
committed only when their licenses allow public redistribution. Otherwise the
repository will retain citations, checksums, metadata, and derived test fixtures
that are legally redistributable, while protected originals remain outside Git.

## Baseline verification

Run from `/Users/user/Documents/Codex` with Python 3.13.1:

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | PASS: 7 tests |
| `python3 -m hedge_desk.cli` | PASS: deterministic paper decision emitted |
| `python3 -m compileall -q hedge_desk tests` | PASS |
| `python3 -m pytest` | UNAVAILABLE: pytest is not installed or declared |
| Git status/history | UNAVAILABLE: directory is not a Git checkout |

The documented `python` commands do not work in this environment; `python3` is
the available interpreter.

## Current component inventory

| Concern | Current implementation | Assessment |
|---|---|---|
| Domain contract | `hedge_desk/domain/models.py` | Typed immutable account, candidate, and decision records; incomplete BIG schema and lineage |
| Compliance | `hedge_desk/compliance/account_gate.py` | Independent product/account eligibility blockers with reason codes |
| Risk | `hedge_desk/risk/ruin.py` | Deterministic Decimal-based MVP RoR estimate plus quote, liquidity, and single-trade loss gates |
| Decision orchestration | `hedge_desk/core/decision.py` | Combines compliance and risk gates deterministically |
| Execution | None | Correct paper-only safety boundary; no execution interface exists |
| CLI | `hedge_desk/cli.py` | Fixed demonstration input and reproducible output |
| Tests | `tests/` | Seven deterministic unit tests covering selected blockers and repeatability |
| Data platform | None | Missing canonical point-in-time storage and ingestion |
| Research/agents/models | None | Missing specialist agents, model abstraction, retrieval, and evaluation harness |
| Audit persistence | None | Decisions are in-memory only; no evidence, intermediate-value, or version ledger |

## Conflicts and technical debt

1. `DecisionStatus.APPROVED_FOR_PAPER` is produced immediately after machine
   gates. The contract has no separate `risk_status` and `human_authorization`
   states, so it cannot represent the mandatory human sign-off gate.
2. `risk_of_ruin_before` is hard-coded to zero rather than calculated from a
   validated portfolio snapshot.
3. The RoR output lacks a model ID/version, normalized inputs, formula metadata,
   parameters, and intermediate calculations. It is deterministic but not yet
   fully reproducible as an audit artifact.
4. `RiskPolicy.assumed_loss_sequence` is unused, creating misleading policy
   surface area.
5. The risk gate evaluates a single candidate, not portfolio drawdown, exposure,
   leverage, concentration, covariance, liquidity, VaR, Expected Shortfall,
   stress loss, gap/overnight risk, capital-at-risk, or maximum permitted size.
6. Proposed-trade fields required by the handoff are absent: decision horizon,
   direction, conviction, expected downside, drivers, counter-signals, evidence,
   agent outputs, and model versions.
7. Quote time is checked, but source lineage (`published_at`, `available_at`,
   `effective_date`, `revision_date`, `source_id`, `ingestion_timestamp`) and
   point-in-time replay controls do not exist.
8. There is no durable audit store, configuration/version capture, schema
   migration strategy, or serialization contract.
9. Package metadata has no development/test dependencies. The README assumes a
   `python` executable that is absent in the inspected environment.
10. The directory has no Git metadata, conflicting with the version-control and
    reproducibility requirements.

No duplicate subsystems were found; the repository is a compact vertical slice.

## Implementation sequence

### Phase 1: Freeze and strengthen the existing vertical slice

- Add reference-case regression tests around RoR boundary values, Decimal
  precision, invalid inputs, future/stale quotes, zero/undefined max loss, and
  fail-closed behavior.
- Split machine risk status from human authorization. A machine pass must yield
  `PENDING` human authorization, never an executable approval.
- Introduce immutable, versioned `RiskCalculation` and `DecisionAuditRecord`
  contracts containing raw/normalized inputs, policy, model ID/version,
  intermediates, output, reason codes, and timestamps.
- Remove or implement the unused `assumed_loss_sequence` field only through a
  reviewed reference case.
- Add an architecture test proving that no execution interface can accept a
  trade without both a machine pass and explicit human approval.

Gate: existing behavior remains covered; all new tests deterministic; an
independent reviewer approves any changed risk formula or threshold behavior.

### Phase 2: Point-in-time data foundation

- Define canonical entity, security, observation, filing/document, price,
  fundamental, macro, and revision schemas.
- Make all observations carry the six required lineage timestamps/identifiers.
- Start with DuckDB/Parquet repositories behind explicit interfaces; reserve
  PostgreSQL/TimescaleDB for operational state.
- Add as-of queries and fixtures that prove future and revised data are excluded.
- Add delisted constituents and historical-universe membership to prevent
  survivorship leakage.

Gate: point-in-time replay tests reject look-ahead, timestamp contamination,
revision leakage, and survivorship bias.

### Phase 3: Deterministic finance and portfolio risk library

- Organize versioned calculators for ratios/valuation, factors/statistics,
  volatility/events, and portfolio risk.
- Implement portfolio snapshots and validated calculators for exposure,
  leverage, concentration, covariance, drawdown, VaR, Expected Shortfall,
  scenario loss, capital-at-risk, and permitted position size.
- Keep orchestration and prose outside calculator modules; calculator outputs are
  typed artifacts with formulas, versions, parameters, and intermediates.
- Validate every financial model against locked reference cases before it can be
  used by a gate.
- Create a research traceability matrix mapping each portfolio-risk requirement
  to exact Swensen/Shiller or other primary sources, implementation requirements,
  assumptions, tests, and independent V&V evidence.
- Keep the authoritative risk-engine package free of LLM/agent dependencies and
  expose only a typed, fail-closed request/result contract to orchestration.

Gate: same snapshot + version + parameters produces byte-stable serialized
calculation results within an explicitly defined serialization format.

### Phase 4: Associate workflow and evidence layer

- Build one end-to-end 10-Q workflow before adding specialist agents.
- Store source document identity, exact cited sections, retrieval timestamps,
  extracted facts, and validation outcomes.
- Allow the agent to retrieve, classify, synthesize, and call tools, but never to
  fill missing quantitative outputs with estimates.
- Evaluate extraction against human-labeled reference answers.

Gate: every narrative claim is connected to evidence or a deterministic tool
artifact; missing inputs fail closed.

### Phase 5: Agents, model abstraction, and committee

- Add a provider-neutral model interface and common evaluation harness.
- Add specialist agents incrementally: filings/earnings, fundamental, quant,
  macro/regime, sentiment, skeptic, then investment committee.
- Define typed inputs/outputs and retain disagreements rather than averaging
  opinions blindly.
- Track agent/task predictive performance without allowing it to override risk.

Gate: committee output is only a proposed trade with `PENDING` risk and human
states.

### Phase 6: Backtest and paper-trading workflow

- Implement strict as-of event replay with historical universe membership,
  transaction costs, and slippage.
- Route every proposed paper order through deterministic portfolio risk, RoR
  policy evaluation, and recorded human approval.
- Keep execution adapters absent until the production governance gate is met.

Gate: integration tests demonstrate that rejected, reduced, errored, missing,
or unapproved decisions cannot reach the paper execution boundary.

## Immediate next change set

The safest first code change is Phase 1 only:

1. add regression/reference tests for the current RoR engine and gates;
2. introduce separate machine-risk and human-authorization states;
3. add a versioned risk calculation/audit artifact without changing the current
   RoR formula;
4. update CLI and README to show a machine-passed but human-pending paper trade;
5. document the independent review required before merging risk-behavior changes.

This change set creates the safety contract needed for all later BIG components
without prematurely building agents or data infrastructure on an ambiguous
decision boundary.
