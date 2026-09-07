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


if __name__ == "__main__":
    unittest.main()
