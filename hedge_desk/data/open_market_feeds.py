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
import xml.etree.ElementTree as ET
import ssl
from dataclasses import dataclass
from datetime import date, timedelta
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
BLS_V1_SERIES_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/{series}"
BEA_DATA_URL = "https://apps.bea.gov/api/data/"
# ECB euro reference rates: the SDMX Data Portal endpoint intermittently closes
# connections, so use the classic daily eurofxref feed (same official data).
ECB_EUROFXREF_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
TREASURY_DAILY_RATES_URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
FDIC_FAILURES_URL = "https://api.fdic.gov/banks/failures"
WORLD_BANK_INDICATOR_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
# IMF DataMapper API: keyless global macro series (real GDP growth %, etc.).
IMF_DATAMAPPER_URL = "https://www.imf.org/external/datamapper/api/v1/{indicator}/{country}"
# Official OECD SDMX API: composite leading indicator, machine-readable CSV.
OECD_CLI_URL = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI/{key}"
# Official Eurostat statistics API: quarterly GDP, returned as JSON-stat.
EUROSTAT_GDP_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp"
# Official FDSN Earthquake Catalog GeoJSON query and NASA EONET v3 events API.
USGS_EARTHQUAKE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NASA_EONET_EVENTS_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"
# Bank of Canada Valet API: official daily FX reference rates (keyless).
BOC_VALET_URL = "https://www.bankofcanada.ca/valet/observations/{series}/json"
# Coinbase exchange-rates API: keyless crypto/fiat reference rates.
COINBASE_RATES_URL = "https://api.coinbase.com/v2/exchange-rates?currency={base}"
# Frankfurter: keyless daily FX reference rates (ECB data, USD-base option).
FRANKFURTER_URL = "https://api.frankfurter.app/latest?from={base}&to={quotes}"

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

# Official daily Treasury par yield curve tenors, sourced from FRED's DGS
# constant-maturity series (the same official Treasury/Fed H.15 rates; the
# home.treasury.gov XML route is unreliable). FRED DGS = "Market Yield on U.S.
# Treasury Securities at X-Year Constant Maturity, Quoted on an Investment
# Basis".
TREASURY_DGS_TENORS: Tuple[str, ...] = (
    "DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5",
    "DGS7", "DGS10", "DGS20", "DGS30",
)

# Nasdaq's public quote/calendar API needs a browser-style UA; it is
# rate-sensitive, so batch callers must cache (see rates_desk FRED caching).
NASDAQ_API_URL = "https://api.nasdaq.com/api/{path}"
_NASDAQ_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
NASDAQ_ETF_SYMBOLS = frozenset(
    {"SPY", "QQQ", "IWM", "DIA", "TLT", "XLF", "XLE", "XLK", "EEM", "GLD"}
)

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


def _system_ssl_context() -> ssl.SSLContext:
    """A verification-preserving SSL context using certifi's CA bundle.

    Python's bundled default verify path (/private/etc/ssl/cert.pem) can lag the
    macOS system keychain and reject valid 2024+ roots (Entrust OV, Sectigo E46)
    that Treasury's and ECB's endpoints present. certifi ships the current roots;
    using it keeps certificate verification fully ON — this is a trust-store fix,
    never a disabling of verification.
    """
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # pragma: no cover - certifi is a declared dependency
        return ssl.create_default_context()


def _default_request_transport(request: urllib.request.Request) -> Tuple[int, bytes]:
    try:
        with urllib.request.urlopen(request, timeout=15, context=_system_ssl_context()) as resp:
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


def _is_transient_status(status: int) -> bool:
    return status == 0 or status == 429 or 500 <= status < 600


def _fetch_json(url: str, provider: str, transport: Transport, retries: int = 2) -> object:
    last_status, last_raw = 0, b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(url)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            return _decode_json(raw, provider)
        last_status, last_raw = status, raw
        if not _is_transient_status(status) or attempt == retries:
            break
        import time as _time
        _time.sleep(1.0 * (attempt + 1))
    body = last_raw[:200].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={body}")


def _fetch_bytes(url: str, provider: str, transport: Transport, retries: int = 2) -> bytes:
    last_status, last_raw = 0, b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(url)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            return raw
        last_status, last_raw = status, raw
        if not _is_transient_status(status) or attempt == retries:
            break
        import time as _time
        _time.sleep(1.0 * (attempt + 1))
    body = last_raw[:200].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={body}")


