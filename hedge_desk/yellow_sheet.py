"""Versioned, content-addressed rationale required before any trade proposal."""

import json
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from enum import Enum
from hashlib import sha256
from typing import TYPE_CHECKING, Any, Mapping, Optional, Tuple

if TYPE_CHECKING:
    from hedge_desk.audit import AuditEvent


YELLOW_SHEET_SCHEMA_VERSION = "hedge-desk-yellow-sheet-1.0.0"
YELLOW_SHEET_POLICY_VERSION = "yellow-sheet-policy-1.0.0"
YELLOW_SHEET_COMPONENT_VERSION = "yellow-sheet-validator-1.0.0"


class TradeAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    REDUCE = "REDUCE"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class EvidenceObservation:
    observation: str
    supports_hypothesis: bool
    source_id: str
    observed_at: datetime
    data_sha256: str
    rule_or_model_version: str


@dataclass(frozen=True)
class TradeLogicRule:
    action: TradeAction
    condition: str


@dataclass(frozen=True)
class InvalidationCondition:
    condition: str
    triggered: bool
    observed_at: datetime
    source_sha256: str


@dataclass(frozen=True)
class CrossMarketContext:
    bonds_and_yields: str
    yield_curve: str
    credit_spreads: str
    equities: str
    volatility: str
    commodities: str
    currencies: str
    liquidity_conditions: str


@dataclass(frozen=True)
class YellowSheetRiskContext:
    position_size: str
    max_loss: str
    drawdown_impact: str
    liquidity: str
    concentration: str
    risk_of_ruin_input_sha256: str
    risk_of_ruin_output_reference: str


@dataclass(frozen=True)
class YellowSheet:
    schema_version: str
    yellow_sheet_id: str
    version: int
    candidate_id: str
    plan_hash: str
    interest: str
    hypothesis: str
    investigation: Tuple[str, ...]
    evidence: Tuple[EvidenceObservation, ...]
    trade_logic: Tuple[TradeLogicRule, ...]
    invalidation: Tuple[InvalidationCondition, ...]
    cross_market_context: CrossMarketContext
    risk_context: YellowSheetRiskContext
    decision_rationale: str
    input_hashes: Tuple[str, ...]
    policy_version: str
    model_version: str
    created_at: datetime
    prior_yellow_sheet_version: Optional[int]
    artifact_sha256: str


@dataclass(frozen=True)
class YellowSheetGate:
    disposition: TradeAction
    reason_codes: Tuple[str, ...]
    yellow_sheet_id: Optional[str]
    yellow_sheet_version: Optional[int]
    artifact_sha256: Optional[str]
    rationale: str


def _valid_hash(value: object) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except (TypeError, ValueError):
        return False


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def yellow_sheet_payload(sheet: YellowSheet, include_artifact_hash: bool = True) -> Mapping[str, Any]:
    payload = _json_value(asdict(sheet))
    if not include_artifact_hash:
        payload.pop("artifact_sha256")
    return payload


