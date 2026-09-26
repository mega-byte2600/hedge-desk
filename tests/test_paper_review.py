import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

from hedge_desk.backoffice import BackOfficeStatus
from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan
from hedge_desk.domain import DecisionStatus
from hedge_desk.paper import (
    HumanAuthorizationStatus,
    MachineRiskStatus,
    PaperReviewQueue,
    approve_paper_trade,
    create_paper_trade_plan,
    load_plan_file,
    reject_paper_trade,
    submit_plan_for_review,
    write_plan_file,
)

DECIDED_AT = FIXTURE_AS_OF + timedelta(minutes=1)


def _machine_reject_plan():
    plan = build_reference_plan()
    rejected_decision = replace(
        plan.risk_decision,
        status=DecisionStatus.BLOCKED,
        reason_codes=("TEST_BLOCK",),
    )
    return create_paper_trade_plan(
        plan.plan_id,
        plan.spread,
        rejected_decision,
        plan.compliance_decision,
        plan.created_at,
        plan.approval_expires_at,
        plan.execution_quote_max_age_seconds,
        event_calendar_gate=plan.event_calendar_gate,
    )


def _compliance_block_plan():
    plan = build_reference_plan()
    blocked_compliance = replace(
        plan.compliance_decision,
        status=BackOfficeStatus.BLOCK,
        reason_codes=("FINRA_SEC_REVIEW_REQUIRED",),
    )
    return create_paper_trade_plan(
        plan.plan_id,
        plan.spread,
        plan.risk_decision,
        blocked_compliance,
        plan.created_at,
        plan.approval_expires_at,
        plan.execution_quote_max_age_seconds,
        event_calendar_gate=plan.event_calendar_gate,
    )


def _plan_file(tmpdir):
    plan = build_reference_plan()
    path = Path(tmpdir) / "plan.json"
    write_plan_file(plan, path)
    return plan, path


