"""Content-addressed Front Office handoff to non-agentic control systems."""

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Tuple

from .scanner import SpreadScanResult
from .session import MarketSessionGate


CANDIDATE_HANDOFF_SCHEMA_VERSION = "premium-candidate-handoff-1.1.0"


@dataclass(frozen=True)
class CandidateControlHandoff:
    schema_version: str
    candidate_id: str
    source_id: str
    source_artifact_sha256: str
    spread_model_id: str
    spread_model_version: str
    maximum_loss: str
    maximum_win: str
    calculation_sha256: str
    market_calendar_sha256: str
    decision_time: str
    latest_entry_time: str
    next_action: str
    trade_authorized: bool
    handoff_sha256: str


def build_candidate_control_handoffs(
    scan: SpreadScanResult,
    session_gate: MarketSessionGate,
) -> Tuple[CandidateControlHandoff, ...]:
    """Bind exact economics; omit probability and Risk of Ruin by design."""
    if not session_gate.admissible:
        return ()
    handoffs = []
    for evaluation in scan.evaluations:
        if not evaluation.admissible or evaluation.calculation is None:
            continue
        calculation = evaluation.calculation
        calculation_payload = {
            "break_even": str(calculation.break_even),
            "calculated_at": calculation.calculated_at.isoformat(),
            "contract_ids": list(calculation.input_contract_ids),
            "expiration_date": calculation.expiration_date.isoformat(),
            "maximum_loss": str(calculation.maximum_loss),
            "model_id": calculation.model_id,
            "model_version": calculation.model_version,
            "net_credit": str(calculation.net_credit),
            "planned_exit_date": calculation.planned_exit_date.isoformat(),
            "quantity": calculation.quantity,
            "source_artifact_sha256": scan.source_artifact_sha256,
            "spread_id": calculation.spread_id,
        }
        calculation_hash = sha256(
            json.dumps(
                calculation_payload, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        payload = {
            "calculation_sha256": calculation_hash,
            "candidate_id": calculation.spread_id,
            "maximum_loss": str(calculation.maximum_loss),
            "maximum_win": str(calculation.net_credit),
            "market_calendar_sha256": session_gate.calendar_artifact_sha256,
            "decision_time": session_gate.decision_time.isoformat(),
            "latest_entry_time": session_gate.latest_entry_time.isoformat(),
            "next_action": "VALIDATED_RISK_INPUT_REQUIRED",
            "schema_version": CANDIDATE_HANDOFF_SCHEMA_VERSION,
            "source_artifact_sha256": scan.source_artifact_sha256,
            "source_id": scan.source_id,
            "spread_model_id": calculation.model_id,
            "spread_model_version": calculation.model_version,
            "trade_authorized": False,
        }
        handoff_hash = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest()
        handoffs.append(
            CandidateControlHandoff(
                CANDIDATE_HANDOFF_SCHEMA_VERSION,
                calculation.spread_id,
                scan.source_id,
                scan.source_artifact_sha256,
                calculation.model_id,
                calculation.model_version,
                str(calculation.maximum_loss),
                str(calculation.net_credit),
                calculation_hash,
                session_gate.calendar_artifact_sha256,
                session_gate.decision_time.isoformat(),
                session_gate.latest_entry_time.isoformat(),
                "VALIDATED_RISK_INPUT_REQUIRED",
                False,
                handoff_hash,
            )
        )
    return tuple(sorted(handoffs, key=lambda item: item.candidate_id))


def validate_candidate_control_handoff(
    handoff: CandidateControlHandoff,
) -> Tuple[str, ...]:
    reasons = []
    if handoff.schema_version != CANDIDATE_HANDOFF_SCHEMA_VERSION:
        reasons.append("HANDOFF_SCHEMA_UNSUPPORTED")
    for field, value in (
        ("SOURCE_ARTIFACT_HASH", handoff.source_artifact_sha256),
        ("CALCULATION_HASH", handoff.calculation_sha256),
        ("MARKET_CALENDAR_HASH", handoff.market_calendar_sha256),
    ):
        try:
            valid = len(value) == 64 and int(value, 16) >= 0
        except ValueError:
            valid = False
        if not valid:
            reasons.append(field + "_INVALID")
    if handoff.next_action != "VALIDATED_RISK_INPUT_REQUIRED":
        reasons.append("HANDOFF_NEXT_ACTION_INVALID")
    if handoff.trade_authorized:
        reasons.append("UNTRUSTED_TRADE_AUTHORIZATION")
    payload = {
        "calculation_sha256": handoff.calculation_sha256,
        "candidate_id": handoff.candidate_id,
        "maximum_loss": handoff.maximum_loss,
        "maximum_win": handoff.maximum_win,
        "market_calendar_sha256": handoff.market_calendar_sha256,
        "decision_time": handoff.decision_time,
        "latest_entry_time": handoff.latest_entry_time,
        "next_action": handoff.next_action,
        "schema_version": handoff.schema_version,
        "source_artifact_sha256": handoff.source_artifact_sha256,
        "source_id": handoff.source_id,
        "spread_model_id": handoff.spread_model_id,
        "spread_model_version": handoff.spread_model_version,
        "trade_authorized": handoff.trade_authorized,
    }
    expected = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if handoff.handoff_sha256 != expected:
        reasons.append("HANDOFF_HASH_MISMATCH")
    return tuple(sorted(reasons))
