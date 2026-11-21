"""Deterministic tests for honest data health (no network, fixed clocks).

Incident 2026-11-19: the nightly batch was REJECTED and every Cboe fetch
returned 403, yet /api/health said "ok" and data quality said "Options/Cboe
present". These tests pin the fix: liveness stays "ok" for the Render probe,
and data health reports RED with named sources.
"""

import json
from datetime import datetime, timedelta, timezone

import pytest

from hedge_desk import server as server_mod
from hedge_desk.data_health import AMBER, GREEN, RED, build_data_health
from hedge_desk.data_quality import SEV_DOWN, SEV_OK, quality_report

NOW = datetime(2026, 11, 20, 16, 0, tzinfo=timezone.utc)


def _healthy_report(generated=NOW - timedelta(hours=11)):
    return {
        "generated_at": generated.isoformat(),
        "macro_environment": {"mode": "REAL_FRED_MACRO", "as_of": "2026-11-20"},
        "rates_environment": {"mode": "REAL_FRED_RATES", "as_of": "2026-11-20"},
        "data_freshness": {"as_of": "2026-11-19", "expected_trading_day": "2026-11-19", "is_current": True},
        "eod_batch_status": "READY_FOR_RESEARCH",
        "eod_source_results": [{"symbol": "F", "status": "PASS", "reason_codes": []}],
        "oil_market": {"mode": "REAL_YAHOO_WTI"},
        "earnings_actuals": {"0000320193": {"mode": "REAL_EDGAR_EARNINGS"}},
        "chain_income": {"SPY": {"mode": "REAL_CBOE_CHAIN_INCOME"}},
        "cash_secured_put_scan": {"F": {"mode": "REAL_CBOE_CSP", "candidate": {"found": True}}},
        "market_context": {"sources": {"fred": {"status": "LIVE"}, "bls": {"status": "LIVE"}}},
    }


def _incident_report():
    """Shape of the real 2026-11-19 nightly that slipped past as 'ok'."""
    r = _healthy_report()
    r["eod_batch_status"] = "REJECTED"
    r["eod_source_results"] = [
        {"symbol": "F", "status": "PASS", "reason_codes": []},
        {"symbol": "LYFT", "status": "QUARANTINE", "reason_codes": ["TRANSPORT_FAILED"]},
    ]
    r["chain_income"] = {"SPY": {"mode": "BLOCKED", "reason": "cboe fetch failed (status 403)"}}
    r["cash_secured_put_scan"] = {
        "F": {"mode": "BLOCKED", "symbol": "F", "reason": "cboe_fetch_403"},
        "LYFT": {"mode": "BLOCKED", "symbol": "LYFT", "reason": "cboe_fetch_403"},
    }
    return r


# --- data_quality: the false OK ------------------------------------------------

def test_quality_flags_per_symbol_blocked_chain_as_down_not_present():
    q = quality_report(_incident_report())
    by_source = {a["source"]: a for a in q["alerts"]}
    assert by_source["Options/Cboe"]["severity"] == SEV_DOWN
    assert "SPY" in by_source["Options/Cboe"]["detail"]
    assert "403" in by_source["Options/Cboe"]["detail"]
    assert by_source["Options/CSP scan"]["severity"] == SEV_DOWN
    assert "2 of 2" in by_source["Options/CSP scan"]["message"]


def test_quality_names_quarantined_eod_symbols():
    q = quality_report(_incident_report())
    eod = {a["source"]: a for a in q["alerts"]}["EOD"]
    assert eod["severity"] == SEV_DOWN
    assert "LYFT(TRANSPORT_FAILED)" in eod["detail"]


def test_quality_per_symbol_all_live_is_ok():
    q = quality_report(_healthy_report())
    assert q["overall"] == SEV_OK, q["summary"]


# --- data_health ---------------------------------------------------------------

def test_healthy_report_is_green():
    h = build_data_health(_healthy_report(), NOW)
    assert h["status"] == GREEN
    assert h["reasons"] == []
    assert h["trade_authorized"] is False


def test_incident_report_is_red_with_named_sources():
    h = build_data_health(_incident_report(), NOW)
    assert h["status"] == RED
    for reason in ("EOD=DOWN", "Options/Cboe=DOWN", "Options/CSP scan=DOWN"):
        assert reason in h["reasons"]
    assert "Options/Cboe" in h["summary"]


def test_missing_artifact_is_red_not_ok():
    h = build_data_health(None, NOW)
    assert h["status"] == RED
    assert h["reasons"] == ["ARTIFACT_MISSING"]


def test_stale_artifact_is_red():
    h = build_data_health(_healthy_report(generated=NOW - timedelta(hours=37)), NOW)
    assert h["status"] == RED
    assert "ARTIFACT_STALE" in h["reasons"]


def test_artifact_within_36_hours_is_not_stale():
    h = build_data_health(_healthy_report(generated=NOW - timedelta(hours=35)), NOW)
    assert "ARTIFACT_STALE" not in h["reasons"]


def test_invalid_timestamp_is_red():
    r = _healthy_report()
    r["generated_at"] = "not-a-time"
    assert build_data_health(r, NOW)["status"] == RED


def test_blocked_context_feed_is_amber_not_green():
    r = _healthy_report()
    r["market_context"]["sources"]["imf"] = {"status": "BLOCKED"}
    h = build_data_health(r, NOW)
    assert h["status"] == AMBER
    assert "MARKET_CONTEXT_PARTIAL" in h["reasons"]


def test_naive_clock_rejected():
    with pytest.raises(ValueError):
        build_data_health(_healthy_report(), datetime(2026, 11, 20, 16, 0))


# --- server: liveness stays ok, data health is honest ------------------------

def _get(path):
    captured = {}

    def start(status, headers):
        captured["status"] = status

    body = b"".join(server_mod.application({"PATH_INFO": path}, start))
    return captured["status"], json.loads(body)


@pytest.fixture
def incident_artifacts(tmp_path, monkeypatch):
    (tmp_path / "am-report-latest.json").write_text(json.dumps(_incident_report()), encoding="utf-8")
    monkeypatch.setattr(server_mod, "ARTIFACTS", tmp_path)
    server_mod._api_cache.clear()
    yield tmp_path
    server_mod._api_cache.clear()


def test_api_health_liveness_ok_but_data_health_red(incident_artifacts):
    status, body = _get("/api/health")
    assert status == "200 OK"  # Render liveness probe keeps passing
    assert body["status"] == "ok"
    assert body["mode"] == "paper"
    assert body["live_orders_enabled"] is False
    assert body["data_health"]["status"] == RED
    assert "Options/Cboe=DOWN" in body["data_health"]["reasons"]


def test_api_health_data_endpoint_lists_components(incident_artifacts):
    status, body = _get("/api/health/data")
    assert status == "200 OK"
    sources = {c["source"]: c["status"] for c in body["components"]}
    assert sources["Options/Cboe"] == RED
    assert sources["EOD"] == RED
    assert body["trade_authorized"] is False


def test_api_health_never_fails_when_scoring_breaks(incident_artifacts, monkeypatch):
    import hedge_desk.data_health as dh

    def boom(*_a, **_k):
        raise RuntimeError("scoring bug")

    monkeypatch.setattr(dh, "build_data_health", boom)
    status, body = _get("/api/health")
    assert status == "200 OK"
    assert body["status"] == "ok"
    assert body["data_health"]["status"] == RED
    assert body["data_health"]["reasons"] == ["HEALTH_EVALUATION_FAILED"]
