"""Tests for the weekly options-seed pipeline (issue #103).

Deterministic: fixed clock, hand-built Cboe-shaped fixture, no network.
Reference cases are exact: DTE is date subtraction, money is Decimal.
"""

from datetime import datetime, timezone
import json

import pytest

from hedge_desk import options_seed_refresh as refresh_mod
from hedge_desk.options_seed import (
    SEED_SCHEMA_VERSION,
    seed_to_dict,
    select_seed_put,
)

AS_OF = datetime(2026, 9, 30, 15, 30, tzinfo=timezone.utc)  # fixed clock


def _opt(symbol, bid, ask, iv, delta, gamma=0.01, theta=-0.05, vega=0.1,
         rho=0.02, oi=1000, vol=100, bid_size=10, ask_size=10):
    return {
        "option": symbol, "bid": bid, "ask": ask,
        "bid_size": bid_size, "ask_size": ask_size,
        "iv": iv, "delta": delta, "gamma": gamma, "theta": theta,
        "vega": vega, "rho": rho, "open_interest": oi, "volume": vol,
    }


def _payload(options):
    return json.dumps({
        "data": {
            "symbol": "SPY", "bid": 760.00, "ask": 760.10,
            "current_price": 760.05, "options": options,
        }
    }).encode()


def _fixture_options():
    return [
        # DTE 12 expiry — in window but not closest to 30
        _opt("SPY261012P00750000", 1.10, 1.20, 0.19, -0.30),
        # DTE 29 expiry — closest to 30, the expected winner
        _opt("SPY261029P00755000", 2.10, 2.20, 0.21, -0.28, oi=5000, vol=200),
        _opt("SPY261029P00750000", 1.60, 1.70, 0.20, -0.22, oi=8000),
        _opt("SPY261029P00760000", 2.90, 3.00, 0.22, -0.35),
        _opt("SPY261029P00770000", 12.00, 12.20, 0.25, -0.80),  # ITM: excluded
        _opt("SPY261029P00745000", 1.20, 1.30, 0.0, -0.18),    # iv 0.0: excluded
        _opt("SPY261029P00740000", 0.0, 1.00, 0.19, -0.15),    # unexecutable: excluded
        _opt("SPY261029C00755000", 8.00, 8.10, 0.21, 0.72),    # call: ignored
        # DTE 41 expiry — outside the 30-day scope
        _opt("SPY261110P00750000", 3.10, 3.20, 0.23, -0.30),
    ]


def test_selects_expiry_closest_to_30_dte_within_window():
    seed = select_seed_put(_payload(_fixture_options()), "SPY", AS_OF)
    assert seed.expiration.isoformat() == "2026-10-29"
    assert seed.dte == 29  # exact: 2026-10-29 minus 2026-09-30


def test_selects_otm_put_with_delta_closest_to_minus_030():
    seed = select_seed_put(_payload(_fixture_options()), "SPY", AS_OF)
    # |-0.28 - (-0.30)| = 0.02 beats 0.05 (760) and 0.08 (750)
    assert seed.contract_id == "SPY261029P00755000"
    assert seed.delta == __import__("decimal").Decimal("-0.28")


def test_money_is_decimal_exact():
    seed = select_seed_put(_payload(_fixture_options()), "SPY", AS_OF)
    assert str(seed.bid) == "2.1"
    assert str(seed.ask) == "2.2"
    assert str(seed.mid) == "2.15"  # exact Decimal mid, no float


def test_zero_greeks_become_null_with_reason_not_zero():
    opts = [_opt("SPY261029P00755000", 2.10, 2.20, 0.21, -0.28, gamma=0.0, rho=0.0)]
    seed = select_seed_put(_payload(opts), "SPY", AS_OF)
    assert seed.gamma is None
    assert seed.rho is None
    fields = dict(seed.unavailable)
    assert fields["gamma"] == "unavailable_in_source"
    assert fields["rho"] == "unavailable_in_source"


def test_malformed_payload_raises():
    with pytest.raises(ValueError):
        select_seed_put(b"not json", "SPY", AS_OF)


def test_no_expiry_in_window_raises():
    opts = [_opt("SPY261110P00750000", 3.10, 3.20, 0.23, -0.30)]  # DTE 41 only
    with pytest.raises(ValueError, match="no put expiration within 30 days"):
        select_seed_put(_payload(opts), "SPY", AS_OF)


def test_naive_clock_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        select_seed_put(_payload(_fixture_options()), "SPY",
                        datetime(2026, 9, 30, 15, 30))


def test_seed_dict_serialisation_contract():
    raw = json.loads(_payload(_fixture_options()).decode())["data"]
    seed = select_seed_put(_payload(_fixture_options()), "SPY", AS_OF)
    d = seed_to_dict(seed, "SPY", raw, AS_OF,
                     {"status": "ok", "refreshed_at": AS_OF.isoformat(), "reason": None})
    assert d["schema_version"] == SEED_SCHEMA_VERSION
    assert d["symbol"] == "SPY" and d["option_type"] == "PUT"
    assert d["days_to_expiration"] == 29
    assert d["source"] == "cboe-delayed" and d["data_mode"] == "batch"
    assert d["trade_authorized"] is False
    for f in ("bid", "ask", "mid", "strike", "implied_volatility", "delta"):
        assert isinstance(d[f], str), f  # Decimal-serialised, never float
    blob = json.dumps(d).lower()
    assert "risk_of_ruin" not in blob and '"ror"' not in blob


def _ok_transport(raw):
    return lambda url: (200, raw)


def test_refresh_writes_seed_on_success(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh_mod, "SEED_PATH", tmp_path / "seed.json")
    rc = refresh_mod.refresh(transport=_ok_transport(_payload(_fixture_options())))
    assert rc == 0
    d = json.loads((tmp_path / "seed.json").read_text())
    assert d["contract_id"] == "SPY261029P00755000"
    assert d["refresh"]["status"] == "ok"


def test_refresh_failure_preserves_last_good_byte_identical(tmp_path, monkeypatch):
    seed_file = tmp_path / "seed.json"
    monkeypatch.setattr(refresh_mod, "SEED_PATH", seed_file)
    assert refresh_mod.refresh(transport=_ok_transport(_payload(_fixture_options()))) == 0
    before = seed_file.read_bytes()

    def failing(url):
        return (500, b"")
    assert refresh_mod.refresh(transport=failing) == 0  # last-good path
    after = json.loads(seed_file.read_bytes())
    before_d = json.loads(before)
    # contract fields byte-identical: nothing synthetic, nothing rewritten
    for f in ("contract_id", "bid", "ask", "mid", "strike", "implied_volatility",
              "delta", "gamma", "theta", "vega", "rho", "as_of"):
        assert after[f] == before_d[f], f
    assert after["refresh"]["status"] == "fetch_failed"
    assert after["refresh"]["reason"]
    assert after["refresh"]["previous_as_of"] == before_d["as_of"]


def test_refresh_failure_with_no_last_good_fails_closed(tmp_path, monkeypatch):
    seed_file = tmp_path / "seed.json"
    monkeypatch.setattr(refresh_mod, "SEED_PATH", seed_file)

    def failing(url):
        raise ConnectionError("down")
    assert refresh_mod.refresh(transport=failing) == 1
    assert not seed_file.exists()  # nothing invented
