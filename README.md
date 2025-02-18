# GitHub Workflow Status Wall

A dashboard that displays GitHub workflow status badges for your organization's repositories.

## Quick Start

1. Install with uv:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. Configure:
   Set the groups and repositories to follow in `config/repos.json`

3. Generate and view:
   ```bash
   generate-badges
   # Open docs/index.html in your browser
   ```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Manual deploy
gh workflow run "Deploy to GitHub Pages"
```

## GitHub Pages Setup

1. Enable GitHub Pages in repository settings (select 'GitHub Actions' as source)
2. Access your badge wall at: `https://[username].github.io/[repository]`
3. Updates automatically every Monday at 00:00 UTC

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
