# src/core/accounting/categories.py

"""
Defines standard accounting categories and their corresponding account numbers
based on the French Plan Comptable Général (PCG), simplified for small business use.
"""

EXPENSE_CATEGORIES = [
    "Achats de marchandises",
    "Achats de matières premières et fournitures",
    "Sous-traitance",
    "Locations",
    "Entretien et réparations",
    "Primes d'assurance",
    "Documentation et honoraires",
    "Transports et déplacements",
    "Frais postaux et télécommunications",
    "Services bancaires",
    "Publicité et relations publiques",
    "Impôts et taxes",
    "Salaires et appointements",
    "Charges sociales",
    "Charges financières",
    "Autres charges",
]

REVENUE_CATEGORIES = [
    "Ventes de produits finis",
    "Prestations de services",
    "Ventes de marchandises",
    "Produits financiers",
    "Subventions d'exploitation",
    "Autres produits",
]

# A default category for items that cannot be classified
DEFAULT_CATEGORY = "Autres"

# Mapping from our simplified categories to official PCG account numbers
CATEGORY_TO_ACCOUNT = {
    # Expense Accounts (Class 6)
    "Achats de marchandises": 607,
    "Achats de matières premières et fournitures": 606,
    "Sous-traitance": 611,
    "Locations": 613,
    "Entretien et réparations": 615,
    "Primes d'assurance": 616,
    "Documentation et honoraires": 622,
    "Transports et déplacements": 625,
    "Frais postaux et télécommunications": 626,
    "Services bancaires": 627,
    "Publicité et relations publiques": 623,
    "Impôts et taxes": 635,
    "Salaires et appointements": 641,
    "Charges sociales": 645,
    "Charges financières": 661,
    "Autres charges": 658,

    # Revenue Accounts (Class 7)
    "Ventes de produits finis": 701,
    "Prestations de services": 706,
    "Ventes de marchandises": 707,
    "Produits financiers": 768,
    "Subventions d'exploitation": 740,
    "Autres produits": 758,

    # Default/Other
    DEFAULT_CATEGORY: 658 # Default to "Autres charges de gestion courante"
}
