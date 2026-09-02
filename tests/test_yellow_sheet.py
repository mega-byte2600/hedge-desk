from dataclasses import replace
from datetime import timedelta
import unittest

from hedge_desk.audit import verify_audit_chain
from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan
from hedge_desk.paper import approve_paper_trade, create_paper_trade_plan
from hedge_desk.yellow_sheet import (
    TradeAction,
    append_yellow_sheet_audit_event,
    calculate_yellow_sheet_hash,
    validate_yellow_sheet,
)


def rehash(sheet, **changes):
    changed = replace(sheet, **changes, artifact_sha256="")
    return replace(changed, artifact_sha256=calculate_yellow_sheet_hash(changed))


class YellowSheetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = build_reference_plan()
        self.sheet = self.plan.yellow_sheet

    def gate(self, sheet=None):
        return validate_yellow_sheet(
            self.sheet if sheet is None else sheet,
            self.plan.risk_decision.candidate_id,
            self.plan.plan_hash,
            FIXTURE_AS_OF,
            120,
        )

    def test_valid_yellow_sheet(self) -> None:
        result = self.gate()
        self.assertEqual(result.disposition, TradeAction.HOLD)
        self.assertEqual(result.reason_codes, ())

    def test_missing_yellow_sheet(self) -> None:
        result = validate_yellow_sheet(
            None, self.plan.risk_decision.candidate_id, self.plan.plan_hash,
            FIXTURE_AS_OF, 120,
        )
        self.assertEqual(result.disposition, TradeAction.NO_TRADE)
        self.assertEqual(result.reason_codes, ("YELLOW_SHEET_MISSING",))

    def test_incomplete_yellow_sheet(self) -> None:
        result = self.gate(rehash(self.sheet, decision_rationale=""))
        self.assertIn("YELLOW_SHEET_REQUIRED_TEXT_MISSING", result.reason_codes)
        self.assertEqual(result.disposition, TradeAction.NO_TRADE)

    def test_stale_evidence(self) -> None:
        stale = replace(
            self.sheet.evidence[0],
            observed_at=FIXTURE_AS_OF - timedelta(seconds=121),
        )
        result = self.gate(rehash(self.sheet, evidence=(stale,)))
        self.assertIn("YELLOW_SHEET_EVIDENCE_STALE", result.reason_codes)

    def test_mismatched_plan_hash(self) -> None:
        result = self.gate(rehash(self.sheet, plan_hash="f" * 64))
        self.assertIn("YELLOW_SHEET_PLAN_HASH_MISMATCH", result.reason_codes)

    def test_revised_yellow_sheet_version(self) -> None:
        revised = rehash(
            self.sheet,
            version=2,
            prior_yellow_sheet_version=1,
            decision_rationale=self.sheet.decision_rationale + " Revised.",
        )
        self.assertEqual(self.gate(revised).reason_codes, ())
        broken = rehash(revised, prior_yellow_sheet_version=None)
        self.assertIn(
            "YELLOW_SHEET_VERSION_LINEAGE_INVALID", self.gate(broken).reason_codes
        )

    def test_invalidation_trigger(self) -> None:
        triggered = replace(self.sheet.invalidation[0], triggered=True)
        result = self.gate(rehash(self.sheet, invalidation=(triggered,)))
        self.assertIn("YELLOW_SHEET_INVALIDATION_TRIGGERED", result.reason_codes)
        self.assertEqual(result.disposition, TradeAction.NO_TRADE)

    def test_no_trade_enforced_at_authorization(self) -> None:
        blocked = create_paper_trade_plan(
            self.plan.plan_id,
            self.plan.spread,
            self.plan.risk_decision,
            self.plan.compliance_decision,
            self.plan.created_at,
            self.plan.approval_expires_at,
            event_calendar_gate=self.plan.event_calendar_gate,
            yellow_sheet=None,
        )
        self.assertEqual(blocked.proposal_disposition, TradeAction.NO_TRADE)
        self.assertIn("YELLOW_SHEET_MISSING", blocked.reason_codes)
        with self.assertRaisesRegex(PermissionError, "cannot override"):
            approve_paper_trade(blocked, "captain", FIXTURE_AS_OF)

    def test_sheet_hash_is_in_tamper_evident_audit_lineage(self) -> None:
        chain = append_yellow_sheet_audit_event(
            (), self.sheet, "yellow-sheet-test-run"
        )
        self.assertEqual(chain[-1].stage, "YELLOW_SHEET")
        self.assertEqual(chain[-1].output_sha256, self.sheet.artifact_sha256)
        self.assertEqual(verify_audit_chain(chain), ())


if __name__ == "__main__":
    unittest.main()
