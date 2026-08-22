"""Deterministic paper Back Office reconciliation; never live certification."""

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any, Dict, Mapping, Tuple

from .compliance import BackOfficeStatus


PAPER_RECONCILIATION_VERSION = "paper-back-office-reconciliation-1.1.0"


@dataclass(frozen=True)
class PaperReconciliation:
    plan_sha256: str
    internal_positions_sha256: str
    broker_positions_sha256: str
    internal_cash: Decimal
    broker_cash: Decimal
    unresolved_fill_count: int
    unresolved_lifecycle_count: int
    reconciled_at: datetime
    lifecycle_artifact_sha256: str
    environment: str
    status: BackOfficeStatus
    reason_codes: Tuple[str, ...]
    live_release_evidence_eligible: bool
    artifact_sha256: str


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) > 0
    except (TypeError, ValueError):
        return False


def evaluate_paper_reconciliation(
    plan_sha256: str,
    internal_positions_sha256: str,
    broker_positions_sha256: str,
    internal_cash: Decimal,
    broker_cash: Decimal,
    unresolved_fill_count: int,
    unresolved_lifecycle_count: int,
    reconciled_at: datetime,
    environment: str = "paper",
    lifecycle_artifact_sha256: str = "",
) -> PaperReconciliation:
    """Reconcile a frozen paper ledger without granting execution authority."""
    if reconciled_at.tzinfo is None:
        raise ValueError("reconciliation timestamp must be timezone-aware")
    if type(unresolved_fill_count) is not int or type(unresolved_lifecycle_count) is not int:
        raise ValueError("reconciliation exception counts must be integers")
    if unresolved_fill_count < 0 or unresolved_lifecycle_count < 0:
        raise ValueError("reconciliation exception counts cannot be negative")
    if not isinstance(internal_cash, Decimal) or not isinstance(broker_cash, Decimal):
        raise ValueError("reconciliation cash values must be Decimal")
    if not internal_cash.is_finite() or not broker_cash.is_finite():
        raise ValueError("reconciliation cash values must be finite")
    reasons = []
    if not _valid_hash(plan_sha256):
        reasons.append("RECONCILIATION_PLAN_HASH_INVALID")
    if lifecycle_artifact_sha256 and not _valid_hash(lifecycle_artifact_sha256):
        reasons.append("LIFECYCLE_ARTIFACT_HASH_INVALID")
    if not _valid_hash(internal_positions_sha256) or not _valid_hash(
        broker_positions_sha256
    ):
        reasons.append("RECONCILIATION_POSITION_HASH_INVALID")
    elif internal_positions_sha256 != broker_positions_sha256:
        reasons.append("POSITION_LEDGER_MISMATCH")
    if internal_cash != broker_cash:
        reasons.append("CASH_LEDGER_MISMATCH")
    if unresolved_fill_count:
        reasons.append("UNRESOLVED_FILL_EXCEPTIONS")
    if unresolved_lifecycle_count:
        reasons.append("UNRESOLVED_LIFECYCLE_EXCEPTIONS")
    if environment != "paper":
        reasons.append("PAPER_RECONCILIATION_ENVIRONMENT_REQUIRED")
    reason_codes = tuple(sorted(set(reasons)))
    status = BackOfficeStatus.BLOCK if reason_codes else BackOfficeStatus.PASS
    payload = {
        "broker_cash": str(broker_cash),
        "broker_positions_sha256": broker_positions_sha256,
        "environment": environment,
        "internal_cash": str(internal_cash),
        "internal_positions_sha256": internal_positions_sha256,
        "live_release_evidence_eligible": False,
        "lifecycle_artifact_sha256": lifecycle_artifact_sha256,
        "plan_sha256": plan_sha256,
        "reason_codes": list(reason_codes),
        "reconciled_at": reconciled_at.isoformat(),
        "status": status.value,
        "unresolved_fill_count": unresolved_fill_count,
        "unresolved_lifecycle_count": unresolved_lifecycle_count,
        "version": PAPER_RECONCILIATION_VERSION,
    }
    artifact_sha256 = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return PaperReconciliation(
        plan_sha256,
        internal_positions_sha256,
        broker_positions_sha256,
        internal_cash,
        broker_cash,
        unresolved_fill_count,
        unresolved_lifecycle_count,
        reconciled_at,
        lifecycle_artifact_sha256,
        environment,
        status,
        reason_codes,
        False,
        artifact_sha256,
    )


def serialize_paper_reconciliation(value: PaperReconciliation) -> Dict[str, Any]:
    return {
        "version": PAPER_RECONCILIATION_VERSION,
        "plan_sha256": value.plan_sha256,
        "internal_positions_sha256": value.internal_positions_sha256,
        "broker_positions_sha256": value.broker_positions_sha256,
        "internal_cash": str(value.internal_cash),
        "broker_cash": str(value.broker_cash),
        "unresolved_fill_count": value.unresolved_fill_count,
        "unresolved_lifecycle_count": value.unresolved_lifecycle_count,
        "reconciled_at": value.reconciled_at.isoformat(),
        "lifecycle_artifact_sha256": value.lifecycle_artifact_sha256,
        "environment": value.environment,
        "status": value.status.value,
        "reason_codes": list(value.reason_codes),
        "live_release_evidence_eligible": value.live_release_evidence_eligible,
        "artifact_sha256": value.artifact_sha256,
    }


def validate_serialized_paper_reconciliation(
    value: Mapping[str, Any],
) -> Tuple[str, ...]:
    try:
        if value.get("version") != PAPER_RECONCILIATION_VERSION:
            raise ValueError("version")
        rebuilt = evaluate_paper_reconciliation(
            str(value["plan_sha256"]),
            str(value["internal_positions_sha256"]),
            str(value["broker_positions_sha256"]),
            Decimal(str(value["internal_cash"])),
            Decimal(str(value["broker_cash"])),
            value["unresolved_fill_count"],
            value["unresolved_lifecycle_count"],
            datetime.fromisoformat(str(value["reconciled_at"])),
            str(value["environment"]),
            str(value["lifecycle_artifact_sha256"]),
        )
        expected = serialize_paper_reconciliation(rebuilt)
    except (ArithmeticError, KeyError, TypeError, ValueError):
        return ("BACK_OFFICE_RECONCILIATION_SCHEMA_INVALID",)
    return (
        ()
        if dict(value) == expected
        else ("BACK_OFFICE_RECONCILIATION_ARTIFACT_INVALID",)
    )
