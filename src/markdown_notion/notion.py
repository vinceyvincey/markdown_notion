"""Module for interacting with the Notion API."""

import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()


class NotionClient:
    def __init__(self):
        """Initialize the Notion client with API token from environment."""
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        self.client = Client(auth=self.token)
