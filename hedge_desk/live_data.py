"""Operational public-data adapters for Emporion.

Production-facing code never substitutes test fixtures for missing market data.
All observations retain source, provider timestamp, receipt time, expected delay,
freshness, and use-scope metadata. No output is trade-authorized.
"""

from __future__ import annotations

import copy
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Callable
from urllib.request import Request, urlopen

from hedge_desk.candidates import build_candidate_feed

LIVE_SCHEMA_VERSION = "emporion-candidates-1.1.0"
CACHE_TTL_SECONDS = 900
TREASURY_URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value={year}"
)
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
SEC_CIKS = {
    "AAPL": 320193,
    "NVDA": 1045810,
    "KO": 21344,
    "JNJ": 200406,
}
_CACHE: dict[str, object] = {"expires_at": 0.0, "payload": None}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _request_text(url: str, *, user_agent: str, timeout: int = 12) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/json, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def _request_json(url: str, *, user_agent: str, timeout: int = 12) -> dict:
    return json.loads(_request_text(url, user_agent=user_agent, timeout=timeout))


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _iso(value: str) -> str:
    value = value.strip()
    if "T" in value:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        parsed = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def fetch_treasury_curve(
    *,
    now: datetime | None = None,
    fetch_text: Callable[[str], str] | None = None,
) -> dict:
    """Fetch the latest official U.S. Treasury par-yield curve observation."""
    now = now or _utc_now()
    url = TREASURY_URL.format(year=now.year)
    user_agent = os.getenv(
        "EMPORION_USER_AGENT",
        "EmporionResearch/0.1 (+https://github.com/mega-byte2600/hedge-desk)",
    )
    try:
        text = fetch_text(url) if fetch_text else _request_text(url, user_agent=user_agent)
        root = ET.fromstring(text)
        rows: list[dict[str, str]] = []
        for node in root.iter():
            if _local_name(node.tag) != "properties":
                continue
            row = {_local_name(child.tag): (child.text or "").strip() for child in node}
            if row.get("NEW_DATE"):
                rows.append(row)
        if not rows:
            raise ValueError("no Treasury observations")
        row = max(rows, key=lambda item: item["NEW_DATE"])
        observed_at = _iso(row["NEW_DATE"])
        observed_dt = datetime.fromisoformat(observed_at)
        age_seconds = max(0, int((now - observed_dt).total_seconds()))
        curve_map = {
            "1M": "BC_1MONTH",
            "3M": "BC_3MONTH",
            "6M": "BC_6MONTH",
            "1Y": "BC_1YEAR",
            "2Y": "BC_2YEAR",
            "3Y": "BC_3YEAR",
            "5Y": "BC_5YEAR",
            "7Y": "BC_7YEAR",
            "10Y": "BC_10YEAR",
            "20Y": "BC_20YEAR",
            "30Y": "BC_30YEAR",
        }
        curve = {}
        for maturity, field in curve_map.items():
            raw = row.get(field)
            if raw not in (None, "", "N/A"):
                try:
                    curve[maturity] = float(raw)
                except ValueError:
                    continue
        if not curve:
            raise ValueError("Treasury curve fields unavailable")
        return {
            "source_id": "us-treasury-daily-par-yield-curve",
            "provider": "U.S. Department of the Treasury",
            "source_kind": "PUBLIC_GOVERNMENT",
            "source_url": url,
            "available": True,
            "observed_at": observed_at,
            "received_at": now.isoformat(),
            "age_seconds": age_seconds,
            "expected_delay": "End-of-day official publication; weekends and federal holidays can extend age.",
            "freshness_state": "CURRENT_OR_EXPECTED_DELAY" if age_seconds <= 4 * 86400 else "STALE",
            "use_scope": "PUBLIC_RESEARCH_SOURCE; downstream redistribution terms must still be respected.",
            "unit": "PERCENT",
            "curve": curve,
        }
    except Exception as exc:
        return {
            "source_id": "us-treasury-daily-par-yield-curve",
            "provider": "U.S. Department of the Treasury",
            "source_kind": "PUBLIC_GOVERNMENT",
            "source_url": url,
            "available": False,
            "observed_at": None,
            "received_at": now.isoformat(),
            "age_seconds": None,
            "expected_delay": "End-of-day official publication; weekends and federal holidays can extend age.",
            "freshness_state": "UNAVAILABLE",
            "use_scope": "PUBLIC_RESEARCH_SOURCE; downstream redistribution terms must still be respected.",
            "error": type(exc).__name__,
        }


