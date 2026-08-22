# Executable Project Status

As of 2026-08-22, the repository is a paper-only research and control system.
It has no broker adapter, no live market-data adapter, no live order path, and
no demonstrated real-money profit.

## Current evidence

- `python3 -m unittest discover -s tests -v`: 303 deterministic tests pass
  locally.
- GitHub CI tests Python 3.9, 3.11, and 3.13 on every push.
- CI enforces an 80% whole-package branch-coverage floor; the current measured
  local baseline is 82%, including subprocess-tested CLI code at zero attribution.
- GitHub's scheduled paper evaluation runs every 15 minutes and uploads the
  JSON war games plus JSON/Markdown morning reports.
- Morning reports are publication-gated, hashed, explicitly PAPER /
  HYPOTHETICAL, and report real-money P&L and real trades as zero.
- The declared synthetic suite contains 69 strategy, timing, execution,
  compliance, and lifecycle war games plus five combined-MVP capital-path
  stresses. Forty-two scenarios are explicit `NO_TRADE` controls.

Run the evidence directly:

```bash
python3 -m compileall -q hedge_desk tests
python3 -m unittest discover -s tests -v
python3 -m hedge_desk.cli --overnight-report
python3 -m hedge_desk.cli --war-games
python3 -m hedge_desk.cli --morning-markdown
```

## MVP matrix

| MVP | Executable status | Honest disposition |
|---|---|---|
| Overnight Premium Desk | Working synthetic vertical slice with cross-underlying executable-economics ranking and calendar-bound session handoff | Human review only; ranking infers no probability, local CLI withholds handoff until session evidence is supplied, and no live execution exists |
| Earnings Event Desk | Working point-in-time surprise ranker, pre-release locked four-arm experiment, and comparison war games | `NO_TRADE`; live estimate vintages, reaction model, validated risk, and strategy pipeline not implemented |
| Arbitrage Observer | Working synchronized executable-edge universe ranker plus war games | `NO_TRADE`; live scanner, risk, and settlement adapters not implemented |
| Dividend Opportunity Desk | Working point-in-time ten-year payout ranking plus CAPE valuation overlay and war games | `NO_TRADE`; live survivorship-safe universe/CAPE adapter and risk pipeline not implemented |
| Open Quant/AI Model Lab | Working dual-team research quorum plus open-artifact and reproducible training-run gates | `NO_TRADE`; no live datasets, training executor, authoritative risk input, or control authority |
| Weather/War/Logistics Futures Event Desk | Working cost/curve-aware synthetic multi-event universe ranker | `NO_TRADE`; live data, validated risk/margin, registration, and contract adapters not implemented |

## Implemented control boundaries

- synchronized option-leg and underlying quotes;
- executable-side option pricing, displayed size, open interest, volume, and
  bid/ask liquidity gates;
- deterministic DTE and planned pre-expiration exit timing;
- executable buy-to-close monitoring with commissions, project-policy profit
  capture/loss thresholds, DTE and event escalation; it requests human review
  and never authorizes an order;
- opening-to-close lineage binds the exact underlying, contract IDs,
  expiration, and quote-source identity before exit economics are evaluated;
- paper closes re-verify the exact approved plan and matching paper-open terms,
  consume source-bound executable exit quotes, and retain the exit artifact hash;
- point-in-time corporate-event calendars complete through expiration;
- independently hashed quantitative inputs and exact validator-issued
  RoR-before/RoR-after outputs for the conventional RoR engine; the agentic
  decision runtime consumes these values and never recalculates them;
- version-bound RoR golden vectors plus an independent rational-arithmetic
  oracle; these verify implementation but do not validate the model for live use;
- separate versioned deterministic compliance, risk, and Back Office artifacts;
- paper Back Office reconciliation binds the exact plan, internal/broker
  position hashes, cash ledgers, fill exceptions, and lifecycle exceptions; a
  passing paper artifact is explicitly ineligible as live-release evidence;
- compliance artifacts bound to a canonical FINRA/SEC/CFTC/OCC regulatory
  traceability hash; all live-counsel approval flags remain false;
- paper options-account evidence for broker approval, timestamped disclosure
  acknowledgement, and broker policy version, all compliance-hash-bound;
- aggregate/symbol maximum-loss gates and a drawdown circuit breaker;
- explicit human authorization bound to the exact plan hash;
- stale/worse/partial/adjusted paper-fill cancellation;
- assignment, expiration, ex-dividend, and settlement lifecycle actions;
- point-in-time replay, tamper-evident audit chain, idempotent scheduling, and
  bound recovery of failed runs.
- complete per-stage audit lineage binding candidate, input/output hashes,
  component version, policy version, stage order, and prior event hash.
- fail-closed local JSONL audit persistence with fsync, full-chain verification,
  duplicate suppression, and corruption rejection; this is not regulated WORM
  storage or a substitute for an external retention service.
- strict local BYO-data envelopes with byte-level hashes; licensed payloads are
  validated in place and are never copied into the public repository.
- point-in-time news/RSS evidence gates that treat transport separately from
  license, reject private/stale/duplicate evidence, and grant no trade authority.
- purged walk-forward Quant/AI evaluation splits with content-addressed,
  chronological train/validation/test windows, embargo gaps, sample minimums,
  and point-in-time cutoff enforcement; split admission grants no risk or trade
  authority.
- a strict canonical option-snapshot schema with exact decimal prices,
  synchronized source identity, and rejection of unknown/model-added fields.
- deterministic enumeration of every admissible vertical spread from a
  validated snapshot, with no forced ranking and explicit `NO_TRADE` output.
- content-addressed candidate handoffs to the conventional V&V boundary that
  contain no probability or Risk of Ruin and cannot authorize a trade.
- AST-enforced trust boundaries confining RoR calculation and validated risk
  input construction, and rejecting broker/network clients from paper runtime.
- reconstructable strategic-allocation evidence binding exact project-policy
  thresholds, weights, supplied CAPE, outcome, and explicit no-RoR/no-trade flags.
- a non-overridable, content-addressed paper-to-live release gate; current
  status is `LIVE_RELEASE_BLOCKED` until every required evidence artifact
  exists, including explicit Back Office reconciliation certification.

## Blocks before forward paper validation or live production

1. Licensed point-in-time market data and historical option-chain adapters.
2. Survivorship-safe corporate actions and event-calendar inputs.
3. Independently validated statistical probability/payoff model and RoR V&V;
   the current risk model is explicitly `0.1.0-unvalidated`.
4. Out-of-sample historical replay with realistic fills, halts, assignments,
   taxes where applicable, and regime separation.
5. Durable external WORM audit/receipt storage and operational monitoring; the
   implemented local JSONL journal is a paper-stage persistence boundary only.
6. Securities/commodities counsel review, broker-specific controls, approvals,
   and a separately authorized live architecture. Open-source disclaimers do
   not satisfy those requirements.
