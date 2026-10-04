"""Deterministic tests for the keyless data-integration modules.

No live network: every test injects a fixture transport. Clocks are fixed.
Run: python3 tests/test_data_integrations.py (from the data-integrations dir)
"""

import sys
import os
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hedge_desk.data.feed_base import FeedResult  # noqa: F401
from hedge_desk.data.nasdaq_calendars import nasdaq_dividends_calendar, nasdaq_splits_calendar
from hedge_desk.data.research_lit import arxiv_search, semantic_scholar_search
from hedge_desk.data.event_wire import GdeltPacer, gdelt_artlist
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


def test_nasdaq_dividends_happy():
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


def test_nasdaq_splits_happy():
    res = nasdaq_splits_calendar(
        "2026-10-04", transport=_ok(_SPLITS_FIXTURE), now=lambda: FIXED_NOW
    )
    assert res.dataset == "splits-calendar"
    row = res.rows[0]
    assert row["symbol"] == "LU"
    assert row["ratio"] == "1 : 10"
    assert row["executionDate_iso"] == "2026-10-23"


def test_nasdaq_bad_date():
    _expect_value_error(nasdaq_dividends_calendar, "not-a-date", transport=_ok(b"{}"))


def test_nasdaq_malformed_payload():
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


def test_nasdaq_transport_error():
    _expect_value_error(
        nasdaq_dividends_calendar, "2026-10-02", transport=_boom, now=lambda: FIXED_NOW
    )


def test_arxiv_happy():
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


def test_arxiv_malformed_xml():
    _expect_value_error(arxiv_search, "all:option", transport=_ok(b"<broken"), now=lambda: FIXED_NOW)


def test_arxiv_transport_error():
    _expect_value_error(arxiv_search, "all:option", transport=_boom, now=lambda: FIXED_NOW)


def test_arxiv_empty_query():
    _expect_value_error(arxiv_search, "  ", transport=_ok(_ARXIV_FIXTURE))


def test_s2_happy():
    res = semantic_scholar_search("options", limit=1, transport=_ok(_S2_FIXTURE), now=lambda: FIXED_NOW)
    assert res.provider_id == "semantic-scholar"
    row = res.rows[0]
    assert row["title"] == "Paper A"
    assert row["abstract"] == "Abstract A."
    assert row["year"] == 2024
    assert row["url"] == "https://example.com/a"
    assert row["authors"] == ["Jane Roe"]


def test_s2_rate_limit_fails_closed():
    try:
        semantic_scholar_search("options", transport=lambda u: (429, _S2_429_FIXTURE), now=lambda: FIXED_NOW)
    except ValueError as exc:
        assert "data unavailable" in str(exc)
        return
    raise AssertionError("expected ValueError on S2 429")


def test_s2_malformed():
    _expect_value_error(
        semantic_scholar_search, "options", transport=_ok(b'{"data": "nope"}'), now=lambda: FIXED_NOW
    )


def _fake_clock(start=1000.0):
    state = {"t": start}
    return state, lambda: state["t"]


def test_gdelt_happy():
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


def test_gdelt_pacing_enforced():
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


def test_gdelt_rate_limit_notice_fails_closed():
    state, clock = _fake_clock()
    pacer = GdeltPacer(clock=clock, sleeper=lambda s: None)
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


def test_gdelt_malformed():
    state, clock = _fake_clock()
    pacer = GdeltPacer(clock=clock, sleeper=lambda s: None)
    _expect_value_error(
        gdelt_artlist,
        "FEDERAL RESERVE",
        transport=_ok(b'{"articles": "nope"}'),
        pacer=pacer,
        now=lambda: FIXED_NOW,
    )


def test_sec_fts_happy():
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


def test_sec_fts_request_shape_verified():
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


def test_sec_fts_bad_date():
    _expect_value_error(
        sec_fulltext_search,
        "x",
        startdt="2026-13-99",
        transport=_ok(_FTS_FIXTURE),
    )


def test_sec_fts_transport_error():
    _expect_value_error(
        sec_fulltext_search, "x", transport=lambda u: (403, b"denied")
    )


def test_sec_fts_malformed():
    _expect_value_error(
        sec_fulltext_search, "x", transport=_ok(b'{"hits": "nope"}')
    )


def main() -> int:
    tests = sorted(
        (name, fn)
        for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    passed, failed = 0, 0
    for name, fn in tests:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - report, don't stop
            failed += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
        else:
            passed += 1
            print(f"PASS {name}")
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
