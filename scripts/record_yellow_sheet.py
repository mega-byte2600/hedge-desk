#!/usr/bin/env python3
"""Record one GP decision as a Yellow Sheet (the product's decision document).

A Yellow Sheet is the decision artifact — thesis (why enter), evidence, what would
prove the thesis wrong (invalidation), a planned exit, and the risk state
auto-filled from the REAL evaluated candidate in the current AM report. This is
distinct from the paper-outcome journal, which captures the observed OUTCOME after
the position settles.

Honesty: the risk_state is pulled from the real report candidate (never typed by an
agent); the thesis/evidence/invalidation/the plan are the GP's own research text;
trade_authorized stays False. Stored in a gitignored local vault.

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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hedge_desk.yellow_sheet import ALLOWED_DECISIONS, record_yellow_sheet

DEFAULT_VAULT = "artifacts/yellow-sheets.jsonl"
DEFAULT_REPORT = "artifacts/am-report-latest.json"


def _candidate_risk_state(report_path: str, symbol: str) -> dict:
    """Pull the REAL evaluated candidate's risk state from the AM report."""
    try:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return {"risk_input_absent": True, "reason": "report_unreadable"}
    csp = report.get("cash_secured_put_scan", {})
    r = csp.get(symbol.upper())
    if not isinstance(r, dict) or r.get("mode") != "CASH_SECURED_PUT":
        return {"risk_input_absent": True, "reason": "no_candidate_in_report"}
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
    p.add_argument("--strike", required=True, help="Short strike, e.g. 32")
    p.add_argument("--strategy", default="CASH_SECURED_PUT",
                   choices=("CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD"))
    p.add_argument("--dte", type=int, default=None)
    p.add_argument("--thesis", required=True, help="Why enter / investment thesis")
    p.add_argument("--evidence", default="", help="Evidence / catalyst")
    p.add_argument("--invalidation", required=True, help="What would prove me wrong")
    p.add_argument("--planned-exit", default="", help="Planned exit / roll rule")
    p.add_argument("--decision", default="PAPER_OPEN", choices=sorted(ALLOWED_DECISIONS))
    p.add_argument("--report", default=DEFAULT_REPORT, help="AM report for risk state")
    p.add_argument("--vault", default=DEFAULT_VAULT, help="Yellow Sheet vault path")
    args = p.parse_args(argv)

    risk = _candidate_risk_state(args.report, args.symbol)
    entry = record_yellow_sheet(
        args.vault, symbol=args.symbol, strategy=args.strategy,
        thesis=args.thesis, evidence=args.evidence, invalidation=args.invalidation,
        planned_exit=getattr(args, "planned_exit"), decision=args.decision,
        strike=args.strike, dte=args.dte, risk_state=risk,
        bound_report_sha256=json.loads(Path(args.report).read_text())["report_sha256"]
        if Path(args.report).is_file() else None,
    )
    print(json.dumps({
        "seq": entry["seq"], "symbol": entry["symbol"], "decision": entry["decision"],
        "entry_sha256": entry["entry_sha256"], "trade_authorized": entry["trade_authorized"],
        "vault": args.vault, "risk_state_source": risk.get("source", "absent"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())