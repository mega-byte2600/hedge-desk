"""Free/open authoritative market-data adapters for paper research.

The adapters in this module deliberately prefer regulators, government agencies,
and public market-structure datasets over scraped web pages or unlicensed feeds.
They are read-only, use the Python standard library, and fail closed on transport,
authentication, or payload errors.

No function in this module authorizes a trade or places an order.
"""

from __future__ import annotations

import base64
import csv
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence, Tuple


Transport = Callable[[str], Tuple[int, bytes]]
RequestTransport = Callable[[urllib.request.Request], Tuple[int, bytes]]

TREASURY_AUCTIONS_URL = (
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    "v1/accounting/od/auctions_query"
)
FINRA_DATA_URL = "https://api.finra.org/data/group/{group}/name/{dataset}"
FINRA_TOKEN_URL = (
    "https://ews.fip.finra.org/fip/rest/ews/oauth2/access_token"
    "?grant_type=client_credentials"
)
CFTC_SODA_URL = "https://publicreporting.cftc.gov/resource/{dataset}.json"
EIA_V2_URL = "https://api.eia.gov/v2/{route}/data/"
NYFED_LATEST_RATES_URL = "https://markets.newyorkfed.org/api/rates/all/latest.json"
NYFED_RATE_HISTORY_URL = "https://markets.newyorkfed.org/api/rates/{segment}/{rate}/last/{limit}.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
BLS_LATEST_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/{series}?latest=true"
ECB_EXR_URL = "https://data-api.ecb.europa.eu/service/data/EXR/{key}"

# Public FINRA fixed-income datasets that are directly useful to a rates/credit desk.
# FINRA public data is free, but its Query API requires a Public Credential and
# OAuth 2.0 bearer token. Client credentials must remain server-side.
FINRA_FIXED_INCOME_DATASETS = frozenset(
    {
        "treasuryDailyAggregates",
        "corporateMarketBreadth",
        "corporateMarketSentiment",
        "corporate144AMarketBreadth",
        "corporate144AMarketSentiment",
        "corporatesAndAgenciesCappedVolume",
        "agencyMarketBreadth",
        "agencyTbaPricing",
    }
)

# CFTC public-reporting Socrata view ids. The API exposes these views through
# /resource/<dataset>.json. Keep the names semantic so callers never depend on ids.
CFTC_COT_DATASETS: Mapping[str, str] = {
    "tff_futures_only": "gpe5-46if",
    "disaggregated_futures_only": "72hh-3qpy",
}

BLS_MACRO_SERIES = frozenset({"CUUR0000SA0", "CUSR0000SA0L1E", "CES0000000001", "LNS14000000"})
ECB_FX_CURRENCIES = frozenset({"USD", "JPY", "GBP", "CHF", "CAD", "AUD", "CNY"})

NYFED_REFERENCE_RATES: Mapping[str, Tuple[str, str]] = {
    "SOFR": ("secured", "sofr"),
    "TGCR": ("secured", "tgcr"),
    "BGCR": ("secured", "bgcr"),
    "EFFR": ("unsecured", "effr"),
    "OBFR": ("unsecured", "obfr"),
}


@dataclass(frozen=True)
class OpenFeedResult:
    provider_id: str
    dataset: str
    rows: Tuple[Mapping[str, object], ...]

    @property
    def row_count(self) -> int:
        return len(self.rows)


def _default_request_transport(request: urllib.request.Request) -> Tuple[int, bytes]:
    try:
        with urllib.request.urlopen(request, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _default_transport(url: str) -> Tuple[int, bytes]:
    user_agent = os.environ.get(
        "MARKET_DATA_USER_AGENT",
        "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
    ).strip()
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    return _default_request_transport(req)


def _sec_transport(url: str) -> Tuple[int, bytes]:
    """SEC transport with a declared bot identity per EDGAR fair-access guidance."""
    contact = os.environ.get("SEC_CONTACT_EMAIL", "").strip()
    user_agent = os.environ.get("SEC_USER_AGENT", "").strip()
    if not user_agent:
        user_agent = (
            f"hedge-desk/1.0 {contact}"
            if contact
            else "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk"
        )
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    return _default_request_transport(req)


def _decode_json(raw: bytes, provider: str) -> object:
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"{provider} returned malformed JSON") from exc


