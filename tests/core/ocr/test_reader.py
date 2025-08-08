import unittest
import os
from src.core.ocr.reader import extract_text_from_image

class TestOcrReader(unittest.TestCase):

    def test_extract_text_from_placeholder_image(self):
        """
        Tests that the OCR reader can extract text from the placeholder image.
        """
        # Construct the path to the test image
        # This assumes the test is run from the root of the project
        image_path = os.path.join('data', 'invoices', 'placeholder_invoice.png')

        # Check if the placeholder image exists
        self.assertTrue(os.path.exists(image_path), f"Test image not found at {image_path}")

        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)

        # Assert that the extracted text is not empty
        self.assertIsNotNone(extracted_text)
        self.assertIsInstance(extracted_text, str)

        # Adjust assertions to match the actual OCR output for the placeholder
        self.assertIn("No. 123", extracted_text)
        self.assertIn("Total", extracted_text)
        self.assertIn("01/01/2024", extracted_text)


if __name__ == '__main__':
    unittest.main()
