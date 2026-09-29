"""CLI-level tests for the data-provider registry (no network)."""

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
        ids = {p["source_id"] for p in payload}
        self.assertIn("sec-edgar-companyfacts", ids)
        self.assertIn("cftc-cot", ids)
        self.assertIn("ust-treasury-fiscal", ids)
        self.assertIn("stooq-eod", ids)
        self.assertIn("alpha-vantage-eod", ids)

    def test_unknown_provider_is_usage_error(self):
        proc = _run("--data-provider", "nope", "--provider-series", "X")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unknown provider", proc.stderr)

    def test_missing_key_provider_fails_closed(self):
        # alpha-vantage with no key must QUARANTINE (CONFIG_MISSING_KEY), not fabricate.
        proc = _run("--data-provider", "alpha-vantage-eod", "--provider-series", "AAPL")
        self.assertEqual(proc.returncode, 1)
        self.assertIn('"status": "QUARANTINE"', proc.stdout)
        self.assertIn("CONFIG_MISSING_KEY", proc.stdout)


if __name__ == "__main__":
    unittest.main()
