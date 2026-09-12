-- Emporion desk: membership schema for Supabase (Postgres).
-- Apply once in the Supabase SQL editor (or via migration).
-- Set SUPABASE_URL + SUPABASE_SERVICE_KEY on the Render service so the
-- membership store persists through redeploys.

create table if not exists members (
    email             text primary key,
    role              text not null,            -- GP | LP | MEMBER | GUEST
    created_at        text not null,
    guest_expires_at  timestamptz,
    subscribed        boolean not null default false,
    investor          boolean not null default false,
    fee_type          text,
    fee_rate          text,
    invite_token      text,
    invite_expires_at timestamptz
);

create table if not exists otps (
    id          bigserial primary key,
    email       text not null,
    code_hash   text not null,
    purpose     text not null,                  -- signin | invite
    expires_at  timestamptz not null,
    used        boolean not null default false,
    created_at  timestamptz not null
);
create index if not exists idx_otps_email on otps (email);

create table if not exists sessions (
    token_hash  text primary key,
    email       text not null,
    created_at  timestamptz not null,
    expires_at  timestamptz not null
);
create index if not exists idx_sessions_email on sessions (email);

create table if not exists broker_links (
    email         text primary key,
    broker        text not null,
    account_label text,
    token_enc     text,                          -- encrypted token reference, never raw
    created_at    timestamptz not null,
    updated_at    timestamptz not null
);

-- Append-only, hash-chained membership audit trail. One row per membership
-- event; each row carries the previous row's hash and its own, so an edit or a
-- deletion breaks the chain. hedge_desk/membership_audit.py claims this as a
-- compliance artifact, and SupabaseMembershipAuditLog already writes to it — but
-- the table was missing from this file, so every append got a 404 that the caller
-- swallowed and the trail recorded nothing in production.
--
-- created_at is text, not timestamptz, on purpose: entry_hash() is computed over
-- the timestamp *string*, so storing a normalised timestamp would break
-- verification of every existing entry.
create table if not exists membership_events (
    seq         bigint primary key,
    event       text not null,
    email       text not null,
    actor       text,
    detail      text,
    created_at  text not null,
    prev_hash   text not null,
    entry_hash  text not null
);
create index if not exists idx_membership_events_email on membership_events (email);
create index if not exists idx_membership_events_created on membership_events (created_at);

-- Row-level security: the service key bypasses RLS; keep RLS on by default so
-- the anon/public key can never read member data or broker links.
alter table members enable row level security;
alter table otps enable row level security;
alter table sessions enable row level security;
alter table broker_links enable row level security;
alter table membership_events enable row level security;
