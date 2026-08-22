# Strategic allocation policy boundary

The portfolio gate operationalizes two broad research principles: diversify
across distinct economic risk sources, and treat unusually high long-horizon
equity valuation as a concentration warning. It does not claim that David
Swensen or Robert Shiller prescribed this repository's exact thresholds.

The checked-in thresholds are explicit project policy requiring independent
validation: at least four positive-weight asset classes, no asset class above
40%, and U.S. equity capped at 30% when the supplied CAPE is at least 30. The
gate requires exact Decimal weights summing to one. It calculates no Risk of
Ruin, forecasts no return, and authorizes no trade.

Before production, the policy needs point-in-time, methodology-consistent CAPE
evidence; tax/liability/liquidity constraints; correlation/regime stress;
instrument look-through; and independent investment-policy approval. Swensen's
institutional/endowment context must not be copied into a personal portfolio
without suitability and implementation analysis.