def _fetch_json(url: str, provider: str, transport: Transport) -> object:
    try:
        status, raw = transport(url)
    except Exception as exc:
        raise ValueError(f"{provider} transport failed") from exc
    if status != 200 or not raw:
        body = raw[:200].decode("utf-8", errors="replace") if raw else ""
        raise ValueError(f"{provider} fetch failed (status {status}) body={body}")
    return _decode_json(raw, provider)


def _fetch_request_json(
    request: urllib.request.Request,
    provider: str,
    transport: RequestTransport,
) -> object:
    try:
        status, raw = transport(request)
    except Exception as exc:
        raise ValueError(f"{provider} transport failed") from exc
    if status != 200 or not raw:
        body = raw[:200].decode("utf-8", errors="replace") if raw else ""
        raise ValueError(f"{provider} fetch failed (status {status}) body={body}")
    return _decode_json(raw, provider)


def _rows_from_list(payload: object, provider: str) -> Tuple[Mapping[str, object], ...]:
    if not isinstance(payload, list):
        raise ValueError(f"{provider} payload is not a row list")
    rows = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError(f"{provider} row is not an object")
        rows.append(row)
    return tuple(rows)


def _positive_limit(limit: int, maximum: int = 1000) -> int:
    if type(limit) is not int or limit < 1 or limit > maximum:
        raise ValueError(f"limit must be an integer from 1 to {maximum}")
    return limit


