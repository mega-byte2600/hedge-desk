"""Direct New York Fed reference-rate market-data adapter.

Official, no-key, read-only source for SOFR, EFFR, OBFR, TGCR and BGCR.
This module provides observations only. It cannot authorize or place trades.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Callable, Optional, Tuple


LATEST_URL = "https://markets.newyorkfed.org/api/rates/all/latest.json"
HISTORY_URL = (
    "https://markets.newyorkfed.org/api/rates/{segment}/{rate}/last/{limit}.json"
)

Transport = Callable[[str], Tuple[int, bytes]]

_RATE_PATHS = {
    "SOFR": ("secured", "sofr"),
    "TGCR": ("secured", "tgcr"),
    "BGCR": ("secured", "bgcr"),
    "EFFR": ("unsecured", "effr"),
    "OBFR": ("unsecured", "obfr"),
}


@dataclass(frozen=True)
class ReferenceRate:
    rate_type: str
    effective_date: str
    percent_rate: Decimal
    volume_billions: Optional[Decimal]
    source_id: str = "nyfed-markets"


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "hedge-desk/1.0 research",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _decimal(value: object) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def _fetch(url: str, transport: Transport) -> Tuple[ReferenceRate, ...]:
    status, raw = transport(url)
    if status != 200 or not raw:
        raise ValueError("NY Fed reference-rate fetch failed (status %s)" % status)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("NY Fed reference-rate payload is malformed JSON") from exc
    rows = payload.get("refRates") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError("NY Fed reference-rate payload has no refRates rows")

    observations = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        rate_type = str(row.get("type", "")).strip().upper()
        effective_date = str(row.get("effectiveDate", "")).strip()
        percent_rate = _decimal(row.get("percentRate"))
        if rate_type not in _RATE_PATHS or not effective_date or percent_rate is None:
            continue
        observations.append(
            ReferenceRate(
                rate_type=rate_type,
                effective_date=effective_date,
                percent_rate=percent_rate,
                volume_billions=_decimal(row.get("volumeInBillions")),
            )
        )
    if not observations:
        raise ValueError("NY Fed reference-rate payload has no usable observations")
    return tuple(observations)


def latest_reference_rates(
    transport: Transport = _default_transport,
) -> Tuple[ReferenceRate, ...]:
    """Return the latest published NY Fed reference-rate observations."""
    return _fetch(LATEST_URL, transport)


def reference_rate_history(
    rate_type: str,
    limit: int = 20,
    transport: Transport = _default_transport,
) -> Tuple[ReferenceRate, ...]:
    """Return recent observations for one supported NY Fed reference rate."""
    normalized = str(rate_type).strip().upper()
    if normalized not in _RATE_PATHS:
        raise ValueError("unsupported NY Fed reference rate: %s" % rate_type)
    if type(limit) is not int or limit < 1 or limit > 1000:
        raise ValueError("limit must be an integer from 1 to 1000")
    segment, slug = _RATE_PATHS[normalized]
    url = HISTORY_URL.format(segment=segment, rate=slug, limit=limit)
    observations = _fetch(url, transport)
    return tuple(row for row in observations if row.rate_type == normalized)


__all__ = [
    "ReferenceRate",
    "latest_reference_rates",
    "reference_rate_history",
]
