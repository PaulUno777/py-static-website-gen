import textwrap
from html_node import ParentNode
from markdown_parser import BlockType, block_to_block_type, markdown_to_blocks
from node_parser import code_to_html_node, heading_to_html_node, list_to_html_node, paragraph_to_html_node, quote_to_html_node, text_node_to_html_node, text_to_text_nodes


def markdown_to_html_node(markdown):
    """
    Convert a markdown string to an HTML node representation.
    
    Args:
        markdown (str): The markdown string to convert.
        
    Returns:
        ParentNode: The root node of the HTML representation.
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(textwrap.dedent(markdown))
    
    # Create a parent node to hold all blocks
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
        
    return ParentNode("div", children, props={"class": "markdown-body"})

def block_to_html_node(block):
    """
    Convert a markdown block to an HTML node representation.
    
    Args:
        block (str): The markdown block to convert.
        
    Returns:
        ParentNode: The HTML node representation of the block.
    """
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    
    elif block_type == BlockType.UNORDERED_LIST:
        return list_to_html_node(block)
    
    elif block_type == BlockType.ORDERED_LIST:
        return list_to_html_node(block, ordered=True)
    
    raise ValueError(f"Unsupported block type: {block_type}")