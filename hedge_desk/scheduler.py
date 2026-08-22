"""Idempotent fail-closed orchestration for 24/7 paper evaluations."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
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
    scheduler_version: str = SCHEDULER_VERSION
    recovery_of: Optional[str] = None


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
            ScheduledRunReceipt(
                request.idempotency_key,
                request.scheduled_for,
                ScheduledRunStatus.DUPLICATE_SUPPRESSED,
                ("DUPLICATE_RUN_SUPPRESSED",),
                None,
                recovery_of=request.recovery_of,
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
                ScheduledRunReceipt(
                    request.idempotency_key,
                    request.scheduled_for,
                    ScheduledRunStatus.FAILED_CLOSED,
                    ("INVALID_RECOVERY_REQUEST",),
                    None,
                    recovery_of=request.recovery_of,
                ),
            )

    if request.environment != "paper":
        return prior_receipts + (
            ScheduledRunReceipt(
                request.idempotency_key,
                request.scheduled_for,
                ScheduledRunStatus.FAILED_CLOSED,
                ("PAPER_ONLY_VIOLATION",),
                None,
                recovery_of=request.recovery_of,
            ),
        )

    try:
        report = report_builder(request.scheduled_for)
        publication = validate_report(report)
        if not publication.publishable:
            return prior_receipts + (
                ScheduledRunReceipt(
                    request.idempotency_key,
                    request.scheduled_for,
                    ScheduledRunStatus.FAILED_CLOSED,
                    publication.reason_codes,
                    None,
                    recovery_of=request.recovery_of,
                ),
            )
        report_hash = report.get("report_sha256")
        if not isinstance(report_hash, str):
            raise ValueError("finalized report hash is missing")
        receipt = ScheduledRunReceipt(
            request.idempotency_key,
            request.scheduled_for,
            ScheduledRunStatus.COMPLETE,
            (),
            report_hash,
            recovery_of=request.recovery_of,
        )
    except Exception:
        receipt = ScheduledRunReceipt(
            request.idempotency_key,
            request.scheduled_for,
            ScheduledRunStatus.FAILED_CLOSED,
            ("EVALUATION_EXCEPTION",),
            None,
            recovery_of=request.recovery_of,
        )
    return prior_receipts + (receipt,)
