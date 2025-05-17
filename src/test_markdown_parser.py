import textwrap
import unittest
from markdown_parser import BlockType, block_to_block_type, markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    #= = = = Test cases for markdown_to_blocks function = = = =
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def test_headings_of_different_levels(self):
        """Test headings of all levels (h1-h6)"""
        md = textwrap.dedent("""\
            # Heading 1
            
            ## Heading 2
            
            ### Heading 3
            
            #### Heading 4
            
            ##### Heading 5
            
            ###### Heading 6
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
                "#### Heading 4",
                "##### Heading 5",
                "###### Heading 6"
            ]
        )
    
    def test_alternative_heading_syntax(self):
        """Test alternative heading syntax with underlines"""
        md = textwrap.dedent("""\
            Heading 1
            =========
            
            Heading 2
            ---------
            
            Paragraph after headings.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Heading 1\n=========",
                "Heading 2\n---------",
                "Paragraph after headings."
            ]
        )
    
    def test_code_blocks(self):
        """Test code blocks with language specification"""
        md = textwrap.dedent("""\
            Regular paragraph.
            
            ```python
            def hello():
                print("Hello, world!")
            ```
            
            ```html
            <div class="container">
              <p>Some HTML content</p>
            </div>
            ```
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Regular paragraph.",
                "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
                "```html\n<div class=\"container\">\n  <p>Some HTML content</p>\n</div>\n```"
            ]
        )
    
    def test_ordered_and_unordered_lists(self):
        """Test both ordered and unordered lists"""
        md = textwrap.dedent("""\
            Unordered list:
            
            - Item 1
            - Item 2
            - Item 3
            
            Ordered list:
            
            1. First item
            2. Second item
            3. Third item
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Unordered list:",
                "- Item 1\n- Item 2\n- Item 3",
                "Ordered list:",
                "1. First item\n2. Second item\n3. Third item"
            ]
        )
    
    def test_nested_lists(self):
        """Test nested lists with indentation"""
        md = textwrap.dedent("""\
            - Top level
              - Nested level 1
                - Nested level 2
            - Another top level
              1. Ordered nested
              2. Second ordered
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "- Top level\n  - Nested level 1\n    - Nested level 2\n- Another top level\n  1. Ordered nested\n  2. Second ordered"
            ]
        )
    
    def test_block_quotes(self):
        """Test block quotes with multiple paragraphs"""
        md = textwrap.dedent("""\
            > This is a blockquote
            > spanning multiple lines.
            >
            > It contains a second paragraph.
            
            Regular paragraph after blockquote.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "> This is a blockquote\n> spanning multiple lines.\n>\n> It contains a second paragraph.",
                "Regular paragraph after blockquote."
            ]
        )
    
    def test_horizontal_rules(self):
        """Test horizontal rules with different syntax"""
        md = textwrap.dedent("""\
            Paragraph before HR.
            
            ---
            
            Paragraph between HRs.
            
            ***
            
            Paragraph between HRs.
            
            ___
            
            Paragraph after HR.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Paragraph before HR.",
                "---",
                "Paragraph between HRs.",
                "***",
                "Paragraph between HRs.",
                "___",
                "Paragraph after HR."
            ]
        )
    
    def test_tables(self):
        """Test markdown tables"""
        md = textwrap.dedent("""\
            | Header 1 | Header 2 |
            |----------|----------|
            | Cell 1   | Cell 2   |
            | Cell 3   | Cell 4   |
            
            Paragraph after table.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n| Cell 3   | Cell 4   |",
                "Paragraph after table."
            ]
        )
    
    def test_html_content(self):
        """Test HTML embedded in markdown"""
        md = textwrap.dedent("""\
            Here's some regular markdown.
            
            <div class="special">
              <h2>HTML Heading</h2>
              <p>This is HTML content.</p>
            </div>
            
            Back to markdown.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Here's some regular markdown.",
                '<div class="special">\n  <h2>HTML Heading</h2>\n  <p>This is HTML content.</p>\n</div>',
                "Back to markdown."
            ]
        )
    
    def test_images_and_links(self):
        """Test blocks with images and links"""
        md = textwrap.dedent("""\
            # Page with Media
            
            Here's an image:
            
            ![Alt text](https://example.com/image.jpg "Image Title")
            
            Here are some [links](https://example.com) in a paragraph.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Page with Media",
                "Here's an image:",
                "![Alt text](https://example.com/image.jpg \"Image Title\")",
                "Here are some [links](https://example.com) in a paragraph."
            ]
        )
    
    def test_frontmatter(self):
        """Test markdown with YAML frontmatter (common in static site generators)"""
        md = textwrap.dedent("""\
            ---
            title: My Page
            date: 2023-05-16
            tags: [markdown, testing]
            ---
            
            # Page Content
            
            This is the actual content.
        """)
        
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "---\ntitle: My Page\ndate: 2023-05-16\ntags: [markdown, testing]\n---",
                "# Page Content",
                "This is the actual content."
            ]
        )
    
    def test_complex_document(self):
        """Test a complex document with multiple markdown elements"""
        md = textwrap.dedent("""\
            ---
            title: Complex Document
            ---
            
            # Main Heading
            
            Introduction paragraph with **bold** and _italic_ text.
            
            ## Section 1
            
            - List item 1
            - List item 2
              - Nested item
            
            > Important blockquote
            > with multiple lines
            
            ```javascript
            // Code example
            function example() {
                return "Hello!";
            }
            ```
            
            ## Section 2
            
            1. First step
            2. Second step
            
            ![Image](image.jpg)
            
            <div class="custom">
            Custom HTML
            </div>
            
            ---
            
            ### Conclusion
            
            Final thoughts.
        """)
        
        expected_blocks = [
            "---\ntitle: Complex Document\n---",
            "# Main Heading",
            "Introduction paragraph with **bold** and _italic_ text.",
            "## Section 1",
            "- List item 1\n- List item 2\n  - Nested item",
            "> Important blockquote\n> with multiple lines",
            "```javascript\n// Code example\nfunction example() {\n    return \"Hello!\";\n}\n```",
            "## Section 2",
            "1. First step\n2. Second step",
            "![Image](image.jpg)",
            "<div class=\"custom\">\nCustom HTML\n</div>",
            "---",
            "### Conclusion",
            "Final thoughts."
        ]
        
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    #= = = = Test cases for block_to_block_type function = = = =
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def test_paragraph(self):
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Mixed content paragraph
        block = "This paragraph has **bold** and _italic_ text and `code`."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Multi-line paragraph
        block = "This is a paragraph\nwith multiple lines\nthat should be treated as one block."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        # Test headings of different levels
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test invalid heading (no space after #)
        block = "#Invalid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test heading with formatting
        block = "## Heading with **bold** and _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_code(self):
        # Simple code block
        block = "```\nfunction test() {\n  return true;\n}\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Code block with language specification
        block = "```python\ndef test():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Invalid code block (missing closing backticks)
        block = "```\nCode without closing backticks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid code block (missing opening backticks)
        block = "Code without opening backticks\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote(self):
        # Simple quote
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Multi-line quote
        block = "> This is a multi-line quote.\n> It spans multiple lines.\n> All lines start with >."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Quote with formatting
        block = "> Quote with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Invalid quote (not all lines start with >)
        block = "> This is a quote.\nThis line doesn't start with >."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        # Simple unordered list
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Unordered list with formatting
        block = "- Item with **bold**\n- Item with _italic_\n- Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Invalid unordered list (not all lines start with -)
        block = "- Item 1\nNot an item\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid unordered list (using * instead of -)
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        # Simple ordered list
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Ordered list with formatting
        block = "1. Item with **bold**\n2. Item with _italic_\n3. Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Invalid ordered list (numbers not starting at 1)
        block = "2. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid ordered list (numbers not incrementing by 1)
        block = "1. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid ordered list (not all lines follow the pattern)
        block = "1. First item\nNot an item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_edge_cases(self):
        # Empty block
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Single character blocks
        block = "a"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Block with only special characters
        block = "###"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Block with nested markdown
        block = "- Outer list item\n  - Nested list item"
        # This should be classified according to the first line only
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Block with mixed markdown that doesn't satisfy any specific type
        block = "1. Item one\n- Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()