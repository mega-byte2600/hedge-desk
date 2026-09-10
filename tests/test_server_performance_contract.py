import unittest
from unittest.mock import patch

from hedge_desk import server


class ServerPerformanceContractTests(unittest.TestCase):
    def setUp(self):
        self._original_web = server.WEB
        server.WEB = server.PACKAGE_ROOT / "web"
        with server._cache_lock:
            server._api_cache.clear()

    def tearDown(self):
        server.WEB = self._original_web

    def _request(self, path, headers=None):
        captured = {}
        environ = {"PATH_INFO": path}
        environ.update(headers or {})

        def start_response(status, response_headers):
            captured["status"] = status
            captured["headers"] = dict(response_headers)

        body = b"".join(server.application(environ, start_response))
        return captured, body

    def test_static_assets_use_short_public_cache_and_etag(self):
        response, body = self._request("/styles.css")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(
            response["headers"]["Cache-Control"],
            "public, max-age=300, stale-while-revalidate=600",
        )
        self.assertTrue(response["headers"]["ETag"].startswith('W/"'))

        revalidated, revalidated_body = self._request(
            "/styles.css",
            {"HTTP_IF_NONE_MATCH": response["headers"]["ETag"]},
        )
        self.assertEqual(revalidated["status"], "304 Not Modified")
        self.assertEqual(revalidated_body, b"")
        self.assertEqual(revalidated["headers"]["ETag"], response["headers"]["ETag"])

    def test_html_remains_revalidation_friendly(self):
        response, body = self._request("/")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(response["headers"]["Cache-Control"], "no-cache")
        self.assertIn("ETag", response["headers"])

    def test_api_payloads_are_not_client_cached(self):
        response, body = self._request("/api/candidates")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(response["headers"]["Cache-Control"], "no-store")

    def test_shared_candidate_payload_is_computed_once_within_ttl(self):
        payload = {"schema_version": "test", "candidates": []}
        with patch.object(server, "build_candidate_feed", return_value=payload) as builder:
            first, first_body = self._request("/api/candidates")
            second, second_body = self._request("/api/candidates")

        self.assertEqual(first["status"], "200 OK")
        self.assertEqual(second["status"], "200 OK")
        self.assertEqual(first_body, second_body)
        self.assertEqual(builder.call_count, 1)

    def test_request_metrics_record_latency_without_public_endpoint(self):
        before = server.performance_snapshot()["requests"]
        response, _ = self._request("/api/about")
        after = server.performance_snapshot()
        self.assertEqual(response["status"], "200 OK")
        self.assertGreaterEqual(after["requests"], before + 1)
        self.assertGreaterEqual(after["mean_ms"], 0.0)
        self.assertGreaterEqual(after["max_ms"], 0.0)

    def test_server_is_threaded_without_new_runtime_dependency(self):
        self.assertTrue(server.ThreadingWSGIServer.daemon_threads)
        self.assertTrue(issubclass(server.ThreadingWSGIServer, server.WSGIServer))

    def test_report_snapshot_is_client_cacheable_for_fast_repeat_loads(self):
        # The console fetches report.json on first load. A short public cache
        # (rather than no-cache) lets repeat visits render from browser cache
        # instead of revalidating against a possibly cold origin.
        response, body = self._request("/report.json")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(
            response["headers"]["Cache-Control"],
            "public, max-age=60, stale-while-revalidate=300",
        )

    def test_console_preloads_report_and_uses_browser_cache(self):
        index = (server.PACKAGE_ROOT / "web" / "index.html").read_text(encoding="utf-8")
        # preload the report so the fetch starts in parallel with the JS
        self.assertIn('rel="preload"', index)
        self.assertIn('href="./report.json"', index)

        app_js = (server.PACKAGE_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        # the client must not opt out of the browser cache with no-store
        self.assertNotIn("cache:'no-store'", app_js)
        self.assertIn("report.json", app_js)

    def test_cold_start_shows_a_waking_message_instead_of_stalling(self):
        app_js = (server.PACKAGE_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("Waking the research desk", app_js)


if __name__ == "__main__":
    unittest.main()
