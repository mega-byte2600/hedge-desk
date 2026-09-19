# AM Report demo — Verification & Validation record

Status of the demoable true-MVP (Overnight Premium Desk AM report) at commit **d23e3c6**
(2026-09-19). Read with the standing V&V rule: **VERIFIED** = meets a spec, measured by a
command; **VALIDATED** = meets the user's stated expectations for function/use. The two
are never conflated.

## 1. Derived spec (the repo pins no hard numeric contract, so derive one)

The demo page and pipeline must, within a stated tolerance:

- **S1 — corrected return basis:** return-on-capital = `net_credit_per_share / strike`
  (the x100 on both sides cancels). Tolerable range per the GP's sizing rule:
  `0.005 ≤ RoC ≤ 0.02` (0.5%–2%).
- **S2 — small-desk capital:** collateral < $5,000 (`CAPITAL_OVER_5K` gate).
- **S3 — wheel timing:** 30–45 DTE.
- **S4 — paper boundary:** every candidate `trade_authorized == False`.
- **S5 — honest fail-closed:** missing artifact → JSON 404 (`artifact_missing`), never
  the SPA shell or a fabricated number; missing risk input → `INDETERMINATE`/`BLOCKED`,
  never an invented approval.
- **S6 — served demo equals the report:** the public/page-served AM report reflects the
  live nightly run (same candidates, same RoC), not a stale snapshot.

## 2. Verified — each claim is backed by a command actually run

| Spec | Evidence (command → result) | Status |
|---|---|---|
| S1 | `scan_cash_secured_put("NKE", ...)` real Cboe → `return_on_capital="0.0128"`; `tests/test_csp_scan.py` pins `0.0132` (credit 1.19 / strike 90) and rejects the old `credit/(strike×100)` | VERIFIED |
| S2 | real run: NKE $3,200; AAL $1,150; LYFT $1,350; CCL $2,000; NCLH $1,300; F $1,200; DVN $4,400 — all < $5k | VERIFIED |
| S3 | every fit candidate DTE = 34 (inside 30–45) | VERIFIED |
| S4 | full suite + generated report: all candidates/trades `trade_authorized=False` | VERIFIED |
| S5 | WSGI drive `/api/am-report` after removing file → `404 not_found` with `error:"artifact_missing"`; `/api/risk-dashboard` → `INDETERMINATE`, `trade_authorized_count:0` | VERIFIED |
| S6 | Tailscale funnel `https://…:8443/am-demo.html` fetched over the public IP returns a page byte-identical (`cmp exit 0`) to the on-disk regenerated page; 7 FITS badges present | VERIFIED |

Test/correctness gates:
- Full unit suite: **719/719 pass** (`python3 -m unittest discover -s tests`, 2026-09-19).
- Server suite 15/15, CSP-scanner suite 4/4, paper-log suite 6/6 (each run to green).
- Render of the demo page: 7 `FITS` rows, RoC `0.0128` present (no stale `0.0000`).

Regression guard added for the S1 fix: `test_sub5k_put_in_gp_band_fits_rules` plus the
tightened SPY-chain assertion; `test_am_demo_routes_serve_real_artifacts_and_fail_closed`
pins S5/S6 at the route level (temp-dir patched, CI-safe).

## 3. Validated — matches the user's stated expectations

- The product centerpiece is the **Overnight Premium Desk**; the equities EOD screen is
  its *feeder* — the demo leads with the cash-secured-put candidate list, exactly as the
  GP re-scoped it (2026-09).
- Ranking and sizing encode the GP's standing rules: **cash-secured put ≈10% OTM,
  30–45 DTE, capital < ~$5k, ~1–2% return on capital deployed**; return is shown on the
  collateral basis, not on max-loss dollars (the assignment trap the GP flagged).
- The wheel is **paper-only and honest**: no order path, no fabricated Risk of Ruin, no
  invented P&L — matching the GP's risk tolerance and claim discipline.
- Learned and acted on: the previous demo surfaced **zero** actionable candidates (megacap
  universe + a units bug in RoC). Both fixed, measured, and recorded — that is validated
  learning, not vanity output.

## 4. Honest limits (not V&V failures — stated boundaries)

- **Schwab execution is not wired.** Broker access is read-only; no order-placement code
  exists (`test` asserts no such path). Risk-gated auto-execution remains a separate,
  gated release behind the deterministic risk engine and kill switch.
- No validated Risk-of-Ruin artifact or real account equity is wired, so survivability is
  `INDETERMINATE`; the gate fails closed rather than substitute a number (AGENTS.md).
- Market data is delayed public reference data (Yahoo EOD, Cboe chains, FRED, SEC)
  licensed only for research; nothing is redistributed.
- The public URL is a tunnel to the local server (dies with the process), not hosting.

## 5. Re-run the verification (one command each)

```bash
python3 -m unittest discover -s tests                                  # 719/719
python3 scripts/record_paper_decision.py --symbol NKE --strike 32 --dte 34 --log /tmp/x.jsonl
bash scripts/demo.sh                                                  # serve; verify below
curl -s http://127.0.0.1:8765/am-demo.html | grep -c "badge ok'>FITS"  # expect 7
curl -s http://127.0.0.1:8765/api/am-report                            # live JSON, fits 7/7
```