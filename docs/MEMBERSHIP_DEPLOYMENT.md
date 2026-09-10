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
| `SUPABASE_ANON_KEY` | Publishable/anon key — safe to expose; enables social login in the browser | for social login |
| `SUPABASE_JWT_SECRET` | Project JWT secret (Settings → API → JWT Settings) — server verifies social-login tokens with it | for social login |
| `SOCIAL_PROVIDERS` | Comma list of enabled IdPs, e.g. `google,github,azure,apple` (default `google,github`) | optional |
| `SCHWAB_CLIENT_ID` / `SCHWAB_CLIENT_SECRET` | Schwab app credentials (server-side only) | for broker linking |
| `SCHWAB_REDIRECT_URI` | Must match the Schwab app callback exactly. Point it at the site root so the console finishes the link | for broker linking |
| `BROKER_LINK_KEY` | Long random value; encrypts broker token references at rest | for broker linking |
| `MEMBERSHIP_SECRET` | HMAC secret for OTP/session hashing. Set a long random value. | yes |
| `GP_EMAIL` | The GP's email — the only account allowed to issue LP invites / view the cap. | yes |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` / `SMTP_FROM_NAME` | OTP email delivery. Without these, codes print to the server log (dev fallback). | for real sign-in emails |
| `GUEST_ACCESS_DAYS` | Guest test-drive length in days (default 31). | optional |

Behaviour: if `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` are set the server uses
the Supabase store; otherwise it falls back to local SQLite (dev only — data
resets on redeploy).

## 2b. Enable social login (Supabase Auth)

1. Supabase dashboard → Authentication → Providers → enable Google / GitHub /
   Microsoft / Apple and paste each provider's OAuth client ID + secret.
2. Authentication → URL Configuration → add your site URL
   (`https://hedge-desk.onrender.com`) to the redirect allow-list so the OAuth
   callback returns to the desk.
3. Set `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`, and `SOCIAL_PROVIDERS` on the
   Render service.

Flow: the browser signs in with the provider via Supabase; the desk's server
**verifies the Supabase JWT** (`SUPABASE_JWT_SECRET`) before issuing its own
role-scoped session cookie. Identity comes from Supabase; role/tier stays with
the desk. If social login is not configured the buttons simply do not appear
and email-OTP still works.

## 3. What the tiers get

| Role | Data | Broker | Cost |
|---|---|---|---|
| GUEST | synthetic only (test drive, 31 days) | no | free |
| MEMBER | real market data | read-only link (then execution, gated) | paid subscription |
| LP | real market data + full desk service | yes | investor in the LLC — never pays |
| GP | everything | everything | operator |

## 3b. Using the desk

- **Sign in** (top-right) — social (Google/GitHub/…) when configured, else the
  email one-time code.
- **Broker connection** appears for members/LPs once `SCHWAB_*` is set. It is
  **read-only**: the desk can read positions and balances and cannot place
  orders.
- **GP console** appears only for `GP_EMAIL`. It shows LP seats used/cap, total
  members, role counts, and lets the GP issue an LP invite by email. The seat
  cap is enforced server-side, so the UI cannot exceed it.

## 3c. Keep the service warm (cold starts)

Render's free tier sleeps after ~15 minutes idle; the first request afterwards
can take 30–60s. Mitigations in place:

- `report.json` is now browser-cacheable, the client no longer uses
  `cache:'no-store'`, and the report is preloaded — so **repeat visits render
  from cache** without a round-trip.
- The console shows *"Waking the research desk…"* after 2.5s instead of
  appearing to hang.
- A local keep-alive pings every 8 minutes and warms `/`, `/api/health`, and
  `/report.json`.

The local pinger only runs while the machine hosting it is awake. For true
always-on, add an **external** uptime monitor (UptimeRobot or cron-job.org —
both free) pointing at `https://<service>.onrender.com/api/health` every 5
minutes. That removes cold starts regardless of your own machine.

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
