"""Durable research job contract shared by Emporion clients and workers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Mapping, Optional, Tuple


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


TERMINAL_JOB_STATES = frozenset({
    JobStatus.COMPLETED,
    JobStatus.FAILED,
    JobStatus.CANCELLED,
    JobStatus.BLOCKED,
})


@dataclass(frozen=True)
class ResearchJob:
    job_id: str
    job_type: str
    requested_by: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    status: JobStatus
    input_dataset_ids: Tuple[str, ...]
    input_parameters: Mapping[str, Any]
    code_version: str
    model_version: Optional[str]
    output_dataset_ids: Tuple[str, ...]
    logs: Tuple[str, ...]
    error_state: Optional[str]


def validate_research_job(job: ResearchJob) -> Tuple[str, ...]:
    """Validate reproducibility metadata without executing the job."""
    reasons = []
    if not job.job_id or not job.job_type or not job.requested_by:
        reasons.append("JOB_IDENTITY_MISSING")
    if job.created_at.tzinfo is None:
        reasons.append("JOB_CREATED_AT_NOT_TIMEZONE_AWARE")
    if job.started_at and job.started_at.tzinfo is None:
        reasons.append("JOB_STARTED_AT_NOT_TIMEZONE_AWARE")
    if job.completed_at and job.completed_at.tzinfo is None:
        reasons.append("JOB_COMPLETED_AT_NOT_TIMEZONE_AWARE")
    if job.started_at and job.started_at < job.created_at:
        reasons.append("JOB_STARTED_BEFORE_CREATED")
    if job.completed_at and not job.started_at:
        reasons.append("JOB_COMPLETED_WITHOUT_START")
    if job.started_at and job.completed_at and job.completed_at < job.started_at:
        reasons.append("JOB_COMPLETED_BEFORE_STARTED")
    if (
        not isinstance(job.input_dataset_ids, tuple)
        or len(set(job.input_dataset_ids)) != len(job.input_dataset_ids)
    ):
        reasons.append("JOB_INPUT_DATASETS_NONCANONICAL")
    if (
        not isinstance(job.output_dataset_ids, tuple)
        or len(set(job.output_dataset_ids)) != len(job.output_dataset_ids)
    ):
        reasons.append("JOB_OUTPUT_DATASETS_NONCANONICAL")
    if any(not item for item in job.input_dataset_ids + job.output_dataset_ids):
        reasons.append("JOB_DATASET_ID_MISSING")
    if not job.code_version:
        reasons.append("JOB_CODE_VERSION_MISSING")
    if job.status in (JobStatus.RUNNING, JobStatus.COMPLETED) and not job.started_at:
        reasons.append("JOB_START_TIME_MISSING")
    if job.status is JobStatus.COMPLETED and (not job.completed_at or not job.output_dataset_ids):
        reasons.append("JOB_COMPLETION_OUTPUT_MISSING")
    if job.status in (JobStatus.FAILED, JobStatus.BLOCKED) and not job.error_state:
        reasons.append("JOB_ERROR_STATE_MISSING")
    if job.status in TERMINAL_JOB_STATES and not job.completed_at:
        reasons.append("JOB_TERMINAL_TIME_MISSING")
    if job.status is JobStatus.QUEUED and (job.started_at or job.completed_at):
        reasons.append("JOB_QUEUED_HAS_EXECUTION_TIMES")
    if any(key.lower() in {"secret", "token", "password", "oauth"} for key in job.input_parameters):
        reasons.append("JOB_PARAMETERS_CONTAIN_SECRET_FIELD")
    return tuple(sorted(set(reasons)))
