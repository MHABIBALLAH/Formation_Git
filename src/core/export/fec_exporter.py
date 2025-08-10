import csv
import io
from typing import List, Dict, Any
from src.core.accounting.entry import AccountingEntry

# The 18 mandatory columns for the FEC file, in order.
FEC_HEADER = [
    "JournalCode", "JournalLib", "EcritureNum", "EcritureDate", "CompteNum",
    "CompteLib", "CompAuxNum", "CompAuxLib", "PieceRef", "PieceDate",
    "EcritureLib", "Debit", "Credit", "EcritureLet", "DateLet",
    "ValidDate", "Montantdevise", "Idevise"
]

def export_to_fec(entries: List[AccountingEntry], journal_code: str = "AC", journal_lib: str = "ACHATS") -> str:
    """
    Exports a list of accounting entries to a string in the French FEC format.

    Args:
        entries: A list of AccountingEntry objects.
        journal_code: The journal code to use for these entries (e.g., 'AC' for Achat).
        journal_lib: The library for the journal.

    Returns:
        A string containing the data in FEC CSV format (tab-delimited).
    """
    output = io.StringIO()
    # Explicitly set the line terminator to `\n` to avoid `\r\n` issues on some systems.
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')

    writer.writerow(FEC_HEADER)

    ecriture_num = 1

    for entry in entries:
        entry_date_str = entry.entry_date.strftime('%Y%m%d')
        debit_str = f"{entry.debit:.2f}".replace('.', ',') if entry.debit is not None else ""
        credit_str = f"{entry.credit:.2f}".replace('.', ',') if entry.credit is not None else ""

        row = [
            journal_code,
            journal_lib,
            str(ecriture_num).zfill(5),
            entry_date_str,
            str(entry.account_number),
            entry.account_name,
            "",  # CompAuxNum
            "",  # CompAuxLib
            "",  # PieceRef
            entry_date_str, # PieceDate
            entry.description,
            debit_str,
            credit_str,
            "",  # EcritureLet
            "",  # DateLet
            entry_date_str, # ValidDate
            "",  # Montantdevise
            ""   # Idevise
        ]
        writer.writerow(row)

    return output.getvalue()
