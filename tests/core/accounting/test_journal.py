import unittest
from datetime import date
from src.core.accounting.journal import generate_entries_from_invoice
from src.core.accounting.entry import AccountingEntry
from src.core.accounting.categories import CATEGORY_TO_ACCOUNT

# Mock data simulating the output of the OCR extractor
MOCK_INVOICE_DATA = {
    'invoice_id': 'INV2023-042',
    'date': '26/10/2023',
    'total_ht': 1000.00,
    'vat_amount': 200.00,
    'total_ttc': 1200.00,
    'line_items': [
        {
            'description': 'Service de conseil',
            'category': 'Documentation et honoraires',
            'quantity': 10, 'unit_price': 75.0, 'total': 750.0
        },
        {
            'description': 'Produit A',
            'category': 'Autres charges', # Using a defined expense category
            'quantity': 2, 'unit_price': 125.0, 'total': 250.0
        }
    ]
}

class TestJournalGenerator(unittest.TestCase):

    def test_successful_generation(self):
        """
        Tests that a valid invoice data dictionary generates a correct and balanced journal entry.
        """
        entries = generate_entries_from_invoice(MOCK_INVOICE_DATA)

        self.assertEqual(len(entries), 4)
        self.assertTrue(all(isinstance(e, AccountingEntry) for e in entries))

        total_debits = sum(e.debit for e in entries if e.debit is not None)
        total_credits = sum(e.credit for e in entries if e.credit is not None)
        self.assertAlmostEqual(total_debits, total_credits)
        self.assertAlmostEqual(total_credits, 1200.00)

        first_debit_entry = entries[0]
        self.assertEqual(first_debit_entry.account_number, CATEGORY_TO_ACCOUNT['Documentation et honoraires'])
        self.assertEqual(first_debit_entry.debit, 750.0)
        self.assertEqual(first_debit_entry.entry_date, date(2023, 10, 26))

        credit_entry = entries[-1]
        self.assertEqual(credit_entry.account_number, 401)
        self.assertEqual(credit_entry.credit, 1200.0)

    def test_missing_data_handling(self):
        """
        Tests that the generator raises a ValueError if essential data is missing.
        """
        incomplete_data = MOCK_INVOICE_DATA.copy()
        del incomplete_data['total_ttc']

        with self.assertRaises(ValueError):
            generate_entries_from_invoice(incomplete_data)

    def test_invalid_date_format(self):
        """
        Tests that the generator raises a ValueError for an invalid date format.
        """
        invalid_date_data = MOCK_INVOICE_DATA.copy()
        invalid_date_data['date'] = '2023-10-26'

        with self.assertRaises(ValueError):
            generate_entries_from_invoice(invalid_date_data)

if __name__ == '__main__':
    unittest.main()
