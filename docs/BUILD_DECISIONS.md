# Hedge Desk Build Decisions

Owner / builder: **mbolton**

This file records product and architecture decisions that should survive beyond chat history and be visible in the repository alongside the code that implements them.

## 2026-09-06 / Data first

**Decision:** Hedge Desk is currently a data-acquisition and research-engineering effort, not a model-training effort.

**Implication:** Exhaust credible public/open and properly licensed sources before paying for additional datasets. Paid sources should fill demonstrated gaps, not precede source discovery.

## 2026-09-06 / Bonds first

**Decision:** Bonds, rates, credit, and financing data are the highest-priority data domain.

**Rationale:** Fixed income provides the discount-rate, financing, liquidity, macro-regime, relative-value, and cross-asset context used across the broader research stack.

**Priority discovery order:**

1. U.S. Treasury yields, auctions, curve and issuance
2. SOFR, repo and secured-financing data
3. Corporate bonds, TRACE, credit spreads and default data
4. Sovereign curves across major regions
5. Swaps, OIS and rate-curve data
6. Municipal bonds
7. MBS and structured fixed income
8. Central-bank and macro series that explain rates regimes

## 2026-09-06 / Open before subscription

**Decision:** Public/open data, government data, open repositories, public research and permissively licensed datasets are the first sourcing layer.

Repository visibility alone is never treated as permission for commercial use. License, provenance, point-in-time integrity, update cadence and entitlement must be reviewed before operational use.

## 2026-09-06 / Research models, not model worship

**Decision:** The Quant / AI desk researches and benchmarks finance-relevant AI systems globally, including public/open work from DeepSeek / High-Flyer and other regional finance-AI projects.

Models are research analysts, not trade authorities. No model may directly authorize a trade.

## 2026-09-06 / Human final gate

**Decision:** mbolton is the final human authorization gate for the current architecture.

Research evidence → deterministic controls → Yellow Sheet → mbolton review. Live brokerage execution is not enabled.

## 2026-09-06 / Fast SDLC

**Decision:** Small commits, frequent PRs, automated tests, security checks and CI/CD are the default operating model.

Breakage is acceptable in branches. Production merges only after required tests pass. Web and iOS clients should converge on the same API contracts and operating boundaries.
