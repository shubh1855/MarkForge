import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


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


class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Hello World"
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><h1>Hello World</h1></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item two
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_quote(self):
        md = """
> hello
> world
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><blockquote>hello world</blockquote></div>",
        )

    def test_mixed(self):
        md = """
# Title

This is **bold** text

- item 1
- item 2
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is <b>bold</b> text</p><ul><li>item 1</li><li>item 2</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
