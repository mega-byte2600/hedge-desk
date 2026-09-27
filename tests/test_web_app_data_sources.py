import json
import unittest
from dataclasses import dataclass
from unittest.mock import patch

from hedge_desk import server as base_server
from hedge_desk import web_app


@dataclass(frozen=True)
class _Rows:
    row_count: int = 1


class DataSourceStatusTests(unittest.TestCase):
    def setUp(self):
        base_server._api_cache.clear()

    def tearDown(self):
        base_server._api_cache.clear()

    def _request(self, path):
        captured = {}

        def start(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(web_app.application({"PATH_INFO": path}, start))
        return captured["status"], captured["headers"], json.loads(body)

    def _patch_public_sources(self):
        return (
            patch.object(web_app, "treasury_yield_curve", return_value=_Rows()),
            patch.object(web_app, "fdic_failures", return_value=_Rows()),
            patch.object(web_app, "world_bank_indicator", return_value=_Rows()),
            patch.object(web_app, "bls_latest_series", return_value=_Rows()),
            patch.object(web_app, "ecb_exchange_rates", return_value=_Rows()),
            patch.object(web_app, "nyfed_reference_rates", return_value=_Rows()),
            patch.object(web_app, "treasury_latest_auctions", return_value=_Rows()),
            patch.object(web_app, "cftc_cot", return_value=_Rows()),
            patch.object(web_app, "sec_submissions", return_value={"cik": "320193"}),
            patch.object(web_app, "eia_v2", return_value=_Rows()),
            patch.object(web_app, "finra_fixed_income", return_value=_Rows()),
        )

    def test_data_source_status_is_paper_only_and_secret_free(self):
        patches = self._patch_public_sources()
        env = {
            "EIA_API_KEY": "eia-test-secret",
            # FINRA intentionally absent: its free Public Credential still
            # requires user-provisioned OAuth client credentials.
        }
        with patch.dict("os.environ", env, clear=True), patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            status, headers, payload = self._request("/api/data-sources")

        self.assertEqual(status, "200 OK")
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertEqual(payload["mode"], "PAPER_RESEARCH_ONLY")
        self.assertFalse(payload["trade_authorized"])
        self.assertFalse(payload["live_orders_enabled"])
        self.assertEqual(payload["source_count"], 12)
        self.assertEqual(payload["sources"]["eia-open-data"]["status"], "LIVE")
        self.assertEqual(payload["sources"]["finra"]["status"], "UNCONFIGURED")
        serialized = json.dumps(payload)
        self.assertNotIn("eia-test-secret", serialized)
        self.assertNotIn("320193", serialized)

    def test_finra_reports_live_only_when_server_credentials_exist_and_probe_passes(self):
        patches = self._patch_public_sources()
        env = {
            "EIA_API_KEY": "eia-test-secret",
            "FINRA_CLIENT_ID": "finra-client",
            "FINRA_CLIENT_SECRET": "finra-test-secret",
        }
        with patch.dict("os.environ", env, clear=True), patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8], patches[9], patches[10]:
            payload = web_app.build_data_source_status()

        self.assertEqual(payload["sources"]["finra"]["status"], "LIVE")
        serialized = json.dumps(payload)
        self.assertNotIn("finra-client", serialized)
        self.assertNotIn("finra-test-secret", serialized)

    def test_upstream_exception_text_is_suppressed(self):
        patches = self._patch_public_sources()
        leaking_error = "upstream failed api_key=must-never-escape"
        with patch.dict("os.environ", {"EIA_API_KEY": "configured"}, clear=True), patches[0], patches[1], patches[2], patches[3], patches[4], patch.object(
            web_app, "nyfed_reference_rates", side_effect=ValueError(leaking_error)
        ), patches[6], patches[7], patches[8], patches[9], patches[10]:
            payload = web_app.build_data_source_status()

        nyfed = payload["sources"]["nyfed-markets"]
        self.assertEqual(nyfed["status"], "BLOCKED")
        self.assertEqual(nyfed["reason_code"], "UPSTREAM_OR_AUTH_FAILURE")
        self.assertNotIn("must-never-escape", json.dumps(payload))

    def test_existing_health_route_delegates_unchanged(self):
        with patch.dict("os.environ", {}, clear=True):
            status, _headers, payload = self._request("/api/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(payload["mode"], "paper")
        self.assertFalse(payload["live_orders_enabled"])


if __name__ == "__main__":
    unittest.main()
