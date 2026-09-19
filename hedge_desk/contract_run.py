"""Income economics for a real option contract, from a validated option chain.

This is the Schwab plug-in point of the true-MVP re-scope: feed any real option
chain that conforms to the canonical ``hedge-desk-option-snapshot-1.0.0`` schema
(a JSON payload + envelope), and get back the executable income economics for
every admissible defined-risk premium structure — net credit, max loss, break
even, return on risk — computed by the already-tested deterministic scanner and
spread arithmetic.

Honesty boundary (matches the desk's discipline):
- Income here is EXECUTABLE-side net credit from real bid/ask quotes in the chain.
  No probability, no Risk of Ruin, no forecast. It is the arithmetic of "sell
  this premium, what do I collect, what is my worst case."
- It computes economics; it does NOT place an order and trade_authorized stays
  False. Only the deterministic risk engine (later) can authorize.
- Proven today against the repo's synthetic chain fixture; ready to accept a
  real chain the GP exports from Schwab once the adapter lands.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

from hedge_desk.data.intake import validate_local_observation
from hedge_desk.options import (
    OptionSnapshot,
    SpreadScanPolicy,
    evaluate_market_session,
    evaluate_option_universe,
    parse_market_session_evidence,
    parse_option_snapshot,
    scan_vertical_credit_spreads,
)

CONTRACT_RUN_VERSION = "hedge-desk-contract-run-1.0.0"


@dataclass(frozen=True)
class ContractIncome:
    contract_id: str
    underlying: str
    option_type: str
    short_strike: str
    long_strike: str
    net_credit_per_share: str
    net_credit: str
    maximum_loss: str
    break_even: str
    return_on_risk: str
    days_to_expiration: int
    admissible: bool
    reason_code: str


def run_contract(
    snapshot_path: Path,
    envelope_path: Path,
    decision_cutoff: datetime,
    maximum_age_seconds: int,
    session_path: Path | None = None,
    minimum_seconds_before_close: int = 0,
    quantity: int = 1,
    commission_per_contract: str = "0.65",
) -> Dict[str, object]:
    """Validate a local option chain and return income economics per spread.

    Mirrors the existing validated local intake (envelope + payload hashing, so a
    licensed payload never enters the repo) and then scans every admissible
    vertical credit spread. Returns the executable net-credit economics.
    """
    from decimal import Decimal

    if decision_cutoff.tzinfo is None:
        raise ValueError("contract-run cutoff must be timezone-aware")

    # Stage 1: provenance + point-in-time gate on the raw payload (never copied).
    intake = validate_local_observation(
        envelope_path, snapshot_path, decision_cutoff, maximum_age_seconds
    )
    if not intake.gate.admissible:
        raise ValueError(
            "contract-run snapshot blocked: "
            + ",".join(intake.gate.reason_codes)
        )
    if intake.artifact.payload_kind != "option_chain":
        raise ValueError("contract-run payload_kind must be option_chain")

    # Stage 2: strict canonical schema parse.
    snapshot = parse_option_snapshot(
        snapshot_path, intake.artifact.source_id, intake.artifact.payload_sha256
    )

    # Stage 3 (optional): exchange-session gate; if absent, fail closed on handoff
    # but still report scan economics.
    session_gate = None
    if session_path is not None:
        session_payload = json.loads(
            session_path.read_text(encoding="utf-8")
        )
        session = parse_market_session_evidence(session_payload)
        session_gate = evaluate_market_session(
            session, decision_cutoff, minimum_seconds_before_close
        )
        if not session_gate.admissible:
            raise ValueError(
                "contract-run session blocked: "
                + ",".join(session_gate.reason_codes)
            )

    policy = SpreadScanPolicy(
        quantity=quantity,
        commission_per_contract=Decimal(commission_per_contract),
    )
    scan = scan_vertical_credit_spreads(snapshot, decision_cutoff, policy)

    incomes = []
    for evaluation in scan.evaluations:
        if not evaluation.admissible or evaluation.calculation is None:
            incomes.append(
                ContractIncome(
                    evaluation.pair_id,
                    snapshot.underlying_quote.symbol,
                    "-",
                    "-",
                    "-",
                    "0.00",
                    "0.00",
                    "0.00",
                    "-",
                    "0.00",
                    0,
                    False,
                    evaluation.reason_code,
                )
            )
            continue
        calc = evaluation.calculation
        incomes.append(
            ContractIncome(
                calc.spread_id,
                calc.underlying,
                snapshot.underlying_quote.symbol,
                str(calc.width_per_share),
                str(calc.break_even),
                str(calc.net_credit / (calc.contract_multiplier * calc.quantity)),
                str(calc.net_credit),
                str(calc.maximum_loss),
                str(calc.break_even),
                str(calc.return_on_risk),
                calc.days_to_expiration,
                True,
                "",
            )
        )

    admissible = [i for i in incomes if i.admissible]
    return {
        "schema_version": CONTRACT_RUN_VERSION,
        "mode": "REAL_OPTION_CHAIN_INCOME",
        "source_id": snapshot.source_id,
        "symbol": snapshot.underlying_quote.symbol,
        "decision_cutoff": decision_cutoff.isoformat(),
        "scan_disposition": scan.disposition,
        "pair_count": scan.pair_count,
        "admissible_count": scan.admissible_count,
        "income_structures": [
            {
                "structure": "VERTICAL_CREDIT_SPREAD",
                "admissible": i.admissible,
                "reason_code": i.reason_code,
                "contract_id": i.contract_id,
                "underlying": i.underlying,
                "net_credit_per_share": i.net_credit_per_share,
                "net_credit": i.net_credit,
                "maximum_loss": i.maximum_loss,
                "break_even": i.break_even,
                "return_on_risk": i.return_on_risk,
                "days_to_expiration": i.days_to_expiration,
                "trade_authorized": False,
            }
            for i in incomes
        ],
        "session_gate_applied": session_gate is not None,
        "note": (
            "Executable-side net credit from real bid/ask quotes. No probability "
            "or Risk of Ruin. No order placed; no trade authorized. Premium "
            "income arithmetic only."
        ),
    }


__all__ = ["CONTRACT_RUN_VERSION", "ContractIncome", "run_contract"]