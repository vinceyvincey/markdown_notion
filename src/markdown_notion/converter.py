"""Module for converting between markdown and Notion block structures."""

from typing import Any, Dict, List


def markdown_to_notion_blocks(markdown_content: dict) -> List[Dict[str, Any]]:
    """
    Convert parsed markdown content to Notion block structure.

    Args:
        markdown_content: Parsed markdown structure

    Returns:
        list: List of Notion blocks
    """
    pass


def text_to_notion_rich_text(text: str) -> List[Dict[str, Any]]:
    """
    Convert markdown-formatted text to Notion rich text array.

    Args:
        text: Text with potential markdown formatting

    Returns:
        list: Notion rich text array
    """
    pass
