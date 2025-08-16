import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

    def test_parentnode_to_html_basic(self):
      child1 = LeafNode("p", "Paragraph 1")
      child2 = LeafNode("p", "Paragraph 2")
      parent = ParentNode("div", [child1, child2])
      self.assertEqual(
        parent.to_html(),
        "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>"
      )

    def test_parentnode_to_html_with_props(self):
      child = LeafNode("span", "child")
      parent = ParentNode("section", [child], {"class": "my-section", "id": "sec1"})
      self.assertEqual(
        parent.to_html(),
        '<section class="my-section" id="sec1"><span>child</span></section>'
      )

    def test_parentnode_to_html_no_tag_raises(self):
      child = LeafNode("p", "child")
      parent = ParentNode(None, [child])
      with self.assertRaises(ValueError):
        parent.to_html()

    def test_parentnode_to_html_no_children_raises(self):
      parent = ParentNode("div", [])
      with self.assertRaises(ValueError):
        parent.to_html()

    def test_parentnode_to_html_none_children_raises(self):
      parent = ParentNode("div", None)
      with self.assertRaises(ValueError):
        parent.to_html()

if __name__ == "__main__":
    unittest.main()