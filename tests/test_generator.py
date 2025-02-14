"""Tests for the badge generator."""

import json
from pathlib import Path

import pytest
from wall.badge_generator import BadgeGenerator


def test_load_config(tmp_path, monkeypatch):
    """Test loading configuration from file."""
    # Create a temporary config file
    config = {
        "organization": "test-org",
        "repositories": [
            {
                "name": "test-repo",
                "workflows": ["all"]
            }
        ]
    }
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "repos.json"
    config_file.write_text(json.dumps(config))

    # Mock environment variables
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    monkeypatch.chdir(tmp_path)

    # Test loading config
    generator = BadgeGenerator()
    assert generator.config["organization"] == "test-org"
    assert len(generator.config["repositories"]) == 1
    assert generator.config["repositories"][0]["name"] == "test-repo"


def test_generate_html():
    """Test HTML generation with sample data."""
    from wall.badge_generator.html_generator import generate_html

    # Sample badge data
    badge_data = [
        {
            "repo": "test-repo",
            "badges": [
                {
                    "url": "https://example.com/badge.svg",
                    "link": "https://example.com/workflow",
                    "name": "Test Workflow"
                }
            ]
        }
    ]

    # Generate HTML
    html = generate_html(badge_data)

    # Basic assertions
    assert "<!DOCTYPE html>" in html
    assert "GitHub Workflow Status Wall" in html
    assert "test-repo" in html
    assert "https://example.com/badge.svg" in html
    assert "https://example.com/workflow" in html
    assert "Test Workflow workflow status" in html
