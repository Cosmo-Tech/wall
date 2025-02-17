"""HTML generation for the workflow status wall."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .templates.components import generate_group_section


def generate_html(grouped_data: Dict[str, List[Dict]]) -> str:
    """Generate HTML page with workflow badges.

    Args:
        grouped_data: Dictionary mapping group names to lists of repository data.
            Each repository should have 'repo' and 'badges' keys.

    Returns:
        str: Generated HTML content.
    """
    # Load base template
    template_path = Path(__file__).parent / "templates" / "base.html"
    with open(template_path) as f:
        template = f.read()

    # Load CSS
    css_path = Path(__file__).parent / "templates" / "styles.css"
    with open(css_path) as f:
        styles = f.read()

    # Generate content
    content = "".join(
        generate_group_section(name, repos) for name, repos in grouped_data.items()
    )

    # Fill template
    return template.format(
        styles=styles,
        content=content,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
