# Connect Emporion to Schwab (step-by-step runbook)

Goal: prove the real Schwab API link works end-to-end, then stage it toward a
gated test contract. Lean: each step has a measurable outcome; nothing here can
transmit your secret to git, logs, or the chat.

Status of what already exists (verified 2026-09-19):
- `hedge_desk/brokers/schwab_oauth.py` — OAuth auth-code flow, read-only scope.
- `hedge_desk/brokers/schwab_readonly.py` — read-only balances/positions.
- `hedge_desk/connect_local.py` — local runner: --auth then exchange+probe.
  CSRF state saved/verified/consumed (0600); secrets dir 0700; no secret in output.
- `hedge_desk/schwab_setup.py` — one-command prompt for keys (getpass), 0600 env.
- 697 unit tests green.

Safety rails (do not skip):
- Secrets live ONLY in `~/.schwab/env.env` (0600). Never in git, chat, logs.
- Every step below is READ-ONLY until explicitly flagged. Placement is a separate,
  release-gated step and is NOT enabled here.

---------------------------------------------------------------
PHASE 1 — PORTAL APP (you, in the browser; ~10 min)
---------------------------------------------------------------
[ ] 1. developer.schwab.com > My Apps > Create App.
[ ] 2. Name it anything; request OAuth scopes. Minimal is read-only; if your app
      is "Trader API - Individual" that is fine.
[ ] 3. Locate the App Key (your SCHWAB_CLIENT_ID) and App Secret (SCHWAB_CLIENT_SECRET).
      The secret is visible only after the app is approved/generated. If it is
      still pending, finish approval now — this is the single go/no-go item.
[ ] 4. Set Callbacks / redirect_uri to exactly:  https://127.0.0.1
      (Schwab rejects mismatches; must match SCHWAB_REDIRECT_URI exactly.)
LEARN: you have an approved app with a visible App Secret + a callback URL.
       If either is missing, stop here — nothing downstream works without it.

---------------------------------------------------------------
PHASE 2 — TURNKEY LOCAL SETUP (you, in the repo terminal; ~3 min)
---------------------------------------------------------------
[ ] 5. cd ~/workspace/projects/hedge-desk
[ ] 6. python3 -m hedge_desk.schwab_setup
        -> prompts: App Key, App Secret (hidden as you type), Redirect URI (https://127.0.0.1)
        -> writes ~/.schwab/env.env mode 0600; prints a Schwab login URL.
[ ] 7. Confirm the file landed and is private:
        ls -l ~/.schwab/env.env        # should show -rw-------
MEASURE: an authorize URL prints and the env file is 0600. If the file is
         missing or group-readable, restart using schwab_setup (it enforces perms).

---------------------------------------------------------------
PHASE 3 — AUTHORIZE & EXCHANGE (you, browser + terminal; ~3 min)
---------------------------------------------------------------
[ ] 8. Open the printed URL in your browser; log in to Schwab.
        You will be redirected to https://127.0.0.1 with a query string:
          ?code=XXXX...&state=YYYY...
[ ] 9. Copy BOTH code and state from the address bar.
[ ] 10. Exchange + probe (the token + read-only call happen on YOUR machine):
        python3 -m hedge_desk.connect_local --env ~/.schwab/env.env --code <code> --state <state>
        -> prints account_count and accounts, or an error like no_saved_state /
           state_mismatch / exchange_failed.
MEASURE: account_count >= 1 (read-only). That is the real data point that
         proves the broker link works. If state_mismatch, you pasted the wrong
         state (rerun --auth to generate a fresh one and retry).

---------------------------------------------------------------
PHASE 4 — STAGE TOWARD A TEST CONTRACT (build-only; NOT live)
---------------------------------------------------------------
[ ] 11. (Later, gated) An order adapter is the NEXT build slice. It is held behind
        the existing release gate (release.py: 9 evidence items; kill-switch DR;
        broker adapter certified). Do NOT place an order until that gate passes.
        This runbook does not enable placement.

LEARN: the decision to build the placement slice is based on the Phase 3
       account_count outcome — the measured connection works. If it does not,
       stop and diagnose (app approval? redirect mismatch? scope?).

---------------------------------------------------------------
V&V / HONESTY LABELS
---------------------------------------------------------------
- VERIFIED: 697 tests green; --auth saves 0600 state, exchange refuses without a
  saved state and consumes it (single-use); no secret in output (all measured).
- VALIDATED: matches the GP's goal — set up the infra to connect, prove it with a
  real read-only call, then decide the placement slice on that measured result.
- NOT YET: any order placement; that requires the release gate evidence.