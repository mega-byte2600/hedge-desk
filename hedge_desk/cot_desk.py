"""CFTC Commitments of Traders (COT) adapter — free, no key, official.

Pulls futures positioning data from the CFTC's public Socrata API. Shows
how traders are positioned (long/short/spread) by category: commercial
(hedgers), non-commercial (speculators), and non-reportable.

Use for: futures catalysts desk — crowding/positioning context, extreme
positioning as a contrarian or trend-confirmation signal.

Source: https://publicreporting.cftc.gov (CFTC public reporting API)
No key required. Data published weekly (Fridays, as of prior Tuesday).
"""

from __future__ import annotations

import datetime as _dt
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

# Socrata API for COT data. 6dca-aqww = Futures Only COT.
COT_API_URL = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"

Transport = Callable[[str], Tuple[int, bytes]]


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "hedge-desk/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return resp.status, body
    except Exception:
        return 0, b""


@dataclass(frozen=True)
class CotReport:
    """One COT report row for a single market."""

    commodity_name: str
    market_name: str
    report_date: str
    open_interest: int
    # Non-commercial (speculators)
    noncomm_long: int
    noncomm_short: int
    noncomm_spread: int
    # Commercial (hedgers)
    comm_long: int
    comm_short: int
    # Derived: net positioning
    noncomm_net: int
    comm_net: int

    def noncomm_net_pct_oi(self) -> float:
        """Non-commercial net as % of open interest. Positive = net long."""
        if self.open_interest <= 0:
            return 0.0
        return 100.0 * self.noncomm_net / self.open_interest


def _int(value: object) -> int:
    try:
        return int(str(value).replace(",", ""))
    except (ValueError, TypeError):
        return 0


def fetch_cot(
    commodity: Optional[str] = None,
    limit: int = 10,
    transport: Transport = _default_transport,
    retries: int = 2,
) -> List[CotReport]:
    """Fetch recent COT reports. Optionally filter by commodity name.

    Returns newest first. Retries transient failures with backoff.
    Raises ValueError on persistent failure (fail closed).
    """
    params = {
        "$limit": str(limit),
        "$order": "report_date_as_yyyy_mm_dd DESC",
    }
    if commodity:
        # Socrata SoQL: match on the CFTC commodity code when the input
        # looks like one (e.g. '088651'), otherwise exact commodity name.
        # Substring matching caused false hits (e.g. 'CRUDE OIL' matching
        # 'FUEL OIL/CRUDE OIL'), so prefer exact matches.
        code = commodity.strip().upper()
        if code.isdigit():
            params["$where"] = f"cftc_commodity_code = '{code}'"
        else:
            params["$where"] = f"upper(commodity_name) = '{code}'"
    url = f"{COT_API_URL}?{urllib.parse.urlencode(params)}"
    last_status: int | None = None
    for attempt in range(retries + 1):
        status, raw = transport(url)
        last_status = status
        if status == 200 and raw:
            break
        if attempt < retries:
            time.sleep(2 ** attempt)
    else:
        raise ValueError(f"cftc COT fetch failed (status {last_status})")
    if status != 200 or not raw:
        raise ValueError(f"cftc COT fetch failed (status {status})")
    try:
        rows = json.loads(raw.decode("utf-8"))
    except ValueError as e:
        raise ValueError(f"cftc COT bad JSON: {e}") from e
    if not isinstance(rows, list):
        raise ValueError("cftc COT unexpected response shape")
    reports = []
    for r in rows:
        noncomm_long = _int(r.get("noncomm_positions_long_all"))
        noncomm_short = _int(r.get("noncomm_positions_short_all"))
        comm_long = _int(r.get("comm_positions_long_all"))
        comm_short = _int(r.get("comm_positions_short_all"))
        reports.append(
            CotReport(
                commodity_name=str(r.get("commodity_name", "")),
                market_name=str(r.get("market_and_exchange_names", "")),
                report_date=str(r.get("report_date_as_yyyy_mm_dd", ""))[:10],
                open_interest=_int(r.get("open_interest_all")),
                noncomm_long=noncomm_long,
                noncomm_short=noncomm_short,
                noncomm_spread=_int(r.get("noncomm_postions_spread_all")),
                comm_long=comm_long,
                comm_short=comm_short,
                noncomm_net=noncomm_long - noncomm_short,
                comm_net=comm_long - comm_short,
            )
        )
    return reports


def cot_summary(
    commodity: str,
    transport: Transport = _default_transport,
) -> Dict[str, object]:
    """One-market COT summary for the futures desk. Fail-closed on error."""
    try:
        reports = fetch_cot(commodity=commodity, limit=1, transport=transport)
    except ValueError as e:
        return {
            "mode": "BLOCKED",
            "commodity": commodity,
            "reason": str(e),
            "data_source": "cftc-public-socrata",
        }
    if not reports:
        return {
            "mode": "BLOCKED",
            "commodity": commodity,
            "reason": f"no COT data for {commodity}",
            "data_source": "cftc-public-socrata",
        }
    r = reports[0]
    return {
        "schema_version": "hedge-desk-cot-1.0.0",
        "mode": "REAL_CFTC_COT",
        "commodity": r.commodity_name,
        "market": r.market_name,
        "report_date": r.report_date,
        "open_interest": r.open_interest,
        "noncomm_long": r.noncomm_long,
        "noncomm_short": r.noncomm_short,
        "noncomm_spread": r.noncomm_spread,
        "noncomm_net": r.noncomm_net,
        "noncomm_net_pct_oi": round(r.noncomm_net_pct_oi(), 2),
        "comm_long": r.comm_long,
        "comm_short": r.comm_short,
        "comm_net": r.comm_net,
        "data_source": "cftc-public-socrata",
        "note": (
            "CFTC Commitments of Traders. Non-commercial = speculators; "
            "commercial = hedgers. Weekly, as of Tuesday."
        ),
    }


__all__ = ["CotReport", "fetch_cot", "cot_summary"]
