#!/usr/bin/env python3

"""Main entry point for the markdown-notion converter."""

import argparse
import sys

from loguru import logger

from markdown_notion.converter_api import MarkdownToNotion
from markdown_notion.log_config import setup_logging


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
        # Initialize converter
        converter = MarkdownToNotion()

        # Convert markdown to Notion
        success = converter.convert_file(
            args.markdown_file,
            args.page_id,
            clear=args.clear,
            update_title=args.update_title,
        )

        if success:
            logger.info("Successfully converted markdown to Notion page")
        else:
            logger.error("Failed to convert markdown to Notion page")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
