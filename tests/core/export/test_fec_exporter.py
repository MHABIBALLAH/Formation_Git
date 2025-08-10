import unittest
import sys
import os
from datetime import date

# Add the project root to the path to allow imports from `src`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.accounting.entry import AccountingEntry
from src.core.export.fec_exporter import export_to_fec, FEC_HEADER

class TestFecExporter(unittest.TestCase):

    def test_fec_export_format(self):
        """
        Tests the basic format of the FEC export.
        """
        # 1. Prepare mock data
        test_entries = [
            AccountingEntry(
                entry_date=date(2023, 10, 26),
                account_number=607000,
                account_name="Achats de marchandises",
                description="Achat de produit A",
                debit=250.00
            ),
            AccountingEntry(
                entry_date=date(2023, 10, 26),
                account_number=445660,
                account_name="TVA Déductible",
                description="TVA sur facture INV-123",
                debit=50.00
            ),
            AccountingEntry(
                entry_date=date(2023, 10, 26),
                account_number=401000,
                account_name="Fournisseurs",
                description="Facture INV-123",
                credit=300.00
            ),
        ]

        # 2. Call the exporter
        fec_content = export_to_fec(test_entries)

        # 3. Perform assertions
        self.assertIsInstance(fec_content, str)

        lines = fec_content.strip().split('\n')

        # Check header
        header = lines[0].split('\t')
        self.assertEqual(header, FEC_HEADER)

        # Check number of rows (1 header + 3 entries)
        self.assertEqual(len(lines), 4)

        # Check a data row
        data_row = lines[1].split('\t')
        self.assertEqual(len(data_row), 18) # Check for 18 columns
        self.assertEqual(data_row[3], "20231026") # Check EcritureDate format
        self.assertEqual(data_row[11], "250,00") # Check Debit format (with comma)
        self.assertEqual(data_row[12], "") # Check empty Credit

if __name__ == '__main__':
    unittest.main()
