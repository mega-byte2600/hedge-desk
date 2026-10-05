"""Deterministic tests for the BEA official-data adapter (no network)."""

import json
import os
import unittest
from unittest.mock import patch

from hedge_desk.data.open_market_feeds import bea_nipa


class BeaFeedTests(unittest.TestCase):
    def test_bea_nipa_parses_official_shape(self):
        payload = {
            "BEAAPI": {
                "Results": {
                    "Data": [
                        {"TableName": "T10101", "LineNumber": "1", "TimePeriod": "2026Q2", "DataValue": "31000.0"},
                        {"TableName": "T10101", "LineNumber": "2", "TimePeriod": "2026Q2", "DataValue": "25000.0"},
                    ]
                }
            }
        }
        seen = {}

        def transport(url):
            seen["url"] = url
            return 200, json.dumps(payload).encode("utf-8")

        result = bea_nipa(table="T10101", frequency="Q", year="2026", transport=transport, api_key="test-key")
        self.assertEqual(result.provider_id, "bea")
        self.assertEqual(result.dataset, "NIPA-T10101-Q")
        self.assertEqual(result.row_count, 2)
        self.assertIn("method=GetData", seen["url"])
        self.assertIn("datasetname=NIPA", seen["url"])
        self.assertIn("TableName=T10101", seen["url"])
        self.assertIn("Year=2026", seen["url"])

    def test_bea_nipa_fails_closed_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "BEA_API_KEY is required"):
                bea_nipa(transport=lambda _: (200, b"{}"))

    def test_bea_nipa_rejects_malformed_payload(self):
        def transport(_):
            return 200, json.dumps({"BEAAPI": {"Results": {}}}).encode("utf-8")

        with self.assertRaisesRegex(ValueError, "no Results.Data rows"):
            bea_nipa(transport=transport, api_key="test-key")

    def test_bea_nipa_validates_inputs_before_fetch(self):
        calls = []

        def transport(url):
            calls.append(url)
            return 200, b"{}"

        with self.assertRaisesRegex(ValueError, "frequency"):
            bea_nipa(frequency="M", transport=transport, api_key="test-key")
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