class RejectPaperTradeTests(unittest.TestCase):
    def test_reject_happy_path_binds_reason_codes_to_plan_hash(self) -> None:
        plan = build_reference_plan()
        rejected = reject_paper_trade(
            plan, "captain", DECIDED_AT, ("THESIS_INVALIDATED", "VOL_TOO_RICH")
        )
        authorization = rejected.authorization
        self.assertIs(authorization.status, HumanAuthorizationStatus.REJECTED)
        self.assertEqual(authorization.human_id, "captain")
        self.assertEqual(authorization.decided_at, DECIDED_AT)
        self.assertEqual(authorization.plan_hash, plan.plan_hash)
        self.assertEqual(
            authorization.reason_codes, ("THESIS_INVALIDATED", "VOL_TOO_RICH")
        )

    def test_reject_requires_reason_codes(self) -> None:
        plan = build_reference_plan()
        with self.assertRaisesRegex(ValueError, "reason code"):
            reject_paper_trade(plan, "captain", DECIDED_AT, ())
        with self.assertRaisesRegex(ValueError, "reason code"):
            reject_paper_trade(plan, "captain", DECIDED_AT, ("  ",))

    def test_reject_requires_human_identity_and_tz_aware_timestamp(self) -> None:
        plan = build_reference_plan()
        with self.assertRaisesRegex(ValueError, "human identity"):
            reject_paper_trade(plan, "  ", DECIDED_AT, ("NO_THESIS",))
        naive = DECIDED_AT.replace(tzinfo=None)
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            reject_paper_trade(plan, "captain", naive, ("NO_THESIS",))

    def test_reject_refuses_expired_plan(self) -> None:
        plan = build_reference_plan()
        with self.assertRaisesRegex(PermissionError, "expired"):
            reject_paper_trade(
                plan,
                "captain",
                plan.approval_expires_at + timedelta(seconds=1),
                ("TOO_LATE",),
            )

    def test_reject_refuses_tampered_plan_hash(self) -> None:
        plan = build_reference_plan()
        tampered = replace(plan, plan_hash="0" * 64)
        with self.assertRaisesRegex(PermissionError, "integrity check failed"):
            reject_paper_trade(tampered, "captain", DECIDED_AT, ("NO_THESIS",))

    def test_reject_refuses_already_decided_plan(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", DECIDED_AT)
        with self.assertRaisesRegex(PermissionError, "already received"):
            reject_paper_trade(approved, "captain", DECIDED_AT, ("CHANGED_MIND",))
        rejected = reject_paper_trade(plan, "captain", DECIDED_AT, ("NO_THESIS",))
        with self.assertRaisesRegex(PermissionError, "already received"):
            reject_paper_trade(rejected, "captain", DECIDED_AT, ("STILL_NO",))

    def test_reject_is_allowed_when_machine_risk_rejects(self) -> None:
        plan = _machine_reject_plan()
        self.assertIs(plan.machine_risk_status, MachineRiskStatus.REJECT)
        rejected = reject_paper_trade(plan, "captain", DECIDED_AT, ("MACHINE_AGREES",))
        self.assertIs(rejected.authorization.status, HumanAuthorizationStatus.REJECTED)
        self.assertEqual(rejected.authorization.reason_codes, ("MACHINE_AGREES",))

    def test_reject_is_allowed_when_compliance_blocks(self) -> None:
        plan = _compliance_block_plan()
        self.assertIs(plan.compliance_decision.status, BackOfficeStatus.BLOCK)
        rejected = reject_paper_trade(plan, "captain", DECIDED_AT, ("COMPLIANCE_BLOCK",))
        self.assertIs(rejected.authorization.status, HumanAuthorizationStatus.REJECTED)


class PaperReviewQueueTests(unittest.TestCase):
    def test_submit_pending_list_and_get(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        pending = queue.pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["plan_id"], plan.plan_id)
        self.assertEqual(pending[0]["plan_hash"], plan.plan_hash)
        self.assertEqual(
            pending[0]["approval_expires_at"], plan.approval_expires_at.isoformat()
        )
        self.assertEqual(pending[0]["machine_risk_status"], "pass")
        self.assertIs(queue.get(plan.plan_id).authorization.status,
                      HumanAuthorizationStatus.PENDING)

    def test_pending_lists_in_submission_order(self) -> None:
        base = build_reference_plan()
        first = replace(base, plan_id="plan-a")
        second = replace(base, plan_id="plan-b")
        queue = PaperReviewQueue()
        queue.submit(second)
        queue.submit(first)
        self.assertEqual(
            [entry["plan_id"] for entry in queue.pending()], ["plan-b", "plan-a"]
        )

    def test_duplicate_submit_refused(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        with self.assertRaisesRegex(ValueError, "duplicate plan_id"):
            queue.submit(plan)

    def test_submit_refuses_non_pending_plan(self) -> None:
        plan = build_reference_plan()
        approved = approve_paper_trade(plan, "captain", DECIDED_AT)
        with self.assertRaisesRegex(ValueError, "only PENDING"):
            PaperReviewQueue().submit(approved)

    def test_get_unknown_plan_id_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            PaperReviewQueue().get("no-such-plan")

    def test_decide_unknown_plan_id_raises_key_error(self) -> None:
        queue = PaperReviewQueue()
        with self.assertRaises(KeyError):
            queue.decide("no-such-plan", "captain", DECIDED_AT, approve=True)

    def test_decide_approve_happy_path(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        decided = queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)
        self.assertIs(decided.authorization.status, HumanAuthorizationStatus.APPROVED)
        self.assertEqual(decided.authorization.plan_hash, plan.plan_hash)
        self.assertEqual(queue.pending(), [])
        self.assertIs(
            queue.get(plan.plan_id).authorization.status,
            HumanAuthorizationStatus.APPROVED,
        )

    def test_decide_reject_happy_path(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        decided = queue.decide(
            plan.plan_id, "captain", DECIDED_AT, approve=False,
            reason_codes=("THESIS_INVALIDATED",),
        )
        self.assertIs(decided.authorization.status, HumanAuthorizationStatus.REJECTED)
        self.assertEqual(
            decided.authorization.reason_codes, ("THESIS_INVALIDATED",)
        )
        self.assertEqual(queue.pending(), [])

    def test_decide_refuses_second_decision(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)
        with self.assertRaisesRegex(PermissionError, "already received"):
            queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)
        with self.assertRaisesRegex(PermissionError, "already received"):
            queue.decide(
                plan.plan_id, "captain", DECIDED_AT, approve=False,
                reason_codes=("CHANGED_MIND",),
            )

    def test_decide_refuses_expired_plan(self) -> None:
        plan = build_reference_plan()
        queue = submit_plan_for_review(plan)
        late = plan.approval_expires_at + timedelta(seconds=1)
        with self.assertRaisesRegex(PermissionError, "expired"):
            queue.decide(plan.plan_id, "captain", late, approve=True)
        with self.assertRaisesRegex(PermissionError, "expired"):
            queue.decide(
                plan.plan_id, "captain", late, approve=False,
                reason_codes=("TOO_LATE",),
            )

    def test_decide_refuses_tampered_plan_hash(self) -> None:
        plan = build_reference_plan()
        tampered = replace(plan, plan_hash="0" * 64)
        queue = submit_plan_for_review(tampered)
        with self.assertRaisesRegex(PermissionError, "integrity check failed"):
            queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)
        with self.assertRaisesRegex(PermissionError, "integrity check failed"):
            queue.decide(
                plan.plan_id, "captain", DECIDED_AT, approve=False,
                reason_codes=("NO_THESIS",),
            )

    def test_decide_cannot_approve_over_machine_reject(self) -> None:
        plan = _machine_reject_plan()
        queue = submit_plan_for_review(plan)
        with self.assertRaisesRegex(PermissionError, "cannot override"):
            queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)

    def test_decide_cannot_approve_over_compliance_block(self) -> None:
        plan = _compliance_block_plan()
        queue = submit_plan_for_review(plan)
        with self.assertRaisesRegex(PermissionError, "compliance block"):
            queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)


