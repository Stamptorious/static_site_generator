from extract_markdown import *

import unittest

import re

class ExtractMarkdown(unittest.TestCase):    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)
    
    def test_extract_markdown_two_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com) and also another [link](https://www.example2.com)"
        )
        self.assertListEqual([("link", "https://www.example.com"), ("link", "https://www.example2.com")], matches)