from markdown_notion.converter import markdown_to_notion_blocks
from markdown_notion.notion import NotionClient
from markdown_notion.parser import parse_markdown_file

__version__ = "0.1.0"

__all__ = [
    "MarkdownToNotion",
    "NotionClient",
    "markdown_to_notion_blocks",
    "parse_markdown_file",
]


class MarkdownToNotion:
    """Main class for converting markdown to Notion pages."""

    def __init__(self, notion_client: NotionClient = None):
        """Initialize the converter.

        Args:
            notion_client: Optional NotionClient instance. If not provided, a new one will be created.
        """
        self.notion = notion_client or NotionClient()

    def convert_file(
        self,
        markdown_file: str,
        page_id: str,
        *,
        clear: bool = False,
        update_title: bool = False,
    ) -> bool:
        """Convert a markdown file to a Notion page.

        Args:
            markdown_file: Path to the markdown file
            page_id: Notion page ID or URL where content will be added
            clear: Whether to clear existing page content before conversion
            update_title: Whether to update page title using markdown filename

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If page_id is invalid
            FileNotFoundError: If markdown file doesn't exist
        """
        from pathlib import Path

        from markdown_notion.main import validate_page_id

        # Validate and normalize page ID
        page_id = validate_page_id(page_id)

        # Validate markdown file
        markdown_path = Path(markdown_file)
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        # Clear page content if requested
        if clear and not self.notion.clear_page_content(page_id):
            return False

        # Update page title if requested
        if update_title:
            title = markdown_path.stem.replace("-", " ").replace("_", " ").title()
            if not self.notion.update_page_title(page_id, title):
                return False

        # Parse markdown file and convert to Notion blocks
        markdown_content = parse_markdown_file(markdown_file)
        notion_blocks = markdown_to_notion_blocks(markdown_content)

        # Append blocks to page
        return self.notion.append_blocks_to_page(page_id, notion_blocks)

    def convert_text(
        self, markdown_text: str, page_id: str, *, clear: bool = False
    ) -> bool:
        """Convert markdown text directly to a Notion page.

        Args:
            markdown_text: Markdown content as string
            page_id: Notion page ID or URL where content will be added
            clear: Whether to clear existing page content before conversion

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If page_id is invalid
        """
        from markdown_notion.main import validate_page_id

        # Validate and normalize page ID
        page_id = validate_page_id(page_id)

        # Clear page content if requested
        if clear and not self.notion.clear_page_content(page_id):
            return False

        # Convert markdown to Notion blocks
        notion_blocks = markdown_to_notion_blocks(markdown_text)

        # Append blocks to page
        return self.notion.append_blocks_to_page(page_id, notion_blocks)
