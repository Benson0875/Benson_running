import unittest
from backend.app import app
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_ping(self):
        response = self.app.get('/api/ping')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['message'], 'pong')

    def test_api_activities(self):
        response = self.app.get('/api/activities')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('activities', data['data'])

    def test_api_analyze(self):
        """測試活動分析 API"""
        test_data = {
            'activity_id': '123',
            'user_profile': {'age': 30, 'weight': 70}
        }
        logger.info("Sending request to /api/analyze...")
        response = self.app.post('/api/analyze', json=test_data, headers={'X-API-Key': 'test_api_key'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('formatted', data)

if __name__ == '__main__':
    unittest.main() 