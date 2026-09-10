"""Minimal full-stack HTTP service for the paper-research web MVP."""

import json
import mimetypes
import os
from pathlib import Path
from socketserver import ThreadingMixIn
from threading import Lock
from time import monotonic, perf_counter
from urllib.request import Request, urlopen
from wsgiref.simple_server import WSGIServer, make_server

from hedge_desk.candidates import build_candidate_feed
from hedge_desk.risk.dashboard import build_candidate_risk_dashboard
from hedge_desk.console_report import build_console_payload
from hedge_desk.overnight import current_morning_report
from hedge_desk.auth_app import make_auth_app, default_membership_store

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEPLOY_ROOT = Path.cwd()
WEB = DEPLOY_ROOT / "dist" if (DEPLOY_ROOT / "dist").is_dir() else PACKAGE_ROOT / "dist"
API_CACHE_SECONDS = max(0.0, float(os.getenv("EMPORION_API_CACHE_SECONDS", "15")))

# Lazy singleton for the membership/auth app. The store is only opened on the
# first auth request so that a plain report server never pays the SQLite cost.
_AUTH_APP = None
_AUTH_APP_LOCK = Lock()
GP_EMAIL = os.getenv("GP_EMAIL", "").strip()


def _auth_app():
    global _AUTH_APP
    if _AUTH_APP is None:
        with _AUTH_APP_LOCK:
            if _AUTH_APP is None:
                store = default_membership_store()
                from hedge_desk.supabase_auth import verifier_from_env
                from hedge_desk.broker_link import default_broker_store
                from hedge_desk.brokers.schwab_oauth import SchwabOAuth, SchwabOAuthConfig
                from hedge_desk.brokers.schwab_readonly import SchwabReadOnlyBroker

                broker_oauth = None
                try:
                    cfg = SchwabOAuthConfig.from_environment()
                    if cfg.configured:
                        broker_oauth = SchwabOAuth(cfg)
                except Exception:
                    broker_oauth = None
                _AUTH_APP = make_auth_app(
                    store,
                    gp_email=GP_EMAIL,
                    jwt_verifier=verifier_from_env(),
                    broker_store=default_broker_store(),
                    broker_oauth=broker_oauth,
                    broker_adapter=SchwabReadOnlyBroker(),
                )
    return _AUTH_APP




class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    """Keep the deployment dependency-light while allowing concurrent reads."""

    daemon_threads = True
    block_on_close = False
    request_queue_size = 256


_cache_lock = Lock()
_api_cache = {}
_metrics_lock = Lock()
_request_metrics = {
    "requests": 0,
    "errors": 0,
    "total_seconds": 0.0,
    "max_seconds": 0.0,
}


