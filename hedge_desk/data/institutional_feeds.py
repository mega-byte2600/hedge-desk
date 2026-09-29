"""Institutional research feeds that complement the core open-market adapters.

This module adds read-only, fail-closed access to public global-liquidity and
market-structure data. It never places orders, authorizes trades, or computes
Risk of Ruin.
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import urllib.parse
import urllib.request
from typing import Mapping, Tuple

from .open_market_feeds import (
    FINRA_DATA_URL,
    OpenFeedResult,
    RequestTransport,
    Transport,
    _default_request_transport,
    _finra_oauth_token,
    _fetch_request_json,
)

BIS_DATA_URL = "https://stats.bis.org/api/v2/data/dataflow/BIS/{flow}/{version}/{key}"
COINBASE_TRADES_URL = "https://api.exchange.coinbase.com/products/{product_id}/trades"

# Vetted BIS global-liquidity series used as macro/credit context. Keep this
# allowlist small so callers cannot turn the adapter into an arbitrary proxy.
BIS_GLOBAL_LIQUIDITY_SERIES: Mapping[str, Tuple[str, str, str]] = {
    "usd_credit_nonbanks_ex_us_yoy": (
        "WS_GLI",
        "1.0",
        "Q.USD.3P.N.A.I.B.771",
    ),
    "usd_bank_credit_em_usd": (
        "WS_GLI",
        "1.0",
        "Q.USD.4T.N.B.I.G.USD",
    ),
    "global_bank_credit_pct_gdp": (
        "WS_GLI",
        "1.0",
        "Q.TO1.5J.A.B.I.A.770",
    ),
}

FINRA_EQUITY_DATASETS: Mapping[str, Tuple[str, str]] = {
    "consolidated_short_interest": ("otcMarket", "consolidatedShortInterest"),
    "reg_sho_daily": ("otcMarket", "regShoDaily"),
}

_PRODUCT_RE = re.compile(r"^[A-Z0-9]{2,12}-[A-Z0-9]{2,12}$")


def _positive_limit(limit: int, maximum: int) -> int:
    if type(limit) is not int or not 1 <= limit <= maximum:
        raise ValueError(f"limit must be an integer from 1 to {maximum}")
    return limit


def _default_bis_transport(url: str) -> Tuple[int, bytes]:
    user_agent = os.environ.get(
        "MARKET_DATA_USER_AGENT",
        "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
    ).strip()
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": user_agent,
        },
    )
    return _default_request_transport(req)


def _default_coinbase_transport(url: str) -> Tuple[int, bytes]:
    user_agent = os.environ.get(
        "MARKET_DATA_USER_AGENT",
        "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
    ).strip()
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    return _default_request_transport(req)


def bis_global_liquidity(
    series: str = "usd_credit_nonbanks_ex_us_yoy",
    limit: int = 8,
    transport: Transport = _default_bis_transport,
) -> OpenFeedResult:
    """Fetch a vetted BIS global-liquidity series (no API key required)."""
    if series not in BIS_GLOBAL_LIQUIDITY_SERIES:
        raise ValueError(f"unsupported BIS global-liquidity series: {series}")
    limit = _positive_limit(limit, 100)
    flow, version, key = BIS_GLOBAL_LIQUIDITY_SERIES[series]
    query = urllib.parse.urlencode({"format": "csv", "lastNObservations": str(limit)})
    url = f"{BIS_DATA_URL.format(flow=flow, version=version, key=key)}?{query}"
    status, raw = transport(url)
    if status != 200 or not raw:
        raise ValueError(f"bis fetch failed (status {status})")
    try:
        text = raw.decode("utf-8-sig")
        rows = list(csv.DictReader(io.StringIO(text)))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ValueError("bis returned malformed CSV") from exc
    if not rows:
        raise ValueError("bis payload has no observations")
    required = {"TIME_PERIOD", "OBS_VALUE"}
    normalized = []
    for row in rows:
        if not required.issubset(row) or not row.get("TIME_PERIOD") or row.get("OBS_VALUE") in (None, ""):
            raise ValueError("bis observation is missing required fields")
        item = dict(row)
        item["series_alias"] = series
        normalized.append(item)
    return OpenFeedResult(
        provider_id="bis",
        dataset=f"{flow}:{series}",
        rows=tuple(normalized),
    )


def coinbase_product_trades(
    product_id: str = "BTC-USD",
    limit: int = 100,
    transport: Transport = _default_coinbase_transport,
) -> OpenFeedResult:
    """Fetch the latest public Coinbase Exchange spot trades for one product."""
    product = product_id.strip().upper()
    if not _PRODUCT_RE.fullmatch(product):
        raise ValueError("invalid Coinbase product id")
    limit = _positive_limit(limit, 1000)
    url = COINBASE_TRADES_URL.format(product_id=urllib.parse.quote(product, safe="-"))
    url = f"{url}?{urllib.parse.urlencode({'limit': str(limit)})}"
    status, raw = transport(url)
    if status != 200 or not raw:
        raise ValueError(f"coinbase-exchange fetch failed (status {status})")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("coinbase-exchange returned malformed JSON") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError("coinbase-exchange payload has no trades")
    rows = []
    required = {"trade_id", "side", "size", "price", "time"}
    for trade in payload:
        if not isinstance(trade, dict) or not required.issubset(trade):
            raise ValueError("coinbase-exchange trade row is malformed")
        if trade.get("side") not in {"buy", "sell"}:
            raise ValueError("coinbase-exchange trade side is invalid")
        row = {field: trade[field] for field in ("time", "trade_id", "price", "size", "side")}
        row["product_id"] = product
        rows.append(row)
    return OpenFeedResult(
        provider_id="coinbase-exchange",
        dataset=f"spot-trades:{product}",
        rows=tuple(rows),
    )


def finra_equity(
    dataset: str,
    limit: int = 50,
    request_transport: RequestTransport = _default_request_transport,
    access_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> OpenFeedResult:
    """Fetch a vetted FINRA equity dataset through the existing OAuth seam."""
    if dataset not in FINRA_EQUITY_DATASETS:
        raise ValueError(f"unsupported FINRA equity dataset: {dataset}")
    limit = _positive_limit(limit, 5000)
    token = (access_token or "").strip() or _finra_oauth_token(
        request_transport,
        client_id=client_id,
        client_secret=client_secret,
    )
    group, dataset_name = FINRA_EQUITY_DATASETS[dataset]
    base = FINRA_DATA_URL.format(group=group, dataset=dataset_name)
    request = urllib.request.Request(
        f"{base}?{urllib.parse.urlencode({'limit': str(limit)})}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "hedge-desk/1.0 research",
        },
    )
    payload = _fetch_request_json(request, "finra-equity", request_transport)
    if not isinstance(payload, list):
        raise ValueError("finra-equity payload is not a row list")
    rows = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError("finra-equity row is not an object")
        rows.append(row)
    return OpenFeedResult(provider_id="finra", dataset=dataset, rows=tuple(rows))
