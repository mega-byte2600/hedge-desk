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

import os

import pytest


@pytest.fixture(autouse=True)
def _sandbox_fred_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("HEDGE_DESK_CACHE_DIR", str(tmp_path / "fred-cache"))
