import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from split_nodes_delimiter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{index}. ") for index, line in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    block_nodes = []

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            block_nodes.append(
                ParentNode(f"h{level}", text_to_children(block[level + 1 :]))
            )
        elif block_type == BlockType.PARAGRAPH:
            block_nodes.append(
                ParentNode("p", text_to_children(block.replace("\n", " ")))
            )
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            block_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            quote_text = " ".join(line[1:].lstrip() for line in block.split("\n"))
            block_nodes.append(ParentNode("blockquote", text_to_children(quote_text)))
        elif block_type == BlockType.UNORDERED_LIST:
            items = [
                ParentNode("li", text_to_children(line[2:]))
                for line in block.split("\n")
            ]
            block_nodes.append(ParentNode("ul", items))
        elif block_type == BlockType.ORDERED_LIST:
            items = [
                ParentNode("li", text_to_children(line.split(". ", 1)[1]))
                for line in block.split("\n")
            ]
            block_nodes.append(ParentNode("ol", items))

    return ParentNode("div", block_nodes)
