from copy import deepcopy
import json
import unittest

from scripts.validate_high_flyer_catalog import CATALOG, validate_catalog


class HighFlyerCatalogTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_is_valid_and_keeps_unreleased_trading_assets_explicit(self):
        result = validate_catalog(self.payload)
        self.assertEqual(result["status"], "VALID")
        self.assertGreaterEqual(result["paper_count"], 10)
        self.assertEqual(result["dataset_count"], 2)
        unavailable = " ".join(self.payload["known_unreleased"]).lower()
        self.assertIn("trading data", unavailable)
        self.assertIn("pretraining corpora", unavailable)

    def test_duplicate_source_id_fails_closed(self):
        attacked = deepcopy(self.payload)
        attacked["sources"][1]["id"] = attacked["sources"][0]["id"]
        with self.assertRaisesRegex(ValueError, "HIGH_FLYER_SOURCE_ID_DUPLICATE"):
            validate_catalog(attacked)

    def test_non_https_and_unknown_desk_fail_closed(self):
        attacked = deepcopy(self.payload)
        attacked["sources"][0]["url"] = "http://example.com"
        with self.assertRaisesRegex(ValueError, "HIGH_FLYER_SOURCE_URL_INVALID"):
            validate_catalog(attacked)
        attacked = deepcopy(self.payload)
        attacked["sources"][0]["desks"] = ["live-trading-desk"]
        with self.assertRaisesRegex(ValueError, "HIGH_FLYER_SOURCE_DESK_INVALID"):
            validate_catalog(attacked)


if __name__ == "__main__":
    unittest.main()
