# Connect Emporion to Schwab (step-by-step runbook)

Goal: prove the real Schwab API link works end-to-end, then stage it toward a
gated test contract. Lean: each step has a measurable outcome; nothing here can
transmit your secret to git, logs, or the chat.

Current branch status (2026-10-03):
- `hedge_desk/brokers/schwab_oauth.py` — documented App authorization-code
  flow; the URL does not guess an OAuth scope.
- `hedge_desk/brokers/schwab_readonly.py` — account discovery and read-only
  balances/positions using Schwab encrypted account hashes.
- `hedge_desk/brokers/schwab_market_data.py` — production REST quotes, option
  chains, expiration chains, market hours, and price history.
- `hedge_desk/brokers/schwab_tokens.py` and `broker_link.py` — encrypted token
  metadata and seven-day refresh-token lifecycle.
- The server exposes authenticated, read-only market-data routes. Account
  hashes remain private; the browser selects an account using an opaque handle.
- `hedge_desk/connect_local.py` — optional local read-only diagnostic runner.
- Automated repository test status is recorded below; the test suite does not
  use a real Schwab account.

Safety rails (do not skip):
- Production credentials live only in Render's server-side environment. Never
  put them in git, browser/frontend settings, logs, or chat.
- Every deployed step below is READ-ONLY. The separate live-release gate is
  still blocked, so this branch does not place, cancel, or replace a live order.

---------------------------------------------------------------
PHASE 1 — PORTAL APP (you, in the browser; ~10 min)
---------------------------------------------------------------
[ ] 1. In developer.schwab.com > My Apps, open the approved production App.
[ ] 2. Confirm both the approved Trader API product and Market Data Production
      access are assigned to that App/client ID.
[ ] 3. Set the callback to exactly the deployed Hedge Desk URL:
      https://hedge-desk.onrender.com (no trailing slash). This exact value must
      also be `SCHWAB_REDIRECT_URI` in Render.
[ ] 4. Locate the App Key and App Secret in the portal. Do not paste either into
      chat, source control, browser code, or logs.
LEARN: the production App has both required product entitlements and its
       callback exactly matches the Render setting.

---------------------------------------------------------------
PHASE 2 — PERSISTENCE + SERVER CONFIG (you, Render/Supabase; ~10 min)
---------------------------------------------------------------
[ ] 5. In Supabase SQL Editor, run `supabase/schema.sql` once if it has not
      already been applied. It creates `broker_links` with RLS enabled.
[ ] 6. In Render > Hedge Desk service > Environment, add/update these server-only
      variables: `SCHWAB_CLIENT_ID`, `SCHWAB_CLIENT_SECRET`,
      `SCHWAB_REDIRECT_URI=https://hedge-desk.onrender.com`, and
      `BROKER_LINK_KEY` (random, at least 32 bytes).
[ ] 7. Ensure `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` are already configured
      on that same service. They must remain server-side. The service key lets
      Hedge Desk persist encrypted OAuth state in Supabase; it does not belong
      in frontend settings.
[ ] 8. Save the Render environment changes and redeploy the reviewed build.
MEASURE: service health is up and broker status no longer reports
         `broker_not_configured`. This release needs no new schema migration.

---------------------------------------------------------------
PHASE 3 — AUTHORIZE & VERIFY (you, Hedge Desk + browser; ~3 min)
---------------------------------------------------------------
[ ] 9. Sign in to Hedge Desk with an entitled MEMBER, LP, or GP account and
      open Account > Connect broker.
[ ] 10. Choose Schwab and complete its sign-in/consent screen. Schwab redirects
       to Hedge Desk; never copy the authorization code into chat.
[ ] 11. Select the intended account from the account selector. Account numbers
       and Schwab account hashes remain private to the server.
[ ] 12. Confirm balances and positions load, then use the read-only market-data
       endpoints listed in `docs/MEMBERSHIP_DEPLOYMENT.md` to verify quotes,
       options chains, expirations, market hours, and history.
MEASURE: broker status is linked, account selector shows an available account,
         and a quote/chain response succeeds for an authenticated user. This
         proves the read-only connection; it does not prove live trading.

---------------------------------------------------------------
PHASE 4 — TRADING STATUS (no operator action for this connection)
---------------------------------------------------------------
Trader API approval does not by itself connect live order placement. This branch
does not expose an order endpoint. Any future live-trading release needs its own
review and the existing risk, compliance, back-office, human approval, and
kill-switch evidence.

---------------------------------------------------------------
V&V / HONESTY LABELS
---------------------------------------------------------------
- VERIFIED on this branch: Focused automated connection tests pass; OAuth state is checked
  single-use; mocked token/account/market-data flows pass. No real account was
  used by tests.
- VALIDATED: account linking and market-data routes have deterministic mocked
  tests; live credentials are not used by tests.
- NOT YET: this branch has not been deployed or exercised with the approved App
  credentials. Live order placement remains unavailable in the app; Trader API
  approval alone does not authorize Hedge Desk to submit trades.