def _fetch_request_json(
    request: urllib.request.Request,
    provider: str,
    transport: RequestTransport,
    retries: int = 2,
) -> object:
    last_status, last_raw = 0, b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(request)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            return _decode_json(raw, provider)
        last_status, last_raw = status, raw
        if not _is_transient_status(status) or attempt == retries:
            break
        import time as _time
        _time.sleep(1.0 * (attempt + 1))
    body = last_raw[:200].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={body}")


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
    """Fetch the latest observation for a vetted BLS macro series.

    Prefer the BLS v2 latest-series route. If that route is unavailable or
    rejects an unregistered request, fall back to the official keyless v1
    single-series route and keep only its newest observation.
    """
    normalized = series.strip().upper()
    if normalized not in BLS_MACRO_SERIES:
        raise ValueError(f"unsupported BLS macro series: {series}")

    payload = None
    v2_error = None
    try:
        candidate = _fetch_json(
            BLS_LATEST_URL.format(series=normalized), "bls-v2", transport
        )
        if isinstance(candidate, dict) and candidate.get("status") == "REQUEST_SUCCEEDED":
            payload = candidate
        else:
            v2_error = "v2 request did not succeed"
    except ValueError as exc:
        v2_error = str(exc)

    if payload is None:
        try:
            candidate = _fetch_json(
                BLS_V1_SERIES_URL.format(series=normalized), "bls-v1", transport
            )
        except ValueError as exc:
            raise ValueError(
                f"bls fetch failed on v2 and v1; v2={v2_error}; v1={exc}"
            ) from exc
        if not isinstance(candidate, dict) or candidate.get("status") != "REQUEST_SUCCEEDED":
            raise ValueError(
                f"bls fetch failed on v2 and v1; v2={v2_error}; v1=request did not succeed"
            )
        payload = candidate

    results = payload.get("Results")
    series_rows = results.get("series") if isinstance(results, dict) else None
    if not isinstance(series_rows, list) or not series_rows:
        raise ValueError("bls payload has no series rows")
    data = series_rows[0].get("data") if isinstance(series_rows[0], dict) else None
    if not isinstance(data, list) or not data:
        raise ValueError("bls payload has no observations")

    rows = []
    for row in data[:1]:
        if isinstance(row, dict):
            item = dict(row)
            item["seriesID"] = normalized
            rows.append(item)
    if not rows:
        raise ValueError("bls payload has no usable observations")
    return OpenFeedResult(provider_id="bls", dataset=normalized, rows=tuple(rows))


def bea_nipa(
    table: str = "T10101",
    frequency: str = "Q",
    year: str = "X",
    transport: Transport = _default_transport,
    api_key: str | None = None,
) -> OpenFeedResult:
    """Fetch a bounded BEA NIPA table using the official Data API.

    BEA API keys are free but required. The key is read server-side from
    BEA_API_KEY unless explicitly injected for deterministic tests.
    """
    key = (api_key if api_key is not None else os.environ.get("BEA_API_KEY", "")).strip()
    if not key:
        raise ValueError("BEA_API_KEY is required for BEA Data API")
    table_name = str(table).strip().upper()
    if not table_name or not table_name.isalnum() or len(table_name) > 16:
        raise ValueError("invalid BEA NIPA table name")
    freq = str(frequency).strip().upper()
    if freq not in {"A", "Q"}:
        raise ValueError("BEA NIPA frequency must be A or Q")
    yr = str(year).strip().upper()
    if yr != "X":
        parts = [p.strip() for p in yr.split(",") if p.strip()]
        if not parts or any(not p.isdigit() or len(p) != 4 for p in parts):
            raise ValueError("invalid BEA NIPA year")
        yr = ",".join(parts)
    query = urllib.parse.urlencode({
        "UserID": key,
        "method": "GetData",
        "datasetname": "NIPA",
        "TableName": table_name,
        "Frequency": freq,
        "Year": yr,
        "ResultFormat": "JSON",
    })
    payload = _fetch_json(f"{BEA_DATA_URL}?{query}", "bea", transport)
    if not isinstance(payload, dict):
        raise ValueError("bea payload is not an object")
    bea_api = payload.get("BEAAPI")
    results = bea_api.get("Results") if isinstance(bea_api, dict) else None
    if isinstance(results, dict) and results.get("Error"):
        raise ValueError("bea request returned an API error")
    data = results.get("Data") if isinstance(results, dict) else None
    if not isinstance(data, list) or not data:
        raise ValueError("bea payload has no Results.Data rows")
    rows = tuple(row for row in data if isinstance(row, dict))
    if not rows:
        raise ValueError("bea payload has no usable data rows")
    return OpenFeedResult("bea", f"NIPA-{table_name}-{freq}", rows)


