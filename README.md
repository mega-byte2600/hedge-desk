# Hedge Desk MVP

> **Corporate motto:** Making money overnight - the dream: making money while
> you sleep.

This is an aspirational product motto, not a promise of investment performance.
The MVP automates overnight research and prepares human-pending, defined-risk
paper-trade proposals. It does not autonomously authorize or execute trades.

This repository implements the first deterministic, paper-only vertical slice
from the Hedge Desk specification.

See [current implementation status](docs/architecture/STATUS.md) for the tested
MVP matrix, war-game coverage, and known production blockers.
See the [sub-$100 data stack](docs/validation/SUB_100_DATA_STACK.md) and
[local data intake contract](docs/validation/LOCAL_DATA_INTAKE.md) before
supplying licensed snapshots.

## Build culture: the 80/20 hacker rule

- **80% working code:** fail fast, build, measure, learn, and ship small tested
  vertical slices.
- **20% ADR:** record only decisions needed to reproduce, review, or safely
  change the software.
- A feature is not real until it has deterministic tests and a runnable path.

## MVP series

1. **Overnight Premium Desk:** defined-risk premium-selling research with a
   planned pre-expiration close.
2. **Earnings Event Paper Desk:** earnings/guidance surprise and market-response
   research with a defined-risk directional leg, independently calculated hedge,
   and explicit `NO_TRADE` outcome.
3. **European Index Box/Parity Observer:** paper-only search for theoretical
   identity dislocations using deterministic executable-side economics.
4. **Dividend Opportunity Desk:** rank sustainable dividend opportunities from
   point-in-time ten-year histories, then compare owning shares, a defined-risk
   option expression, and `NO_TRADE`. Long calls do not receive dividends, so
   the system must never equate buying a call with earning the cash payout.
5. **Open Quant/AI Model Lab:** independent Quant and AI research teams using
   versioned open code, open-weight models where applicable, explicit licenses,
   immutable hashes, frozen training cutoffs, and reproducible evaluations.
   Neither team can create authoritative RoR, clear compliance, or authorize a
   trade.
6. **Weather/War/Logistics Futures Event Desk:** compare validated physical
   event surprise with what the curve already prices, basis, roll, liquidity,
   margin, and transaction costs. Physical delivery and live trading are
   disabled.

Together these MVPs build toward a coordinated 24/7 research orchestration. Each
MVP shares the same deterministic calculation, independent risk, audit, and
human-authorization controls.

Specialized research agents include an Arbitrage Research Agent and an
off-exchange-flow research path. An independent Compliance Agent assists a
deterministic Compliance Policy Engine. Human judgment remains a distinct,
explicit decision point and cannot override risk or compliance blocks.

The system evaluates every trade candidate through independent gates:

1. source provenance, entitlement, point-in-time, and schema validation;
2. account/product eligibility and deterministic compliance policy;
3. portfolio exposure and conventional economic-risk controls;
4. exact-plan human authorization for paper execution.

Passing every gate produces a paper-trade decision record. It never submits an
order to a broker.

## Run

```bash
python -m hedge_desk.cli
python -m hedge_desk.cli --approve --human-id captain
python -m hedge_desk.cli --projects
python -m hedge_desk.cli --overnight-report
python -m hedge_desk.cli --war-games
python -m hedge_desk.cli --morning-markdown
python -m unittest discover -s tests -v
```

The default command stops at `human_authorization_required`. The second command
simulates a named human approval and paper-only open/close against a frozen
synthetic fixture; it does not connect to a broker or market-data vendor.

The overnight report evaluates every registered MVP through separately labeled
`OBSERVED`, `STAT`, `BIG`, `DETERMINISTIC_RISK`,
`DETERMINISTIC_COMPLIANCE`, and `HUMAN` layers. Until real
licensed adapters exist, it truthfully runs synthetic fixtures and returns
`NO_TRADE` for architecture-only projects. GitHub Actions runs this paper-only
evaluation every 15 minutes, 24/7, and retains its JSON report for 30 days.
GitHub scheduling is best-effort; delayed runs do not constitute a production
uptime guarantee.

## Safety boundary

- No broker adapter exists.
- Undefined-loss, stale-price, and insufficient-liquidity candidates are
  blocked.
- Risk estimates are model outputs requiring independent validation; they are
  not guarantees of future loss or portfolio survival.
