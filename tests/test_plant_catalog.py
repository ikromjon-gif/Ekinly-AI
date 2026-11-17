import unittest

from plant_catalog import TEXTS, class_names, descriptions, get_pretty_name


class PlantCatalogTests(unittest.TestCase):
    def test_catalog_has_38_unique_classes_and_descriptions(self):
        self.assertEqual(len(class_names), 38)
        self.assertEqual(len(set(class_names)), 38)
        self.assertEqual(set(class_names), set(descriptions))

    def test_ui_text_is_available_in_all_supported_languages(self):
        self.assertEqual(set(TEXTS), {"english", "korean", "uzbek"})
        required_keys = {"title", "plant_leaf", "detect_btn", "diagnosis_title"}
        for language in TEXTS.values():
            self.assertTrue(required_keys.issubset(language))

    def test_pretty_name_conversion(self):
        self.assertEqual(
            get_pretty_name("Tomato___Early_blight"),
            "Tomato - Early blight",
        )


if __name__ == "__main__":
    unittest.main()
