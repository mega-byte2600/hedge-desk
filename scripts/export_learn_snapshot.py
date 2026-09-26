#!/usr/bin/env python3
"""Export a compact, timestamped Learn-tab snapshot for the iOS app.

Reads the real nightly report (artifacts/am-report-latest.json) and writes
ios/TradeDesk/TradeDesk/LearnSnapshot.json — every figure carries its as-of
date and source. Nothing is invented: blocked sources stay blocked, and the
screen shows pass/screened-out exactly as the pipeline evaluated.

Usage:
    python3 scripts/export_learn_snapshot.py [--report PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = REPO / "artifacts" / "am-report-latest.json"
DEFAULT_OUT = REPO / "ios" / "TradeDesk" / "TradeDesk" / "LearnSnapshot.json"

SCHEMA = "hedge-desk-learn-snapshot-1.0.0"
MAX_CONTRACTS = 8


def _fnum(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=str(DEFAULT_REPORT))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    report = json.loads(Path(args.report).read_text())
    freshness = report.get("data_freshness", {}) or {}
    as_of = freshness.get("as_of") or "unknown"

    vix = report.get("vix_regime", {}) or {}
    vix_hist = vix.get("history", []) or []
    vix_last = vix_hist[-1] if vix_hist else [as_of, None]

    oil = report.get("oil_market", {}) or {}
    spy = (report.get("chain_income", {}) or {}).get("SPY", {}) or {}
    rates = report.get("rates_environment", {}) or {}

    screen = []
    csp = report.get("cash_secured_put_scan", {}) or {}
    for symbol in sorted(csp):
        entry = csp[symbol] or {}
        cand = entry.get("candidate", {}) or {}
        if not cand.get("found"):
            continue
        roc = _fnum(cand.get("return_on_capital"))
        reasons = entry.get("eval_reasons", []) or []
        screen.append({
            "symbol": symbol,
            # Pipeline field is return_on_capital; for a cash-secured put the
            # capital at risk IS the collateral, so the app labels it
            # "return on collateral".
            "return_on_collateral": roc,
            "strike": str(cand.get("strike")) if cand.get("strike") is not None else None,
            "expiration": cand.get("expiration"),
            "dte": cand.get("dte"),
            "credit_per_share": str(cand.get("net_credit_per_share")) if cand.get("net_credit_per_share") is not None else None,
            "collateral": str(cand.get("collateral_required")) if cand.get("collateral_required") is not None else None,
            "fits_rules": bool(entry.get("fits_gp_rules")),
            "screen_out_reason": reasons[0] if reasons else None,
            "source": entry.get("data_source") or "nightly pipeline",
        })
    screen.sort(key=lambda c: (c["return_on_collateral"] is None, -(c["return_on_collateral"] or 0)))
    screen = screen[:MAX_CONTRACTS]

    eod_raw = report.get("eod_batch_status")
    eod_status = eod_raw.get("status") if isinstance(eod_raw, dict) else eod_raw

    snapshot = {
        "schema_version": SCHEMA,
        "generated_at": report.get("generated_at"),
        "as_of": as_of,
        "is_current": bool(freshness.get("is_current", False)),
        "vix": {
            "level": _fnum(vix_last[1]),
            "as_of": vix_last[0],
            "source": "Yahoo Finance (^VIX), daily close",
            "mode": vix.get("mode") or "UNKNOWN",
        },
        "wti": {
            "level": _fnum(oil.get("last_close")),
            "as_of": oil.get("as_of") or as_of,
            "source": "Yahoo Finance (CL=F), daily close",
            "mode": oil.get("mode") or "UNKNOWN",
        },
        "spy_chain": {
            "mode": spy.get("mode") or "UNKNOWN",
            "structures": len(spy.get("gated_income_structures", []) or []),
            "as_of": as_of,
            "source": "Cboe delayed quotes (~15 min)",
        },
        "rates": {
            "mode": rates.get("mode") or "UNKNOWN",
            "note": "Treasury data was unavailable in the latest run — shown as blocked, not estimated.",
        },
        "csp_screen": screen,
        "candidate_count": report.get("candidate_count"),
        "eod_status": eod_status or "UNKNOWN",
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(f"wrote {out} ({len(screen)} screened contracts, as_of={as_of})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
