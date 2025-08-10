import unittest
from src.core.vat.calculator import validate_invoice_totals

# Mock data for testing
VALID_DATA = {
    'total_ht': 100.0, 'vat_amount': 20.0, 'total_ttc': 120.0, 'vat_rate': 20.0
}
VALID_DATA_NO_RATE = {
    'total_ht': 100.0, 'vat_amount': 20.0, 'total_ttc': 120.0
}
INVALID_SUM_DATA = {
    'total_ht': 100.0, 'vat_amount': 20.0, 'total_ttc': 125.0 # Should be 120.0
}
INVALID_RATE_DATA = {
    'total_ht': 100.0, 'vat_amount': 20.0, 'total_ttc': 120.0, 'vat_rate': 10.0 # Rate is wrong
}
MISSING_DATA = {
    'total_ht': 100.0, 'vat_amount': 20.0 # Missing total_ttc
}

class TestVatCalculator(unittest.TestCase):

    def test_valid_totals_with_rate(self):
        """Tests that validation passes with correct data, including the rate."""
        self.assertTrue(validate_invoice_totals(VALID_DATA))

    def test_valid_totals_without_rate(self):
        """Tests that validation passes if the rate is not provided but other totals are correct."""
        self.assertTrue(validate_invoice_totals(VALID_DATA_NO_RATE))

    def test_invalid_sum(self):
        """Tests that validation fails when HT + VAT does not equal TTC."""
        self.assertFalse(validate_invoice_totals(INVALID_SUM_DATA))

    def test_invalid_rate(self):
        """Tests that validation fails when the VAT rate calculation is incorrect."""
        self.assertFalse(validate_invoice_totals(INVALID_RATE_DATA))

    def test_missing_data(self):
        """Tests that validation fails if essential financial data is missing."""
        self.assertFalse(validate_invoice_totals(MISSING_DATA))

    def test_zero_values(self):
        """Tests that validation handles zero values correctly."""
        zero_data = {'total_ht': 100.0, 'vat_amount': 0.0, 'total_ttc': 100.0, 'vat_rate': 0.0}
        self.assertTrue(validate_invoice_totals(zero_data))

if __name__ == '__main__':
    unittest.main()
