import os
import shutil
import sys
from page_generator import  generate_pages_recursive

def clean_public(clean_dir="public"):
    """
    Clean the public directory by removing it and creating a new one.
    """
    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
    os.makedirs(clean_dir)

def copy_static(dest_dir="public"):
    """
    Copy static files to the public directory.
    """
    if os.path.exists("static"):
        for item in os.listdir("static"):
            if item == "template.html":
                continue  # skip template
            s = os.path.join("static", item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir =  sys.argv[2] if len(sys.argv) > 2 else "public"

    clean_public(dest_dir)
    copy_static(dest_dir)
    generate_pages_recursive("content", "static/template.html", dest_dir, base_path)

if __name__ == "__main__":
    main()