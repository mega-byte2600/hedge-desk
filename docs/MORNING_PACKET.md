# Emporion — Overnight Build Review (GP morning packet, 2026-09-20)

Open the demo: https://astra-mini.tail16a2cd.ts.net:8443/am-demo.html
(local: bash scripts/demo.sh → http://127.0.0.1:8765/am-demo.html)

## What you're looking at (the Overnight Premium Desk AM report)

- 7 cash-secured-put candidates that fit your wheel (ranked best-first by
  return-on-capital, credit-offset): AAL 1.41%, NKE 1.30%, 1.25%, 1.16%, 0.84%,
  0.82%, DVN 0.55% — all <$5k capital, 34 DTE, real Cboe delayed chains.
- Survivability per candidate (PASS/FAIL/INDETERMINATE) — INDETERMINATE until you
  set real account equity.
- **Compounding scale** (the "get big" design, holding the 2%-of-equity rule):
  top fit AAL $1,150/contract → 1 contract @$100k, 4 @$250k, 8 @$500k, 17 @$1M.
- **Decision ledger — Yellow Sheets** (your correction, built properly): record a
  decision as a Yellow Sheet (thesis/evidence/invalidation/exit + auto-filled
  risk), distinct from the paper outcome log.
- Real VIX regime, FRED macro (CPI/unemployment/curve), rates, earnings.

## 30 commits this session, 753/753 tests green (7s, offline/deterministic)

Highlights:
- return_on_capital basis fixed (was 100x too small) + sub-$55 GP-fit universe
- real data wired: VIX, FRED macro (CPI/unemployment/5y/30y) — all free/no-auth
- 4:30pm EST scheduled batch (launchd), concurrent fetches, bounded FRED timeout,
  data-freshness gate (knows today's close vs prior day)
- account-equity input → survivability + wheel_fit + scale_position (compounding)
- Yellow Sheet decision artifact + CLI + ledger
- peer review (6 SOUL profiles, 6 model families) caught 5 real defects — all fixed
- overnight peer review (4 specialists) caught and fixed two more:
  - QUANT/RISK: csp_scan collateral was gross strike×100 while evaluate_premium
    offsets credit — same put showed 1.281% vs 1.298%. Now consistent (credit-offset).
  - ENGINEER: the record CLI wrote before validating input. Now validates strike/DTE/
    report/symbol-match before any vault write.

## What needs YOU (the only thing I won't fake)

The Measure side of the loop is empty: 0 decisions recorded. To close it:
  python3 scripts/record_yellow_sheet.py --symbol NKE --strike 32 \
    --thesis "Sell 10% OTM cash-secured put; bank the premium." \
    --invalidation "Underlying gaps below 32 within the DTE." \
    --planned-exit "Expire worthless at 34 DTE."
And set real account equity so survivability evaluates:
  export ACCOUNT_EQUITY=25000   (or put it in data/account_equity.txt, gitignored)

## Honest limits (unchanged)

- Schwab execution NOT wired (read-only); the gated release is behind the risk
  engine + kill switch.
- Paper-only, no probability/RoR (survivability INDETERMINATE without real equity).
- Forward-earnings calendar still externally gated (429/404) — not fabricated.
- Delayed public reference data (Yahoo/Cboe/FRED/SEC), not a live feed.

## Review path

1. The attached dashboard: docs/status/BML_PROGRESS_2026-09-19.md (full commit table).
2. V&V record: docs/validation/AM_DEMO_VV.md (every claim tied to a command).
3. README: docs/MVP_DEMO_README.md.