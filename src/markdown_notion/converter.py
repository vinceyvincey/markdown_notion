"""Module for converting between markdown and Notion block structures."""

import re
from typing import Any, Dict, List

from loguru import logger


def markdown_to_notion_blocks(markdown_content: dict) -> List[Dict[str, Any]]:
    """
    Convert parsed markdown content to Notion block structure.

    Args:
        markdown_content: Parsed markdown structure containing type and content

    Returns:
        list: List of Notion blocks
    """
    logger.info("Converting markdown content to Notion blocks")
    logger.debug(f"Processing {len(markdown_content['blocks'])} markdown blocks")

    blocks = []

    for block in markdown_content["blocks"]:
        block_type = block["type"]
        logger.trace(f"Converting block of type: {block_type}")

        try:
            if block_type.startswith("heading_"):
                level = int(block_type[-1])
                logger.debug(f"Processing heading level {level}")
                blocks.append(
                    {
                        "type": "heading_" + str(level),
                        "heading_" + str(level): {
                            "rich_text": text_to_notion_rich_text(block["content"]),
                            "color": "default",
                            "is_toggleable": False,
                        },
                    }
                )

            elif block_type == "paragraph":
                blocks.append(
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": text_to_notion_rich_text(block["content"]),
                            "color": "default",
                        },
                    }
                )

            elif block_type in ["bulleted_list", "numbered_list"]:
                notion_type = (
                    "bulleted_list_item"
                    if block_type == "bulleted_list"
                    else "numbered_list_item"
                )
                logger.debug(f"Processing {block_type} with type {notion_type}")

                for item in block["items"]:
                    blocks.append(
                        {
                            "type": notion_type,
                            notion_type: {
                                "rich_text": text_to_notion_rich_text(item["content"]),
                                "color": "default",
                                "children": _convert_nested_list_items(
                                    item.get("children", []), notion_type
                                ),
                            },
                        }
                    )

            elif block_type == "code":
                logger.debug(
                    f"Processing code block with language: {block.get('language', 'plain text')}"
                )
                blocks.append(
                    {
                        "type": "code",
                        "code": {
                            "rich_text": text_to_notion_rich_text(block["content"]),
                            "language": block.get("language", "plain text"),
                        },
                    }
                )

            elif block_type == "quote":
                blocks.append(
                    {
                        "type": "quote",
                        "quote": {
                            "rich_text": text_to_notion_rich_text(block["content"]),
                            "color": "default",
                        },
                    }
                )

            elif block_type == "image":
                logger.debug(f"Processing image with URL: {block['url']}")
                blocks.append(
                    {
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {"url": block["url"]},
                            "caption": text_to_notion_rich_text(
                                block.get("caption", "")
                            ),
                        },
                    }
                )

            elif block_type == "table":
                rows = block["rows"]
                has_header = block.get("has_header", True)
                logger.debug(
                    f"Processing table with {len(rows)} rows, has_header: {has_header}"
                )

                table_block = {
                    "type": "table",
                    "table": {
                        "table_width": len(rows[0]) if rows else 0,
                        "has_column_header": has_header,
                        "has_row_header": False,
                        "children": [],
                    },
                }

                for row in rows:
                    table_block["table"]["children"].append(
                        {
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": cell}}]
                                    for cell in row
                                ]
                            },
                        }
                    )

                blocks.append(table_block)

            elif block_type == "divider":
                blocks.append({"type": "divider", "divider": {}})

        except Exception as e:
            logger.error(f"Error converting block type {block_type}: {e}")
            raise

    logger.info(f"Successfully converted {len(blocks)} Notion blocks")
    return blocks


def _convert_nested_list_items(items: List[Dict], parent_type: str) -> List[Dict]:
    """Convert nested list items to Notion blocks."""
    logger.trace(f"Converting nested list items of type: {parent_type}")
    if not items:
        return []

    nested_blocks = []
    for item in items:
        nested_blocks.append(
            {
                "type": parent_type,
                parent_type: {
                    "rich_text": text_to_notion_rich_text(item["content"]),
                    "color": "default",
                    "children": _convert_nested_list_items(
                        item.get("children", []), parent_type
                    ),
                },
            }
        )
    logger.trace(f"Converted {len(nested_blocks)} nested items")
    return nested_blocks


