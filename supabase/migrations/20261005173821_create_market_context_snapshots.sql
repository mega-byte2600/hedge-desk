create table if not exists public.market_context_snapshots (
    snapshot_key text primary key check (snapshot_key = 'latest'),
    schema_version text not null,
    generated_at timestamptz not null,
    status text not null check (status in ('LIVE', 'DEGRADED', 'BLOCKED')),
    live_sources integer not null default 0 check (live_sources >= 0),
    blocked_sources integer not null default 0 check (blocked_sources >= 0),
    unconfigured_sources integer not null default 0 check (unconfigured_sources >= 0),
    payload jsonb not null check (jsonb_typeof(payload) = 'object'),
    updated_at timestamptz not null default now()
);

alter table public.market_context_snapshots enable row level security;
revoke all on table public.market_context_snapshots from public, anon, authenticated;
grant select, insert, update on table public.market_context_snapshots to service_role;