def treasury_latest_auctions(
    limit: int = 25,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Return the latest Treasury auction records from Fiscal Data (no key)."""
    limit = _positive_limit(limit, 1000)
    query = urllib.parse.urlencode(
        {
            "sort": "-auction_date",
            "format": "json",
            "page[number]": "1",
            "page[size]": str(limit),
        }
    )
    payload = _fetch_json(f"{TREASURY_AUCTIONS_URL}?{query}", "treasury-fiscaldata", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("treasury-fiscaldata payload has no data rows")
    return OpenFeedResult(
        provider_id="treasury-fiscaldata",
        dataset="treasury-securities-auctions",
        rows=_rows_from_list(payload["data"], "treasury-fiscaldata"),
    )


def _finra_oauth_token(
    transport: RequestTransport,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> str:
    client = (client_id if client_id is not None else os.environ.get("FINRA_CLIENT_ID", "")).strip()
    secret = (
        client_secret
        if client_secret is not None
        else os.environ.get("FINRA_CLIENT_SECRET", "")
    ).strip()
    if not client or not secret:
        raise ValueError("FINRA_CLIENT_ID and FINRA_CLIENT_SECRET are required")
    basic = base64.b64encode(f"{client}:{secret}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        FINRA_TOKEN_URL,
        data=b"",
        method="POST",
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {basic}",
            "User-Agent": "hedge-desk/1.0 research",
        },
    )
    payload = _fetch_request_json(request, "finra-auth", transport)
    if not isinstance(payload, dict):
        raise ValueError("finra-auth token payload is malformed")
    token = str(payload.get("access_token", "")).strip()
    if not token:
        raise ValueError("finra-auth token payload has no access_token")
    return token


def finra_fixed_income(
    dataset: str,
    limit: int = 50,
    request_transport: RequestTransport = _default_request_transport,
    access_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> OpenFeedResult:
    """Fetch a vetted FINRA public fixed-income dataset via OAuth 2.0.

    FINRA's Public Credential is free, but authentication is required. In
    production, provide FINRA_CLIENT_ID and FINRA_CLIENT_SECRET as server-side
    environment variables. Tests may inject a short-lived access_token.
    """
    if dataset not in FINRA_FIXED_INCOME_DATASETS:
        raise ValueError(f"unsupported FINRA fixed-income dataset: {dataset}")
    limit = _positive_limit(limit, 5000)
    token = (access_token or "").strip() or _finra_oauth_token(
        request_transport, client_id=client_id, client_secret=client_secret
    )
    base = FINRA_DATA_URL.format(group="fixedIncomeMarket", dataset=dataset)
    query = urllib.parse.urlencode({"limit": str(limit)})
    request = urllib.request.Request(
        f"{base}?{query}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "hedge-desk/1.0 research",
        },
    )
    payload = _fetch_request_json(request, "finra", request_transport)
    return OpenFeedResult(
        provider_id="finra",
        dataset=dataset,
        rows=_rows_from_list(payload, "finra"),
    )



def bls_latest_series(
    series: str,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch the latest observation for a vetted BLS macro series (no key required)."""
    normalized = series.strip().upper()
    if normalized not in BLS_MACRO_SERIES:
        raise ValueError(f"unsupported BLS macro series: {series}")
    payload = _fetch_json(BLS_LATEST_URL.format(series=normalized), "bls", transport)
    if not isinstance(payload, dict) or payload.get("status") != "REQUEST_SUCCEEDED":
        raise ValueError("bls request did not succeed")
    results = payload.get("Results")
    series_rows = results.get("series") if isinstance(results, dict) else None
    if not isinstance(series_rows, list) or not series_rows:
        raise ValueError("bls payload has no series rows")
    data = series_rows[0].get("data") if isinstance(series_rows[0], dict) else None
    if not isinstance(data, list) or not data:
        raise ValueError("bls payload has no observations")
    rows = []
    for row in data:
        if isinstance(row, dict):
            item = dict(row)
            item["seriesID"] = normalized
            rows.append(item)
    return OpenFeedResult(provider_id="bls", dataset=normalized, rows=tuple(rows))


def ecb_exchange_rates(
    currencies: Sequence[str] = ("USD", "JPY", "GBP", "CHF"),
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch latest ECB euro reference FX rates (no key required)."""
    normalized = []
    for currency in currencies:
        code = str(currency).strip().upper()
        if code not in ECB_FX_CURRENCIES:
            raise ValueError(f"unsupported ECB FX currency: {currency}")
        if code not in normalized:
            normalized.append(code)
    if not normalized:
        raise ValueError("at least one ECB FX currency is required")
    key = f"D.{'+'.join(normalized)}.EUR.SP00.A"
    query = urllib.parse.urlencode({"format": "csvdata", "lastNObservations": "1"})
    url = f"{ECB_EXR_URL.format(key=key)}?{query}"
    try:
        status, raw = transport(url)
    except Exception as exc:
        raise ValueError("ecb-fx transport failed") from exc
    if status != 200 or not raw:
        body = raw[:200].decode("utf-8", errors="replace") if raw else ""
        raise ValueError(f"ecb-fx fetch failed (status {status}) body={body}")
    try:
        text = raw.decode("utf-8-sig")
        parsed = tuple(dict(row) for row in csv.DictReader(io.StringIO(text)))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ValueError("ecb-fx returned malformed CSV") from exc
    if not parsed:
        raise ValueError("ecb-fx payload has no observations")
    return OpenFeedResult(provider_id="ecb-fx", dataset="EXR", rows=parsed)


def cftc_cot(
    report: str = "tff_futures_only",
    limit: int = 100,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch CFTC COT rows from the official public-reporting API (no key)."""
    try:
        dataset_id = CFTC_COT_DATASETS[report]
    except KeyError as exc:
        raise ValueError(f"unsupported CFTC COT report: {report}") from exc
    limit = _positive_limit(limit, 5000)
    query = urllib.parse.urlencode({"$limit": str(limit), "$order": "report_date_as_yyyy_mm_dd DESC"})
    url = f"{CFTC_SODA_URL.format(dataset=dataset_id)}?{query}"
    payload = _fetch_json(url, "cftc-cot", transport)
    return OpenFeedResult(
        provider_id="cftc-cot",
        dataset=report,
        rows=_rows_from_list(payload, "cftc-cot"),
    )


def nyfed_reference_rates(
    rate: str | None = None,
    limit: int = 5,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch NY Fed administered reference rates (SOFR/EFFR/etc.; no key)."""
    if rate is None:
        payload = _fetch_json(NYFED_LATEST_RATES_URL, "nyfed-markets", transport)
        dataset = "all-latest"
    else:
        normalized = rate.strip().upper()
        try:
            segment, slug = NYFED_REFERENCE_RATES[normalized]
        except KeyError as exc:
            raise ValueError(f"unsupported NY Fed reference rate: {rate}") from exc
        limit = _positive_limit(limit, 1000)
        url = NYFED_RATE_HISTORY_URL.format(segment=segment, rate=slug, limit=limit)
        payload = _fetch_json(url, "nyfed-markets", transport)
        dataset = normalized.lower()
    if not isinstance(payload, dict) or not isinstance(payload.get("refRates"), list):
        raise ValueError("nyfed-markets payload has no refRates rows")
    return OpenFeedResult(
        provider_id="nyfed-markets",
        dataset=dataset,
        rows=_rows_from_list(payload["refRates"], "nyfed-markets"),
    )


def eia_v2(
    route: str,
    data: Sequence[str] = ("value",),
    limit: int = 100,
    transport: Transport = _default_transport,
    api_key: str | None = None,
) -> OpenFeedResult:
    """Fetch an EIA API v2 dataset. EIA keys are free but required by EIA."""
    key = (api_key if api_key is not None else os.environ.get("EIA_API_KEY", "")).strip()
    if not key:
        raise ValueError("EIA_API_KEY is required for EIA Open Data v2")
    normalized = route.strip().strip("/")
    if not normalized or ".." in normalized or any(part == "" for part in normalized.split("/")):
        raise ValueError("invalid EIA route")
    if not data or any(not field or not field.replace("_", "").replace("-", "").isalnum() for field in data):
        raise ValueError("invalid EIA data field")
    limit = _positive_limit(limit, 5000)
    pairs = [("api_key", key), ("length", str(limit)), ("offset", "0")]
    pairs.extend(("data[]", field) for field in data)
    query = urllib.parse.urlencode(pairs)
    url = f"{EIA_V2_URL.format(route=normalized)}?{query}"
    payload = _fetch_json(url, "eia-open-data", transport)
    if not isinstance(payload, dict):
        raise ValueError("eia-open-data payload is not an object")
    response = payload.get("response")
    if not isinstance(response, dict) or not isinstance(response.get("data"), list):
        raise ValueError("eia-open-data payload has no response.data rows")
    return OpenFeedResult(
        provider_id="eia-open-data",
        dataset=normalized,
        rows=_rows_from_list(response["data"], "eia-open-data"),
    )


def _normalize_cik(cik: str | int) -> str:
    raw = str(cik).strip()
    if not raw.isdigit() or len(raw) > 10:
        raise ValueError("CIK must contain at most 10 digits")
    return raw.zfill(10)


def sec_submissions(
    cik: str | int,
    transport: Transport = _sec_transport,
) -> Mapping[str, object]:
    """Fetch SEC EDGAR company submission history (no API key)."""
    normalized = _normalize_cik(cik)
    payload = _fetch_json(SEC_SUBMISSIONS_URL.format(cik=normalized), "sec-edgar", transport)
    if not isinstance(payload, dict) or "cik" not in payload:
        raise ValueError("sec-edgar submissions payload is malformed")
    return payload


def sec_companyfacts(
    cik: str | int,
    transport: Transport = _sec_transport,
) -> Mapping[str, object]:
    """Fetch SEC XBRL company facts for one issuer (no API key)."""
    normalized = _normalize_cik(cik)
    payload = _fetch_json(SEC_COMPANYFACTS_URL.format(cik=normalized), "sec-edgar", transport)
    if not isinstance(payload, dict) or "facts" not in payload:
        raise ValueError("sec-edgar companyfacts payload is malformed")
    return payload


__all__ = [
    "BLS_MACRO_SERIES",
    "CFTC_COT_DATASETS",
    "ECB_FX_CURRENCIES",
    "FINRA_FIXED_INCOME_DATASETS",
    "NYFED_REFERENCE_RATES",
    "OpenFeedResult",
    "bls_latest_series",
    "cftc_cot",
    "ecb_exchange_rates",
    "eia_v2",
    "finra_fixed_income",
    "nyfed_reference_rates",
    "sec_companyfacts",
    "sec_submissions",
    "treasury_latest_auctions",
]
