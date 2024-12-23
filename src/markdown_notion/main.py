#!/usr/bin/env python3

from loguru import logger


def main():
    """Main entry point for the markdown-notion converter."""
    logger.info("Starting markdown-notion converter")
    # Your main logic will go here
    pass


if __name__ == "__main__":
    # Configure logger
    logger.add("markdown_notion.log", rotation="10 MB", level="INFO")
    main()
