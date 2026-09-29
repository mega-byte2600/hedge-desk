"""Normalize authoritative multi-asset feeds into nightly research context.

This module is deliberately read-only. It converts the free/open provider
adapters into a compact, schema-versioned object that can be embedded in the
nightly report and rendered by web/iOS clients. Credentials remain server-side;
no secret, access token, account data, PII, or PHI is returned.
"""

from __future__ import annotations

import os
from datetime import date, timedelta
from typing import Callable, Dict, Mapping, Sequence

from hedge_desk.data.open_market_feeds import (
    OpenFeedResult,
    bank_of_canada_fx,
    bls_latest_series,
    cftc_cot,
    ecb_exchange_rates,
    fdic_failures,
    imf_gdp_growth,
    nasdaq_earnings_calendar,
    nasdaq_quote,
    treasury_yield_curve,
    world_bank_indicator,
    eia_v2,
    finra_fixed_income,
    nyfed_reference_rates,
    treasury_latest_auctions,
)
from hedge_desk.data.institutional_feeds import (
    bis_global_liquidity,
    coinbase_product_trades,
    finra_equity,
)
from hedge_desk.data.public_signal_feeds import (
    bea_nipa_table,
    nws_active_alerts,
    usda_nass_crop_progress,
)
from hedge_desk.rates_desk import fred_series_rows

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


def _blocked(provider_id: str, reason_code: str, detail: str | None = None) -> Dict[str, object]:
    result = {
        "provider_id": provider_id,
        "status": "BLOCKED",
        "observation_count": 0,
        "reason_code": reason_code,
    }
    if detail:
        import re

        clean = re.sub(
            r"(api_key|apikey|token|userid|key)=[^&\s]+",
            r"\1=[REDACTED]",
            detail,
            flags=re.IGNORECASE,
        )
        result["detail"] = clean[:200]
    return result


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


def _treasury_curve_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    latest: Dict[str, Dict[str, object]] = {}
    for row in result.rows:
        tenor = str(row.get("tenor", ""))
        if tenor and (
            tenor not in latest
            or str(row.get("date", "")) > str(latest[tenor].get("date", ""))
        ):
            latest[tenor] = _pick(row, ("tenor", "date", "value"))
    return [latest[tenor] for tenor in sorted(latest)]


def _fdic_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = ("NAME", "CERT", "FIN", "CITYST", "FAILDATE", "SAVR", "RESTYPE1")
    return [_pick(row, keys) for row in result.rows[:10]]


def _world_bank_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = ("indicator", "country", "countryiso3code", "date", "value", "unit")
    return [_pick(row, keys) for row in result.rows[:10]]


def _bis_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "TIME_PERIOD",
        "OBS_VALUE",
        "TITLE",
        "UNIT_MEASURE",
        "CURRENCY",
        "BORROWERS_CTY",
        "series_alias",
    )
    return [_pick(row, keys) for row in result.rows[:12]]


def _coinbase_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = ("time", "trade_id", "product_id", "price", "size", "side")
    return [_pick(row, keys) for row in result.rows[:100]]


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


def _bls_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    return [
        _pick(row, ("seriesID", "year", "period", "periodName", "value", "latest"))
        for row in result.rows[:5]
    ]


def _ecb_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    return [_pick(row, ("currency", "rate", "date", "base")) for row in result.rows[:10]]


def _imf_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    return [_pick(row, ("date", "value", "indicator", "country")) for row in result.rows[-10:]]


def _boc_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    return [_pick(row, ("date", "series", "value")) for row in result.rows[-10:]]


def _nws_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "id",
        "event",
        "severity",
        "certainty",
        "urgency",
        "headline",
        "areaDesc",
        "sent",
        "effective",
        "expires",
    )
    return [_pick(row, keys) for row in result.rows[:25]]


def _bea_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "TableName",
        "LineNumber",
        "LineDescription",
        "TimePeriod",
        "DataValue",
        "UNIT_MULT",
        "CL_UNIT",
    )
    return [_pick(row, keys) for row in result.rows[:25]]


def _usda_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "commodity_desc",
        "statisticcat_desc",
        "unit_desc",
        "short_desc",
        "Value",
        "year",
        "week_ending",
        "state_alpha",
        "agg_level_desc",
        "domain_desc",
    )
    return [_pick(row, keys) for row in result.rows[:25]]


def _nasdaq_quote_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    return [
        _pick(
            row,
            (
                "symbol",
                "assetClass",
                "lastSalePrice",
                "netChange",
                "percentageChange",
                "lastTradeTimestamp",
                "isRealTime",
                "bidPrice",
                "askPrice",
            ),
        )
        for row in result.rows
    ]


def _nasdaq_earnings_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = ("symbol", "name", "marketCap", "time", "epsForecast", "noOfEsts", "calendarDate")
    return [_pick(row, keys) for row in result.rows[:25]]


def _finra_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
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


