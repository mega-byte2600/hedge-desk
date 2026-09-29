"""Production launcher with a sanitized EIA connectivity probe.

The probe validates the configured server-side EIA credential against the exact
petroleum inventory dataset used by Hedge Desk. It logs only provider status and
row count; credentials and payload contents are never emitted. A failed external
probe does not prevent the web process from starting because the application
itself already fails the EIA source closed as BLOCKED/UNCONFIGURED.
"""

from __future__ import annotations

import os

from hedge_desk.data.open_market_feeds import eia_v2
from hedge_desk.web_app import main as serve


def probe_eia_startup() -> str:
    """Return and log a secret-free EIA production connectivity status."""
    if not os.environ.get("EIA_API_KEY", "").strip():
        status = "UNCONFIGURED"
        print("production_probe provider=eia-open-data status=UNCONFIGURED rows=0", flush=True)
        return status

    try:
        result = eia_v2("petroleum/stoc/wstk", data=("value",), limit=1)
        rows = result.row_count
        status = "LIVE" if rows > 0 else "BLOCKED"
    except Exception:
        rows = 0
        status = "BLOCKED"

    print(
        f"production_probe provider=eia-open-data status={status} rows={rows}",
        flush=True,
    )
    return status


def main() -> None:
    probe_eia_startup()
    serve()


__all__ = ["main", "probe_eia_startup"]
