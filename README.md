# GitHub Workflow Status Wall

A mobile-first dashboard that displays GitHub workflow status badges for your organization's repositories.

## Features

- Groups repositories by type (Backend, Frontend, Infrastructure)
- Responsive design that works on all devices
- Automatic weekly updates via GitHub Actions
- Deploys to GitHub Pages
- Dark mode support and PWA capabilities

## Quick Start

1. Install with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   uv pip install -e .
   ```

2. Configure:
   ```bash
   # .env
   TOKEN=your_github_token
   ```

   ```json
   # config/repos.json
   {
     "organization": "your-org",
     "Backend": [
       { "name": "api-service" },
       { "name": "worker-service" }
     ],
     "Frontend": [
       { "name": "web-app" }
     ]
   }
   ```

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
