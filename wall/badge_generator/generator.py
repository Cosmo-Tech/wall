"""Core functionality for generating GitHub workflow status badges."""

import json
import os
from pathlib import Path
from typing import Dict, List, TypedDict

from dotenv import load_dotenv
from github import Github
from github.Repository import Repository
from github.Workflow import Workflow

from .html_generator import generate_html
from .logger import logger


class RepoConfig(TypedDict):
    """Type definition for repository configuration."""
    name: str


class Config(TypedDict, total=False):
    """Type definition for overall configuration."""
    organization: str
    Backend: List[RepoConfig]
    Frontend: List[RepoConfig]
    Infrastructure: List[RepoConfig]


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

    def _check_repo_visibility(self, repo: Repository) -> bool:
        """Check if a repository is public.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            bool: True if public, False if private/internal
        """
        return repo.visibility == "public"

    def get_repository_workflows(self, owner: str, repo_name: str) -> List[Workflow]:
        """Fetch all workflows from the repository.
        
        Args:
            owner: Repository owner/organization.
            repo_name: Repository name.
            
        Returns:
            List[Workflow]: List of workflow objects.
        """
        try:
            repo = self.github.get_repo(f'{owner}/{repo_name}')
            
            # Check visibility and warn if not public
            if not self._check_repo_visibility(repo):
                logger.warning(
                    f"Repository {owner}/{repo_name} is not public "
                    f"(visibility: {repo.visibility}). "
                    "Ensure you have appropriate access tokens."
                )
            
            logger.info(f"Fetching workflows for {owner}/{repo_name}")
            workflows = list(repo.get_workflows())
            for workflow in workflows:
                logger.debug(f"Found workflow: {workflow.name} ({workflow.path})")
            return workflows
        except Exception as e:
            logger.error(f"Error fetching workflows for {owner}/{repo_name}: {e}")
            return []

    def generate_badges(self):
        """Generate the badge wall HTML file."""
        grouped_data = {}
        
        # Process each group
        for group_name, repos in self.config.items():
            if group_name == "organization":
                continue
                
            logger.info(f"Processing {group_name} repositories")
            group_data = []
            for repo in repos:
                workflows = self.get_repository_workflows(
                    self.config['organization'],
                    repo['name']
                )

                repo_badges = []
                for workflow in workflows:
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
                    group_data.append({
                        'repo': repo['name'],
                        'badges': repo_badges
                    })
            
            if group_data:
                grouped_data[group_name] = group_data

        html = generate_html(grouped_data)
        with open('index.html', 'w') as f:
            f.write(html)
        logger.info(f"Generated badge wall at: {os.path.abspath('index.html')}")


def main():
    """Entry point for the badge generator."""
    generator = BadgeGenerator()
    generator.generate_badges()


if __name__ == '__main__':
    main()
