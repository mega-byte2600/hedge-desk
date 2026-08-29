# Hedge Desk MVP Status

Date: Friday, August 28, 2026

## Current Status

Sprint 1 has moved from concept notes to a runnable local MVP demo.

Working locally:
- Local backend server.
- Static web demo.
- Markdown pre-U.S.-open desk packet.
- Week-ahead premium desk brief.
- Multi-symbol delayed market tape.
- Sortable tables.
- Options timing gate.
- Risk-of-ruin gate.
- Account/compliance gate.
- Deterministic policy plane.
- Source/entitlement contracts.
- Hash-chained audit events.
- Schwab read-only integration boundary.
- Explicit block on agent order placement.

## Demo Commands

```bash
cd /Users/cebu/Documents/BIG
python3 -m unittest discover -s tests -v
python3 -m hedge_desk.demo
python3 -m hedge_desk.server
```

Open:

```text
http://127.0.0.1:8765/demo
```

## Verification

Latest local verification:
- 16 tests passing.
- Week-ahead report coverage included.
- No live trading code path.
- Schwab order placement is structurally blocked.
- No third-party runtime dependencies.
- No broker credentials required for demo.

## Current MVP Boundary

Allowed:
- Research.
- Paper-only demo.
- 20-minute delayed market snapshots.
- Schwab read-only OAuth scaffold.
- Account/risk/policy gating.

Blocked:
- Agent trade placement.
- Live order routing.
- Undefined-risk options/futures strategies in MVP.
- Unmarked real-time claims.
- Premium candidates without DTE, premium/extrinsic value, max loss, and ruin check.

## Week-Ahead Focus

The next desk layer focuses on Monday, August 31 through Friday, September 4, 2026:
- U.S. jobs and rate repricing.
- Japan yen and BOJ tightening risk.
- Oil/geopolitical volatility.
- Tech/AI valuation sensitivity.

The website now surfaces these as simple week-ahead premium cards so the desk can quickly decide what to watch, what to block, and what could enter paper-only premium review.

## Immediate Next Work

1. Finish Schwab OAuth callback/token handling for read-only account data.
2. Add SQLite persistence for decisions, quotes, audit events, and account snapshots.
3. Add paper broker state: cash, positions, simulated fills, exposure.
4. Add real SEC ticker lookup and companyfacts fetch behind backend source contracts.
5. Add GitHub security workflow: secret scanning, dependency scan, and branch protection review.
