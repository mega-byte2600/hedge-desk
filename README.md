# Hedge Desk MVP

> **Corporate motto:** Making money overnight - the dream: making money while
> you sleep.

This is an aspirational product motto, not a promise of investment performance.
The MVP automates overnight research and prepares human-pending, defined-risk
paper-trade proposals. It does not autonomously authorize or execute trades.

This repository implements the first deterministic, paper-only vertical slice
from the Hedge Desk specification.

## MVP series

1. **Overnight Premium Desk:** defined-risk premium-selling research with a
   planned pre-expiration close.
2. **Earnings Event Paper Desk:** earnings/guidance surprise and market-response
   research with a defined-risk directional leg, independently calculated hedge,
   and explicit `NO_TRADE` outcome.

Together these MVPs build toward a coordinated 24/7 research orchestration. Each
MVP shares the same deterministic calculation, independent risk, audit, and
human-authorization controls.

The system evaluates every trade candidate through two independent gates:

1. account and product eligibility;
2. economic risk, including defined maximum loss and a conservative
   risk-of-ruin approximation.

Passing both gates produces a paper-trade decision record. It never submits an
order to a broker.

## Run

```bash
python -m hedge_desk.cli
python -m unittest discover -s tests -v
```

## Safety boundary

- No broker adapter exists.
- Undefined-loss, stale-price, and insufficient-liquidity candidates are
  blocked.
- Risk estimates are model outputs requiring independent validation; they are
  not guarantees of future loss or portfolio survival.
