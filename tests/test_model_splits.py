from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.models import EvaluationWindow, evaluate_purged_walk_forward_split


UTC = timezone.utc
EVALUATED = datetime(2026, 8, 22, tzinfo=UTC)


def windows():
    return (
        EvaluationWindow("train", datetime(2020, 1, 1, tzinfo=UTC),
                         datetime(2023, 12, 31, tzinfo=UTC), 1000, "a" * 64),
        EvaluationWindow("validation", datetime(2024, 1, 8, tzinfo=UTC),
                         datetime(2024, 12, 31, tzinfo=UTC), 250, "b" * 64),
        EvaluationWindow("test", datetime(2025, 1, 8, tzinfo=UTC),
                         datetime(2025, 12, 31, tzinfo=UTC), 250, "c" * 64),
    )


class ModelSplitTests(unittest.TestCase):
    def test_purged_point_in_time_split_is_research_only_and_reproducible(self) -> None:
        result = evaluate_purged_walk_forward_split(
            *windows(), timedelta(days=7), EVALUATED
        )
        self.assertTrue(result.admissible)
        self.assertFalse(result.authoritative_risk_input)
        self.assertFalse(result.trade_authorized)
        self.assertEqual(len(result.artifact_sha256), 64)
        self.assertEqual(result, evaluate_purged_walk_forward_split(
            *windows(), timedelta(days=7), EVALUATED
        ))

    def test_overlap_and_future_test_data_fail_closed(self) -> None:
        train, validation, test = windows()
        result = evaluate_purged_walk_forward_split(
            train,
            replace(validation, started_at=train.ended_at),
            replace(test, ended_at=EVALUATED + timedelta(days=1)),
            timedelta(days=7),
            EVALUATED,
        )
        self.assertIn("TRAIN_VALIDATION_PURGE_VIOLATION", result.reason_codes)
        self.assertIn("MODEL_SPLIT_POINT_IN_TIME_VIOLATION", result.reason_codes)

    def test_collision_and_small_sample_fail_closed(self) -> None:
        train, validation, test = windows()
        result = evaluate_purged_walk_forward_split(
            train,
            replace(validation, dataset_sha256=train.dataset_sha256),
            replace(test, observation_count=99),
            timedelta(days=7),
            EVALUATED,
        )
        self.assertIn("MODEL_SPLIT_HASH_COLLISION", result.reason_codes)
        self.assertIn("MODEL_SPLIT_SAMPLE_INSUFFICIENT", result.reason_codes)

    def test_negative_embargo_or_naive_clock_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "embargo cannot be negative"):
            evaluate_purged_walk_forward_split(
                *windows(), timedelta(seconds=-1), EVALUATED
            )
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            evaluate_purged_walk_forward_split(
                *windows(), timedelta(days=7), EVALUATED.replace(tzinfo=None)
            )


if __name__ == "__main__":
    unittest.main()
