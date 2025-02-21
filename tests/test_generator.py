"""Tests for the badge generator."""

import json

from wall.badge_generator.config.config_manager import ConfigManager
from wall.badge_generator.services.badge_service import BadgeService
from wall.badge_generator.services.github_service import GitHubService


def test_config_manager(tmp_path, monkeypatch):
    """Test configuration manager."""
    # Create a temporary config file
    config = {"organization": "test-org", "Backend": [{"name": "test-repo"}]}
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "repos.json"
    config_file.write_text(json.dumps(config))

    # Mock environment variables
    monkeypatch.setenv("TOKEN", "dummy-token")
    monkeypatch.chdir(tmp_path)

    # Test loading config
    config_manager = ConfigManager()
    loaded_config = config_manager.get_config()
    assert loaded_config["organization"] == "test-org"
    assert len(loaded_config["Backend"]) == 1
    assert loaded_config["Backend"][0]["name"] == "test-repo"
    assert config_manager.get_github_token() == "dummy-token"


def test_github_service(mocker):
    """Test GitHub service."""
    service = GitHubService("dummy-token")

    # Test URL generation
    mock_workflow = mocker.Mock()
    mock_workflow.path = "test.yml"
    workflow_url = service.get_workflow_url("test-org", "test-repo", mock_workflow)
    assert workflow_url == "https://github.com/test-org/test-repo/actions/workflows/test"


def test_badge_service(mocker):
    """Test badge service."""
    # Mock GitHub service
    github_service = mocker.Mock()
    mock_workflow = mocker.Mock()
    mock_workflow.name = "Test Workflow"
    mock_workflow.path = "workflows/test.yml"
    mock_workflow.html_url = "https://example.com/workflow"
    mock_workflow.badge_url = "https://example.com/badge.svg"
    mock_workflow.state = "active"
    github_service.get_repository_workflows.return_value = [mock_workflow]

    # Create badge service
    service = BadgeService(github_service)

    # Test badge generation
    badges = service.generate_repository_badges("test-org", "test-repo")
    assert len(badges) == 1
    assert badges[0]["link"] == "https://example.com/workflow"
    assert badges[0]["name"] == "Test Workflow"
    assert badges[0]["url"] == "https://example.com/badge.svg"
    assert badges[0]["state"] == "active"


def test_generate_html():
    """Test HTML generation with sample data."""
    from wall.badge_generator.html_generator import generate_html

    # Sample badge data
    badge_data = {
        "Backend": [
            {
                "repo": "test-repo",
                "badges": [
                    {
                        "url": "https://example.com/badge.svg",
                        "link": "https://example.com/workflow",
                        "name": "Test Workflow",
                    }
                ],
            }
        ]
    }

    # Generate HTML
    html = generate_html(badge_data)

    # Basic assertions
    assert "<!DOCTYPE html>" in html
    assert "GitHub Workflow Status Wall" in html
    assert "test-repo" in html
    assert "https://example.com/badge.svg" in html
    assert "https://example.com/workflow" in html
    assert "Test Workflow workflow status" in html
