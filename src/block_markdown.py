from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    cleaned_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            cleaned_blocks.append(stripped)

    return cleaned_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST
