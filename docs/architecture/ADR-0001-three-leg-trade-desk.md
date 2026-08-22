# ADR-0001: Three-Leg Agentic Trade Desk and First MVP

- Status: Accepted for implementation planning
- Date: 2026-08-21
- Scope: Paper research and paper trading only

## Decision

### Locked product vision

**Corporate motto: Making money overnight - the dream: making money while you
sleep.**

The preferred MVP expression is simple, defined-risk option-premium research on
autopilot. Here, "autopilot" means the system works continuously to collect and
validate data, detect candidate patterns, call deterministic calculators, run
independent risk controls, monitor paper positions, and prepare an auditable
morning decision packet. It never means an agent can authorize a trade, generate
RoR, bypass risk, or place a live order.

The motto is aspirational and must not be represented as guaranteed or easy
profit. The MVP earns the claim only as a measured paper result: positive net
out-of-sample performance after realistic costs and tail-risk accounting,
followed by a meaningful forward paper-trading period.

The BIG/Hedge Desk will support three strategy-research legs behind one common
point-in-time data, deterministic calculation, independent risk, audit, and
human-authorization architecture:

1. defined-risk equity-option premium research;
2. U.S. equity CAPE/payout screening;
3. weather, war, logistics, and shipping event research for commodity futures.

The first MVP is a single defined-risk equity-option credit-spread workflow that
opens by selling premium and plans to close before expiration. It demonstrates
the 24/7 research system without enabling automatic or live execution.

Working MVP name: **Overnight Premium Desk**.

No strategy is assumed to make money. Profitability is an empirical acceptance
question evaluated out of sample after fees, spreads, slippage, assignment,
exercise, liquidity, financing, taxes where modeled, and tail loss.

## Common control plane

```text
Licensed/public sources
        |
        v
Point-in-time ingestion + provenance + quality gates
        |
        +--------------------+
        |                    |
        v                    v
Agent research plane     Deterministic calculation plane
retrieve/classify        prices/features/scenarios/risk
propose/explain          versioned + conventionally V&V'd
        |                    |
        +----------+---------+
                   v
            Proposed trade only
                   v
       Independent deterministic risk engine
                   v
             PASS / REDUCE / REJECT
                   v
          Mandatory human authorization
                   v
       Paper execution boundary (MVP only)
```

Agents never calculate, estimate, alter, or substitute authoritative Risk of
Ruin. The deterministic risk engine has no LLM dependency. Agent-generated
values are untrusted until a non-agentic validator accepts their source,
schema, units, timestamp, and provenance.

## Leg 1: Defined-risk option premium research

### Strategy boundary

The MVP studies liquid, defined-risk vertical credit spreads only. It excludes:

- naked calls and non-cash-secured naked puts;
- undefined maximum loss;
- contracts with stale or unvalidated quotes;
- automatic order routing;
- holding through expiration by default;
- discretionary agent-created volatility, Greeks, probabilities, or prices.

The Options Clearing Corporation states that options involve risk and that
writers can face significant losses, margin calls, liquidity changes, and
assignment risk. A spread can reduce but does not eliminate risk. See the
[OCC Characteristics and Risks of Standardized Options](https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document).

### Deterministic candidate calculations

Versioned code, not an agent, calculates:

- bid/ask-aware net credit and maximum loss;
- break-even and return on defined risk;
- days to expiration and planned exit window;
- exercise/assignment and ex-dividend flags;
- spread width, quote age, open interest, volume, and liquidity exclusions;
- implied-volatility and Greeks only from validated market inputs and a named,
  tested model;
- historical scenario P&L, gap loss, stress loss, concentration, and portfolio
  exposure;
- transaction-cost and conservative fill assumptions;
- authoritative portfolio risk, permitted size, and RoR artifact.

Uploaded Hull, MIT, Stanford, and other materials are requirements and test-case
references as cataloged in `docs/validation/SOURCE_CATALOG.md`. They are not
runtime prompts and are not copied into the public repository.

### Agent responsibilities

Agents may retrieve option-chain evidence, classify events, compare deterministic
outputs, summarize risks, challenge the thesis, and propose a candidate. The
proposal remains `PENDING` risk and `PENDING` human authorization.

### MVP acceptance test

Given a frozen historical option-chain snapshot, underlying snapshot, corporate
calendar, portfolio snapshot, model versions, and policy:

1. ingestion rejects future, revised, stale, crossed, or incomplete inputs;
2. deterministic code produces a reproducible calculation artifact;
3. the agent produces a cited proposal without creating quantitative values;
4. independent risk produces `PASS`, `REDUCE`, or `REJECT` plus immutable V&V
   evidence;
5. no paper order is created until a human explicitly authorizes that proposal;
6. replay includes realistic close-before-expiration rules, early assignment,
   fees, spreads, slippage, and adverse gaps;
7. the strategy must beat declared baselines out of sample within prespecified
   risk limits before any forward paper pilot is called successful.

### Pattern and contract-timing discipline

The strategy starts from the hypothesis that recurring, explainable patterns in
price, volatility, liquidity, events, and time decay can identify occasions when
defined-risk premium is attractive relative to loss scenarios. Pattern
recognition alone never creates an approved bet.

Each candidate must bind the pattern to the contract's actual time frame:

