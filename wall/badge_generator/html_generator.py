"""HTML generation for the workflow status wall."""

from datetime import datetime
from typing import Dict, List


def generate_badges_html(badges: List[Dict]) -> str:
    """Generate HTML for workflow badges.
    
    Args:
        badges: List of badge information dictionaries.
        
    Returns:
        str: Generated badges HTML.
    """
    return ''.join(
        f'''
        <a href="{badge['link']}" target="_blank" class="badge">
            <img src="{badge['url']}" alt="{badge['name']} workflow status" />
        </a>'''
        for badge in badges
    )


def generate_html(grouped_data: Dict[str, List[Dict]]) -> str:
    """Generate HTML page with workflow badges.
    
    Args:
        grouped_data: Dictionary mapping group names to lists of repository data.
            Each repository should have 'repo' and 'badges' keys.
            
    Returns:
        str: Generated HTML content.
    """
    groups_html = ''
    for group_name, repos in grouped_data.items():
        repos_html = ''
        for repo in repos:
            repos_html += f'''
            <div class="repo-section">
                <h3>{repo['repo']}</h3>
                <div class="badge-container">{generate_badges_html(repo['badges'])}</div>
            </div>'''
            
        groups_html += f'''
        <div class="group-section">
            <h2>{group_name}</h2>
            <div class="repos-container">{repos_html}</div>
        </div>'''

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Workflow Status Wall</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            max-width: 100%;
            margin: 0 auto;
            padding: 10px;
            background-color: #f6f8fa;
        }}
        h1 {{
            text-align: center;
            color: #24292e;
            margin: 10px 0 20px 0;
            font-size: 1.5em;
        }}
        .group-section {{
            background-color: white;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        h2 {{
            font-size: 1.2em;
            margin: 0 0 10px 0;
            color: #24292e;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 5px;
        }}
        h3 {{
            font-size: 1em;
            margin: 0 0 5px 0;
            color: #24292e;
        }}
        .repo-section {{
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            background-color: #fafbfc;
        }}
        .repos-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
        }}
        .badge-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .badge {{
            text-decoration: none;
            transition: opacity 0.2s;
        }}
        .badge:hover {{
            opacity: 0.8;
        }}
        .badge img {{
            height: 16px;
        }}
        .updated-at {{
            text-align: center;
            color: #586069;
            font-size: 0.8em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>GitHub Workflow Status Wall</h1>
    {groups_html}
    <div class="updated-at">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>'''
