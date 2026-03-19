from textnode import *

import re

from extract_markdown import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Syntax, formatted section not closed")
        for i in range (0, len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            elif i % 2 == 1:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extract = extract_markdown_images(old_node.text)
        if len(extract) == 0: 
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        for ext in extract:
            image_alt, image_link = ext
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE,image_link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extract = extract_markdown_links(old_node.text)
        if len(extract) == 0: 
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        for ext in extract:
            link_alt, link = ext
            sections = original_text.split(f"[{link_alt}]({link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK ,link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_text_nodes(text):
    base_node = [TextNode(text, TextType.TEXT)]
    base_node = split_nodes_delimiter(base_node, "**", TextType.BOLD)
    base_node = split_nodes_delimiter(base_node, "_", TextType.ITALIC)
    base_node = split_nodes_delimiter(base_node, "`", TextType.CODE)
    base_node = split_nodes_image(base_node)
    base_node = split_nodes_link(base_node)
    return base_node