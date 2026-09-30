import os
import shutil
import sys

from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode
from textnode import TextNode, TextType


def copy_all(source_directory: str, destination_directory: str):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.mkdir(destination_directory)

    for item_name in os.listdir(source_directory):
        source_path = os.path.join(source_directory, item_name)
        destination_path = os.path.join(destination_directory, item_name)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_all(source_path, destination_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_string = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    os.makedirs(dest_dir_path, exist_ok=True)

    for entry_name in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry_name)
        destination_path = os.path.join(dest_dir_path, entry_name)

        if os.path.isfile(source_path):
            if entry_name.endswith(".md"):
                html_path = os.path.splitext(destination_path)[0] + ".html"
                generate_page(source_path, template_path, html_path,basepath)
        else:
            generate_pages_recursive(source_path, template_path, destination_path,basepath)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_all("static", "docs")
    generate_pages_recursive("content", "template.html", "docs",basepath)
    


if __name__ == "__main__":
    main()
