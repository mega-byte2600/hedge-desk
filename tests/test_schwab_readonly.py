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
    def test_account_hashes_read_only_without_plain_numbers(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS))
        result = broker.account_hashes("tok")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])
        self.assertEqual(result["account_hashes"], ["abc", "def"])
        self.assertNotIn("12345678", str(result))

    def test_positions_read_only(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_POSITIONS))
        result = broker.positions("tok", "abc")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])
        self.assertEqual(len(result["positions"]), 1)
        self.assertNotIn("12345678", str(result))

    def test_balances_read_only(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_POSITIONS))
        result = broker.balances("tok", "abc")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["read_only"])
        self.assertIn("cashBalance", result["balances"])
        self.assertNotIn("12345678", str(result))

    def test_missing_token_fails_closed(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS))
        result = broker.account_hashes("")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "missing_token")

    def test_http_error_fails_closed(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(401, b"unauthorized"))
        result = broker.account_hashes("bad")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["http_status"], 401)

    def test_transport_exception_fails_closed(self):
        def boom(method, url, headers):
            raise OSError("network down")

        broker = SchwabReadOnlyBroker(transport=boom)
        result = broker.account_numbers("tok")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "transport_failure")

    def test_only_get_is_used_against_the_broker(self):
        capture = []
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_ACCOUNTS, capture))
        broker.account_hashes("tok")
        broker.positions("tok", "abc")
        broker.balances("tok", "abc")
        self.assertTrue(capture)
        self.assertTrue(all(c["method"] == "GET" for c in capture),
                        "read-only adapter must only issue GET requests")

    def test_hash_is_used_in_account_path_and_plain_number_is_never_used(self):
        capture = []
        broker = SchwabReadOnlyBroker(transport=make_transport(200, FIXTURE_POSITIONS, capture))
        broker.positions("tok", "hash/value")
        self.assertIn("/accounts/hash%2Fvalue?fields=positions", capture[0]["url"])
        self.assertNotIn("12345678", capture[0]["url"])

    def test_account_discovery_schema_errors_fail_closed(self):
        broker = SchwabReadOnlyBroker(transport=make_transport(200, b'{"unexpected":true}'))
        self.assertEqual(broker.account_hashes("tok")["error"], "unexpected_response_schema")

    def test_adapter_rejects_non_schwab_https_hosts(self):
        with self.assertRaisesRegex(ValueError, "official HTTPS host"):
            SchwabReadOnlyBroker(base_url="https://example.com")

    def test_module_contains_no_order_paths(self):
        src = Path(__file__).resolve().parents[1] / "hedge_desk" / "brokers" / "schwab_readonly.py"
        text = src.read_text(encoding="utf-8").lower()
        for forbidden in ("submit_order", "placeorder", "place_order", "cancel_order", "replace_order", "/orders"):
            self.assertNotIn(forbidden, text, f"read-only adapter must not contain {forbidden}")


if __name__ == "__main__":
    unittest.main()
