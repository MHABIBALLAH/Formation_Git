# src/core/accounting/categories.py

"""
Defines standard accounting categories based on the French Plan Comptable Général (PCG),
simplified for small business use.
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
