import re

def extract_markdown_images(text):
    """
    Extract all markdown images from text and return a list of tuples
    containing the alt text and URL for each image.
    
    Args:
        text (str): The markdown text to parse
        
    Returns:
        List[Tuple[str, str]]: List of (alt_text, url) tuples
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extract all markdown links from text and return a list of tuples
    containing the text and URL for each link.
    
    Args:
        text (str): The markdown text to parse
        
    Returns:
        List[Tuple[str, str]]: List of (text, url) tuples
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

