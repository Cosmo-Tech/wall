"""Logging configuration for the badge generator."""

import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

# Configure Rich logger
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            console=Console(file=sys.stderr),
        )
    ],
)

logger = logging.getLogger("badge_generator")
console = Console()
