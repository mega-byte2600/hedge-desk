"""Research and approval events on the tamper-evident trail.

The domain weighting puts records and supervisory review at the centre, so these events
must land on the same append-only hash chain as membership events, and a review recorded
without an actor or without reason codes must be refused rather than stored.
"""

import os
import tempfile
import unittest

from hedge_desk.membership_audit import MembershipAuditLog, verify_chain
from hedge_desk.research_audit import (
    GATE_BLOCKED,
    REPORT_PUBLISHED,
    RESEARCH_EVENTS,
    ResearchAudit,
    ResearchEvent,
)


class ResearchEventValidationTests(unittest.TestCase):
    def test_unknown_event_is_refused(self):
        with self.assertRaises(ValueError):
            ResearchEvent("research_something_new", "SPY", "gp@example.com", ["X"])

    def test_missing_actor_is_refused(self):
        # An anonymous review is not a record.
        with self.assertRaises(ValueError):
            ResearchEvent(GATE_BLOCKED, "SPY", "   ", ["RISK_GATE_BLOCKED"])

    def test_missing_subject_is_refused(self):
        with self.assertRaises(ValueError):
            ResearchEvent(GATE_BLOCKED, "", "gp@example.com", ["RISK_GATE_BLOCKED"])

    def test_reason_codes_are_required(self):
        with self.assertRaises(ValueError):
            ResearchEvent(GATE_BLOCKED, "SPY", "gp@example.com", [])

    def test_detail_is_reproducible(self):
        event = ResearchEvent(GATE_BLOCKED, "SPY", "risk@desk", ["A", "B"], detail="tier=guest")
        self.assertEqual(event.as_detail(), "subject=SPY; codes=A,B; detail=tier=guest")

    def test_event_set_is_closed(self):
        self.assertEqual(
            RESEARCH_EVENTS,
            frozenset({"research_review_recorded", "research_gate_cleared", "research_gate_blocked", "research_report_published"}),
        )


class ResearchAuditChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.log = MembershipAuditLog(os.path.join(self.tmp, "audit.db"))
        self.audit = ResearchAudit(self.log)

    def tearDown(self):
        self.log.close()

    def test_a_review_lands_on_the_chain_and_verifies(self):
        entry = self.audit.review("SPY", "gp@example.com", ["HUMAN_REVIEWED"])
        self.assertEqual(entry["event"], "research_review_recorded")
        self.assertEqual(entry["actor"], "gp@example.com")
        self.assertIn("subject=SPY", entry["detail"])
        self.assertEqual(self.audit.verify(), [], "the chain must stay intact")

    def test_gate_events_are_recorded_in_order(self):
        self.audit.gate_cleared("SPY", "risk@desk", ["RISK_GATE_CLEARED"])
        self.audit.gate_blocked("QQQ", "risk@desk", ["RISK_GATE_BLOCKED", "CONCENTRATION"])
        self.audit.report_published("morning-report", "gp@example.com", ["PAPER_ONLY"])
        entries = self.audit.entries()
        self.assertEqual([e["seq"] for e in entries], [1, 2, 3])
        self.assertEqual(entries[2]["event"], REPORT_PUBLISHED)
        self.assertEqual(self.audit.verify(), [])

    def test_tampering_breaks_verification(self):
        self.audit.review("SPY", "gp@example.com", ["HUMAN_REVIEWED"])
        self.audit.gate_cleared("SPY", "risk@desk", ["RISK_GATE_CLEARED"])
        entries = self.audit.entries()
        entries[0]["detail"] = "subject=SPY; codes=FORGED"
        self.assertTrue(verify_chain(entries), "an edited entry must fail verification")

    def test_research_and_membership_events_share_one_chain(self):
        # Same log, same chain: a research decision and a membership event interleave and
        # the sequence still verifies.
        self.log.record("guest_signin", "someone@example.com", actor="someone@example.com")
        self.audit.gate_cleared("SPY", "risk@desk", ["RISK_GATE_CLEARED"])
        self.log.record("lp_invited", "lp@example.com", actor="gp@example.com")
        entries = self.log.entries()
        self.assertEqual([e["seq"] for e in entries], [1, 2, 3])
        self.assertEqual(entries[1]["event"], "research_gate_cleared")
        self.assertEqual(self.log.verify(), [])

    def test_research_audit_requires_a_log(self):
        with self.assertRaises(ValueError):
            ResearchAudit(None)


if __name__ == "__main__":
    unittest.main()
