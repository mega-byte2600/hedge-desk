# ADR-0004: Dividend Opportunity Desk as MVP 4

Status: Accepted for architecture; implementation not started

## Decision

Add the **Dividend Opportunity Desk** as the fourth project in the Hedge Desk
MVP series. It is not currently working software and must remain labeled
`architecture_only` until its ingestion, calculations, tests, and paper workflow
exist.

The desk will calculate point-in-time ten-year dividend histories and evaluate
three mutually exclusive expressions:

1. own shares when actual dividend entitlement is part of the thesis;
2. use a defined-risk option when the thesis is directional rather than receipt
   of the dividend;
3. `NO_TRADE` when neither expression clears its gates.

A long call does not receive the issuer's cash dividend. Expected dividends,
ex-dividend dates, early exercise, assignment, option premium, volatility, and
breakeven must therefore be modeled separately.

## Required observed inputs

- declaration, ex-dividend, record, and payment timestamps;
- regular and special cash dividends adjusted for splits;
- contemporaneous price, shares, earnings, free cash flow, and net debt;
- payout ratio and coverage using values known at each historical as-of date;
- option bid, ask, size, IV, Greeks, expiration, and exercise style;
- corporate actions, delistings, transaction costs, and taxes as applicable.

## Required outputs

The desk must keep `OBSERVED`, `STAT`, `BIG`, deterministic risk/RoR, and
`HUMAN` fields distinct. Ranking by headline yield alone is prohibited. The
research output must expose dividend cuts, special distributions, payout
sustainability, price decline, total return, and yield-trap flags.

## Acceptance boundary

Architecture status may advance only when the project has deterministic
reference calculations, point-in-time fixtures, failure-path tests, a runnable
paper-only CLI path, and independent financial-model V&V. Agents cannot generate
the authoritative RoR or authorize execution.
