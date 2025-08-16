print("hello world")
from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
  new_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(new_text_node)

main()