"""Research and approval events on the tamper-evident trail.

The membership trail recorded who joined, subscribed, or was invited. The domain weight
says records and supervisory review are where the obligation actually sits, so the same
append-only hash chain now carries the research decisions too: which gate cleared, who
reviewed, and with what inputs.

Design: this is a thin, validating facade over ``MembershipAuditLog``. It does not
reimplement the chain — the chain is already correct and verified by its own tests — it
enforces the *shape* of research events so a review cannot be recorded with no actor, and
so every decision carries reason codes and enough context to reproduce it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

# Event names are a closed set: an unrecognised research event is a bug, not a new feature,
# and a free-text event would make the trail unauditable.
REVIEW_RECORDED = "research_review_recorded"
GATE_CLEARED = "research_gate_cleared"
GATE_BLOCKED = "research_gate_blocked"
REPORT_PUBLISHED = "research_report_published"

RESEARCH_EVENTS = frozenset({REVIEW_RECORDED, GATE_CLEARED, GATE_BLOCKED, REPORT_PUBLISHED})


@dataclass(frozen=True)
class ResearchEvent:
    """A research or approval event, validated before it reaches the chain."""

    event: str
    subject: str          # what the decision was about (candidate, desk, or report id)
    actor: str            # who made it; a review with no actor is not a record
    reason_codes: Sequence[str]
    detail: str = ""

    def __post_init__(self) -> None:
        if self.event not in RESEARCH_EVENTS:
            raise ValueError(f"unrecognised research event: {self.event!r}")
        if not str(self.subject).strip():
            raise ValueError("a research event needs a subject")
        if not str(self.actor).strip():
            raise ValueError("a research event needs an actor; an anonymous review is not a record")
        if not self.reason_codes:
            raise ValueError("every research decision must retain reason codes")

    def as_detail(self) -> str:
        """The detail string stored on the chain: reproducible and machine-readable."""
        codes = ",".join(str(c) for c in self.reason_codes)
        return f"subject={self.subject}; codes={codes}; detail={self.detail}".strip()


class ResearchAudit:
    """Append research events to the same append-only, hash-chained trail as membership."""

    def __init__(self, audit) -> None:
        if audit is None:
            raise ValueError("an audit log is required")
        self._audit = audit

    def record(self, event: ResearchEvent) -> dict:
        return self._audit.record(event.event, event.subject, actor=event.actor, detail=event.as_detail())

    # Convenience wrappers, so callers express intent rather than raw event names.
    def review(self, subject: str, actor: str, reason_codes: Sequence[str], detail: str = "") -> dict:
        return self.record(ResearchEvent(REVIEW_RECORDED, subject, actor, reason_codes, detail))

    def gate_cleared(self, subject: str, actor: str, reason_codes: Sequence[str], detail: str = "") -> dict:
        return self.record(ResearchEvent(GATE_CLEARED, subject, actor, reason_codes, detail))

    def gate_blocked(self, subject: str, actor: str, reason_codes: Sequence[str], detail: str = "") -> dict:
        return self.record(ResearchEvent(GATE_BLOCKED, subject, actor, reason_codes, detail))

    def report_published(self, subject: str, actor: str, reason_codes: Sequence[str], detail: str = "") -> dict:
        return self.record(ResearchEvent(REPORT_PUBLISHED, subject, actor, reason_codes, detail))

    def entries(self, limit: int = 500) -> list[dict]:
        return self._audit.entries(limit)

    def verify(self) -> list[str]:
        """Empty list means the chain is intact."""
        return self._audit.verify()


def default_research_audit() -> Optional[ResearchAudit]:
    """Build from the environment, or ``None`` when no audit backend is configured.

    Returning ``None`` rather than a silent in-memory stand-in keeps the fail-closed
    posture: callers must decide what an unconfigured audit means for them.
    """
    from hedge_desk.membership_audit import default_audit_log

    log = default_audit_log()
    return ResearchAudit(log) if log is not None else None


__all__ = [
    "GATE_BLOCKED",
    "GATE_CLEARED",
    "REPORT_PUBLISHED",
    "RESEARCH_EVENTS",
    "REVIEW_RECORDED",
    "ResearchAudit",
    "ResearchEvent",
    "default_research_audit",
]
