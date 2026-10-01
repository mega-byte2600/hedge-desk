"""Tests for the Emporion options workbench data layer.

Deterministic: fixed clocks, hand-built seed fixture (faithful to the real
artifacts/options-seed-latest.json shape), no network. Endpoint tests call the
WSGI application directly with ARTIFACTS pointed at a tmp dir.

UI contract pinned here (for the web/ workbench port):
  * /api/options-seed -> 200 + application/json when the artifact exists;
    404 + {"error": "artifact_missing"} when it does not (fails closed, so the
    UI can always distinguish missing from present).
  * data_mode is one of live/batch/scenario; the seed is always "batch".
  * freshness: "fresh" within 8 days of now, else "stale". The UI shows
    "batch · <date> — stale, refresh pending" when stale.
  * validation rejects days_to_expiration > 30 with reason
    seed_dte_out_of_workbench_scope; the UI shows "data unavailable —
    contract DTE {n} exceeds the 30-day workbench limit".
  * no greek may be zero-filled or silently null; unavailable analytics are
    null AND declared in unavailable_fields with a reason.
"""

import io
import json
import re
import tokenize
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from hedge_desk import options_seed as seed_mod
from hedge_desk import server as server_mod
from hedge_desk.options_seed import (
    DATA_MODE,
    DATA_MODES,
    SEED_SCHEMA_VERSION,
    seed_freshness,
    seed_to_dict,
    validate_seed_dict,
)

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)  # fixed clock
AS_OF = datetime(2026, 10, 1, 1, 12, 10, tzinfo=timezone.utc)  # real seed clock


def _seed_fixture(**overrides):
    """Hand-built fixture in the exact shape of the real seed (SPY 2026-10-30
    749 put, DTE 29 — values mirror the real artifact, this is not live data)."""
    d = {
        "schema_version": SEED_SCHEMA_VERSION,
        "mode": "REAL_CBOE_DELAYED_SEED",
        "symbol": "SPY",
        "contract_id": "SPY261030P00749000",
        "option_type": "PUT",
        "strike": "749",
        "expiration": "2026-10-30",
        "days_to_expiration": 29,
        "bid": "6.45",
        "ask": "6.52",
        "mid": "6.485",
        "implied_volatility": "0.1526",
        "delta": "-0.3022",
        "gamma": "0.0106",
        "theta": "-0.198",
        "vega": "0.7685",
        "rho": "-0.1703",
        "unavailable_fields": [],
        "open_interest": 859,
        "volume": 309,
        "underlying_bid": "758.90",
        "underlying_ask": "759.00",
        "underlying_price": "758.95",
        "as_of": "2026-10-01T01:12:10+00:00",
        "source": "cboe-delayed",
        "data_mode": "batch",
        "refresh": {"status": "ok",
                   "refreshed_at": "2026-10-01T01:12:10+00:00", "reason": None},
        "trade_authorized": False,
    }
    d.update(overrides)
    return d


