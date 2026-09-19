"""Data-freshness gate for the after-close batch (honest point-in-time).

The batch runs at 4:30pm EST after the close. The EOD source may not have
published today's bar yet, so the report must say whether it is running on
today's close or on the prior trading day's close — never silently present
yesterday's bar as today's.

This is a pure, deterministic helper (no network): given the batch cutoff and the
per-symbol last-bar dates, it reports the expected trading day and whether the
data is current. Market holidays are approximated by weekdays; a holiday shows as
"not current" (honest, slightly conservative) rather than a fabricated today.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable, Sequence

FRESHNESS_VERSION = "hedge-desk-data-freshness-1.0.0"


def expected_trading_day(cutoff: date) -> date:
    """Most recent weekday (Mon-Fri) on or before ``cutoff``."""
    d = cutoff
    while d.weekday() >= 5:  # Sat=5, Sun=6
        d -= timedelta(days=1)
    return d


def freshness_summary(
    last_bar_dates: Iterable[str],
    cutoff: date,
) -> dict:
    """Summarize whether the batch is running on the current trading day's close.

    ``last_bar_dates`` are the per-symbol source last-bar dates (ISO strings).
    Returns a schema-versioned dict with the expected trading day, the latest bar
    actually present, and an explicit ``is_current`` flag plus a human note.
    """
    dates = [d for d in last_bar_dates if d]
    as_of = max(dates) if dates else None
    expected = expected_trading_day(cutoff)
    is_current = as_of == expected.isoformat()
    if as_of is None:
        note = "No EOD bars present; batch has no close data."
    elif is_current:
        note = f"Running on {as_of} close (current trading day)."
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


__all__ = ["FRESHNESS_VERSION", "expected_trading_day", "freshness_summary"]