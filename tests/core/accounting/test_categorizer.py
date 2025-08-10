import unittest
from src.core.accounting.categorizer import categorize_item, DEFAULT_CATEGORY

class TestCategorizer(unittest.TestCase):

    def test_known_keyword(self):
        """Tests that a known keyword is correctly categorized."""
        description = "Facture pour service de conseil"
        expected_category = "Documentation et honoraires"
        self.assertEqual(categorize_item(description), expected_category)

    def test_no_keyword(self):
        """Tests that a description with no keywords returns the default category."""
        description = "Achat de produit XYZ"
        self.assertEqual(categorize_item(description), DEFAULT_CATEGORY)

    def test_empty_description(self):
        """Tests that an empty description returns the default category."""
        description = ""
        self.assertEqual(categorize_item(description), DEFAULT_CATEGORY)

    def test_case_insensitivity(self):
        """Tests that the matching is case-insensitive."""
        description = "Prestation de SERVICE"
        expected_category = "Prestations de services"
        self.assertEqual(categorize_item(description), expected_category)

    def test_accent_normalization(self):
        """Tests that accents are handled correctly."""
        description = "Réparation et maintenance"
        expected_category = "Entretien et réparations"
        self.assertEqual(categorize_item(description), expected_category)

    def test_multiple_keywords(self):
        """Tests that the first keyword found determines the category."""
        description = "Assurance pour la location de voiture"
        expected_category = "Primes d'assurance"
        self.assertEqual(categorize_item(description), expected_category)

if __name__ == '__main__':
    unittest.main()
