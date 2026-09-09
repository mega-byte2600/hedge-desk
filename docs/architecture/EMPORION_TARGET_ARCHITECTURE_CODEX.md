# EMPORION TARGET ARCHITECTURE

## High-Flyer-inspired research system scaled for a small quantitative organization

### Engineering objective

Build Emporion as **one research operating system with three clients**:

**iOS**  
**Android**  
**Web**

The product is not the website.

The product is the shared research, data, risk, provenance, and decision platform underneath all three clients.

Do not create three independent application architectures.

Do not optimize prematurely for enterprise scale.

Do not make the relational database the center of the research system.

The primary architectural principle is:

**Filesystem first for research data. APIs for application state, orchestration, authorization, and controlled access.**

The governing product principle remains:

**Survival before conviction.**

# 1. Architecture at a glance

```text
                         EMPORION

                 EXTERNAL DATA SOURCES
         Market / Bonds / Macro / SEC / News
                         │
                         ▼
                 INGESTION SERVICES
                    Python workers
                         │
                validate / normalize
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      CONTROL PLANE              DATA PLANE

       PostgreSQL                 Parquet
       transactional              file-native
       authoritative              research corpus
             │                       │
             │                       ▼
             │                     DuckDB
             │                  analytical engine
             │                       │
             └──────────┬────────────┘
                        │
                        ▼
                RESEARCH COMPUTE
                        │
             Shared asynchronous jobs
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      QUANT           RESEARCH         AI/ML
                        │
                        ▼
                 Research Results
                        │
                   Yellow Sheet
                        │
                        ▼
             DETERMINISTIC RoR
                        │
                        ▼
                  Human Review
                        │
                        ▼
                 Emporion API
                        │
           ┌────────────┼─────────────┐
           ▼            ▼             ▼
       SwiftUI       Compose         React
         iOS          Android          Web
```

# 2. The core High-Flyer principle we are copying

Do not copy High-Flyer's physical scale.

Copy its separation of **storage, metadata, compute, research jobs, and application interfaces**.

High-Flyer's 3FS architecture explicitly separates metadata services from bulk storage, uses a transactional metadata store, and exposes ordinary filesystem semantics to applications. Its design notes specifically state that many datasets are stored as CSV/Parquet and that the familiar filesystem interface reduces adaptation overhead.

Emporion should implement the same conceptual pattern at small scale:

```text
High-Flyer scale             Emporion scale

Distributed NVMe      →      Local NVMe / object storage
3FS                   →      Filesystem abstraction
FoundationDB metadata →      PostgreSQL catalog
Large compute cluster →      Mac mini + workers
CSV / Parquet         →      Parquet
Distributed analytics →      DuckDB + Python
Job scheduler         →      Lightweight job queue
```

Do not install or reproduce 3FS. At current scale, the normal filesystem gives us the interface we want.

# 3. Research data plane

Use **Apache Parquet** as the primary format for large analytical datasets: market prices, bond prices, yield curves, rates, economic series, fundamentals, derived SEC data, feature matrices, backtest inputs and outputs, model features and inference results, and historical research snapshots.

Parquet is a first-class storage contract. Do not convert every research dataset into database rows merely because PostgreSQL exists.

# 4. Local analytical engine

Use **DuckDB** as the default research query engine. DuckDB should query Parquet directly.

```sql
SELECT symbol, trading_date, close, volume
FROM read_parquet('data/normalized/equities/**/*.parquet')
WHERE symbol = 'AAPL'
  AND trading_date >= DATE '2025-01-01';
```

DuckDB supports column and predicate pushdown against Parquet. The purpose is to make the filesystem behave like a capable analytical database without operating another database server.

# 5. Filesystem contract

```text
data/
  raw/
    market/
    bonds/
    rates/
    macro/
    fundamentals/
    filings/
    news/
    alternative/
  normalized/
    equities/
    bonds/
    rates/
    macro/
    fundamentals/
  features/
    market/
    fundamental/
    macro/
    cross_asset/
    risk/
  research/
    candidates/
    desks/
    scenarios/
    model_outputs/
  backtests/
  models/
    training/
    inference/
    evaluation/
  snapshots/
  manifests/
  quarantine/
```

Rules: `raw` is immutable whenever practical. `normalized` contains validated canonical schemas. `features` contains reproducible derived datasets. `research` contains derived outputs. `quarantine` contains failed or suspicious ingestion. `manifests` describes datasets. Never silently rewrite historical raw data.

