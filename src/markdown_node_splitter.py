from markdown_extractors import extract_markdown_images, extract_markdown_links
from text_node import TextNode, TextType

# Supported delimiters for inline markdown styling
SUPPORTED_DELIMITERS = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in SUPPORTED_DELIMITERS:
        raise ValueError(f"Unsupported delimiter: {delimiter}")
    
    if SUPPORTED_DELIMITERS[delimiter] != text_type:
        raise ValueError(f"Delimiter '{delimiter}' does not match TextType '{text_type}'")

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        parts = text.split(delimiter)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid delimiter usage in: {text}")

        for i, part in enumerate(parts):
            if part == "":
                continue  # Skip empty parts caused by leading/trailing delimiter
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt_text, url in matches:
            parts = text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = parts[1]
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for anchor_text, url in matches:
            parts = text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes