from datetime import datetime
from typing import Dict, Any, List

from src.core.accounting.entry import AccountingEntry
from src.core.accounting.categories import CATEGORY_TO_ACCOUNT, DEFAULT_CATEGORY

# Standard account numbers from the French Plan Comptable Général (PCG)
FOURNISSEUR_ACCOUNT = 401  # Compte Fournisseurs (Accounts Payable)
TVA_DEDUCTIBLE_ACCOUNT = 44566  # TVA sur autres biens et services déductible

def generate_entries_from_invoice(invoice_data: Dict[str, Any]) -> List[AccountingEntry]:
    """
    Generates a list of accounting entries from a dictionary of extracted invoice data.

    Args:
        invoice_data: The structured data extracted from the invoice.

    Returns:
        A list of AccountingEntry objects representing the journal entries for the invoice.
    """
    entries = []

    # --- Validate input data ---
    required_keys = ['date', 'total_ttc', 'total_ht', 'vat_amount', 'line_items']
    if not all(key in invoice_data and invoice_data[key] is not None for key in required_keys):
        # Or raise a custom exception
        raise ValueError("Invoice data is missing required fields for journal entry generation.")

    try:
        # Convert date string 'dd/mm/yyyy' to a date object
        entry_date = datetime.strptime(invoice_data['date'], '%d/%m/%Y').date()
    except (ValueError, TypeError):
        raise ValueError("Invalid date format in invoice data. Expected 'dd/mm/yyyy'.")

    # --- Create Debit Entries for each line item (Expense) ---
    for item in invoice_data['line_items']:
        account_number = CATEGORY_TO_ACCOUNT.get(item['category'], CATEGORY_TO_ACCOUNT[DEFAULT_CATEGORY])
        account_name = item['category']

        entries.append(AccountingEntry(
            entry_date=entry_date,
            account_number=account_number,
            account_name=account_name,
            description=item['description'],
            debit=item['total']
        ))

    # --- Create Debit Entry for VAT ---
    if invoice_data['vat_amount'] > 0:
        entries.append(AccountingEntry(
            entry_date=entry_date,
            account_number=TVA_DEDUCTIBLE_ACCOUNT,
            account_name="TVA Déductible",
            description=f"TVA sur facture {invoice_data.get('invoice_id', '')}",
            debit=invoice_data['vat_amount']
        ))

    # --- Create Credit Entry for the Supplier ---
    entries.append(AccountingEntry(
        entry_date=entry_date,
        account_number=FOURNISSEUR_ACCOUNT,
        account_name="Fournisseurs",
        description=f"Facture {invoice_data.get('invoice_id', '')}",
        credit=invoice_data['total_ttc']
    ))

    # --- Verification (optional but good practice) ---
    total_debits = sum(e.debit for e in entries if e.debit is not None)
    total_credits = sum(e.credit for e in entries if e.credit is not None)
    if not round(total_debits, 2) == round(total_credits, 2):
        raise ValueError("Debits and credits do not balance.")

    return entries
