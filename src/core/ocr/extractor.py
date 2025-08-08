import re
from typing import Dict, Any, Optional, List
from src.core.accounting.categorizer import categorize_item

def _search_pattern(text: str, pattern: str, group: int = 1) -> Optional[str]:
    """Helper function to search for a regex pattern and return a specific group."""
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(group).strip()
    return None

def _parse_amount(amount_str: Optional[str]) -> Optional[float]:
    """Helper function to parse a string amount into a float."""
    if amount_str is None:
        return None
    cleaned_str = amount_str.replace(' ', '').replace(',', '.')
    try:
        return float(cleaned_str)
    except (ValueError, TypeError):
        return None

def _parse_line_items(text: str) -> List[Dict[str, Any]]:
    """
    Parses the line items from the invoice's OCR text using a robust regex.
    """
    items = []
    table_match = re.search(r"Description\s*\|.*?\n(.*?)Total HT:", text, re.DOTALL | re.IGNORECASE)

    if not table_match:
        return items

    table_text = table_match.group(1)
    lines = table_text.strip().split('\n')

    line_pattern = re.compile(r"^(.*?)\s*?(\d+)\s*.*?([\d,]+\.\d{2})\s*\|?\s*([\d,]+\.\d{2})$")

    for line in lines:
        match = line_pattern.search(line)
        if match:
            description = match.group(1).replace('|', '').strip()
            quantity = int(match.group(2))
            unit_price = _parse_amount(match.group(3))
            total = _parse_amount(match.group(4))

            category = categorize_item(description)

            items.append({
                "description": description,
                "category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total
            })
    return items


def extract_invoice_data(text: str) -> Dict[str, Any]:
    """
    Extracts structured data from raw OCR text using regular expressions.
    """
    patterns = {
        'invoice_id': r"FACTURE N°:\s*(\S+)",
        'date': r"Date:\s*(\d{2}/\d{2}/\d{4})",
        'total_ht': r"Total HT:\s*([\d\s,.]+)",
        'total_ttc': r"Total TTC:\s*([\d\s,.]+)"
    }

    raw_data = {key: _search_pattern(text, pat) for key, pat in patterns.items()}

    # Custom handling for VAT to extract both rate and amount
    vat_rate = None
    vat_amount_str = None
    vat_pattern = r"TVA\s*\(?\s*(\d+\.?\d*)\s*%\s*\)?:\s*([\d\s,.]+)"
    vat_match = re.search(vat_pattern, text, re.IGNORECASE)
    if vat_match:
        vat_rate = _parse_amount(vat_match.group(1))
        vat_amount_str = vat_match.group(2)
    else:
        # Fallback to old pattern if rate is not found, just get the amount
        vat_amount_str = _search_pattern(text, r"TVA:\s*([\d\s,.]+)")

    line_items = _parse_line_items(text)

    data = {
        'invoice_id': raw_data.get('invoice_id'),
        'date': raw_data.get('date'),
        'total_ht': _parse_amount(raw_data.get('total_ht')),
        'vat_rate': vat_rate,
        'vat_amount': _parse_amount(vat_amount_str),
        'total_ttc': _parse_amount(raw_data.get('total_ttc')),
        'line_items': line_items
    }

    return data
