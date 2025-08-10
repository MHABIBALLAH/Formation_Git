import unittest
import json
from src.api.app import app

class TestApi(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check_endpoint(self):
        """Tests the /api/health endpoint."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {"status": "ok"})

    def test_dashboard_serve_endpoint(self):
        """Tests that the root endpoint serves the index.html file."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for the main application title in the header
        self.assertIn(b'<h1>ComptaAI</h1>', response.data)
        # Check for the page title, handling UTF-8 encoding for accents
        self.assertIn('Résumé Financier'.encode('utf-8'), response.data)

    def test_summary_endpoint(self):
        """Tests the /api/summary endpoint for correct structure and data types."""
        response = self.app.get('/api/summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        expected_keys = [
            'total_expenses_ht', 'total_vat_deductible', 'total_expenses_ttc',
            'total_revenue', 'net_profit_loss'
        ]
        for key in expected_keys:
            self.assertIn(key, data)

        self.assertIsInstance(data['total_expenses_ht'], (int, float))

if __name__ == '__main__':
    unittest.main()
