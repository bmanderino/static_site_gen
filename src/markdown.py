import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue
      split_nodes = []
      sections = old_node.text.split(delimiter)
      if len(sections) % 2 == 0:
          raise ValueError("invalid markdown, formatted section not closed")
      for i in range(len(sections)):
          if sections[i] == "":
              continue
          if i % 2 == 0:
              split_nodes.append(TextNode(sections[i], TextType.TEXT))
          else:
              split_nodes.append(TextNode(sections[i], text_type))
      new_nodes.extend(split_nodes)
  return new_nodes



def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            #We expect ONLY TextType.TEXT. If we got some other "type", just add it to the list so it can be returned, as is

        text = node.text #reference the text with less typing
        matches = extract_markdown_images(text) #helper function returns a list of tuples
        if not matches:
            new_nodes.append(node)
            continue
            #If there are no results from the helper function, then there are no images in the text. Save it and move on.

        cursor = 0 #setting a starting position
        for alt, url in matches: #loop through our helper function results
            token = f"![{alt}]({url})" #regex to ruturn this specific image in the iteration of the loop
            k = text.find(token, cursor) #find the index of the beginning of our image
            if k == -1:
                # Defensive: if not found, bail out by appending the rest as text
                break
            before = text[cursor:k] #create a substring of anything before our image, starting at the cursor position (which moves as the loop progresses)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT)) #if it exists, it must be text, so append a text node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url)) #now append our image
            cursor = k + len(token) #update the cursor to the end of our imgage

        tail = text[cursor:] #after the loop, whatever remains, if anything, must be text
        if tail:
            new_nodes.append(TextNode(tail, TextType.TEXT)) #append the text
    return new_nodes #return everything


def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
      if node.text_type != TextType.TEXT:
          new_nodes.append(node)
          continue

      text = node.text
      matches = extract_markdown_links(text)
      if not matches:
          new_nodes.append(node)
          continue

      cursor = 0
      for alt, url in matches:
          token = f"[{alt}]({url})"
          k = text.find(token, cursor)
          if k == -1:
              break
          if k > 0 and text[k - 1] == '!': #if there's an !, it's an image, not a link. Move on
              cursor = k + 1
              continue
          before = text[cursor:k]
          if before:
              new_nodes.append(TextNode(before, TextType.TEXT))
          new_nodes.append(TextNode(alt, TextType.LINK, url))
          cursor = k + len(token)

      tail = text[cursor:]
      if tail:
          new_nodes.append(TextNode(tail, TextType.TEXT))
  return new_nodes


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    bolded = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    italiced = split_nodes_delimiter(bolded, "_", TextType.ITALIC)
    coded = split_nodes_delimiter(italiced, "`", TextType.CODE)
    imaged = split_nodes_image(coded)
    return split_nodes_link(imaged)


def markdown_to_blocks(markdown):
    result = []
    split_content = markdown.split("\n\n")
    for content in split_content:
        if not content:
            continue
        result.append(content.strip())
    return result