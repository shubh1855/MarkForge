import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me</a>')

    def test_leaf_to_html_escapes_text(self):
        node = LeafNode("p", '5 < 7 & "ok"')
        self.assertEqual(node.to_html(), "<p>5 &lt; 7 &amp; &quot;ok&quot;</p>")

    def test_leaf_to_html_escapes_plain_text(self):
        node = LeafNode(None, "x < y & z")
        self.assertEqual(node.to_html(), "x &lt; y &amp; z")

    def test_props_to_html_escapes_attributes(self):
        node = HTMLNode("a", "Hello", None, {"href": 'https://x.com?a=1&b="2"'})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://x.com?a=1&amp;b=&quot;2&quot;"',
        )

    def test_img_renders_as_void_element(self):
        node = LeafNode("img", "", {"src": "/img.png", "alt": 'A "quote"'})
        self.assertEqual(
            node.to_html(),
            '<img src="/img.png" alt="A &quot;quote&quot;">',
        )

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'class': 'text'})")

    def test_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_missing_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_missing_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold"),
                        LeafNode(None, " text"),
                    ],
                )
            ],
        )
        self.assertEqual(node.to_html(), "<div><p><b>Bold</b> text</p></div>")


if __name__ == "__main__":
    unittest.main()
