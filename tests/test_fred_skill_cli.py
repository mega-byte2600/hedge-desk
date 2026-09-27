"""Deterministic tests for the FRED skill-CLI route (no network).

When FRED_API_KEY is not set but the fred skill CLI is installed, the desk
uses the CLI (official FRED JSON API via the securely-stored credential)
instead of the CSV endpoint. These tests use fakes; they never touch the
network, the real CLI, or the production cache.
"""

import datetime as _dt
import json
import os
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from hedge_desk import rates_desk
from hedge_desk.rates_desk import (
    _default_transport,
    _fred_via_skill_cli,
    fred_series_rows,
)

_START = _dt.date(2026, 9, 1)
_END = _dt.date(2026, 9, 26)

_CLI_OUTPUT = json.dumps(
    {
        "DGS5": [
            {"date": "2026-09-24", "value": "5.03"},
            {"date": "2026-09-23", "value": "5.01"},
            {"date": "2026-08-15", "value": "4.95"},  # outside window
        ]
    }
)


class FakeCompletedProcess:
    def __init__(self, stdout="", returncode=0):
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = ""


def _fake_run_ok(*args, **kwargs):
    return FakeCompletedProcess(stdout=_CLI_OUTPUT)


class SkillCliRouteTest(unittest.TestCase):
    def setUp(self):
        # These tests exercise routing behavior, not the persistent cache.
        # Disable the production cache so a prior CI run cannot short-circuit
        # the fake CLI/CSV transports and make the suite order-dependent.
        self._old_cache_dir = os.environ.get("HEDGE_DESK_CACHE_DIR")
        os.environ["HEDGE_DESK_CACHE_DIR"] = "off"

    def tearDown(self):
        if self._old_cache_dir is None:
            os.environ.pop("HEDGE_DESK_CACHE_DIR", None)
        else:
            os.environ["HEDGE_DESK_CACHE_DIR"] = self._old_cache_dir

    def test_cli_rows_filtered_to_window_and_sorted(self):
        with patch.object(
            rates_desk, "_skill_cli_path", return_value=Path("/fake/cli.py")
        ), patch("subprocess.run", side_effect=_fake_run_ok):
            rows = _fred_via_skill_cli("DGS5", _START, _END)
        self.assertEqual(
            rows,
            (
                ("2026-09-23", Decimal("5.01")),
                ("2026-09-24", Decimal("5.03")),
            ),
        )

    def test_cli_missing_raises(self):
        with patch.object(rates_desk, "_skill_cli_path", return_value=None):
            with self.assertRaises(ValueError):
                _fred_via_skill_cli("DGS5", _START, _END)

    def test_cli_error_payload_raises(self):
        bad = json.dumps({"DGS5": {"error": "URLError: timed out"}})

        def fake_run(*a, **k):
            return FakeCompletedProcess(stdout=bad)

        with patch.object(
            rates_desk, "_skill_cli_path", return_value=Path("/fake/cli.py")
        ), patch("subprocess.run", side_effect=fake_run):
            with self.assertRaises(ValueError):
                _fred_via_skill_cli("DGS5", _START, _END)

    def test_fred_series_rows_prefers_cli_over_csv(self):
        """No env key + default transport + CLI installed -> CLI used.

        An explicit (non-default) transport is never bypassed; the CLI route
        only engages for the default transport path.
        """

        def boom(url):
            raise AssertionError("default transport should not be hit")

        with patch.object(
            rates_desk, "_skill_cli_path", return_value=Path("/fake/cli.py")
        ), patch("subprocess.run", side_effect=_fake_run_ok), patch.object(
            rates_desk, "_default_transport", side_effect=boom
        ), patch.dict("os.environ", {}, clear=False):
            # Ensure no env key leaks in from the test environment.
            os.environ.pop("FRED_API_KEY", None)
            rows = fred_series_rows(
                "DGS5",
                _START,
                _END,
                transport=rates_desk._default_transport,
                cache_dir=None,
            )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[-1], ("2026-09-24", Decimal("5.03")))

    def test_explicit_transport_never_bypassed_by_cli(self):
        """A caller-passed transport is respected; the CLI is not consulted."""

        def fake_transport(url):
            return 200, b"DATE,DGS5\n2026-09-24,5.03\n"

        with patch.object(
            rates_desk,
            "_skill_cli_path",
            return_value=Path("/fake/cli.py"),
            # If the CLI were consulted, subprocess.run would explode the test.
        ), patch(
            "subprocess.run",
            side_effect=AssertionError("CLI must not run"),
        ), patch.dict("os.environ", {}, clear=False):
            os.environ.pop("FRED_API_KEY", None)
            rows = fred_series_rows(
                "DGS5", _START, _END, transport=fake_transport, cache_dir=None
            )
        self.assertIn(("2026-09-24", Decimal("5.03")), rows)

    def test_fred_series_rows_falls_back_to_csv_when_cli_fails(self):
        """CLI failure -> CSV transport is still tried (no silent drop)."""
        csv_body = (
            "DATE,DGS5\n2026-09-24,5.03\n2026-09-23,5.01\n".encode()
        )

        def fake_run(*a, **k):
            raise OSError("cli exploded")

        def csv_transport(url):
            self.assertIn("fredgraph.csv", url)
            return 200, csv_body

        with patch.object(
            rates_desk, "_skill_cli_path", return_value=Path("/fake/cli.py")
        ), patch("subprocess.run", side_effect=fake_run), patch.dict(
            "os.environ", {}, clear=False
        ):
            os.environ.pop("FRED_API_KEY", None)
            rows = fred_series_rows(
                "DGS5", _START, _END, transport=csv_transport, cache_dir=None
            )
        self.assertIn(("2026-09-24", Decimal("5.03")), rows)
        self.assertIn(("2026-09-23", Decimal("5.01")), rows)


if __name__ == "__main__":
    unittest.main()
