from enum import Enum

from split_nodes import *

from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    result = []
    for block in blocks:
        block = block.strip()
        if block != '':
            result.append(block)
    return result
    
def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```") and len(block.split("\n")) > 1:
        return BlockType.CODE
    elif block.startswith(">"):
        for line in block.split('\n'):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDEREDLIST
    elif block.startswith("1. "):
        counter = 0
        for line in block.split("\n"):
            counter += 1
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDEREDLIST
    else: return BlockType.PARAGRAPH       

def text_to_children(text):
    textnodes = text_to_text_nodes(text)
    leafnodes = []
    for node in textnodes:
        print(repr(node))
        html = text_node_to_html_node(node)
        leafnodes.append(html)
    return leafnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.QUOTE:
            split_block = block.split("\n")
            stripped_blocks = []
            for split in split_block:
                stripped_blocks.append(split.lstrip(">").strip())
            new_block = "\n".join(stripped_blocks)
            new_node = ParentNode("blockquote", text_to_children(new_block))
            children.append(new_node)
        elif block_type == BlockType.UNORDEREDLIST:
            split_block = block.split("\n")
            li_nodes = []
            for split in split_block:
                li_nodes.append(ParentNode("li", text_to_children(split.lstrip("-").strip())))
            new_node = ParentNode("ul", li_nodes)
            children.append(new_node)
        elif block_type == BlockType.ORDEREDLIST:
            split_block = block.split("\n")
            li_nodes = []
            for split in split_block:
                li_nodes.append(ParentNode("li", text_to_children(split.split(". ", 1)[1])))
                
            new_node = ParentNode("ol", li_nodes)
            children.append(new_node)
        elif block_type == BlockType.CODE:
            strip_block = block[4:-3]
            
            html_node = text_node_to_html_node(TextNode(strip_block, TextType.CODE))
            new_node = ParentNode("pre", [html_node])
            children.append(new_node)
        elif block_type == BlockType.HEADING:
            number_count = 0
            for char in block:
                if char == "#":
                    number_count += 1
                elif char != "#":
                    break
            text = block[number_count + 1:]
            new_node = ParentNode(f"h{number_count}", text_to_children(text))
            children.append(new_node)
        elif block_type == BlockType.PARAGRAPH:
            block_split = block.split("\n")
            new_block = ' '.join(block_split)
            new_node = ParentNode("p", text_to_children(new_block))
            children.append(new_node)
    return ParentNode("div", children)