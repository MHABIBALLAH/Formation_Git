import re
from typing import Dict, List
from src.core.accounting.categories import EXPENSE_CATEGORIES, REVENUE_CATEGORIES, DEFAULT_CATEGORY

# A mapping of keywords to specific accounting categories.
# The keywords should be in lowercase and normalized (no accents).
KEYWORD_TO_CATEGORY: Dict[str, str] = {
    # Expense Keywords
    "achats de marchandises": "Achats de marchandises",
    "matieres premieres": "Achats de matières premières et fournitures",
    "fourniture": "Achats de matières premières et fournitures",
    "sous-traitance": "Sous-traitance",
    "location": "Locations",
    "loyer": "Locations",
    "entretien": "Entretien et réparations",
    "reparation": "Entretien et réparations", # Corrected this
    "assurance": "Primes d'assurance",
    "documentation": "Documentation et honoraires",
    "honoraires": "Documentation et honoraires",
    "conseil": "Documentation et honoraires",
    "transport": "Transports et déplacements",
    "deplacement": "Transports et déplacements",
    "frais postaux": "Frais postaux et télécommunications",
    "telephone": "Frais postaux et télécommunications",
    "bancaire": "Services bancaires",
    "publicite": "Publicité et relations publiques",
    "marketing": "Publicité et relations publiques",
    "impot": "Impôts et taxes",
    "taxe": "Impôts et taxes",
    "salaire": "Salaires et appointements", # Corrected from "salaires"
    "remuneration": "Salaires et appointements",
    "charges sociales": "Charges sociales",
    "charges financieres": "Charges financières",
    "interet": "Charges financières", # Corrected from "interets"

    # Revenue Keywords
    "ventes de marchandises": "Ventes de marchandises",
    "prestations de services": "Prestations de services",
    "service": "Prestations de services",
}

def _normalize_text(text: str) -> str:
    """
    Normalizes text for keyword matching by making it lowercase and removing accents.
    """
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', text)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii.lower()


def categorize_item(description: str) -> str:
    """
    Categorizes a line item based on its description using a keyword-matching system.
    It prioritizes longer keywords to find the most specific match.
    """
    if not description:
        return DEFAULT_CATEGORY

    normalized_desc = _normalize_text(description)

    sorted_keywords = sorted(KEYWORD_TO_CATEGORY.keys(), key=len, reverse=True)

    for keyword in sorted_keywords:
        if keyword in normalized_desc:
            return KEYWORD_TO_CATEGORY[keyword]

    return DEFAULT_CATEGORY
