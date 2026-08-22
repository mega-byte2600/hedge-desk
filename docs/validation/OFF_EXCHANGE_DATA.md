# FINRA off-exchange transparency evidence

The official [FINRA OTC Transparency page](https://www.finra.org/filing-reporting/otc-transparency)
states that FINRA publishes delayed aggregate OTC trading information reported
by ATSs and member firms. The [FINRA Developer Center](https://developer.finra.org/docs)
documents public API datasets including `weeklySummary` and
`weeklySummaryHistoric`.

This is useful free evidence for historical participation research, but it is
not real-time dark-pool order flow, does not reveal unexecuted hidden orders,
and cannot support front-running. `evaluate_otc_weekly_observation` preserves
the publication/receipt clock, requires the declared tier delay, calculates
only descriptive shares-per-trade, and emits no directional or trade authority.

The FINRA website terms and attribution requirements still apply. Preserve the
retrieval terms, source hash, publication timestamp, query, and API version in
the private data manifest; commit only permitted data/derivatives.
