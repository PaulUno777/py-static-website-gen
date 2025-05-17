import os
import shutil
from markdown_processor import markdown_to_html_node
from page_generator import generate_page

def clean_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")

def copy_static():
    if os.path.exists("static"):
        shutil.copytree(
            "static",
            "public",
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("template.html")
        )


def main():
    clean_public()
    copy_static()
    generate_page(
        from_path="content/index.md",
        template_path="static/template.html",
        dest_path="public/index.html"
    )

if __name__ == "__main__":
    main()