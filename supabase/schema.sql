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

-- Row-level security: the service key bypasses RLS; keep RLS on by default so
-- the anon/public key can never read member data or broker links.
alter table members enable row level security;
alter table otps enable row level security;
alter table sessions enable row level security;
alter table broker_links enable row level security;
