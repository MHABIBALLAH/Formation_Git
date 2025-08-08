import unittest
import os
from src.core.ocr.reader import extract_text_from_image

class TestOcrReader(unittest.TestCase):

    def test_extract_text_from_synthetic_image(self):
        """
        Tests that the OCR reader can extract text from the synthetic invoice image.
        """
        image_path = os.path.join('data', 'invoices', 'synthetic_invoice.png')
        self.assertTrue(os.path.exists(image_path), f"Test image not found at {image_path}")

        extracted_text = extract_text_from_image(image_path)

        self.assertIsNotNone(extracted_text)
        self.assertIsInstance(extracted_text, str)

        # Check for some key labels from the more detailed synthetic invoice
        self.assertIn("FACTURE N°", extracted_text)
        self.assertIn("Total TTC", extracted_text)
        self.assertIn("Votre Entreprise", extracted_text)

if __name__ == '__main__':
    unittest.main()
