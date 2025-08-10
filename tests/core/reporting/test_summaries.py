import unittest
from src.core.reporting.summaries import generate_financial_summary

# Mock data for testing
MOCK_INVOICE_1 = {
    'total_ht': 100.0, 'vat_amount': 20.0, 'total_ttc': 120.0
}
MOCK_INVOICE_2 = {
    'total_ht': 50.0, 'vat_amount': 5.0, 'total_ttc': 55.0
}

class TestFinancialSummary(unittest.TestCase):

    def test_summary_with_single_invoice(self):
        """Tests that the summary is calculated correctly for a single invoice."""
        summary = generate_financial_summary([MOCK_INVOICE_1])
        self.assertAlmostEqual(summary['total_expenses_ht'], 100.0)
        self.assertAlmostEqual(summary['total_vat_deductible'], 20.0)
        self.assertAlmostEqual(summary['total_expenses_ttc'], 120.0)
        self.assertAlmostEqual(summary['net_profit_loss'], -100.0)

    def test_summary_with_multiple_invoices(self):
        """Tests that the summary correctly aggregates data from multiple invoices."""
        summary = generate_financial_summary([MOCK_INVOICE_1, MOCK_INVOICE_2])
        self.assertAlmostEqual(summary['total_expenses_ht'], 150.0)
        self.assertAlmostEqual(summary['total_vat_deductible'], 25.0)
        self.assertAlmostEqual(summary['total_expenses_ttc'], 175.0)
        self.assertAlmostEqual(summary['net_profit_loss'], -150.0)

    def test_summary_with_empty_list(self):
        """Tests that the summary handles an empty list of invoices gracefully."""
        summary = generate_financial_summary([])
        self.assertAlmostEqual(summary['total_expenses_ht'], 0.0)
        self.assertAlmostEqual(summary['total_vat_deductible'], 0.0)
        self.assertAlmostEqual(summary['total_expenses_ttc'], 0.0)
        self.assertAlmostEqual(summary['net_profit_loss'], 0.0)

    def test_summary_with_missing_data(self):
        """Tests that the summary ignores invoices with missing data."""
        incomplete_invoice = {'total_ht': 100.0} # Missing other keys
        summary = generate_financial_summary([incomplete_invoice, MOCK_INVOICE_1])
        # Should only calculate based on the valid invoice
        self.assertAlmostEqual(summary['total_expenses_ht'], 200.0)
        self.assertAlmostEqual(summary['total_vat_deductible'], 20.0)
        self.assertAlmostEqual(summary['total_expenses_ttc'], 120.0)

if __name__ == '__main__':
    unittest.main()
