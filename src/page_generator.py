import os
from markdown_processor import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extract the H1 title from a markdown string.

    Args:
        markdown (str): The markdown content.

    Returns:
        str: The title string without the '#'.

    Raises:
        ValueError: If no H1 header is found.
    """
    for line in markdown.splitlines():
        if line.strip().startswith("# "):  # Only h1, not ## or ###
            return line.strip()[2:].strip()
    raise ValueError("No H1 header found in markdown.")

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Fix href/src paths for GitHub Pages subdirectory deployment
    page = page.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                
                # Compute relative path from content/ root
                relative_path = os.path.relpath(from_path, dir_path_content)
                
                # Change .md to .html
                dest_relative_path = os.path.splitext(relative_path)[0] + ".html"
                
                # Final destination path inside public/
                dest_path = os.path.join(dest_dir_path, dest_relative_path)

                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Generate the page
                generate_page(from_path, template_path, dest_path, base_path)