import unittest

from markdown_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![one](url1) text ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Some links: [Google](https://google.com) and [GitHub](https://github.com)"
        )
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ], matches)

    def test_ignore_image_in_links(self):
        text = "This is a link: [hello](http://example.com) and image ![pic](img.png)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("hello", "http://example.com")])

    def test_no_matches(self):
        self.assertEqual(extract_markdown_images("Just text"), [])
        self.assertEqual(extract_markdown_links("Just text"), [])

if __name__ == "__main__":
    unittest.main()