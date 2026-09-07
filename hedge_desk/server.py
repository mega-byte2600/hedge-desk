"""Minimal full-stack HTTP service for the Emporion research web MVP."""

import json
import mimetypes
import os
from pathlib import Path
from urllib.request import Request, urlopen
from wsgiref.simple_server import make_server

from hedge_desk.live_data import build_operational_candidate_feed

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEPLOY_ROOT = Path.cwd()
WEB = DEPLOY_ROOT / "dist" if (DEPLOY_ROOT / "dist").is_dir() else PACKAGE_ROOT / "dist"


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


def _supabase_status():
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_ANON_KEY", "")
    if not url or not key:
        return {"configured": False, "reachable": False}
    try:
        request = Request(url + "/rest/v1/", headers={"apikey": key, "Authorization": "Bearer " + key})
        with urlopen(request, timeout=5) as response:
            return {"configured": True, "reachable": 200 <= response.status < 500}
    except Exception:
        return {"configured": True, "reachable": False}


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/api/health":
        return _json(
            start_response,
            {
                "service": "hedge-desk-web",
                "product": "Emporion",
                "status": "ok",
                "mode": "paper",
                "research_only": True,
                "live_orders_enabled": False,
                "supabase": _supabase_status(),
            },
        )
    if path == "/api/candidates":
        return _json(start_response, build_operational_candidate_feed())
    if path == "/api/data":
        payload = build_operational_candidate_feed()
        return _json(
            start_response,
            {
                "schema_version": payload["schema_version"],
                "generated_at": payload["generated_at"],
                "data_priority": payload["data_priority"],
                "data_state": payload["data_state"],
                "sources_available": payload["sources_available"],
                "sources_total": payload["sources_total"],
                "sources": payload["sources"],
            },
        )
    if path == "/api/about":
        return _json(
            start_response,
            {
                "product": "Emporion",
                "tagline": "Markets · Intelligence · Discipline",
                "parent": "Bolton Investment Group (BIG)",
                "display_name": "mbolton",
                "linkedin_url": "https://www.linkedin.com/in/bolton-2600/",
            },
        )
    relative = "index.html" if path in ("/", "") else path.lstrip("/")
    target = (WEB / relative).resolve()
    if WEB.resolve() not in target.parents and target != WEB.resolve():
        return _json(start_response, {"error": "not_found"}, "404 Not Found")
    if not target.is_file():
        target = WEB / "index.html"
    if not target.is_file():
        return _json(start_response, {"error": "web_assets_missing"}, "503 Service Unavailable")
    body = target.read_bytes()
    content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
    start_response("200 OK", [("Content-Type", content_type), ("Content-Length", str(len(body)))])
    return [body]


def main():
    port = int(os.getenv("PORT", "8765"))
    with make_server("0.0.0.0", port, application) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
