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

