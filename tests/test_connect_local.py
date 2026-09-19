"""Deterministic tests for the local-only Schwab connector (no real creds)."""

import tempfile
import unittest
from pathlib import Path

from hedge_desk.connect_local import build_authorize_url, exchange_and_probe, load_env


def _env():
    return {
        "SCHWAB_CLIENT_ID": "TEST_APP_KEY",
        "SCHWAB_CLIENT_SECRET": "TEST_SECRET",
        "SCHWAB_REDIRECT_URI": "https://127.0.0.1/callback",
    }


class ConnectLocalTests(unittest.TestCase):
    def test_not_configured(self):
        result = build_authorize_url({})
        self.assertEqual(result["status"], "not_configured")

    def test_authorize_url_built_and_state_generated(self):
        result = build_authorize_url(_env())
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["state"])
        self.assertIn("response_type=code", result["authorize_url"])
        self.assertIn("scope=readonly", result["authorize_url"])

    def test_state_mismatch_rejected(self):
        r = exchange_and_probe(_env(), "code", "expected", "wrong")
        self.assertEqual(r["status"], "error")
        self.assertEqual(r["error"], "state_mismatch")

    def test_env_file_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "env.env"
            p.write_text("# comment\nSCHWAB_CLIENT_ID=\"MYKEY\"\nSCHWAB_CLIENT_SECRET=s3cret\n", encoding="utf-8")
            env = load_env(p)
            self.assertEqual(env["SCHWAB_CLIENT_ID"], "MYKEY")
            self.assertEqual(env["SCHWAB_CLIENT_SECRET"], "s3cret")

    def test_secret_never_in_returned_payload(self):
        # exchange_and_probe with a real transport would hit network; the point here
        # is the module must never place the secret in any returned dict. The
        # not-configured path is proof-by-construction; a failed exchange also
        # returns no secret.
        r = exchange_and_probe(_env(), "", "s", "s")
        self.assertEqual(r["status"], "error")
        blob = repr(r)
        for banned in ("TEST_SECRET", "s3cret"):
            self.assertNotIn(banned, blob)


if __name__ == "__main__":
    unittest.main()