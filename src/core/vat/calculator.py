import math
from typing import Dict, Any

def validate_invoice_totals(invoice_data: Dict[str, Any]) -> bool:
    """
    Validates the consistency of invoice totals (HT, TVA, TTC).

    Checks two things:
    1. Total HT + VAT Amount == Total TTC
    2. If a VAT rate is available, Total HT * (VAT Rate / 100) == VAT Amount

    Args:
        invoice_data: The structured data extracted from the invoice.

    Returns:
        True if the totals are consistent, False otherwise.
    """
    total_ht = invoice_data.get('total_ht')
    vat_amount = invoice_data.get('vat_amount')
    total_ttc = invoice_data.get('total_ttc')
    vat_rate = invoice_data.get('vat_rate')

    # Cannot validate if essential values are missing
    if total_ht is None or vat_amount is None or total_ttc is None:
        return False

    # 1. Check if HT + VAT = TTC
    # We use a small tolerance to handle potential floating point inaccuracies.
    if not math.isclose(total_ht + vat_amount, total_ttc, rel_tol=1e-2):
        return False

    # 2. If rate is available, check if calculated VAT matches extracted VAT
    if vat_rate is not None:
        # Avoid division by zero, although rate should not be zero.
        if vat_rate > 0:
            calculated_vat = total_ht * (vat_rate / 100)
            if not math.isclose(calculated_vat, vat_amount, rel_tol=1e-2):
                return False

    # All checks passed
    return True
