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
]
