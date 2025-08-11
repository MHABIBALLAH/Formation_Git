import unittest
import json
import os

from src.api.app import create_app
from src.api.extensions import db
from src.core.auth.models import User
from src.core.invoicing.models import Invoice
from src.core.cashflow.models import Transaction

class CashflowTestCase(unittest.TestCase):

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

    def test_cashflow_summary(self):
        """Test the cashflow summary endpoint."""
        # Step 1: Check initial empty state
        res_empty = self.client.get('/api/cashflow')
        self.assertEqual(res_empty.status_code, 200)
        data_empty = json.loads(res_empty.data)
        self.assertEqual(data_empty['total_inflows'], 0)
        self.assertEqual(data_empty['total_outflows'], 0)
        self.assertEqual(data_empty['net_balance'], 0)

        # Step 2: Create a transaction by validating an invoice
        self._create_and_validate_invoice()

        # Step 3: Check the summary again
        res_full = self.client.get('/api/cashflow')
        self.assertEqual(res_full.status_code, 200)
        data_full = json.loads(res_full.data)
        self.assertEqual(data_full['total_inflows'], 0)
        self.assertEqual(data_full['total_outflows'], 120.00) # The debit transaction
        self.assertEqual(data_full['net_balance'], -120.00)

    def test_cashflow_date_filtering(self):
        """Test the date filtering on the cashflow summary endpoint."""
        invoice = self._create_and_validate_invoice()
        invoice_date = invoice.invoice_date.strftime('%Y-%m-%d')

        # Filter for a date range that includes the transaction
        res_included = self.client.get(f'/api/cashflow?start_date={invoice_date}&end_date={invoice_date}')
        data_included = json.loads(res_included.data)
        self.assertEqual(data_included['total_outflows'], 120.00)

        # Filter for a date range that excludes the transaction
        res_excluded = self.client.get('/api/cashflow?start_date=2000-01-01&end_date=2000-01-02')
        data_excluded = json.loads(res_excluded.data)
        self.assertEqual(data_excluded['total_outflows'], 0)

if __name__ == '__main__':
    unittest.main()