def text_to_notion_rich_text(text: str) -> List[Dict[str, Any]]:
    """
    Convert markdown-formatted text to Notion rich text array.

    Args:
        text: Text with potential markdown formatting (bold, italic, code, links, math, etc.)

    Returns:
        list: Notion rich text array with appropriate annotations
    """
    logger.trace("Converting text to Notion rich text")
    logger.trace(f"Input text length: {len(text)} characters")

    if not text:
        return []

    try:
        rich_text_blocks = []
        current_position = 0
        text_length = len(text)

        # Regular expressions for markdown patterns
        patterns = {
            "bold_italic": r"\*\*\*(.+?)\*\*\*|___(.+?)___",  # ***text*** or ___text___
            "bold": r"\*\*(.+?)\*\*|__(.+?)__",  # **text** or __text__
            "italic": r"\*(.+?)\*|_(.+?)_",  # *text* or _text_
            "strikethrough": r"~~(.+?)~~",  # ~~text~~
            "code": r"`(.+?)`",  # `code`
            "link": r"\[(.+?)\]\((.+?)\)",  # [text](url)
            "superscript": r"\^(.+?)\^",  # ^text^
            "subscript": r"~(.+?)~",  # ~text~
            "math_block": r"\$\$(.+?)\$\$",  # $$block math$$
            "math_inline": r"\$(.+?)\$",  # $inline math$
            "highlight": r"==(.+?)==",  # ==text==
        }

        while current_position < text_length:
            # Find the next markdown pattern
            next_match = None
            next_pattern = None
            next_start = text_length

            for pattern_name, pattern in patterns.items():
                match = re.search(pattern, text[current_position:])
                if match and (current_position + match.start() < next_start):
                    next_match = match
                    next_pattern = pattern_name
                    next_start = current_position + match.start()

            if next_match and next_pattern:
                # Add any text before the pattern
                if next_start > current_position:
                    rich_text_blocks.append(
                        {
                            "type": "text",
                            "text": {"content": text[current_position:next_start]},
                        }
                    )
                    logger.trace(
                        f"Added plain text of length {next_start - current_position}"
                    )

                # Process the matched pattern
                if next_pattern == "link":
                    link_text, url = next_match.groups()
                    logger.trace(f"Processing link: {link_text} -> {url}")
                    rich_text_blocks.append(
                        {
                            "type": "text",
                            "text": {"content": link_text, "link": {"url": url}},
                        }
                    )
                elif next_pattern in ["math_block", "math_inline"]:
                    math_content = next_match.group(1)
                    logger.trace(f"Processing math content of type: {next_pattern}")
                    rich_text_blocks.append(
                        {"type": "equation", "equation": {"expression": math_content}}
                    )
                else:
                    content = next(
                        group for group in next_match.groups() if group is not None
                    )
                    logger.trace(f"Processing {next_pattern} content")
                    block = {
                        "type": "text",
                        "text": {"content": content},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                    }

                    if next_pattern == "bold_italic":
                        block["annotations"]["bold"] = True
                        block["annotations"]["italic"] = True
                    elif next_pattern == "bold":
                        block["annotations"]["bold"] = True
                    elif next_pattern == "italic":
                        block["annotations"]["italic"] = True
                    elif next_pattern == "strikethrough":
                        block["annotations"]["strikethrough"] = True
                    elif next_pattern == "code":
                        block["annotations"]["code"] = True
                    elif next_pattern == "superscript":
                        superscript_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
                        block["text"]["content"] = content.translate(superscript_map)
                    elif next_pattern == "subscript":
                        subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
                        block["text"]["content"] = content.translate(subscript_map)
                    elif next_pattern == "highlight":
                        block["annotations"]["color"] = "yellow_background"

                    rich_text_blocks.append(block)

                current_position = current_position + next_match.end()
            else:
                # Add remaining text
                remaining_text = text[current_position:]
                if remaining_text:
                    rich_text_blocks.append(
                        {"type": "text", "text": {"content": remaining_text}}
                    )
                break

        logger.trace(f"Created {len(rich_text_blocks)} rich text blocks")
        return (
            rich_text_blocks
            if rich_text_blocks
            else [{"type": "text", "text": {"content": text}}]
        )

    except Exception as e:
        logger.error(f"Error converting text to rich text: {e}")
        raise
