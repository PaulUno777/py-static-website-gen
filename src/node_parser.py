import re
from html_node import LeafNode, ParentNode
from markdown_node_splitter import (split_nodes_delimiter, split_nodes_image, split_nodes_link)
from text_node import TextNode, TextType

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode based on its type.
    
    Args:
        text_node: A TextNode object
        
    Returns:
        A HTMLNode object representing the HTML equivalent of the TextNode
        
    Raises:
        ValueError: If the TextNode has an unsupported type
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
        
def text_to_children(text):
    """
    Convert a text string to a list of HTMLNode objects.
    
    Args:
        text: A string containing the text to convert
        
    Returns:
        A list of HTMLNode objects representing the HTML equivalent of the text
    """
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def paragraph_to_html_node(text):
    """
    Convert a paragraph string to an HTMLNode object.
    
    Args:
        text: A string containing the paragraph text
        
    Returns:
        A ParentNode object representing the HTML equivalent of the paragraph
    """
    lines = text.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(text):
    level = 0
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(text):
        raise ValueError("Invalid heading format")
    text = text[level + 1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(text):
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("invalid code block")
    text_code = text[4:-3].strip()
    raw_text_node = TextNode(text_code, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])

def quote_to_html_node(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def list_to_html_node(text, ordered=False):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    list_tag = "ol" if ordered else "ul"
    list_node = ParentNode(list_tag, [])
    
    for i, line in enumerate(lines):
        if ordered:
            match = re.match(r"(\d+)\.\s+(.*)", line)
            if not match:
                raise ValueError(f"Invalid ordered list item: '{line}'")
            index, content = int(match.group(1)), match.group(2)
            if index != i + 1:
                raise ValueError(f"Ordered list must increment properly: got {index}, expected {i + 1}")
        else:
            if not line.startswith("- "):
                raise ValueError(f"Invalid unordered list item: '{line}'")
            content = line[2:]

        children = text_to_children(content)
        list_node.children.append(ParentNode("li", children))
    return list_node