# 6. Dataset partitioning

Partition large datasets predictably, for example:

```text
data/normalized/equities/
  venue=NASDAQ/
    symbol=AAPL/
      year=2026/
        month=09/
          part-000.parquet
```

Potential dimensions include asset class, venue, symbol, year, month, and source. Do not over-partition into millions of tiny files. Benchmark realistic file sizes before establishing production defaults.

# 7. Dataset manifests

Every material dataset should have metadata independent of the files themselves.

```json
{
  "dataset_id": "us_equity_daily",
  "schema_version": "1.2.0",
  "source": "provider_name",
  "created_at": "2026-09-08T21:00:00Z",
  "min_timestamp": "2000-01-01",
  "max_timestamp": "2026-09-08",
  "row_count": 183294882,
  "format": "parquet",
  "partitioning": ["symbol", "year"],
  "validation_status": "passed",
  "checksum": "...",
  "parent_dataset": null
}
```

The system must know what the data is, where it came from, when it was retrieved, which schema and transformation produced it, whether validation passed, and which downstream research used it.

# 8. PostgreSQL control plane

PostgreSQL is the authoritative transactional system. It is **not** the bulk research warehouse.

Store users, organizations, permissions, candidates, watchlists, research job state, dataset catalog/manifests, provenance metadata, Yellow Sheets, scenario metadata, portfolio state, RoR evaluations, compliance state, human approvals, audit events, model registry metadata, integration configuration, application configuration, and notification state.

Never store millions of market observations in PostgreSQL merely because it is convenient.

# 9. Database provider

Do not architect Emporion around Supabase. Architect around **PostgreSQL**.

Supabase may provide managed PostgreSQL, authentication, storage, and developer tooling. The application must remain portable to another PostgreSQL provider. Use normal migrations. Avoid vendor-specific database features unless materially useful. Apply PostgreSQL row-level security where appropriate.

# 10. Compute plane

Research desks must not own dedicated infrastructure. They submit jobs to a common compute layer.

```text
               EMPORION JOB SYSTEM

                      Queue
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
   ingestion         quant          AI/model
      jobs            jobs             jobs
       └───────────────┼───────────────┘
                       ▼
                Worker scheduler
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
      Mac mini      Render CPU      GPU later
```

Initially avoid Kubernetes, Kafka, Spark, Ray clusters, distributed databases, and distributed filesystem software unless empirical workload proves they are needed. Start with a lightweight durable worker queue.

# 11. Job contract

Every job should have `job_id`, `job_type`, `requested_by`, `created_at`, `started_at`, `completed_at`, `status`, `input_dataset_ids`, `input_parameters`, `code_version`, `model_version`, `output_dataset_ids`, `logs`, and `error_state`.

Valid states: `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `BLOCKED`.

A material output must be traceable to dataset version, source, code version, model version, parameters, and execution timestamp.

# 12. API philosophy

Do not use APIs internally simply because APIs look modern. Use direct filesystem access when worker and data plane share trusted infrastructure.

Use APIs for mobile and web applications, authentication, authorization, workflow mutation, job submission, application state, remote compute coordination, service integrations, and risk evaluation requests.

Do not route a 40 GB Parquet dataset through REST. Submit a job or reference a dataset location instead.

# 13. Emporion API

Use Python and FastAPI unless repository inspection demonstrates a stronger existing foundation. Version the application contract under `/api/v1/`.

Core namespaces:

```text
/auth
/candidates
/desks
/research
/datasets
/jobs
/scenarios
/yellow-sheets
/risk
/portfolio
/integrations
/system
```

Representative endpoints:

```text
GET  /api/v1/candidates
GET  /api/v1/candidates/{id}
GET  /api/v1/datasets
GET  /api/v1/datasets/{id}
POST /api/v1/jobs
GET  /api/v1/jobs/{id}
POST /api/v1/scenarios
POST /api/v1/yellow-sheets
PUT  /api/v1/yellow-sheets/{id}
POST /api/v1/risk/evaluate
GET  /api/v1/system/health
```

# 14. Contract-first clients

Create an OpenAPI contract from the backend. Generate or strongly type client models from the contract for Swift, Kotlin, and TypeScript. Do not independently recreate candidate, risk, or Yellow Sheet schemas three times. Native view models are fine; domain vocabulary must remain common.

# 15. iOS application

Use **Swift + SwiftUI**.

```text
Views
  │
