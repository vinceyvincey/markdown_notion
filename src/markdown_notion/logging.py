"""Module for configuring logging settings."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def setup_logging(
    verbose: bool = False,
    log_file: Optional[str] = "markdown_notion.log",
    log_dir: Optional[str] = None,
) -> None:
    """
    Configure logging settings for the application.

    Args:
        verbose: Whether to enable debug logging to console
        log_file: Name of the log file (default: markdown_notion.log)
        log_dir: Directory for log files (default: current directory)
    """
    # Remove default logger
    logger.remove()

    # Configure console logging format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Add console logger with appropriate level
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, format=log_format, level=log_level)

    # Add file logger if specified
    if log_file:
        if log_dir:
            # Create log directory if it doesn't exist
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)
            log_file = str(log_path / log_file)

        logger.add(
            log_file,
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            level="DEBUG",
            format=log_format,
        )
        logger.debug(f"File logging enabled: {log_file}")
