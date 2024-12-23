"""Module for parsing markdown files into an intermediate representation."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import markdown
from bs4 import BeautifulSoup
from loguru import logger


def parse_markdown_file(file_path: str) -> dict:
    """
    Parse a markdown file and return a structured representation.

    Args:
        file_path: Path to the markdown file

    Returns:
        dict: Structured representation of the markdown content
    """
    logger.info(f"Parsing markdown file: {file_path}")
    path = Path(file_path)
    if not path.exists():
        logger.error(f"Markdown file not found: {file_path}")
        raise FileNotFoundError(f"Markdown file not found: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
            logger.debug(f"Successfully read {len(content)} characters from file")
        return parse_markdown_text(content)
    except Exception as e:
        logger.error(f"Error reading markdown file: {e}")
        raise


def parse_markdown_text(text: str) -> dict:
    """
    Parse markdown text and return a structured representation.

    Args:
        text: Raw markdown text

    Returns:
        dict: Structured representation of the markdown content that matches
             the expected input format for markdown_to_notion_blocks
    """
    logger.info("Starting markdown text parsing")
    logger.debug(f"Input text length: {len(text)} characters")

    # Initialize markdown parser with extensions
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",  # Convert newlines to line breaks
            "attr_list",  # Support for custom attributes
            "def_list",  # Definition lists
            "md_in_html",  # Parse markdown inside HTML
        ]
    )
    logger.debug("Initialized markdown parser with extensions")

    try:
        # Convert markdown to HTML
        html = md.convert(text)
        logger.debug(f"Converted markdown to HTML: {len(html)} characters")

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        logger.debug("Created BeautifulSoup parser")

        # Process the HTML into our intermediate structure
        blocks = []

        for element in soup.children:
            if element.name is None:  # Skip empty text nodes
                continue

            block = _process_element(element)
            if block:
                blocks.append(block)
                logger.trace(f"Processed block of type: {block['type']}")

        result = {"blocks": blocks}
        logger.info(f"Successfully parsed markdown into {len(blocks)} blocks")
        return result

    except Exception as e:
        logger.error(f"Error parsing markdown text: {e}")
        raise


def _process_element(element: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """Process a BeautifulSoup element into our intermediate structure."""
    if element.name is None:
        return None

    logger.trace(f"Processing element of type: {element.name}")

    try:
        # Handle headings
        if element.name.startswith("h") and len(element.name) == 2:
            level = int(element.name[1])
            return {"type": f"heading_{level}", "content": element.get_text()}

        # Handle paragraphs
        elif element.name == "p":
            return {"type": "paragraph", "content": element.get_text()}

        # Handle code blocks
        elif element.name == "pre":
            code_element = element.find("code")
            language = (
                code_element.get("class", [""])[0].replace("language-", "")
                if code_element
                else "plain text"
            )
            logger.debug(f"Processing code block with language: {language}")
            return {
                "type": "code",
                "content": code_element.get_text()
                if code_element
                else element.get_text(),
                "language": language,
            }

        # Handle lists
        elif element.name in ["ul", "ol"]:
            items = []
            for li in element.find_all("li", recursive=False):
                item = {"content": _get_list_item_text(li), "children": []}
                # Process nested lists
                nested_list = li.find(["ul", "ol"], recursive=False)
                if nested_list:
                    nested_items = _process_list(nested_list)
                    item["children"].extend(nested_items)
                items.append(item)

            list_type = "bulleted_list" if element.name == "ul" else "numbered_list"
            logger.debug(f"Processed {list_type} with {len(items)} items")
            return {
                "type": list_type,
                "items": items,
            }

        # Handle blockquotes
        elif element.name == "blockquote":
            return {"type": "quote", "content": element.get_text()}

        # Handle tables
        elif element.name == "table":
            rows = []
            for tr in element.find_all("tr"):
                row = [td.get_text().strip() for td in tr.find_all(["td", "th"])]
                rows.append(row)

            has_header = bool(element.find("th"))
            logger.debug(
                f"Processed table with {len(rows)} rows, has_header: {has_header}"
            )
            return {"type": "table", "rows": rows, "has_header": has_header}

        # Handle horizontal rules
        elif element.name == "hr":
            return {"type": "divider"}

        logger.debug(f"Unhandled element type: {element.name}")
        return None

    except Exception as e:
        logger.error(f"Error processing element {element.name}: {e}")
        raise


def _process_list(list_element: BeautifulSoup) -> List[Dict[str, Any]]:
    """Process a list element and its nested lists."""
    logger.trace("Processing nested list")
    items = []
    for li in list_element.find_all("li", recursive=False):
        item = {"content": _get_list_item_text(li), "children": []}
        nested_list = li.find(["ul", "ol"], recursive=False)
        if nested_list:
            nested_items = _process_list(nested_list)
            item["children"].extend(nested_items)
        items.append(item)
    logger.trace(f"Processed {len(items)} nested list items")
    return items


def _get_list_item_text(li: BeautifulSoup) -> str:
    """Extract text content from a list item, excluding nested lists."""
    # Clone the element to avoid modifying the original
    li_copy = BeautifulSoup(str(li), "html.parser")
    # Remove nested lists
    for nested_list in li_copy.find_all(["ul", "ol"]):
        nested_list.decompose()
    return li_copy.get_text().strip()
