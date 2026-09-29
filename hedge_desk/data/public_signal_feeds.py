"""Authoritative public-signal adapters for weather, macro, and agriculture.

These adapters extend the Hedge Desk's zero/low-cost public data plane without
adding trade authority. Credentials are read only from server-side environment
variables, transport errors fail closed, and returned rows retain source fields
for downstream provenance.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from typing import Callable, Mapping, Tuple

from hedge_desk.data.open_market_feeds import OpenFeedResult


Transport = Callable[[urllib.request.Request], Tuple[int, bytes]]

NWS_API_URL = "https://api.weather.gov"
BEA_API_URL = "https://apps.bea.gov/api/data"
USDA_NASS_API_URL = "https://quickstats.nass.usda.gov/api/api_GET/"


def _default_transport(request: urllib.request.Request) -> Tuple[int, bytes]:
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _user_agent() -> str:
    return os.environ.get(
        "MARKET_DATA_USER_AGENT",
        "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
    ).strip()


def _json_request(
    url: str,
    provider: str,
    transport: Transport,
    *,
    retries: int = 2,
) -> object:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/geo+json, application/json",
            "User-Agent": _user_agent(),
        },
    )
    last_status = 0
    last_raw = b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(request)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            try:
                return json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                raise ValueError(f"{provider} returned malformed JSON") from exc
        last_status, last_raw = status, raw
        if not (status == 0 or status == 429 or 500 <= status < 600) or attempt == retries:
            break
        time.sleep(float(attempt + 1))
    detail = last_raw[:160].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={detail}")


def _positive_limit(limit: int, maximum: int = 500) -> int:
    if type(limit) is not int or limit < 1 or limit > maximum:
        raise ValueError(f"limit must be an integer from 1 to {maximum}")
    return limit


def nws_active_alerts(
    *,
    area: str | None = None,
    limit: int = 25,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch active National Weather Service alerts (no API key required).

    ``area`` may be a two-letter NWS area/state code. When omitted, the API
    returns active alerts nationally and the adapter caps the normalized result.
    """

    limit = _positive_limit(limit, 100)
    params = {"status": "actual", "message_type": "alert"}
    if area is not None:
        normalized = area.strip().upper()
        if len(normalized) != 2 or not normalized.isalpha():
            raise ValueError("NWS area must be a two-letter code")
        params["area"] = normalized
    url = f"{NWS_API_URL}/alerts/active?{urllib.parse.urlencode(params)}"
    payload = _json_request(url, "nws", transport)
    features = payload.get("features") if isinstance(payload, dict) else None
    if not isinstance(features, list):
        raise ValueError("nws payload has no features list")

    rows = []
    for feature in features[:limit]:
        if not isinstance(feature, dict):
            continue
        properties = feature.get("properties")
        if not isinstance(properties, dict):
            continue
        rows.append(
            {
                key: properties.get(key)
                for key in (
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
                    "status",
                    "messageType",
                )
                if properties.get(key) not in (None, "")
            }
        )
    return OpenFeedResult("nws", "active-alerts", tuple(rows))


def bea_nipa_table(
    table_name: str = "T10101",
    *,
    frequency: str = "Q",
    year: str = "X",
    api_key: str | None = None,
    limit: int = 50,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch a BEA NIPA table using a free server-side API key."""

    limit = _positive_limit(limit, 500)
    key = (api_key if api_key is not None else os.environ.get("BEA_API_KEY", "")).strip()
    if not key:
        raise ValueError("BEA_API_KEY is required")
    table = table_name.strip().upper()
    if not table or len(table) > 32 or not table.replace("_", "").isalnum():
        raise ValueError("invalid BEA table name")
    freq = frequency.strip().upper()
    if freq not in {"A", "Q", "M"}:
        raise ValueError("BEA frequency must be A, Q, or M")

    params = {
        "UserID": key,
        "method": "GetData",
        "datasetname": "NIPA",
        "TableName": table,
        "Frequency": freq,
        "Year": str(year),
        "ResultFormat": "JSON",
    }
    payload = _json_request(
        f"{BEA_API_URL}?{urllib.parse.urlencode(params)}", "bea", transport
    )
    root = payload.get("BEAAPI") if isinstance(payload, dict) else None
    results = root.get("Results") if isinstance(root, dict) else None
    if not isinstance(results, dict):
        raise ValueError("bea payload has no Results object")
    errors = results.get("Error")
    if errors:
        raise ValueError("bea API returned an error")
    data = results.get("Data")
    if not isinstance(data, list):
        raise ValueError("bea payload has no Data rows")
    rows = tuple(row for row in data[:limit] if isinstance(row, dict))
    return OpenFeedResult("bea", f"NIPA:{table}", rows)


def usda_nass_crop_progress(
    commodity: str = "CORN",
    *,
    year: int | None = None,
    state_alpha: str | None = None,
    api_key: str | None = None,
    limit: int = 50,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch USDA NASS Quick Stats weekly crop-condition/progress rows.

    The free NASS API key remains server-side. The query is intentionally narrow
    to avoid bulk extraction and to keep this adapter decision-oriented.
    """

    limit = _positive_limit(limit, 500)
    key = (
        api_key if api_key is not None else os.environ.get("USDA_NASS_API_KEY", "")
    ).strip()
    if not key:
        raise ValueError("USDA_NASS_API_KEY is required")
    crop = commodity.strip().upper()
    if not crop or len(crop) > 40 or not all(ch.isalnum() or ch in " -" for ch in crop):
        raise ValueError("invalid USDA commodity")
    query_year = year if year is not None else date.today().year
    if type(query_year) is not int or query_year < 1900 or query_year > date.today().year + 1:
        raise ValueError("invalid USDA year")

    params = {
        "key": key,
        "format": "JSON",
        "source_desc": "SURVEY",
        "sector_desc": "CROPS",
        "commodity_desc": crop,
        "freq_desc": "WEEKLY",
        "year": str(query_year),
    }
    if state_alpha is None:
        params["agg_level_desc"] = "NATIONAL"
    else:
        state = state_alpha.strip().upper()
        if len(state) != 2 or not state.isalpha():
            raise ValueError("USDA state_alpha must be a two-letter code")
        params["agg_level_desc"] = "STATE"
        params["state_alpha"] = state

    payload = _json_request(
        f"{USDA_NASS_API_URL}?{urllib.parse.urlencode(params)}",
        "usda-nass",
        transport,
    )
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list):
        raise ValueError("usda-nass payload has no data rows")
    rows = tuple(row for row in data[:limit] if isinstance(row, dict))
    return OpenFeedResult("usda-nass", f"weekly:{crop}", rows)


__all__ = [
    "BEA_API_URL",
    "NWS_API_URL",
    "USDA_NASS_API_URL",
    "bea_nipa_table",
    "nws_active_alerts",
    "usda_nass_crop_progress",
]
