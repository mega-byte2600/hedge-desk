"""Deterministic tests for the data-freshness gate (no network)."""

import unittest
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from hedge_desk.freshness import (
    expected_trading_day,
    freshness_summary,
    latest_completed_trading_day,
)

PT = ZoneInfo("America/Los_Angeles")
UTC = timezone.utc


def _at_2054_pt(year, month, day):
    """The nightly batch time (20:54 PT) on a given calendar day."""
    return datetime(year, month, day, 20, 54, tzinfo=PT)


class FreshnessTests(unittest.TestCase):
    def test_expected_trading_day_skips_weekend(self):
        # 2026-09-19 is a Saturday -> expected trading day is Friday 09-18.
        self.assertEqual(expected_trading_day(date(2026, 9, 19)), date(2026, 9, 18))
        # a Wednesday stays itself
        self.assertEqual(expected_trading_day(date(2026, 9, 16)), date(2026, 9, 16))

    def test_current_when_as_of_matches_expected(self):
        s = freshness_summary(["2026-09-18"], date(2026, 9, 19))
        self.assertTrue(s["is_current"])
        self.assertEqual(s["as_of"], "2026-09-18")
        self.assertEqual(s["expected_trading_day"], "2026-09-18")

    def test_stale_when_as_of_is_prior_day(self):
        # running on Thursday's close when Friday's is expected -> not current
        s = freshness_summary(["2026-09-17"], date(2026, 9, 18))
        self.assertFalse(s["is_current"])
        self.assertIn("not yet", s["note"])

    def test_no_bars_is_not_current(self):
        s = freshness_summary([], date(2026, 9, 18))
        self.assertFalse(s["is_current"])
        self.assertIsNone(s["as_of"])


class MarketTimeCutoffTests(unittest.TestCase):
    """latest_completed_trading_day reads the clock in America/New_York.

    Regression: the 20:54 PT batch runs at 23:54 ET but on the next UTC
    day, so deriving the expected day from the UTC date made the gate
    expect a close that cannot exist yet (failed closed 2026-11-03/04/05/
    08/09). Each failing night below must now expect that same day's close.
    """

    def test_failing_nights_expect_same_day_close(self):
        for day, expected in (
            (9, date(2026, 11, 9)),    # Mon
            (10, date(2026, 11, 10)),  # Tue
            (11, date(2026, 11, 11)),  # Wed (Veterans Day; NYSE open)
            (12, date(2026, 11, 12)),  # Thu
            (13, date(2026, 11, 13)),  # Fri (tonight's run)
        ):
            with self.subTest(day=day):
                self.assertEqual(
                    latest_completed_trading_day(_at_2054_pt(2026, 11, day)),
                    expected,
                )

    def test_weekend_evenings_expect_friday(self):
        self.assertEqual(
            latest_completed_trading_day(_at_2054_pt(2026, 11, 8)),  # Sun
            date(2026, 11, 6),
        )
        self.assertEqual(
            latest_completed_trading_day(_at_2054_pt(2026, 11, 7)),  # Sat
            date(2026, 11, 6),
        )

    def test_before_close_expects_prior_trading_day(self):
        # Mon 12:00 PT = 15:00 ET, before the close: Friday's close.
        self.assertEqual(
            latest_completed_trading_day(datetime(2026, 11, 9, 12, 0, tzinfo=PT)),
            date(2026, 11, 6),
        )
        # Tue 00:30 PT = 03:30 ET, before the open: Monday's close.
        self.assertEqual(
            latest_completed_trading_day(datetime(2026, 11, 10, 0, 30, tzinfo=PT)),
            date(2026, 11, 9),
        )

    def test_at_and_after_close_expects_today(self):
        # Mon 13:00 PT = 16:00 ET, exactly the close: today counts.
        self.assertEqual(
            latest_completed_trading_day(datetime(2026, 11, 9, 13, 0, tzinfo=PT)),
            date(2026, 11, 9),
        )
        # Mon 13:30 PT = 16:30 ET, the daily-run time: today counts.
        self.assertEqual(
            latest_completed_trading_day(datetime(2026, 11, 9, 13, 30, tzinfo=PT)),
            date(2026, 11, 9),
        )

    def test_same_instant_in_utc(self):
        # Mon 20:54 PT is Tue 04:54 UTC; the market-time reading is identical.
        self.assertEqual(
            latest_completed_trading_day(datetime(2026, 11, 10, 4, 54, tzinfo=UTC)),
            date(2026, 11, 9),
        )

    def test_spring_forward_week(self):
        # DST 2026 starts Sun Mar 8; Mon Mar 9 20:54 PDT = 23:54 EDT.
        self.assertEqual(
            latest_completed_trading_day(_at_2054_pt(2026, 3, 9)),
            date(2026, 3, 9),
        )

    def test_holiday_still_fails_closed(self):
        # Thanksgiving Thu Nov 26 2026: NYSE closed, but the module only
        # approximates holidays as weekdays, so the expectation stays Nov 26
        # and a run on Nov 25 bars is honestly not current — never faked.
        expected = latest_completed_trading_day(_at_2054_pt(2026, 11, 26))
        self.assertEqual(expected, date(2026, 11, 26))
        self.assertFalse(freshness_summary(["2026-11-25"], expected)["is_current"])

    def test_naive_datetime_rejected(self):
        with self.assertRaises(ValueError):
            latest_completed_trading_day(datetime(2026, 11, 9, 20, 54))

    def test_mid_session_partial_bar_is_not_current(self):
        # Observed in the live simulation Fri 2026-11-13 ~11:12 ET: the
        # source already shows a bar for today, but today's close has not
        # happened. The gate must not certify a partial bar as the close —
        # and must not claim the prior close is "not yet published" when
        # it is present in the data.
        now = datetime(2026, 11, 13, 11, 12, tzinfo=ZoneInfo("America/New_York"))
        expected = latest_completed_trading_day(now)
        self.assertEqual(expected, date(2026, 11, 12))
        s = freshness_summary(["2026-11-13"], expected)
        self.assertFalse(s["is_current"])
        self.assertNotIn("not yet published", s["note"])
        self.assertIn("whose close has not happened yet", s["note"])

    def test_gate_passes_on_the_failing_nights(self):
        # End-to-end at the helper level: with the real bar dates recorded
        # by the failed runs, the gate is current where the UTC-date
        # derivation said it was not.
        for day in (9, 10, 11, 12):
            with self.subTest(day=day):
                bar = f"2026-11-{day:02d}"
                expected = latest_completed_trading_day(_at_2054_pt(2026, 11, day))
                summary = freshness_summary([bar], expected)
                self.assertTrue(summary["is_current"], summary)
                self.assertEqual(
                    summary["note"], f"Running on {bar} close (current trading day)."
                )
                # The old derivation (UTC date as cutoff) failed this case.
                self.assertFalse(
                    freshness_summary([bar], date(2026, 11, day + 1))["is_current"]
                )


if __name__ == "__main__":
    unittest.main()
