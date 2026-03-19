from enum import Enum



from htmlnode import *
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        if url == None:
            self.url = None
        else: self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else: return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if TextType.TEXT == text_node.text_type:
        return LeafNode(None, text_node.text)
    elif TextType.BOLD == text_node.text_type:
        return LeafNode("b", text_node.text)
    elif TextType.ITALIC == text_node.text_type:
        return LeafNode("i", text_node.text)
    elif TextType.CODE == text_node.text_type:
        return LeafNode("code", text_node.text)
    elif TextType.LINK == text_node.text_type:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif TextType.IMAGE == text_node.text_type:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else: raise ValueError(f"invalid text type: {text_node.text_type}")

