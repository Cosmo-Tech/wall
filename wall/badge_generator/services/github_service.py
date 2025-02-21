"""GitHub API interaction service."""

from typing import List

from github import Auth, Github
from github.Repository import Repository
from github.Workflow import Workflow

from ..logger import logger


class GitHubService:
    """Service for interacting with GitHub API."""

    def __init__(self, token: str):
        """Initialize the GitHub service with credentials.

        Args:
            token: GitHub API token
        """
        self.github = Github(auth=Auth.Token(token))

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
            repo = self.github.get_repo(f"{owner}/{repo_name}")

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

    def get_workflow_url(self, owner: str, repo: str, workflow: Workflow) -> str:
        """Generate the workflow URL.

        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            workflow: The workflow object.

        Returns:
            str: URL for the workflow page.
        """
        # Convert the workflow path to a URL path by removing .yml extension
        workflow_path = workflow.path.replace(".yml", "")
        return f"https://github.com/{owner}/{repo}/actions/workflows/{workflow_path}"
