"""FRED measurement and cache regressions with fixed dates and no network."""
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from hedge_desk import rates_desk as rates, web_app


class FredQualityTests(unittest.TestCase):
    def test_probe_counts_rows_and_discloses_scope_not_freshness(self):
        class Clock(date):
            @classmethod
            def today(cls):
                return cls(2026, 10, 5)
        with patch.object(web_app, 'date', Clock), patch.object(web_app, 'fred_series_rows', return_value=(("2026-08-01", Decimal('321')), ("2026-09-01", Decimal('322')))):
            result = web_app._probe_source('fred', True, False, web_app._probe_fred)
        self.assertEqual(result['status'], 'LIVE')
        self.assertEqual(result['observation_count'], 2)
        self.assertEqual(result['dataset'], 'CPIAUCSL')
        self.assertEqual(result['observation_age_days'], 34)
        self.assertEqual(result['freshness_status'], 'NOT_ASSESSED')
        self.assertEqual(result['coverage_status'], 'NOT_ASSESSED')

    def test_nightly_measurement_is_not_overwritten(self):
        self.assertNotIn("cells[1].textContent = 'Live'", web_app._DASHBOARD_API_LAYER)
        self.assertIn('freshness and coverage not assessed', web_app._DASHBOARD_API_LAYER)

    def test_expired_or_legacy_cache_refetches_and_failure_does_not_serve_it(self):
        for fetched_at in (None, 1000):
            with self.subTest(fetched_at=fetched_at), tempfile.TemporaryDirectory() as directory:
                cache = Path(directory)/'fred'/'DGS10'/'2026-09-01_2026-09-30.json'
                cache.parent.mkdir(parents=True)
                payload = {'series': 'DGS10', 'start': '2026-09-01', 'end': '2026-09-30', 'rows': [['2026-09-01', '4']]}
                if fetched_at is not None:
                    payload['fetched_at'] = fetched_at
                cache.write_text(json.dumps(payload))
                with patch.object(rates.time, 'time', return_value=5000):
                    with self.assertRaises(ValueError):
                        rates.fred_series_rows('DGS10', date(2026,9,1), date(2026,9,30), lambda url: (503, b''), cache_dir=Path(directory), retries=0)
                    result = rates.fred_series_rows('DGS10', date(2026,9,1), date(2026,9,30), lambda url: (200, b'observation_date,DGS10\n2026-09-30,5\n'), cache_dir=Path(directory), retries=0)
                self.assertEqual(result, (('2026-09-30', Decimal('5')),))

    def test_concurrent_cache_writers_leave_one_valid_atomic_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            barrier = Barrier(2)
            def fetch(url):
                barrier.wait(timeout=5)
                return 200, b'observation_date,DGS10\n2026-09-30,5\n'
            def call():
                return rates.fred_series_rows('DGS10', date(2026,9,1), date(2026,9,30), fetch, cache_dir=Path(directory), retries=0)
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _: call(), range(2)))
            self.assertEqual(results[0], results[1])
            files = list((Path(directory)/'fred'/'DGS10').iterdir())
            self.assertEqual(len(files), 1)
            self.assertEqual(json.loads(files[0].read_text())['rows'], [['2026-09-30', '5']])

    def test_dates_missing_nonfinite_sorting_and_conflicts(self):
        raw = b'observation_date,DGS10\n2026-09-02,5\n2026-09-01,4\n2026-09-03,.\n2026-09-04,NaN\n'
        self.assertEqual(rates._parse_fred_csv(raw), (('2026-09-01', Decimal('4')), ('2026-09-02', Decimal('5'))))
        for raw in (b'observation_date,DGS10\n2026-02-30,4\n', b'observation_date,DGS10\n2026-09-01,4\n2026-09-01,5\n', b'<html>failure</html>'):
            with self.assertRaises(ValueError):
                rates._parse_fred_csv(raw)
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            rates._parse_fred_json(b'{"count":2,"observations":[{"date":"2026-09-01","value":"4"}]}')

    def test_window_filters_and_keyed_errors_are_secret_free(self):
        with patch.dict('os.environ', {'FRED_API_KEY': 'never-disclose', 'HEDGE_DESK_CACHE_DIR': 'off'}):
            def broken(url):
                raise RuntimeError(url)
            with self.assertRaises(ValueError) as error:
                rates.fred_series_rows('DGS10', date(2026,9,1), date(2026,9,30), broken, retries=0)
            self.assertNotIn('never-disclose', str(error.exception))
        self.assertEqual(rates._validated_rows((('2026-08-31', '4'), ('2026-09-01', '5')), date(2026,9,1), date(2026,9,30)), (('2026-09-01', Decimal('5')),))
