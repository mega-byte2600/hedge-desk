"""CLI-level tests for the data-provider catalog (no network)."""

import json
import subprocess
import sys
import unittest

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "hedge_desk.cli", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
    )


class ProviderCliTests(unittest.TestCase):
    def test_list_providers_no_network(self):
        proc = _run("--list-providers")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        ids = {p["provider_id"] for p in payload}
        for expected in ("sec-edgar", "cftc-cot", "treasury-fiscaldata",
                         "stooq", "alpha-vantage", "fred", "nws", "eia-open-data"):
            self.assertIn(expected, ids)
        # key-gated providers disclose their env var, keyless ones disclose None
        alpha = next(p for p in payload if p["provider_id"] == "alpha-vantage")
        self.assertEqual(alpha["auth_env_var"], "ALPHA_VANTAGE_API_KEY")
        sec = next(p for p in payload if p["provider_id"] == "sec-edgar")
        self.assertIsNone(sec["auth_env_var"])
        self.assertTrue(sec["public_without_key"])

    def test_unknown_provider_is_usage_error(self):
        proc = _run("--data-provider", "nope", "--provider-series", "X")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("no live feed wired", proc.stderr)

    def test_key_gated_provider_fails_closed_without_key(self):
        # alpha-vantage has no open_market_feeds live handler -> clear usage error,
        # not a fabricated fetch. Key-gated feeds stay disabled until provisioned.
        proc = _run("--data-provider", "alpha-vantage", "--provider-series", "AAPL")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("no live feed wired", proc.stderr)

    def test_unknown_feed_param_is_reported(self):
        proc = _run("--data-provider", "ecb-fx", "--provider-param", "bogus=1")
        self.assertNotEqual(proc.returncode, 0)
        # fail closed on the unexpected kwarg, never fabricate rows
        self.assertIn("ecb-fx feed failed", proc.stderr)


if __name__ == "__main__":
    unittest.main()