def _json(start_response, payload, status="200 OK"):
    body = json.dumps(payload).encode("utf-8")
    start_response(
        status,
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [body]


def _static_cache_control(target):
    """Cache immutable-ish assets briefly while keeping HTML immediately fresh.

    report.json is a data snapshot the console must fetch on first load; giving
    it a short browser cache (plus stale-while-revalidate) means repeat visits
    render instantly from cache instead of making a revalidation round-trip to
    the origin, which is what makes a cold/slow instance feel sluggish.
    """

    suffix = target.suffix.lower()
    if suffix == ".json":
        return "public, max-age=60, stale-while-revalidate=300"
    if suffix in {".css", ".js", ".mjs", ".svg", ".png", ".jpg", ".jpeg", ".webp"}:
        return "public, max-age=300, stale-while-revalidate=600"
    return "no-cache"


def _etag_for(target):
    stat = target.stat()
    return f'W/"{stat.st_mtime_ns:x}-{stat.st_size:x}"'


def _cached(key, builder):
    if API_CACHE_SECONDS <= 0:
        return builder()
    now = monotonic()
    with _cache_lock:
        entry = _api_cache.get(key)
        if entry and entry[0] > now:
            return entry[1]
        value = builder()
        _api_cache[key] = (now + API_CACHE_SECONDS, value)
        return value


def _record_request(elapsed, status):
    with _metrics_lock:
        _request_metrics["requests"] += 1
        if status >= 500:
            _request_metrics["errors"] += 1
        _request_metrics["total_seconds"] += elapsed
        _request_metrics["max_seconds"] = max(_request_metrics["max_seconds"], elapsed)


def performance_snapshot():
    """Return process-local request timing counters for tests and operational inspection."""

    with _metrics_lock:
        requests = _request_metrics["requests"]
        total = _request_metrics["total_seconds"]
        return {
            "requests": requests,
            "errors": _request_metrics["errors"],
            "mean_ms": round((total / requests) * 1000, 3) if requests else 0.0,
            "max_ms": round(_request_metrics["max_seconds"] * 1000, 3),
        }


def build_live_console_payload():
    """Regenerate a fresh, validated desk-console payload from the engine.

    Mirrors the deploy-time export (scripts/build_web.py) but runs the engine
    now, so the console can show a report generated moments ago rather than
    only the last committed deploy snapshot. Rejected by the release gate if
    the freshly computed report is not publishable.
    """
    report = current_morning_report()
    return build_console_payload(report)


def _supabase_status():
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "") or os.getenv("SUPABASE_ANON_KEY", "")
    if not url or not key:
        return {"configured": False, "reachable": False}
    try:
        # The REST schema root now requires a secret key. Auth health is the
        # supported public-key probe and does not expose or query user data.
        request = Request(url + "/auth/v1/health", headers={"apikey": key})
        with urlopen(request, timeout=5) as response:
            return {"configured": True, "reachable": 200 <= response.status < 300}
    except Exception:
        return {"configured": True, "reachable": False}


def _dispatch(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    # Membership/auth surface. All /api/auth/* requests are handled by the
    # auth app; the report/candidate/risk-dashboard endpoints below stay
    # public so the guest "test drive" tier remains open.
    if path.startswith("/api/auth/"):
        return _auth_app()(environ, start_response)
    if path == "/api/health":
        return _json(start_response, {"service": "hedge-desk-web", "status": "ok", "mode": "paper", "live_orders_enabled": False, "supabase": _cached("supabase-status", _supabase_status)})
    if path == "/api/candidates":
        return _json(start_response, _cached("candidates", build_candidate_feed))
    if path == "/api/risk-dashboard":
        return _json(start_response, _cached("risk-dashboard", build_candidate_risk_dashboard))
    if path == "/api/about":
        return _json(start_response, {"display_name": "mbolton", "linkedin_url": "https://www.linkedin.com/in/bolton-2600/"})
    if path == "/api/report":
        return _json(start_response, _cached("console-report", build_live_console_payload))
    relative = "index.html" if path in ("/", "") else path.lstrip("/")
    target = (WEB / relative).resolve()
    if WEB.resolve() not in target.parents and target != WEB.resolve():
        return _json(start_response, {"error": "not_found"}, "404 Not Found")
    if not target.is_file():
        target = WEB / "index.html"
    if not target.is_file():
        return _json(start_response, {"error": "web_assets_missing"}, "503 Service Unavailable")

    content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
    cache_control = _static_cache_control(target)
    etag = _etag_for(target)
    if environ.get("HTTP_IF_NONE_MATCH") == etag:
        start_response("304 Not Modified", [("Cache-Control", cache_control), ("ETag", etag)])
        return [b""]

    body = target.read_bytes()
    start_response(
        "200 OK",
        [
            ("Content-Type", content_type),
            ("Content-Length", str(len(body))),
            ("Cache-Control", cache_control),
            ("ETag", etag),
        ],
    )
    return [body]


def application(environ, start_response):
    started = perf_counter()
    status_code = 500

    def measured_start_response(status, headers, exc_info=None):
        nonlocal status_code
        status_code = int(status.split(" ", 1)[0])
        if exc_info is None:
            return start_response(status, headers)
        return start_response(status, headers, exc_info)

    try:
        return _dispatch(environ, measured_start_response)
    finally:
        _record_request(perf_counter() - started, status_code)


def main():
    port = int(os.getenv("PORT", "8765"))
    with make_server("0.0.0.0", port, application, server_class=ThreadingWSGIServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
