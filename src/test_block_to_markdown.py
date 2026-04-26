import unittest
from block_markdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
