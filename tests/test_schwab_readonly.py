import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from hedge_desk.schwab_readonly import SchwabConfig, SchwabReadOnlyClient


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def read(self):
        return json.dumps(self.payload).encode()


class SchwabReadOnlyTests(unittest.TestCase):
    def test_missing_credentials_fail_closed(self) -> None:
        client = SchwabReadOnlyClient(SchwabConfig("", "", "http://localhost/cb", Path("none")))
        self.assertFalse(client.readiness()["ready_for_authorization_url"])
        self.assertTrue(client.readiness()["orders_blocked"])
        with self.assertRaises(ValueError):
            client.authorization_url()

    def test_authorization_state_and_token_are_secret_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token.json"
            client = SchwabReadOnlyClient(SchwabConfig("client", "secret", "http://localhost/cb", path))
            url = client.authorization_url()
            state = parse_qs(urlparse(url).query)["state"][0]
            with self.assertRaises(PermissionError):
                client.exchange_callback("code", "wrong-state")
            with patch("urllib.request.urlopen", return_value=_Response({"access_token": "private", "refresh_token": "refresh"})):
                result = client.exchange_callback("code", state)
            self.assertEqual(result["access_mode"], "READ_ONLY")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertNotIn("private", json.dumps(result))

    def test_client_exposes_no_order_operation(self) -> None:
        names = set(dir(SchwabReadOnlyClient))
        self.assertFalse(any("order" in name.lower() for name in names))


if __name__ == "__main__":
    unittest.main()
