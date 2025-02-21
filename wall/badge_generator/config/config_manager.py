"""Configuration management for the badge generator."""

import json
import os
from pathlib import Path
from typing import List, TypedDict

from dotenv import load_dotenv

from ..logger import logger


class RepoConfig(TypedDict):
    """Type definition for repository configuration."""

    name: str


class Config(TypedDict, total=False):
    """Type definition for overall configuration."""

    organization: str
    Backend: List[RepoConfig]
    Frontend: List[RepoConfig]
    Infrastructure: List[RepoConfig]


class ConfigManager:
    """Manages configuration loading and validation."""

    def __init__(self):
        """Initialize the configuration manager."""
        self.config = self._load_config()
        self.github_token = self._load_github_token()

    def _load_github_token(self) -> str:
        """Load GitHub token from environment.

        Returns:
            str: GitHub API token

        Raises:
            ValueError: If TOKEN environment variable is not set
        """
        load_dotenv()
        token = os.getenv("TOKEN")
        if not token:
            raise ValueError("TOKEN environment variable is required")
        return token

    def _load_config(self) -> Config:
        """Load repository configuration from config/repos.json.

        Returns:
            Config: The loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file is not found.
        """
        config_path = Path("config/repos.json")
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config = json.load(f)
            logger.info(
                f"Loaded configuration for organization: {config.get('organization')}"
            )
            return config

    def get_config(self) -> Config:
        """Get the loaded configuration.

        Returns:
            Config: The current configuration
        """
        return self.config

    def get_github_token(self) -> str:
        """Get the GitHub API token.

        Returns:
            str: The GitHub API token
        """
        return self.github_token