def ecb_exchange_rates(
    currencies: Sequence[str] = ("USD", "JPY", "GBP", "CHF"),
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch latest ECB euro reference FX rates (no key required).

    Uses the official daily eurofxref feed (EUR base); the SDMX Data Portal
    endpoint intermittently drops connections.
    """
    normalized = []
    for currency in currencies:
        code = str(currency).strip().upper()
        if code not in ECB_FX_CURRENCIES:
            raise ValueError(f"unsupported ECB FX currency: {currency}")
        if code not in normalized:
            normalized.append(code)
    if not normalized:
        raise ValueError("at least one ECB FX currency is required")
    raw = _fetch_bytes(ECB_EUROFXREF_URL, "ecb-fx", transport)
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError("ecb-fx returned malformed XML") from exc
    # eurofxref nests Cube elements: Envelope > Cube > Cube(time=...) > Cube(currency, rate)
    wanted = set(normalized)
    rows = []
    ref_date = ""
    for cube in root.iter():
        tag = cube.tag.split("}", 1)[-1]
        if tag != "Cube":
            continue
        if "time" in cube.attrib:
            ref_date = str(cube.attrib["time"])
            continue
        code = str(cube.attrib.get("currency", "")).upper()
        rate = str(cube.attrib.get("rate", ""))
        if code in wanted and rate:
            rows.append({"currency": code, "rate": rate, "date": ref_date, "base": "EUR"})
    if not rows:
        raise ValueError("ecb-fx payload has no observations")
    return OpenFeedResult(provider_id="ecb-fx", dataset="eurofxref-daily", rows=tuple(rows))



def treasury_yield_curve(
    year: int | None = None,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch official U.S. Treasury daily par yield curve rates.

    Sources the constant-maturity par yields from FRED's DGS series (the same
    official Treasury/Fed H.15 rates); the home.treasury.gov XML route is
    unreliable. Attribution is honest: provider_id is "fred".
    """
    import datetime as _dt
    from hedge_desk.rates_desk import fred_series_rows  # lazy: avoid import cycle

    target_year = year if year is not None else _dt.date.today().year
    if type(target_year) is not int or target_year < 1990 or target_year > 2100:
        raise ValueError("invalid Treasury yield-curve year")
    end = _dt.date.today()
    start = end - _dt.timedelta(days=14)
    rows = []
    for tenor in TREASURY_DGS_TENORS:
        try:
            obs = fred_series_rows(tenor, start, end, transport=transport)
        except ValueError as exc:
            raise ValueError(f"treasury-rates FRED fetch failed for {tenor}: {exc}") from exc
        for day, value in obs[-5:]:
            rows.append({"tenor": tenor, "date": str(day), "value": str(value)})
    if not rows:
        raise ValueError("treasury-rates payload has no observations")
    return OpenFeedResult("fred", "treasury_par_yield_curve_DGS", tuple(rows))


def fdic_failures(
    limit: int = 10,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent U.S. bank failures from FDIC BankFind."""
    limit = _positive_limit(limit, 1000)
    query = urllib.parse.urlencode({
        "limit": str(limit),
        "sort_by": "FAILDATE",
        "sort_order": "DESC",
    })
    payload = _fetch_json(f"{FDIC_FAILURES_URL}?{query}", "fdic", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("fdic payload has no data rows")
    rows = []
    for item in payload["data"]:
        if isinstance(item, dict):
            row = item.get("data") if isinstance(item.get("data"), dict) else item
            rows.append(row)
    if not rows:
        raise ValueError("fdic payload has no failure rows")
    return OpenFeedResult("fdic", "bank-failures", tuple(rows))


def world_bank_indicator(
    indicator: str,
    country: str = "USA",
    per_page: int = 5,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent World Bank indicator observations."""
    allowed = {
        "NY.GDP.MKTP.CD",
        "FP.CPI.TOTL.ZG",
        "SL.UEM.TOTL.ZS",
        "NE.EXP.GNFS.ZS",
        "GC.DOD.TOTL.GD.ZS",
    }
    normalized_indicator = indicator.strip().upper()
    normalized_country = country.strip().upper()
    if normalized_indicator not in allowed:
        raise ValueError(f"unsupported World Bank indicator: {indicator}")
    if not normalized_country.isalnum() or len(normalized_country) > 3:
        raise ValueError("invalid World Bank country code")
    per_page = _positive_limit(per_page, 1000)
    query = urllib.parse.urlencode({
        "format": "json",
        "per_page": str(per_page),
        "mrnev": str(per_page),
    })
    url = WORLD_BANK_INDICATOR_URL.format(
        country=normalized_country,
        indicator=normalized_indicator,
    ) + "?" + query
    payload = _fetch_json(url, "world-bank", transport)
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise ValueError("world-bank payload has no data rows")
    rows = tuple(row for row in payload[1] if isinstance(row, dict) and row.get("value") is not None)
    if not rows:
        raise ValueError("world-bank payload has no observations")
    return OpenFeedResult("world-bank", normalized_indicator, rows)


def imf_gdp_growth(
    country: str = "USA",
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch IMF real GDP growth (%) series (keyless global macro).

    Uses the IMF DataMapper API (official WEO-based series). Returns the
    indicator's annual observations for the requested country code.
    """
    normalized_country = country.strip().upper()
    if not normalized_country.isalnum() or len(normalized_country) > 3:
        raise ValueError("invalid IMF country code")
    url = IMF_DATAMAPPER_URL.format(indicator="NGDP_RPCH", country=normalized_country)
    payload = _fetch_json(url, "imf", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("values"), dict):
        raise ValueError("imf payload has no values")
    series = payload["values"].get("NGDP_RPCH", {})
    if not isinstance(series, dict) or not series:
        raise ValueError("imf payload has no NGDP_RPCH observations")
    # DataMapper nests by country: {country_code: {year: value}}.
    country_series = series.get(normalized_country, {})
    if not isinstance(country_series, dict) or not country_series:
        raise ValueError(f"imf payload has no NGDP_RPCH observations for {normalized_country}")
    rows = tuple(
        {"date": str(year), "value": value, "indicator": "NGDP_RPCH", "country": normalized_country}
        for year, value in sorted(country_series.items())
        if isinstance(value, (int, float))
    )
    if not rows:
        raise ValueError("imf payload has no numeric observations")
    return OpenFeedResult("imf", "NGDP_RPCH", rows)


def oecd_composite_leading_indicator(
    country: str = "USA",
    start_period: str | None = None,
    end_period: str | None = None,
    limit: int = 36,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch a bounded OECD composite-leading-indicator time series."""
    normalized_country = country.strip().upper()
    if len(normalized_country) != 3 or not normalized_country.isascii() or not normalized_country.isalpha():
        raise ValueError("invalid OECD country code")
    limit = _positive_limit(limit, 200)
    today = date.today()
    start_period = start_period or today.replace(year=today.year - 2).strftime("%Y-%m")
    end_period = end_period or today.strftime("%Y-%m")
    for period in (start_period, end_period):
        if (len(period) != 7 or period[4] != "-" or not period[:4].isdigit()
                or not period[5:].isdigit() or not 1 <= int(period[5:]) <= 12):
            raise ValueError("periods must be YYYY-MM")
    if start_period > end_period:
        raise ValueError("start_period must not follow end_period")
    # The OECD sample key selects monthly CLI amplitude-adjusted index data.
    key = f"{normalized_country}.M.LI...AA...H"
    query = urllib.parse.urlencode({
        "startPeriod": start_period,
        "endPeriod": end_period,
        "dimensionAtObservation": "AllDimensions",
        "format": "csvfile",
    })
    raw = _fetch_bytes(OECD_CLI_URL.format(key=key) + "?" + query, "oecd", transport)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if not reader.fieldnames or not {"TIME_PERIOD", "OBS_VALUE"}.issubset(reader.fieldnames):
        raise ValueError("oecd CSV is missing observation columns")
    rows = tuple(
        {key: row.get(key) for key in ("REF_AREA", "MEASURE", "TIME_PERIOD", "OBS_VALUE") if row.get(key) not in (None, "")}
        for row in reader
        if row.get("TIME_PERIOD") and row.get("OBS_VALUE") not in (None, "")
    )[-limit:]
    if not rows:
        raise ValueError("oecd payload has no observations")
    return OpenFeedResult("oecd", "DF_CLI", rows)


def eurostat_quarterly_gdp(
    geo: str = "EA20",
    periods: int = 8,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent Euro-area quarterly GDP from Eurostat's JSON-stat API."""
    normalized_geo = geo.strip().upper()
    if not normalized_geo.isascii() or not normalized_geo.replace("_", "").isalnum() or len(normalized_geo) > 16:
        raise ValueError("invalid Eurostat geography code")
    periods = _positive_limit(periods, 40)
    query = urllib.parse.urlencode({
        "freq": "Q", "unit": "CLV10_MEUR", "na_item": "B1GQ",
        "s_adj": "SCA", "geo": normalized_geo,
        "lastTimePeriod": str(periods), "lang": "en",
    })
    payload = _fetch_json(EUROSTAT_GDP_URL + "?" + query, "eurostat", transport)
    if not isinstance(payload, dict):
        raise ValueError("eurostat payload is not an object")
    dimensions, sizes = payload.get("id"), payload.get("size")
    dimension = payload.get("dimension")
    values = payload.get("value")
    if not isinstance(dimensions, list) or not isinstance(sizes, list) or not isinstance(dimension, dict):
        raise ValueError("eurostat payload has no JSON-stat dimensions")
    if "time" not in dimensions or len(dimensions) != len(sizes):
        raise ValueError("eurostat payload has no time dimension")
    time_index = dimensions.index("time")
    if any(size != 1 for i, size in enumerate(sizes) if i != time_index):
        raise ValueError("eurostat query returned ambiguous non-time dimensions")
    categories = dimension.get("time", {}).get("category", {}).get("index")
    if not isinstance(categories, dict) or not categories:
        raise ValueError("eurostat payload has no time categories")
    stride = 1
    for size in sizes[time_index + 1:]:
        stride *= size
    rows = []
    for period, category_index in sorted(categories.items(), key=lambda item: item[1]):
        offset = category_index * stride
        if isinstance(values, list):
            value = values[offset] if offset < len(values) else None
        elif isinstance(values, dict):
            value = values.get(str(offset))
        else:
            raise ValueError("eurostat payload has no observation values")
        if value not in (None, ""):
            rows.append({"date": str(period), "value": value, "geo": normalized_geo,
                         "indicator": "B1GQ", "unit": "CLV10_MEUR"})
    if not rows:
        raise ValueError("eurostat payload has no GDP observations")
    return OpenFeedResult("eurostat", "namq_10_gdp", tuple(rows))


def usgs_earthquakes(
    days: int = 30,
    min_magnitude: float = 4.5,
    limit: int = 25,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent material earthquakes using a bounded USGS GeoJSON query."""
    days = _positive_limit(days, 365)
    limit = _positive_limit(limit, 500)
    if not isinstance(min_magnitude, (int, float)) or not 0 <= min_magnitude <= 10:
        raise ValueError("min_magnitude must be between 0 and 10")
    end = date.today()
    query = urllib.parse.urlencode({
        "format": "geojson", "starttime": (end - timedelta(days=days)).isoformat(),
        "endtime": end.isoformat(), "minmagnitude": str(min_magnitude),
        "orderby": "time", "limit": str(limit),
    })
    payload = _fetch_json(USGS_EARTHQUAKE_URL + "?" + query, "usgs", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("features"), list):
        raise ValueError("usgs payload has no GeoJSON features")
    rows = []
    for feature in payload["features"][:limit]:
        if not isinstance(feature, dict) or not isinstance(feature.get("properties"), dict):
            continue
        properties = feature["properties"]
        geometry = feature.get("geometry") if isinstance(feature.get("geometry"), dict) else {}
        coordinates = geometry.get("coordinates")
        row = {"event_id": feature.get("id"), "magnitude": properties.get("mag"),
               "time": properties.get("time"), "place": properties.get("place"),
               "title": properties.get("title"), "url": properties.get("url")}
        if isinstance(coordinates, list) and len(coordinates) >= 2:
            row.update({"longitude": coordinates[0], "latitude": coordinates[1]})
            if len(coordinates) > 2:
                row["depth_km"] = coordinates[2]
        rows.append({key: value for key, value in row.items() if value not in (None, "")})
    return OpenFeedResult("usgs", "earthquakes-m4_5-30d", tuple(rows))


def nasa_eonet_events(
    days: int = 30,
    limit: int = 25,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent open natural events from NASA EONET v3."""
    days = _positive_limit(days, 365)
    limit = _positive_limit(limit, 500)
    query = urllib.parse.urlencode({"status": "open", "days": str(days), "limit": str(limit)})
    payload = _fetch_json(NASA_EONET_EVENTS_URL + "?" + query, "nasa-eonet", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("events"), list):
        raise ValueError("nasa-eonet payload has no events")
    rows = []
    for event in payload["events"][:limit]:
        if not isinstance(event, dict):
            continue
        geometries = event.get("geometry") if isinstance(event.get("geometry"), list) else []
        latest = geometries[-1] if geometries and isinstance(geometries[-1], dict) else {}
        categories = event.get("categories") if isinstance(event.get("categories"), list) else []
        sources = event.get("sources") if isinstance(event.get("sources"), list) else []
        rows.append({
            "event_id": event.get("id"), "title": event.get("title"),
            "categories": [item.get("id") for item in categories if isinstance(item, dict) and item.get("id")],
            "sources": [item.get("id") for item in sources if isinstance(item, dict) and item.get("id")],
            "date": latest.get("date"), "geometry_type": latest.get("type"),
            "coordinates": latest.get("coordinates"),
        })
    return OpenFeedResult("nasa-eonet", "open-natural-events", tuple(rows))


def bank_of_canada_fx(
    series: str = "FXUSDCAD",
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch official Bank of Canada daily FX reference rate (keyless).

    Valet API returns daily observations for a named series (e.g. FXUSDCAD).
    """
    normalized = series.strip().upper()
    if not normalized.isalnum() or len(normalized) > 12:
        raise ValueError("invalid Bank of Canada series code")
    url = BOC_VALET_URL.format(series=normalized)
    payload = _fetch_json(url, "bank-of-canada", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("observations"), list):
        raise ValueError("bank-of-canada payload has no observations")
    rows = []
    for obs in payload["observations"]:
        if not isinstance(obs, dict):
            continue
        date = str(obs.get("d", ""))
        val = (obs.get(normalized) or {}).get("v") if isinstance(obs.get(normalized), dict) else None
        if date and val is not None:
            rows.append({"date": date, "series": normalized, "value": str(val)})
    if not rows:
        raise ValueError("bank-of-canada payload has no numeric observations")
    return OpenFeedResult("bank-of-canada", normalized, tuple(rows))


def coinbase_exchange_rates(
    base: str = "USD",
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch Coinbase reference exchange rates (keyless crypto/fiat).

    Returns the base currency's rate against a fixed set of major currencies
    and crypto assets. Rates are Coinbase's public reference rates.
    """
    normalized = base.strip().upper()
    if not normalized.isalnum() or len(normalized) > 5:
        raise ValueError("invalid Coinbase base currency")
    url = COINBASE_RATES_URL.format(base=normalized)
    payload = _fetch_json(url, "coinbase", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), dict):
        raise ValueError("coinbase payload has no data")
    rates = payload["data"].get("rates", {})
    if not isinstance(rates, dict) or not rates:
        raise ValueError("coinbase payload has no rates")
    wanted = ("BTC", "ETH", "EUR", "JPY", "GBP", "CAD", "AUD", "CHF", "CNY")
    rows = tuple(
        {"base": normalized, "quote": code, "rate": str(rates[code])}
        for code in wanted
        if code in rates
    )
    if not rows:
        raise ValueError("coinbase payload has no wanted rates")
    return OpenFeedResult("coinbase", f"exchange-rates-{normalized}", rows)


def frankfurter_fx(
    base: str = "USD",
    quotes: Sequence[str] = ("EUR", "GBP", "JPY", "CAD", "CHF"),
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch Frankfurter daily FX reference rates (keyless, ECB data).

    USD-base reference rates that complement the ECB euro-base feed. Returns
    the chosen base currency's rate against a set of major quote currencies.
    """
    normalized = base.strip().upper()
    if not normalized.isalnum() or len(normalized) > 5:
        raise ValueError("invalid Frankfurter base currency")
    wanted = []
    for q in quotes:
        code = str(q).strip().upper()
        if not code.isalnum() or len(code) > 5:
            raise ValueError(f"invalid Frankfurter quote currency: {q}")
        if code not in wanted:
            wanted.append(code)
    if not wanted:
        raise ValueError("at least one Frankfurter quote currency is required")
    url = FRANKFURTER_URL.format(base=normalized, quotes=",".join(wanted))
    payload = _fetch_json(url, "frankfurter", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("rates"), dict):
        raise ValueError("frankfurter payload has no rates")
    rates = payload["rates"]
    ref_date = str(payload.get("date", ""))
    rows = tuple(
        {"base": str(payload.get("base", normalized)), "quote": code, "rate": str(rates[code]), "date": ref_date}
        for code in wanted
        if code in rates
    )
    if not rows:
        raise ValueError("frankfurter payload has no wanted rates")
    return OpenFeedResult("frankfurter", f"fx-{normalized}", rows)


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


def _nasdaq_transport(url: str) -> Tuple[int, bytes]:
    """Nasdaq's public API requires a browser-style User-Agent."""
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": _NASDAQ_UA},
    )
    return _default_request_transport(req)


def _nasdaq_asset_class(symbol: str, override: str | None = None) -> str:
    if override:
        normalized = override.strip().lower()
        if normalized in ("stocks", "etf"):
            return normalized
        raise ValueError(f"unsupported Nasdaq asset class: {override}")
    return "etf" if symbol.strip().upper() in NASDAQ_ETF_SYMBOLS else "stocks"


def nasdaq_quote(
    symbols: Sequence[str],
    asset_classes: Mapping[str, str] | None = None,
    transport: Transport = _nasdaq_transport,
) -> OpenFeedResult:
    """Fetch Nasdaq quote snapshots for watchlist symbols (no key required).

    Nasdaq rate-limits aggressively; batch callers should call this once per
    run and cache. Fail-closed on 429/transport errors.
    """
    overrides = asset_classes or {}
    rows = []
    for symbol in symbols:
        sym = str(symbol).strip().upper()
        if not sym or not sym.replace(".", "").replace("-", "").isalnum():
            raise ValueError(f"invalid Nasdaq symbol: {symbol}")
        asset_class = _nasdaq_asset_class(sym, overrides.get(sym))
        url = NASDAQ_API_URL.format(path=f"quote/{sym}/info") + "?" + urllib.parse.urlencode(
            {"assetclass": asset_class}
        )
        payload = _fetch_json(url, "nasdaq", transport)
        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            raise ValueError("nasdaq quote payload has no data object")
        primary = data.get("primaryData") if isinstance(data.get("primaryData"), dict) else {}
        rows.append({
            "symbol": sym,
            "assetClass": asset_class,
            "lastSalePrice": primary.get("lastSalePrice"),
            "netChange": primary.get("netChange"),
            "percentageChange": primary.get("percentageChange"),
            "lastTradeTimestamp": primary.get("lastTradeTimestamp"),
            "isRealTime": primary.get("isRealTime"),
            "bidPrice": primary.get("bidPrice"),
            "askPrice": primary.get("askPrice"),
        })
    return OpenFeedResult(provider_id="nasdaq", dataset="quote-info", rows=tuple(rows))


def nasdaq_option_chain(
    symbol: str,
    asset_class: str | None = None,
    limit: int = 200,
    transport: Transport = _nasdaq_transport,
) -> OpenFeedResult:
    """Fetch Nasdaq delayed option-chain rows for one symbol (no key required).

    Group-header rows (no strike) are dropped; each row carries call/put
    bid/ask/last/volume/open-interest per strike.
    """
    sym = str(symbol).strip().upper()
    if not sym:
        raise ValueError("Nasdaq option-chain symbol is required")
    limit = _positive_limit(limit, 5000)
    cls = _nasdaq_asset_class(sym, asset_class)
    query = urllib.parse.urlencode({"assetclass": cls, "limit": str(limit)})
    url = NASDAQ_API_URL.format(path=f"quote/{sym}/option-chain") + "?" + query
    payload = _fetch_json(url, "nasdaq", transport)
    data = payload.get("data") if isinstance(payload, dict) else None
    table = data.get("table") if isinstance(data, dict) else None
    raw_rows = table.get("rows") if isinstance(table, dict) else None
    if not isinstance(raw_rows, list):
        raise ValueError("nasdaq option-chain payload has no table rows")
    rows = []
    for row in raw_rows:
        if not isinstance(row, dict) or row.get("strike") in (None, ""):
            continue  # expiry group header, not a strike row
        rows.append({
            "symbol": sym,
            "expiryGroup": row.get("expirygroup"),
            "strike": row.get("strike"),
            "callLast": row.get("c_Last"),
            "callBid": row.get("c_Bid"),
            "callAsk": row.get("c_Ask"),
            "callVolume": row.get("c_Volume"),
            "callOpenInterest": row.get("c_Openinterest"),
            "putLast": row.get("p_Last"),
            "putBid": row.get("p_Bid"),
            "putAsk": row.get("p_Ask"),
            "putVolume": row.get("p_Volume"),
            "putOpenInterest": row.get("p_Openinterest"),
        })
    if not rows:
        raise ValueError("nasdaq option-chain payload has no strike rows")
    return OpenFeedResult(provider_id="nasdaq", dataset="option-chain", rows=tuple(rows))


def nasdaq_earnings_calendar(
    day,
    transport: Transport = _nasdaq_transport,
) -> OpenFeedResult:
    """Fetch Nasdaq's earnings-calendar rows for one date (no key required)."""
    import datetime as _dt
    if isinstance(day, (_dt.date, _dt.datetime)):
        day_str = day.strftime("%Y-%m-%d")
    else:
        day_str = str(day).strip()
        try:
            _dt.date.fromisoformat(day_str)
        except ValueError as exc:
            raise ValueError(f"invalid earnings-calendar date: {day}") from exc
    query = urllib.parse.urlencode({"date": day_str})
    url = NASDAQ_API_URL.format(path="calendar/earnings") + "?" + query
    payload = _fetch_json(url, "nasdaq", transport)
    data = payload.get("data") if isinstance(payload, dict) else None
    raw_rows = data.get("rows") if isinstance(data, dict) else None
    if not isinstance(raw_rows, list):
        raise ValueError("nasdaq earnings-calendar payload has no rows")
    rows = []
    for row in raw_rows:
        if isinstance(row, dict):
            item = dict(row)
            item["calendarDate"] = day_str
            rows.append(item)
    return OpenFeedResult(provider_id="nasdaq", dataset="earnings-calendar", rows=tuple(rows))



__all__ = [
    "BLS_MACRO_SERIES",
    "CFTC_COT_DATASETS",
    "ECB_FX_CURRENCIES",
    "FINRA_FIXED_INCOME_DATASETS",
    "NYFED_REFERENCE_RATES",
    "OpenFeedResult",
    "NASDAQ_ETF_SYMBOLS",
    "TREASURY_DGS_TENORS",
    "bls_latest_series",
    "bea_nipa",
    "cftc_cot",
    "ecb_exchange_rates",
    "eia_v2",
    "finra_fixed_income",
    "nasdaq_earnings_calendar",
    "nasdaq_option_chain",
    "nasdaq_quote",
    "world_bank_indicator",
    "treasury_yield_curve",
    "fdic_failures",
    "nyfed_reference_rates",
    "imf_gdp_growth",
    "oecd_composite_leading_indicator",
    "eurostat_quarterly_gdp",
    "usgs_earthquakes",
    "nasa_eonet_events",
    "bank_of_canada_fx",
    "frankfurter_fx",
    "sec_companyfacts",
    "sec_submissions",
    "treasury_latest_auctions",
]
