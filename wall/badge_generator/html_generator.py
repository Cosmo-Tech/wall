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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#f6f8fa">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path fill='%23218bff' d='M8 0a8 8 0 100 16A8 8 0 008 0zm3.5 8.5l-5 3a.5.5 0 01-.75-.4v-6a.5.5 0 01.75-.4l5 3a.5.5 0 010 .8z'/></svg>">
    <title>GitHub Workflow Status Wall</title>
    <style>
        /* Base mobile styles */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f6f8fa;
            font-size: 16px;
        }}

        .container {{
            padding: env(safe-area-inset-top, 10px) env(safe-area-inset-right, 10px) 
                     env(safe-area-inset-bottom, 10px) env(safe-area-inset-left, 10px);
            max-width: 100%;
        }}

        h1 {{
            font-size: 1.25em;
            padding: 10px;
            margin: 0;
            background-color: white;
            position: sticky;
            top: 0;
            z-index: 1;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            color: #24292e;
        }}

        .group-section {{
            margin: 10px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        h2 {{
            font-size: 1.1em;
            padding: 10px;
            margin: 0;
            background: #f1f3f5;
            color: #24292e;
            border-bottom: 1px solid #e1e4e8;
        }}

        .repo-section {{
            padding: 8px;
            border-bottom: 1px solid #eaecef;
        }}

        h3 {{
            font-size: 0.9em;
            margin: 0 0 4px 0;
            color: #24292e;
        }}

        .badge-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}

        .badge {{
            text-decoration: none;
            transition: opacity 0.2s;
        }}

        .badge:hover {{
            opacity: 0.8;
        }}

        .badge img {{
            height: 14px;
        }}

        .updated-at {{
            text-align: center;
            color: #586069;
            font-size: 0.8em;
            padding: 10px;
            background: white;
            margin-top: 10px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        /* Tablet breakpoint */
        @media (min-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            .repos-container {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                padding: 10px;
            }}
            
            .repo-section {{
                border: 1px solid #eaecef;
                border-radius: 4px;
                margin: 0;
            }}
        }}

        /* Desktop breakpoint */
        @media (min-width: 1024px) {{
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            .repos-container {{
                grid-template-columns: repeat(3, 1fr);
            }}
            
            .badge img {{
                height: 16px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            h2 {{
                font-size: 1.2em;
            }}

            h3 {{
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <h1>GitHub Workflow Status Wall</h1>
    <div class="container">
        {groups_html}
    </div>
    <div class="updated-at">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>'''
