#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, TypedDict

from dotenv import load_dotenv
from github import Github
from github.Workflow import Workflow

# Load environment variables
load_dotenv()

class RepoConfig(TypedDict):
    name: str
    workflows: List[str]

class Config(TypedDict):
    organization: str
    repositories: List[RepoConfig]

class BadgeGenerator:
    def __init__(self):
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError('GITHUB_TOKEN environment variable is required')
        self.github = Github(token)
        self.config = self._load_config()

    def _load_config(self) -> Config:
        """Load repository configuration from config/repos.json"""
        config_path = Path('config/repos.json')
        if not config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {config_path}')
        
        with open(config_path) as f:
            return json.load(f)

    def _get_workflow_badge_url(self, owner: str, repo: str, workflow_id: str) -> str:
        """Generate the badge URL for a workflow"""
        return f'https://github.com/{owner}/{repo}/actions/workflows/{workflow_id}/badge.svg'

    def _get_workflow_url(self, owner: str, repo: str, workflow_id: str) -> str:
        """Generate the workflow URL"""
        return f'https://github.com/{owner}/{repo}/actions/workflows/{workflow_id}'

    def get_repository_workflows(self, owner: str, repo_name: str) -> List[Workflow]:
        """Fetch standard workflows from .github/workflows directory"""
        workflows = []
        try:
            repo = self.github.get_repo(f'{owner}/{repo_name}')
            standard_workflows = ['ci.yml', 'build.yml', 'test.yml']
            
            for workflow_file in standard_workflows:
                try:
                    workflow = repo.get_workflow('.github/workflows/' + workflow_file)
                    workflows.append(workflow)
                except Exception:
                    # Skip if workflow doesn't exist
                    continue
            
            return workflows
        except Exception as e:
            print(f'Error fetching workflows for {owner}/{repo_name}: {e}')
            return []

    def generate_html(self, badge_data: List[Dict]) -> str:
        """Generate HTML page with workflow badges"""
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

    def generate_badges(self):
        """Main function to generate the badge wall"""
        badge_data = []

        for repo in self.config['repositories']:
            workflows = self.get_repository_workflows(
                self.config['organization'],
                repo['name']
            )

            repo_badges = []
            for workflow in workflows:
                if 'all' in repo['workflows'] or workflow.name in repo['workflows']:
                    workflow_id = workflow.path.split('/')[-1]
                    repo_badges.append({
                        'url': self._get_workflow_badge_url(
                            self.config['organization'],
                            repo['name'],
                            workflow_id
                        ),
                        'link': self._get_workflow_url(
                            self.config['organization'],
                            repo['name'],
                            workflow_id
                        ),
                        'name': workflow.name
                    })

            # Only add repositories that have matching workflows
            if repo_badges:
                badge_data.append({
                    'repo': repo['name'],
                    'badges': repo_badges
                })

        html = self.generate_html(badge_data)
        with open('index.html', 'w') as f:
            f.write(html)
        print(f'Generated badge wall at: {os.path.abspath("index.html")}')

if __name__ == '__main__':
    generator = BadgeGenerator()
    generator.generate_badges()
