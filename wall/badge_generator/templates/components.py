"""HTML component generators for the badge wall."""

from typing import Dict, List


def generate_badge(badge: Dict) -> str:
    """Generate HTML for a single badge.

    Args:
        badge: Dictionary containing badge information with 'link', 'url', and 'name' keys.

    Returns:
        str: Generated badge HTML.
    """
    return f'''
    <a href="{badge["link"]}" target="_blank" class="badge">
        <img src="{badge["url"]}" alt="{badge["name"]} workflow status" />
    </a>'''


def generate_repo_section(repo: Dict) -> str:
    """Generate HTML for a repository section.

    Args:
        repo: Dictionary containing repository information with 'repo' and 'badges' keys.

    Returns:
        str: Generated repository section HTML.
    """
    badges_html = "".join(generate_badge(badge) for badge in repo["badges"])
    return f"""
    <div class="repo-section">
        <h3>{repo["repo"]}</h3>
        <div class="badge-container">{badges_html}</div>
    </div>"""


def generate_group_section(name: str, repos: List[Dict]) -> str:
    """Generate HTML for a group section.

    Args:
        name: Group name.
        repos: List of repository dictionaries.

    Returns:
        str: Generated group section HTML.
    """
    repos_html = "".join(generate_repo_section(repo) for repo in repos)
    return f"""
    <div class="group-section">
        <h2>{name}</h2>
        <div class="repos-container">{repos_html}</div>
    </div>"""