View Models
  │
Repositories
  │
API Client + Local Cache
```

Optimize for candidate monitoring, what changed, research summaries, evidence review, Yellow Sheet capture, risk state, notifications, human decision workflows, and portfolio awareness. Do not turn the phone into the primary large-scale backtesting environment. Do not make iOS authoritative for Risk of Ruin.

# 16. Android application

Use **Kotlin + Jetpack Compose**.

```text
Compose UI
    │
ViewModel
    │
Repository
    │
Remote API + Local DB/cache
```

Use coroutines and Flow. Do not allow Compose UI elements to call remote services directly.

# 17. Mobile local data

Cache candidate summaries, recent research, desk metadata, Yellow Sheet drafts, non-sensitive configuration, and recent risk results. Cached state is never authoritative for portfolio controls.

An offline device must never generate an implicit RoR PASS.

Risk states: `NOT_EVALUATED`, `PASS`, `BLOCK`, `INVALID_INPUT`, `STALE`, `UNAVAILABLE`.

# 18. Offline strategy

Mobile is **offline tolerant, not offline authoritative**. Users can open recent research, review cached candidates, draft Yellow Sheets, and read previously retrieved evidence. Draft changes may synchronize later.

Portfolio state, risk approval, broker connectivity, execution, and authoritative decision records must reconcile with the server.

# 19. Web application

Do not abandon web. Reduce its strategic role initially. Use **React + TypeScript**.

Web is the research workstation for large tables, data exploration, comparisons, deep research, dataset inspection, scenario analysis, Yellow Sheet editing, administration, integration configuration, and diagnostics.

Mobile is the monitoring and decision companion. Web is the deep-work surface.

# 20. Product surfaces

```text
WEB
Explore
Analyze
Compare
Configure
Investigate
Build

MOBILE
Monitor
Review
Capture
Respond
Approve
Observe
```

Do not force identical layouts. Share domain semantics, not pixel design.

# 21. Risk of Ruin

Risk of Ruin remains an independent deterministic control.

```text
Research → Candidate → Yellow Sheet → Risk inputs → RoR Engine → PASS/BLOCK → Human review
```

AI cannot override RoR, change PASS/BLOCK, silently replace deterministic inputs, or manufacture missing risk data. The authoritative risk engine runs server-side or in trusted compute. Clients display results.

# 22. Integration architecture

External systems use provider adapters:

```text
Emporion
   ├── MarketDataProvider
   ├── MacroDataProvider
   ├── FilingProvider
   ├── NewsProvider
   ├── ModelProvider
   ├── BrokerProvider
   └── NotificationProvider
```

Vendor semantics stop at the adapter boundary. The rest of Emporion uses its own domain models.

# 23. Secrets

No secret belongs in React, Swift source, Kotlin source, GitHub, Parquet datasets, dataset manifests, or API responses. Use environment-specific secure configuration. Backend service credentials remain server-side.

# 24. Growth model

## Stage 0

`Mac mini → Parquet → DuckDB → Python`

## Stage 1

`React / Swift / Kotlin → FastAPI → PostgreSQL → local Parquet/DuckDB → worker process`

## Stage 2

`Clients → FastAPI instances → PostgreSQL → Job queue → Workers → Object storage → Parquet`

Move durable research files to S3-compatible storage while preserving logical paths and manifests.

## Stage 3

Only if measured: Redis, additional workers, dedicated compute, GPU services, ClickHouse, stream processing.

## Stage 4

Only at institutional scale investigate distributed analytical engines, distributed scheduling, dedicated storage clusters, high-speed networking, specialized distributed filesystems, and multi-region control planes.

# 25. Repository architecture

Prefer a monorepo while the organization is small.

```text
emporion/
  apps/
    web/
    ios/
    android/
  services/
    api/
    worker/
    risk/
  packages/
    contracts/
    schemas/
    domain/
  research/
    ingestion/
    features/
    models/
    backtests/
    notebooks/
  data/
    manifests/
    schemas/
  infra/
    render/
    database/
    local/
  tests/
    contract/
    integration/
    e2e/
  docs/
    architecture/
    datasets/
    api/
    operations/
