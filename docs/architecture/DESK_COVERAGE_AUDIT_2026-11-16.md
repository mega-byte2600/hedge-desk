# Research desk coverage audit — 2026-11-16

This audit compares each desk's visible mandate with the current implementation. “Live” means an actual feed or dated source is connected; it does not mean every analytic capability is complete. No desk authorizes a trade.

| Desk | Advertised job | Implemented evidence and workflow | Gaps disclosed to the user |
|---|---|---|---|
| 1 — Overnight Premium | Defined-risk option premium research, position monitoring, exit review | Existing nightly report and options research | Not a live options execution or position-monitoring service; no order connection. |
| 2 — Earnings Event | Dated earnings event and equity/options/no-trade comparison | Existing event research and earnings report | Completeness and freshness are report-specific; the desk UI must expose source timestamps. |
| 3 — Box / Parity Observer | Box/parity after spreads, fees, settlement, financing | Existing analysis framework and report | A theoretical relationship is not an executable edge; complete venue quotes and financing must be verified for each case. |
| 4 — Dividend Opportunity | Payout durability, shareholder yield, valuation and alternatives | Existing dividend research | Current report inputs and dates govern; no automatic investment conclusion. |
| 5 — Short Sale Research | Filing-grounded, watchlist-only short research with counter-thesis, catalysts, liquidity, short interest, borrow, invalidation | Approved-watchlist prices and returns; asynchronous SEC EDGAR submissions for supported CIKs; source-linked filings; explicit one-cohort depreciation sensitivity requiring exact SEC filing and user-entered inputs; recurring 48-hour Burry/Cassandra research task | SEC submission feed does not parse filing facts or create a thesis. Catalyst, short-interest, borrow/locate, and complete counter-thesis remain unevaluated until separately sourced. Unsupported CIKs and unavailable SEC responses are explicit statuses. Reddit is an unverified lead only. No Burry score or universal “Burry formula” is claimed. |
| 6 — Weather / War / Futures | Track physical events and assess them against commodity/futures markets | Carpe DATA event context now includes NWS alerts, NASA EONET, USGS, CFTC positioning, available EIA/USDA data, and paced GDELT conflict-news leads. Feed status and provenance are exposed. | Conflict news is a lead, not event confirmation. The app does not yet ingest matched contract-month curves, location/grade basis, roll, executable costs, and complete contract specifications. Therefore it blocks a ranked futures candidate instead of fabricating one. |
| 7 — Bonds & Rates | Connect Treasury, real rates, policy, credit, duration and liquidity | Dedicated ten-indicator dashboard, triggers, vote balance, Kalshi pricing, counter-evidence, Graham sensitivity | The JSON board is a dated snapshot (2026-11-13), not a fresh streaming feed. The UI now shows a stale-snapshot warning after two days and states that the daily brief may be newer. Values must be refreshed from cited sources before they are treated as current. |

## Desk 5 model boundary

The depreciation panel computes the explicitly stated straight-line scenario:

`eligible asset cost × time-in-service fraction × (1 / scenario useful life − 1 / reported useful life)`

It then applies the supplied tax rate to the annual expense delta, holds the supplied diluted share count constant, and computes a constant-P/E price sensitivity. Inputs must be traceable to a specific SEC filing and the page labels the calculation a one-cohort scenario. It does not infer GPU spending, construction-in-progress, accumulated cohorts, replacement capital expenditure, or DCF value. It does not decide that reported accounting is wrong. This is a reproducible sensitivity method prompted by Burry's publicly described depreciation concern, not a claim to have recovered his private model.

The 48-hour Desk 5 research task uses Burry's official Cassandra Unchained publication as the primary source. Reddit can surface discussion or source links but cannot establish authorship or a thesis fact; claims require primary filings or attributable statements and independent corroboration.

## Validation note

Automated coverage tests anchor the mobile Research Desk card copy and routes, Desk 5/6 data gates, and Desk 7 freshness warning. Targeted backend tests cover SEC mapping/filing links, decimal sensitivity math, event feed normalization and rate-limit behavior. The complete legacy suite cannot currently complete in this environment because the dashboard test dependencies include Plotly, which is not installed; that dependency limitation is not reported as a passing suite.
