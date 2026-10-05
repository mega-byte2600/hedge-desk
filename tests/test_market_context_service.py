import unittest
from unittest.mock import patch

from hedge_desk import market_context_service


class MarketContextServiceTests(unittest.TestCase):
    def tearDown(self):
        with market_context_service._lock:
            market_context_service._snapshot = None
            market_context_service._built_at = 0.0
            market_context_service._refreshing = False
            market_context_service._store_checked = False

    def test_first_request_returns_without_waiting_for_provider_fanout(self):
        with patch.object(market_context_service, "Thread") as thread:
            snapshot = market_context_service.get_market_context_snapshot()

        self.assertEqual(snapshot["status"], "LOADING")
        self.assertFalse(snapshot["trade_authorized"])
        thread.assert_called_once()
        thread.return_value.start.assert_called_once()

    def test_last_good_snapshot_is_returned_while_refresh_runs(self):
        saved = {
            "schema_version": "hedge-desk-market-context-1.0.0",
            "status": "DEGRADED",
            "live_sources": 1,
            "blocked_sources": 1,
            "unconfigured_sources": 0,
            "sources": {},
            "trade_authorized": False,
        }
        with market_context_service._lock:
            market_context_service._snapshot = saved
            market_context_service._built_at = 0.0
            market_context_service._refreshing = True

        with patch.object(market_context_service, "Thread") as thread:
            snapshot = market_context_service.get_market_context_snapshot()

        self.assertIs(snapshot, saved)
        self.assertFalse(snapshot["trade_authorized"])
        thread.assert_not_called()


if __name__ == "__main__":
    unittest.main()
