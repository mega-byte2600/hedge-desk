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

from typing import Dict

from hedge_desk.candidates import (
    build_candidate_feed,
    build_earnings_candidate_feed,
    build_macro_candidate_feed,
    build_real_eod_candidate_feed,
)
from hedge_desk.risk.dashboard import build_candidate_risk_dashboard
from hedge_desk.console_report import build_console_payload
from hedge_desk.overnight import current_morning_report
from hedge_desk.auth_app import make_auth_app, default_membership_store

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEPLOY_ROOT = Path.cwd()
WEB = DEPLOY_ROOT / "web" if (DEPLOY_ROOT / "web").is_dir() else PACKAGE_ROOT / "web"
# Prefer the repo-root artifacts (where the nightly batch / committed report
# live) over the installed-package dir, so Render serves the real report.
ARTIFACTS = (DEPLOY_ROOT / "artifacts") if (DEPLOY_ROOT / "artifacts").is_dir() else PACKAGE_ROOT / "artifacts"
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
                from hedge_desk.membership_audit import default_audit_log

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
                    audit=default_audit_log(),
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


def _redirect(start_response, location: str):
    """Issue a 302 redirect to ``location``."""
    start_response("302 Found", [("Location", location), ("Content-Length", "0")])
    return [b""]


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


def _serve_artifact(start_response, path: Path, as_json: bool = False):
    """Serve a regenerated artifacts/ file (AM demo page or live report JSON).

    The web console is built from dist/, but the true-MVP AM report is produced
    into artifacts/ by the nightly run. Directly serving that file (rather than
    copying it into dist/) keeps generated output out of the static bundle and
    always surfaces the latest regenerated report. Fails closed to 404 if the
    artifact has not been generated yet.
    """
    try:
        body = path.read_bytes()
    except (OSError, ValueError):
        return _json(start_response, {"error": "artifact_missing", "path": path.name},
                     "404 Not Found")
    content_type = (
        "application/json" if as_json
        else mimetypes.guess_type(str(path))[0] or "text/html; charset=utf-8"
    )
    cache = "no-store" if as_json else "no-cache"  # HTML revalidates (regens nightly); JSON never cached client-side
    start_response(
        "200 OK",
        [
            ("Content-Type", content_type),
            ("Content-Length", str(len(body))),
            ("Cache-Control", cache),
            ("ETag", _etag_for(path)),
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
    """Serve a built value from a short-lived cache.

    The builder runs *outside* the lock. It used to run inside, so one slow build
    serialised every other endpoint: ``_cached("supabase-status", ...)`` does a
    urlopen with a 5s timeout on the health path that Render polls, and while it
    was in flight a request for the engine-backed report or risk dashboard blocked
    behind it. A concurrent miss may now build twice, which is harmless for these
    idempotent builders and far cheaper than a cross-endpoint stall.
    """
    if API_CACHE_SECONDS <= 0:
        return builder()
    with _cache_lock:
        entry = _api_cache.get(key)
        if entry and entry[0] > monotonic():
            return entry[1]
    value = builder()
    with _cache_lock:
        _api_cache[key] = (monotonic() + API_CACHE_SECONDS, value)
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


NIGHTLY_OUTCOMES_SCHEMA = "hedge-desk-nightly-outcomes-1.0.0"


def build_nightly_outcomes_payload(
    report_path: str = "artifacts/am-report-latest.json",
) -> Dict[str, object]:
    """Serve the real nightly paper outcomes + yellow sheets for the Scenario Lab.

    Reads the committed AM report (the same artifact the dashboard renders) and
    exposes its ``paper_outcome_summary`` and ``yellow_sheets`` sections verbatim,
    so the Scenario Lab can show observed outcomes instead of the frozen
    synthetic war-games. Empty is honest: when no paper outcomes have been
    recorded yet the payload says so explicitly instead of inventing scenarios.
    Raises FileNotFoundError / ValueError when the report is missing or
    unreadable (the route maps these to a 503 with an explicit reason).
    """
    from pathlib import Path as _Path

    path = _Path(report_path)
    if not path.is_file():
        raise FileNotFoundError(f"nightly report not found: {report_path}")
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"nightly report unreadable: {exc}") from exc
    if not isinstance(report, dict):
        raise ValueError("nightly report is not a JSON object")
    outcomes = report.get("paper_outcome_summary")
    sheets = report.get("yellow_sheets")
    return {
        "schema_version": NIGHTLY_OUTCOMES_SCHEMA,
        "mode": "REAL_NIGHTLY_OUTCOMES",
        "report_sha256": report.get("report_sha256", ""),
        "paper_outcome_summary": outcomes
        if isinstance(outcomes, dict)
        else {"status": "NO_OUTCOMES_RECORDED"},
        "yellow_sheets": sheets
        if isinstance(sheets, dict)
        else {"status": "NO_SHEETS_RECORDED"},
        # Research input only. The Scenario Lab never authorizes a trade.
        "trade_authorized": False,
        "note": (
            "Observed paper outcomes from the nightly batch, not a forecast. "
            "An empty outcome set is reported as empty — never synthesized."
        ),
    }


def _nightly_outcomes_or_503(start_response):
    try:
        return _json(
            start_response, _cached("nightly-outcomes", build_nightly_outcomes_payload)
        )
    except (FileNotFoundError, ValueError) as exc:
        return _json(
            start_response,
            {
                "schema_version": NIGHTLY_OUTCOMES_SCHEMA,
                "mode": "REAL_NIGHTLY_OUTCOMES",
                "status": "NIGHTLY_REPORT_UNAVAILABLE",
                "reason": str(exc),
                "trade_authorized": False,
            },
            "503 Service Unavailable",
        )


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
    # Membership/auth surface. The auth app owns the auth, tier, data-gate,
    # and broker routes; the report/candidate/risk-dashboard endpoints below
    # stay public so the guest "test drive" tier remains open.
    if path.startswith("/api/auth/") or path.startswith("/api/broker/") or path in (
        "/api/tier",
        "/api/data/real",
    ):
        return _auth_app()(environ, start_response)
    if path == "/api/health":
        return _json(start_response, {"service": "hedge-desk-web", "status": "ok", "mode": "paper", "live_orders_enabled": False, "supabase": _cached("supabase-status", _supabase_status)})
    if path == "/api/candidates":
        return _json(start_response, _cached("candidates", build_candidate_feed))
    if path == "/api/eod-candidates":
        return _json(start_response, _cached("eod-candidates", build_real_eod_candidate_feed))
    if path == "/api/earnings-candidates":
        return _json(start_response, _cached("earnings-candidates", build_earnings_candidate_feed))
    if path == "/api/macro-candidates":
        return _json(start_response, _cached("macro-candidates", build_macro_candidate_feed))
    if path == "/api/nightly-outcomes":
        return _nightly_outcomes_or_503(start_response)
    if path == "/api/risk-dashboard":
        return _json(start_response, _cached("risk-dashboard", build_candidate_risk_dashboard))
    if path == "/api/about":
        return _json(start_response, {"display_name": "mbolton", "linkedin_url": "https://www.linkedin.com/in/bolton-2600/"})
    if path == "/api/report":
        return _json(start_response, _cached("console-report", build_live_console_payload))
    # True-MVP demo: serve the regenerated AM report page / live report JSON
    # straight from artifacts/ (the real EOD -> overnight -> AM candidate output).
    # Live overview dashboard (was /am-demo); old path redirects. Root serves
    # the dashboard directly so the bare prod URL shows the real report.
    # Landing page at root; dashboard at /dashboard; guide at /guide.
    if (ARTIFACTS / "am-demo.html").is_file() and (path in ("/dashboard", "/dashboard.html")):
        return _serve_artifact(start_response, ARTIFACTS / "am-demo.html")
    if path in ("/am-demo", "/am-demo.html"):
        return _redirect(start_response, "/dashboard")
    if path == "/api/am-report":
        return _serve_artifact(start_response, ARTIFACTS / "am-report-latest.json", as_json=True)
    # Muse/Toby's Selling Options Premium visual guide (static, self-contained).
    if path in ("/guide/selling-options-premium", "/guide/selling-options-premium.html"):
        guide = DEPLOY_ROOT / "docs" / "guides" / "selling-options-premium-visual-guide.html"
        if not guide.is_file():
            guide = PACKAGE_ROOT / "docs" / "guides" / "selling-options-premium-visual-guide.html"
        if guide.is_file():
            return _serve_artifact(start_response, guide)
        return _json(start_response, {"error": "artifact_missing", "path": "guide"}, "404 Not Found")
    relative = "index.html" if path in ("/", "") else path.lstrip("/")
    target = (WEB / relative).resolve()
    if WEB.resolve() not in target.parents and target != WEB.resolve():
        return _json(start_response, {"error": "not_found"}, "404 Not Found")
    if not target.is_file():
        # The console is a single-page app, so an extension-less path falls back to
        # the shell for deep links. Anything else is a real miss: an unknown
        # /api/* route or a missing asset must be a JSON 404. Previously every miss
        # returned the HTML shell with 200, so a client's fetch('/api/typo') got
        # HTML that it then tried to parse as JSON, and a mistyped route looked
        # like it had succeeded.
        if path.startswith("/api/") or Path(relative).suffix:
            return _json(start_response, {"error": "not_found", "path": path}, "404 Not Found")
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
