# Executable Project Status

As of 2026-08-22, the repository is a paper-only research and control system.
It has no broker adapter, no live market-data adapter, no live order path, and
no demonstrated real-money profit.

## Current evidence

- `python3 -m unittest discover -s tests -v`: 190 deterministic tests pass
  locally.
- GitHub CI tests Python 3.9, 3.11, and 3.13 on every push.
- GitHub's scheduled paper evaluation runs every 15 minutes and uploads the
  JSON war games plus JSON/Markdown morning reports.
- Morning reports are publication-gated, hashed, explicitly PAPER /
  HYPOTHETICAL, and report real-money P&L and real trades as zero.
- The declared synthetic suite contains 50 strategy, timing, execution, compliance, and lifecycle
  war games plus five combined-MVP capital-path stresses.

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
| Overnight Premium Desk | Working synthetic vertical slice | Human review only; no live execution |
| Earnings Event Desk | Working point-in-time EPS/revenue surprise universe ranker plus comparison war games | `NO_TRADE`; live estimate vintages, reaction model, validated risk, and strategy pipeline not implemented |
| Arbitrage Observer | Working synchronized executable-edge universe ranker plus war games | `NO_TRADE`; live scanner, risk, and settlement adapters not implemented |
| Dividend Opportunity Desk | Working point-in-time ten-year universe ranking plus war games | `NO_TRADE`; live universe adapter and risk pipeline not implemented |
| Open Quant/AI Model Lab | Working dual-team research quorum plus open-artifact gate | `NO_TRADE`; no authoritative risk input or training pipeline |
| Weather/War/Logistics Futures Event Desk | Working cost/curve-aware synthetic multi-event universe ranker | `NO_TRADE`; live data, validated risk/margin, registration, and contract adapters not implemented |

## Implemented control boundaries

- synchronized option-leg and underlying quotes;
- executable-side option pricing, displayed size, open interest, volume, and
  bid/ask liquidity gates;
- deterministic DTE and planned pre-expiration exit timing;
- point-in-time corporate-event calendars complete through expiration;
- independently hashed quantitative inputs for the conventional RoR engine;
- separate versioned deterministic compliance, risk, and Back Office artifacts;
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
- strict local BYO-data envelopes with byte-level hashes; licensed payloads are
  validated in place and are never copied into the public repository.
- a strict canonical option-snapshot schema with exact decimal prices,
  synchronized source identity, and rejection of unknown/model-added fields.
- deterministic enumeration of every admissible vertical spread from a
  validated snapshot, with no forced ranking and explicit `NO_TRADE` output.
- content-addressed candidate handoffs to the conventional V&V boundary that
  contain no probability or Risk of Ruin and cannot authorize a trade.
- AST-enforced trust boundaries confining RoR calculation and validated risk
  input construction, and rejecting broker/network clients from paper runtime.
- a non-overridable, content-addressed paper-to-live release gate; current
  status is `LIVE_RELEASE_BLOCKED` until every required evidence artifact exists.

## Blocks before forward paper validation or live production

1. Licensed point-in-time market data and historical option-chain adapters.
2. Survivorship-safe corporate actions and event-calendar inputs.
3. Independently validated statistical probability/payoff model and RoR V&V;
   the current risk model is explicitly `0.1.0-unvalidated`.
4. Out-of-sample historical replay with realistic fills, halts, assignments,
   taxes where applicable, and regime separation.
5. Durable external audit/receipt storage and operational monitoring.
6. Securities/commodities counsel review, broker-specific controls, approvals,
   and a separately authorized live architecture. Open-source disclaimers do
   not satisfy those requirements.
