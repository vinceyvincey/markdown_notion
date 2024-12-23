"""Module for interacting with the Notion API."""

import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from loguru import logger
from notion_client import Client

load_dotenv()


class NotionClient:
    def __init__(self):
        """Initialize the Notion client with API token from environment."""
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            logger.error("NOTION_TOKEN environment variable is missing")
            raise ValueError("NOTION_TOKEN environment variable is required")

        logger.info("Initializing Notion client")
        try:
            self.client = Client(auth=self.token)
            # Test the connection by getting the bot user
            self.client.users.me
            logger.info("Successfully connected to Notion API")
        except Exception as e:
            logger.error(f"Failed to initialize Notion client: {e}")
            raise

    def append_blocks_to_page(self, page_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """
        Append blocks to a Notion page.

        Args:
            page_id: The ID of the Notion page
            blocks: List of block objects to append

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Appending {len(blocks)} blocks to page {page_id}")

        try:
            # Verify page exists and is accessible
            self.client.pages.retrieve(page_id)
            logger.debug(f"Successfully verified access to page {page_id}")

            # Notion API has a limit of 100 blocks per request
            batch_size = 100
            for i in range(0, len(blocks), batch_size):
                batch = blocks[i : i + batch_size]
                logger.debug(f"Processing batch of {len(batch)} blocks")

                self.client.blocks.children.append(block_id=page_id, children=batch)
                logger.debug(f"Successfully appended batch {i//batch_size + 1}")

            logger.info("Successfully appended all blocks to page")
            return True

        except Exception as e:
            logger.error(f"Error appending blocks to page: {e}")
            return False

    def clear_page_content(self, page_id: str) -> bool:
        """
        Clear all content from a Notion page.

        Args:
            page_id: The ID of the Notion page

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Clearing content from page {page_id}")

        try:
            # Get all blocks in the page
            blocks = self.client.blocks.children.list(block_id=page_id)

            # Delete each block
            for block in blocks["results"]:
                self.client.blocks.delete(block_id=block["id"])
                logger.trace(f"Deleted block {block['id']}")

            logger.info(
                f"Successfully cleared {len(blocks['results'])} blocks from page"
            )
            return True

        except Exception as e:
            logger.error(f"Error clearing page content: {e}")
            return False

    def update_page_title(self, page_id: str, title: str) -> bool:
        """
        Update the title of a Notion page.

        Args:
            page_id: The ID of the Notion page
            title: New title for the page

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Updating title of page {page_id}")

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={"title": {"title": [{"text": {"content": title}}]}},
            )
            logger.info(f"Successfully updated page title to: {title}")
            return True

        except Exception as e:
            logger.error(f"Error updating page title: {e}")
            return False
