class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    if self.props is None:
      return ""
    output = ""
    for k in self.props:
      output += f' {k}="{self.props[k]}"'
    return output

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"


class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
    self.tag = tag
    self.value = value
    self.props = props

  def to_html(self):
    if not self.value:
      raise ValueError("invalid HTML: no value")
    if self.tag and not self.props:
      return f"<{self.tag}>{self.value}</{self.tag}>"
    elif self.tag and self.props:
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    else:
      return self.value


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)
    self.tag = tag
    self.children = children
    self.props = props

  def to_html(self):
    if not self.props:
      self.props = ""
    if not self.tag:
      raise ValueError("invalid HTML: no tag")
    if not self.children:
      raise ValueError("invalid ParentNode: no children")
    result = f'<{self.tag}{self.props_to_html()}>'

    for child in self.children:
      result += child.to_html()

    result += f'</{self.tag}>'
    return result