def _finra_equity_summary(result: OpenFeedResult) -> list[Dict[str, object]]:
    keys = (
        "tradeReportDate",
        "securitiesInformationProcessorSymbolIdentifier",
        "shortParQuantity",
        "shortExemptParQuantity",
        "totalParQuantity",
        "marketCode",
        "settlementDate",
        "symbolCode",
        "currentShortPositionQuantity",
        "previousShortPositionQuantity",
        "changePercent",
        "daysToCoverQuantity",
    )
    return [_pick(row, keys) for row in result.rows[:25]]


def build_market_context(
    *,
    nyfed_fetch: Callable[..., OpenFeedResult] = nyfed_reference_rates,
    treasury_fetch: Callable[..., OpenFeedResult] = treasury_latest_auctions,
    cftc_fetch: Callable[..., OpenFeedResult] = cftc_cot,
    bls_fetch: Callable[..., OpenFeedResult] = bls_latest_series,
    treasury_curve_fetch: Callable[..., OpenFeedResult] = treasury_yield_curve,
    fdic_fetch: Callable[..., OpenFeedResult] = fdic_failures,
    world_bank_fetch: Callable[..., OpenFeedResult] = world_bank_indicator,
    bis_fetch: Callable[..., OpenFeedResult] = bis_global_liquidity,
    ecb_fetch: Callable[..., OpenFeedResult] = ecb_exchange_rates,
    nws_fetch: Callable[..., OpenFeedResult] = nws_active_alerts,
    bea_fetch: Callable[..., OpenFeedResult] = bea_nipa_table,
    usda_fetch: Callable[..., OpenFeedResult] = usda_nass_crop_progress,
    eia_fetch: Callable[..., OpenFeedResult] = eia_v2,
    finra_fetch: Callable[..., OpenFeedResult] = finra_fixed_income,
    finra_equity_fetch: Callable[..., OpenFeedResult] = finra_equity,
    fred_fetch: Callable[..., object] = fred_series_rows,
    nasdaq_quote_fetch: Callable[..., OpenFeedResult] = nasdaq_quote,
    nasdaq_earn_fetch: Callable[..., OpenFeedResult] = nasdaq_earnings_calendar,
    coinbase_fetch: Callable[..., OpenFeedResult] = coinbase_product_trades,
    imf_fetch: Callable[..., OpenFeedResult] = imf_gdp_growth,
    boc_fetch: Callable[..., OpenFeedResult] = bank_of_canada_fx,
    watchlist: Sequence[str] = ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA"),
) -> Dict[str, object]:
    """Build fail-closed cross-asset context from authoritative provider APIs."""

    sources: Dict[str, Dict[str, object]] = {}

    try:
        end = date.today()
        rows = fred_fetch("DFF", end - timedelta(days=14), end)
        if not rows:
            raise ValueError("empty FRED series")
        sources["fred"] = {
            "provider_id": "fred",
            "dataset": "DFF",
            "status": "LIVE",
            "observation_count": len(rows),
            "observations": [
                {"date": str(day), "value": str(value)} for day, value in rows[-5:]
            ],
        }
    except Exception as exc:
        sources["fred"] = _blocked("fred", "UPSTREAM_OR_AUTH_FAILURE", str(exc))

    try:
        result = nyfed_fetch()
        sources["nyfed-markets"] = _live(result, _nyfed_summary(result))
    except Exception as exc:
        sources["nyfed-markets"] = _blocked(
            "nyfed-markets", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    try:
        result = treasury_fetch(limit=5)
        sources["treasury-fiscaldata"] = _live(result, _treasury_summary(result))
    except Exception as exc:
        sources["treasury-fiscaldata"] = _blocked(
            "treasury-fiscaldata", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    try:
        result = treasury_curve_fetch()
        sources["treasury-rates"] = _live(result, _treasury_curve_summary(result))
    except Exception as exc:
        sources["treasury-rates"] = _blocked(
            "treasury-rates", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    try:
        result = fdic_fetch(limit=10)
        sources["fdic"] = _live(result, _fdic_summary(result))
    except Exception as exc:
        sources["fdic"] = _blocked("fdic", "UPSTREAM_OR_PARSE_FAILURE", str(exc))

    try:
        result = world_bank_fetch("NY.GDP.MKTP.CD", country="USA", per_page=5)
        sources["world-bank"] = _live(result, _world_bank_summary(result))
    except Exception as exc:
        sources["world-bank"] = _blocked(
            "world-bank", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    try:
        result = bis_fetch(series="usd_credit_nonbanks_ex_us_yoy", limit=8)
        sources["bis"] = _live(result, _bis_summary(result))
    except Exception as exc:
        sources["bis"] = _blocked("bis", "UPSTREAM_OR_PARSE_FAILURE", str(exc))

    try:
        result = bls_fetch("CUUR0000SA0")
        sources["bls"] = _live(result, _bls_summary(result))
    except Exception as exc:
        sources["bls"] = _blocked("bls", "UPSTREAM_OR_PARSE_FAILURE", str(exc))

    try:
        result = ecb_fetch(("USD", "JPY", "GBP", "CHF"))
        sources["ecb-fx"] = _live(result, _ecb_summary(result))
    except Exception as exc:
        sources["ecb-fx"] = _blocked("ecb-fx", "UPSTREAM_OR_PARSE_FAILURE", str(exc))

    try:
        result = imf_fetch(country="USA")
        sources["imf"] = _live(result, _imf_summary(result))
    except Exception as exc:
        sources["imf"] = _blocked("imf", "UPSTREAM_OR_PARSE_FAILURE", str(exc))

    try:
        result = boc_fetch(series="FXUSDCAD")
        sources["bank-of-canada"] = _live(result, _boc_summary(result))
    except Exception as exc:
        sources["bank-of-canada"] = _blocked(
            "bank-of-canada", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    try:
        result = nws_fetch(limit=25)
        sources["nws"] = _live(result, _nws_summary(result))
    except Exception as exc:
        sources["nws"] = _blocked("nws", "UPSTREAM_OR_RATE_LIMIT", str(exc))

    try:
        result = cftc_fetch(report="tff_futures_only", limit=25)
        sources["cftc-cot"] = _live(result, _cftc_summary(result))
    except Exception as exc:
        sources["cftc-cot"] = _blocked(
            "cftc-cot", "UPSTREAM_OR_PARSE_FAILURE", str(exc)
        )

    if os.environ.get("BEA_API_KEY", "").strip():
        try:
            result = bea_fetch("T10101", frequency="Q", year="X", limit=25)
            sources["bea"] = _live(result, _bea_summary(result))
        except Exception as exc:
            sources["bea"] = _blocked("bea", "UPSTREAM_OR_AUTH_FAILURE", str(exc))
    else:
        sources["bea"] = _unconfigured("bea")

    if os.environ.get("USDA_NASS_API_KEY", "").strip():
        try:
            result = usda_fetch("CORN", year=date.today().year, limit=25)
            sources["usda-nass"] = _live(result, _usda_summary(result))
        except Exception as exc:
            sources["usda-nass"] = _blocked(
                "usda-nass", "UPSTREAM_OR_AUTH_FAILURE", str(exc)
            )
    else:
        sources["usda-nass"] = _unconfigured("usda-nass")

    if os.environ.get("EIA_API_KEY", "").strip():
        try:
            result = eia_fetch("petroleum/stoc/wstk", data=("value",), limit=5)
            sources["eia-open-data"] = _live(result, _eia_summary(result))
        except Exception as exc:
            sources["eia-open-data"] = _blocked(
                "eia-open-data", "UPSTREAM_OR_AUTH_FAILURE", str(exc)
            )
    else:
        sources["eia-open-data"] = _unconfigured("eia-open-data")

    finra_configured = bool(
        os.environ.get("FINRA_CLIENT_ID", "").strip()
        and os.environ.get("FINRA_CLIENT_SECRET", "").strip()
    )
    if finra_configured:
        try:
            fixed_income = finra_fetch("corporateMarketBreadth", limit=10)
            equity_flow = finra_equity_fetch("reg_sho_daily", limit=25)
            sources["finra"] = {
                "provider_id": "finra",
                "dataset": "fixed-income-and-equity-flow",
                "status": "LIVE",
                "observation_count": fixed_income.row_count + equity_flow.row_count,
                "observations": {
                    "fixed_income": _finra_summary(fixed_income),
                    "reg_sho_daily": _finra_equity_summary(equity_flow),
                },
            }
        except Exception as exc:
            sources["finra"] = _blocked("finra", "UPSTREAM_OR_AUTH_FAILURE", str(exc))
    else:
        sources["finra"] = _unconfigured("finra")

    try:
        result = nasdaq_quote_fetch(tuple(watchlist))
        sources["nasdaq-quotes"] = _live(result, _nasdaq_quote_summary(result))
    except Exception as exc:
        sources["nasdaq-quotes"] = _blocked(
            "nasdaq-quotes", "UPSTREAM_OR_RATE_LIMIT", str(exc)
        )

    try:
        result = nasdaq_earn_fetch(date.today() + timedelta(days=1))
        sources["nasdaq-earnings"] = _live(result, _nasdaq_earnings_summary(result))
    except Exception as exc:
        sources["nasdaq-earnings"] = _blocked(
            "nasdaq-earnings", "UPSTREAM_OR_RATE_LIMIT", str(exc)
        )

    try:
        result = coinbase_fetch("BTC-USD", limit=100)
        sources["coinbase-exchange"] = _live(result, _coinbase_summary(result))
    except Exception as exc:
        sources["coinbase-exchange"] = _blocked(
            "coinbase-exchange", "UPSTREAM_OR_RATE_LIMIT", str(exc)
        )

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