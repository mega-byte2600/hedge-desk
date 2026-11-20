"""Honest data health for /api/health and /api/health/data.

`/api/health` is the Render liveness probe, so it must keep answering 200 with
``status: ok`` while the process is up. Liveness is not data health. Before this
module, the endpoint said "ok" even when the nightly batch was REJECTED and the
Cboe chain was BLOCKED (2026-11-19). This module reports data health separately,
from the latest nightly artifact, re-scored with the current quality rules.

Pure and deterministic: pass the report dict and a timezone-aware ``now``.
No network, no orders, no probabilities, no Risk of Ruin.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from hedge_desk.data_quality import (
    SEV_DOWN,
    SEV_MISSING,
    SEV_OK,
    SEV_STALE,
    quality_report,
)

HEALTH_VERSION = "hedge-desk-data-health-1.0.0"

GREEN = "GREEN"
AMBER = "AMBER"
RED = "RED"

# The nightly batch runs every evening (launchd, about 20:55 PT). Allow one
# missed run plus margin before the artifact itself counts as stale.
MAX_ARTIFACT_AGE = timedelta(hours=36)

_SEVERITY_TO_STATUS = {
    SEV_OK: GREEN,
    SEV_STALE: AMBER,
    SEV_DOWN: RED,
    SEV_MISSING: RED,
}
_STATUS_RANK = {GREEN: 0, AMBER: 1, RED: 2}


def _parse_ts(value: object) -> Optional[datetime]:
    if not isinstance(value, str) or not value:
        return None
    try:
        ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return ts if ts.tzinfo is not None else None


def _worst(statuses: List[str]) -> str:
    worst = GREEN
    for s in statuses:
        if _STATUS_RANK[s] > _STATUS_RANK[worst]:
            worst = s
    return worst


def build_data_health(report: Optional[Dict], now: datetime) -> Dict[str, object]:
    """Score the latest nightly report as GREEN, AMBER, or RED with reasons."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    if not isinstance(report, dict) or not report:
        return {
            "schema_version": HEALTH_VERSION,
            "status": RED,
            "reasons": ["ARTIFACT_MISSING"],
            "summary": "No nightly report is available, so data health is unknown.",
            "components": [],
            "trade_authorized": False,
        }

    reasons: List[str] = []
    components: List[Dict[str, str]] = []

    generated = _parse_ts(report.get("generated_at"))
    if generated is None:
        artifact_status = RED
        reasons.append("ARTIFACT_TIMESTAMP_INVALID")
        age_hours = None
    else:
        age = now - generated
        age_hours = round(age.total_seconds() / 3600, 1)
        if age > MAX_ARTIFACT_AGE:
            artifact_status = RED
            reasons.append("ARTIFACT_STALE")
        else:
            artifact_status = GREEN
    components.append({
        "source": "Nightly batch artifact",
        "status": artifact_status,
        "message": (
            f"Generated {age_hours} h ago" if age_hours is not None else "Generated time unknown"
        ),
    })

    quality = quality_report(report, as_of=now.date())
    for alert in quality["alerts"]:
        status = _SEVERITY_TO_STATUS.get(alert["severity"], RED)
        components.append({
            "source": alert["source"],
            "status": status,
            "message": alert["message"],
            "detail": alert.get("detail", ""),
        })
        if status != GREEN:
            reasons.append(f"{alert['source']}={alert['severity']}")

    context = report.get("market_context") or {}
    sources = context.get("sources") if isinstance(context, dict) else None
    if isinstance(sources, dict):
        items = list(sources.items())
    elif isinstance(sources, list):
        items = [(s.get("provider_id", "?"), s) for s in sources if isinstance(s, dict)]
    else:
        items = []
    if items:
        counts: Dict[str, int] = {}
        blocked: List[str] = []
        for pid, src in items:
            st = src.get("status") if isinstance(src, dict) else str(src)
            counts[st] = counts.get(st, 0) + 1
            if st == "BLOCKED":
                blocked.append(str(pid))
        # Context feeds are supporting evidence, not the desk's primary data:
        # a blocked context feed is AMBER, never silently GREEN.
        ctx_status = AMBER if blocked else GREEN
        components.append({
            "source": "Market context feeds",
            "status": ctx_status,
            "message": ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
            "detail": f"Blocked: {', '.join(sorted(blocked))}." if blocked else "",
        })
        if blocked:
            reasons.append("MARKET_CONTEXT_PARTIAL")

    status = _worst([c["status"] for c in components])
    red = [c["source"] for c in components if c["status"] == RED]
    amber = [c["source"] for c in components if c["status"] == AMBER]
    if status == GREEN:
        summary = "All monitored data sources are healthy."
    else:
        parts = []
        if red:
            parts.append("RED: " + ", ".join(red))
        if amber:
            parts.append("AMBER: " + ", ".join(amber))
        summary = "; ".join(parts) + "."
    return {
        "schema_version": HEALTH_VERSION,
        "status": status,
        "reasons": reasons,
        "summary": summary,
        "artifact_generated_at": report.get("generated_at"),
        "artifact_age_hours": age_hours,
        "components": components,
        "quality_schema_version": quality["schema_version"],
        "trade_authorized": False,
    }
