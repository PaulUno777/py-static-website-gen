from enum import Enum
import re


def markdown_to_blocks(markdown):
    """
    Split markdown string into blocks based on one or more blank lines.
    A block is a section of text separated by one or more blank lines.
    """
    # Normalize line endings and strip leading/trailing whitespace
    markdown = markdown.strip()

    # Use regex to split on 2+ newlines (including lines that may contain spaces/tabs)
    raw_blocks = re.split(r'\n\s*\n', markdown)

    # Trim each block
    return [block.strip() for block in raw_blocks if block.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Determine the type of markdown block based on its content.
    
    Args:
        block (str): A single block of markdown text (already stripped of leading/trailing whitespace)
        
    Returns:
        BlockType: The type of the markdown block
    """
    # Check if it's a heading
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check if it's a code block
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # Check if it's a quote block
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check if it's an unordered list
    if all(line.strip().startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check if it's an ordered list
    # First, check if all lines start with a number followed by a period and space
    if all(re.match(r'^\d+\. ', line.strip()) for line in lines):
        # Then check if the numbers start at 1 and increment by 1
        numbers = [int(re.match(r'^(\d+)\. ', line.strip()).group(1)) for line in lines]
        expected_numbers = list(range(1, len(numbers) + 1))
        if numbers == expected_numbers:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph if none of the above conditions are met
    return BlockType.PARAGRAPH