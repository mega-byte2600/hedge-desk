"""Deterministic option-contract and spread calculations."""

from .spreads import (
    CONTRACT_MULTIPLIER,
    SPREAD_MODEL_ID,
    SPREAD_MODEL_VERSION,
    OptionQuote,
    OptionType,
    UnderlyingQuote,
    VerticalCreditSpread,
    VerticalSpreadCalculation,
    calculate_vertical_credit_spread,
)
from .events import (
    CorporateEventType,
    EventCalendarGate,
    ScheduledCorporateEvent,
    evaluate_event_calendar,
)
from .snapshot import (
    OPTION_SNAPSHOT_SCHEMA_VERSION,
    OptionSnapshot,
    parse_option_snapshot,
)
from .scanner import (
    SpreadPairEvaluation,
    SpreadScanPolicy,
    SpreadScanResult,
    scan_vertical_credit_spreads,
)
from .handoff import (
    CANDIDATE_HANDOFF_SCHEMA_VERSION,
    CandidateControlHandoff,
    build_candidate_control_handoffs,
    validate_candidate_control_handoff,
)
from .session import (
    MARKET_SESSION_SCHEMA_VERSION,
    MarketSessionEvidence,
    MarketSessionGate,
    evaluate_market_session,
    parse_market_session_evidence,
)
from .universe import (
    OptionUniverseEvaluation,
    RankedOptionCandidate,
    evaluate_option_universe,
)

__all__ = [
    "CONTRACT_MULTIPLIER",
    "SPREAD_MODEL_ID",
    "SPREAD_MODEL_VERSION",
    "OptionQuote",
    "OptionType",
    "UnderlyingQuote",
    "VerticalCreditSpread",
    "VerticalSpreadCalculation",
    "calculate_vertical_credit_spread",
    "CorporateEventType",
    "EventCalendarGate",
    "ScheduledCorporateEvent",
    "evaluate_event_calendar",
    "OPTION_SNAPSHOT_SCHEMA_VERSION",
    "OptionSnapshot",
    "parse_option_snapshot",
    "SpreadPairEvaluation",
    "SpreadScanPolicy",
    "SpreadScanResult",
    "scan_vertical_credit_spreads",
    "CANDIDATE_HANDOFF_SCHEMA_VERSION",
    "CandidateControlHandoff",
    "build_candidate_control_handoffs",
    "validate_candidate_control_handoff",
    "MarketSessionEvidence",
    "MarketSessionGate",
    "MARKET_SESSION_SCHEMA_VERSION",
    "evaluate_market_session",
    "parse_market_session_evidence",
    "OptionUniverseEvaluation", "RankedOptionCandidate", "evaluate_option_universe",
]
