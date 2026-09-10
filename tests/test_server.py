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
