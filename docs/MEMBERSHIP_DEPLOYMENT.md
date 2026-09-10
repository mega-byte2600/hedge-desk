# Membership deployment (Render + Supabase)

The membership layer runs on the existing Render service. For real members to
survive redeploys, persistence must point at Supabase (Render free disk is
ephemeral).

## 1. Create the Supabase tables

In your Supabase project: SQL editor → run `supabase/schema.sql`.
It creates `members`, `otps`, `sessions`, `broker_links` and enables RLS.

## 2. Set environment variables on the Render service

| Variable | Purpose | Required |
|---|---|---|
| `SUPABASE_URL` | Project URL, e.g. `https://xxxx.supabase.co` | yes (for persistence) |
| `SUPABASE_SERVICE_KEY` | Service role key (server-side only — never ship to the browser) | yes (for persistence) |
| `MEMBERSHIP_SECRET` | HMAC secret for OTP/session hashing. Set a long random value. | yes |
| `GP_EMAIL` | The GP's email — the only account allowed to issue LP invites / view the cap. | yes |
| `BROKER_LINK_KEY` | Key used to encrypt broker token references at rest. | only when broker linking is enabled |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` / `SMTP_FROM_NAME` | OTP email delivery. Without these, codes print to the server log (dev fallback). | for real sign-in emails |
| `GUEST_ACCESS_DAYS` | Guest test-drive length in days (default 31). | optional |

Behaviour: if `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` are set the server uses
the Supabase store; otherwise it falls back to local SQLite (dev only — data
resets on redeploy).

## 3. What the tiers get

| Role | Data | Broker | Cost |
|---|---|---|---|
| GUEST | synthetic only (test drive, 31 days) | no | free |
| MEMBER | real market data | read-only link (then execution, gated) | paid subscription |
| LP | real market data + full desk service | yes | investor in the LLC — never pays |
| GP | everything | everything | operator |

## 4. Safety notes

- The `SUPABASE_SERVICE_KEY` is server-side only. Never expose it to the
  browser or commit it. RLS is on for all tables.
- `MEMBERSHIP_SECRET` and `BROKER_LINK_KEY` must be long random values and must
  not be rotated casually (rotating invalidates existing sessions / broker links).
- Real-money execution is **not** enabled. Broker access is read-only; order
  placement is absent and gated behind the deterministic risk engine plus
  legal/fund-structure review.
- LPs are investors in the LLC, not payers. Fee schedules are set by the GP in
  the operating agreement. Obtain securities counsel before any live LP capital.
