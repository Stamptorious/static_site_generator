import unittest

from markdown_blocks import *

class TestMarkdownBlocks(unittest.TestCase):  

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
    
    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is a paragraph


This is another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is a paragraph",
            "This is another paragraph",
        ],
    )

    def test_markdown_to_blocks_empty(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_block_type_PARAGRAPH(self):
        self.assertEqual(block_to_block_type("This is text"), BlockType.PARAGRAPH)
    
    def test_block_type_HEADING(self):
        self.assertEqual(block_to_block_type("#### This is text"), BlockType.HEADING)
    
    def test_block_type_CODE(self):
        self.assertEqual(block_to_block_type("```\nThis is text```"), BlockType.CODE)
    
    def test_block_type_QUOTE(self):
        self.assertEqual(block_to_block_type(">This\n>is text"), BlockType.QUOTE)
    
    def test_block_type_UNORDERED(self):
        self.assertEqual(block_to_block_type("- This\n- is text"), BlockType.UNORDEREDLIST)
    
    def test_block_type_ORDERED(self):
        self.assertEqual(block_to_block_type("1. This\n2. is text"), BlockType.ORDEREDLIST)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_quoteblock(self):
    md = """
> This is a **quote**
> This is another _quote_

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><blockquote>This is a <b>quote</b>\nThis is another <i>quote</i></blockquote></div>"
    )

def test_ULIST(self):
    md = """
- This is a **list**
- This is a _list_

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><ul><li>This is a <b>list</b></li><li>This is a <i>list</i></li></ul></div>"
    )


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


if __name__ == "__main__":
    unittest.main()