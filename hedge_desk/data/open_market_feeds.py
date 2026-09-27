"""Free/open authoritative market-data adapters for paper research.

The adapters in this module deliberately prefer regulators, government agencies,
and public market-structure datasets over scraped web pages or unlicensed feeds.
They are read-only, use the Python standard library, and fail closed on transport
or payload errors.

No function in this module authorizes a trade or places an order.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence, Tuple


Transport = Callable[[str], Tuple[int, bytes]]

TREASURY_AUCTIONS_URL = (
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    "v1/accounting/od/auctions_query"
)
FINRA_DATA_URL = "https://api.finra.org/data/group/{group}/name/{dataset}"
CFTC_SODA_URL = "https://publicreporting.cftc.gov/resource/{dataset}.json"
EIA_V2_URL = "https://api.eia.gov/v2/{route}/data/"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# Public FINRA fixed-income datasets that are directly useful to a rates/credit desk.
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


@dataclass(frozen=True)
class OpenFeedResult:
    provider_id: str
    dataset: str
    rows: Tuple[Mapping[str, object], ...]

    @property
    def row_count(self) -> int:
        return len(self.rows)


def _default_transport(url: str) -> Tuple[int, bytes]:
    user_agent = os.environ.get(
        "MARKET_DATA_USER_AGENT",
        "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
    ).strip()
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _fetch_json(url: str, provider: str, transport: Transport) -> object:
    try:
        status, raw = transport(url)
    except Exception as exc:
        raise ValueError(f"{provider} transport failed") from exc
    if status != 200 or not raw:
        raise ValueError(f"{provider} fetch failed (status {status})")
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"{provider} returned malformed JSON") from exc


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


def finra_fixed_income(
    dataset: str,
    limit: int = 50,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch a vetted public FINRA fixed-income market dataset (no key)."""
    if dataset not in FINRA_FIXED_INCOME_DATASETS:
        raise ValueError(f"unsupported FINRA fixed-income dataset: {dataset}")
    limit = _positive_limit(limit, 5000)
    base = FINRA_DATA_URL.format(group="fixedIncomeMarket", dataset=dataset)
    query = urllib.parse.urlencode({"limit": str(limit)})
    payload = _fetch_json(f"{base}?{query}", "finra", transport)
    return OpenFeedResult(
        provider_id="finra",
        dataset=dataset,
        rows=_rows_from_list(payload, "finra"),
    )


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
    transport: Transport = _default_transport,
) -> Mapping[str, object]:
    """Fetch SEC EDGAR company submission history (no API key)."""
    normalized = _normalize_cik(cik)
    payload = _fetch_json(SEC_SUBMISSIONS_URL.format(cik=normalized), "sec-edgar", transport)
    if not isinstance(payload, dict) or "cik" not in payload:
        raise ValueError("sec-edgar submissions payload is malformed")
    return payload


def sec_companyfacts(
    cik: str | int,
    transport: Transport = _default_transport,
) -> Mapping[str, object]:
    """Fetch SEC XBRL company facts for one issuer (no API key)."""
    normalized = _normalize_cik(cik)
    payload = _fetch_json(SEC_COMPANYFACTS_URL.format(cik=normalized), "sec-edgar", transport)
    if not isinstance(payload, dict) or "facts" not in payload:
        raise ValueError("sec-edgar companyfacts payload is malformed")
    return payload


__all__ = [
    "CFTC_COT_DATASETS",
    "FINRA_FIXED_INCOME_DATASETS",
    "OpenFeedResult",
    "cftc_cot",
    "eia_v2",
    "finra_fixed_income",
    "sec_companyfacts",
    "sec_submissions",
    "treasury_latest_auctions",
]
