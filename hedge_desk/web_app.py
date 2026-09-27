"""Production WSGI entry point for market-data health and normalized context.

All existing web behavior delegates to :mod:`hedge_desk.server`. This module
adds two bounded operational/research endpoints:

``/api/data-sources`` verifies connectivity without returning provider payloads.
``/api/market-context`` returns a compact normalized cross-asset research view.

Credentials remain server-side. Neither endpoint returns secrets, account data,
PII, PHI, or trading authorization.
"""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, Mapping
from wsgiref.simple_server import make_server

from hedge_desk import server as base_server
from hedge_desk.data.open_market_feeds import (
    cftc_cot,
    eia_v2,
    finra_fixed_income,
    nyfed_reference_rates,
    sec_submissions,
    treasury_latest_auctions,
)
from hedge_desk.market_context import build_market_context


DATA_SOURCE_STATUS_SCHEMA = "hedge-desk-data-source-status-1.1.0"


def _json(start_response, payload, status="200 OK"):
    body = json.dumps(payload, sort_keys=True).encode("utf-8")
    start_response(
        status,
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [body]


def _observation_count(value: object) -> int:
    row_count = getattr(value, "row_count", None)
    if type(row_count) is int:
        return max(row_count, 0)
    if isinstance(value, Mapping):
        return 1 if value else 0
    return 0


def _probe_source(
    provider_id: str,
    configured: bool,
    credential_required: bool,
    fetcher: Callable[[], object],
) -> Dict[str, object]:
    if not configured:
        return {
            "provider_id": provider_id,
            "status": "UNCONFIGURED",
            "configured": False,
            "credential_required": credential_required,
            "observation_count": 0,
            "reason_code": "CREDENTIALS_NOT_CONFIGURED",
        }
    try:
        result = fetcher()
        count = _observation_count(result)
        if count < 1:
            return {
                "provider_id": provider_id,
                "status": "BLOCKED",
                "configured": True,
                "credential_required": credential_required,
                "observation_count": 0,
                "reason_code": "EMPTY_OR_INVALID_RESPONSE",
            }
        return {
            "provider_id": provider_id,
            "status": "LIVE",
            "configured": True,
            "credential_required": credential_required,
            "observation_count": count,
            "reason_code": None,
        }
    except Exception:
        return {
            "provider_id": provider_id,
            "status": "BLOCKED",
            "configured": True,
            "credential_required": credential_required,
            "observation_count": 0,
            "reason_code": "UPSTREAM_OR_AUTH_FAILURE",
        }


def build_data_source_status() -> Dict[str, object]:
    """Probe authoritative research feeds with bounded, non-payload requests."""
    eia_configured = bool(os.environ.get("EIA_API_KEY", "").strip())
    finra_configured = bool(
        os.environ.get("FINRA_CLIENT_ID", "").strip()
        and os.environ.get("FINRA_CLIENT_SECRET", "").strip()
    )

    definitions = {
        "nyfed-markets": (
            True,
            False,
            lambda: nyfed_reference_rates(),
        ),
        "treasury-fiscaldata": (
            True,
            False,
            lambda: treasury_latest_auctions(limit=1),
        ),
        "cftc-cot": (
            True,
            False,
            lambda: cftc_cot(limit=1),
        ),
        "sec-edgar": (
            True,
            False,
            lambda: sec_submissions(320193),
        ),
        "eia-open-data": (
            eia_configured,
            True,
            lambda: eia_v2("petroleum/stoc/wstk", data=("value",), limit=1),
        ),
        "finra": (
            finra_configured,
            True,
            lambda: finra_fixed_income("corporateMarketBreadth", limit=1),
        ),
    }

    sources: Dict[str, Dict[str, object]] = {}
    runnable = {}
    for provider_id, (configured, credential_required, fetcher) in definitions.items():
        if configured:
            runnable[provider_id] = (credential_required, fetcher)
        else:
            sources[provider_id] = _probe_source(
                provider_id, False, credential_required, fetcher
            )

    if runnable:
        with ThreadPoolExecutor(max_workers=len(runnable)) as pool:
            futures = {
                pool.submit(
                    _probe_source,
                    provider_id,
                    True,
                    credential_required,
                    fetcher,
                ): provider_id
                for provider_id, (credential_required, fetcher) in runnable.items()
            }
            for future in as_completed(futures):
                provider_id = futures[future]
                try:
                    sources[provider_id] = future.result()
                except Exception:
                    sources[provider_id] = {
                        "provider_id": provider_id,
                        "status": "BLOCKED",
                        "configured": True,
                        "credential_required": runnable[provider_id][0],
                        "observation_count": 0,
                        "reason_code": "PROBE_FAILURE",
                    }

    ordered = {key: sources[key] for key in sorted(sources)}
    counts = {"LIVE": 0, "BLOCKED": 0, "UNCONFIGURED": 0}
    for item in ordered.values():
        state = str(item["status"])
        counts[state] = counts.get(state, 0) + 1

    return {
        "schema_version": DATA_SOURCE_STATUS_SCHEMA,
        "mode": "PAPER_RESEARCH_ONLY",
        "trade_authorized": False,
        "live_orders_enabled": False,
        "source_count": len(ordered),
        "live_count": counts.get("LIVE", 0),
        "blocked_count": counts.get("BLOCKED", 0),
        "unconfigured_count": counts.get("UNCONFIGURED", 0),
        "sources": ordered,
    }


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/api/data-sources":
        payload = base_server._cached("data-source-status", build_data_source_status)
        return _json(start_response, payload)
    if path == "/api/market-context":
        payload = base_server._cached("market-context", build_market_context)
        return _json(start_response, payload)
    return base_server.application(environ, start_response)


def main():
    port = int(os.getenv("PORT", "8765"))
    with make_server(
        "0.0.0.0",
        port,
        application,
        server_class=base_server.ThreadingWSGIServer,
    ) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
