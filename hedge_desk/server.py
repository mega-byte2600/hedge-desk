"""Dependency-free local API for the paper-only iOS MVP."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple
from urllib.parse import parse_qs, urlparse

from hedge_desk.demo import json_value
from hedge_desk.schwab_readonly import SchwabConfig, SchwabReadOnlyClient


def build_server(host: str, port: int) -> Tuple[ThreadingHTTPServer, SchwabReadOnlyClient]:
    schwab = SchwabReadOnlyClient(SchwabConfig.from_environment())

    class Handler(BaseHTTPRequestHandler):
        def _json(self, status: int, payload: object) -> None:
            body = json.dumps(json_value(payload), sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 - stdlib handler contract
            parsed = urlparse(self.path)
            if parsed.path == "/api/status":
                self._json(200, {
                    "mode": "PAPER_ONLY", "orders_blocked": True,
                    "schwab": schwab.readiness(), "yellow_sheet_required": True,
                })
            elif parsed.path == "/api/schwab/readiness":
                self._json(200, schwab.readiness())
            elif parsed.path == "/api/schwab/authorize":
                try:
                    location = schwab.authorization_url()
                except ValueError as exc:
                    self._json(503, {"error": str(exc), "orders_blocked": True})
                    return
                self.send_response(302)
                self.send_header("Location", location)
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
            elif parsed.path == "/api/schwab/callback":
                values = parse_qs(parsed.query)
                try:
                    result = schwab.exchange_callback(
                        values.get("code", [""])[0], values.get("state", [""])[0]
                    )
                except (PermissionError, ValueError, OSError) as exc:
                    self._json(400, {"error": str(exc), "orders_blocked": True})
                    return
                self._json(200, result)
            elif parsed.path == "/api/schwab/account-numbers":
                try:
                    self._json(200, {"accounts": schwab.account_numbers(), "orders_blocked": True})
                except (PermissionError, OSError, ValueError) as exc:
                    self._json(503, {"error": str(exc), "orders_blocked": True})
            elif parsed.path in ("/api/dividends", "/api/earnings"):
                self._json(200, {"candidates": [], "disposition": "NO_TRADE"})
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self) -> None:  # noqa: N802 - fail closed for every mutation
            self._json(405, {"error": "read-only backend", "orders_blocked": True})

        def log_message(self, format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer((host, port), Handler), schwab


def main() -> None:
    host = os.environ.get("HEDGE_DESK_HOST", "127.0.0.1")
    port = int(os.environ.get("HEDGE_DESK_PORT", "8765"))
    server, _ = build_server(host, port)
    print(f"Hedge Desk PAPER_ONLY API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
