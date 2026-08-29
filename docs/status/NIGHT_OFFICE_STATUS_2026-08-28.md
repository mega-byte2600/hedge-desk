# Night Office Status

Date: Friday, August 28, 2026

## Status

The local MVP now includes a night-office operating layer for the premium desk. This is designed to support the next morning demo and the Monday, August 31 through Friday, September 4, 2026 watch window.

## Added Locally

- Night-office brief generator.
- Night-office checklist on the web demo.
- Week-ahead premium desk cards on the web demo.
- Market tape separate from trade candidate symbols.
- Sortable market and candidate tables.
- 20-minute delayed quote labeling.
- Options timing controls: DTE, trigger action, premium, extrinsic value, entry window.
- Schwab read-only backend boundary remains in place.
- Agent order placement remains blocked.

## Night Office Workflow

The night process now covers:

1. Risk: recompute ruin contribution and aggregate boundary.
2. Global macro: review Japan/yen, rates, oil, gold, U.S. futures, and volatility.
3. Catalysts: map jobs, inflation, BOJ, oil/geopolitical, earnings, and SEC filing events to instrument channels.
4. Compliance: check account type, product permission, defined-risk requirement, and source trace.
5. Model V&V: record assumptions, limits, validation needs, and tests.

## Week-Ahead Focus

Premium desk themes surfaced in the website:

- U.S. jobs and rate repricing: SPY, QQQ, IWM, TLT, VIX.
- Japan yen and BOJ tightening risk: USD/JPY, EWJ/DXJ, rates read-through.
- Oil/geopolitical volatility: USO, XLE, CL futures read-through.
- Tech/AI valuation sensitivity: QQQ and broad growth exposure.

## Validation Anchors

The operating model is aligned to:

- Bloomberg-style portfolio/risk workflows: unified risk, performance, positions, events, pre-trade controls, scenarios.
- Bloomberg MARS/PORT-style risk framing: cross-asset risk, stress testing, integrated data, and reporting.
- Federal Reserve model-risk guidance: intended use, conceptual soundness, data quality, outcome analysis, monitoring, governance, and effective challenge.
- HBS case method framing: decision-making with incomplete information and clear action ownership.
- Tuck experiential framing: connect research, practitioners, and application.

## Verification

Latest local verification:

- 17 tests passing.
- Demo generation produces:
  - `reports/pre_us_open_demo.md`
  - `reports/hedge_desk_demo.html`
  - `reports/week_ahead_premium_brief.md`
  - `reports/night_office_brief.md`

## Sources

- Bloomberg PORT: https://professional.bloomberg.com/products/bloomberg-terminal/portfolio-analytics/
- Bloomberg MARS: https://professional.bloomberg.com/products/risk/mars/
- Bloomberg Asset Management Workflow: https://professional.bloomberg.com/institutions/asset-management/
- Federal Reserve Model Risk Guidance: https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
- HBS Case Method: https://www.hbs.edu/mba/academic-experience/the-case-method
- Tuck Center for Private Equity and Venture Capital: https://cpevc.tuck.dartmouth.edu/
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
