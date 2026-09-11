import json
import unittest
from pathlib import Path

from hedge_desk.brokers.schwab_readonly import SchwabReadOnlyBroker


def make_transport(status=200, payload=b"{}", capture=None):
    def transport(method, url, headers):
        if capture is not None:
            capture.append({"method": method, "url": url, "headers": headers})
        return status, payload

    return transport


FIXTURE_ACCOUNTS = json.dumps(
    [
        {"accountNumber": "12345678", "hashValue": "abc"},
        {"accountNumber": "87654321", "hashValue": "def"},
    ]
).encode()

FIXTURE_POSITIONS = json.dumps(
    {
        "securitiesAccount": {
            "accountNumber": "12345678",
            "currentBalances": {"liquidationValue": 100000.00, "cashBalance": 2500.00},
            "positions": [
                {"instrument": {"symbol": "AAPL", "assetType": "EQUITY"}, "longQuantity": 10, "marketValue": 1900.0},
            ],
        }
    }
).encode()


class SchwabReadOnlyTests(unittest.TestCase):
    def test_account_numbers_read_only(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS))
        result = broker.account_numbers("tok")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])
        self.assertEqual(result["account_numbers"], ["12345678", "87654321"])

    def test_positions_read_only(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_POSITIONS))
        result = broker.positions("tok", "12345678")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])
        self.assertIn("securitiesAccount", result["positions"])

    def test_balances_read_only(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_POSITIONS))
        result = broker.balances("tok", "12345678")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])

    def test_missing_token_fails_closed(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS))
        result = broker.account_numbers("")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "missing_token")

    def test_http_error_fails_closed(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(401, b"unauthorized"))
        result = broker.account_numbers("bad")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["http_status"], 401)

    def test_transport_exception_fails_closed(self):
        def boom(method, url, headers):
            raise OSError("network down")

        broker = SchwabReadOnlyBroker(transport=boom)
        result = broker.account_numbers("tok")
        self.assertEqual(result["status"], "error")
        self.assertIn("transport", result["error"])

    def test_only_get_is_used_against_the_broker(self):
        capture = []
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS, capture))
        broker.account_numbers("tok")
        broker.positions("tok", "12345678")
        broker.balances("tok", "12345678")
        self.assertTrue(capture)
        self.assertTrue(all(c["method"] == "GET" for c in capture),
                        "read-only adapter must only issue GET requests")

    def test_module_contains_no_order_paths(self):
        src = Path(__file__).resolve().parents[1] / "hedge_desk" / "brokers" / "schwab_readonly.py"
        text = src.read_text(encoding="utf-8").lower()
        for forbidden in ("submit_order", "placeorder", "place_order", "cancel_order", "replace_order", "/orders"):
            self.assertNotIn(forbidden, text, f"read-only adapter must not contain {forbidden}")


if __name__ == "__main__":
    unittest.main()
