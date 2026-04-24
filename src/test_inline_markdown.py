import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_code_split(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[2].text, " text")

    def test_bold_split(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_no_delimiter(self):
        node = TextNode("Just text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just text")

    def test_unmatched_delimiter(self):
        node = TextNode("This is `broken text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_splits(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[1].text, "b")
        self.assertEqual(result[3].text, "d")

    def test_only_delimiter_content(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        matches = extract_markdown_images(text)

        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a [link](https://boot.dev)")
        self.assertListEqual(
            [("link", "https://boot.dev")],
            matches,
        )

    def test_extract_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        matches = extract_markdown_links(text)

        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches,
        )

    def test_links_ignore_images(self):
        text = "![img](url1) and [link](url2)"
        matches = extract_markdown_links(text)

        self.assertListEqual(
            [("link", "url2")],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
