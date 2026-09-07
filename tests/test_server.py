import json
import unittest
from unittest.mock import patch

from hedge_desk.server import application

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

    def test_candidate_api_covers_all_six_desks(self):
        status, payload = self.request('/api/candidates')
        self.assertEqual(status, '200 OK')
        self.assertEqual(len({row['desk_id'] for row in payload['candidates']}), 6)
        self.assertTrue(all(not row['trade_authorized'] for row in payload['candidates']))
