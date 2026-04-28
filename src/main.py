import os
import sys
import shutil
from block_markdown import markdown_to_html_node


def copy_static(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    _copy_recursive(src, dest)


def _copy_recursive(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} → {dest_path}")
            shutil.copy(src_path, dest_path)

        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_recursive(src_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath):
    for item in os.listdir(content_dir):
        src_path = os.path.join(content_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                html_dest = dest_path.replace(".md", ".html")
                generate_page(src_path, template_path, html_dest, basepath)

        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No H1 header found")


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static("static", "docs")
    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath,
    )


if __name__ == "__main__":
    main()
