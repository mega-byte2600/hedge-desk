import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hedge_desk import web_app


def _call(path):
    captured = {}

    def start_response(status, headers, exc_info=None):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(
        web_app.application(
            {
                "PATH_INFO": path,
                "REQUEST_METHOD": "GET",
                "HTTP_HOST": "localhost",
                "wsgi.url_scheme": "https",
            },
            start_response,
        )
    )
    return captured, body


class LiveDataPlaneWebTests(unittest.TestCase):
    def test_market_context_endpoint_is_json_and_never_authorizes_trading(self):
        payload = {
            "schema_version": "hedge-desk-market-context-1.0.0",
            "status": "LIVE",
            "live_sources": 5,
            "sources": {"finra": {"status": "LIVE", "observation_count": 1}},
            "trade_authorized": False,
        }
        with patch.object(web_app, "build_market_context", return_value=payload), patch.object(
            web_app.base_server, "_cached", side_effect=lambda _key, builder: builder()
        ):
            captured, body = _call("/api/market-context")

        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(captured["headers"]["Content-Type"], "application/json")
        self.assertEqual(captured["headers"]["Cache-Control"], "no-store")
        decoded = json.loads(body)
        self.assertEqual(decoded["sources"]["finra"]["status"], "LIVE")
        self.assertFalse(decoded["trade_authorized"])

    def test_dashboard_injects_live_api_layer_without_replacing_nightly_health(self):
        original = (
            "<!doctype html><html><body><div class='grid'>"
            "<div class='card wide'><h3>Source health — what the batch actually closed on</h3>"
            "<table class='health'></table></div></div></body></html>"
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "am-demo.html"
            path.write_text(original, encoding="utf-8")
            with patch.object(web_app.base_server, "ARTIFACTS", Path(td)):
                captured, body = _call("/dashboard")

        text = body.decode("utf-8")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("authoritative-api-layer-v1", text)
        self.assertIn("/api/data-sources", text)
        self.assertIn("/api/market-context", text)
        self.assertIn("Source health — what the batch actually closed on", text)
        # New copy is set via JS at runtime; assert the JS contains it.
        self.assertIn("Last night", text)
        self.assertIn("what went into this report", text)
        self.assertIn("Data sources — live connections", text)
        self.assertNotIn("FINRA_CLIENT_SECRET", text)
        # No internal jargon in user-facing strings. The reason_code values
        # appear in JS as comparison targets (not displayed); assert the
        # display mapping uses plain language instead.
        self.assertIn("Couldn't reach the source just now", text)
        self.assertIn("Not connected yet", text)
        self.assertNotIn("production probes", text)
        self.assertNotIn("strategy-input", text)
        # The raw code must not be used as display text via replaceAll.
        self.assertNotIn("replaceAll('_', ' ')", text)

    def test_dashboard_etag_works_with_enhancement_version(self):
        html = "<html><body><div class='grid'></div></body></html>"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "am-demo.html"
            path.write_text(html, encoding="utf-8")
            with patch.object(web_app.base_server, "ARTIFACTS", Path(td)):
                first, _ = _call("/dashboard")
                etag = first["headers"]["ETag"]
                captured = {}

                def start_response(status, headers, exc_info=None):
                    captured["status"] = status
                    captured["headers"] = dict(headers)

                body = b"".join(
                    web_app.application(
                        {"PATH_INFO": "/dashboard", "HTTP_IF_NONE_MATCH": etag},
                        start_response,
                    )
                )
        self.assertEqual(captured["status"], "304 Not Modified")
        self.assertEqual(body, b"")


if __name__ == "__main__":
    unittest.main()
