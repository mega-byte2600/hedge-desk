# Emporion True-MVP Demo — Overnight Premium Desk AM Report (real data)

This is the demo of the actual product: the **Overnight Premium Desk** hands the GP a
risk-vetted cash-secured-put candidate list before the open. The equities EOD screen is
the universe feeder; the premiums are the money-maker. Everything on the page is measured
from **real data** — no synthetic fixtures, no invented numbers.

## What it is

`AM Report` renders one run of the batch pipeline:

```
real EOD closes (Yahoo) ──▶ feature plane ──▶ premium candidates
real Cboe delayed option chains ──▶ cash-secured-put wheel scan (GP-fit)
real FRED rates ──▶ rates environment      real SEC EDGAR ──▶ earnings actuals
real VIX ──▶ premium-timing regime         real FRED ──▶ macro (CPI, unemployment, 5y/30y)
append-only paper journal ──▶ learning loop
```

Every candidate is `trade_authorized = False` and the page says so. This is research and
a decision aid, not an order and not investment advice.

## Run it (one command, ~20s)

```bash
cd ~/workspace/projects/hedge-desk
bash scripts/demo.sh
```

- Console shell:   http://127.0.0.1:8765/
- **AM report:**   http://127.0.0.1:8765/am-demo.html   ← the MVP demo
- Live report:     http://127.0.0.1:8765/api/am-report   (JSON, the report that feeds it)

`demo.sh` regenerates the report from the live pipeline before serving, so the page is
always fresh. Health check: `/api/health` returns `mode: "paper"`,
`live_orders_enabled: false`.

### Scheduled batch (4:30pm EST after close)

The pipeline is meant to run after the market close and work until the batch is done.
A launchd job fires it automatically at **4:30pm EST** (13:30 local — both US coasts
shift DST together, so 16:30 Eastern is always 13:30 local year-round):

```bash
launchctl list | grep emporion        # com.emporion.nightly should be present
bash scripts/run_nightly_batch.sh     # run it manually right now
```

Each run writes a timestamped log to `artifacts/logs/nightly-<ts>.log` (last 30 kept)
and regenerates `am-report-latest.json` + `am-demo.html`, which the server serves live.
The report's `data_freshness` field states whether it is running on today's close or the
prior trading day's (at 4:30pm the source may not have published today's bar yet).

### Public URL (this Mac, while the server runs)

https://astra-mini.tail16a2cd.ts.net:8443/am-demo.html

That is a Tailscale Funnel to the local server on port 8765 — a **tunnel, not hosting**:
it stays up while the Mac is on and the process runs, and it is not a deploy. The durable
answer is Render/deploy; this is the "open it from your phone right now" path.

## What to show, section by section

1. **Equity premium candidates** — collateral/margin from real EOD closes.
2. **Premium income spreads** — net credit and max loss from a real Cboe delayed chain,
   each with its execution-gate decision (kill switch OFF by default → BLOCKED).
3. **Feature plane** — deterministic 1/5/21-day returns, realized vol, range position
   from 3 months of real EOD.
4. **Cash-secured-put wheel scan (the product)** — a real Cboe chain per underlying, with
   the GP's rules applied. Today's run surfaces **7 FITS** candidates, each under $5k
   capital, 34 DTE, return-on-capital 0.55%–1.39%:

   | Symbol | Strike | Capital | RoC |
   |---|---|---|---|
   | NKE | 32 | $3,200 | 1.28% |
   | AAL  | 11.50 | $1,150 | 1.39% |
   | LYFT | 13.50  | $1,350 | 1.26% |
   | CCL | 20 | $2,000 | 1.15% |
   | NCLH | 13 | $1,300 | 1.23% |
   | F | 12 | $1,200 | 0.83% |
   | DVN | 44 | $4,400 | 0.55% |

   Return on capital = net credit / strike. (This was the bug: the scanner divided credit
   by strike×100, reporting ~0.013% and flagging every candidate — fixed, verified.)
5. **Paper-outcome loop** — the append-only journal; empty until the GP records a decision.
6. **Rates environment** — real FRED observations.
7. **Earnings actuals** — real SEC EDGAR filings.

## The GP-fit rules encoded (your stated sizing)

- **Return on capital deployed ~0.5–2%** per trade — net credit / collateral (the x100
  cancels), NOT return on max-loss dollars (the assignment-trap figure).
- **Cash-secured put ~10% OTM, 30–45 DTE**, conservative wheel.
- **Capital required < ~$5k** per position. That is why the universe is sub-$55 liquid
  names (NKE, CCL, AAL, LYFT, NCLH, F, DVN): a 10% OTM CSP needs ~$0.9×price×100, so
  underlyings under ~$55 fit the small desk. Megacaps need $20k–$68k and were the reason
  the original demo had zero actionable candidates.

## Record a decision (closes the Learn loop)

The desk's actionable metric is "the GP acts on a premium candidate." Recording one is a
two-second command that appends to the paper journal (surfaced in panel 5):

```bash
python3 scripts/record_paper_decision.py --symbol NKE --strike 32 --dte 34
# later, the observed outcome:
python3 scripts/record_paper_decision.py --symbol NKE --strike 32 --dte 34 \
    --outcome EXPIRED_WORTHLESS --premium-received 0.41
```

Append-only, content-hashed, `trade_authorized=False` (paper intent, never an order).

## V&V status

See `docs/validation/AM_DEMO_VV.md` for the full record. Summary:

- **Verified** (measured by commands): full unit suite green (719 tests), CSP scan
  returns corrected RoC on the GP band, demo page renders 7 FITS from the live pipeline,
  funnel serves the byte-identical page, paper-log rejects invalid outcomes.
- **Validated** (matches your stated expectations): the demo is the Overnight Premium Desk
  AM candidate list ranked for your sizing (cash-secured seller first, <$5k, ~1–2%
  return-on-collateral), real data, honest limits stated.

## Honest limits (say them plainly)

- **Schwab is NOT wired for execution.** Broker access is read-only; no order code path
  exists. Building risk-gated auto-execution is the next gated release, behind the
  deterministic risk engine + kill switch.
- **Paper only, by design.** No live orders, no P&L, no real capital.
- **No probability or Risk of Ruin** is computed. Survivability is INDETERMINATE until a
  real account balance is wired; the gate fails closed rather than fabricate.
- Market data is **delayed** public reference data (Yahoo EOD, Cboe delayed chains) —
  not a licensed execution feed, not redistributed.
- The public URL is a **tunnel** (dies with the process), not hosting.