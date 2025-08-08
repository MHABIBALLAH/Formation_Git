import unittest
import os
from src.core.ocr.reader import extract_text_from_image
from src.core.ocr.extractor import extract_invoice_data
from src.core.accounting.categories import DEFAULT_CATEGORY

class TestOcrExtractor(unittest.TestCase):

    def test_extract_data_from_synthetic_invoice(self):
        """
        Tests that the extractor can parse data, including line items and categories,
        from the synthetic invoice.
        """
        image_path = os.path.join('data', 'invoices', 'synthetic_invoice.png')
        self.assertTrue(os.path.exists(image_path))

        raw_text = extract_text_from_image(image_path)
        self.assertIsNotNone(raw_text)

        extracted_data = extract_invoice_data(raw_text)

        # --- Define Expected Data ---
        expected_line_items = [
            {
                'description': 'Service de conseil',
                'category': 'Documentation et honoraires',
                'quantity': 10,
                'unit_price': 75.0,
                'total': 750.0
            },
            {
                'description': 'Produit À',
                'category': DEFAULT_CATEGORY,
                'quantity': 12,
                'unit_price': 125.0,
                'total': 250.0
            }
        ]

        # --- Assertions ---
        self.assertEqual(extracted_data['invoice_id'], 'INV2023-042')
        self.assertEqual(extracted_data['date'], '26/10/2023')
        self.assertEqual(extracted_data['total_ht'], 1000.00)
        self.assertEqual(extracted_data['total_ttc'], 1200.00)
        self.assertEqual(extracted_data['line_items'], expected_line_items)


if __name__ == '__main__':
    unittest.main()