- observation timestamp and feature lookback;
- option quote and underlying timestamp;
- days to expiration, earnings/ex-dividend/macro events, and planned exit;
- expected decay horizon and adverse-move window;
- deterministic scenario distribution and maximum loss;
- evidence that the signal was available before the decision;
- proof that the same rule survives out-of-sample and regime-separated testing.

Agents may label or explain a pattern. Versioned deterministic code calculates
all prices, probabilities used by policy, Greeks, payoffs, scenarios, sizing,
portfolio risk, and RoR. A correct historical story without point-in-time replay
is rejected as leakage.

## Leg 2: U.S. equity CAPE and payout screen

### Methodological correction

Robert Shiller's published CAPE data are primarily a long-history aggregate U.S.
market series, not a ready-made ranking of individual companies. His data also
notes that the shift from dividends toward repurchases affects CAPE and provides
a total-return CAPE treatment. See [Robert Shiller's Yale data page](https://www.econ.yale.edu/~shiller/data.htm).

The desk will therefore implement two distinct views:

1. aggregate market/regime CAPE and total-return CAPE context;
2. an explicitly named company-level cyclically adjusted earnings/payout screen,
   validated as a separate model rather than called "Shiller CAPE" by default.

### Point-in-time screen inputs

- historical prices and membership, including delisted securities;
- as-reported earnings with publication/availability/revision timestamps;
- CPI/deflator convention;
- dividends, special dividends, repurchases, issuance, and splits;
- sector and accounting comparability flags;
- liquidity, market capitalization, leverage, profitability, and payout coverage.

Deterministic scoring keeps valuation and payout dimensions separate: cyclically
adjusted earnings yield, dividend yield, net payout/shareholder yield, coverage,
quality, leverage, and drawdown. Negative/missing earnings, financial-sector
comparability, major restructurings, and insufficient history are explicit flags,
not silently imputed values.

The output is a research-priority funnel, never an automatic buy list. Every top
candidate must state what is priced in, first rejection risk, what makes it
investable, what kills it, and the next diligence workflow.

## Leg 3: Weather, war, logistics, and shipping futures research

### Event-sensing architecture

Crawler/connectors ingest only permitted sources and retain timestamps, license,
checksums, revisions, and raw evidence. Candidate source families include:

- NOAA/NCEI observations and climate data via the
  [Climate Data Online API](https://www.ncei.noaa.gov/cdo-web/webservices/v2);
- USDA crop, citrus, condition, acreage, yield, and production publications;
- EIA petroleum, trade, inventory, production, and forecast data through the
  [EIA Open Data API](https://www.eia.gov/opendata/documentation.php);
- EIA oil-transit chokepoint analysis and licensed shipping/AIS feeds;
- exchange contract specifications, settlement calendars, warehouse/delivery
  rules, and licensed futures curves;
- official government alerts, sanctions, port/canal notices, and suitably
  licensed news.

Agents may identify and connect events (for example, freeze/hurricane exposure to
citrus regions or a shipping disruption to an oil route). Deterministic code must
quantify location exposure, forecast surprise, crop/flow sensitivity, futures
curve state, basis, roll, liquidity, margin, scenarios, and portfolio risk.

### No textbook-obvious-profit assumption

Known weather, disasters, war, and shipping disruption may already be reflected
in futures prices. The CFTC specifically warns against easy-profit claims based
on seasonal weather, natural disasters, war, or other well-known information;
leveraged futures losses can exceed initial deposits. See the
[CFTC seasonal-information advisory](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_seasonal.html),
[natural-disaster advisory](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_falseprom.html),
and [futures market basics](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/FuturesMarketBasics/index.htm).

The research question is therefore not "did an event occur?" It is:

```text
validated event surprise
minus what the curve already prices
minus basis/roll/cost/liquidity effects
under deterministic scenarios and portfolio limits
```

No futures execution is part of the first MVP.

## Shipping-data intake

User-provided trackers are welcome. Before use, record provider, field dictionary,
timestamp semantics, update latency, coverage, correction behavior, license,
redistribution limits, vessel identity method, port/geofence method, missing-data
behavior, and known spoofing/blackout limitations. Restricted AIS/shipping data
must remain outside the public repository; only permitted metadata and synthetic
or redistributable fixtures may be committed.

EIA notes that disruption of major oil chokepoints can delay supply and increase
shipping costs, but this physical-market fact does not itself establish a
tradable futures edge. See [EIA World Oil Transit Chokepoints](https://www.eia.gov/international/content/analysis/special_topics/World_Oil_Transit_Chokepoints/).

## Delivery sequence

1. Implement the common typed evidence/calculation/proposal/risk/authorization
   contracts and architecture tests.
2. Build the option credit-spread frozen-snapshot demo with deterministic V&V.
3. Add strict historical replay and paper monitoring; do not optimize on the
   test set.
4. Build the CAPE/payout point-in-time screen as a research funnel.
5. Add weather and energy observation pipelines and event labeling.
6. Accept a licensed shipping tracker and build synthetic disruption fixtures.
7. Add futures research proposals only after contract, curve, margin, delivery,
   basis, and roll models pass independent V&V.

## Deferred decisions

- exact option universe, DTE band, delta/strike selection, profit target, stop,
  and exit timing;
- licensed option-chain and historical quote provider;
- company-level cyclically adjusted earnings definition and payout weights;
- exact commodity contracts and exchange data licenses;
- shipping/AIS provider and permitted retention/redistribution;
- capital and portfolio policy thresholds;
- any live or brokerage connectivity.
