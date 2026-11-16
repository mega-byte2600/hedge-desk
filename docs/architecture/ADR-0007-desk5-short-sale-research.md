# ADR-0007: Desk 5 Short Sale Research

- Status: Accepted for research-scope change; implementation remains a research
  framework until connected to the approved watchlist and live primary-source
  evidence workflow.
- Date: 2026-11-16
- Supersedes the Desk 5 product scope in ADR-0005. The legacy project identifier
  `open-quant-ai-model-lab` remains stable for existing reports and mobile clients.

## Decision

Desk 5 is the Short Sale Research Desk. Its purpose is to develop, source, and
challenge short-sale research candidates from the GP-approved watchlist. It does
not run a default universe or treat an index ETF as a short thesis.

Each case must include a point-in-time bear thesis; SEC filing evidence and
independent corroboration; catalyst and timing; valuation basis; strongest
counter-thesis; liquidity and volatility context; dated short-interest source;
borrow status; conflicts disclosure; and explicit thesis-invalidation conditions.
Incomplete research stays incomplete. A complete case may advance only to
independent human review.

## Professional and regulatory reference lenses

- CFA Institute Standards V(A), V(B), and VI(A): reasonable basis, clear
  communication, and conflict identification/disclosure.
- FINRA Series 7 content outline: short-sale order marking, locate, borrow,
  delivery, securities lending, and Regulation SHO knowledge.
- FINRA Series 4 content outline: supervisory lens for options-related Desk 5
  research; it does not turn this application into a registered supervisor.
- SEC Regulation SHO Rules 200, 201, 203, and 204: execution-side marking,
  price-test, locate, and close-out requirements. Desk 5 does not certify these.

## Key boundaries

- Borrow/locate availability and fees are broker-specific and time-sensitive;
  unknown stays unknown and cannot be represented as borrowable.
- Short-sale volume is not the same measure as reported short interest.
- Desk 5 does not create a composite score, probability, price target, order,
  locate, or trade authorization.
- Market data and watchlist membership must be validated by existing
  non-agentic data controls before an item enters a candidate set.

## References

- CFA Institute, Standard V(A), Diligence and Reasonable Basis:
  https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-v-a
- CFA Institute, Standard V(B), Communication with Clients and Prospective Clients:
  https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-v-b
- CFA Institute, Standard VI(A), Avoid or Disclose Conflicts:
  https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-vi-a
- FINRA, Series 7 Content Outline:
  https://www.finra.org/sites/default/files/2025-10/Series_7_Content_Outline.pdf
- FINRA, Series 4 Content Outline:
  https://www.finra.org/sites/default/files/Series_4_Outline.pdf
- SEC, Regulation SHO FAQs:
  https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8
- FINRA, Short Interest — What It Is, What It Is Not:
  https://syndication.finra.org/content/short-interest-what-it-what-it-not
