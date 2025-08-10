import unittest
import json
from src.api.app import create_app

class TestApi(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask app."""
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up the app context."""
        self.app_context.pop()

    def test_health_check_endpoint(self):
        """Tests the /api/health endpoint, which should always be public."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {"status": "ok"})

    def test_root_is_public(self):
        """Tests that the root URL ('/') is public and serves the main page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>ComptaAI</title>', response.data)

if __name__ == '__main__':
    unittest.main()
