from dataclasses import replace
from datetime import date, timedelta
import unittest

from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan
from hedge_desk.options import (
    CorporateEventType,
    OptionType,
    ScheduledCorporateEvent,
    evaluate_event_calendar,
)


class OptionEventGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spread = build_reference_plan().spread

    def event(self, event_type: CorporateEventType, event_date: date):
        return ScheduledCorporateEvent(
            "event-1", "TEST", event_type, event_date,
            FIXTURE_AS_OF - timedelta(days=1), "a" * 64,
        )

    def test_complete_empty_calendar_passes(self) -> None:
        result = evaluate_event_calendar(
            "TEST", FIXTURE_AS_OF, self.spread.expiration_date, (), self.spread,
            OptionType.PUT, self.spread.break_even,
        )
        self.assertTrue(result.admissible)
        self.assertEqual(len(result.calendar_sha256), 64)

    def test_earnings_inside_holding_window_blocks(self) -> None:
        result = evaluate_event_calendar(
            "TEST", FIXTURE_AS_OF, self.spread.expiration_date,
            (self.event(CorporateEventType.EARNINGS, date(2026, 8, 5)),),
            self.spread, OptionType.PUT, self.spread.break_even,
        )
        self.assertIn("EARNINGS_INSIDE_PLANNED_HOLDING_WINDOW", result.reason_codes)

    def test_incomplete_or_late_calendar_evidence_blocks(self) -> None:
        late = replace(
            self.event(CorporateEventType.EARNINGS, date(2026, 8, 30)),
            published_at=FIXTURE_AS_OF + timedelta(seconds=1),
        )
        result = evaluate_event_calendar(
            "TEST", FIXTURE_AS_OF, date(2026, 8, 20), (late,), self.spread,
            OptionType.PUT, self.spread.break_even,
        )
        self.assertIn("EVENT_CALENDAR_INCOMPLETE_THROUGH_EXPIRATION", result.reason_codes)
        self.assertIn("EVENT_NOT_POINT_IN_TIME", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
