"""Deterministic tests for the keyless data-integration modules.

No live network: every test injects a fixture transport. Clocks are fixed.
Sleeps are patched out. Run any of:
  python3 tests/test_data_integrations.py
  python -m unittest tests.test_data_integrations -v
  python -m unittest discover -s tests -v
"""

import io
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hedge_desk.data.feed_base as feed_base
import hedge_desk.data.event_wire as event_wire
from hedge_desk.data.feed_base import FeedResult  # noqa: F401
from hedge_desk.data.nasdaq_calendars import nasdaq_dividends_calendar, nasdaq_splits_calendar
from hedge_desk.data.research_lit import arxiv_search, semantic_scholar_search
from hedge_desk.data.event_wire import (
    GDELT_MIN_PACING_SECONDS,
    GdeltPacer,
    gdelt_artlist,
)
from hedge_desk.data.sec_fts import sec_fulltext_search

FIXED_NOW = "2026-10-04T19:00:00+00:00"

_DIVIDENDS_FIXTURE = b"""{"data":{"calendar":{"asOf":"Fri, Oct 2, 2026","headers":{"symbol":"Symbol"},
"rows":[{"companyName":"Alico, Inc. Common Stock","symbol":"ALCO",
"dividend_Ex_Date":"10/02/2026","payment_Date":"10/16/2026","record_Date":"10/02/2026",
"dividend_Rate":0.05,"indicated_Annual_Dividend":0.2,"announcement_Date":"9/08/2026"}]}}}"""

_SPLITS_FIXTURE = b"""{"data":{"asOf":"Sun, Oct 4, 2026",
"rows":[{"symbol":"LU","name":"Lufax Holding Ltd","ratio":"1 : 10","executionDate":"10/23/2026"}]}}"""