class PlanFileTests(unittest.TestCase):
    def test_plan_file_round_trip(self) -> None:
        plan = build_reference_plan()
        with tempfile.TemporaryDirectory() as directory:
            path = write_plan_file(plan, Path(directory) / "plan.json")
            loaded = load_plan_file(path)
        self.assertEqual(loaded, plan)
        self.assertEqual(loaded.plan_hash, plan.plan_hash)

    def test_plan_file_refuses_non_paper_environment(self) -> None:
        plan = build_reference_plan()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            write_plan_file(plan, path)
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["environment"] = "live"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-paper"):
                load_plan_file(path)

    def test_plan_file_refuses_unknown_schema(self) -> None:
        plan = build_reference_plan()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            write_plan_file(plan, path)
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["schema_version"] = "paper-plan-file-9.9.9"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported plan file schema"):
                load_plan_file(path)

    def test_tampered_plan_file_fails_integrity_on_decide(self) -> None:
        plan = build_reference_plan()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            write_plan_file(plan, path)
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["plan"]["spread"]["net_credit"] = "999.99"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = load_plan_file(path)
            queue = submit_plan_for_review(loaded)
            with self.assertRaisesRegex(PermissionError, "integrity check failed"):
                queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)

    def test_machine_risk_status_tamper_fails_integrity_on_decide(self) -> None:
        # Guard-bypass regression test: flipping machine_risk_status
        # FAIL->PASS in the plan file must break the plan hash. Otherwise a
        # hand-edited file would let a human approve a machine-rejected plan.
        plan = _machine_reject_plan()
        self.assertEqual(plan.machine_risk_status, MachineRiskStatus.REJECT)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            write_plan_file(plan, path)
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["plan"]["machine_risk_status"] = "pass"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = load_plan_file(path)
            queue = submit_plan_for_review(loaded)
            with self.assertRaisesRegex(PermissionError, "integrity check failed"):
                queue.decide(plan.plan_id, "captain", DECIDED_AT, approve=True)


