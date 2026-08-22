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


@dataclass(frozen=True)
class ScheduledRunReceipt:
    idempotency_key: str
    scheduled_for: datetime
    status: ScheduledRunStatus
    reason_codes: Tuple[str, ...]
    report_sha256: Optional[str]
    scheduler_version: str = SCHEDULER_VERSION


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
        )
    except Exception:
        receipt = ScheduledRunReceipt(
            request.idempotency_key,
            request.scheduled_for,
            ScheduledRunStatus.FAILED_CLOSED,
            ("EVALUATION_EXCEPTION",),
            None,
        )
    return prior_receipts + (receipt,)
