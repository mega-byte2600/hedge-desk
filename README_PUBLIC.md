# Hedge Desk Research Console

Hedge Desk is an independent, paper-only research platform built by **mbolton** to evaluate six specialized market research workflows with explicit evidence requirements, deterministic controls, and human review.

## Goal

Produce research candidates that are explainable, reproducible, and control-gated before any human decision. The public MVP does not place live orders and does not represent seed-universe symbols as qualified trade recommendations.

## Current MVP status

- Six research desks are exposed through the web console.
- Candidate symbols are a seed research universe, not method-qualified picks.
- Golden Master, white-box, black-box, smoke, CodeQL, and secret-pattern checks gate deployment.
- Live order execution is disabled.
- Supabase is used for backend connectivity health; the public MVP does not expose secrets.

## Data and research sources

The current public console uses validated synthetic fixtures for deterministic research demonstrations and a code-ready Papers With Backtest news adapter for licensed research workflows. Public High-Flyer / DeepSeek research, models, repositories, methods, and open infrastructure may inform the Quant / AI Model Lab where applicable, but proprietary hedge-fund data, internal signals, positions, or non-public research are not represented as available.

## Market data timing

The current public MVP is **not connected to a real-time quote feed**. Therefore a market-data delay such as “15 minutes” or “20 minutes” would be misleading. The console displays **Reference snapshot / Quote delay: N/A** until a timestamped market-data provider is connected. When a provider is added, the UI should show provider, entitlement, as-of timestamp, and measured delay from the last received quote.

## Research controls

Every candidate remains non-authorized until required evidence is present and deterministic controls pass. The Yellow Sheet workflow records Interest → Hypothesis → Investigation → Evidence → Rule → Trade → Review. No Yellow Sheet means no trade. Portfolio survival / Risk of Ruin logic remains independent of LLM-generated research, and human authorization is required before any future live execution path.

## Six desks

1. Overnight Premium
2. Earnings Event
3. Box / Parity Observer
4. Dividend Opportunity
5. Quant / AI Model Lab
6. Futures Event

## Public-use note

This site is a research and engineering demonstration, not investment advice. Symbols shown in the candidate board are research-universe inputs unless the UI explicitly states that a method-qualified evidence gate has been satisfied.