_ARXIV_FIXTURE = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry><id>http://arxiv.org/abs/2601.00001v1</id>
<title>Option Pricing with Neural Nets</title>
<summary>We study option pricing.</summary>
<published>2026-01-05T00:00:00Z</published>
<author><name>Ada Lovelace</name></author>
<author><name>Alan Turing</name></author>
<link href="https://arxiv.org/abs/2601.00001v1" rel="alternate" type="text/html"/>
</entry>
<entry><id>http://arxiv.org/abs/2601.00002v1</id>
<title>Volatility Forecasting</title>
<summary>Forecasting realized volatility.</summary>
<published>2025-12-20T00:00:00Z</published>
<author><name>John Doe</name></author>
<link href="https://arxiv.org/abs/2601.00002v1" rel="alternate" type="text/html"/>
</entry></feed>"""

_S2_FIXTURE = b"""{"data":[{"title":"Paper A","abstract":"Abstract A.","year":2024,
"url":"https://example.com/a","authors":[{"name":"Jane Roe"}]}]}"""

_S2_429_FIXTURE = b"""{"message": "Too Many Requests. Please wait and try again", "code": "429"}"""

_GDELT_FIXTURE = b"""{"articles":[{"url":"https://example.com/news1","url_mobile":"",
"title":"Fed holds rates","seendate":"20261004T120000Z","socialimage":"",
"domain":"example.com","language":"English","sourcecountry":"United States"}]}"""

_GDELT_NOTICE = (
    b"Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com "
    b"for larger queries.\n"
)

_FTS_FIXTURE = b"""{"hits":{"hits":[{"_source":{"form":"8-K","c_name":"ACME Corp","c_cik":"0001234567",
"f_date":"2026-09-30","adsh":"0001234567-26-000001","title":"Material agreement"}}]}}"""

_OPENFIGI_FIXTURE = b"""[{"data":[{"figi":"BBG000BPH459","name":"Apple Inc",
"ticker":"AAPL","exchCode":"US","shareClassFIGI":"BBG001S5N8V8","securityType":"Common Stock"}]},
{"error":"No identifier found."}]"""


def _ok(payload: bytes):
    return lambda url: (200, payload)


def _boom(url):
    return (0, b"connection refused")


def _request_ok(payload: bytes):
    return lambda req: (200, payload)


def _request_status(status: int, payload: bytes):
    return lambda req: (status, payload)


def _expect_value_error(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except ValueError:
        return
    raise AssertionError(f"expected ValueError from {fn.__name__}")


def _fake_clock(start=1000.0):
    state = {"t": start}
    return state, lambda: state["t"]


def _no_sleep():
    return mock.patch("time.sleep")


class FeedBaseTests(unittest.TestCase):
    def test_feed_result_row_count(self):
        r = FeedResult(provider_id="p", dataset="d", rows=({"a": 1}, {"a": 2}))
        self.assertEqual(r.row_count, 2)
        self.assertEqual(r.fetched_at, "")
        self.assertEqual(FeedResult(provider_id="p", dataset="d", rows=()).row_count, 0)

    def test_utc_now_iso(self):
        from datetime import datetime

        ts = feed_base.utc_now_iso()
        self.assertIsNotNone(datetime.fromisoformat(ts).tzinfo)

    def test_is_transient_status(self):
        for s in (0, 429, 500, 503, 599):
            self.assertTrue(feed_base._is_transient_status(s), s)
        for s in (200, 201, 400, 401, 403, 404, 600):
            self.assertFalse(feed_base._is_transient_status(s), s)

    def test_positive_limit_ok(self):
        self.assertEqual(feed_base._positive_limit(1), 1)
        self.assertEqual(feed_base._positive_limit(1000), 1000)
        self.assertEqual(feed_base._positive_limit(5, maximum=10), 5)

    def test_positive_limit_rejects(self):
        for bad in (0, -3, 1001, "5", 5.0, True, None):
            with self.assertRaises(ValueError, msg=repr(bad)):
                feed_base._positive_limit(bad)
        with self.assertRaises(ValueError):
            feed_base._positive_limit(11, maximum=10)

    def test_decode_json_ok(self):
        self.assertEqual(feed_base._decode_json(b'{"a":1}', "p"), {"a": 1})

    def test_decode_json_malformed(self):
        with self.assertRaises(ValueError) as ctx:
            feed_base._decode_json(b"{nope", "p")
        self.assertIn("malformed JSON", str(ctx.exception))

    def test_decode_json_bad_utf8(self):
        with self.assertRaises(ValueError):
            feed_base._decode_json(b"\xff\xfe\x00bad", "p")

    def test_rows_from_list_ok(self):
        self.assertEqual(feed_base._rows_from_list([{"a": 1}], "p"), ({"a": 1},))
        self.assertEqual(feed_base._rows_from_list([], "p"), ())

    def test_rows_from_list_not_a_list(self):
        with self.assertRaises(ValueError):
            feed_base._rows_from_list({"a": 1}, "p")

    def test_rows_from_list_row_not_object(self):
        with self.assertRaises(ValueError):
            feed_base._rows_from_list([{"a": 1}, 42], "p")

    def test_normalize_iso_date_formats(self):
        self.assertEqual(feed_base._normalize_iso_date("10/02/2026"), "2026-10-02")
        self.assertEqual(feed_base._normalize_iso_date("2026-10-02"), "2026-10-02")
        self.assertIsNone(feed_base._normalize_iso_date(""))
        self.assertIsNone(feed_base._normalize_iso_date("   "))
        self.assertIsNone(feed_base._normalize_iso_date(None))
        self.assertIsNone(feed_base._normalize_iso_date("not a date"))
        self.assertIsNone(feed_base._normalize_iso_date("13/45/2026"))

    def test_fetch_json_success(self):
        with _no_sleep() as ms:
            out = feed_base._fetch_json("http://x", "prov", lambda u: (200, b'{"a":1}'))
        self.assertEqual(out, {"a": 1})
        ms.assert_not_called()

    def test_fetch_json_retries_transient_then_succeeds(self):
        calls = {"n": 0}

        def t(u):
            calls["n"] += 1
            return (503, b"") if calls["n"] == 1 else (200, b'{"ok":true}')

        with _no_sleep() as ms:
            out = feed_base._fetch_json("http://x", "prov", t)
        self.assertEqual(out, {"ok": True})
        ms.assert_called_once_with(1.0)

    def test_fetch_json_exhausts_retries(self):
        with _no_sleep() as ms:
            with self.assertRaises(ValueError) as ctx:
                feed_base._fetch_json("http://x", "prov", lambda u: (503, b"busy"))
        self.assertIn("status 503", str(ctx.exception))
        self.assertIn("busy", str(ctx.exception))
        self.assertEqual([c.args[0] for c in ms.call_args_list], [1.0, 2.0])

    def test_fetch_json_non_transient_fails_fast(self):
        with _no_sleep() as ms:
            with self.assertRaises(ValueError) as ctx:
                feed_base._fetch_json("http://x", "prov", lambda u: (404, b"nope"))
        self.assertIn("status 404", str(ctx.exception))
        ms.assert_not_called()

    def test_fetch_json_transport_raises(self):
        def boom(u):
            raise RuntimeError("down")

        with _no_sleep():
            with self.assertRaises(ValueError) as ctx:
                feed_base._fetch_json("http://x", "prov", boom)
        self.assertIn("status 0", str(ctx.exception))

    def test_fetch_json_malformed_body(self):
        with self.assertRaises(ValueError) as ctx:
            feed_base._fetch_json("http://x", "prov", lambda u: (200, b"not json"))
        self.assertIn("malformed JSON", str(ctx.exception))

    def test_fetch_json_empty_200_body(self):
        with self.assertRaises(ValueError) as ctx:
            feed_base._fetch_json("http://x", "prov", lambda u: (200, b""))
        self.assertIn("status 200", str(ctx.exception))

    def test_fetch_bytes_success(self):
        with _no_sleep() as ms:
            out = feed_base._fetch_bytes("http://x", "prov", lambda u: (200, b"raw"))
        self.assertEqual(out, b"raw")
        ms.assert_not_called()

    def test_fetch_bytes_retries_then_succeeds(self):
        calls = {"n": 0}

        def t(u):
            calls["n"] += 1
            return (429, b"slow") if calls["n"] == 1 else (200, b"raw")

        with _no_sleep() as ms:
            out = feed_base._fetch_bytes("http://x", "prov", t)
        self.assertEqual(out, b"raw")
        ms.assert_called_once_with(1.0)

    def test_fetch_bytes_exhausts_retries(self):
        with _no_sleep() as ms:
            with self.assertRaises(ValueError) as ctx:
                feed_base._fetch_bytes("http://x", "prov", lambda u: (500, b""))
        self.assertIn("status 500", str(ctx.exception))
        self.assertEqual([c.args[0] for c in ms.call_args_list], [1.0, 2.0])

    def test_fetch_bytes_transport_raises(self):
        def boom(u):
            raise ConnectionError("nope")

        with _no_sleep():
            with self.assertRaises(ValueError) as ctx:
                feed_base._fetch_bytes("http://x", "prov", boom)
        self.assertIn("status 0", str(ctx.exception))

    def test_urlopen_success(self):
        fake = mock.MagicMock()
        fake.__enter__.return_value = fake
        fake.status = 200
        fake.read.return_value = b"data"
        with mock.patch.object(urllib.request, "urlopen", return_value=fake):
            self.assertEqual(
                feed_base._urlopen(urllib.request.Request("http://x"), 5),
                (200, b"data"),
            )

    def test_urlopen_http_error(self):
        err = urllib.error.HTTPError(
            "http://x", 404, "Not Found", {}, io.BytesIO(b"nope")
        )
        with mock.patch.object(urllib.request, "urlopen", side_effect=err):
            self.assertEqual(
                feed_base._urlopen(urllib.request.Request("http://x"), 5),
                (404, b"nope"),
            )

    def test_urlopen_generic_error(self):
        with mock.patch.object(urllib.request, "urlopen", side_effect=OSError("boom")):
            status, raw = feed_base._urlopen(urllib.request.Request("http://x"), 5)
        self.assertEqual(status, 0)
        self.assertIn(b"boom", raw)

    def test_make_get_transport_builds_request(self):
        with mock.patch.object(
            feed_base, "_urlopen", return_value=(200, b"ok")
        ) as m:
            t = feed_base.make_get_transport({"X-Custom": "yes"}, timeout=7)
            self.assertEqual(t("http://example.com/x"), (200, b"ok"))
            req, timeout = m.call_args[0]
            headers = {k.lower(): v for k, v in req.header_items()}
            self.assertEqual(headers.get("x-custom"), "yes")
            self.assertEqual(timeout, 7)
            self.assertEqual(req.full_url, "http://example.com/x")

    def test_sec_user_agent_prefers_env_override(self):
        with mock.patch.dict(
            os.environ, {"SEC_USER_AGENT": "custom-agent/2.0"}, clear=False
        ):
            self.assertEqual(feed_base._sec_user_agent(), "custom-agent/2.0")

    def test_sec_user_agent_uses_contact_email(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("SEC_USER_AGENT", "SEC_CONTACT_EMAIL")
        }
        env["SEC_CONTACT_EMAIL"] = "desk@example.com"
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(
                feed_base._sec_user_agent(), "hedge-desk/1.0 desk@example.com"
            )

    def test_sec_user_agent_default(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("SEC_USER_AGENT", "SEC_CONTACT_EMAIL")
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(feed_base._sec_user_agent(), feed_base._DEFAULT_UA)

    def test_default_transports_are_callable(self):
        for t in (
            feed_base._default_transport,
            feed_base._nasdaq_transport,
            feed_base._sec_transport,
        ):
            self.assertTrue(callable(t))


class NasdaqCalendarTests(unittest.TestCase):
    def test_nasdaq_dividends_happy(self):
        res = nasdaq_dividends_calendar(
            "2026-10-02", transport=_ok(_DIVIDENDS_FIXTURE), now=lambda: FIXED_NOW
        )
        assert res.provider_id == "nasdaq-calendars"
        assert res.dataset == "dividends-calendar"
        assert res.fetched_at == FIXED_NOW
        row = res.rows[0]
        assert row["symbol"] == "ALCO"
        assert row["dividend_Ex_Date_iso"] == "2026-10-02"
        assert row["payment_Date_iso"] == "2026-10-16"
        assert row["announcement_Date_iso"] == "2026-09-08"
        assert row["calendarDate"] == "2026-10-02"

    def test_nasdaq_splits_happy(self):
        res = nasdaq_splits_calendar(
            "2026-10-04", transport=_ok(_SPLITS_FIXTURE), now=lambda: FIXED_NOW
        )
        assert res.dataset == "splits-calendar"
        row = res.rows[0]
        assert row["symbol"] == "LU"
        assert row["ratio"] == "1 : 10"
        assert row["executionDate_iso"] == "2026-10-23"

    def test_nasdaq_bad_date(self):
        _expect_value_error(nasdaq_dividends_calendar, "not-a-date", transport=_ok(b"{}"))

    def test_nasdaq_malformed_payload(self):
        _expect_value_error(
            nasdaq_dividends_calendar,
            "2026-10-02",
            transport=_ok(b'{"data": "nope"}'),
            now=lambda: FIXED_NOW,
        )
        _expect_value_error(
            nasdaq_splits_calendar,
            "2026-10-02",
            transport=_ok(b"not json"),
            now=lambda: FIXED_NOW,
        )

    def test_nasdaq_transport_error(self):
        with _no_sleep():
            _expect_value_error(
                nasdaq_dividends_calendar,
                "2026-10-02",
                transport=_boom,
                now=lambda: FIXED_NOW,
            )

    def test_nasdaq_day_accepts_date_and_datetime(self):
        import datetime as dt

        captured = {}

        def spy(url):
            captured["url"] = url
            return (200, _DIVIDENDS_FIXTURE)

        nasdaq_dividends_calendar(dt.date(2026, 10, 2), transport=spy, now=lambda: FIXED_NOW)
        self.assertIn("date=2026-10-02", captured["url"])
        nasdaq_splits_calendar(
            dt.datetime(2026, 10, 4, 12, 30), transport=spy, now=lambda: FIXED_NOW
        )
        self.assertIn("date=2026-10-04", captured["url"])

    def test_nasdaq_dividends_unparsable_date_keeps_raw(self):
        payload = b'{"data":{"calendar":{"rows":[{"symbol":"X","dividend_Ex_Date":"TBD","payment_Date":""}]}}}'
        res = nasdaq_dividends_calendar(
            "2026-10-02", transport=_ok(payload), now=lambda: FIXED_NOW
        )
        row = res.rows[0]
        self.assertEqual(row["dividend_Ex_Date"], "TBD")
        self.assertIsNone(row["dividend_Ex_Date_iso"])
        self.assertIsNone(row["payment_Date_iso"])
        self.assertEqual(row["calendarDate"], "2026-10-02")

    def test_nasdaq_calendar_missing_rows(self):
        _expect_value_error(
            nasdaq_dividends_calendar,
            "2026-10-02",
            transport=_ok(b'{"data":{"calendar":{}}}'),
            now=lambda: FIXED_NOW,
        )
        _expect_value_error(
            nasdaq_splits_calendar,
            "2026-10-02",
            transport=_ok(b'{"data":{}}'),
            now=lambda: FIXED_NOW,
        )

    def test_nasdaq_payload_not_object(self):
        _expect_value_error(
            nasdaq_dividends_calendar,
            "2026-10-02",
            transport=_ok(b"[1,2]"),
            now=lambda: FIXED_NOW,
        )

    def test_nasdaq_calendar_rows_not_list(self):
        _expect_value_error(
            nasdaq_dividends_calendar,
            "2026-10-02",
            transport=_ok(b'{"data":{"calendar":{"rows":{"a":1}}}}'),
            now=lambda: FIXED_NOW,
        )

    def test_nasdaq_calendar_non_dict_shape(self):
        # calendar present but not a dict -> rows read from data.rows
        payload = b'{"data":{"calendar":["x"],"rows":[{"symbol":"Y","executionDate":"10/23/2026"}]}}'
        res = nasdaq_splits_calendar(
            "2026-10-04", transport=_ok(payload), now=lambda: FIXED_NOW
        )
        self.assertEqual(res.rows[0]["symbol"], "Y")
        self.assertEqual(res.rows[0]["executionDate_iso"], "2026-10-23")

    def test_nasdaq_splits_transport_error(self):
        with _no_sleep():
            _expect_value_error(
                nasdaq_splits_calendar,
                "2026-10-04",
                transport=_boom,
                now=lambda: FIXED_NOW,
            )

    def test_nasdaq_429_fails_closed(self):
        with _no_sleep():
            try:
                nasdaq_dividends_calendar(
                    "2026-10-02",
                    transport=lambda u: (429, b"slow"),
                    now=lambda: FIXED_NOW,
                )
            except ValueError as exc:
                self.assertIn("status 429", str(exc))
                return
        raise AssertionError("expected ValueError on nasdaq 429")


class ResearchLitTests(unittest.TestCase):
    def test_arxiv_happy(self):
        res = arxiv_search("all:option", max_results=2, transport=_ok(_ARXIV_FIXTURE), now=lambda: FIXED_NOW)
        assert res.provider_id == "arxiv"
        assert res.row_count == 2
        row = res.rows[0]
        assert row["title"] == "Option Pricing with Neural Nets"
        assert row["abstract"] == "We study option pricing."
        assert row["year"] == "2026"
        assert row["url"] == "https://arxiv.org/abs/2601.00001v1"
        assert row["authors"] == ["Ada Lovelace", "Alan Turing"]
        assert row["source"] == "arxiv"
        assert row["arxiv_id"] == "2601.00001v1"

    def test_arxiv_malformed_xml(self):
        _expect_value_error(arxiv_search, "all:option", transport=_ok(b"<broken"), now=lambda: FIXED_NOW)

    def test_arxiv_transport_error(self):
        with _no_sleep():
            _expect_value_error(arxiv_search, "all:option", transport=_boom, now=lambda: FIXED_NOW)

    def test_arxiv_empty_query(self):
        _expect_value_error(arxiv_search, "  ", transport=_ok(_ARXIV_FIXTURE))

    def test_arxiv_start_validation(self):
        _expect_value_error(
            arxiv_search, "all:x", start=-1, transport=_ok(_ARXIV_FIXTURE)
        )
        _expect_value_error(
            arxiv_search, "all:x", start="0", transport=_ok(_ARXIV_FIXTURE)
        )

    def test_arxiv_max_results_validation(self):
        _expect_value_error(
            arxiv_search, "all:x", max_results=0, transport=_ok(_ARXIV_FIXTURE)
        )
        _expect_value_error(
            arxiv_search, "all:x", max_results=501, transport=_ok(_ARXIV_FIXTURE)
        )

    def test_arxiv_empty_feed(self):
        feed = b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        res = arxiv_search("all:x", transport=_ok(feed), now=lambda: FIXED_NOW)
        self.assertEqual(res.rows, ())
        self.assertEqual(res.row_count, 0)

    def test_arxiv_entry_without_id_fails_closed(self):
        feed = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>No id</title></entry></feed>'
        _expect_value_error(arxiv_search, "all:x", transport=_ok(feed), now=lambda: FIXED_NOW)

    def test_arxiv_non_atom_root(self):
        _expect_value_error(
            arxiv_search,
            "all:x",
            transport=_ok(b"<html><body>nope</body></html>"),
            now=lambda: FIXED_NOW,
        )

    def test_arxiv_missing_optional_fields(self):
        feed = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/2601.9v1</id></entry></feed>'
        res = arxiv_search("all:x", transport=_ok(feed), now=lambda: FIXED_NOW)
        row = res.rows[0]
        self.assertEqual(row["title"], "")
        self.assertEqual(row["abstract"], "")
        self.assertEqual(row["year"], "")
        self.assertEqual(row["authors"], [])
        self.assertEqual(row["url"], "http://arxiv.org/abs/2601.9v1")
        self.assertEqual(row["arxiv_id"], "2601.9v1")

    def test_arxiv_author_without_name_skipped(self):
        feed = (
            b'<feed xmlns="http://www.w3.org/2005/Atom">'
            b'<entry><id>http://arxiv.org/abs/1v1</id>'
            b'<author><name>  </name></author><author></author>'
            b'<link href="https://arxiv.org/abs/1v1" rel="alternate"/></entry></feed>'
        )
        res = arxiv_search("all:x", transport=_ok(feed), now=lambda: FIXED_NOW)
        self.assertEqual(res.rows[0]["authors"], [])

    def test_arxiv_server_error_fails_closed(self):
        with _no_sleep():
            _expect_value_error(
                arxiv_search, "all:x", transport=lambda u: (500, b"err"), now=lambda: FIXED_NOW
            )

    def test_arxiv_query_params(self):
        captured = {}

        def spy(url):
            captured["url"] = url
            return (200, b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>')

        arxiv_search("ti:volatility", max_results=5, start=10, transport=spy, now=lambda: FIXED_NOW)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(captured["url"]).query)
        self.assertEqual(q["search_query"], ["ti:volatility"])
        self.assertEqual(q["start"], ["10"])
        self.assertEqual(q["max_results"], ["5"])
        self.assertEqual(q["sortBy"], ["submittedDate"])
        self.assertEqual(q["sortOrder"], ["descending"])

    def test_s2_happy(self):
        res = semantic_scholar_search("options", limit=1, transport=_ok(_S2_FIXTURE), now=lambda: FIXED_NOW)
        assert res.provider_id == "semantic-scholar"
        row = res.rows[0]
        assert row["title"] == "Paper A"
        assert row["abstract"] == "Abstract A."
        assert row["year"] == 2024
        assert row["url"] == "https://example.com/a"
        assert row["authors"] == ["Jane Roe"]

    def test_s2_rate_limit_fails_closed(self):
        with _no_sleep():
            try:
                semantic_scholar_search("options", transport=lambda u: (429, _S2_429_FIXTURE), now=lambda: FIXED_NOW)
            except ValueError as exc:
                assert "data unavailable" in str(exc)
                return
        raise AssertionError("expected ValueError on S2 429")

    def test_s2_malformed(self):
        _expect_value_error(
            semantic_scholar_search, "options", transport=_ok(b'{"data": "nope"}'), now=lambda: FIXED_NOW
        )

    def test_s2_empty_query(self):
        _expect_value_error(semantic_scholar_search, "  ", transport=_ok(_S2_FIXTURE))

    def test_s2_empty_fields(self):
        _expect_value_error(
            semantic_scholar_search, "x", fields=["  ", ""], transport=_ok(_S2_FIXTURE)
        )

    def test_s2_limit_validation(self):
        _expect_value_error(
            semantic_scholar_search, "x", limit=0, transport=_ok(_S2_FIXTURE)
        )
        _expect_value_error(
            semantic_scholar_search, "x", limit=101, transport=_ok(_S2_FIXTURE)
        )

    def test_s2_paper_not_object(self):
        _expect_value_error(
            semantic_scholar_search,
            "x",
            transport=_ok(b'{"data":[42]}'),
            now=lambda: FIXED_NOW,
        )

    def test_s2_authors_not_list(self):
        res = semantic_scholar_search(
            "x",
            transport=_ok(b'{"data":[{"title":"T","authors":"nobody"}]}'),
            now=lambda: FIXED_NOW,
        )
        self.assertEqual(res.rows[0]["authors"], [])

    def test_s2_missing_optional_fields(self):
        res = semantic_scholar_search(
            "x", transport=_ok(b'{"data":[{}]}'), now=lambda: FIXED_NOW
        )
        row = res.rows[0]
        self.assertEqual(row["title"], "")
        self.assertEqual(row["abstract"], "")
        self.assertIsNone(row["year"])
        self.assertEqual(row["url"], "")
        self.assertEqual(row["authors"], [])
        self.assertEqual(row["source"], "semantic-scholar")

    def test_s2_payload_not_object(self):
        _expect_value_error(
            semantic_scholar_search, "x", transport=_ok(b"[1,2]"), now=lambda: FIXED_NOW
        )

    def test_s2_rate_limit_message_in_error_body(self):
        with _no_sleep():
            try:
                semantic_scholar_search(
                    "x", transport=lambda u: (403, b"Too Many Requests"), now=lambda: FIXED_NOW
                )
            except ValueError as exc:
                self.assertIn("data unavailable", str(exc))
                return
        raise AssertionError("expected ValueError")

    def test_s2_server_error_reraises(self):
        with _no_sleep():
            try:
                semantic_scholar_search(
                    "x", transport=lambda u: (500, b"boom"), now=lambda: FIXED_NOW
                )
            except ValueError as exc:
                self.assertNotIn("data unavailable", str(exc))
                self.assertIn("status 500", str(exc))
                return
        raise AssertionError("expected ValueError")

    def test_s2_query_params(self):
        captured = {}

        def spy(url):
            captured["url"] = url
            return (200, b'{"data":[]}')

        res = semantic_scholar_search(
            "quantum", limit=3, fields=["title", "year"], transport=spy, now=lambda: FIXED_NOW
        )
        q = urllib.parse.parse_qs(urllib.parse.urlparse(captured["url"]).query)
        self.assertEqual(q["query"], ["quantum"])
        self.assertEqual(q["limit"], ["3"])
        self.assertEqual(q["fields"], ["title,year"])
        self.assertEqual(res.rows, ())


class EventWireTests(unittest.TestCase):
    def _pacer(self):
        state, clock = _fake_clock()
        return GdeltPacer(clock=clock, sleeper=lambda s: None)

    def test_gdelt_happy(self):
        state, clock = _fake_clock()
        sleeps = []
        pacer = GdeltPacer(clock=clock, sleeper=sleeps.append)
        res = gdelt_artlist(
            "FEDERAL RESERVE",
            maxrecords=1,
            transport=_ok(_GDELT_FIXTURE),
            pacer=pacer,
            now=lambda: FIXED_NOW,
        )
        assert res.provider_id == "gdelt"
        row = res.rows[0]
        assert row["title"] == "Fed holds rates"
        assert row["domain"] == "example.com"
        assert row["sourcecountry"] == "United States"
        assert sleeps == [], "first call must not sleep"

    def test_gdelt_pacing_enforced(self):
        state, clock = _fake_clock()
        sleeps = []
        pacer = GdeltPacer(clock=clock, sleeper=sleeps.append)
        pacer.wait()
        state["t"] += 2.0  # only 2s elapsed
        pacer.wait()
        assert len(sleeps) == 1
        assert abs(sleeps[0] - 4.0) < 1e-9, f"expected 4.0s pace sleep, got {sleeps[0]}"
        # after full gap, no sleep
        state["t"] += 10.0
        pacer.wait()
        assert len(sleeps) == 1

    def test_gdelt_rate_limit_notice_fails_closed(self):
        pacer = self._pacer()
        try:
            gdelt_artlist(
                "FEDERAL RESERVE",
                transport=_ok(_GDELT_NOTICE),
                pacer=pacer,
                now=lambda: FIXED_NOW,
            )
        except ValueError as exc:
            assert "data unavailable" in str(exc)
            return
        raise AssertionError("expected ValueError on GDELT rate-limit notice")

    def test_gdelt_malformed(self):
        pacer = self._pacer()
        _expect_value_error(
            gdelt_artlist,
            "FEDERAL RESERVE",
            transport=_ok(b'{"articles": "nope"}'),
            pacer=pacer,
            now=lambda: FIXED_NOW,
        )

    def test_gdelt_empty_query(self):
        _expect_value_error(gdelt_artlist, "  ", transport=_ok(_GDELT_FIXTURE))

    def test_gdelt_maxrecords_validation(self):
        pacer = self._pacer()
        _expect_value_error(
            gdelt_artlist, "x", maxrecords=0, transport=_ok(_GDELT_FIXTURE), pacer=pacer
        )
        _expect_value_error(
            gdelt_artlist, "x", maxrecords=251, transport=_ok(_GDELT_FIXTURE), pacer=pacer
        )
        _expect_value_error(
            gdelt_artlist, "x", maxrecords="25", transport=_ok(_GDELT_FIXTURE), pacer=pacer
        )

    def test_gdelt_uses_default_pacer_when_none(self):
        saved_calls, saved_last = (
            event_wire._default_pacer._calls_made,
            event_wire._default_pacer._last_call,
        )
        event_wire._default_pacer._calls_made = 0
        try:
            res = gdelt_artlist(
                "x", transport=_ok(_GDELT_FIXTURE), pacer=None, now=lambda: FIXED_NOW
            )
            self.assertEqual(res.provider_id, "gdelt")
        finally:
            event_wire._default_pacer._calls_made = saved_calls
            event_wire._default_pacer._last_call = saved_last

    def test_gdelt_fetch_error_carrying_rate_limit_marker(self):
        pacer = self._pacer()
        with _no_sleep():
            try:
                gdelt_artlist(
                    "x",
                    transport=lambda u: (429, _GDELT_NOTICE),
                    pacer=pacer,
                    now=lambda: FIXED_NOW,
                )
            except ValueError as exc:
                self.assertIn("data unavailable", str(exc))
                return
        raise AssertionError("expected ValueError")

    def test_gdelt_fetch_error_without_marker_reraises(self):
        pacer = self._pacer()
        with _no_sleep():
            try:
                gdelt_artlist(
                    "x", transport=lambda u: (500, b"boom"), pacer=pacer, now=lambda: FIXED_NOW
                )
            except ValueError as exc:
                self.assertNotIn("data unavailable", str(exc))
                self.assertIn("status 500", str(exc))
                return
        raise AssertionError("expected ValueError")

    def test_gdelt_payload_not_object(self):
        pacer = self._pacer()
        _expect_value_error(
            gdelt_artlist, "x", transport=_ok(b"[1]"), pacer=pacer, now=lambda: FIXED_NOW
        )

    def test_gdelt_no_articles_list(self):
        pacer = self._pacer()
        _expect_value_error(
            gdelt_artlist,
            "x",
            transport=_ok(b'{"articles": {}}'),
            pacer=pacer,
            now=lambda: FIXED_NOW,
        )

    def test_gdelt_article_not_object(self):
        pacer = self._pacer()
        _expect_value_error(
            gdelt_artlist,
            "x",
            transport=_ok(b'{"articles": [7]}'),
            pacer=pacer,
            now=lambda: FIXED_NOW,
        )

    def test_gdelt_empty_articles(self):
        pacer = self._pacer()
        res = gdelt_artlist(
            "x", transport=_ok(b'{"articles": []}'), pacer=pacer, now=lambda: FIXED_NOW
        )
        self.assertEqual(res.rows, ())
        self.assertEqual(res.dataset, "doc-artlist")

    def test_gdelt_query_params(self):
        captured = {}

        def spy(url):
            captured["url"] = url
            return (200, b'{"articles": []}')

        pacer = self._pacer()
        gdelt_artlist(
            "FEDERAL RESERVE", maxrecords=7, transport=spy, pacer=pacer, now=lambda: FIXED_NOW
        )
        q = urllib.parse.parse_qs(urllib.parse.urlparse(captured["url"]).query)
        self.assertEqual(q["query"], ["FEDERAL RESERVE"])
        self.assertEqual(q["mode"], ["artlist"])
        self.assertEqual(q["maxrecords"], ["7"])
        self.assertEqual(q["format"], ["json"])

    def test_pacer_negative_gap_rejected(self):
        with self.assertRaises(ValueError):
            GdeltPacer(min_gap=-1.0)

    def test_pacer_default_gap(self):
        self.assertEqual(GdeltPacer()._min_gap, GDELT_MIN_PACING_SECONDS)

    def test_pacer_zero_gap_ok(self):
        p = GdeltPacer(min_gap=0.0)
        self.assertEqual(p._min_gap, 0.0)


class SecFtsTests(unittest.TestCase):
    def test_sec_fts_happy(self):
        # Request shape verified live 2026-10-04: GET with q/forms/startdt params.
        # Response fixture follows the documented elastic-style hits shape.
        res = sec_fulltext_search(
            '"stock repurchase"',
            forms=["10-Q"],
            startdt="2026-01-01",
            transport=_ok(_FTS_FIXTURE),
            now=lambda: FIXED_NOW,
        )
        assert res.provider_id == "sec-fts"
        row = res.rows[0]
        assert row["form"] == "8-K"
        assert row["company"] == "ACME Corp"
        assert row["file_date"] == "2026-09-30"
        assert row["accession"] == "0001234567-26-000001"

    def test_sec_fts_request_shape_verified(self):
        # Pins the verified-live request shape: GET with q/forms/startdt params.
        captured = {}

        def spy(url: str):
            captured["url"] = url
            return (200, b'{"hits": {"hits": []}}')

        res = sec_fulltext_search(
            '"stock repurchase"',
            forms=["10-Q"],
            startdt="2026-01-01",
            transport=spy,
            now=lambda: FIXED_NOW,
        )
        url = captured["url"]
        assert url.startswith("https://efts.sec.gov/LATEST/search-index?"), url
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        assert query["q"] == ['"stock repurchase"'], query
        assert query["forms"] == ["10-Q"], query
        assert query["startdt"] == ["2026-01-01"], query
        assert res.rows == ()

    def test_sec_fts_bad_date(self):
        _expect_value_error(
            sec_fulltext_search,
            "x",
            startdt="2026-13-99",
            transport=_ok(_FTS_FIXTURE),
        )

    def test_sec_fts_transport_error(self):
        _expect_value_error(
            sec_fulltext_search, "x", transport=lambda u: (403, b"denied")
        )

    def test_sec_fts_malformed(self):
        _expect_value_error(
            sec_fulltext_search, "x", transport=_ok(b'{"hits": "nope"}')
        )

    def test_sec_fts_empty_query(self):
        _expect_value_error(sec_fulltext_search, "   ", transport=_ok(_FTS_FIXTURE))

    def test_sec_fts_no_forms(self):
        _expect_value_error(
            sec_fulltext_search, "x", forms=[], transport=_ok(_FTS_FIXTURE)
        )
        _expect_value_error(
            sec_fulltext_search, "x", forms=["  ", ""], transport=_ok(_FTS_FIXTURE)
        )

    def test_sec_fts_enddt(self):
        _expect_value_error(
            sec_fulltext_search, "x", enddt="yesterday", transport=_ok(_FTS_FIXTURE)
        )
        captured = {}

        def spy(url: str):
            captured["url"] = url
            return (200, b'{"hits": {"hits": []}}')

        res = sec_fulltext_search(
            "x", enddt="2026-10-01", transport=spy, now=lambda: FIXED_NOW
        )
        q = urllib.parse.parse_qs(urllib.parse.urlparse(captured["url"]).query)
        self.assertEqual(q["enddt"], ["2026-10-01"])
        self.assertNotIn("startdt", q)
        self.assertEqual(res.rows, ())

    def test_sec_fts_hits_as_bare_list(self):
        payload = b'{"hits": [{"form": "10-K", "c_name": "Foo"}]}'
        res = sec_fulltext_search("x", transport=_ok(payload), now=lambda: FIXED_NOW)
        self.assertEqual(res.rows[0]["form"], "10-K")
        self.assertEqual(res.rows[0]["company"], "Foo")

    def test_sec_fts_payload_not_object(self):
        _expect_value_error(sec_fulltext_search, "x", transport=_ok(b"[1]"))

    def test_sec_fts_hit_not_object(self):
        _expect_value_error(
            sec_fulltext_search, "x", transport=_ok(b'{"hits": {"hits": [9]}}')
        )

    def test_sec_fts_hit_without_source_uses_hit(self):
        payload = b'{"hits": {"hits": [{"form": "S-1", "c_name": "Bar Inc"}]}}'
        res = sec_fulltext_search("x", transport=_ok(payload), now=lambda: FIXED_NOW)
        self.assertEqual(res.rows[0]["company"], "Bar Inc")
        self.assertEqual(res.rows[0]["form"], "S-1")

    def test_sec_fts_alternate_field_names(self):
        payload = (
            b'{"hits": {"hits": [{"_source": {'
            b'"form": "10-Q", "companyName": "Alt Co", "cik": "0009999999",'
            b'"filedAt": "2026-08-15", "accessionNumber": "0009999999-26-000009",'
            b'"title": "Quarterly"}}]}}'
        )
        res = sec_fulltext_search("x", transport=_ok(payload), now=lambda: FIXED_NOW)
        row = res.rows[0]
        self.assertEqual(row["company"], "Alt Co")
        self.assertEqual(row["cik"], "0009999999")
        self.assertEqual(row["file_date"], "2026-08-15")
        self.assertEqual(row["accession"], "0009999999-26-000009")
        self.assertEqual(row["raw"]["companyName"], "Alt Co")

    def test_sec_fts_empty_hits(self):
        res = sec_fulltext_search(
            "x", transport=_ok(b'{"hits": {"hits": []}}'), now=lambda: FIXED_NOW
        )
        self.assertEqual(res.rows, ())

    def test_sec_fts_default_forms_in_request(self):
        captured = {}

        def spy(url: str):
            captured["url"] = url
            return (200, b'{"hits": {"hits": []}}')

        sec_fulltext_search("x", transport=spy, now=lambda: FIXED_NOW)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(captured["url"]).query)
        self.assertIn("10-K", q["forms"][0])
        self.assertIn("DEF 14A", q["forms"][0])


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(
        f"\n{result.testsRun} run, "
        f"{len(result.failures)} failed, {len(result.errors)} errors"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
