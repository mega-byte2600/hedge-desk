# BIG Data Source Architecture

Date: 2026-08-21

## Decision

Use an open-source-first ingestion framework with entitlement-aware source
adapters. The public repository contains schemas, transforms, manifests, hashes,
synthetic fixtures, and small permission-cleared reference cases. It does not
contain scraped or licensed vendor payloads.

There is no adequate free/open authoritative stack for all of:

- survivorship-clean U.S. equity prices, corporate actions, historical universe
  membership, and delisting returns;
- point-in-time analyst estimate vintages;
- complete historical options chains, executable quotes, IV, and Greeks.

Claims of unbiased profitability in those domains require licensed Tier 1 data.

## Tier 0: open and official MVP stack

| Domain | Preferred sources | Role |
|---|---|---|
| Filings and actuals | [SEC EDGAR/XBRL APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), issuer IR | Legal entity, filings, earnings actuals, guidance, primary evidence |
| Macro and vintages | BLS, BEA, Federal Reserve, [FRED/ALFRED](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html), U.S. Treasury | CPI, labor, rates, liquidity, release/vintage-aware features |
| Current universe | Nasdaq symbol directory | Bootstrap only; not historical-universe evidence |
| Futures positioning | [CFTC COT historical files](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm) | Weekly positioning context with separate as-of/release dates |
| Weather | [NOAA/NCEI CDO](https://www.ncei.noaa.gov/cdo-web/webservices/v2), National Weather Service | Observations, climatology, alerts, revisions |
| Agriculture | [USDA NASS Quick Stats](https://www.nass.usda.gov/developer/), WASDE, Crop Progress | Acreage, condition, yield, production, scheduled releases |
| Energy | [EIA API v2](https://www.eia.gov/opendata/documentation.php) | Inventories, production, storage, trade, forecasts |
| U.S. shipping research | [NOAA/BOEM/USCG Marine Cadastre AIS](https://coast.noaa.gov/digitalcoast/data/vesseltraffic.html) | Historical U.S. vessel traffic and congestion research |
| News/events | SEC/IR, Federal Register, official agency alerts | Primary event evidence |
| Tests | Synthetic option/equity/event snapshots | Deterministic public unit and architecture tests |

Tier 0 supports provenance, event detection, deterministic calculations,
orchestration, and paper demonstrations. It does not support claims of complete
or execution-grade market coverage.

## Tier 1: licensed research and market-data upgrades

| Need | Preferred family | Repository rule |
|---|---|---|
| Security master, delistings, corporate actions, survivorship-safe equity returns | CRSP | No raw rows in Git; manifests and derived aggregate expectations only |
| Standardized fundamentals and links | Compustat / CRSP-Compustat Merged | Metadata only |
| Point-in-time analyst estimates | IBES | Metadata only |
| Academic historical options | OptionMetrics IvyDB | Metadata only |
| Real-time U.S. options | OPRA via entitled vendor; Cboe LiveVol/Hanweck/DataShop | No payloads without express redistribution rights |
| Intraday equities | TAQ or licensed consolidated/direct feeds | Metadata only by default |
| Futures curves and settlements | CME DataMine or licensed exchange vendor | Effective-dated specs; payloads outside Git |
| Timestamped news | Reuters, Dow Jones, LSEG, Bloomberg or other licensed feed | Metadata only unless contract permits excerpts/fixtures |
| Global shipping/cargo | Spire, Kpler, Vortexa, MarineTraffic or equivalent | Contract-specific; metadata only |

The conventional empirical-finance research family includes CRSP, Compustat,
CRSP/Compustat Merged, IBES, OptionMetrics, TAQ, the Fama-French Data Library,
SEC filings/XBRL, FRED/ALFRED, and appropriately licensed Cboe series. This is a
description of common research infrastructure, not an endorsement by Yale, HBS,
Tuck, or any other institution.

## Aggregator boundary

- Earnings Whispers is human-only unless written commercial machine-use rights
  are obtained. Its reviewed terms restrict content to personal non-commercial
  use and restrict reproduction/distribution.
- [Finviz API usage rules](https://finviz.com/knowledge-base/market-data-research/api/usage-limits)
  identify personal-use licensing and prohibit redistribution, republishing, and
  raw historical exports. Finviz may be a human discovery interface but is not a
  canonical crawler or public-fixture source without negotiated rights.
- Cboe delayed quote pages are human reference only where automated extraction
  is prohibited. Use licensed Cboe/OPRA products for machine ingestion.

Aggregators never outrank issuer, regulator, exchange, or entitled primary data.

## Canonical observation contract

Every observation retains:

```text
source_id
original_identifier
observation_time
release_time
available_at
ingestion_time
effective_date
revision_or_vintage
retrieval_url
terms_version
content_hash
schema_version
transformation_version
entitlement_class
```

Source adapters must fail closed on unknown units, timestamp semantics,
revision status, entitlement, or identifier mapping.

## Fixture and storage policy

- Government/open data: small, dated, attributed fixtures only after checking
  dataset-specific reuse terms.
- Issuer documents: accession/URL, timestamps, hashes, and minimal factual
  extracts; do not mirror full copyrighted releases by default.
- Exchange/vendor/academic licensed data: raw payloads remain outside Git unless
  the contract expressly permits redistribution.
- Public unit tests: synthetic inputs.
- Golden integration tests: tiny permission-cleared snapshots.
- Backtests: entitlement-aware external storage with immutable manifests and
  reproducible transforms.

## Acquisition order

1. Implement Tier 0 adapters and canonical lineage contracts.
2. Use synthetic fixtures for the option and earnings MVP vertical slices.
3. Obtain CRSP/Compustat/IBES or an equivalent point-in-time research license for
   equity/earnings validation.
4. Obtain OptionMetrics for historical options research or an equivalent
   licensed source with quote/contract detail.
5. Add OPRA/Cboe and CME entitlements only when forward paper monitoring needs
   execution-quality data.
6. Add licensed news and shipping sources only after their incremental signal is
   defined and testable.

## Off-exchange and dark-market research

Public data can support statistical inference about off-exchange activity, but
not identification of a hedge fund, beneficial owner, hidden order, or intent.

Source layers:

- consolidated equity trades reported through FINRA Trade Reporting Facilities
  for transactions executed otherwise than on an exchange;
- licensed TAQ/consolidated feeds with trade conditions, timestamps, quotes, and
  off-exchange identifiers;
- delayed [FINRA OTC/ATS transparency](https://www.finra.org/filing-reporting/otc-transparency)
  for issue/venue volume and concentration;
- public [SEC Form ATS-N filings](https://www.sec.gov/about/divisions-offices/division-trading-markets/alternative-trading-systems/form-ats-n-filings-information)
  for venue operating methods and conflicts;
- Rule 605 execution-quality reports where applicable;
- FINRA short-volume context, explicitly not mislabeled as short interest;
- delayed 13F holdings as coarse validation context only, never event-time labels.

Confidential CAT data, subscriber identity, live hidden ATS order books, and
hedge-fund intent are unavailable to this public system. The model must use
`institutional_like_off_exchange_flow` terminology rather than `hedge_fund_trade`.

### Deterministic statistical inference model

Versioned non-LLM software may estimate a latent off-exchange flow state from
pre-registered features such as:

- off-exchange share of volume and change versus a rolling baseline;
- trade-size distribution, odd-lot/block buckets, and signed-flow estimators;
- ATS venue concentration and delayed volume changes;
- spread, depth, volatility, order imbalance, and price impact;
- post-trade mark-outs over fixed horizons;
- sector/index-neutral abnormal volume and return;
- borrow, short-volume, corporate-event, and earnings-window controls.

The STAT model may output a probability and calibrated uncertainty. It may not output
a named actor or assert manipulation, accumulation, distribution, or direction
as fact without direct evidence.

### Statistical evidence standard

- Pre-register the feature set, direction, horizon, universe, exclusions,
  estimator, and primary endpoint.
- Report effect size and a 95% confidence interval for interpretability.
- Require `p < 0.005` for confirmatory claims, after the prespecified
  multiple-testing correction.
- Use time-ordered development, validation, and untouched test periods.
- Report calibration, false-discovery rate, sensitivity to trade-signing method,
  clustered dependence, regime stability, costs, and data-delay effects.
- A 95% confidence interval and `p < 0.005` are separate requirements; do not
  describe one as satisfying the other.
- Exploratory findings are labeled exploratory and cannot drive a risk gate.

### Mandatory output labels

Every research packet keeps these fields visually and structurally separate:

| Label | Meaning | Authority |
|---|---|---|
| `OBSERVED_STATISTIC` | Direct deterministic calculation from identified sourced data | Reproducible fact about the dataset, subject to source limits |
| `STAT_MODEL_OUTPUT` | Probability, effect estimate, p-value, confidence interval, and calibration from the named deterministic statistical model requested for off-exchange inference | Statistical model output, never an observed fact |
| `BIG_MODEL_OUTPUT` | BIG's integrated research conclusion combining validated observations, STAT outputs, deterministic finance artifacts, sourced fundamentals/events, and structured agent work | Proposed research conclusion, never an observed statistic or authorization |
| `AGENT_INTERPRETATION` | Agent-generated explanation, hypothesis, contradiction, or summary | Non-authoritative narrative |
| `RISK_POLICY_DECISION` | PASS/REDUCE/REJECT from independent deterministic risk software | Machine control |
| `COMPLIANCE_POLICY_DECISION` | PASS/REVIEW/REJECT from independent compliance controls | Machine/control decision with escalation where required |
| `HUMAN_DECISION` | Explicit authorization or rejection by an identified human | Final authorization |

Agents may explain `OBSERVED_STATISTIC`, `STAT_MODEL_OUTPUT`, and
`BIG_MODEL_OUTPUT` artifacts but cannot edit, relabel, or promote them. Neither
model output becomes an `OBSERVED_STATISTIC`, regardless of confidence.

### Human factor and decision point

Human judgment is neither an observed statistic nor a BIG model inference. It
has its own input and output records:

- `HUMAN_CONTEXT`: stated objective, loss tolerance, constraints, conflicts,
  fatigue/time-zone acknowledgement, and unresolved questions;
- `HUMAN_REVIEW`: acknowledgement of the exact evidence, model uncertainty,
  agent counter-thesis, risk result, compliance result, costs, and maximum loss;
- `HUMAN_DECISION`: `APPROVE_PAPER`, `REJECT`, or `REQUEST_MORE_EVIDENCE` with
  identity, timestamp, rationale, and immutable candidate hash.

The interface must not collapse these lanes into a single score. It presents:

```text
Observed statistics
STAT model output + uncertainty
BIG model output
Agent interpretation + skeptic view
Deterministic risk decision
Deterministic compliance decision
Unresolved evidence gaps
---------------- HUMAN DECISION POINT ----------------
Approve paper | Reject | Request more evidence
```

A human can reject any candidate. A human cannot convert `RISK ... REJECT` or
`COMPLIANCE ... BLOCK` into approval. Any input, policy, model, price, size,
instrument, or timestamp change invalidates the approval token and returns the
candidate to review.

## News, RSS, and discussion-source gap filling

News and feeds form a discovery and context plane, not the authoritative market,
fundamental, or risk-calculation plane.

Preferred tiers:

1. Official issuer/regulator/agency feeds. The SEC provides
   [EDGAR and SEC RSS feeds](https://www.sec.gov/about/rss-feeds), including
   company/form-filtered EDGAR searches.
2. Licensed professional news. Reuters content and APIs require an appropriate
   [Reuters license](https://reutersagency.com/license-reuters-content/); raw
   stories are not committed or redistributed unless the contract permits it.
3. Open event discovery. GDELT event, mention, and knowledge-graph data may
   provide multilingual weak signals, but underlying article rights remain
   separate and events require primary-source confirmation.
4. Public RSS and newsgroups. These may generate hypotheses and sentiment/burst
   indicators only after feed-specific license review, manipulation controls,
   source scoring, deduplication, timestamp validation, and corroboration.

The ingestion record retains publisher, author/account where public, URL/message
ID, publication and observation times, update/delete state, license, content
hash, language, extraction version, and corroborating primary evidence.

No discussion item may directly populate reported earnings, consensus, price,
contract, position, risk, or compliance fields. Suspected leaks, hacked material,
embargoed releases, private tips, or possible MNPI are quarantined.

The STAT model may compute source reliability, novelty, burst, cross-source
agreement, sentiment, and event probability with uncertainty. The BIG model may
use validated STAT outputs as one input. An agent may summarize the narrative.
All remain distinct from primary facts and the human decision.
