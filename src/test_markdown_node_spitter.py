import unittest
from markdown_node_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from text_node import TextNode, TextType

class TestMarkdownNodeSplitter(unittest.TestCase):
    def test_single_code_block(self):
        node = TextNode("Text with `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_blocks(self):
        node = TextNode("**bold** and **strong**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_unmatched_delimiter(self):
        node = TextNode("This is `broken markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_mixed_nodes(self):
        node1 = TextNode("This is `code`", TextType.TEXT)
        node2 = TextNode("Bold", TextType.BOLD)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            node2
        ]
        self.assertEqual(result, expected)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "Check this [site](https://example.com) and [repo](https://github.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("repo", TextType.LINK, "https://github.com"),
            ],
            new_nodes
        )

    def test_no_images(self):
        node = TextNode("No images here.", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_no_links(self):
        node = TextNode("No links here.", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_mixed_non_text_node(self):
        node = TextNode("image", TextType.IMAGE, "https://img.com")
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])

if __name__ == "__main__":
    unittest.main()