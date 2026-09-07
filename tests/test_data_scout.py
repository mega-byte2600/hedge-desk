import unittest
from unittest.mock import patch

from hedge_desk import data_scout


class DataScoutTests(unittest.TestCase):
    @patch("hedge_desk.data_scout._github_json")
    def test_search_marks_missing_license_unsafe(self, mock_get):
        mock_get.return_value = {"items": [{
            "full_name": "example/finance-dataset",
            "html_url": "https://github.com/example/finance-dataset",
            "description": "Open financial dataset in parquet",
            "stargazers_count": 10,
            "updated_at": "2026-09-01T00:00:00Z",
            "license": None,
        }]}
        rows = data_scout.search_github("finance dataset")
        self.assertEqual(rows[0].commercial_use_status, "NO_LICENSE_METADATA_DO_NOT_USE")
        self.assertTrue(rows[0].dataset_signal)
        self.assertFalse(rows[0].open_license)

    @patch("hedge_desk.data_scout._github_json")
    def test_search_recognizes_permissive_license(self, mock_get):
        mock_get.return_value = {"items": [{
            "full_name": "example/quant-data",
            "html_url": "https://github.com/example/quant-data",
            "description": "Options volatility dataset",
            "stargazers_count": 5,
            "updated_at": "2026-09-02T00:00:00Z",
            "license": {"spdx_id": "MIT"},
        }]}
        rows = data_scout.search_github("options dataset")
        self.assertTrue(rows[0].open_license)
        self.assertEqual(rows[0].commercial_use_status, "OPEN_LICENSE_REVIEW_STILL_REQUIRED")

    @patch("hedge_desk.data_scout._github_json")
    def test_bond_dataset_is_classified_and_prioritized(self, mock_get):
        mock_get.return_value = {"items": [{
            "full_name": "example/treasury-yield-data",
            "html_url": "https://github.com/example/treasury-yield-data",
            "description": "US Treasury bond yield curve dataset with SOFR rates",
            "stargazers_count": 2,
            "updated_at": "2026-09-03T00:00:00Z",
            "license": {"spdx_id": "CC0-1.0"},
        }]}
        row = data_scout.search_github("treasury bond dataset yield curve rates")[0]
        self.assertTrue(row.bond_priority)
        self.assertIn("FIXED_INCOME_RATES", row.asset_classes)
        self.assertIn("SOVEREIGN", row.asset_classes)
        self.assertIn("AMERICAS", row.regions)
        self.assertGreaterEqual(row.discovery_score, 80)

    @patch("hedge_desk.data_scout.search_github")
    def test_discover_deduplicates_and_prefers_stronger_candidate(self, mock_search):
        a = data_scout.DatasetCandidate("x/repo", "u", "dataset", 1, "2026-01-01", "MIT", True, True, "OPEN_LICENSE_REVIEW_STILL_REQUIRED", "now", "q1", discovery_score=60)
        b = data_scout.DatasetCandidate("x/repo", "u", "dataset", 8, "2026-01-02", "MIT", True, True, "OPEN_LICENSE_REVIEW_STILL_REQUIRED", "now", "q2", discovery_score=70)
        mock_search.side_effect = [[a], [b]]
        result = data_scout.discover(["q1", "q2"])
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(result["candidates"][0]["stars"], 8)
        self.assertIs(result["commercial_use_assumed"], False)
        self.assertEqual(result["builder"], "mbolton")
        self.assertEqual(result["priority"], "BONDS_RATES_CREDIT_FIRST")
        self.assertIs(result["model_training_enabled"], False)

    @patch("hedge_desk.data_scout.search_github")
    def test_bond_candidate_sorts_before_non_bond_candidate(self, mock_search):
        equity = data_scout.DatasetCandidate("x/equity", "u", "equity dataset", 100, "2026-01-02", "MIT", True, True, "OPEN_LICENSE_REVIEW_STILL_REQUIRED", "now", "q1", asset_classes=("EQUITIES",), bond_priority=False, discovery_score=95)
        bonds = data_scout.DatasetCandidate("x/bonds", "u", "treasury dataset", 1, "2026-01-01", "MIT", True, True, "OPEN_LICENSE_REVIEW_STILL_REQUIRED", "now", "q2", asset_classes=("FIXED_INCOME_RATES",), bond_priority=True, discovery_score=80)
        mock_search.side_effect = [[equity], [bonds]]
        result = data_scout.discover(["q1", "q2"])
        self.assertEqual(result["candidates"][0]["repo"], "x/bonds")


if __name__ == "__main__":
    unittest.main()
