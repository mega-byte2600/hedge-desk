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


def build_real_eod_candidate_feed(
    report_path: str = "artifacts/am-report-latest.json",
) -> Dict[str, object]:
    """Serve the latest real-EOD premium candidates from the nightly AM report.

    Reads the content-addressed AM report written by ``hedge_desk.nightly`` and
    maps each premium candidate into the shared ResearchCandidate contract so the
    web console and iOS app can render real data. Fails closed: if the report is
    missing or unreadable, returns an empty feed with a clear reason — never
    fabricated candidates.
    """
    import json as _json
    from pathlib import Path as _Path

    path = _Path(report_path)
    if not path.is_file():
        return {
            "schema_version": CANDIDATE_SCHEMA_VERSION,
            "mode": "REAL_EOD",
            "candidate_definition": "NIGHTLY_REPORT_MISSING",
            "candidates": [],
            "reason": "am-report-latest.json not found; run the nightly orchestrator",
        }
    try:
        report = _json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, _json.JSONDecodeError):
        return {
            "schema_version": CANDIDATE_SCHEMA_VERSION,
            "mode": "REAL_EOD",
            "candidate_definition": "NIGHTLY_REPORT_UNREADABLE",
            "candidates": [],
            "reason": "am-report-latest.json unreadable",
        }
    candidates = []
    for item in report.get("candidates", []):
        candidates.append(
            {
                "desk_id": "overnight-premium-desk",
                "symbol": item.get("symbol", ""),
                "instrument_type": "EQUITY_OPTIONS",
                "stage": "REAL_EOD_CANDIDATE",
                "method": (
                    f"{item.get('strategy', '')} defined-risk premium; "
                    f"strike {item.get('strike', '')}; capital required "
                    f"${item.get('requirement', '')}"
                ),
                "evidence_needed": "Real option chain for executable premium",
                # Force False: the research feed never authorizes a trade. An
                # incoming true flag is data, not authority, and must never leak
                # through to a client as an executable signal.
                "trade_authorized": False,
            }
        )
    return {
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "mode": "REAL_EOD",
        "candidate_definition": "REAL_EOD_PREMIUM_CANDIDATES",
        "report_sha256": report.get("report_sha256", ""),
        "candidates": candidates,
    }


# ---------------------------------------------------------------------------
# Earnings-desk and macro-desk real-data feeds (Hermes handoff 2026-09-26)
#
# Same contract and fail-closed discipline as build_real_eod_candidate_feed:
# read the nightly AM report, map real observations into ResearchCandidate
# dicts, never fabricate. trade_authorized is always forced False.
# ---------------------------------------------------------------------------

# SEC EDGAR CIK -> ticker for watchlist names. Explicit and auditable; an
# unknown CIK falls back to the CIK itself rather than a guessed symbol.
CIK_TO_SYMBOL = {
    "0000320193": "AAPL",
    "0000789019": "MSFT",
    "0001045810": "NVDA",
    "0001318605": "TSLA",
}

_EARNINGS_SCHEMA = "hedge-desk-candidates-1.0.0"
_MACRO_SCHEMA = "hedge-desk-candidates-1.0.0"


def _read_nightly_report(report_path):
    """Return (report_dict, None) or (None, reason_string). Fail closed."""
    import json as _json
    from pathlib import Path as _Path

    path = _Path(report_path)
    if not path.is_file():
        return None, "am-report-latest.json not found; run the nightly orchestrator"
    try:
        return _json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, UnicodeError, _json.JSONDecodeError):
        return None, "am-report-latest.json unreadable"


def _missing_feed(schema, mode, definition, reason):
    return {
        "schema_version": schema,
        "mode": mode,
        "candidate_definition": definition,
        "candidates": [],
        "reason": reason,
    }


