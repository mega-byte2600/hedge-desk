"""Shared paper-research candidate contract for web and iOS clients."""

from dataclasses import asdict, dataclass
from typing import Dict, Tuple

CANDIDATE_SCHEMA_VERSION = "hedge-desk-candidates-1.0.0"

@dataclass(frozen=True)
class ResearchCandidate:
    desk_id: str
    symbol: str
    instrument_type: str
    stage: str
    method: str
    evidence_needed: str
    trade_authorized: bool = False

SEED_CANDIDATES: Tuple[ResearchCandidate, ...] = (
    ResearchCandidate("overnight-premium-desk", "SPY", "ETF_OPTIONS", "AWAITING_CURRENT_CHAIN", "Defined-risk premium after liquidity, volatility, event, and executable-spread checks.", "Current option chain, volatility surface, calendar, and executable bid/ask."),
    ResearchCandidate("overnight-premium-desk", "QQQ", "ETF_OPTIONS", "AWAITING_CURRENT_CHAIN", "Defined-risk premium after liquidity, volatility, event, and executable-spread checks.", "Current option chain, volatility surface, calendar, and executable bid/ask."),
    ResearchCandidate("earnings-event-desk", "AAPL", "EQUITY_OPTIONS", "AWAITING_EVENT_EVIDENCE", "Earnings surprise versus point-in-time expectations, followed by observed price reaction.", "Confirmed event, frozen consensus, release, and post-release reaction."),
    ResearchCandidate("earnings-event-desk", "NVDA", "EQUITY_OPTIONS", "AWAITING_EVENT_EVIDENCE", "Earnings surprise versus point-in-time expectations, followed by observed price reaction.", "Confirmed event, frozen consensus, release, and post-release reaction."),
    ResearchCandidate("arbitrage-observer", "SPX", "INDEX_OPTIONS", "AWAITING_EXECUTABLE_QUOTES", "Put-call parity or box dislocation after spreads, fees, settlement, and financing.", "Synchronized quotes, settlement terms, fees, and financing cost."),
    ResearchCandidate("arbitrage-observer", "XSP", "INDEX_OPTIONS", "AWAITING_EXECUTABLE_QUOTES", "Put-call parity or box dislocation after spreads, fees, settlement, and financing.", "Synchronized quotes, settlement terms, fees, and financing cost."),
    ResearchCandidate("dividend-opportunity-desk", "KO", "EQUITY", "AWAITING_FUNDAMENTALS", "Dividend durability, payout capacity, shareholder yield, and valuation.", "Point-in-time payouts, cash flow, issuance, buybacks, price, and valuation."),
    ResearchCandidate("dividend-opportunity-desk", "JNJ", "EQUITY", "AWAITING_FUNDAMENTALS", "Dividend durability, payout capacity, shareholder yield, and valuation.", "Point-in-time payouts, cash flow, issuance, buybacks, price, and valuation."),
    ResearchCandidate("open-quant-ai-model-lab", "SPY", "ETF", "AWAITING_OOS_SCORE", "Independent quant and AI hypotheses with leakage-controlled out-of-sample tests.", "Versioned features, purged walk-forward result, costs, and model quorum."),
    ResearchCandidate("open-quant-ai-model-lab", "QQQ", "ETF", "AWAITING_OOS_SCORE", "Independent quant and AI hypotheses with leakage-controlled out-of-sample tests.", "Versioned features, purged walk-forward result, costs, and model quorum."),
    ResearchCandidate("event-futures-desk", "CL", "FUTURES_ROOT", "AWAITING_PHYSICAL_EVENT", "Physical weather, war, or logistics surprise compared with the futures curve.", "Validated event, current curve, basis, roll, margin, liquidity, and costs."),
    ResearchCandidate("event-futures-desk", "NG", "FUTURES_ROOT", "AWAITING_PHYSICAL_EVENT", "Physical weather, war, or logistics surprise compared with the futures curve.", "Validated event, current curve, basis, roll, margin, liquidity, and costs."),
    ResearchCandidate("event-futures-desk", "ZW", "FUTURES_ROOT", "AWAITING_PHYSICAL_EVENT", "Physical weather, war, or logistics surprise compared with the futures curve.", "Validated event, current curve, basis, roll, margin, liquidity, and costs."),
)

def build_candidate_feed() -> Dict[str, object]:
    return {
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "mode": "PAPER_RESEARCH_ONLY",
        "candidate_definition": "SEED_UNIVERSE_NOT_METHOD_QUALIFIED",
        "candidates": [asdict(candidate) for candidate in SEED_CANDIDATES],
    }
