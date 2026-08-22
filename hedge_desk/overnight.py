"""Deterministic paper-only overnight evaluation and morning report."""

from datetime import datetime, timezone
from typing import Any, Dict, Tuple

from hedge_desk.data import DataArtifact, validate_data_artifact
from hedge_desk.data.contracts import sha256_text
from hedge_desk.demo import FIXTURE_AS_OF, FIXTURE_ID, build_reference_plan, json_value
from hedge_desk.evaluation import (
    Disposition,
    EvaluationLayer,
    EvaluationStatus,
    LayerEvaluation,
    ProjectEvaluation,
)
from hedge_desk.paper import HumanAuthorizationStatus, MachineRiskStatus
from hedge_desk.backoffice import BackOfficeStatus
from hedge_desk.projects import MVP_PROJECTS, ProjectStatus, validate_project_registry
from hedge_desk.wargames import build_war_game_report
from hedge_desk.replay import build_replay_evaluation


OVERNIGHT_RUNNER_VERSION = "1.0.0"


def _reference_artifact() -> DataArtifact:
    return DataArtifact(
        artifact_id="synthetic-option-chain-v1",
        payload_kind="option_chain",
        source_id="synthetic-fixture",
        license_id="repository-synthetic-fixture",
        source_as_of=FIXTURE_AS_OF,
        received_at=FIXTURE_AS_OF,
        payload_sha256=sha256_text("TEST-95-90-PUT-CREDIT|2026-07-28T20:00:00Z"),
        synthetic=True,
        redistribution_allowed=True,
    )


def _inactive_project(project_id: str, evaluated_at: datetime) -> ProjectEvaluation:
    layers = tuple(
        LayerEvaluation(
            layer=layer,
            status=EvaluationStatus.NOT_IMPLEMENTED,
            reason_codes=("PROJECT_NOT_IMPLEMENTED",),
            metrics={},
        )
        for layer in EvaluationLayer
    )
    return ProjectEvaluation(project_id, evaluated_at, Disposition.NO_TRADE, layers)


def evaluate_reference_projects() -> Tuple[ProjectEvaluation, ...]:
    """Evaluate every registered project without inventing unbuilt strategies."""
    validate_project_registry()
    artifact = _reference_artifact()
    data_gate = validate_data_artifact(artifact, FIXTURE_AS_OF, maximum_age_seconds=0)
    plan = build_reference_plan()
    observed = LayerEvaluation(
        EvaluationLayer.OBSERVED,
        EvaluationStatus.PASS if data_gate.admissible else EvaluationStatus.BLOCKED,
        data_gate.reason_codes,
        {
            "synthetic": "true",
            "net_credit": str(plan.spread.net_credit),
            "maximum_loss": str(plan.spread.maximum_loss),
            "break_even": str(plan.spread.break_even),
        },
        (artifact.artifact_id,),
    )
    # No statistical inference is claimed by this executable-side reference case.
    stat = LayerEvaluation(
        EvaluationLayer.STAT,
        EvaluationStatus.NOT_REQUIRED,
        ("REFERENCE_ECONOMICS_ONLY",),
        {},
    )
    big = LayerEvaluation(
        EvaluationLayer.BIG,
        EvaluationStatus.PASS,
        (),
        {"proposal": "defined-risk synthetic put credit spread"},
        (FIXTURE_ID,),
    )
    risk_pass = plan.machine_risk_status is MachineRiskStatus.PASS
    risk = LayerEvaluation(
        EvaluationLayer.DETERMINISTIC_RISK,
        EvaluationStatus.PASS if risk_pass else EvaluationStatus.BLOCKED,
        plan.reason_codes,
        {
            "risk_artifact": plan.plan_hash,
            "risk_of_ruin": str(plan.risk_decision.risk_of_ruin_after),
        },
        (plan.plan_hash,),
    )
    compliance_pass = plan.compliance_decision.status is BackOfficeStatus.PASS
    compliance = LayerEvaluation(
        EvaluationLayer.DETERMINISTIC_COMPLIANCE,
        EvaluationStatus.PASS if compliance_pass else EvaluationStatus.BLOCKED,
        plan.compliance_decision.reason_codes,
        {"policy_version": plan.compliance_decision.policy_version},
        (plan.plan_hash,),
    )
    human_pending = plan.authorization.status is HumanAuthorizationStatus.PENDING
    human = LayerEvaluation(
        EvaluationLayer.HUMAN,
        EvaluationStatus.PENDING if human_pending else EvaluationStatus.BLOCKED,
        ("HUMAN_AUTHORIZATION_REQUIRED",) if human_pending else (),
        {},
        (plan.plan_hash,),
    )
    premium = ProjectEvaluation(
        MVP_PROJECTS[0].project_id,
        FIXTURE_AS_OF,
        Disposition.HUMAN_REVIEW
        if data_gate.admissible and risk_pass and compliance_pass
        else Disposition.NO_TRADE,
        (observed, stat, big, risk, compliance, human),
    )
    inactive = tuple(
        _inactive_project(project.project_id, FIXTURE_AS_OF)
        for project in MVP_PROJECTS[1:]
        if project.status is ProjectStatus.ARCHITECTURE_ONLY
    )
    return (premium,) + inactive


def build_morning_report(generated_at: datetime) -> Dict[str, Any]:
    if generated_at.tzinfo is None:
        raise ValueError("report timestamp must be timezone-aware")
    evaluations = evaluate_reference_projects()
    human_review = sum(
        evaluation.disposition is Disposition.HUMAN_REVIEW
        for evaluation in evaluations
    )
    no_trade = sum(
        evaluation.disposition is Disposition.NO_TRADE for evaluation in evaluations
    )
    return {
        "report_type": "paper_hypothetical_morning_evaluation",
        "runner_version": OVERNIGHT_RUNNER_VERSION,
        "generated_at": generated_at.isoformat(),
        "environment": "paper",
        "complete": True,
        "live_orders_enabled": False,
        "real_money_pnl": "0",
        "real_trades_executed": 0,
        "summary": {
            "projects_evaluated": len(evaluations),
            "human_review": human_review,
            "no_trade": no_trade,
        },
        "limitations": [
            "Synthetic fixtures only; no current market opportunity is claimed.",
            "Hypothetical paper output is not investment advice or a performance guarantee.",
            "Architecture-only projects correctly return NO_TRADE.",
        ],
        "projects": json_value(evaluations),
        "war_games": build_war_game_report(),
        "chronological_replay": build_replay_evaluation(),
    }


def current_morning_report() -> Dict[str, Any]:
    return build_morning_report(datetime.now(timezone.utc))
