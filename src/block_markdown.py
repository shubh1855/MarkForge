from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    raise ValueError("invalid block type")


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = 0
    for c in block:
        if c == "#":
            level += 1
        else:
            break

    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]

    raw = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw)

    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    children = []

    for item in items:
        text = item.split(". ", 1)[1]
        children.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ol", children)


def ulist_to_html_node(block):
    items = block.split("\n")
    children = []

    for item in items:
        text = item[2:]
        children.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ul", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned = []

    for line in lines:
        cleaned.append(line.lstrip(">").strip())

    text = " ".join(cleaned)
    return ParentNode("blockquote", text_to_children(text))
