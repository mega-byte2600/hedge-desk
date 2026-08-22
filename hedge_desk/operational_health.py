"""Deterministic health evaluation for the latest paper-only scheduled run."""

from dataclasses import dataclass
from datetime import datetime
from math import ceil
from typing import Any, Mapping, Tuple

from hedge_desk.reporting import validate_report
from hedge_desk.scheduler import validate_serialized_scheduled_run_receipt


HEALTH_EVALUATOR_VERSION = "paper-run-health-1.0.0"


@dataclass(frozen=True)
class PaperRunHealth:
    status: str
    evaluated_at: datetime
    report_age_seconds: int
    reason_codes: Tuple[str, ...]
    live_authorized: bool = False


def evaluate_paper_run_health(
    report: Mapping[str, Any],
    receipt: Mapping[str, Any],
    journal_event_count: int,
    journal_head_hash: str,
    evaluated_at: datetime,
    maximum_age_seconds: int,
    expected_code_commit: str,
) -> PaperRunHealth:
    if evaluated_at.tzinfo is None:
        raise ValueError("health evaluation time must be timezone-aware")
    if type(maximum_age_seconds) is not int or maximum_age_seconds < 0:
        raise ValueError("maximum age must be a nonnegative integer")
    if type(journal_event_count) is not int or journal_event_count < 0:
        raise ValueError("journal event count must be a nonnegative integer")
    if not isinstance(expected_code_commit, str) or not expected_code_commit:
        raise ValueError("expected code commit is required")
    reasons = list(validate_serialized_scheduled_run_receipt(receipt))
    if not validate_report(dict(report)).publishable:
        reasons.append("REPORT_NOT_PUBLISHABLE")
    try:
        generated_at = datetime.fromisoformat(str(report["generated_at"]))
        if generated_at.tzinfo is None:
            raise ValueError
        exact_age = (evaluated_at - generated_at).total_seconds()
        age = ceil(exact_age)
    except (KeyError, TypeError, ValueError):
        generated_at = evaluated_at
        age = 0
        exact_age = 0
        reasons.append("REPORT_TIME_INVALID")
    if exact_age < 0:
        reasons.append("REPORT_FROM_FUTURE")
    elif exact_age > maximum_age_seconds:
        reasons.append("LATEST_RUN_STALE")
    if receipt.get("status") != "COMPLETE":
        reasons.append("SCHEDULED_RUN_INCOMPLETE")
    if receipt.get("report_sha256") != report.get("report_sha256"):
        reasons.append("REPORT_RECEIPT_HASH_MISMATCH")
    if report.get("code_commit") != expected_code_commit:
        reasons.append("CODE_COMMIT_MISMATCH")
    if (
        report.get("environment") != "paper"
        or report.get("live_orders_enabled") is not False
        or report.get("real_trades_executed") != 0
    ):
        reasons.append("PAPER_ONLY_VIOLATION")
    audit = report.get("audit_chain", {})
    if (
        journal_event_count != audit.get("event_count")
        or journal_head_hash != audit.get("head_hash")
    ):
        reasons.append("AUDIT_JOURNAL_REPORT_MISMATCH")
    reason_codes = tuple(sorted(set(reasons)))
    return PaperRunHealth(
        "HEALTHY_PAPER" if not reason_codes else "BLOCKED",
        evaluated_at,
        age,
        reason_codes,
        False,
    )
