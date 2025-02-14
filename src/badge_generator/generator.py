"""Core functionality for generating GitHub workflow status badges."""

import json
import os
from pathlib import Path
from typing import Dict, List, TypedDict

from dotenv import load_dotenv
from github import Github
from github.Workflow import Workflow

from .html_generator import generate_html


class RepoConfig(TypedDict):
    """Type definition for repository configuration."""
    name: str
    workflows: List[str]


class Config(TypedDict):
    """Type definition for overall configuration."""
    organization: str
    repositories: List[RepoConfig]


class BadgeGenerator:
    """Generates a wall of GitHub workflow status badges."""

    def __init__(self):
        """Initialize the badge generator with GitHub credentials."""
        load_dotenv()
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError('GITHUB_TOKEN environment variable is required')
        self.github = Github(token)
        self.config = self._load_config()

    def _load_config(self) -> Config:
        """Load repository configuration from config/repos.json.
        
        Returns:
            Config: The loaded configuration.
            
        Raises:
            FileNotFoundError: If the configuration file is not found.
        """
        config_path = Path('config/repos.json')
        if not config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {config_path}')
        
        with open(config_path) as f:
            return json.load(f)

    def _get_workflow_badge_url(self, owner: str, repo: str, workflow_id: str) -> str:
        """Generate the badge URL for a workflow.
        
        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            workflow_id: Workflow file name.
            
        Returns:
            str: URL for the workflow status badge.
        """
        return f'https://github.com/{owner}/{repo}/actions/workflows/{workflow_id}/badge.svg'

    def _get_workflow_url(self, owner: str, repo: str, workflow_id: str) -> str:
        """Generate the workflow URL.
        
        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            workflow_id: Workflow file name.
            
        Returns:
            str: URL for the workflow page.
        """
        return f'https://github.com/{owner}/{repo}/actions/workflows/{workflow_id}'

    def get_repository_workflows(self, owner: str, repo_name: str) -> List[Workflow]:
        """Fetch standard workflows from .github/workflows directory.
        
        Args:
            owner: Repository owner/organization.
            repo_name: Repository name.
            
        Returns:
            List[Workflow]: List of workflow objects.
        """
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

    def generate_badges(self):
        """Generate the badge wall HTML file."""
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

        html = generate_html(badge_data)
        with open('index.html', 'w') as f:
            f.write(html)
        print(f'Generated badge wall at: {os.path.abspath("index.html")}')


def main():
    """Entry point for the badge generator."""
    generator = BadgeGenerator()
    generator.generate_badges()


if __name__ == '__main__':
    main()
