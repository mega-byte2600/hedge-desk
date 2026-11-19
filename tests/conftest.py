"""Repo-wide test isolation: never let tests touch the production FRED cache.

``hedge_desk.rates_desk.fred_series_rows`` caches observations under
``artifacts/.cache/fred`` by default. Tests that run the nightly pipeline
with fake transports would otherwise write stub rows (e.g. "1.0") into that
real cache directory, and a later production batch would serve those stubs
as genuine FRED observations. This actually happened on 2026-09-26:
``test_nightly.py`` / ``test_oil_desk.py`` fake-rate transports poisoned the
cache and the committed ``am-report-latest.json`` shipped fabricated macro
values labeled REAL_FRED_MACRO.

This autouse fixture redirects ``HEDGE_DESK_CACHE_DIR`` at a per-test tmp
directory for the whole suite, so no test can ever poison production cache
entries again. Tests that need explicit cache control (e.g.
``test_fred_cache.py``) still override the variable in their own setUp.
"""


import pytest


@pytest.fixture(autouse=True)
def _sandbox_fred_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("HEDGE_DESK_CACHE_DIR", str(tmp_path / "fred-cache"))


# --- Hermetic network guard (CarpeDATA invariant 5) --------------------------
# Any attempt to open a non-loopback connection during the session raises, so
# a leaking test fails loudly instead of silently hitting a real provider.
# Local servers on 127.0.0.1/::1 stay allowed. Equivalent to pytest-socket's
# --disable-socket --allow-hosts=127.0.0.1.
import os
import socket

_LOOPBACK = {"127.0.0.1", "::1", "localhost"}
_real_create_connection = socket.create_connection


class LiveNetworkBlocked(OSError):
    """Raised when a test tries to reach the live network."""


def _guarded_create_connection(address, *args, **kwargs):
    host = str(address[0]) if isinstance(address, tuple) else str(address)
    if host in _LOOPBACK:
        return _real_create_connection(address, *args, **kwargs)
    raise LiveNetworkBlocked(f"test attempted live network access to {host}; inject a transport")


@pytest.fixture(autouse=True, scope="session")
def _no_live_network():
    saved = {k: os.environ.pop(k) for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy") if k in os.environ}
    socket.create_connection = _guarded_create_connection
    try:
        yield
    finally:
        socket.create_connection = _real_create_connection
        os.environ.update(saved)
