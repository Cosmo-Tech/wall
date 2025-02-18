"""Badge generation service."""

from typing import Dict, List
from pathlib import Path

from ..html_generator import generate_html
from ..logger import logger
from .github_service import GitHubService


class BadgeService:
    """Service for generating workflow status badges."""

    def __init__(self, github_service: GitHubService):
        """Initialize the badge service.
        
        Args:
            github_service: Initialized GitHub service instance
        """
        self.github_service = github_service

    def generate_repository_badges(
        self, organization: str, repo_name: str
    ) -> List[Dict[str, str]]:
        """Generate badges for a repository's workflows.

        Args:
            organization: Repository owner/organization
            repo_name: Repository name

        Returns:
            List[Dict[str, str]]: List of badge data dictionaries
        """
        workflows = self.github_service.get_repository_workflows(organization, repo_name)
        repo_badges = []
        for workflow in workflows:
            workflow_id = workflow.path.split("/")[-1]
            repo_badges.append(
                {
                    "url": workflow.badge_url,
                    "link": self.github_service.get_workflow_url(
                        organization, repo_name, workflow_id
                    ),
                    "name": workflow.name,
                    "state": workflow.state
                }
            )
        return repo_badges

    def generate_badge_wall(self, grouped_repos: Dict[str, List[Dict]]) -> None:
        """Generate the badge wall HTML file.

        Args:
            grouped_repos: Dictionary mapping repository groups to repository lists
        """
        grouped_data = {}

        # Process each group
        for group_name, repos in grouped_repos.items():
            if group_name == "organization":
                continue

            logger.info(f"Processing {group_name} repositories")
            group_data = []
            
            for repo in repos:
                badges = self.generate_repository_badges(
                    grouped_repos["organization"], repo["name"]
                )

                # Only add repositories that have matching workflows
                if badges:
                    group_data.append({"repo": repo["name"], "badges": badges})

            if group_data:
                grouped_data[group_name] = group_data

        # Generate HTML
        html = generate_html(grouped_data)
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        with open(docs_dir / "index.html", "w") as f:
            f.write(html)
        logger.info(f"Generated badge wall at: {docs_dir / 'index.html'}")
