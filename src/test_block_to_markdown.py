import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_input(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), [])

    def test_extra_newlines(self):
        md = "\n\nHello\n\n\nWorld\n\n"
        self.assertEqual(markdown_to_blocks(md), ["Hello", "World"])


class TestBlockTypes(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_code(self):
        block = "```\ncode here\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote(self):
        block = "> quote\n> another line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        block = "- item1\n- item2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_paragraph(self):
        block = "Just a normal paragraph"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_invalid_ordered_list(self):
        block = "1. first\n3. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
