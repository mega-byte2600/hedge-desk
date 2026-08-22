from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.options.session import MarketSessionEvidence, evaluate_market_session


OPEN = datetime(2026, 8, 21, 13, 30, tzinfo=timezone.utc)
CLOSE = datetime(2026, 8, 21, 20, 0, tzinfo=timezone.utc)


def evidence():
    return MarketSessionEvidence("OPRA", OPEN, CLOSE, OPEN, "a" * 64)


class MarketSessionTests(unittest.TestCase):
    def test_exact_latest_entry_passes_then_one_microsecond_blocks(self) -> None:
        latest = CLOSE - timedelta(minutes=15)
        self.assertTrue(evaluate_market_session(evidence(), latest, 900).admissible)
        result = evaluate_market_session(
            evidence(), latest + timedelta(microseconds=1), 900
        )
        self.assertIn("MARKET_ENTRY_WINDOW_CLOSED", result.reason_codes)

    def test_preopen_and_late_calendar_fail_closed(self) -> None:
        preopen = evaluate_market_session(evidence(), OPEN - timedelta(seconds=1), 900)
        self.assertIn("MARKET_NOT_OPEN", preopen.reason_codes)
        late = replace(evidence(), received_at=OPEN + timedelta(minutes=1))
        result = evaluate_market_session(late, OPEN, 900)
        self.assertIn("MARKET_CALENDAR_NOT_POINT_IN_TIME", result.reason_codes)

    def test_invalid_calendar_is_not_inferred(self) -> None:
        result = evaluate_market_session(
            replace(evidence(), regular_close=OPEN, calendar_artifact_sha256="bad"),
            OPEN,
            900,
        )
        self.assertIn("MARKET_SESSION_INTERVAL_INVALID", result.reason_codes)
        self.assertIn("MARKET_CALENDAR_HASH_INVALID", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
