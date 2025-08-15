import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
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
        node = HTMLNode("a", "Hello, world", None, {"href":"https://www.boot.dev", "meat":"pie"})
        self.assertEqual(
            'HTMLNode(a, Hello, world, None,  href="https://www.boot.dev" meat="pie")', repr(node)
        )

    def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

      node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
      self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

      node = LeafNode(None, "Hello, world!")
      self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()