def fetch_sec_submission_context(
    ticker: str,
    cik: int,
    *,
    now: datetime | None = None,
    fetch_json: Callable[[str], dict] | None = None,
) -> dict:
    """Fetch the latest 10-K/10-Q/8-K filing metadata from the SEC submissions API."""
    now = now or _utc_now()
    url = SEC_SUBMISSIONS_URL.format(cik=cik)
    user_agent = os.getenv(
        "SEC_USER_AGENT",
        "EmporionResearch/0.1 (+https://github.com/mega-byte2600/hedge-desk)",
    )
    try:
        payload = fetch_json(url) if fetch_json else _request_json(url, user_agent=user_agent)
        recent = payload.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        filed = recent.get("filingDate", [])
        accession = recent.get("accessionNumber", [])
        primary = recent.get("primaryDocument", [])
        choices = []
        for index, form in enumerate(forms):
            if form not in {"10-K", "10-Q", "8-K"} or index >= len(filed):
                continue
            choices.append(
                (
                    filed[index],
                    form,
                    accession[index] if index < len(accession) else "",
                    primary[index] if index < len(primary) else "",
                )
            )
        if not choices:
            raise ValueError("no current SEC filing metadata")
        filing_date, form, accession_number, primary_document = max(choices, key=lambda item: item[0])
        observed_at = _iso(filing_date)
        age_seconds = max(0, int((now - datetime.fromisoformat(observed_at)).total_seconds()))
        return {
            "source_id": "sec-edgar-submissions",
            "provider": "U.S. Securities and Exchange Commission",
            "source_kind": "PUBLIC_GOVERNMENT",
            "source_url": url,
            "available": True,
            "ticker": ticker,
            "cik": cik,
            "form": form,
            "accession_number": accession_number,
            "primary_document": primary_document,
            "observed_at": observed_at,
            "received_at": now.isoformat(),
            "age_seconds": age_seconds,
            "expected_delay": "SEC filing metadata updates after accepted EDGAR submissions.",
            "freshness_state": "CURRENT_FILING_CONTEXT",
            "use_scope": "PUBLIC_RESEARCH_SOURCE; automated access must follow SEC fair-access guidance.",
        }
    except Exception as exc:
        return {
            "source_id": "sec-edgar-submissions",
            "provider": "U.S. Securities and Exchange Commission",
            "source_kind": "PUBLIC_GOVERNMENT",
            "source_url": url,
            "available": False,
            "ticker": ticker,
            "cik": cik,
            "observed_at": None,
            "received_at": now.isoformat(),
            "age_seconds": None,
            "expected_delay": "SEC filing metadata updates after accepted EDGAR submissions.",
            "freshness_state": "UNAVAILABLE",
            "use_scope": "PUBLIC_RESEARCH_SOURCE; automated access must follow SEC fair-access guidance.",
            "error": type(exc).__name__,
        }


def _rates_candidates(treasury: dict) -> list[dict]:
    if not treasury.get("available"):
        return []
    out = []
    for maturity in ("2Y", "5Y", "10Y", "30Y"):
        value = treasury.get("curve", {}).get(maturity)
        if value is None:
            continue
        out.append(
            {
                "desk_id": "open-quant-ai-model-lab",
                "symbol": f"UST{maturity}",
                "instrument_type": "US_TREASURY_PAR_YIELD",
                "stage": "OBSERVED_PUBLIC_RATE",
                "method": "Rates and curve regime context for cross-asset quantitative research.",
                "evidence_needed": "History, curve transforms, financing context, and desk-specific qualification before any actionable conclusion.",
                "trade_authorized": False,
                "method_qualified": False,
                "source_id": treasury["source_id"],
                "provider": treasury["provider"],
                "observed_at": treasury["observed_at"],
                "expected_delay": treasury["expected_delay"],
                "freshness_state": treasury["freshness_state"],
                "observed_value": value,
                "observed_unit": treasury["unit"],
            }
        )
    return out


def build_operational_candidate_feed(
    *,
    now: datetime | None = None,
    fetch_text: Callable[[str], str] | None = None,
    fetch_json: Callable[[str], dict] | None = None,
    use_cache: bool = True,
) -> dict:
    """Return source-enriched candidates without ever fabricating missing observations."""
    now = now or _utc_now()
    if use_cache and _CACHE["payload"] is not None and time.monotonic() < float(_CACHE["expires_at"]):
        return copy.deepcopy(_CACHE["payload"])

    treasury = fetch_treasury_curve(now=now, fetch_text=fetch_text)
    sec = {
        ticker: fetch_sec_submission_context(ticker, cik, now=now, fetch_json=fetch_json)
        for ticker, cik in SEC_CIKS.items()
    }

    base = build_candidate_feed()
    candidates = []
    for original in base["candidates"]:
        row = dict(original)
        row["method_qualified"] = False
        row["source_context"] = []
        if row["symbol"] in sec:
            context = sec[row["symbol"]]
            row["source_context"].append(
                {
                    key: context.get(key)
                    for key in (
                        "source_id",
                        "provider",
                        "available",
                        "form",
                        "observed_at",
                        "expected_delay",
                        "freshness_state",
                    )
                    if key in context
                }
            )
        if treasury.get("available") and row["desk_id"] in {
            "overnight-premium-desk",
            "arbitrage-observer",
            "open-quant-ai-model-lab",
            "event-futures-desk",
        }:
            row["source_context"].append(
                {
                    "source_id": treasury["source_id"],
                    "provider": treasury["provider"],
                    "available": True,
                    "observed_at": treasury["observed_at"],
                    "expected_delay": treasury["expected_delay"],
                    "freshness_state": treasury["freshness_state"],
                }
            )
        candidates.append(row)

    candidates.extend(_rates_candidates(treasury))
    sources = [treasury, *sec.values()]
    available_count = sum(1 for source in sources if source.get("available"))
    payload = {
        "schema_version": LIVE_SCHEMA_VERSION,
        "mode": "RESEARCH_ONLY",
        "candidate_definition": "SOURCE_ENRICHED_RESEARCH_UNIVERSE_NOT_TRADE_AUTHORIZED",
        "generated_at": now.isoformat(),
        "refresh_policy_seconds": CACHE_TTL_SECONDS,
        "data_state": "PARTIAL_PUBLIC_DATA" if available_count else "PUBLIC_DATA_UNAVAILABLE",
        "data_priority": "BONDS_RATES_CREDIT_FIRST",
        "sources_available": available_count,
        "sources_total": len(sources),
        "sources": sources,
        "candidates": candidates,
    }
    if use_cache:
        _CACHE["payload"] = copy.deepcopy(payload)
        _CACHE["expires_at"] = time.monotonic() + CACHE_TTL_SECONDS
    return payload
