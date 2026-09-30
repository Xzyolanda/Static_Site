from collections.abc import Callable

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unmatched delimiter {delimiter!r}"
            )

        for index, section in enumerate(sections):
            if not section:
                continue

            node_type = text_type if index % 2 else TextType.TEXT
            new_nodes.append(TextNode(section, node_type))

    return new_nodes


def _split_nodes_by_markdown_matches(
    old_nodes: list[TextNode],
    extract_matches: Callable[[str], list[tuple[str, str]]],
    marker_prefix: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_matches(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for label, url in matches:
            marker = f"{marker_prefix}[{label}]({url})"
            text_before_match, remaining_text = remaining_text.split(marker, 1)

            if text_before_match:
                new_nodes.append(TextNode(text_before_match, TextType.TEXT))
            new_nodes.append(TextNode(label, text_type, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown_matches(
        old_nodes,
        extract_markdown_images,
        "!",
        TextType.IMAGE,
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown_matches(
        old_nodes,
        extract_markdown_links,
        "",
        TextType.LINK,
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
