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
    war_games = report.get("war_games", {})
    if (
        not isinstance(war_games, dict)
        or war_games.get("source") != "synthetic_fixture"
        or war_games.get("all_declared_scenarios_included") is not True
    ):
        reasons.append("WAR_GAME_DISCLOSURE_INVALID")
    serialized = json.dumps(report, sort_keys=True).lower()
    if any(claim in serialized for claim in PROHIBITED_PERFORMANCE_CLAIMS):
        reasons.append("PROHIBITED_PERFORMANCE_CLAIM")
    reason_codes = tuple(sorted(set(reasons)))
    return PublicationDecision(not reason_codes, reason_codes)
