from dataclasses import replace
from datetime import timedelta
import unittest

from hedge_desk.replay import (
    ReplayEventKind,
    reference_replay,
    reference_pending_replay,
    validate_replay,
)


class ReplayTests(unittest.TestCase):
    def test_complete_reference_replay_passes(self) -> None:
        self.assertTrue(validate_replay(reference_replay()).valid)
        pending = reference_pending_replay()
        self.assertTrue(validate_replay(pending).valid)
        self.assertEqual(pending[-1].kind, ReplayEventKind.HUMAN_PENDING)

    def test_fill_before_human_approval_fails(self) -> None:
        events = list(reference_replay())
        fill_index = tuple(event.kind for event in events).index(ReplayEventKind.PAPER_FILL)
        approval_index = tuple(event.kind for event in events).index(ReplayEventKind.HUMAN_APPROVED)
        fill = events[fill_index]
        approval = events[approval_index]
        events[fill_index] = replace(
            fill, received_time=approval.received_time - timedelta(microseconds=1)
        )
        self.assertIn(
            "REPLAY_RECEIVE_ORDER_INVALID", validate_replay(tuple(events)).reason_codes
        )

    def test_missing_compliance_stage_fails(self) -> None:
        events = tuple(
            event for event in reference_replay()
            if event.kind is not ReplayEventKind.COMPLIANCE_COMPLETE
        )
        self.assertIn("REPLAY_STAGE_ORDER_INVALID", validate_replay(events).reason_codes)

    def test_received_before_publication_is_lookahead_failure(self) -> None:
        events = list(reference_replay())
        event = events[0]
        events[0] = replace(
            event, received_time=event.event_time - timedelta(microseconds=1)
        )
        self.assertIn("RECEIVED_BEFORE_EVENT", validate_replay(tuple(events)).reason_codes)


if __name__ == "__main__":
    unittest.main()
