"""Canonical report hashing and fail-closed publication validation."""

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict, Mapping, Tuple


PROHIBITED_PERFORMANCE_CLAIMS = (
    "guaranteed profit",
    "sure pick",
    "risk-free profit",
    "easy money",
)


@dataclass(frozen=True)
class PublicationDecision:
    publishable: bool
    reason_codes: Tuple[str, ...]


def canonical_report_bytes(report: Mapping[str, Any]) -> bytes:
    payload = {key: value for key, value in report.items() if key != "report_sha256"}
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def finalize_report(report: Mapping[str, Any]) -> Dict[str, Any]:
    finalized = dict(report)
    finalized["report_sha256"] = sha256(canonical_report_bytes(finalized)).hexdigest()
    return finalized


def validate_report(report: Mapping[str, Any]) -> PublicationDecision:
    reasons = []
    expected_hash = sha256(canonical_report_bytes(report)).hexdigest()
    if report.get("report_sha256") != expected_hash:
        reasons.append("REPORT_HASH_INVALID")
    if report.get("report_type") != "paper_hypothetical_morning_evaluation":
        reasons.append("HYPOTHETICAL_LABEL_REQUIRED")
    if report.get("environment") != "paper" or report.get("live_orders_enabled") is not False:
        reasons.append("PAPER_ONLY_BOUNDARY_REQUIRED")
    if report.get("real_money_pnl") != "0" or report.get("real_trades_executed") != 0:
        reasons.append("REAL_PERFORMANCE_CLAIM_BLOCKED")
    if not report.get("complete"):
        reasons.append("INCOMPLETE_REPORT")
    if not report.get("limitations"):
        reasons.append("REQUIRED_LIMITATIONS_MISSING")
    replay = report.get("chronological_replay", {})
    if not isinstance(replay, dict) or replay.get("valid") is not True:
        reasons.append("REPLAY_LINEAGE_INVALID")
    audit = report.get("audit_chain", {})
    if not isinstance(audit, dict) or audit.get("valid") is not True:
        reasons.append("AUDIT_CHAIN_INVALID")
    batch = report.get("data_batch", {})
    if (
        not isinstance(batch, dict)
        or batch.get("status") != "READY_FOR_RESEARCH"
        or not isinstance(batch.get("manifest_sha256"), str)
        or len(batch.get("manifest_sha256", "")) != 64
    ):
        reasons.append("DATA_BATCH_NOT_READY")
    stat = report.get("stat_evaluation", {})
    if (
        not isinstance(stat, dict)
        or stat.get("label") != "STAT"
        or stat.get("source") != "synthetic_fixture"
        or stat.get("p_value") is not None
        or stat.get("confidence_interval") is not None
        or stat.get("inference_status") != "INSUFFICIENT_SAMPLE"
    ):
        reasons.append("STAT_DISCLOSURE_INVALID")
    war_games = report.get("war_games", {})
    if (
        not isinstance(war_games, dict)
        or war_games.get("source") != "synthetic_fixture"
        or war_games.get("all_declared_scenarios_included") is not True
    ):
        reasons.append("WAR_GAME_DISCLOSURE_INVALID")
    manifest = war_games.get("fixture_manifest", {}) if isinstance(war_games, dict) else {}
    if (
        not isinstance(manifest, dict)
        or manifest.get("scenario_count") != 28
        or not isinstance(manifest.get("fixture_sha256"), str)
        or len(manifest.get("fixture_sha256", "")) != 64
    ):
        reasons.append("WAR_GAME_MANIFEST_INVALID")
    portfolio_stress = report.get("portfolio_stress", {})
    stress_hash_valid = False
    if isinstance(portfolio_stress, dict):
        stress_payload = {
            key: value
            for key, value in portfolio_stress.items()
            if key != "stress_report_sha256"
        }
        stress_hash_valid = portfolio_stress.get("stress_report_sha256") == sha256(
            json.dumps(
                stress_payload, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
    if (
        not isinstance(portfolio_stress, dict)
        or portfolio_stress.get("report_type")
        != "synthetic_hypothetical_portfolio_stress"
        or portfolio_stress.get("source") != "synthetic_fixture"
        or portfolio_stress.get("scenario_count") != 5
        or portfolio_stress.get("inference_status")
        != "INSUFFICIENT_SYNTHETIC_SAMPLE"
        or portfolio_stress.get("real_money_pnl") != "0"
        or not isinstance(portfolio_stress.get("fixture_sha256"), str)
        or len(portfolio_stress.get("fixture_sha256", "")) != 64
        or not isinstance(portfolio_stress.get("stress_report_sha256"), str)
        or len(portfolio_stress.get("stress_report_sha256", "")) != 64
        or not stress_hash_valid
    ):
        reasons.append("PORTFOLIO_STRESS_DISCLOSURE_INVALID")
    serialized = json.dumps(report, sort_keys=True).lower()
    if any(claim in serialized for claim in PROHIBITED_PERFORMANCE_CLAIMS):
        reasons.append("PROHIBITED_PERFORMANCE_CLAIM")
    reason_codes = tuple(sorted(set(reasons)))
    return PublicationDecision(not reason_codes, reason_codes)


def compare_morning_reports(
    previous: Mapping[str, Any], current: Mapping[str, Any]
) -> Dict[str, Any]:
    """Return a deterministic, non-performance-claiming delta between valid reports."""
    previous_decision = validate_report(previous)
    current_decision = validate_report(current)
    if not previous_decision.publishable or not current_decision.publishable:
        raise ValueError("report comparison requires two publishable reports")

    previous_projects = {
        project["project_id"]: project["disposition"] for project in previous["projects"]
    }
    current_projects = {
        project["project_id"]: project["disposition"] for project in current["projects"]
    }
    project_ids = sorted(set(previous_projects) | set(current_projects))
    disposition_changes = [
        {
            "project_id": project_id,
            "previous": previous_projects.get(project_id, "ABSENT"),
            "current": current_projects.get(project_id, "ABSENT"),
        }
        for project_id in project_ids
        if previous_projects.get(project_id) != current_projects.get(project_id)
    ]

    def war_summary(report: Mapping[str, Any]) -> Mapping[str, Any]:
        return report["war_games"]["summary"]

    def premium_metrics(report: Mapping[str, Any]) -> Mapping[str, Any]:
        return war_summary(report)["premium_fixed_trade"]["descriptive_metrics"]

    comparison = {
        "comparison_type": "paper_hypothetical_run_delta",
        "previous_report_sha256": previous["report_sha256"],
        "current_report_sha256": current["report_sha256"],
        "real_money_pnl_change": "0",
        "real_trades_executed_change": 0,
        "project_disposition_changes": disposition_changes,
        "war_game_changes": {
            "scenario_count": {
                "previous": war_summary(previous)["total_scenario_count"],
                "current": war_summary(current)["total_scenario_count"],
            },
            "no_trade_control_count": {
                "previous": war_summary(previous)["no_trade_control_count"],
                "current": war_summary(current)["no_trade_control_count"],
            },
            "fixture_sha256_changed": previous["war_games"]["fixture_manifest"][
                "fixture_sha256"
            ]
            != current["war_games"]["fixture_manifest"]["fixture_sha256"],
        },
        "synthetic_premium_metric_changes": {
            metric: {
                "previous": premium_metrics(previous)[metric],
                "current": premium_metrics(current)[metric],
            }
            for metric in ("total_pnl", "maximum_drawdown", "expected_shortfall")
        },
    }
    comparison["comparison_sha256"] = sha256(
        json.dumps(comparison, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return comparison


def render_morning_markdown(report: Mapping[str, Any]) -> str:
    """Render a concise human control report only after publication validation."""
    decision = validate_report(report)
    if not decision.publishable:
        raise ValueError(
            "morning report is not publishable: " + ",".join(decision.reason_codes)
        )
    summary = report["summary"]
    war_games = report["war_games"]
    war_summary = war_games["summary"]
    premium = war_summary["premium_fixed_trade"]
    metrics = premium["descriptive_metrics"]
    portfolio_stress = report["portfolio_stress"]
    stress_metrics = portfolio_stress["descriptive_metrics"]
    projects = report["projects"]
    premium_project = next(
        project for project in projects if project["project_id"] == "overnight-premium-desk"
    )
    premium_layers = {layer["layer"]: layer for layer in premium_project["layers"]}
    lines = [
        "# Hedge Desk Morning Evaluation",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Actual status",
        "",
        f"- Real money P&L: ${report['real_money_pnl']}",
        f"- Real trades executed: {report['real_trades_executed']}",
        "- Environment: PAPER / HYPOTHETICAL",
        "- Live orders enabled: false",
        "",
        "## Project evaluation",
        "",
        "| Project | Disposition |",
        "|---|---|",
    ]
    lines.extend(
        f"| {project['project_id']} | {project['disposition']} |"
        for project in projects
    )
    lines.extend(
        [
            "",
            "## Synthetic war games",
            "",
            f"- Total declared scenarios: {war_summary['total_scenario_count']}",
            f"- NO_TRADE controls: {war_summary['no_trade_control_count']}",
            f"- Premium profitable stresses: {premium['profitable_scenarios']}",
            f"- Premium losing stresses: {premium['losing_scenarios']}",
            f"- Premium synthetic total P&L: ${metrics['total_pnl']}",
            f"- Premium synthetic maximum drawdown: ${metrics['maximum_drawdown']}",
            f"- Premium synthetic expected shortfall: ${metrics['expected_shortfall']}",
            f"- Inference status: {metrics['inference_status']}",
            f"- STAT Brier score: {report['stat_evaluation']['brier_score']}",
            f"- STAT inference: {report['stat_evaluation']['inference_status']}",
            f"- STAT p-value: {report['stat_evaluation']['p_value']}",
            f"- STAT 95% CI: {report['stat_evaluation']['confidence_interval']}",
            f"- BIG proposal (agent research): {premium_layers['BIG']['metrics']['proposal']}",
            f"- Deterministic risk model: {premium_layers['DETERMINISTIC_RISK']['metrics']['risk_model_id']} {premium_layers['DETERMINISTIC_RISK']['metrics']['risk_model_version']}",
            f"- Validated risk-input artifact: `{premium_layers['DETERMINISTIC_RISK']['metrics']['risk_input_artifact']}`",
            "",
            "## Combined-MVP capital stress",
            "",
            f"- Synthetic scenarios: {portfolio_stress['scenario_count']}",
            f"- Starting synthetic capital: ${portfolio_stress['starting_capital']}",
            f"- Synthetic total P&L: ${stress_metrics['total_pnl']}",
            f"- Synthetic maximum drawdown: ${stress_metrics['maximum_drawdown']}",
            f"- Inference status: {portfolio_stress['inference_status']}",
            "",
            "## Control verification",
            "",
            f"- Data batch: {report['data_batch']['status']}",
            f"- Chronological replay valid: {str(report['chronological_replay']['valid']).lower()}",
            f"- Audit chain valid: {str(report['audit_chain']['valid']).lower()}",
            f"- Report SHA-256: `{report['report_sha256']}`",
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    return "\n".join(lines) + "\n"
