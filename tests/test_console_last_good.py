import json

from hedge_desk import server


def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("HEDGE_DESK_STATE_DIR", str(tmp_path))


def test_stale_payload_is_labelled_and_never_authorizes(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    server.save_last_good_console({"schema_version": "desk-console-1", "report": {}}, now=1_000.0)
    got = server.load_last_good_console("upstream 503", now=1_000.0 + 7200)
    assert got["freshness"]["status"] == "STALE"
    assert got["freshness"]["age_seconds"] == 7200
    assert got["freshness"]["trade_authorized"] is False
    assert "upstream 503" in got["freshness"]["live_error"]


def test_too_old_or_missing_fails_closed(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    assert server.load_last_good_console("x", now=1.0) is None
    server.save_last_good_console({"a": 1}, now=0.0)
    assert server.load_last_good_console("x", now=server.LAST_GOOD_MAX_AGE_SECONDS + 1.0) is None


def test_route_serves_stale_on_live_failure(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    import time
    server.save_last_good_console({"schema_version": "desk-console-1", "report": {}}, now=time.time() - 60)

    def boom():
        raise RuntimeError("data unavailable: quotes down")

    monkeypatch.setattr(server, "build_live_console_payload", boom)
    server._api_cache.pop("console-report", None)
    captured = {}
    body = b"".join(server.application({"PATH_INFO": "/api/report", "REQUEST_METHOD": "GET"},
                                       lambda s, h: captured.update(status=s)))
    assert captured["status"].startswith("200")
    assert json.loads(body)["freshness"]["status"] == "STALE"


def test_route_503_without_last_good(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    monkeypatch.setattr(server, "build_live_console_payload",
                        lambda: (_ for _ in ()).throw(RuntimeError("down")))
    server._api_cache.pop("console-report", None)
    captured = {}
    b"".join(server.application({"PATH_INFO": "/api/report", "REQUEST_METHOD": "GET"},
                                lambda s, h: captured.update(status=s)))
    assert captured["status"].startswith("503")


def test_options_seed_freshness_against_weekly_sla():
    from datetime import datetime, timedelta, timezone

    now = datetime(2026, 11, 19, tzinfo=timezone.utc)
    fresh = server.options_seed_freshness({"as_of": (now - timedelta(days=3)).isoformat()}, now)
    assert fresh["status"] == "CURRENT" and fresh["age_seconds"] == 3 * 86400
    old = server.options_seed_freshness({"as_of": (now - timedelta(days=9)).isoformat()}, now)
    assert old["is_stale"]
    failed = server.options_seed_freshness(
        {"as_of": now.isoformat(), "refresh": {"status": "fetch_failed"}}, now)
    assert failed["is_stale"]
    assert server.options_seed_freshness({}, now)["status"] == "UNKNOWN"
