from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.options.session import (
    MarketSessionEvidence,
    evaluate_market_session,
    parse_market_session_evidence,
)


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

    def test_parser_rejects_unknown_fields_and_naive_time_remains_blocked(self) -> None:
        payload = {
            "schema_version": "hedge-desk-market-session-1.0.0",
            "venue": "OPRA", "regular_open": "2026-08-21T13:30:00",
            "regular_close": "2026-08-21T20:00:00Z",
            "received_at": "2026-08-21T12:00:00Z",
            "calendar_artifact_sha256": "a" * 64,
        }
        parsed = parse_market_session_evidence(payload)
        result = evaluate_market_session(parsed, OPEN, 900)
        self.assertIn("MARKET_SESSION_TIMESTAMP_NOT_TIMEZONE_AWARE", result.reason_codes)
        payload["extra"] = True
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            parse_market_session_evidence(payload)


if __name__ == "__main__":
    unittest.main()
