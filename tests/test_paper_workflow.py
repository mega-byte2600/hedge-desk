from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
import unittest

from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan, run_reference_demo
from hedge_desk.domain import DecisionStatus
from hedge_desk.backoffice import BackOfficeStatus
from hedge_desk.paper import (
    HumanAuthorization,
    HumanAuthorizationStatus,
    MachineRiskStatus,
    approve_paper_trade,
    close_paper_trade,
    create_paper_trade_plan,
    execute_paper_open,
)


class PaperWorkflowTests(unittest.TestCase):
    def test_reference_plan_stops_at_human_checkpoint(self) -> None:
        output = run_reference_demo()
        self.assertEqual(output["next_action"], "human_authorization_required")
        self.assertEqual(output["plan"]["authorization"]["status"], "pending")
        self.assertNotIn("paper_open", output)

    def test_unapproved_plan_cannot_execute(self) -> None:
        with self.assertRaisesRegex(PermissionError, "human authorization"):
            execute_paper_open(build_reference_plan(), FIXTURE_AS_OF)

    def test_authorization_is_bound_to_exact_plan_hash(self) -> None:
        plan = build_reference_plan()
        forged = replace(
            plan,
            authorization=HumanAuthorization(
                status=HumanAuthorizationStatus.APPROVED,
                human_id="captain",
                decided_at=FIXTURE_AS_OF,
                plan_hash="wrong-plan",
            ),
        )
        with self.assertRaisesRegex(PermissionError, "not bound"):
            execute_paper_open(forged, FIXTURE_AS_OF)

    def test_material_change_after_approval_invalidates_plan(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", FIXTURE_AS_OF)
        changed_spread = replace(
            approved.spread,
            net_credit=approved.spread.net_credit + Decimal("0.01"),
        )
        changed_plan = replace(approved, spread=changed_spread)
        with self.assertRaisesRegex(PermissionError, "integrity check failed"):
            execute_paper_open(changed_plan, FIXTURE_AS_OF)

    def test_changed_portfolio_snapshot_invalidates_plan(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", FIXTURE_AS_OF)
        changed_compliance = replace(
            approved.compliance_decision,
            portfolio_snapshot_sha256="f" * 64,
        )
        changed_plan = replace(approved, compliance_decision=changed_compliance)
        with self.assertRaisesRegex(PermissionError, "integrity check failed"):
            execute_paper_open(changed_plan, FIXTURE_AS_OF)

    def test_stale_or_unknown_control_artifact_cannot_create_plan(self) -> None:
        plan = build_reference_plan()
        stale_risk = replace(
            plan.risk_decision,
            evaluated_at=FIXTURE_AS_OF - timedelta(seconds=121),
        )
        with self.assertRaisesRegex(ValueError, "risk control artifact is stale"):
            create_paper_trade_plan(
                plan.plan_id,
                plan.spread,
                stale_risk,
                plan.compliance_decision,
                plan.created_at,
                plan.approval_expires_at,
            )
        unknown_policy = replace(
            plan.compliance_decision, policy_version="unapproved-policy"
        )
        with self.assertRaisesRegex(ValueError, "policy version is not approved"):
            create_paper_trade_plan(
                plan.plan_id,
                plan.spread,
                plan.risk_decision,
                unknown_policy,
                plan.created_at,
                plan.approval_expires_at,
            )

    def test_control_artifact_exact_age_boundary_passes(self) -> None:
        plan = build_reference_plan()
        boundary_risk = replace(
            plan.risk_decision,
            evaluated_at=FIXTURE_AS_OF - timedelta(seconds=120),
        )
        created = create_paper_trade_plan(
            plan.plan_id,
            plan.spread,
            boundary_risk,
            plan.compliance_decision,
            plan.created_at,
            plan.approval_expires_at,
        )
        self.assertEqual(created.risk_decision.risk_model_version, "0.1.0-unvalidated")

    def test_human_cannot_override_machine_rejection(self) -> None:
        plan = build_reference_plan()
        rejected_decision = replace(
            plan.risk_decision,
            status=DecisionStatus.BLOCKED,
            reason_codes=("TEST_BLOCK",),
        )
        rejected_plan = create_paper_trade_plan(
            plan.plan_id,
            plan.spread,
            rejected_decision,
            plan.compliance_decision,
            plan.created_at,
            plan.approval_expires_at,
            plan.execution_quote_max_age_seconds,
        )
        self.assertIs(rejected_plan.machine_risk_status, MachineRiskStatus.REJECT)
        with self.assertRaisesRegex(PermissionError, "cannot override"):
            approve_paper_trade(rejected_plan, "captain", FIXTURE_AS_OF)

    def test_human_cannot_override_back_office_block(self) -> None:
        plan = build_reference_plan()
        blocked_compliance = replace(
            plan.compliance_decision,
            status=BackOfficeStatus.BLOCK,
            reason_codes=("FINRA_SEC_REVIEW_REQUIRED",),
        )
        blocked_plan = create_paper_trade_plan(
            plan.plan_id,
            plan.spread,
            plan.risk_decision,
            blocked_compliance,
            plan.created_at,
            plan.approval_expires_at,
            plan.execution_quote_max_age_seconds,
        )
        with self.assertRaisesRegex(PermissionError, "Back Office compliance block"):
            approve_paper_trade(blocked_plan, "captain", FIXTURE_AS_OF)

    def test_expired_human_approval_cannot_execute(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", FIXTURE_AS_OF)
        with self.assertRaisesRegex(PermissionError, "expired"):
            execute_paper_open(approved, plan.approval_expires_at + timedelta(seconds=1))

    def test_quote_freshness_boundary_is_enforced(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", FIXTURE_AS_OF)
        execute_paper_open(approved, FIXTURE_AS_OF + timedelta(seconds=120))
        with self.assertRaisesRegex(PermissionError, "quotes are stale"):
            execute_paper_open(approved, FIXTURE_AS_OF + timedelta(seconds=121))

    def test_paper_close_pnl_is_deterministic(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", FIXTURE_AS_OF)
        opened = execute_paper_open(approved, FIXTURE_AS_OF + timedelta(minutes=1))
        closed = close_paper_trade(
            opened,
            exit_debit_per_share=Decimal("0.40"),
            exit_commission_per_contract=Decimal("0.65"),
            closed_at=FIXTURE_AS_OF + timedelta(days=1),
        )
        self.assertEqual(closed.exit_debit, Decimal("40.00"))
        self.assertEqual(closed.exit_commission, Decimal("1.30"))
        self.assertEqual(closed.realized_pnl, Decimal("77.40"))

    def test_approved_demo_is_reproducible(self) -> None:
        first = run_reference_demo(True, "captain")
        second = run_reference_demo(True, "captain")
        self.assertEqual(first, second)
        self.assertEqual(first["paper_close"]["realized_pnl"], "77.40")


if __name__ == "__main__":
    unittest.main()
