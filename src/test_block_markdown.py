import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    text_to_children,
)


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_strips_whitespace(self):
        markdown = "  # Heading  \n\n  A paragraph with spaces.  "
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["# Heading", "A paragraph with spaces."],
        )

    def test_markdown_to_blocks_removes_empty_blocks(self):
        markdown = "\n\nFirst block\n\n\n\n   \n\nSecond block\n\n"
        self.assertEqual(markdown_to_blocks(markdown), ["First block", "Second block"])

    def test_markdown_to_blocks_with_empty_document(self):
        self.assertEqual(markdown_to_blocks(" \n\n \n"), [])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("### A heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> First quote line\n>Second quote line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "A paragraph\nwith multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_is_paragraph(self):
        block = "1. First item\n3. Skipped item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_heading_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH
        )

    def test_text_to_children_converts_inline_markdown(self):
        children = text_to_children(
            "Text with **bold** and [link](https://example.com)"
        )
        self.assertEqual(
            "".join(child.to_html() for child in children),
            'Text with <b>bold</b> and <a href="https://example.com">link</a>',
        )

    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_lists_and_quote(self):
        md = """> A quote with **bold** text
>continues here

- First _item_
- Second item

1. First item
2. Second `item`"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>A quote with <b>bold</b> text continues here</blockquote>"
            "<ul><li>First <i>item</i></li><li>Second item</li></ul>"
            "<ol><li>First item</li><li>Second <code>item</code></li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
