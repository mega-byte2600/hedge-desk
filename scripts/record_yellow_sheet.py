#!/usr/bin/env python3
"""Record one GP decision as a Yellow Sheet (the product's decision document).

A Yellow Sheet is the decision artifact — thesis (why enter), evidence, what would
prove the thesis wrong (invalidation), a planned exit, and the risk state
auto-filled from the REAL evaluated candidate in the current AM report. This is
distinct from the paper-outcome journal, which captures the observed OUTCOME after
the position settles.

Honesty: the risk_state is pulled from the real report candidate (never typed by an
agent); the thesis/evidence/invalidation/the plan are the GP's own research text;
trade_authorized stays False. Stored in a gitignored local vault. Inputs are
validated semantically BEFORE any vault modification (ENGINEER peer-review).

Usage:
  python3 scripts/record_yellow_sheet.py --symbol NKE --strike 32 \
    --thesis "Sell 10% OTM cash-secured put; bank the premium." \
    --invalidation "Underlying gaps below 32 within the DTE." \
    --planned-exit "Let expire worthless at 34 DTE." \
    --decision PAPER_OPEN
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hedge_desk.yellow_sheet import ALLOWED_DECISIONS, record_yellow_sheet

DEFAULT_VAULT = "artifacts/yellow-sheets.jsonl"
DEFAULT_REPORT = "artifacts/am-report-latest.json"


def _positive_strike(value: str) -> str:
    try:
        d = Decimal(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"strike must be a number, got {value!r}")
    if not d.is_finite() or d <= 0:
        raise argparse.ArgumentTypeError(f"strike must be finite and > 0, got {value!r}")
    return value


def _dte(value: str) -> int:
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"dte must be an integer, got {value!r}")
    if not 1 <= v <= 365:
        raise argparse.ArgumentTypeError(f"dte must be 1..365, got {value!r}")
    return v


def _load_report(report_path: str) -> dict:
    path = Path(report_path)
    if not path.is_file():
        raise SystemExit(f"fatal: report not found: {path} (run the nightly batch first)")
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise SystemExit(f"fatal: report unreadable or invalid JSON: {path}")
    if not isinstance(report, dict) or "cash_secured_put_scan" not in report:
        raise SystemExit("fatal: report missing cash_secured_put_scan (not an AM report)")
    return report


def _candidate_risk_state(report: dict, symbol: str) -> dict:
    """Pull the REAL evaluated candidate's risk state from the AM report.

    Fail-closed (ENGINEER): if the symbol has no evaluated candidate in the report,
    refuse to write rather than invent a risk state.
    """
    csp = report.get("cash_secured_put_scan", {})
    r = csp.get(symbol.upper())
    if not isinstance(r, dict) or r.get("mode") != "CASH_SECURED_PUT":
        raise SystemExit(
            f"fatal: no cash-secured-put candidate for {symbol.upper()} in the report; "
            "refusing to write a Yellow Sheet without a real risk state"
        )
    candidate = r.get("candidate", {})
    return {
        "strategy": "CASH_SECURED_PUT",
        "strike": candidate.get("strike"),
        "dte": candidate.get("dte"),
        "net_credit_per_share": candidate.get("net_credit_per_share"),
        "collateral_required": candidate.get("collateral_required"),
        "return_on_capital": candidate.get("return_on_capital"),
        "max_loss": candidate.get("max_loss"),
        "survivability": r.get("survivability"),
        "fits_gp_rules": r.get("fits_gp_rules"),
        "eval_reasons": r.get("eval_reasons"),
        "source": r.get("data_source"),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Record one GP decision as a Yellow Sheet."
    )
    p.add_argument("--symbol", required=True, help="Underlying symbol, e.g. NKE")
    p.add_argument("--strike", required=True, type=_positive_strike, help="Short strike, e.g. 32")
    p.add_argument("--strategy", default="CASH_SECURED_PUT",
                   choices=("CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD"))
    p.add_argument("--dte", type=_dte, default=None, help="Days to expiration (1..365)")
    p.add_argument("--thesis", required=True, help="Why enter / investment thesis")
    p.add_argument("--evidence", default="", help="Evidence / catalyst")
    p.add_argument("--invalidation", required=True, help="What would prove me wrong")
    p.add_argument("--planned-exit", default="", help="Planned exit / roll rule")
    p.add_argument("--decision", default="PAPER_OPEN", choices=sorted(ALLOWED_DECISIONS))
    p.add_argument("--report", default=DEFAULT_REPORT, help="AM report for risk state")
    p.add_argument("--vault", default=DEFAULT_VAULT, help="Yellow Sheet vault path")
    args = p.parse_args(argv)

    # All validation happens BEFORE any vault write (ENGINEER peer-review).
    report = _load_report(args.report)
    risk = _candidate_risk_state(report, args.symbol)
    bound = report.get("report_sha256")
    if not bound or not isinstance(bound, str) or len(bound) != 64:
        raise SystemExit("fatal: report has no valid report_sha256; refusing to write")

    entry = record_yellow_sheet(
        args.vault, symbol=args.symbol, strategy=args.strategy,
        thesis=args.thesis, evidence=args.evidence, invalidation=args.invalidation,
        planned_exit=getattr(args, "planned_exit"), decision=args.decision,
        strike=args.strike, dte=args.dte, risk_state=risk, bound_report_sha256=bound,
    )
    print(json.dumps({
        "seq": entry["seq"], "symbol": entry["symbol"], "decision": entry["decision"],
        "entry_sha256": entry["entry_sha256"], "trade_authorized": entry["trade_authorized"],
        "vault": args.vault, "risk_state_source": risk.get("source", "absent"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())