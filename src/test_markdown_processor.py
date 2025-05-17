import textwrap
import unittest
from html_node import HTMLNode
from markdown_processor import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><p>This is <b>bolded</b> paragraph text in a p tag here</p>'
            '<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>',
        )

    def test_codeblock(self):
        md = textwrap.dedent("""\
            ```
            def hello_world():
                print("Hello, world!")
            ```
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><pre><code>def hello_world():\n    print("Hello, world!")</code></pre></div>',
        )

    def test_headings(self):
        md = textwrap.dedent("""\
            # Heading 1

            ## Heading 2

            ### Heading 3 with **bold**
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3></div>',
        )

    def test_blockquote(self):
        md = textwrap.dedent("""\
            > This is a blockquote
            > with multiple lines
            > and **formatting**
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><blockquote>This is a blockquote with multiple lines and <b>formatting</b></blockquote></div>',
        )

    def test_unordered_list(self):
        md = textwrap.dedent("""\
            - Item 1
            - Item 2 with **bold**
            - Item 3 with _italic_
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3 with <i>italic</i></li></ul></div>',
        )

    def test_ordered_list(self):
        md = textwrap.dedent("""\
            1. First item
            2. Second item with **bold**
            3. Third item with _italic_
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div class="markdown-body"><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ol></div>',
        )

    def test_mixed_content(self):
        md = textwrap.dedent("""\
            # Mixed Markdown Document

            This is a paragraph with **bold** and _italic_ text.

            ## Subheading

            - List item 1
            - List item 2

            > This is a blockquote
            > with multiple lines

            ```
            This is a code block
            with multiple lines
            ```

            1. Ordered item 1
            2. Ordered item 2
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = '<div class="markdown-body">' + \
            '<h1>Mixed Markdown Document</h1>' + \
            '<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>' + \
            '<h2>Subheading</h2>' + \
            '<ul><li>List item 1</li><li>List item 2</li></ul>' + \
            '<blockquote>This is a blockquote with multiple lines</blockquote>' + \
            '<pre><code>This is a code block\nwith multiple lines\n</code></pre>' + \
            '<ol><li>Ordered item 1</li><li>Ordered item 2</li></ol>' + \
            '</div>'
        self.assertIn('<div class="markdown-body">', html)
        self.assertIn("</div>", html)
        self.assertIn("<h1>Mixed Markdown Document</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<h2>Subheading</h2>", html)
        self.assertIn("<ul><li>List item 1</li><li>List item 2</li></ul>", html)
        self.assertIn("<blockquote>This is a blockquote with multiple lines</blockquote>", html)
        self.assertIn("<pre><code>This is a code block\nwith multiple lines</code></pre>", html)
        self.assertIn("<ol><li>Ordered item 1</li><li>Ordered item 2</li></ol>", html)
           

    def test_empty_document(self):
        node = markdown_to_html_node("")
        html = node.to_html()
        self.assertEqual(html, '<div class="markdown-body"></div>')

    def test_nested_formatting(self):
        md = textwrap.dedent("""\
            This paragraph has **bold with _italic_ inside** and `code` elements.
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn('<div class="markdown-body"><p>', html)
        self.assertIn("</p></div>", html)
        self.assertIn("<b>", html)
        self.assertIn("<code>", html)

if __name__ == "__main__":
    unittest.main()