import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_multiple_image(self):
        node = TextNode("![a](u1) middle ![b](u2)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "a")
        self.assertEqual(result[2].text, "b")

    def test_no_image(self):
        node = TextNode("just text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_links_and_images(self):
        node = TextNode(
            "text ![img](url1) and [link](url2)",
            TextType.TEXT,
        )

        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)

        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].text_type, TextType.LINK)

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text(self):
        text = "just normal text"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [TextNode("just normal text", TextType.TEXT)],
        )

    def test_only_bold(self):
        text = "**bold**"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [TextNode("bold", TextType.BOLD)],
        )

    def test_mixed_types(self):
        text = "`code` and **bold**"
        nodes = text_to_textnodes(text)

        self.assertEqual(nodes[0].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text_type, TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
