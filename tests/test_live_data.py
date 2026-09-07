import unittest
from datetime import datetime, timezone

from hedge_desk.live_data import build_operational_candidate_feed, fetch_treasury_curve


TREASURY_XML = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
      xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices">
  <entry><content type="application/xml"><m:properties>
    <d:NEW_DATE>2026-09-03T00:00:00</d:NEW_DATE><d:BC_2YEAR>3.55</d:BC_2YEAR>
    <d:BC_5YEAR>3.88</d:BC_5YEAR><d:BC_10YEAR>4.20</d:BC_10YEAR><d:BC_30YEAR>4.86</d:BC_30YEAR>
  </m:properties></content></entry>
  <entry><content type="application/xml"><m:properties>
    <d:NEW_DATE>2026-09-04T00:00:00</d:NEW_DATE><d:BC_2YEAR>3.57</d:BC_2YEAR>
    <d:BC_5YEAR>3.91</d:BC_5YEAR><d:BC_10YEAR>4.22</d:BC_10YEAR><d:BC_30YEAR>4.88</d:BC_30YEAR>
  </m:properties></content></entry>
</feed>"""


def fake_sec(_url):
    return {
        "filings": {
            "recent": {
                "form": ["8-K", "10-Q"],
                "filingDate": ["2026-09-02", "2026-08-01"],
                "accessionNumber": ["0000000000-26-000001", "0000000000-26-000002"],
                "primaryDocument": ["event.htm", "quarter.htm"],
            }
        }
    }


class OperationalDataTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc)

    def test_treasury_parser_selects_latest_public_observation(self):
        source = fetch_treasury_curve(now=self.now, fetch_text=lambda _url: TREASURY_XML)
        self.assertTrue(source["available"])
        self.assertEqual(source["curve"]["10Y"], 4.22)
        self.assertEqual(source["observed_at"], "2026-09-04T00:00:00+00:00")
        self.assertIn("expected_delay", source)

    def test_operational_feed_adds_real_rates_without_trade_authority(self):
        feed = build_operational_candidate_feed(
            now=self.now,
            fetch_text=lambda _url: TREASURY_XML,
            fetch_json=fake_sec,
            use_cache=False,
        )
        self.assertEqual(feed["schema_version"], "emporion-candidates-1.1.0")
        self.assertEqual(feed["data_priority"], "BONDS_RATES_CREDIT_FIRST")
        symbols = {row["symbol"] for row in feed["candidates"]}
        self.assertTrue({"UST2Y", "UST5Y", "UST10Y", "UST30Y"}.issubset(symbols))
        self.assertTrue(all(row["trade_authorized"] is False for row in feed["candidates"]))
        ust10 = next(row for row in feed["candidates"] if row["symbol"] == "UST10Y")
        self.assertEqual(ust10["observed_value"], 4.22)
        self.assertEqual(ust10["provider"], "U.S. Department of the Treasury")

    def test_source_failure_never_invents_market_values(self):
        def fail(_url):
            raise TimeoutError("offline")

        feed = build_operational_candidate_feed(
            now=self.now,
            fetch_text=fail,
            fetch_json=fail,
            use_cache=False,
        )
        self.assertEqual(feed["data_state"], "PUBLIC_DATA_UNAVAILABLE")
        self.assertFalse(any(row["symbol"].startswith("UST") for row in feed["candidates"]))
        self.assertTrue(all(row["trade_authorized"] is False for row in feed["candidates"]))


if __name__ == "__main__":
    unittest.main()
