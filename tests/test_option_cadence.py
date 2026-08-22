from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.options import evaluate_premium_cadence


NOW = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


class OptionCadenceTests(unittest.TestCase):
    def test_no_prior_entry_allows_research_but_never_authorizes_trade(self) -> None:
        result = evaluate_premium_cadence(NOW, None)
        self.assertTrue(result.new_entry_evaluation_allowed)
        self.assertTrue(result.monitoring_allowed)
        self.assertFalse(result.trade_authorized)
        self.assertEqual(len(result.artifact_sha256), 64)

    def test_exact_21_day_boundary_in_new_month_passes(self) -> None:
        evaluated = datetime(2026, 8, 1, 12, 0, tzinfo=timezone.utc)
        result = evaluate_premium_cadence(
            evaluated, evaluated - timedelta(days=21)
        )
        self.assertTrue(result.new_entry_evaluation_allowed)
        self.assertEqual(result.reason_codes, ())

    def test_same_month_or_one_microsecond_early_blocks_new_entry_only(self) -> None:
        same_month = evaluate_premium_cadence(NOW, NOW - timedelta(days=1))
        self.assertIn("MONTHLY_NEW_ENTRY_ALREADY_EVALUATED", same_month.reason_codes)
        self.assertTrue(same_month.monitoring_allowed)
        evaluated = datetime(2026, 8, 1, 12, 0, tzinfo=timezone.utc)
        early = evaluate_premium_cadence(
            evaluated,
            evaluated - timedelta(days=21) + timedelta(microseconds=1),
        )
        self.assertIn("MINIMUM_ENTRY_INTERVAL_NOT_REACHED", early.reason_codes)
        self.assertTrue(early.monitoring_allowed)

    def test_future_or_naive_times_fail_closed(self) -> None:
        future = evaluate_premium_cadence(NOW, NOW + timedelta(days=1))
        self.assertIn("LAST_ENTRY_FROM_FUTURE", future.reason_codes)
        self.assertFalse(future.new_entry_evaluation_allowed)
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            evaluate_premium_cadence(NOW.replace(tzinfo=None), None)

    def test_month_identity_is_normalized_to_new_york_not_input_offset(self) -> None:
        evaluated = datetime(2026, 8, 1, 0, 30, tzinfo=timezone.utc)
        prior = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
        result = evaluate_premium_cadence(evaluated, prior)
        self.assertIn("MONTHLY_NEW_ENTRY_ALREADY_EVALUATED", result.reason_codes)
        self.assertEqual(result.cadence_timezone, "America/New_York")
        with self.assertRaisesRegex(ValueError, "timezone invalid"):
            evaluate_premium_cadence(evaluated, prior, cadence_timezone="Mars/Base")


if __name__ == "__main__":
    unittest.main()
