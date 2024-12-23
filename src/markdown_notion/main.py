#!/usr/bin/env python3

"""Main entry point for the markdown-notion converter."""

import argparse
import sys
from pathlib import Path

from loguru import logger

from markdown_notion.converter import markdown_to_notion_blocks
from markdown_notion.logging import setup_logging
from markdown_notion.notion import NotionClient
from markdown_notion.parser import parse_markdown_file


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


def main():
    """Main entry point for the markdown-notion converter."""
    parser = argparse.ArgumentParser(
        description="Convert markdown files to Notion pages"
    )
    parser.add_argument(
        "markdown_file",
        type=str,
        help="Path to the markdown file to convert",
    )
    parser.add_argument(
        "page_id",
        type=str,
        help="Notion page ID or URL where content will be added",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing page content before conversion",
    )
    parser.add_argument(
        "--update-title",
        action="store_true",
        help="Update page title using markdown filename",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        help="Directory for log files",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose, log_dir=args.log_dir)
    logger.info("Starting markdown to Notion conversion")

    try:
        # Validate and normalize page ID
        page_id = validate_page_id(args.page_id)
        logger.debug(f"Normalized page ID: {page_id}")

        # Validate markdown file
        markdown_path = Path(args.markdown_file)
        if not markdown_path.exists():
            logger.error(f"Markdown file not found: {args.markdown_file}")
            sys.exit(1)

        # Initialize Notion client
        notion = NotionClient()

        # Clear page content if requested
        if args.clear:
            if not notion.clear_page_content(page_id):
                logger.error("Failed to clear page content")
                sys.exit(1)

        # Update page title if requested
        if args.update_title:
            title = markdown_path.stem.replace("-", " ").replace("_", " ").title()
            if not notion.update_page_title(page_id, title):
                logger.error("Failed to update page title")
                sys.exit(1)

        # Parse markdown file
        markdown_content = parse_markdown_file(args.markdown_file)

        # Convert to Notion blocks
        notion_blocks = markdown_to_notion_blocks(markdown_content)

        # Append blocks to page
        if not notion.append_blocks_to_page(page_id, notion_blocks):
            logger.error("Failed to append blocks to page")
            sys.exit(1)

        logger.info("Successfully converted markdown to Notion page")

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
