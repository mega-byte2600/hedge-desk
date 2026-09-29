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
# ECB euro reference rates: the SDMX Data Portal endpoint intermittently closes
# connections, so use the classic daily eurofxref feed (same official data).
ECB_EUROFXREF_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
TREASURY_DAILY_RATES_URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
FDIC_FAILURES_URL = "https://api.fdic.gov/banks/failures"
WORLD_BANK_INDICATOR_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"

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
    "sec_companyfacts",
    "sec_submissions",
    "treasury_latest_auctions",
]
