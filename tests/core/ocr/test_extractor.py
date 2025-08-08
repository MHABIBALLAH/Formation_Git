import unittest
import os
from src.core.ocr.reader import extract_text_from_image
from src.core.ocr.extractor import extract_invoice_data

class TestOcrExtractor(unittest.TestCase):

    def test_extract_data_from_synthetic_invoice(self):
        """
        Tests that the extractor can parse data from the synthetic invoice.
        """
        image_path = os.path.join('data', 'invoices', 'synthetic_invoice.png')
        self.assertTrue(os.path.exists(image_path), f"Test image not found at {image_path}")

        # 1. Get the raw text from the image
        raw_text = extract_text_from_image(image_path)
        self.assertIsNotNone(raw_text)

        # 2. Extract structured data from the text
        extracted_data = extract_invoice_data(raw_text)

        # 3. Define the expected data
        expected_data = {
            'invoice_id': 'INV2023-042',
            'date': '26/10/2023',
            'total_ht': 1000.00,
            'vat_amount': 200.00,
            'total_ttc': 1200.00
        }

        # 4. Assert that the extracted data matches the expected data
        self.assertEqual(extracted_data, expected_data)

if __name__ == '__main__':
    unittest.main()
