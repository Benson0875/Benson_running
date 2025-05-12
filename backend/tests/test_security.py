import unittest
from backend.app import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_key_validation(self):
        response = self.app.get('/api/activities', headers={'X-API-Key': 'invalid_key'})
        self.assertEqual(response.status_code, 401)

    def test_user_authentication(self):
        response = self.app.get('/api/user', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 