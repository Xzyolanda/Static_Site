import unittest
from typing import cast

from split_nodes_delimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Plain text", TextType.TEXT, None)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_with_different_text(self):
        node = TextNode("First text", TextType.TEXT)
        node2 = TextNode("Second text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_different_text_type(self):
        node = TextNode("Formatted text", TextType.BOLD)
        node2 = TextNode("Formatted text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_different_url(self):
        node = TextNode("A link", TextType.LINK, "https://example.com")
        node2 = TextNode("A link", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_bold(self):
        html_node = text_node_to_html_node(TextNode("Bold text", TextType.BOLD))
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_node_to_html_node_italic(self):
        html_node = text_node_to_html_node(TextNode("Italic text", TextType.ITALIC))
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_node_to_html_node_code(self):
        html_node = text_node_to_html_node(TextNode("print('hi')", TextType.CODE))
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_text_node_to_html_node_link(self):
        html_node = text_node_to_html_node(
            TextNode("Example", TextType.LINK, "https://example.com")
        )
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        html_node = text_node_to_html_node(
            TextNode(
                "An example image", TextType.IMAGE, "https://example.com/image.png"
            )
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "An example image"},
        )

    def test_text_node_to_html_node_with_unsupported_type_raises_value_error(self):
        node = TextNode("Unknown", cast(TextType, None))
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter_code(self):
        nodes = split_nodes_delimiter(
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        nodes = split_nodes_delimiter(
            [TextNode("Text with **bold words** included", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold words", TextType.BOLD),
                TextNode(" included", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        nodes = split_nodes_delimiter(
            [TextNode("An _italic phrase_ here", TextType.TEXT)],
            "_",
            TextType.ITALIC,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_preserves_non_text_nodes(self):
        bold_node = TextNode("Already bold", TextType.BOLD)
        nodes = split_nodes_delimiter(
            [bold_node, TextNode(" and `code`", TextType.TEXT)],
            "`",
            TextType.CODE,
        )
        self.assertEqual(
            nodes,
            [
                bold_node,
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_with_unmatched_delimiter_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "unmatched delimiter"):
            split_nodes_delimiter(
                [TextNode("An unclosed `code block", TextType.TEXT)],
                "`",
                TextType.CODE,
            )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
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

    def test_split_nodes_image_at_text_edges(self):
        new_nodes = split_nodes_image(
            [TextNode("![first](https://one.test) after", TextType.TEXT)]
        )
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://one.test"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_preserves_non_text_nodes(self):
        bold_node = TextNode("Already bold", TextType.BOLD)
        self.assertListEqual([bold_node], split_nodes_image([bold_node]))

    def test_split_nodes_image_preserves_text_without_images(self):
        node = TextNode("No images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_ignores_images(self):
        new_nodes = split_nodes_link(
            [
                TextNode(
                    "![image](https://image.test) then [link](https://link.test)",
                    TextType.TEXT,
                )
            ]
        )
        self.assertListEqual(
            [
                TextNode("![image](https://image.test) then ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.test"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_preserves_non_text_nodes_and_no_matches(self):
        code_node = TextNode("code", TextType.CODE)
        text_node = TextNode("No links here", TextType.TEXT)
        self.assertListEqual(
            [code_node, text_node],
            split_nodes_link([code_node, text_node]),
        )

    def test_text_to_textnodes_with_all_supported_markdown(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_with_plain_text(self):
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            text_to_textnodes("Just plain text"),
        )


if __name__ == "__main__":
    unittest.main()
