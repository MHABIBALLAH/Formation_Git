from typing import List, Dict, Any

def generate_financial_summary(invoices: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Generates a financial summary from a list of processed invoice data.

    For now, this assumes all invoices are purchase invoices (expenses).

    Args:
        invoices: A list of invoice data dictionaries.

    Returns:
        A dictionary containing summary metrics.
    """
    total_expenses_ht = 0.0
    total_vat_deductible = 0.0
    total_expenses_ttc = 0.0

    for invoice in invoices:
        # We only consider invoices that have been successfully processed
        if invoice.get('total_ht') is not None:
            total_expenses_ht += invoice['total_ht']
        if invoice.get('vat_amount') is not None:
            total_vat_deductible += invoice['vat_amount']
        if invoice.get('total_ttc') is not None:
            total_expenses_ttc += invoice['total_ttc']

    # In the future, we would also process revenues and calculate profit/loss
    summary = {
        "total_expenses_ht": round(total_expenses_ht, 2),
        "total_vat_deductible": round(total_vat_deductible, 2),
        "total_expenses_ttc": round(total_expenses_ttc, 2),
        "total_revenue": 0.0, # Placeholder
        "net_profit_loss": round(0 - total_expenses_ht, 2) # Placeholder
    }

    return summary