def _get(path):
    captured = {}

    def start(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(server_mod.application({"PATH_INFO": path}, start))
    return captured["status"], captured["headers"], body


# 1. Seed loading ------------------------------------------------------------

def test_options_seed_endpoint_serves_artifact_as_json(tmp_path, monkeypatch):
    (tmp_path / "options-seed-latest.json").write_text(
        json.dumps(_seed_fixture()), encoding="utf-8")
    monkeypatch.setattr(server_mod, "ARTIFACTS", tmp_path)

    status, headers, body = _get("/api/options-seed")
    assert status == "200 OK"
    assert headers["Content-Type"] == "application/json"
    d = json.loads(body)
    assert d["schema_version"] == "hedge-desk-options-seed-1.0.0"
    for f in ("contract_id", "strike", "expiration", "bid", "ask", "mid",
              "implied_volatility", "as_of", "source", "data_mode"):
        assert d.get(f), f  # present and non-empty
    assert d["days_to_expiration"] <= 30
    for g in ("delta", "gamma", "theta", "vega", "rho"):
        assert g in d, g  # greeks present in the payload
    assert d["trade_authorized"] is False


# 2. Missing seed -------------------------------------------------------------

def test_options_seed_endpoint_missing_artifact_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(server_mod, "ARTIFACTS", tmp_path)  # no seed file

    status, headers, body = _get("/api/options-seed")
    assert status == "404 Not Found"
    assert headers["Content-Type"] == "application/json"
    d = json.loads(body)  # JSON error body, not an HTML page:
    assert d["error"] == "artifact_missing"  # -> the UI can distinguish
    assert d["path"] == "options-seed-latest.json"  # missing from present


# 3. Stale seed ---------------------------------------------------------------

def test_seed_freshness_within_8_days_is_fresh():
    assert seed_freshness(NOW - timedelta(days=7), NOW) == "fresh"
    assert seed_freshness(NOW - timedelta(days=8), NOW) == "fresh"  # boundary


def test_seed_freshness_older_than_8_days_is_stale():
    assert seed_freshness(NOW - timedelta(days=9), NOW) == "stale"
    assert seed_freshness(AS_OF - timedelta(days=30), NOW) == "stale"


def test_seed_freshness_future_as_of_is_fresh():
    assert seed_freshness(NOW + timedelta(hours=1), NOW) == "fresh"


def test_seed_freshness_rejects_naive_clock():
    with pytest.raises(ValueError, match="timezone-aware"):
        seed_freshness(datetime(2026, 9, 20, 12, 0), NOW)
    with pytest.raises(ValueError, match="timezone-aware"):
        seed_freshness(NOW - timedelta(days=1), datetime(2026, 10, 1, 12, 0))


def test_stale_seed_label_inputs_the_ui_needs():
    # The UI shows "batch · <date> — stale, refresh pending": both inputs it
    # composes are pinned — the seed's data_mode and its freshness.
    d = _seed_fixture()
    assert d["data_mode"] == "batch"
    assert seed_freshness(datetime.fromisoformat(d["as_of"]),
                          datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
                          ) == "stale"


# 4. Data-mode labeling -------------------------------------------------------

def test_seed_payload_carries_batch_data_mode():
    seed = seed_mod.SeedContract(
        contract_id="SPY261030P00749000", strike=Decimal("749"),
        expiration=date(2026, 10, 30), dte=29,
        bid=Decimal("6.45"), ask=Decimal("6.52"), mid=Decimal("6.485"),
        iv=Decimal("0.1526"), delta=Decimal("-0.3022"),
        gamma=Decimal("0.0106"), theta=Decimal("-0.198"),
        vega=Decimal("0.7685"), rho=Decimal("-0.1703"),
        unavailable=(), open_interest=859, volume=309,
    )
    d = seed_to_dict(seed, "SPY",
                     {"bid": 758.90, "ask": 759.00, "current_price": 758.95},
                     AS_OF, {"status": "ok", "refreshed_at": AS_OF.isoformat(),
                             "reason": None})
    assert d["data_mode"] == "batch"
    assert d["data_mode"] == DATA_MODE
    validate_seed_dict(d)  # real pipeline output always validates


def test_data_mode_contract_lists_live_batch_scenario():
    # UI contract: live (reserved real-time), batch (this weekly seed),
    # scenario (user-driven hypothetical from real base data — never market data).
    assert set(DATA_MODES) == {"live", "batch", "scenario"}
    assert DATA_MODE == "batch"


def test_validate_seed_dict_rejects_unknown_data_mode():
    with pytest.raises(ValueError, match="seed_unknown_data_mode"):
        validate_seed_dict(_seed_fixture(data_mode="realtime"))


# 5. No-synthetic-data guard ---------------------------------------------------

def test_real_seed_artifact_validates_clean():
    # Scans the workbench-relevant seed path itself: the committed artifact
    # must pass validation (no placeholder/zero-filled greeks).
    path = Path(seed_mod.__file__).resolve().parents[1] / "artifacts" / "options-seed-latest.json"
    assert path.is_file()  # tracked in git; never absent on this branch
    validate_seed_dict(json.loads(path.read_text(encoding="utf-8")))


def test_validate_seed_dict_rejects_null_iv_without_unavailable_entry():
    with pytest.raises(ValueError, match="seed_null_or_zero_iv"):
        validate_seed_dict(_seed_fixture(implied_volatility=None))


def test_validate_seed_dict_rejects_zero_bid_or_ask():
    with pytest.raises(ValueError, match="seed_unexecutable_quote"):
        validate_seed_dict(_seed_fixture(bid="0.00"))
    with pytest.raises(ValueError, match="seed_unexecutable_quote"):
        validate_seed_dict(_seed_fixture(ask="0.00"))


def test_validate_seed_dict_rejects_zero_filled_greek():
    # A greek of exactly 0.0 is the source's placeholder for "not computed".
    with pytest.raises(ValueError, match=r"seed_zero_filled_greek:gamma"):
        validate_seed_dict(_seed_fixture(gamma="0.00"))


def test_validate_seed_dict_rejects_undeclared_unavailable_greek():
    with pytest.raises(ValueError,
                       match=r"seed_undeclared_unavailable_greek:gamma"):
        validate_seed_dict(_seed_fixture(gamma=None))


def test_validate_seed_dict_accepts_declared_unavailable_greek():
    d = _seed_fixture(
        gamma=None,
        unavailable_fields=[{"field": "gamma",
                             "reason": "unavailable_in_source"}])
    validate_seed_dict(d)  # null + explicit reason is the honest shape


def test_validate_seed_dict_rejects_wrong_schema_version():
    with pytest.raises(ValueError, match="seed_bad_schema_version"):
        validate_seed_dict(_seed_fixture(schema_version="v9"))


# 6. DTE cap -------------------------------------------------------------------

def test_validate_seed_dict_rejects_dte_over_30():
    # UI: "data unavailable — contract DTE {n} exceeds the 30-day workbench limit".
    with pytest.raises(ValueError, match="seed_dte_out_of_workbench_scope"):
        validate_seed_dict(_seed_fixture(days_to_expiration=41))


def test_validate_seed_dict_accepts_dte_at_30_boundary():
    validate_seed_dict(_seed_fixture(days_to_expiration=30))


# 7. RoR boundary ---------------------------------------------------------------

def _code_only(path: Path) -> str:
    """Module source with strings and comments stripped, so prose compliance
    declarations (the modules deliberately state they produce NO Risk of Ruin)
    are not mistaken for code references to an RoR value."""
    parts = []
    for tok in tokenize.generate_tokens(io.StringIO(
            path.read_text(encoding="utf-8")).readline):
        if tok.type in (tokenize.COMMENT, tokenize.STRING, tokenize.NL,
                        tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                        tokenize.ENDMARKER):
            continue
        parts.append(tok.string)
    return " ".join(parts)


@pytest.mark.parametrize("rel", ["hedge_desk/options_seed.py",
                                 "hedge_desk/options_seed_refresh.py"])
def test_options_seed_modules_reference_no_risk_of_ruin_value(rel):
    code = _code_only(Path(seed_mod.__file__).resolve().parents[1] / rel)
    assert "risk_of_ruin" not in code.lower()  # no such symbol in code
    assert re.search(r"\bror\b", code, re.IGNORECASE) is None
    assert re.search(r"\bruin\b", code, re.IGNORECASE) is None
