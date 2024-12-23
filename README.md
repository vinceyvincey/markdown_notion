# Markdown to Notion Converter

A powerful Python tool that converts markdown files into beautifully formatted Notion pages while preserving formatting, structure, and rich content.

## Features

- **Rich Text Support**
  - Bold, italic, strikethrough
  - Code blocks with syntax highlighting
  - Mathematical formulas (inline and block)
  - Superscript and subscript
  - Links and highlights

- **Block Elements**
  - Headings (H1-H6)
  - Nested lists (bulleted and numbered)
  - Code blocks with language detection
  - Tables with header support
  - Blockquotes
  - Images (external URLs)
  - Horizontal rules

- **Notion Integration**
  - Direct upload to Notion pages
  - Batch processing of blocks
  - Page content management
  - Title updating

- **Advanced Features**
  - URL or ID-based page targeting
  - Content clearing option
  - Automatic title generation
  - Comprehensive logging

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/markdown-notion.git
   cd markdown-notion
   ```

2. Install the package:
   ```bash
   pip install .
   ```

## Configuration

1. Create a Notion integration:
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Click "New integration"
   - Give it a name and submit
   - Copy the integration token

2. Set up environment:
   ```bash
   export NOTION_TOKEN='your-integration-token'
   ```
   Or create a `.env` file:
   ```
   NOTION_TOKEN=your-integration-token
   ```

3. Share your Notion page with the integration:
   - Open the Notion page you want to use
   - Click "Share" and invite your integration
   - Copy the page ID from the URL (last part after the last dash)

## Usage

### Basic Usage

Convert a markdown file to a Notion page:
```bash
markdown-notion input.md page-id
```

You can use either the page ID or the full Notion URL:
```bash
markdown-notion input.md https://notion.so/workspace/Page-Name-123456789...
```

### Advanced Options

Clear existing page content before conversion:
```bash
markdown-notion input.md page-id --clear
```

Update page title using markdown filename:
```bash
markdown-notion input.md page-id --update-title
```

Enable verbose logging:
```bash
markdown-notion input.md page-id -v
```

Specify log directory:
```bash
markdown-notion input.md page-id --log-dir ./logs
```

### Full Command Reference

```bash
markdown-notion [-h] [-v] [--clear] [--update-title] [--log-dir LOG_DIR] markdown_file page_id
```

Arguments:
- `markdown_file`: Path to the markdown file to convert
- `page_id`: Notion page ID or URL where content will be added
- `-v, --verbose`: Enable verbose logging
- `--clear`: Clear existing page content before conversion
- `--update-title`: Update page title using markdown filename
- `--log-dir`: Directory for log files

## Supported Markdown Syntax

```markdown
# Heading 1
## Heading 2 (up to h6)

**Bold** and *italic* and ***both***
~~strikethrough~~ and `code`
==highlighted text==

Mathematical formulas: $inline$ and $$blocks$$

Superscript: ^2^ and Subscript: ~2~

[Links](https://example.com)
![Images](https://example.com/image.jpg)

- Bulleted lists
  - With nesting
    - Multiple levels

1. Numbered lists
   1. Also with nesting
   2. And multiple items

> Blockquotes
> Multiple lines

\```python
def code_blocks():
    print("With syntax highlighting")
\```

| Tables | With    |
|--------|---------|
| Header | Support |
```

## Development

Requirements:
- Python 3.13+
- Dependencies listed in `pyproject.toml`

Running tests:
```bash
pytest
```

## Logging

Logs are written to:
- Console (INFO level by default, DEBUG with `-v`)
- File (DEBUG level, rotated at 10MB)
  - Default: `markdown_notion.log`
  - Custom directory with `--log-dir`

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and feature requests, please use the GitHub issue tracker.
