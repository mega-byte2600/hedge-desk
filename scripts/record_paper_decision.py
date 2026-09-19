#!/usr/bin/env python3
"""Record one GP paper decision into the append-only journal (closes the Learn loop).

The desk's actionable metric is "the user acted on a premium candidate." This is
the two-second surface for that action: after the GP reviews the AM report and
picks a cash-secured-put (or covered-call / credit-spread) candidate, they record
it here as an ENTERED_PAPER entry. The nightly AM report's paper panel then shows
the decision and later its observed outcome.

Honesty: this records a PAPER decision by the user only. It never places an order
and never fabricates an outcome; trade_authorized stays False. Absent real fills,
a "decision" is an ENTERED_PAPER intent, later updated by the user with the actual
market outcome once it settles.

Usage:
  python3 scripts/record_paper_decision.py --symbol NKE --strike 32 --dte 34
  python3 scripts/record_paper_decision.py --symbol AAL --strike 11.5 \
      --outcome EXPIRED_WORTHLESS --premium-received 0.16
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(__file__.rsplit("/", 2)[0]))  # repo root so hedge_desk imports

from hedge_desk.paper_log import ALLOWED_OUTCOMES, append_outcome

DEFAULT_LOG = "artifacts/paper-outcomes.jsonl"


def build_candidate_id(symbol: str, strike: str, dte: int | None) -> str:
    """Stable, readable candidate id from the premium-desk candidate fields."""
    limb = str(strike)
    if dte is not None:
        limb = f"{limb}|dte={dte}"
    return f"{str(symbol).upper()}|{limb}"


def main(argv=None) -> int:
    choices = sorted(ALLOWED_OUTCOMES)
    p = argparse.ArgumentParser(
        description="Append one observed paper decision/outcome to the journal."
    )
    p.add_argument("--symbol", required=True, help="Underlying symbol, e.g. NKE")
    p.add_argument("--strike", required=True, help="Short strike, e.g. 32")
    p.add_argument("--dte", type=int, default=None, help="Days to expiration (optional)")
    p.add_argument(
        "--strategy",
        default="CASH_SECURED_PUT",
        choices=("CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD"),
    )
    p.add_argument("--outcome", default="ENTERED_PAPER", choices=choices,
                   help="Paper decision/outcome to record (default: ENTERED_PAPER)")
    p.add_argument("--premium-received", default=None,
                   help="Observed premium received per contract if known")
    p.add_argument("--candidate-id", default=None,
                   help="Override the generated candidate id")
    p.add_argument("--log", default=DEFAULT_LOG,
                   help=f"Journal path (default: {DEFAULT_LOG})")
    args = p.parse_args(argv)

    cid = args.candidate_id or build_candidate_id(args.symbol, args.strike, args.dte)
    entry = append_outcome(
        args.log,
        candidate_id=cid,
        symbol=args.symbol,
        strategy=args.strategy,
        outcome=args.outcome,
        premium_received=args.premium_received,
        entered_at=datetime.now(timezone.utc),
    )
    print(json.dumps(
        {
            "candidate_id": entry["candidate_id"],
            "seq": entry["seq"],
            "outcome": entry["outcome"],
            "entry_sha256": entry["entry_sha256"],
            "trade_authorized": entry["trade_authorized"],
            "log": args.log,
        },
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())