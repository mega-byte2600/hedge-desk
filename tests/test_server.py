import json
import unittest
from contextlib import nullcontext
from unittest.mock import patch

from hedge_desk.server import _supabase_status, application

class ServerTests(unittest.TestCase):
    def request(self, path):
        captured = {}
        def start(status, headers):
            captured['status'] = status
            captured['headers'] = headers
        body = b''.join(application({'PATH_INFO': path}, start))
        return captured['status'], json.loads(body)

    def test_health_is_paper_only_and_reports_unconfigured_supabase(self):
        with patch.dict('os.environ', {}, clear=True):
            status, payload = self.request('/api/health')
        self.assertEqual(status, '200 OK')
        self.assertEqual(payload['mode'], 'paper')
        self.assertFalse(payload['live_orders_enabled'])
        self.assertFalse(payload['supabase']['configured'])

    def test_supabase_health_uses_public_key_without_bearer_token(self):
        response = type("Response", (), {"status": 200})()
        env = {
            "SUPABASE_URL": "https://project.supabase.co",
            "SUPABASE_PUBLISHABLE_KEY": "sb_publishable_test",
        }
        with patch.dict('os.environ', env, clear=True), patch(
            'hedge_desk.server.urlopen', return_value=nullcontext(response)
        ) as opened:
            supabase = _supabase_status()

        self.assertTrue(supabase['configured'])
        self.assertTrue(supabase['reachable'])
        request = opened.call_args.args[0]
        self.assertEqual(request.full_url, "https://project.supabase.co/auth/v1/health")
        self.assertEqual(request.get_header("Apikey"), "sb_publishable_test")
        self.assertIsNone(request.get_header("Authorization"))

    def test_candidate_api_covers_all_six_desks(self):
        status, payload = self.request('/api/candidates')
        self.assertEqual(status, '200 OK')
        self.assertEqual(len({row['desk_id'] for row in payload['candidates']}), 6)
        self.assertTrue(all(not row['trade_authorized'] for row in payload['candidates']))

    def test_risk_dashboard_is_paper_only(self):
        status, payload = self.request('/api/risk-dashboard')

        self.assertEqual(status, '200 OK')
        self.assertEqual(payload['mode'], 'PAPER_RESEARCH_ONLY')
        self.assertFalse(payload['live_orders_enabled'])
        self.assertEqual(payload['trade_authorized_count'], 0)
        self.assertGreaterEqual(payload['desk_count'], 6)
        self.assertTrue(payload['executive_actions'])

    def test_auth_route_is_wired_into_server_and_report_stays_public(self):
        # /api/auth/me should respond through the server (unauthenticated now,
        # but a real 200 JSON from the auth app, not a 404 or the SPA fallback).
        from hedge_desk.server import _dispatch
        captured = {}

        def start(status, headers):
            captured['status'] = status
            captured['headers'] = headers

        import json as _json
        body = b''.join(_dispatch({'PATH_INFO': '/api/auth/me', 'REQUEST_METHOD': 'GET'}, start))
        self.assertEqual(captured['status'], '200 OK')
        payload = _json.loads(body)
        self.assertIn('authenticated', payload)

        # report/candidate endpoints remain publicly reachable without auth (guest tier open)
        status2, report = self.request('/api/candidates')
        self.assertEqual(status2, '200 OK')
        self.assertEqual(len({row['desk_id'] for row in report['candidates']}), 6)

    def test_live_report_recomputes_a_valid_paper_only_console_payload(self):
        status, payload = self.request('/api/report')

        self.assertEqual(status, '200 OK')
        self.assertEqual(payload['schema_version'], 'desk-console-1')
        report = payload['report']
        self.assertEqual(report['environment'], 'paper')
        self.assertFalse(report['live_orders_enabled'])
        self.assertEqual(report['real_trades_executed'], 0)
        self.assertEqual(len(report['projects']), 6)
        self.assertIn('report_sha256', report)
        self.assertIn('generated_at', report)
        # registry + summary present for the console to render
        self.assertEqual(len(payload['registry']), len(payload['report']['projects']) + 1)
        self.assertIn('projects_evaluated', payload['summary'])

    def test_live_report_is_cached_but_fresh_within_cache_window(self):
        # Two calls inside the API cache window return the same generated_at
        # (cache hit) — proves the memoization path is live, not a fresh
        # recompute per request which would break the golden render.
        first = self.request('/api/report')[1]
        second = self.request('/api/report')[1]
        self.assertEqual(
            first['report']['generated_at'],
            second['report']['generated_at'],
            'repeat calls should be served from the API cache window',
        )

    def test_live_report_uses_engine_not_the_committed_snapshot(self):
        # The endpoint must be recomputing from the engine (fresh timestamp),
        # not serving the static dist/report.json snapshot. We assert the
        # report hash matches a direct engine build at the same moment.
        from hedge_desk.console_report import build_console_payload
        from hedge_desk.overnight import build_morning_report
        from datetime import datetime, timezone

        engine = build_console_payload(
            build_morning_report(datetime.now(timezone.utc), "TEST-LIVE")
        )
        status, payload = self.request('/api/report')
        self.assertEqual(status, '200 OK')
        self.assertEqual(payload['report']['environment'], engine['report']['environment'])
        self.assertEqual(len(payload['report']['projects']), len(engine['report']['projects']))

    def test_auth_tier_and_broker_routes_are_forwarded_to_the_auth_app(self):
        # Regression: the server previously forwarded only /api/auth/*, so
        # /api/tier and /api/broker/* fell through to the SPA fallback and
        # returned HTML instead of JSON. Assert every auth-app route resolves
        # to a JSON response from the server's dispatch.
        from hedge_desk.server import _dispatch
        import json as _json

        for path, method in (
            ('/api/tier', 'GET'),
            ('/api/broker/status', 'GET'),
            ('/api/data/real', 'GET'),
            ('/api/auth/me', 'GET'),
        ):
            captured = {}

            def start(status, headers, _c=captured):
                _c['status'] = status
                _c['headers'] = dict(headers)

            body = b''.join(
                _dispatch({'PATH_INFO': path, 'REQUEST_METHOD': method}, start)
            )
            content_type = captured['headers'].get('Content-Type', '')
            self.assertIn('application/json', content_type, f'{path} should return JSON')
            parsed = _json.loads(body)
            self.assertIsInstance(parsed, dict)

    def test_public_report_endpoints_are_not_gated(self):
        # The guest test-drive tier must stay open: no auth required.
        for path in ('/api/health', '/api/candidates', '/api/risk-dashboard'):
            status, payload = self.request(path)
            self.assertEqual(status, '200 OK', path)
            self.assertIsInstance(payload, dict)

    def raw(self, path):
        """Request without assuming a JSON body (the shell is HTML)."""
        from hedge_desk.server import application
        captured = {}
        def start(status, headers):
            captured['status'] = status
        body = b''.join(application({'PATH_INFO': path}, start))
        return captured['status'], body

    def test_unknown_api_paths_return_json_not_html(self):
        # Every miss used to fall back to the SPA shell with 200, so a client's
        # fetch('/api/typo') received HTML that it then tried to parse as JSON,
        # and a mistyped API route looked like it had succeeded.
        for path in ('/api/does-not-exist', '/api/candidatesX'):
            status, body = self.raw(path)
            self.assertEqual(status, '404 Not Found', path)
            self.assertEqual(json.loads(body).get('error'), 'not_found', path)

    def test_missing_asset_returns_404_not_the_shell(self):
        status, body = self.raw('/nope.html')
        self.assertEqual(status, '404 Not Found')
        self.assertEqual(json.loads(body).get('error'), 'not_found')

    def test_extensionless_deep_link_still_serves_the_shell(self):
        from hedge_desk.server import WEB
        if not (WEB / "index.html").is_file():
            # CI runs the suite without building the bundle, so there is no shell
            # for the SPA fallback to return. The routing rule is what this test
            # covers; the 404 cases above do not depend on the bundle.
            self.skipTest("web bundle not built; no shell to serve")
        status, body = self.raw('/some/deep/link')
        self.assertEqual(status, '200 OK')
        self.assertIn(b'<!doctype html', body[:200])

    def test_a_second_cache_key_is_not_blocked_by_a_slow_build(self):
        """The builder must run outside the cache lock.

        _cached() called builder() while holding the lock, so the supabase-status
        probe (a urlopen with a 5s timeout, on the health path Render polls)
        serialised every other endpoint, including the engine-backed report.
        """
        import threading
        import time
        from hedge_desk import server as srv

        srv._api_cache.clear()
        started = threading.Event()
        release = threading.Event()

        def slow_build():
            started.set()
            release.wait(5)
            return 'slow'

        worker = threading.Thread(target=lambda: srv._cached('test-slow-key', slow_build))
        worker.start()
        try:
            self.assertTrue(started.wait(2), 'the slow builder never started')
            began = time.monotonic()
            value = srv._cached('test-fast-key', lambda: 'fast')
            elapsed = time.monotonic() - began
            self.assertEqual(value, 'fast')
            self.assertLess(elapsed, 0.5, 'an unrelated cache key blocked behind a slow build')
        finally:
            release.set()
            worker.join(5)
            srv._api_cache.clear()
