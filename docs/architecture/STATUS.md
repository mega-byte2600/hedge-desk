# Executable Project Status

As of 2026-08-22, the repository is a paper-only research and control system.
It has no broker adapter, no live market-data adapter, no live order path, and
no demonstrated real-money profit.

## Current evidence

- `python3 -m unittest discover -s tests -v`: 105 deterministic tests pass
  locally.
- GitHub CI tests Python 3.9, 3.11, and 3.13 on every push.
- GitHub's scheduled paper evaluation runs every 15 minutes and uploads the
  JSON war games plus JSON/Markdown morning reports.
- Morning reports are publication-gated, hashed, explicitly PAPER /
  HYPOTHETICAL, and report real-money P&L and real trades as zero.
- The declared synthetic suite contains 28 strategy, execution, and lifecycle
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
| Earnings Event Desk | Deterministic synthetic comparison war games | `NO_TRADE`; strategy pipeline not implemented |
| Arbitrage Observer | Executable-side synthetic edge war games | `NO_TRADE`; market scanner not implemented |
| Dividend Opportunity Desk | Shares/call/no-trade synthetic war games | `NO_TRADE`; point-in-time screen not implemented |
| Open Quant/AI Model Lab | Open-license/reproducibility artifact gate | `NO_TRADE`; training pipeline not implemented |

## Implemented control boundaries

- synchronized option-leg and underlying quotes;
- executable-side option pricing, displayed size, open interest, volume, and
  bid/ask liquidity gates;
- deterministic DTE and planned pre-expiration exit timing;
- independently hashed quantitative inputs for the conventional RoR engine;
- versioned deterministic risk and Back Office artifacts;
- aggregate/symbol maximum-loss gates and a drawdown circuit breaker;
- explicit human authorization bound to the exact plan hash;
- stale/worse/partial/adjusted paper-fill cancellation;
- assignment, expiration, ex-dividend, and settlement lifecycle actions;
- point-in-time replay, tamper-evident audit chain, idempotent scheduling, and
  bound recovery of failed runs.

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
