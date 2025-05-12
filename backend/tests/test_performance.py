import unittest
import time
from backend.app import app

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_ping_response_time(self):
        start_time = time.time()
        response = self.app.get('/api/ping')
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.1)  # 回應時間應小於 0.1 秒

    def test_api_activities_response_time(self):
        start_time = time.time()
        response = self.app.get('/api/activities')
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.2)  # 回應時間應小於 0.2 秒

    def test_api_analyze_response_time(self):
        start_time = time.time()
        response = self.app.post('/api/analyze', json={'data': 'test'})
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.3)  # 回應時間應小於 0.3 秒

if __name__ == '__main__':
    unittest.main() 