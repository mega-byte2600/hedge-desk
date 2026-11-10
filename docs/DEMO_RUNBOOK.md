# Emporion demo runbook

The Hedge Desk console is public. No account, sign-in, membership, subscription,
investor seat, or broker link is required. The legacy auth, tier, and broker API
routes return `410 Gone`.

## Start and verify

```bash
python3 scripts/build_web.py
bash scripts/demo.sh
node scripts/smoke_console.mjs http://127.0.0.1:8765
node scripts/vv_console.mjs http://127.0.0.1:8765
```

Open `http://127.0.0.1:8765`. For the deployed console, use
<https://hedge-desk.onrender.com>.

## Five-minute walkthrough

1. Open the public console and review the overview and report timestamp.
2. Open Candidates, then inspect one research desk and its evidence.
3. Open Research desks and inspect each paper-only workflow.
4. Open Yellow Sheets and save a research note; confirm it remains in this browser.
5. Open Research resources and About. Explain that the desk is research and decision
   support only and does not authorize or place trades.
6. Open `/api/data-sources` to review current public-feed connectivity, including SEC
   EDGAR. `LIVE` means the bounded probe returned usable data; `BLOCKED` means the
   source did not return usable data on that check.

## Claims and boundaries

- The console uses live data where the feed status says `LIVE`; do not call a blocked
  or unconfigured source live.
- Research output is not investment advice, a recommendation, or an offer to sell a
  security.
- All candidates remain paper research. The service cannot place live orders.
- No performance history or future return is promised.
- The console does not estimate or substitute the authoritative Risk of Ruin value.

## If something breaks

- If the first page is slow, wait for the Render free service to wake, then reload once.
- If the console is blank, run `node scripts/smoke_console.mjs` and inspect the server
  log before changing code.
- If a feed is `BLOCKED`, inspect its public source response and configured server-side
  identity or credentials. Do not describe it as live until the probe passes.
