"""Entry point for the badge generator."""

from .config.config_manager import ConfigManager
from .services.github_service import GitHubService
from .services.badge_service import BadgeService
from .logger import logger


def main():
    """Entry point for the badge generator."""
    try:
        # Initialize services
        config_manager = ConfigManager()
        github_service = GitHubService(config_manager.get_github_token())
        badge_service = BadgeService(github_service)

        # Generate badges
        logger.info("Starting badge generation")
        badge_service.generate_badge_wall(config_manager.get_config())
        logger.info("Badge generation completed successfully")

    except Exception as e:
        logger.error(f"Error generating badges: {e}")
        raise


if __name__ == "__main__":
    main()
