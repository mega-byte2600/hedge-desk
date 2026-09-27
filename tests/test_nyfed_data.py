import json
import unittest
from decimal import Decimal

from hedge_desk.data.nyfed import latest_reference_rates, reference_rate_history


def _transport(payload, status=200, seen=None):
    raw = json.dumps(payload).encode("utf-8")

    def fetch(url):
        if seen is not None:
            seen.append(url)
        return status, raw

    return fetch


class NyFedReferenceRateTests(unittest.TestCase):
    def test_latest_rates_parse_official_shape(self):
        seen = []
        rows = latest_reference_rates(
            transport=_transport(
                {
                    "refRates": [
                        {
                            "effectiveDate": "2026-09-24",
                            "type": "SOFR",
                            "percentRate": 3.88,
                            "volumeInBillions": 2990,
                        },
                        {
                            "effectiveDate": "2026-09-24",
                            "type": "EFFR",
                            "percentRate": 3.88,
                            "volumeInBillions": 105,
                        },
                    ]
                },
                seen=seen,
            )
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].rate_type, "SOFR")
        self.assertEqual(rows[0].percent_rate, Decimal("3.88"))
        self.assertEqual(rows[0].volume_billions, Decimal("2990"))
        self.assertEqual(
            seen[0],
            "https://markets.newyorkfed.org/api/rates/all/latest.json",
        )

    def test_history_uses_supported_official_route(self):
        seen = []
        rows = reference_rate_history(
            "SOFR",
            limit=5,
            transport=_transport(
                {
                    "refRates": [
                        {
                            "effectiveDate": "2026-09-24",
                            "type": "SOFR",
                            "percentRate": "3.88",
                            "volumeInBillions": "2990",
                        }
                    ]
                },
                seen=seen,
            ),
        )
        self.assertEqual(rows[0].source_id, "nyfed-markets")
        self.assertTrue(seen[0].endswith("/api/rates/secured/sofr/last/5.json"))

    def test_unsupported_rate_fails_before_network(self):
        with self.assertRaisesRegex(ValueError, "unsupported NY Fed"):
            reference_rate_history("LIBOR", transport=_transport({}))

    def test_bad_http_and_payload_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "status 503"):
            latest_reference_rates(transport=lambda _url: (503, b"down"))
        with self.assertRaisesRegex(ValueError, "malformed JSON"):
            latest_reference_rates(transport=lambda _url: (200, b"not-json"))
        with self.assertRaisesRegex(ValueError, "no refRates"):
            latest_reference_rates(transport=_transport({"other": []}))

    def test_non_rate_rows_are_ignored(self):
        rows = latest_reference_rates(
            transport=_transport(
                {
                    "refRates": [
                        {
                            "effectiveDate": "2026-09-25",
                            "type": "SOFRAI",
                            "average30day": 3.70,
                        },
                        {
                            "effectiveDate": "2026-09-24",
                            "type": "BGCR",
                            "percentRate": 3.86,
                            "volumeInBillions": 1253,
                        },
                    ]
                }
            )
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].rate_type, "BGCR")


if __name__ == "__main__":
    unittest.main()