```

Do not split into many repositories until team boundaries require it.

# 26. Research code versus application code

Keep them visibly separate: application system under `services/`; research system under `research/`. Notebooks are exploratory. Production research logic must move into tested Python modules/jobs. Never make a notebook the sole production implementation of a critical calculation.

# 27. Dataset schemas

Define schemas centrally: `Instrument`, `Quote`, `Bar`, `YieldCurvePoint`, `MacroObservation`, `FundamentalObservation`, `SourceRecord`, `Candidate`, `ResearchResult`, `Scenario`, `YellowSheet`, `RiskEvaluation`.

Schema changes require versioning. A research result retains the schema version that produced it.

# 28. Provenance

Every significant research observation needs source, `retrieved_at`, `effective_at`, dataset, dataset version, transformation, and quality status.

Emporion must be able to trace:

`Candidate → Research Result → Feature → Dataset → Source`

and answer: **Where did this conclusion come from?**

# 29. Testing

Required layers: unit tests, dataset/schema validation, API contract tests, research job tests, risk engine tests, integration adapter tests, Swift tests, Android tests, React tests, and end-to-end workflows.

A `RiskEvaluation` returned by the API must have equivalent semantics on web, iOS, and Android. The same applies to Candidate, YellowSheet, Scenario, JobState, and ResearchResult.

# 30. Observability

Every deployed component identifies environment, version, Git SHA, and health. Use correlation IDs across API and workers. Log job IDs and dataset IDs. Do not log secrets or private research text indiscriminately.

# 31. Performance philosophy

Measure dataset scan latency, queue wait time, job execution time, API latency, database query latency, Parquet size/file count, DuckDB query performance, mobile startup/synchronization, and web load. Add infrastructure only in response to measured bottlenecks.

# 32. Explicitly prohibited premature architecture

Do not introduce Kubernetes, Kafka, Spark, Hadoop, 3FS, FoundationDB, Cassandra, MongoDB, Elasticsearch, ClickHouse, Redis, microservice explosion, GraphQL, service mesh, or multiple cloud providers merely for architectural sophistication. Require a demonstrated requirement and benchmark.

Elegant architecture means fewer components with clear responsibilities.

# 33. First implementation sequence

**Phase A:** Document existing Emporion behavior, lock current tests, create ADRs.

**Phase B:** Establish Parquet conventions, dataset manifest schema, DuckDB research interface, PostgreSQL catalog.

**Phase C:** Create durable job abstraction and move ingestion/research operations behind jobs.

**Phase D:** Create versioned FastAPI contract and common application schemas.

**Phase E:** Modernize React web client against the new contract. Do not rewrite backend logic into React.

**Phase F:** Build iOS client in SwiftUI: Overview, Candidates, Candidate detail, Research, Risk, Yellow Sheets, Settings.

**Phase G:** Build Android equivalent using Compose with API/domain parity.

**Phase H:** Add authentication and controlled synchronization.

**Phase I:** Add external service adapters.

**Phase J:** Benchmark before adding infrastructure.

# 34. Architecture acceptance test

Codex is not finished until it demonstrates:

```text
External data source
      ↓
ingestion job
      ↓
validated Parquet dataset
      ↓
dataset manifest
      ↓
PostgreSQL catalog registration
      ↓
DuckDB research query
      ↓
research job
      ↓
candidate
      ↓
Yellow Sheet
      ↓
deterministic RoR evaluation
      ↓
API
      ↓
Web + iOS + Android
```

All three clients must show the same authoritative state.

# 35. Architectural North Star

Emporion grows by scaling four independent planes: **DATA, COMPUTE, CONTROL, CLIENT**.

Do not entangle them.

The result should permit one machine today, several workers tomorrow, and cloud storage plus a compute cluster later without rewriting the research model.

That is the High-Flyer lesson worth copying: not its hardware or scale, but the discipline of separating the data plane from compute and control planes.

# 36. Final Codex instruction

Before making architectural changes:

1. Inspect the current repository completely.
2. Map existing components to this target architecture.
3. Preserve working functionality.
4. Identify what already satisfies the design.
5. Create ADRs for material deviations.
6. Implement incrementally.
7. Run tests after each material migration.
8. Never overwrite newer unrelated work.
9. Never force push `main`.
10. Do not add infrastructure unless it solves a demonstrated requirement.
11. Keep filesystem and Parquet workflows first-class.
12. Keep authoritative risk logic outside all presentation clients.
13. Preserve portability across hosting providers.
14. Record every deployment with timestamp, branch, commit, tests, and production status.

The desired outcome is not the largest architecture.

It is the **smallest architecture that retains the structural advantages of a world-class quantitative research platform**.
