from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.jobs import JobStatus, ResearchJob, validate_research_job


NOW = datetime(2026, 9, 8, 21, 0, tzinfo=timezone.utc)


def job() -> ResearchJob:
    return ResearchJob(
        job_id="job-001",
        job_type="quant.backtest",
        requested_by="user-001",
        created_at=NOW,
        started_at=NOW + timedelta(seconds=1),
        completed_at=NOW + timedelta(seconds=10),
        status=JobStatus.COMPLETED,
        input_dataset_ids=("us_equity_daily",),
        input_parameters={"symbol": "AAPL", "lookback_days": 252},
        code_version="abc123",
        model_version=None,
        output_dataset_ids=("backtest-output-001",),
        logs=("started", "completed"),
        error_state=None,
    )


class ResearchJobContractTests(unittest.TestCase):
    def test_completed_job_records_reproducible_lineage(self) -> None:
        self.assertEqual(validate_research_job(job()), ())

    def test_completed_job_requires_output_dataset_and_terminal_time(self) -> None:
        reasons = validate_research_job(
            replace(job(), output_dataset_ids=(), completed_at=None)
        )

        self.assertIn("JOB_COMPLETION_OUTPUT_MISSING", reasons)
        self.assertIn("JOB_TERMINAL_TIME_MISSING", reasons)

    def test_queued_job_cannot_claim_execution_times(self) -> None:
        reasons = validate_research_job(
            replace(job(), status=JobStatus.QUEUED, output_dataset_ids=())
        )

        self.assertIn("JOB_QUEUED_HAS_EXECUTION_TIMES", reasons)

    def test_failed_and_blocked_jobs_require_error_state(self) -> None:
        for status in (JobStatus.FAILED, JobStatus.BLOCKED):
            with self.subTest(status=status):
                reasons = validate_research_job(
                    replace(job(), status=status, output_dataset_ids=(), error_state=None)
                )
                self.assertIn("JOB_ERROR_STATE_MISSING", reasons)

    def test_job_parameters_do_not_carry_secret_fields(self) -> None:
        reasons = validate_research_job(
            replace(job(), input_parameters={"token": "do-not-store"})
        )

        self.assertIn("JOB_PARAMETERS_CONTAIN_SECRET_FIELD", reasons)


if __name__ == "__main__":
    unittest.main()
