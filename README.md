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

## Installing the PWA on Your Phone

1. Open the GitHub Workflow Status Wall in your mobile browser.
2. Tap the browser menu (usually three dots or lines in the upper right corner).
3. Select "Add to Home screen" or "Install app".
4. Follow the prompts to add the app to your home screen.
5. The app will now be available on your home screen for quick access.
