import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_test(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_equal(self):
        node = TextNode("hello", TextType.TEXT, url="example.com")
        node2 = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_textype_not_equal(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
