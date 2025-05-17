import unittest
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_with_whitespace(self):
        md = "   #   Hello    "
        self.assertEqual(extract_title(md), "Hello")

    def test_no_title_raises(self):
        md = "This has no title"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_ignores_h2_h3(self):
        md = "## Not a title\n### Still not a title"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()