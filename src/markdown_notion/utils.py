"""Utility functions for markdown-notion converter."""


def validate_page_id(page_id: str) -> str:
    """
    Validate and normalize the Notion page ID.

    Args:
        page_id: Raw page ID or URL

    Returns:
        str: Normalized page ID
    """
    # Handle full URLs
    if page_id.startswith("https://"):
        # Extract ID from URL
        parts = page_id.split("/")
        page_id = parts[-1].split("-")[-1]

    # Remove any hyphens
    page_id = page_id.replace("-", "")

    # Validate length
    if len(page_id) != 32:
        raise ValueError("Invalid Notion page ID format")

    return page_id
