"""Nasdaq corporate-actions calendars (keyless, no API key).

Endpoints (verified live 2026-10-04 with the browser User-Agent copied from
hedge_desk/data/open_market_feeds.py::_nasdaq_transport):
  - https://api.nasdaq.com/api/calendar/dividends?date=YYYY-MM-DD
  - https://api.nasdaq.com/api/calendar/splits?date=YYYY-MM-DD

Feeds: Dividend Opportunity desk (ex-date / pay-date / yield fields) and
candidate corporate actions. Fail closed on transport errors, non-200 status,
or malformed payloads. Rows keep the raw Nasdaq fields plus ISO-normalized
date fields; a row with an unparsable date keeps the raw value and gets
None for the ISO field (a date-format quirk is not a payload failure).

Nasdaq rate-limits aggressively; callers must cache once per run, same as the
existing nasdaq_quote adapter.
"""

from __future__ import annotations

import datetime as _dt
import urllib.parse
from typing import Callable, Mapping

from .feed_base import (
    FeedResult,
    Transport,
    _fetch_json,
    _nasdaq_transport,
    _normalize_iso_date,
    _rows_from_list,
    utc_now_iso,
)

NASDAQ_DIVIDENDS_URL = "https://api.nasdaq.com/api/calendar/dividends"
NASDAQ_SPLITS_URL = "https://api.nasdaq.com/api/calendar/splits"


def _validate_day(day: object) -> str:
    if isinstance(day, (_dt.date, _dt.datetime)):
        return day.strftime("%Y-%m-%d")
    day_str = str(day).strip()
    try:
        _dt.date.fromisoformat(day_str)
    except ValueError as exc:
        raise ValueError(f"invalid nasdaq calendar date: {day}") from exc
    return day_str


def _rows_from_calendar_payload(payload: object, provider: str) -> tuple:
    if not isinstance(payload, dict):
        raise ValueError(f"{provider} payload is not an object")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError(f"{provider} payload has no data object")
    calendar = data.get("calendar")
    if isinstance(calendar, dict):
        raw_rows = calendar.get("rows")
    else:  # splits calendar nests rows directly under data
        raw_rows = data.get("rows")
    return _rows_from_list(raw_rows, provider)


def _normalize_row(
    row: Mapping[str, object], date_fields: tuple, calendar_date: str
) -> Mapping[str, object]:
    item = dict(row)
    for field in date_fields:
        item[f"{field}_iso"] = _normalize_iso_date(item.get(field))
    item["calendarDate"] = calendar_date
    return item


def nasdaq_dividends_calendar(
    day: object,
    transport: Transport = _nasdaq_transport,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Dividend-calendar rows for one date (YYYY-MM-DD)."""
    day_str = _validate_day(day)
    url = NASDAQ_DIVIDENDS_URL + "?" + urllib.parse.urlencode({"date": day_str})
    payload = _fetch_json(url, "nasdaq-calendars", transport)
    rows = _rows_from_calendar_payload(payload, "nasdaq-calendars")
    normalized = tuple(
        _normalize_row(
            row,
            ("dividend_Ex_Date", "payment_Date", "record_Date", "announcement_Date"),
            day_str,
        )
        for row in rows
    )
    return FeedResult(
        provider_id="nasdaq-calendars",
        dataset="dividends-calendar",
        rows=normalized,
        fetched_at=now(),
    )


def nasdaq_splits_calendar(
    day: object,
    transport: Transport = _nasdaq_transport,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Split-calendar rows for one date (YYYY-MM-DD)."""
    day_str = _validate_day(day)
    url = NASDAQ_SPLITS_URL + "?" + urllib.parse.urlencode({"date": day_str})
    payload = _fetch_json(url, "nasdaq-calendars", transport)
    rows = _rows_from_calendar_payload(payload, "nasdaq-calendars")
    normalized = tuple(
        _normalize_row(row, ("executionDate",), day_str) for row in rows
    )
    return FeedResult(
        provider_id="nasdaq-calendars",
        dataset="splits-calendar",
        rows=normalized,
        fetched_at=now(),
    )


__all__ = [
    "NASDAQ_DIVIDENDS_URL",
    "NASDAQ_SPLITS_URL",
    "nasdaq_dividends_calendar",
    "nasdaq_splits_calendar",
]
