"""Normalize authoritative multi-asset feeds into nightly research context.

This module is deliberately read-only. It converts the free/open provider
adapters into a compact, schema-versioned object that can be embedded in the
nightly report and rendered by web/iOS clients. Credentials remain server-side;
no secret, access token, account data, PII, or PHI is returned.
"""

from __future__ import annotations

import os
from typing import Callable, Dict, Mapping, Sequence

from hedge_desk.data.open_market_feeds import (
    OpenFeedResult,
    cftc_cot,
    eia_v2,
    finra_fixed_income,
    nyfed_reference_rates,
    treasury_latest_auctions,
)

MARKET_CONTEXT_SCHEMA = "hedge-desk-market-context-1.0.0"


def _pick(row: Mapping[str, object], keys: Sequence[str]) -> Dict[str, object]:
    return {key: row[key] for key in keys if key in row and row[key] not in (None, "")}


def _live(result: OpenFeedResult, observations: object) -> Dict[str, object]:
    return {
        "provider_id": result.provider_id,
        "dataset": result.dataset,
        "status": "LIVE",
        "observation_count": result.row_count,
        "observations": observations,
    }


def _blocked(provider_id: str, reason_code: str) -> Dict[str, object]:
    return {
        "provider_id": provider_id,
        "status": "BLOCKED",
        "observation_count": 0,
        "reason_code": reason_code,
    }


def _unconfigured(provider_id: str) -> Dict[str, object]:
    return {
        "provider_id": provider_id,
        "status": "UNCONFIGURED",
        "observation_count": 0,
        "reason_code": "CREDENTIALS_NOT_CONFIGURED",
    }


def _nyfed_summary(result: OpenFeedResult) -> Dict[str, object]:
    rates: Dict[str, object] = {}
    for row in result.rows:
        name = str(row.get("type", "")).upper()
        if name not in {"SOFR", "EFFR", "OBFR", "TGCR", "BGCR"}:
            continue
        item = _pick(
            row,
            (
                "percentRate",
                "effectiveDate",
                "publicationDate",
                "volumeInBillions",
                "revisionIndicator",
            ),
        )
        if item:
            rates[name] = item
    return rates


def _treasury_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "auction_date",
        "issue_date",
        "maturity_date",
        "security_type",
        "security_term",
        "high_investment_rate",
        "high_yield",
        "total_tendered",
        "total_accepted",
    )
    return [_pick(row, keys) for row in result.rows[:5]]


def _eia_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "period",
        "value",
        "units",
        "series-description",
        "product-name",
        "process-name",
        "area-name",
    )
    return [_pick(row, keys) for row in result.rows[:5]]


def _cftc_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "market_and_exchange_names",
        "report_date_as_yyyy_mm_dd",
        "open_interest_all",
        "dealer_positions_long_all",
        "dealer_positions_short_all",
        "asset_mgr_positions_long",
        "asset_mgr_positions_short",
        "lev_money_positions_long",
        "lev_money_positions_short",
    )
    return [_pick(row, keys) for row in result.rows[:10]]


def _finra_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    # FINRA dataset field names evolve. Preserve only common breadth/date fields
    # when present instead of coupling the report to a provider-specific schema.
    keys = (
        "date",
        "weekStartDate",
        "productCategory",
        "marketSegment",
        "advances",
        "declines",
        "unchanged",
        "advancePercent",
        "declinePercent",
        "advancesPercent",
        "declinesPercent",
    )
    return [_pick(row, keys) for row in result.rows[:10]]


def build_market_context(
    *,
    nyfed_fetch: Callable[..., OpenFeedResult] = nyfed_reference_rates,
    treasury_fetch: Callable[..., OpenFeedResult] = treasury_latest_auctions,
    cftc_fetch: Callable[..., OpenFeedResult] = cftc_cot,
    eia_fetch: Callable[..., OpenFeedResult] = eia_v2,
    finra_fetch: Callable[..., OpenFeedResult] = finra_fixed_income,
) -> Dict[str, object]:
    """Build fail-closed cross-asset context from authoritative provider APIs."""

    sources: Dict[str, Dict[str, object]] = {}

    try:
        result = nyfed_fetch()
        sources["nyfed-markets"] = _live(result, _nyfed_summary(result))
    except Exception:
        sources["nyfed-markets"] = _blocked("nyfed-markets", "UPSTREAM_OR_PARSE_FAILURE")

    try:
        result = treasury_fetch(limit=5)
        sources["treasury-fiscaldata"] = _live(result, _treasury_summary(result))
    except Exception:
        sources["treasury-fiscaldata"] = _blocked(
            "treasury-fiscaldata", "UPSTREAM_OR_PARSE_FAILURE"
        )

    try:
        result = cftc_fetch(report="tff_futures_only", limit=25)
        sources["cftc-cot"] = _live(result, _cftc_summary(result))
    except Exception:
        sources["cftc-cot"] = _blocked("cftc-cot", "UPSTREAM_OR_PARSE_FAILURE")

    if os.environ.get("EIA_API_KEY", "").strip():
        try:
            result = eia_fetch("petroleum/stoc/wstk", data=("value",), limit=5)
            sources["eia-open-data"] = _live(result, _eia_summary(result))
        except Exception:
            sources["eia-open-data"] = _blocked(
                "eia-open-data", "UPSTREAM_OR_AUTH_FAILURE"
            )
    else:
        sources["eia-open-data"] = _unconfigured("eia-open-data")

    finra_configured = bool(
        os.environ.get("FINRA_CLIENT_ID", "").strip()
        and os.environ.get("FINRA_CLIENT_SECRET", "").strip()
    )
    if finra_configured:
        try:
            result = finra_fetch("corporateMarketBreadth", limit=10)
            sources["finra"] = _live(result, _finra_summary(result))
        except Exception:
            sources["finra"] = _blocked("finra", "UPSTREAM_OR_AUTH_FAILURE")
    else:
        sources["finra"] = _unconfigured("finra")

    live = sum(1 for item in sources.values() if item.get("status") == "LIVE")
    blocked = sum(1 for item in sources.values() if item.get("status") == "BLOCKED")
    unconfigured = sum(
        1 for item in sources.values() if item.get("status") == "UNCONFIGURED"
    )

    return {
        "schema_version": MARKET_CONTEXT_SCHEMA,
        "status": "LIVE" if live and not blocked else ("DEGRADED" if live else "BLOCKED"),
        "live_sources": live,
        "blocked_sources": blocked,
        "unconfigured_sources": unconfigured,
        "sources": sources,
        "trade_authorized": False,
    }


__all__ = ["MARKET_CONTEXT_SCHEMA", "build_market_context"]