class PaperReviewCliTests(unittest.TestCase):
    def _run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, "-m", "hedge_desk.cli", *argv],
            capture_output=True, text=True, check=False,
        )

    def test_cli_paper_review_lists_pending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan, path = _plan_file(directory)
            result = self._run_cli("--paper-review", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        pending = json.loads(result.stdout)["pending"]
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["plan_id"], plan.plan_id)
        self.assertEqual(pending[0]["plan_hash"], plan.plan_hash)
        self.assertEqual(pending[0]["machine_risk_status"], "pass")

    def test_cli_paper_decide_approves(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan, path = _plan_file(directory)
            result = self._run_cli(
                "--paper-decide", str(path),
                "--human-id", "captain",
                "--decided-at", DECIDED_AT.isoformat(),
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)
        self.assertEqual(decision["plan_id"], plan.plan_id)
        self.assertEqual(decision["plan_hash"], plan.plan_hash)
        self.assertEqual(decision["status"], "approved")
        self.assertEqual(decision["human_id"], "captain")
        self.assertEqual(decision["environment"], "paper")

    def test_cli_paper_decide_rejects_with_reason_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan, path = _plan_file(directory)
            result = self._run_cli(
                "--paper-decide", str(path),
                "--human-id", "captain",
                "--decided-at", DECIDED_AT.isoformat(),
                "--reject",
                "--reason-codes", "THESIS_INVALIDATED,VOL_TOO_RICH",
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)
        self.assertEqual(decision["status"], "rejected")
        self.assertEqual(
            decision["reason_codes"], ["THESIS_INVALIDATED", "VOL_TOO_RICH"]
        )

    def test_cli_paper_decide_persists_approval_to_plan_file(self) -> None:
        # The runner only opens plans whose FILE says APPROVED, so the CLI
        # must write the decision back — otherwise review dead-ends.
        with tempfile.TemporaryDirectory() as directory:
            plan, path = _plan_file(directory)
            result = self._run_cli(
                "--paper-decide", str(path),
                "--human-id", "captain",
                "--decided-at", DECIDED_AT.isoformat(),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            reloaded = load_plan_file(path)
        self.assertEqual(
            reloaded.authorization.status, HumanAuthorizationStatus.APPROVED
        )
        self.assertEqual(reloaded.authorization.human_id, "captain")

    def test_cli_paper_decide_persists_rejection_to_plan_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan, path = _plan_file(directory)
            result = self._run_cli(
                "--paper-decide", str(path),
                "--human-id", "captain",
                "--decided-at", DECIDED_AT.isoformat(),
                "--reject",
                "--reason-codes", "THESIS_INVALIDATED",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            reloaded = load_plan_file(path)
        self.assertEqual(
            reloaded.authorization.status, HumanAuthorizationStatus.REJECTED
        )

    def test_cli_paper_decide_requires_human_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, path = _plan_file(directory)
            result = self._run_cli("--paper-decide", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--human-id", result.stderr)

    def test_cli_paper_decide_reject_requires_reason_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, path = _plan_file(directory)
            result = self._run_cli(
                "--paper-decide", str(path),
                "--human-id", "captain",
                "--decided-at", DECIDED_AT.isoformat(),
                "--reject",
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reason code", result.stderr)

    def test_cli_refuses_non_paper_plan_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, path = _plan_file(directory)
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["environment"] = "live"
            path.write_text(json.dumps(raw), encoding="utf-8")
            review = self._run_cli("--paper-review", str(path))
            decide = self._run_cli(
                "--paper-decide", str(path), "--human-id", "captain"
            )
        self.assertNotEqual(review.returncode, 0)
        self.assertNotEqual(decide.returncode, 0)
        self.assertIn("non-paper", review.stderr)


if __name__ == "__main__":
    unittest.main()