def build_earnings_candidate_feed(
    report_path: str = "artifacts/am-report-latest.json",
) -> Dict[str, object]:
    """Serve real earnings-desk research items from the nightly AM report.

    Maps each ``earnings_actuals`` entry with mode REAL_EDGAR_EARNINGS (real
    SEC EDGAR GAAP EPS actuals) into the shared candidate contract. Entries
    that are BLOCKED or malformed are skipped, never guessed. No consensus is
    fabricated: surprise is only mentioned when the desk computed it from a
    real supplied estimate.
    """
    report, reason = _read_nightly_report(report_path)
    if report is None:
        return _missing_feed(
            _EARNINGS_SCHEMA,
            "REAL_EDGAR",
            "NIGHTLY_REPORT_MISSING" if "not found" in reason else "NIGHTLY_REPORT_UNREADABLE",
            reason,
        )
    candidates = []
    for cik, entry in (report.get("earnings_actuals") or {}).items():
        if not isinstance(entry, dict) or entry.get("mode") != "REAL_EDGAR_EARNINGS":
            continue
        obs = entry.get("observation") or {}
        if not isinstance(obs, dict):
            continue
        symbol = CIK_TO_SYMBOL.get(str(cik), str(cik))
        fy_eps = obs.get("latest_fy_eps", "?")
        fy_period = obs.get("latest_fy_period", "?")
        q_eps = obs.get("latest_quarterly_eps", "?")
        q_period = obs.get("latest_quarterly_period", "?")
        pq_eps = obs.get("prior_quarterly_eps", "?")
        pq_period = obs.get("prior_quarterly_period", "?")
        method = (
            f"SEC EDGAR actuals (OBSERVED, point-in-time filings): FY EPS {fy_eps} "
            f"({fy_period}); latest quarterly EPS {q_eps} ({q_period}) vs prior "
            f"{pq_eps} ({pq_period}). Earnings surprise versus point-in-time "
            f"expectations, followed by observed price reaction."
        )
        candidates.append(
            {
                "desk_id": "earnings-event-desk",
                "symbol": symbol,
                "cik": str(cik),
                "instrument_type": "EQUITY",
                "stage": "REAL_EDGAR_EARNINGS",
                "method": method,
                "observation": {
                    "latest_quarterly_eps": q_eps,
                    "latest_quarterly_period": q_period,
                    "prior_quarterly_eps": pq_eps,
                    "prior_quarterly_period": pq_period,
                    "latest_fy_eps": fy_eps,
                    "latest_fy_period": fy_period,
                },
                "evidence_needed": (
                    "Confirmed event, frozen consensus, release, and post-release "
                    "reaction. Surprise is computed only when a real analyst "
                    "estimate is supplied — never fabricated."
                ),
                "data_source": entry.get("data_source", "sec-edgar"),
                # Force False: research input, never a trade signal.
                "trade_authorized": False,
            }
        )
    return {
        "schema_version": _EARNINGS_SCHEMA,
        "mode": "REAL_EDGAR",
        "candidate_definition": "REAL_EDGAR_EARNINGS_ACTUALS",
        "report_sha256": report.get("report_sha256", ""),
        "candidates": candidates,
    }


def build_macro_candidate_feed(
    report_path: str = "artifacts/am-report-latest.json",
) -> Dict[str, object]:
    """Serve real macro/rates research items from the nightly AM report.

    Maps real FRED observations (macro_environment / rates_environment) into
    the shared candidate contract as research watch items — macro backdrop
    for premium pricing and valuation discount rates, not trade signals.
    BLOCKED or missing sections yield an empty feed with a reason, never
    invented values.
    """
    report, reason = _read_nightly_report(report_path)
    if report is None:
        return _missing_feed(
            _MACRO_SCHEMA,
            "REAL_FRED",
            "NIGHTLY_REPORT_MISSING" if "not found" in reason else "NIGHTLY_REPORT_UNREADABLE",
            reason,
        )
    candidates = []

    def _add(desk_id, symbol, label, value, date, source, series):
        if value is None or date is None:
            return
        candidates.append(
            {
                "desk_id": desk_id,
                "symbol": symbol,
                "instrument_type": "MACRO_SERIES",
                "stage": "REAL_FRED_OBSERVATION",
                "method": (
                    f"{label}: {value}% as of {date} (FRED {series}, {source}). "
                    f"Macro backdrop for premium pricing and valuation discount "
                    f"rates — not a trade signal."
                ),
                "evidence_needed": f"Next FRED release for {series}.",
                "data_source": source,
                "trade_authorized": False,
            }
        )

    macro = report.get("macro_environment") or {}
    if isinstance(macro, dict) and macro.get("mode") == "REAL_FRED_MACRO":
        src = macro.get("data_source", "fred")
        _add("macro-rates-desk", "UNRATE", "Unemployment rate",
             macro.get("unemployment_rate_pct"), macro.get("unemployment_date"), src, "UNRATE")
        _add("macro-rates-desk", "DGS5", "5Y Treasury yield",
             macro.get("treasury_5y"), macro.get("treasury_5y_date"), src, "DGS5")
        _add("macro-rates-desk", "DGS30", "30Y Treasury yield",
             macro.get("treasury_30y"), macro.get("treasury_30y_date"), src, "DGS30")
    rates = report.get("rates_environment") or {}
    if isinstance(rates, dict) and rates.get("mode") == "REAL_FRED_RATES":
        src = rates.get("data_source", "fred")
        _add("macro-rates-desk", "FEDFUNDS", "Fed funds effective rate",
             rates.get("fed_funds_effective_rate"), rates.get("as_of"), src, "FEDFUNDS")
        _add("macro-rates-desk", "DGS10", "10Y Treasury yield",
             rates.get("treasury_10y_yield"), rates.get("as_of"), src, "DGS10")
    definition = "REAL_FRED_MACRO_OBSERVATIONS" if candidates else "FRED_SECTIONS_BLOCKED"
    feed = {
        "schema_version": _MACRO_SCHEMA,
        "mode": "REAL_FRED",
        "candidate_definition": definition,
        "report_sha256": report.get("report_sha256", ""),
        "candidates": candidates,
    }
    if not candidates:
        feed["reason"] = (
            "macro_environment and rates_environment are BLOCKED or missing in "
            "the latest nightly report; no values invented"
        )
    return feed
