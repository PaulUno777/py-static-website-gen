import unittest
from html_node import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
        
        # Test with None props explicitly
        node = HTMLNode("p", "Hello, world!", props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode("a", "Click me", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(
            "a", 
            "Click me", 
            props={
                "href": "https://www.example.com", 
                "target": "_blank", 
                "class": "button"
            }
        )
        # Create a set of expected parts because the order of attributes can vary
        expected_parts = {
            ' href="https://www.example.com"',
            ' target="_blank"',
            ' class="button"'
        }
        
        # Check that each expected part is in the result
        result = node.props_to_html()
        for part in expected_parts:
            self.assertIn(part, result)
        
        # Check the result starts with a space and has the correct total length
        self.assertTrue(result.startswith(' '))
        self.assertEqual(len(result), sum(len(part) for part in expected_parts))
    
    def test_to_html_not_implemented(self):
        # Test that to_html raises NotImplementedError
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_repr(self):
        # Test the __repr__ method
        node = HTMLNode("div", "Content", props={"class": "container"})
        expected = 'HTMLNode(tag=div, value=Content, children=None, props={\'class\': \'container\'})'
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        result = parent_node.to_html()
        
        # Check parts since attribute order may vary
        self.assertTrue(result.startswith("<div"))
        self.assertTrue(result.endswith("><span>child</span></div>"))
        self.assertIn(' class="container"', result)
        self.assertIn(' id="main"', result)
    
    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("must have a tag", str(context.exception))
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("must have children", str(context.exception))
    
    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    
    def test_to_html_complex_nesting(self):
        # Create a more complex nested structure
        # <div>
        #   <header><h1>Title</h1></header>
        #   <main>
        #     <p><b>Bold text</b> Normal text</p>
        #     <p>Another paragraph</p>
        #   </main>
        #   <footer>Footer text</footer>
        # </div>
        
        title = LeafNode("h1", "Title")
        header = ParentNode("header", [title])
        
        p1_children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, " Normal text")
        ]
        p1 = ParentNode("p", p1_children)
        
        p2 = ParentNode("p", [LeafNode(None, "Another paragraph")])
        
        main = ParentNode("main", [p1, p2])
        
        footer = ParentNode("footer", [LeafNode(None, "Footer text")])
        
        page = ParentNode("div", [header, main, footer])
        
        expected = "<div><header><h1>Title</h1></header><main><p><b>Bold text</b> Normal text</p><p>Another paragraph</p></main><footer>Footer text</footer></div>"
        
        self.assertEqual(page.to_html(), expected)

if __name__ == "__main__":
    unittest.main()