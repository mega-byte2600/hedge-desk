"""Production WSGI entry point for market-data health and normalized context.

All existing web behavior delegates to :mod:`hedge_desk.server`. This module
adds bounded operational/research endpoints and a live enhancement to the
nightly dashboard. Credentials remain server-side. No secret, account data,
PII, PHI, or trading authorization is returned.
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
    sec_companyfacts,
    sec_submissions,
    treasury_latest_auctions,
)
from hedge_desk.market_context import build_market_context
from hedge_desk.rates_desk import fred_series_rows
from datetime import date, timedelta


DATA_SOURCE_STATUS_SCHEMA = "hedge-desk-data-source-status-1.1.0"

_DASHBOARD_API_LAYER = r"""
<script id="authoritative-api-layer-v1">
(() => {
  const LABELS = {
    'nyfed-markets': 'Money markets (NY Fed)',
    'treasury-fiscaldata': 'Treasury auctions (U.S. Treasury)',
    'cftc-cot': 'Futures positioning (CFTC)',
    'sec-edgar': 'Company filings (SEC)',
    'eia-open-data': 'Energy data (EIA)',
    'finra': 'Bond market data (FINRA)',
    'fred': 'Economic data (FRED)'
  };

  function detail(provider, contextSource, probe) {
    if (!probe || probe.status !== 'LIVE') {
      // Never show internal reason codes (UPSTREAM_OR_AUTH_FAILURE, etc.) to readers.
      // Map to plain-language explanations.
      const code = probe && probe.reason_code;
      if (code === 'CREDENTIALS_NOT_CONFIGURED') return 'Not connected yet';
      if (code === 'EMPTY_OR_INVALID_RESPONSE') return "Source didn't return usable data";
      if (code === 'UPSTREAM_OR_AUTH_FAILURE') return "Couldn't reach the source just now";
      if (code === 'PROBE_FAILURE') return "Couldn't reach the source just now";
      return 'Not available right now';
    }
    const obs = contextSource && contextSource.observations;
    if (provider === 'nyfed-markets' && obs) {
      return ['SOFR','EFFR','OBFR','TGCR','BGCR']
        .filter(k => obs[k] && obs[k].percentRate != null)
        .map(k => `${k} ${obs[k].percentRate}%`)
        .join(' · ') || `${probe.observation_count} data points`;
    }
    if (provider === 'treasury-fiscaldata' && Array.isArray(obs) && obs[0]) {
      const x = obs[0];
      return [x.security_type, x.security_term, x.auction_date && `auction ${x.auction_date}`]
        .filter(Boolean).join(' · ');
    }
    if (provider === 'eia-open-data' && Array.isArray(obs) && obs[0]) {
      const x = obs[0];
      return [x.period, x.value != null && `${x.value} ${x.units || ''}`.trim(), x['series-description']]
        .filter(Boolean).join(' · ');
    }
    if (provider === 'cftc-cot' && Array.isArray(obs) && obs[0]) {
      return `${obs.length} markets tracked · latest ${obs[0].report_date_as_yyyy_mm_dd || 'report'}`;
    }
    if (provider === 'finra' && Array.isArray(obs) && obs[0]) {
      const x = obs[0];
      const breadth = x.advances != null && x.declines != null ? `${x.advances} up / ${x.declines} down` : null;
      return [x.date || x.weekStartDate, x.productCategory || x.marketSegment, breadth]
        .filter(Boolean).join(' · ') || `${probe.observation_count} data points`;
    }
    return `${probe.observation_count} data points`;
  }

  function mount(status, context) {
    const grid = document.querySelector('.grid');
    if (!grid || document.getElementById('authoritative-api-card')) return;

    const oldHealth = grid.querySelector('.card.wide h3');
    if (oldHealth && oldHealth.textContent.includes('Source health')) {
      oldHealth.textContent = 'Last night\u2019s data — what went into this report';
    }

    const fred = (status.sources || {}).fred;
    if (fred && fred.status === 'LIVE') {
      grid.querySelectorAll('tr').forEach(tr => {
        if (!tr.textContent.includes('Rates (FRED)')) return;
        const cells = tr.querySelectorAll('td');
        if (cells.length >= 3) {
          cells[1].textContent = 'Live';
          cells[1].className = 'ok';
          cells[2].textContent = 'Working now; last night\u2019s report was made before the fix.';
        }
      });
    }

    const card = document.createElement('div');
    card.className = 'card wide';
    card.id = 'authoritative-api-card';

    const heading = document.createElement('h3');
    heading.textContent = 'Data sources — live connections';
    card.appendChild(heading);

    const summary = document.createElement('p');
    summary.className = 'muted';
    const live = status.live_count || 0;
    const total = status.source_count || 0;
    const blocked = status.blocked_count || 0;
    summary.textContent = `${live} of ${total} sources connected` +
      (blocked ? ` · ${blocked} unavailable` : '') +
      '. Checked just now.';
    card.appendChild(summary);

    const table = document.createElement('table');
    table.className = 'health';
    table.innerHTML = '<thead><tr><th>Source</th><th>Status</th><th>Details</th></tr></thead>';
    const tbody = document.createElement('tbody');
    Object.entries(status.sources || {}).forEach(([provider, probe]) => {
      const tr = document.createElement('tr');
      const name = document.createElement('td');
      name.textContent = LABELS[provider] || provider;
      const state = document.createElement('td');
      const isLive = probe.status === 'LIVE';
      const isUnconfigured = probe.reason_code === 'CREDENTIALS_NOT_CONFIGURED';
      state.textContent = isLive ? 'Live' : (isUnconfigured ? 'Not connected' : 'Unavailable');
      state.className = isLive ? 'ok' : 'warn';
      const info = document.createElement('td');
      info.className = 'muted';
      info.textContent = detail(provider, (context.sources || {})[provider], probe);
      tr.append(name, state, info);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    card.appendChild(table);
    grid.insertBefore(card, grid.firstChild);
  }

  Promise.all([
    fetch('/api/data-sources', {cache: 'no-store'}).then(r => {
      if (!r.ok) throw new Error('source status unavailable');
      return r.json();
    }),
    fetch('/api/market-context', {cache: 'no-store'}).then(r => {
      if (!r.ok) throw new Error('market context unavailable');
      return r.json();
    })
  ]).then(([status, context]) => mount(status, context)).catch(() => {
    const grid = document.querySelector('.grid');
    if (!grid || document.getElementById('authoritative-api-card')) return;
    const card = document.createElement('div');
    card.className = 'card wide';
    card.id = 'authoritative-api-card';
    const h = document.createElement('h3');
    h.textContent = 'Data sources — live connections';
    const p = document.createElement('p');
    p.className = 'muted';
    p.textContent = 'Could not check sources just now. Try refreshing the page.';
    card.append(h, p);
    grid.insertBefore(card, grid.firstChild);
  });
})();
</script>
"""


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
    except Exception as exc:
        detail = str(exc)[:200]
        # Redact credentials from error messages
        import re
        detail = re.sub(r"(api_key|apikey|token)=[^&\s]+", r"\1=[REDACTED]", detail, flags=re.IGNORECASE)
        return {
            "provider_id": provider_id,
            "status": "BLOCKED",
            "configured": True,
            "credential_required": credential_required,
            "observation_count": 0,
            "reason_code": "UPSTREAM_OR_AUTH_FAILURE",
            "detail": detail,
        }


def build_data_source_status() -> Dict[str, object]:
    """Probe authoritative research feeds with bounded, non-payload requests."""
    eia_configured = bool(os.environ.get("EIA_API_KEY", "").strip())
    finra_configured = bool(
        os.environ.get("FINRA_CLIENT_ID", "").strip()
        and os.environ.get("FINRA_CLIENT_SECRET", "").strip()
    )

    def probe_sec():
        try:
            return sec_submissions(320193)
        except Exception:
            return sec_companyfacts(320193)

    definitions = {
        "fred": (
            True,
            False,
            lambda: {
                "latest": fred_series_rows(
                    "CPIAUCSL",
                    date.today() - timedelta(days=60),
                    date.today(),
                    retries=0,
                )[-1]
            },
        ),
        "nyfed-markets": (True, False, lambda: nyfed_reference_rates()),
        "treasury-fiscaldata": (True, False, lambda: treasury_latest_auctions(limit=1)),
        "cftc-cot": (True, False, lambda: cftc_cot(limit=1)),
        "sec-edgar": (True, False, probe_sec),
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


def _serve_enhanced_dashboard(environ, start_response):
    path = base_server.ARTIFACTS / "am-demo.html"
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return _json(
            start_response,
            {"error": "artifact_missing", "path": "am-demo.html"},
            "404 Not Found",
        )
    if "authoritative-api-layer-v1" not in html:
        marker = "</body>"
        html = html.replace(marker, _DASHBOARD_API_LAYER + marker, 1)
    body = html.encode("utf-8")
    etag = base_server._etag_for(path)[:-1] + "-api-layer-v1\""
    if environ.get("HTTP_IF_NONE_MATCH") == etag:
        start_response("304 Not Modified", [("Cache-Control", "no-cache"), ("ETag", etag)])
        return [b""]
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-cache"),
            ("ETag", etag),
        ],
    )
    return [body]


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/api/data-sources":
        payload = base_server._cached("data-source-status", build_data_source_status)
        return _json(start_response, payload)
    if path == "/api/market-context":
        payload = base_server._cached("market-context", build_market_context)
        return _json(start_response, payload)
    if path in ("/dashboard", "/dashboard.html"):
        return _serve_enhanced_dashboard(environ, start_response)
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
