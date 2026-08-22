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
        or manifest.get("scenario_count") != 17
        or not isinstance(manifest.get("fixture_sha256"), str)
        or len(manifest.get("fixture_sha256", "")) != 64
    ):
        reasons.append("WAR_GAME_MANIFEST_INVALID")
    serialized = json.dumps(report, sort_keys=True).lower()
    if any(claim in serialized for claim in PROHIBITED_PERFORMANCE_CLAIMS):
        reasons.append("PROHIBITED_PERFORMANCE_CLAIM")
    reason_codes = tuple(sorted(set(reasons)))
    return PublicationDecision(not reason_codes, reason_codes)


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
    projects = report["projects"]
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
