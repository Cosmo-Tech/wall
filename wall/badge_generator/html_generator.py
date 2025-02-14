"""HTML generation for the workflow status wall."""

from datetime import datetime
from typing import Dict, List


def generate_html(badge_data: List[Dict]) -> str:
    """Generate HTML page with workflow badges.
    
    Args:
        badge_data: List of dictionaries containing repository and badge information.
            Each dictionary should have 'repo' and 'badges' keys.
            
    Returns:
        str: Generated HTML content.
    """
    badges_html = ''
    for repo in badge_data:
        badges = ''
        for badge in repo['badges']:
            badges += f'''
            <a href="{badge['link']}" target="_blank" class="badge">
                <img src="{badge['url']}" alt="{badge['name']} workflow status" />
            </a>'''
        
        badges_html += f'''
        <div class="repo-section">
            <h2>{repo['repo']}</h2>
            <div class="badge-container">{badges}</div>
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
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f6f8fa;
        }}
        h1 {{
            text-align: center;
            color: #24292e;
            margin-bottom: 40px;
        }}
        .repo-section {{
            background-color: white;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        h2 {{
            margin-top: 0;
            color: #24292e;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 10px;
        }}
        .badge-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .badge {{
            text-decoration: none;
            transition: opacity 0.2s;
        }}
        .badge:hover {{
            opacity: 0.8;
        }}
        .badge img {{
            height: 20px;
        }}
        .updated-at {{
            text-align: center;
            color: #586069;
            font-size: 0.9em;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <h1>GitHub Workflow Status Wall</h1>
    {badges_html}
    <div class="updated-at">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>'''
