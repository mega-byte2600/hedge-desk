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

## What a Yellow Sheet is for

A Yellow Sheet is the internal investment-thesis and diligence record for a research idea. It exists to force the idea into a testable form before capital is considered: what attracted attention, what hypothesis is being tested, which evidence supports or contradicts it, what would invalidate it, which rule would permit action, and what must be reviewed afterward.

The longer-term vision may include a disciplined group of capital partners in which mbolton acts in a sponsor or GP role and qualified partners evaluate opportunities as prospective LPs. In that context, Yellow Sheets provide a common diligence language and an auditable research trail. They are not subscription documents and do not themselves create, market, or authorize an investment.

## Capital-formation boundary

This public console is a research and engineering demonstration. It is not an offer to sell securities, a solicitation of an offer to buy securities, an invitation to subscribe to a fund, or investment advice. Viewing, writing, or exporting a Yellow Sheet is not an indication of interest or a commitment of capital.

If a future private fund or investment vehicle is formed, any investor outreach, eligibility or accreditation process where applicable, disclosures, offering documents, subscriptions, sanctions screening, custody, and acceptance of capital would occur through a separate legal and compliance process reviewed by qualified counsel and the relevant service providers. The public research console is intentionally kept separate from that process.

## Six desks

1. Overnight Premium
2. Earnings Event
3. Box / Parity Observer
4. Dividend Opportunity
5. Quant / AI Model Lab
6. Futures Event

## Public-use note

Symbols shown in the candidate board are research-universe inputs unless the UI explicitly states that a method-qualified evidence gate has been satisfied. No performance projection, return promise, or live trade authorization is implied.
