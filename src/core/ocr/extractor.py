import re
from typing import Dict, Any, Optional

def _search_pattern(text: str, pattern: str, group: int = 1) -> Optional[str]:
    """Helper function to search for a regex pattern and return a specific group."""
    # Using re.MULTILINE to handle patterns that may be at the start of a line
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(group).strip()
    return None

def _parse_amount(amount_str: Optional[str]) -> Optional[float]:
    """Helper function to parse a string amount into a float."""
    if amount_str is None:
        return None
    # Remove spaces, replace comma with dot for float conversion
    # Handles cases like "1 000.00" or "1,000.00"
    cleaned_str = amount_str.replace(' ', '').replace(',', '.')
    try:
        return float(cleaned_str)
    except (ValueError, TypeError):
        return None

def extract_invoice_data(text: str) -> Dict[str, Any]:
    """
    Extracts structured data from raw OCR text using regular expressions.
    """

    # Define patterns for each piece of data
    patterns = {
        'invoice_id': r"FACTURE N°:\s*(\S+)",
        'date': r"Date:\s*(\d{2}/\d{2}/\d{4})",
        'total_ht': r"Total HT:\s*([\d\s,.]+)",
        'vat_amount': r"TVA\s*(?:\(\s*\d+\s*%\))?:\s*([\d\s,.]+)", # Makes percentage optional
        'total_ttc': r"Total TTC:\s*([\d\s,.]+)"
    }

    # Extract raw string data
    raw_data = {key: _search_pattern(text, pat) for key, pat in patterns.items()}

    # Structure and parse the final data
    data = {
        'invoice_id': raw_data.get('invoice_id'),
        'date': raw_data.get('date'),
        'total_ht': _parse_amount(raw_data.get('total_ht')),
        'vat_amount': _parse_amount(raw_data.get('vat_amount')),
        'total_ttc': _parse_amount(raw_data.get('total_ttc'))
    }

    return data
