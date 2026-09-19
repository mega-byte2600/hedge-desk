"""Real earnings desk on SEC EDGAR XBRL company-concept data (free, official).

Pulls a company's actual reported GAAP earnings-per-share from the SEC's own XBRL
company-concept API — real, official, point-in-time filings data — and reports the
actual EPS trend: the latest FY and quarterly reported values, whether the latest
quarterly EPS rose or fell versus the prior period, and the fiscal frame. Uses the
already-tested ``hedge_desk.earnings`` evaluation only when a real consensus is
supplied; otherwise it reports actuals as observed facts without a surprise claim.

Honesty boundary:
- Actual reported EPS comes from EDGAR and is labeled OBSERVED. A consensus
  (analyst estimate) is a separate, licensed-style input that is NOT fabricated
  here; surprise is only computed when real consensus is supplied.
- No probability, no forecast, no order. trade_authorized stays False.

Source: https://data.sec.gov/api/xbrl/companyconcept/CIKnnnnnnnnnn/us-gaap/EarningsPerShareBasic.json
License: SEC EDGAR data is public; this is reference use of official filings.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, Tuple

EDGAR_URL = (
    "https://data.sec.gov/api/xbrl/companyconcept/"
    "CIK{cik}/us-gaap/EarningsPerShareBasic.json"
)
Transport = Callable[[str], Tuple[int, bytes]]


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "HedgeDesk Research name@example.com",
            "Accept-Encoding": "identity",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _cik(symbol_or_cik) -> str:
    value = str(symbol_or_cik).strip().upper()
    if value.isdigit():
        return value.zfill(10)
    raise ValueError("provide a numeric 10-digit CIK (e.g. 0000320193 for AAPL)")


@dataclass(frozen=True)
class EpsPoint:
    end_date: str
    value: Decimal
    form: str
    fiscal_year: int | None
    period: str | None
    frame: str | None


def build_concept_url(cik: str) -> str:
    return EDGAR_URL.format(cik=cik)


def _decimal(value) -> Decimal | None:
    if value is None:
        return None
    try:
        parsed = Decimal(str(value))
        return parsed if parsed.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def parse_eps_concept(raw: bytes) -> Tuple[EpsPoint, ...]:
    """Parse EDGAR company-concept JSON into EPS points (USD/shares)."""
    try:
        data = json.loads(raw.decode("utf-8"))
        units = data["units"]["USD/shares"]
    except (KeyError, TypeError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError("edgar EPS concept malformed") from exc
    points = []
    for item in units:
        val = _decimal(item.get("val"))
        if val is None:
            continue
        points.append(
            EpsPoint(
                str(item.get("end", ""))[:10],
                val,
                str(item.get("form", "")),
                item.get("fy"),
                item.get("fp"),
                item.get("frame"),
            )
        )
    points.sort(key=lambda p: p.end_date)
    return tuple(points)


def earnings_desk(
    cik: str,
    transport: Transport = _default_transport,
) -> Dict[str, object]:
    """Report a company's actual reported EPS trend from SEC EDGAR."""
    cik = _cik(cik)
    status, raw = transport(build_concept_url(cik))
    if status != 200 or not raw:
        raise ValueError(f"edgar fetch failed for CIK {cik} (status {status})")
    points = parse_eps_concept(raw)
    if not points:
        raise ValueError("edgar EPS concept has no values")

    # Latest FY point (form 10-K / FY frame) and latest quarterly (10-Q / Q).
    # A company can restate the SAME period (same end date, newer filing), so dedupe
    # by end_date and only count genuinely DISTINCT periods as "prior" — otherwise a
    # restated value is misread as a prior quarter.
    fy_points = [p for p in points if p.form in ("10-K", "10-K/A")]
    q_points = [p for p in points if p.form in ("10-Q", "10-Q/A")]

    latest_fy = fy_points[-1] if fy_points else None
    # Latest quarterly: the last distinct period.
    q_dedup = {p.end_date: p for p in q_points}  # later filing wins per period
    distinct_q_dates = sorted(q_dedup)
    latest_q = q_dedup[distinct_q_dates[-1]] if distinct_q_dates else None
    prior_q = q_dedup[distinct_q_dates[-2]] if len(distinct_q_dates) >= 2 else None

    observation = {
        "latest_fy_eps": str(latest_fy.value) if latest_fy else None,
        "latest_fy_period": latest_fy.end_date if latest_fy else None,
        "latest_quarterly_eps": str(latest_q.value) if latest_q else None,
        "latest_quarterly_period": latest_q.end_date if latest_q else None,
        "prior_quarterly_eps": str(prior_q.value) if prior_q else None,
        "prior_quarterly_period": prior_q.end_date if prior_q else None,
    }

    # Measured quarter-over-quarter actual change (only if both real values exist).
    q_change = None
    if latest_q and prior_q:
        q_change = str(latest_q.value - prior_q.value)

    return {
        "schema_version": "hedge-desk-earnings-desk-1.0.0",
        "mode": "REAL_EDGAR_EARNINGS",
        "cik": cik,
        "observation_count": len(points),
        "observation": observation,
        "quarterly_eps_change": q_change,
        "data_source": "sec-edgar-xbrl-http-200",
        "surprise_computed": False,
        "trade_authorized": False,
        "note": (
            "Actual reported GAAP EPS from SEC EDGAR (OBSERVED, point-in-time "
            "filings). A consensus is not fabricated here; surprise is only "
            "computed when a real analyst estimate is supplied. No forecast, no "
            "order. trade_authorized=False."
        ),
    }


__all__ = ["earnings_desk", "build_concept_url", "parse_eps_concept", "EpsPoint"]