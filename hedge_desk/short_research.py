"""Evidence-completeness gates for Desk 5 short-sale research.

This module prepares research for review. It does not score, recommend, size,
locate, authorize, or execute a short sale.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from urllib.parse import urlparse
from typing import Tuple


class ShortResearchStatus(str, Enum):
    INCOMPLETE_RESEARCH = "INCOMPLETE_RESEARCH"
    READY_FOR_INDEPENDENT_REVIEW = "READY_FOR_INDEPENDENT_REVIEW"


@dataclass(frozen=True)
class SourceReference:
    source_type: str
    label: str
    url: str
    published_at: datetime


@dataclass(frozen=True)
class ShortResearchCase:
    symbol: str
    as_of: datetime
    bear_thesis: str
    sources: Tuple[SourceReference, ...]
    catalyst_and_timing: str
    counter_thesis: str
    valuation_basis: str
    liquidity_and_volatility: str
    borrow_status: str
    invalidation_conditions: str
    conflicts_disclosed: bool


@dataclass(frozen=True)
class ShortResearchReview:
    status: ShortResearchStatus
    reason_codes: Tuple[str, ...]
    borrow_confirmed: bool
    trade_authorized: bool = False


REQUIRED_TEXT_FIELDS = (
    ("bear_thesis", "BEAR_THESIS_MISSING"),
    ("catalyst_and_timing", "CATALYST_OR_TIMING_MISSING"),
    ("counter_thesis", "COUNTER_THESIS_MISSING"),
    ("valuation_basis", "VALUATION_BASIS_MISSING"),
    ("liquidity_and_volatility", "LIQUIDITY_OR_VOLATILITY_CONTEXT_MISSING"),
    ("invalidation_conditions", "THESIS_INVALIDATION_MISSING"),
)


def review_short_research(case: ShortResearchCase) -> ShortResearchReview:
    """Check whether a short thesis has enough disclosed evidence for human review."""
    if not isinstance(case, ShortResearchCase):
        raise TypeError("case must be a ShortResearchCase")
    reasons = []
    if not isinstance(case.as_of, datetime) or case.as_of.tzinfo is None:
        reasons.append("RESEARCH_AS_OF_NOT_TIMEZONE_AWARE")
    if not case.symbol or case.symbol.strip() != case.symbol:
        reasons.append("SYMBOL_INVALID")
    for field, code in REQUIRED_TEXT_FIELDS:
        value = getattr(case, field)
        if not isinstance(value, str) or not value.strip():
            reasons.append(code)
    if not case.conflicts_disclosed:
        reasons.append("CONFLICTS_NOT_REVIEWED")

    valid_sources = []
    for source in case.sources:
        parsed = urlparse(source.url)
        if (parsed.scheme != "https" or not parsed.netloc or not source.label.strip()
                or not isinstance(source.published_at, datetime)
                or source.published_at.tzinfo is None):
            reasons.append("SOURCE_REFERENCE_INVALID")
            continue
        if isinstance(case.as_of, datetime) and case.as_of.tzinfo and source.published_at > case.as_of:
            reasons.append("SOURCE_AFTER_RESEARCH_AS_OF")
            continue
        valid_sources.append(source)
    if not any(s.source_type == "SEC_FILING" for s in valid_sources):
        reasons.append("SEC_FILING_EVIDENCE_MISSING")
    if not any(s.source_type == "SHORT_INTEREST_REPORT" for s in valid_sources):
        reasons.append("DATED_SHORT_INTEREST_REPORT_MISSING")
    if not any(s.source_type in {"INDEPENDENT_SOURCE", "REGULATORY_SOURCE"} for s in valid_sources):
        reasons.append("INDEPENDENT_CORROBORATION_MISSING")

    borrow_confirmed = case.borrow_status == "BROKER_CONFIRMED"
    # Borrow is an execution-side fact, not a prerequisite for surfacing a research lead.
    if case.borrow_status not in {"BROKER_CONFIRMED", "UNAVAILABLE", "UNKNOWN", "NOT_CHECKED"}:
        reasons.append("BORROW_STATUS_INVALID")
    if borrow_confirmed and not any(s.source_type == "BROKER_BORROW_QUOTE" for s in valid_sources):
        reasons.append("BROKER_BORROW_EVIDENCE_MISSING")
    status = (ShortResearchStatus.READY_FOR_INDEPENDENT_REVIEW if not reasons
              else ShortResearchStatus.INCOMPLETE_RESEARCH)
    return ShortResearchReview(status, tuple(dict.fromkeys(reasons)), borrow_confirmed)
