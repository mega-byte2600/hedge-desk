from datetime import datetime, timedelta, timezone
from decimal import Decimal
import os
import unittest
from unittest.mock import patch

from hedge_desk.data import evaluate_pwb_daily_news, load_pwb_daily_news


NOW = datetime(2026, 9, 7, 12, tzinfo=timezone.utc)


def row(**changes):
    value = {
        "symbols": ["HAL"],
        "datetime": "2026-09-05T08:00:00+00:00",
        "title": "Halliburton example headline",
        "url": "https://example.com/news/hal",
        "authors": [],
        "summary": "Vendor text must not be retained.",
        "source": "Example News",
        "topics": [{"topic": "energy", "relevance_score": "0.9"}],
        "sentiment": 0.4,
        "symbol_sentiment": [{"symbol": "HAL", "sentiment_score": 0.5}],
    }
    value.update(changes)
    return value


class PwbNewsTests(unittest.TestCase):
    def test_emits_derived_feature_without_vendor_text(self):
        result = evaluate_pwb_daily_news(
            [row()], license_id="pwb-account-entitlement", evaluated_at=NOW,
            source_timezone=timezone.utc,
        )
        self.assertTrue(result.gate.admissible)
        self.assertFalse(result.raw_content_retained)
        self.assertFalse(result.trade_authorized)
        self.assertEqual(result.features[0].symbol, "HAL")
        self.assertEqual(result.features[0].average_symbol_sentiment, Decimal("0.5"))
        self.assertNotIn("headline", repr(result))
        self.assertNotIn("Vendor text", repr(result))

    def test_one_day_embargo_blocks_same_day_lookahead(self):
        result = evaluate_pwb_daily_news(
            [row(datetime="2026-09-07T08:00:00+00:00")],
            license_id="pwb-account-entitlement", evaluated_at=NOW,
            source_timezone=timezone.utc,
        )
        self.assertFalse(result.gate.admissible)
        self.assertIn("NEWS_POINT_IN_TIME_VIOLATION", result.gate.rejected_observations[0][1])

    def test_naive_vendor_timestamp_requires_explicit_timezone(self):
        with self.assertRaisesRegex(ValueError, "PWB_NEWS_SOURCE_TIMEZONE_REQUIRED"):
            evaluate_pwb_daily_news(
                [row(datetime="2026-09-05 08:00:00")],
                license_id="pwb-account-entitlement", evaluated_at=NOW,
                source_timezone=None,
            )

    def test_duplicate_evidence_and_out_of_range_sentiment_fail_closed(self):
        duplicate = evaluate_pwb_daily_news(
            [row(), row()], license_id="pwb-account-entitlement",
            evaluated_at=NOW, source_timezone=timezone.utc,
        )
        self.assertEqual(len(duplicate.gate.admitted_observation_ids), 1)
        self.assertIn("NEWS_DUPLICATE_EVIDENCE", duplicate.gate.rejected_observations[0][1])
        with self.assertRaisesRegex(ValueError, "PWB_NEWS_SENTIMENT_INVALID"):
            evaluate_pwb_daily_news(
                [row(symbol_sentiment=[{"symbol": "HAL", "sentiment_score": 2}])],
                license_id="pwb-account-entitlement", evaluated_at=NOW,
                source_timezone=timezone.utc,
            )

    def test_loader_requires_credential_and_uses_canonical_dataset_id(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "PWB_NEWS_API_CREDENTIAL_REQUIRED"):
                load_pwb_daily_news(lambda _: [])
        called = []
        with patch.dict(os.environ, {"PWB_API_KEY": "secret"}, clear=True):
            loaded = load_pwb_daily_news(lambda dataset: called.append(dataset) or [row()])
        self.assertEqual(called, ["All-Daily-News"])
        self.assertEqual(len(loaded), 1)


if __name__ == "__main__":
    unittest.main()
