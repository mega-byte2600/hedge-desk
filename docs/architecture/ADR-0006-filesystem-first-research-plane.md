# ADR-0006: Filesystem-First Research Data Plane

## Status

Accepted

## Context

Emporion is one research operating system with web, iOS, and Android clients. The product is the shared research, data, risk, provenance, and decision platform underneath those clients. Bulk research data should not be forced into PostgreSQL rows simply because PostgreSQL exists.

## Decision

Emporion treats Parquet files under `data/` as the primary analytical storage contract for material research datasets. PostgreSQL remains the control plane for users, permissions, job state, catalog metadata, approvals, audit events, and application state.

The initial implementation adds strict Python contracts for:

- dataset manifests with provenance, storage path, row count, validation status, partitioning, checksum, parent dataset, transformation, and canonical manifest hash;
- durable research jobs with input/output dataset IDs, parameters, code version, optional model version, logs, status, timestamps, and error state.

DuckDB is the preferred analytical reader for Parquet once production query code is introduced, but this ADR does not add a new runtime dependency until a measured workload requires it.

## Consequences

- Workers can read local or object-backed Parquet directly instead of routing large datasets through REST.
- Clients and APIs exchange dataset IDs, job IDs, and summaries, not bulk market observations.
- Dataset changes become auditable through manifest hashes.
- Job outputs remain traceable to input datasets, parameters, code version, model version, and execution timestamps.
- PostgreSQL or Supabase may catalog the manifests, but neither becomes the bulk research warehouse.

## Explicit Non-Goals

- No Kubernetes, Kafka, Spark, Ray, ClickHouse, Redis, distributed filesystem, service mesh, or microservice split is introduced by this decision.
- No live trading behavior changes.
- No Risk of Ruin override is introduced.
