# Schwab Trader API integration status

Updated 2026-10-03 on `feature/schwab-trader-v1`.

## What this branch wires

- The member account flow exchanges Schwab's authorization code, discovers
  account hashes, and stores OAuth and account metadata in the existing AES-GCM
  encrypted broker-link record.
- Members select a Schwab account through an opaque server-generated handle;
  neither account numbers nor account hashes are returned to the browser.
- Access tokens are refreshed before expiry. The refresh response is persisted
  before the protected API call; an expired seven-day refresh-token window
  requires a new Schwab consent flow.
- The read-only brokerage adapter reads balances and positions. The production
  Market Data adapter batches quotes and supports chains, expirations, market
  hours, and price history. Authenticated member endpoints expose these data.
- This release includes no order adapter or order endpoint.

## Schwab portal details verified

The authenticated Schwab Developer Portal's production specifications and
documentation confirm:

- Trader API base URL: `https://api.schwabapi.com/trader/v1`.
- Market Data base URL: `https://api.schwabapi.com/marketdata/v1`.
- OAuth is an authorization-code flow. The authorization URL uses the approved
  App's client ID and exact callback URI; no `scope` query parameter is
  documented. Token responses report `scope=api`.
- Token responses report `expires_in=1800` (30-minute access token). Schwab's
  documentation says refresh tokens are valid for seven days; if expired or
  invalidated, the member must repeat consent. The token manager uses a strict
  seven-day maximum age and persists any refreshed state before continuing.
- `GET /accounts/accountNumbers` returns the encrypted account ID used in
  account-specific paths. The docs do not establish that this hash is stable
  indefinitely, so the service rediscovers hashes at each new link.
- `POST /accounts/{accountNumber}/previewOrder` is documented. Successful
  order POSTs return HTTP 201 and a `Location` header identifying the order.
  Account-path `accountNumber` means Schwab's encrypted account ID, not the
  brokerage account number.
- Order entry documents equity and option assets, and the application's order
  request throttle is configured from 0 to 120 POST/PUT/DELETE requests per
  minute per account. The actual app setting is not visible in the API spec;
  this code never retries HTTP 429.
- The Trader API does not document a paper sandbox in the specifications
  reviewed. Testing is mock-only.

## Live execution boundary

The repository's `docs/SCHWAB_CONNECT_RUNBOOK.md`, `AGENTS.md`,
`docs/architecture/STATUS.md`, and `docs/architecture/ADR-0003-arbitrage-compliance-and-human-controls.md`
keep production order routing behind a separately reviewed live release. The
existing execution decision only authorizes paper actions, the release gate
currently reports live blocked, and CI asserts there is no live broker
submission endpoint. This work does not change those controls or introduce live order routing.

Before a separate release can enable trading, the repo still needs an approved
live authorization artifact flowing through Risk of Ruin, Compliance, Back
Office, human approval, and the kill switch. Broker-specific option approval
levels, outside-normal-hours behavior, and the live app's configured throttle
must also be confirmed. No adapter-side check can substitute for those gates.

## Deployment configuration

Server-side environment variables:

- `SCHWAB_CLIENT_ID`
- `SCHWAB_CLIENT_SECRET`
- `SCHWAB_REDIRECT_URI` (must exactly match the Schwab App callback)
- `BROKER_LINK_KEY` (random secret of at least 32 bytes)
- `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` (or `SUPABASE_SERVICE_ROLE_KEY`)
  when broker links must persist across Render restarts

Do not put credentials, OAuth tokens, account numbers, or account hashes in the
browser, repository, CI, logs, or chat. `SCHWAB_TRADING_ENABLED` is not a
production order-release switch; setting it alone does not enable a live order
path.

## Remaining operator steps

1. In the Schwab App, verify its callback is exactly the value deployed as
   `SCHWAB_REDIRECT_URI` and confirm the approved Trader API product is assigned
   to that App/client ID.
2. Add the server-side variables above in the deployment secret manager.
3. Deploy this branch only after its independent review and the repository's
   release process; then sign in as an entitled member, connect Schwab, and
   verify the account list and read-only quote/chain endpoints.
4. Keep live order placement disabled. A separate reviewed release is required
   before live order routing may be introduced.
