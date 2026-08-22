from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.data import NewsObservation, NewsTransport, evaluate_news_batch


NOW = datetime(2026, 8, 22, 9, 0, tzinfo=timezone.utc)


def item():
    return NewsObservation(
        "news-1", "licensed-news-source", "https://example.com/news/1",
        "internal-research-entitlement", NewsTransport.RSS,
        NOW - timedelta(minutes=2), NOW - timedelta(minutes=1), "a" * 64,
        True, False,
    )


class NewsDataTests(unittest.TestCase):
    def test_boolean_age_flags_and_zero_hash_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonnegative integer"):
            evaluate_news_batch((item(),), NOW, True)
        result = evaluate_news_batch((replace(
            item(), publicly_available=1, content_sha256="0" * 64
        ),), NOW, 300)
        reasons = result.rejected_observations[0][1]
        self.assertIn("NEWS_ENTITLEMENT_FLAGS_INVALID", reasons)
        self.assertIn("NEWS_CONTENT_HASH_INVALID", reasons)

    def test_rss_can_admit_hashed_research_evidence_but_not_trade_or_commit(self) -> None:
        result = evaluate_news_batch((item(),), NOW, 120)
        self.assertTrue(result.admissible)
        self.assertTrue(result.research_evidence_only)
        self.assertFalse(result.trade_authorized)
        self.assertFalse(result.raw_content_commit_allowed)

    def test_missing_license_private_or_late_news_fails_closed(self) -> None:
        attacked = replace(
            item(), license_id="", publicly_available=False,
            received_at=NOW + timedelta(seconds=1),
        )
        result = evaluate_news_batch((attacked,), NOW, 120)
        self.assertFalse(result.admissible)
        reasons = result.rejected_observations[0][1]
        self.assertIn("NEWS_PROVENANCE_OR_LICENSE_MISSING", reasons)
        self.assertIn("NEWS_NOT_PUBLICLY_AVAILABLE", reasons)
        self.assertIn("NEWS_POINT_IN_TIME_VIOLATION", reasons)

    def test_duplicate_url_or_content_is_rejected(self) -> None:
        duplicate = replace(item(), observation_id="news-2")
        result = evaluate_news_batch((duplicate, item()), NOW, 120)
        self.assertEqual(len(result.admitted_observation_ids), 1)
        self.assertIn("NEWS_DUPLICATE_EVIDENCE", result.rejected_observations[0][1])


if __name__ == "__main__":
    unittest.main()
