import unittest
import json
import os
import datetime

from src.api.app import create_app
from src.api.extensions import db
from src.core.auth.models import User
from src.core.invoicing.models import Invoice
from src.core.vat.models import VatRecord

class VatTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a new database for each test."""
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._register_and_login()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _register_and_login(self):
        """Helper to register and log in a user for tests."""
        self.client.post('/api/auth/register', data=json.dumps(dict(username="testuser", password="password")), content_type='application/json')
        self.client.post('/api/auth/login', data=json.dumps(dict(username="testuser", password="password")), content_type='application/json')

    def _create_and_validate_invoice(self):
        """Helper to upload and validate the synthetic invoice."""
        invoice_path = os.path.join(self.app.config['BASE_DIR'], 'data', 'invoices', 'synthetic_invoice.png')
        with open(invoice_path, 'rb') as img:
            data = {'file': (img, 'synthetic_invoice.png')}
            self.client.post('/api/invoices/upload', content_type='multipart/form-data', data=data)

        invoice = Invoice.query.first()
        self.client.post(f'/api/invoices/{invoice.id}/validate')
        return invoice

    def test_vat_report_generation(self):
        """Test that validating an invoice correctly creates/updates a VAT record."""
        self._create_and_validate_invoice()

        # Verify VatRecord was created
        vat_record = VatRecord.query.first()
        self.assertIsNotNone(vat_record)
        self.assertEqual(vat_record.period_key, '2023-01') # From synthetic_invoice.png
        self.assertEqual(float(vat_record.total_deductible_vat), 20.00)
        self.assertEqual(float(vat_record.vat_due), -20.00)

    def test_vat_report_api(self):
        """Test the GET /api/vat/reports endpoint."""
        # Check empty state
        res_empty = self.client.get('/api/vat/reports')
        self.assertEqual(res_empty.status_code, 200)
        self.assertEqual(json.loads(res_empty.data), [])

        # Create data
        self._create_and_validate_invoice()

        # Check again
        res_full = self.client.get('/api/vat/reports')
        self.assertEqual(res_full.status_code, 200)
        data = json.loads(res_full.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['period_key'], '2023-01')
        self.assertEqual(float(data[0]['total_deductible_vat']), 20.00)

    def test_vat_report_api_filtering(self):
        """Test date filtering for the VAT reports API."""
        self._create_and_validate_invoice()

        # Date range that should include the record
        res_included = self.client.get('/api/vat/reports?start_date=2023-01-01&end_date=2023-01-31')
        self.assertEqual(len(json.loads(res_included.data)), 1)

        # Date range that should exclude the record
        res_excluded = self.client.get('/api/vat/reports?start_date=2024-01-01&end_date=2024-01-31')
        self.assertEqual(len(json.loads(res_excluded.data)), 0)

if __name__ == '__main__':
    unittest.main()
