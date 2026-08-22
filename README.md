# Hedge Desk MVP

This repository implements the first deterministic, paper-only vertical slice
from the Hedge Desk specification.

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

