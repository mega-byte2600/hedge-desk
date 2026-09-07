"""Candidate risk dashboard for the paper research surface."""

from collections import Counter
from typing import Dict, Mapping, Optional

from hedge_desk.candidates import build_candidate_feed


def build_candidate_risk_dashboard(candidate_feed: Optional[Mapping[str, object]] = None) -> Dict[str, object]:
    """Summarize research candidates without authorizing trades."""
    feed = candidate_feed or build_candidate_feed()
    candidates = list(feed.get("candidates", []))
    desk_counts = Counter(str(row.get("desk_id", "")) for row in candidates)
    stage_counts = Counter(str(row.get("stage", "")) for row in candidates)
    evidence_gaps = Counter(_evidence_lane(str(row.get("evidence_needed", ""))) for row in candidates)
    authorized = [row for row in candidates if row.get("trade_authorized") is True]
    high_attention = [
        row
        for row in candidates
        if str(row.get("stage", "")).startswith(("AWAITING_CURRENT", "AWAITING_EXECUTABLE", "AWAITING_PHYSICAL"))
    ]

    return {
        "schema_version": "hedge-desk-risk-dashboard-1.0.0",
        "mode": "PAPER_RESEARCH_ONLY",
        "trade_authorized_count": len(authorized),
        "live_orders_enabled": False,
        "candidate_count": len(candidates),
        "desk_count": len([desk for desk in desk_counts if desk]),
        "stage_counts": dict(sorted(stage_counts.items())),
        "desk_counts": dict(sorted(desk_counts.items())),
        "evidence_gaps": dict(sorted(evidence_gaps.items())),
        "attention_queue": [
            {
                "symbol": row.get("symbol"),
                "desk_id": row.get("desk_id"),
                "stage": row.get("stage"),
                "evidence_needed": row.get("evidence_needed"),
            }
            for row in high_attention[:6]
        ],
        "executive_actions": _executive_actions(evidence_gaps, len(authorized)),
    }


def _evidence_lane(text: str) -> str:
    lowered = text.lower()
    if "option chain" in lowered or "quotes" in lowered or "bid/ask" in lowered:
        return "market_microstructure"
    if "event" in lowered or "release" in lowered or "calendar" in lowered:
        return "event_validation"
    if "fundamentals" in lowered or "cash flow" in lowered or "valuation" in lowered:
        return "fundamental_validation"
    if "walk-forward" in lowered or "model" in lowered or "features" in lowered:
        return "model_validation"
    return "source_validation"


def _executive_actions(evidence_gaps: Counter, authorized_count: int) -> list:
    actions = []
    if authorized_count:
        actions.append("Remove trade authorization from candidate records before publication.")
    else:
        actions.append("Keep the web surface research-only: candidate feed shows zero trade-authorized records.")
    if evidence_gaps.get("market_microstructure"):
        actions.append("Prioritize executable bid/ask, option-chain, and liquidity evidence before any premium desk review.")
    if evidence_gaps.get("event_validation"):
        actions.append("Freeze event calendars and source timestamps for earnings, futures, and catalyst workflows.")
    if evidence_gaps.get("model_validation"):
        actions.append("Require out-of-sample model evidence before promoting any quant or AI idea.")
    if len(actions) < 4:
        actions.append("Use the attention queue as the morning research checklist for human review.")
    return actions[:4]
