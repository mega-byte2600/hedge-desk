from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.off_exchange import OtcWeeklyObservation, evaluate_otc_weekly_observation


NOW = datetime(2026, 8, 22, 9, 0, tzinfo=timezone.utc)


def observation():
    return OtcWeeklyObservation(
        "finra-week-1", "TEST", "T1", date(2026, 7, 27), 100000, 1000,
        NOW - timedelta(days=1), NOW - timedelta(days=1), 14, "a" * 64,
    )


class OffExchangeTests(unittest.TestCase):
    def test_finra_aggregate_is_descriptive_delayed_and_never_live_signal(self) -> None:
        result = evaluate_otc_weekly_observation(observation(), NOW)
        self.assertTrue(result.admissible)
        self.assertEqual(result.average_shares_per_trade, Decimal("100"))
        self.assertTrue(result.delayed_aggregate_evidence)
        self.assertFalse(result.live_hidden_order_visibility)
        self.assertFalse(result.directional_signal_authorized)
        self.assertFalse(result.trade_authorized)

    def test_understated_delay_or_lookahead_fails_closed(self) -> None:
        attacked = replace(
            observation(), declared_publication_delay_days=0,
            received_at=NOW + timedelta(seconds=1),
        )
        result = evaluate_otc_weekly_observation(attacked, NOW)
        self.assertIn("OTC_PUBLICATION_DELAY_UNDERSTATED", result.reason_codes)
        self.assertIn("OTC_POINT_IN_TIME_VIOLATION", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
