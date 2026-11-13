"""Surface pins for the markets ticker (branch toby/market-ticker-refresh).

The ticker must stay a small, honest slice: one mount hook in the page
shell, assets listed in the deploy bundle, a committed feed artifact,
and no color encoding of direction (green is reserved for the
fresh-feed dot). Feed rows come only from the committed artifact; the
browser may call exactly one external host (the CNBC quote API, the
verified CORS-friendly keyless endpoint) and only for user-added
symbols. These tests pin the wiring so a later edit cannot silently
drop the strip from the deploy bundle or add an unvetted live call.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class MarketTickerSurfaceTest(unittest.TestCase):
    def test_index_mounts_ticker_with_explicit_hook(self):
        html = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="market-ticker"', html)
        self.assertEqual(html.count('id="market-ticker"'), 1)
        self.assertIn('href="./market-ticker.css"', html)
        self.assertIn('src="./market-ticker.mjs"', html)
        # The mount sits in the shell, outside the SPA root, so route
        # renders cannot wipe it.
        self.assertLess(html.index('id="market-ticker"'), html.index('id="main"'))

    def test_console_assets_include_ticker_files(self):
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        for name in ("market-ticker.css", "market-ticker.mjs", "market-ticker.json"):
            self.assertIn(f'"{name}"', build)
            self.assertTrue((WEB / name).is_file(), name)

    def test_committed_feed_shape(self):
        feed = json.loads((WEB / "market-ticker.json").read_text(encoding="utf-8"))
        self.assertEqual(feed["schema_version"], "market-ticker-1")
        self.assertRegex(feed["generated_at"], r"^\d{4}-\d{2}-\d{2}T")
        self.assertRegex(feed["as_of"], r"^\d{4}-\d{2}-\d{2}$")
        symbols = [q["symbol"] for q in feed["quotes"]]
        # Every default row is either quoted or explicitly quarantined
        # (intraday runs quarantine ^RUT: Yahoo returns no 1m bars for
        # it). A row that silently vanishes fails this test.
        covered = set(symbols) | set(feed.get("unavailable_symbols") or [])
        for sym in ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "PLTR",
                    "^GSPC", "^IXIC", "^DJI", "^RUT", "^TNX", "^FVX", "^IRX"):
            self.assertIn(sym, covered)
        for entry in feed.get("unavailable") or []:
            self.assertTrue(entry.get("symbol"))
            self.assertTrue(entry.get("reason"))
        self.assertIn(feed["mode"], ("intraday", "close"))
        self.assertIsInstance(feed["order"], list)
        for q in feed["quotes"]:
            self.assertIn(q["kind"], ("etf", "equity", "index", "rate"))
            for key in ("price", "previous_close", "change", "change_pct"):
                self.assertIsInstance(q[key], (int, float))
            self.assertRegex(q["quote_time"], r"^\d{4}-\d{2}-\d{2}T.*Z$")
            self.assertIn(q["session"], ("intraday", "close"))
            self.assertTrue(q["source"])
            # No placeholder or synthetic markers in a shipped feed.
            self.assertNotIn("synthetic", json.dumps(q).lower())

    def test_browser_module_calls_only_the_allowlisted_quote_host(self):
        js = (WEB / "market-ticker.mjs").read_text(encoding="utf-8")
        self.assertIn("FEED_URL = './market-ticker.json'", js)
        hosts = set(re.findall(r"https?://([^/'\"`\)]+)", js))
        # One external host, for user-added symbols only: CNBC, whose
        # Access-Control-Allow-Origin: * header was verified live.
        self.assertEqual(hosts, {"quote.cnbc.com"})
        self.assertNotIn("finance.yahoo", js)
        self.assertNotIn("api.nasdaq.com", js)
        self.assertNotRegex(js, r"(?i)api[_-]?key|secret|bearer")

    def test_green_is_reserved_for_the_fresh_feed_dot(self):
        css = (WEB / "market-ticker.css").read_text(encoding="utf-8")
        self.assertEqual(css.count("var(--live"), 1)
        self.assertIn(".mkt-dot-live", css)
        self.assertEqual(css.count("#35c26e"), 1)
        self.assertIn("background: var(--live, #35c26e);", css)
        self.assertIsNone(re.search(r":\s*red\b", css))
        self.assertNotIn("#ff0000", css)

    def test_generator_is_stdlib_only(self):
        src = (ROOT / "scripts" / "build_market_ticker.py").read_text(encoding="utf-8")
        imports = set(re.findall(r"^import (\w+)|^from (\w+)", src, re.M))
        flat = {a or b for a, b in imports}
        # subprocess (FRED helper CLI) and os (helper path/env) are
        # stdlib; anything else must justify itself here first.
        self.assertTrue(flat <= {"argparse", "json", "os", "subprocess", "sys",
                                 "urllib", "datetime", "pathlib", "zoneinfo",
                                 "__future__"}, flat)


if __name__ == "__main__":
    unittest.main()