def calculate_yellow_sheet_hash(sheet: YellowSheet) -> str:
    encoded = json.dumps(
        yellow_sheet_payload(sheet, include_artifact_hash=False),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def build_yellow_sheet(**values: Any) -> YellowSheet:
    """Build and content-address a typed sheet; validation remains a separate gate."""
    sheet = YellowSheet(artifact_sha256="", **values)
    return replace(sheet, artifact_sha256=calculate_yellow_sheet_hash(sheet))


def validate_yellow_sheet(
    sheet: Optional[YellowSheet],
    candidate_id: str,
    plan_hash: str,
    evaluated_at: datetime,
    max_evidence_age_seconds: int,
) -> YellowSheetGate:
    reasons = []
    if sheet is None:
        return YellowSheetGate(TradeAction.NO_TRADE, ("YELLOW_SHEET_MISSING",), None, None, None, "No Yellow Sheet was supplied.")
    if evaluated_at.tzinfo is None or max_evidence_age_seconds <= 0:
        raise ValueError("Yellow Sheet gate requires an aware clock and positive freshness limit")
    if sheet.schema_version != YELLOW_SHEET_SCHEMA_VERSION:
        reasons.append("YELLOW_SHEET_SCHEMA_UNSUPPORTED")
    if not sheet.yellow_sheet_id or sheet.version <= 0:
        reasons.append("YELLOW_SHEET_IDENTITY_INVALID")
    if sheet.version == 1 and sheet.prior_yellow_sheet_version is not None:
        reasons.append("YELLOW_SHEET_VERSION_LINEAGE_INVALID")
    if sheet.version > 1 and sheet.prior_yellow_sheet_version != sheet.version - 1:
        reasons.append("YELLOW_SHEET_VERSION_LINEAGE_INVALID")
    if sheet.candidate_id != candidate_id:
        reasons.append("YELLOW_SHEET_CANDIDATE_MISMATCH")
    if sheet.plan_hash != plan_hash:
        reasons.append("YELLOW_SHEET_PLAN_HASH_MISMATCH")
    if sheet.policy_version != YELLOW_SHEET_POLICY_VERSION:
        reasons.append("YELLOW_SHEET_POLICY_UNAPPROVED")
    if not sheet.model_version.strip():
        reasons.append("YELLOW_SHEET_MODEL_VERSION_MISSING")
    if sheet.created_at.tzinfo is None or sheet.created_at > evaluated_at:
        reasons.append("YELLOW_SHEET_TIMESTAMP_INVALID")
    if any(not value.strip() for value in (sheet.interest, sheet.hypothesis, sheet.decision_rationale)):
        reasons.append("YELLOW_SHEET_REQUIRED_TEXT_MISSING")
    if not sheet.investigation or any(not item.strip() for item in sheet.investigation):
        reasons.append("YELLOW_SHEET_INVESTIGATION_INCOMPLETE")
    expected_actions = set(TradeAction)
    actions = [rule.action for rule in sheet.trade_logic]
    if set(actions) != expected_actions or len(actions) != len(expected_actions) or any(not rule.condition.strip() for rule in sheet.trade_logic):
        reasons.append("YELLOW_SHEET_TRADE_LOGIC_INCOMPLETE")
    if not sheet.evidence:
        reasons.append("YELLOW_SHEET_EVIDENCE_MISSING")
    for item in sheet.evidence:
        if not item.observation.strip() or not item.source_id.strip() or not item.rule_or_model_version.strip() or not _valid_hash(item.data_sha256):
            reasons.append("YELLOW_SHEET_EVIDENCE_INVALID")
        if item.observed_at.tzinfo is None or item.observed_at > evaluated_at:
            reasons.append("YELLOW_SHEET_EVIDENCE_TIMESTAMP_INVALID")
        elif (evaluated_at - item.observed_at).total_seconds() > max_evidence_age_seconds:
            reasons.append("YELLOW_SHEET_EVIDENCE_STALE")
    if not sheet.invalidation:
        reasons.append("YELLOW_SHEET_INVALIDATION_MISSING")
    for item in sheet.invalidation:
        if not item.condition.strip() or item.observed_at.tzinfo is None or not _valid_hash(item.source_sha256):
            reasons.append("YELLOW_SHEET_INVALIDATION_INVALID")
        if item.triggered:
            reasons.append("YELLOW_SHEET_INVALIDATION_TRIGGERED")
    cross_market = asdict(sheet.cross_market_context)
    if any(not str(value).strip() for value in cross_market.values()):
        reasons.append("YELLOW_SHEET_CROSS_MARKET_INCOMPLETE")
    risk = asdict(sheet.risk_context)
    if any(not str(value).strip() for value in risk.values()) or not _valid_hash(sheet.risk_context.risk_of_ruin_input_sha256):
        reasons.append("YELLOW_SHEET_RISK_CONTEXT_INCOMPLETE")
    if not sheet.input_hashes or tuple(sorted(set(sheet.input_hashes))) != sheet.input_hashes or any(not _valid_hash(value) for value in sheet.input_hashes):
        reasons.append("YELLOW_SHEET_INPUT_HASHES_INVALID")
    if sheet.artifact_sha256 != calculate_yellow_sheet_hash(sheet):
        reasons.append("YELLOW_SHEET_ARTIFACT_HASH_MISMATCH")
    ordered = tuple(sorted(set(reasons)))
    return YellowSheetGate(
        TradeAction.NO_TRADE if ordered else TradeAction.HOLD,
        ordered,
        sheet.yellow_sheet_id,
        sheet.version,
        sheet.artifact_sha256,
        sheet.decision_rationale,
    )


def append_yellow_sheet_audit_event(
    chain: Tuple["AuditEvent", ...], sheet: YellowSheet, run_id: str
) -> Tuple["AuditEvent", ...]:
    """Persist a validated sheet hash in the existing tamper-evident lineage."""
    from hedge_desk.audit import append_audit_event

    prior_output = chain[-1].output_sha256 if chain else "0" * 64
    occurred_at = (
        max(sheet.created_at, chain[-1].occurred_at) if chain else sheet.created_at
    )
    return append_audit_event(
        chain, run_id, "YELLOW_SHEET", occurred_at, sheet.yellow_sheet_id,
        sheet.candidate_id, prior_output, sheet.artifact_sha256,
        YELLOW_SHEET_COMPONENT_VERSION, sheet.policy_version,
    )
