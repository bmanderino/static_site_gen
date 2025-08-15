class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    output = ""
    for k in self.props:
      output += f' {k}="{self.props[k]}"'
    return output

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"