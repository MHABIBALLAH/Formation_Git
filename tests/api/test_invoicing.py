import unittest
import json
import os
from io import BytesIO

from src.api.app import create_app
from src.api.extensions import db
from src.core.auth.models import User
from src.core.invoicing.models import Invoice

class InvoicingTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a new database for each test."""
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Register a test user and log them in
        self._register_and_login()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _register_and_login(self):
        """Helper to register and log in a user for tests."""
        # Register
        self.client.post(
            '/api/auth/register',
            data=json.dumps(dict(username="testuser", password="password")),
            content_type='application/json'
        )
        # Login
        self.client.post(
            '/api/auth/login',
            data=json.dumps(dict(username="testuser", password="password")),
            content_type='application/json'
        )

    def test_upload_invoice_no_file(self):
        """Test invoice upload fails when no file is provided."""
        res = self.client.post('/api/invoices/upload')
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'No file part', res.data)

    def test_upload_invoice_success(self):
        """Test successful invoice upload and processing."""
        # We need to mock the OCR/parsing functions as they are slow and require external dependencies
        # For this test, we'll assume they work and focus on the endpoint logic.
        # A full integration test would be separate. Here, we can't easily mock.
        # Let's instead upload a real (but tiny) image file.
        # The synthetic invoice from the `data` dir is perfect.

        # This test is more of an integration test, which is fine for now.
        # Note: This relies on the `data/invoices/synthetic_invoice.png` file.
        invoice_path = os.path.join(self.app.config['BASE_DIR'], 'data', 'invoices', 'synthetic_invoice.png')

        with open(invoice_path, 'rb') as img:
            data = {'file': (img, 'synthetic_invoice.png')}
            res = self.client.post(
                '/api/invoices/upload',
                content_type='multipart/form-data',
                data=data,
                follow_redirects=True
            )

        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Invoice processed successfully', res.data)

        # Verify the invoice was created in the DB
        invoice = Invoice.query.first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.filename, 'synthetic_invoice.png')
        self.assertEqual(invoice.status, 'completed')
        self.assertEqual(invoice.supplier, 'FOURNISSEUR ABC')
        self.assertGreater(len(invoice.line_items), 0)

    def test_list_invoices(self):
        """Test listing invoices for the current user."""
        # First, check that the list is empty
        res_empty = self.client.get('/api/invoices')
        self.assertEqual(res_empty.status_code, 200)
        self.assertEqual(json.loads(res_empty.data), [])

        # Upload an invoice to populate the list
        invoice_path = os.path.join(self.app.config['BASE_DIR'], 'data', 'invoices', 'synthetic_invoice.png')
        with open(invoice_path, 'rb') as img:
            data = {'file': (img, 'synthetic_invoice.png')}
            self.client.post('/api/invoices/upload', content_type='multipart/form-data', data=data)

        # Now, check the list again
        res_full = self.client.get('/api/invoices')
        self.assertEqual(res_full.status_code, 200)
        data = json.loads(res_full.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['filename'], 'synthetic_invoice.png')
        self.assertEqual(data[0]['status'], 'completed')

if __name__ == '__main__':
    unittest.main()
