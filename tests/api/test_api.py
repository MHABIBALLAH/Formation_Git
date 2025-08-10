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
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'Tableau de Bord Financier', response.data)

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
