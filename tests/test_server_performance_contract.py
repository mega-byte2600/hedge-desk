import unittest

from hedge_desk import server


class ServerPerformanceContractTests(unittest.TestCase):
    def _request(self, path):
        captured = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(server.application({"PATH_INFO": path}, start_response))
        return captured, body

    def test_static_assets_use_short_public_cache(self):
        response, body = self._request("/styles.css")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(
            response["headers"]["Cache-Control"],
            "public, max-age=300, stale-while-revalidate=600",
        )

    def test_html_remains_revalidation_friendly(self):
        response, body = self._request("/")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(response["headers"]["Cache-Control"], "no-cache")

    def test_api_payloads_are_not_cached(self):
        response, body = self._request("/api/candidates")
        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(body)
        self.assertEqual(response["headers"]["Cache-Control"], "no-store")

    def test_server_is_threaded_without_new_runtime_dependency(self):
        self.assertTrue(server.ThreadingWSGIServer.daemon_threads)
        self.assertTrue(issubclass(server.ThreadingWSGIServer, server.WSGIServer))


if __name__ == "__main__":
    unittest.main()
