# src/core/vat/rates.py

"""
Defines the standard VAT (TVA) rates applicable in France.
These values are based on standard rates and should be verified for specific use cases.
"""

# Taux Normal (Standard Rate)
VAT_RATE_NORMAL = 20.0

# Taux Intermédiaire (Intermediate Rate)
VAT_RATE_INTERMEDIATE = 10.0

# Taux Réduit (Reduced Rate)
VAT_RATE_REDUCED = 5.5

# Taux Super-Réduit (Super-Reduced Rate)
VAT_RATE_SUPER_REDUCED = 2.1

# A dictionary to hold all rates for easy access
VAT_RATES = {
    "normal": VAT_RATE_NORMAL,
    "intermediate": VAT_RATE_INTERMEDIATE,
    "reduced": VAT_RATE_REDUCED,
    "super_reduced": VAT_RATE_SUPER_REDUCED,
}
