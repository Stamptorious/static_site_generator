import unittest

from split_nodes import *

from textnode import *

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_unchanged(self):
        old_nodes = [TextNode("This text is a test", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), [TextNode("This text is a test", TextType.BOLD)])

    def test_split_nodes_BOLD(self):
        old_nodes = [TextNode("This **text** is **a** test",  TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
                          [ 
                              TextNode("This ", TextType.TEXT), 
                              TextNode("text", TextType.BOLD),
                              TextNode(" is ", TextType.TEXT),
                              TextNode("a", TextType.BOLD),
                              TextNode(" test", TextType.TEXT)
                          ]
        ) 

    def test_split_nodes_ITALIC(self):
        old_nodes = [TextNode("This _text_ is a test", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "_", TextType.ITALIC), 
                         [TextNode("This ", TextType.TEXT),
                          TextNode("text", TextType.ITALIC),
                          TextNode(" is a test", TextType.TEXT)
                          ]
                          )
    
    def test_split_nodes_CODE(self):
        old_nodes = [TextNode("This `text` is a test", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "`", TextType.CODE), 
                         [TextNode("This ", TextType.TEXT),
                          TextNode("text", TextType.CODE),
                          TextNode(" is a test", TextType.TEXT)
                          ]
                          )
        
    def test_split_nodes_INVALID(self):
        old_nodes = [TextNode("This **text is a test", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_image(self):
        old_nodes = [TextNode("This text has an ![image](https://i.imgur.com/example.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual([TextNode("This text has an ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, "https://i.imgur.com/example.png")]
                          , new_nodes)
        
    def test_split_nodes_link(self):
        old_nodes = [TextNode("This text has a [link](https://www.example.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual([TextNode("This text has a ", TextType.TEXT),
                          TextNode("link", TextType.LINK, "https://www.example.com")]
                          , new_nodes)
    
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
    
    
