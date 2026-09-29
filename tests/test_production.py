import unittest
from dataclasses import dataclass
from unittest.mock import patch

from hedge_desk import production


@dataclass(frozen=True)
class _Rows:
    row_count: int = 1


class ProductionProbeTests(unittest.TestCase):
    def test_eia_probe_is_live_when_configured_and_rows_return(self):
        with patch.dict("os.environ", {"EIA_API_KEY": "test-secret"}, clear=True), patch.object(
            production, "eia_v2", return_value=_Rows()
        ) as fetch, patch("builtins.print") as output:
            status = production.probe_eia_startup()

        self.assertEqual(status, "LIVE")
        fetch.assert_called_once_with("petroleum/stoc/wstk", data=("value",), limit=1)
        logged = " ".join(str(arg) for call in output.call_args_list for arg in call.args)
        self.assertIn("status=LIVE", logged)
        self.assertNotIn("test-secret", logged)

    def test_eia_probe_is_unconfigured_without_key(self):
        with patch.dict("os.environ", {}, clear=True), patch.object(production, "eia_v2") as fetch:
            status = production.probe_eia_startup()

        self.assertEqual(status, "UNCONFIGURED")
        fetch.assert_not_called()

    def test_eia_probe_fails_closed_without_logging_exception(self):
        with patch.dict("os.environ", {"EIA_API_KEY": "test-secret"}, clear=True), patch.object(
            production, "eia_v2", side_effect=ValueError("api_key=test-secret upstream failure")
        ), patch("builtins.print") as output:
            status = production.probe_eia_startup()

        self.assertEqual(status, "BLOCKED")
        logged = " ".join(str(arg) for call in output.call_args_list for arg in call.args)
        self.assertIn("status=BLOCKED", logged)
        self.assertNotIn("test-secret", logged)
        self.assertNotIn("upstream failure", logged)


if __name__ == "__main__":
    unittest.main()
