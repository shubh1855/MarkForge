from textnode import TextNode, TextType
from textnode import text_node_to_html_node
import unittest


class TestTextNodeToHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")

    def test_code(self):
        node = TextNode("code()", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://google.com")

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.com")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://img.com")
        self.assertEqual(html_node.props["alt"], "alt text")

    def test_rendered_nodes_escape_html(self):
        text_node = TextNode("<script>", TextType.TEXT)
        link_node = TextNode("Click <here>", TextType.LINK, 'https://x.com?a=1&b="2"')
        image_node = TextNode('alt "text"', TextType.IMAGE, "https://img.com?q=1&x=2")

        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            "&lt;script&gt;",
        )
        self.assertEqual(
            text_node_to_html_node(link_node).to_html(),
            '<a href="https://x.com?a=1&amp;b=&quot;2&quot;">Click &lt;here&gt;</a>',
        )
        self.assertEqual(
            text_node_to_html_node(image_node).to_html(),
            '<img src="https://img.com?q=1&amp;x=2" alt="alt &quot;text&quot;">',
        )

    def test_invalid_type(self):
        class FakeType:
            pass

        node = TextNode("oops", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
