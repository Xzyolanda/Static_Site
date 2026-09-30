import unittest

from textnode import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_returns_multiple_matches(self):
        matches = extract_markdown_images(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_allows_empty_alt_text(self):
        matches = extract_markdown_images(
            "An image: ![](https://example.com/image.png)"
        )
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_links_returns_multiple_matches(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "![image](https://example.com/image.png) and [a link](https://example.com)"
        )
        self.assertListEqual([("a link", "https://example.com")], matches)

    def test_extract_markdown_extractors_return_empty_list_without_matches(self):
        text = "This paragraph has no Markdown links or images."
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))


if __name__ == "__main__":
    unittest.main()
