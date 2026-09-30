import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extracts_h1_title(self):
        markdown = "# My page title\n\nSome paragraph text."
        self.assertEqual(extract_title(markdown), "My page title")

    def test_ignores_lower_level_headings(self):
        markdown = "## A subtitle\n\n# Main title\n\n### Another subtitle"
        self.assertEqual(extract_title(markdown), "Main title")

    def test_raises_error_when_h1_is_missing(self):
        markdown = "## Only a subtitle\n\nThis document has no h1."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_strips_title_whitespace(self):
        markdown = "#   A title with extra spaces   "
        self.assertEqual(extract_title(markdown), "A title with extra spaces")


if __name__ == "__main__":
    unittest.main()
