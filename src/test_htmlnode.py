import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            "a",
            "Click me",
            {"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">Click me</a>',
        )

    def test_leaf_to_html_without_value_raises_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_to_html_with_nested_parent(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("span", "Nested text")]),
                LeafNode("em", "Sibling text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><span>Nested text</span></p><em>Sibling text</em></div>",
        )

    def test_parent_to_html_without_tag_raises_value_error(self):
        node = ParentNode(None, [])
        with self.assertRaisesRegex(ValueError, "must have a tag"):
            node.to_html()

    def test_parent_to_html_without_children_raises_value_error(self):
        node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "must have children"):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
