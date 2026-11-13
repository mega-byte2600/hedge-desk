"""Data-freshness gate for the after-close batch (honest point-in-time).

The batch runs after the close. The EOD source may not have
published today's bar yet, so the report must say whether it is running on
today's close or on the prior trading day's close — never silently present
yesterday's bar as today's.

The "today" in that sentence is market time, not server time: the batch runs
at 20:54 PT, which is 23:54 ET but already the next day in UTC. Deriving the
expected trading day from the UTC date made every Sunday–Thursday evening run
expect a close that cannot exist yet, so the gate failed closed on fresh data
eight nights running (2026-11-03/04/05/08/09/10/11/12). The expected day is therefore
the latest trading day whose 16:00 ET close has passed, computed in
America/New_York.

This is a pure, deterministic helper (no network): given the batch cutoff and the
per-symbol last-bar dates, it reports the expected trading day and whether the
data is current. Market holidays are approximated by weekdays; a holiday shows as
"not current" (honest, slightly conservative) rather than a fabricated today.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Iterable, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

FRESHNESS_VERSION = "hedge-desk-data-freshness-1.0.0"

# NYSE regular-session close; a trading day counts as complete once the
# market-time clock has passed it. EOD bars published after the close are
# covered by the fail-closed branch of freshness_summary (expected today,
# bars not yet present -> not current), never by moving the expectation.
MARKET_TIMEZONE = "America/New_York"
MARKET_CLOSE_TIME = time(16, 0)


def expected_trading_day(cutoff: date) -> date:
    """Most recent weekday (Mon-Fri) on or before ``cutoff``."""
    d = cutoff
    while d.weekday() >= 5:  # Sat=5, Sun=6
        d -= timedelta(days=1)
    return d


def latest_completed_trading_day(now: datetime) -> date:
    """Most recent trading day whose 16:00 ET close has passed.

    ``now`` must be timezone-aware; it is read in America/New_York. Before
    the 16:00 ET close, today has not completed, so the expectation is the
    previous trading day; from 16:00 ET on, it is today (rolled back over
    weekends). A run at 20:54 PT therefore expects that same day's close,
    not the next UTC day's.
    """
    if now.tzinfo is None:
        raise ValueError("cutoff must be timezone-aware")
    try:
        market_tz = ZoneInfo(MARKET_TIMEZONE)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("market timezone data unavailable") from exc
    market_now = now.astimezone(market_tz)
    base = market_now.date()
    if market_now.time() < MARKET_CLOSE_TIME:
        base -= timedelta(days=1)
    return expected_trading_day(base)


def _summarize(
    last_bar_dates: Iterable[str],
    expected: date,
) -> dict:
    dates = [d for d in last_bar_dates if d]
    as_of = max(dates) if dates else None
    is_current = as_of == expected.isoformat()
    if as_of is None:
        note = "No EOD bars present; batch has no close data."
    elif is_current:
        note = f"Running on {as_of} close (current trading day)."
    elif as_of > expected.isoformat():
        # Mid-session run: the source already shows a bar for a trading day
        # whose close has not happened yet (a partial bar). The gate must
        # neither certify it as the close nor claim the prior close is
        # "not yet published" — it is present; today simply has not closed.
        note = (
            f"Latest bar is {as_of}, from a trading day whose close has not "
            f"happened yet (expected completed trading day "
            f"{expected.isoformat()})."
        )
    else:
        note = (
            f"Running on {as_of} close; {expected.isoformat()} close not yet "
            "published by the source. Data is the prior trading day's close."
        )
    return {
        "schema_version": FRESHNESS_VERSION,
        "expected_trading_day": expected.isoformat(),
        "as_of": as_of,
        "is_current": is_current,
        "note": note,
    }


def freshness_summary(
    last_bar_dates: Iterable[str],
    cutoff: date,
) -> dict:
    """Summarize whether the batch is running on the current trading day's close.

    ``last_bar_dates`` are the per-symbol source last-bar dates (ISO strings).
    ``cutoff`` is a calendar date: the expected day is the most recent weekday
    on or before it. Callers with a timestamp should derive that date with
    :func:`latest_completed_trading_day` instead of passing a UTC date.
    Returns a schema-versioned dict with the expected trading day, the latest bar
    actually present, and an explicit ``is_current`` flag plus a human note.
    """
    return _summarize(last_bar_dates, expected_trading_day(cutoff))


__all__ = [
    "FRESHNESS_VERSION",
    "MARKET_TIMEZONE",
    "MARKET_CLOSE_TIME",
    "expected_trading_day",
    "freshness_summary",
    "latest_completed_trading_day",
]
