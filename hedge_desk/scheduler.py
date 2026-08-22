"""Idempotent fail-closed orchestration for 24/7 paper evaluations."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Callable, Mapping, Optional, Tuple

from hedge_desk.reporting import validate_report


SCHEDULER_VERSION = "paper-scheduler-1.0.0"


class ScheduledRunStatus(str, Enum):
    COMPLETE = "COMPLETE"
    FAILED_CLOSED = "FAILED_CLOSED"
    DUPLICATE_SUPPRESSED = "DUPLICATE_SUPPRESSED"


@dataclass(frozen=True)
class ScheduledRunRequest:
    idempotency_key: str
    scheduled_for: datetime
    environment: str = "paper"
    recovery_of: Optional[str] = None


@dataclass(frozen=True)
class ScheduledRunReceipt:
    idempotency_key: str
    scheduled_for: datetime
    status: ScheduledRunStatus
    reason_codes: Tuple[str, ...]
    report_sha256: Optional[str]
    receipt_sha256: str
    scheduler_version: str = SCHEDULER_VERSION
    recovery_of: Optional[str] = None


def _make_receipt(
    request: ScheduledRunRequest,
    status: ScheduledRunStatus,
    reason_codes: Tuple[str, ...],
    report_sha256: Optional[str],
) -> ScheduledRunReceipt:
    ordered_reasons = tuple(sorted(set(reason_codes)))
    payload = {
        "idempotency_key": request.idempotency_key,
        "scheduled_for": request.scheduled_for.isoformat(),
        "status": status.value,
        "reason_codes": list(ordered_reasons),
        "report_sha256": report_sha256,
        "scheduler_version": SCHEDULER_VERSION,
        "recovery_of": request.recovery_of,
    }
    receipt_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ScheduledRunReceipt(
        request.idempotency_key,
        request.scheduled_for,
        status,
        ordered_reasons,
        report_sha256,
        receipt_hash,
        recovery_of=request.recovery_of,
    )


def validate_scheduled_run_receipt(receipt: ScheduledRunReceipt) -> Tuple[str, ...]:
    expected = _make_receipt(
        ScheduledRunRequest(
            receipt.idempotency_key,
            receipt.scheduled_for,
            recovery_of=receipt.recovery_of,
        ),
        receipt.status,
        receipt.reason_codes,
        receipt.report_sha256,
    )
    reasons = []
    if receipt.scheduler_version != SCHEDULER_VERSION:
        reasons.append("SCHEDULER_VERSION_INVALID")
    if receipt.reason_codes != tuple(sorted(set(receipt.reason_codes))):
        reasons.append("SCHEDULER_REASON_CODES_NONCANONICAL")
    if receipt.receipt_sha256 != expected.receipt_sha256:
        reasons.append("SCHEDULER_RECEIPT_HASH_MISMATCH")
    if receipt.status is ScheduledRunStatus.COMPLETE:
        if receipt.reason_codes or not receipt.report_sha256:
            reasons.append("SCHEDULER_COMPLETE_STATE_INVALID")
    elif receipt.report_sha256 is not None:
        reasons.append("SCHEDULER_NONCOMPLETE_REPORT_HASH_PRESENT")
    return tuple(sorted(reasons))


def validate_serialized_scheduled_run_receipt(
    value: Mapping[str, object],
) -> Tuple[str, ...]:
    expected_fields = {
        "idempotency_key", "scheduled_for", "status", "reason_codes",
        "report_sha256", "receipt_sha256", "scheduler_version", "recovery_of",
    }
    if set(value) != expected_fields:
        return ("SCHEDULER_RECEIPT_SCHEMA_INVALID",)
    try:
        raw_reasons = value["reason_codes"]
        if not isinstance(raw_reasons, list):
            raise ValueError("reason schema")
        receipt = ScheduledRunReceipt(
            str(value["idempotency_key"]),
            datetime.fromisoformat(str(value["scheduled_for"])),
            ScheduledRunStatus(str(value["status"])),
            tuple(str(item) for item in raw_reasons),
            None if value["report_sha256"] is None else str(value["report_sha256"]),
            str(value["receipt_sha256"]),
            str(value["scheduler_version"]),
            None if value["recovery_of"] is None else str(value["recovery_of"]),
        )
    except (TypeError, ValueError):
        return ("SCHEDULER_RECEIPT_SCHEMA_INVALID",)
    return validate_scheduled_run_receipt(receipt)


def execute_scheduled_run(
    request: ScheduledRunRequest,
    prior_receipts: Tuple[ScheduledRunReceipt, ...],
    report_builder: Callable[[datetime], Mapping[str, object]],
) -> Tuple[ScheduledRunReceipt, ...]:
    """Execute at most once and never convert an exception into a pass."""
    if not request.idempotency_key:
        raise ValueError("scheduled run idempotency key is required")
    if request.scheduled_for.tzinfo is None:
        raise ValueError("scheduled run timestamp must be timezone-aware")
    if request.recovery_of == request.idempotency_key:
        raise ValueError("a recovery run requires a distinct idempotency key")

    if any(
        receipt.idempotency_key == request.idempotency_key
        and receipt.status is not ScheduledRunStatus.DUPLICATE_SUPPRESSED
        for receipt in prior_receipts
    ):
        return prior_receipts + (
            _make_receipt(
                request,
                ScheduledRunStatus.DUPLICATE_SUPPRESSED,
                ("DUPLICATE_RUN_SUPPRESSED",),
                None,
            ),
        )

    if request.recovery_of is not None:
        recovery_sources = tuple(
            receipt
            for receipt in prior_receipts
            if receipt.idempotency_key == request.recovery_of
            and receipt.status is not ScheduledRunStatus.DUPLICATE_SUPPRESSED
        )
        valid_recovery = (
            len(recovery_sources) == 1
            and recovery_sources[0].status is ScheduledRunStatus.FAILED_CLOSED
            and recovery_sources[0].scheduled_for == request.scheduled_for
        )
        if not valid_recovery:
            return prior_receipts + (
                _make_receipt(
                    request,
                    ScheduledRunStatus.FAILED_CLOSED,
                    ("INVALID_RECOVERY_REQUEST",),
                    None,
                ),
            )

    if request.environment != "paper":
        return prior_receipts + (
            _make_receipt(
                request,
                ScheduledRunStatus.FAILED_CLOSED,
                ("PAPER_ONLY_VIOLATION",),
                None,
            ),
        )

    try:
        report = report_builder(request.scheduled_for)
        publication = validate_report(report)
        if not publication.publishable:
            return prior_receipts + (
                _make_receipt(
                    request,
                    ScheduledRunStatus.FAILED_CLOSED,
                    publication.reason_codes,
                    None,
                ),
            )
        report_hash = report.get("report_sha256")
        if not isinstance(report_hash, str):
            raise ValueError("finalized report hash is missing")
        receipt = _make_receipt(
            request,
            ScheduledRunStatus.COMPLETE,
            (),
            report_hash,
        )
    except Exception:
        receipt = _make_receipt(
            request,
            ScheduledRunStatus.FAILED_CLOSED,
            ("EVALUATION_EXCEPTION",),
            None,
        )
    return prior_receipts + (receipt,)
