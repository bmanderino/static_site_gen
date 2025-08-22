import unittest

from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestTextNode(unittest.TestCase):
  def test_split_textnode(self):
    new_nodes = split_nodes_delimiter([TextNode("Hello, World", TextType.IMAGE)], "*", TextType.BOLD)
    self.assertEqual(new_nodes, [TextNode("Hello, World", TextType.IMAGE)])

    new_nodes = split_nodes_delimiter([TextNode("Hello, World", TextType.TEXT)], "*", TextType.BOLD)
    self.assertEqual(new_nodes, [TextNode("Hello, World", TextType.TEXT)])

    new_nodes = split_nodes_delimiter([TextNode("Hello, *World*", TextType.TEXT)], "*", TextType.BOLD)
    self.assertEqual(new_nodes, [TextNode("Hello, ", TextType.TEXT), TextNode("World", TextType.BOLD)])

  def test_image_tuple_list(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    result = extract_markdown_images(text)
    self.assertListEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

  def test_link_tuple_list(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    result = extract_markdown_links(text)
    self.assertListEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube","https://www.youtube.com/@bootdotdev")])

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    node = TextNode("This is text with no images!", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("This is text with no images!", TextType.TEXT)], new_nodes)

  def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
    )


  def test_text_to_textnodes(self):
    result = text_to_textnodes(
      "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
      )
    self.assertListEqual(result,[
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
])

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

if __name__ == "__main__":
    unittest.main()