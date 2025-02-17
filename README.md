# GitHub Workflow Status Wall

A mobile-first dashboard that displays GitHub workflow status badges for your organization's repositories.

## Features

- Groups repositories by type (Backend, Frontend, Infrastructure)
- Responsive design that works on all devices
- Automatic weekly updates via GitHub Actions
- Deploys to GitHub Pages
- Dark mode support and PWA capabilities
- Clean, modular architecture
- Comprehensive documentation

## Quick Start

1. Install with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   uv pip install -e .
   ```

2. Configure:
   See [Configuration Guide](docs/configuration/options.md) for detailed setup instructions.

3. Generate and view:
   ```bash
   generate-badges
   # Open docs/index.html in your browser
   ```

## Architecture

The project follows clean architecture principles with clear separation of concerns:

- **Services Layer**: Handles GitHub API interactions and badge generation
- **Configuration Layer**: Manages settings and environment variables
- **Template Layer**: Generates the HTML output
- **Entry Point**: Orchestrates the application flow

See [Architecture Overview](docs/architecture/overview.md) for detailed documentation.

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Manual deploy
gh workflow run "Deploy to GitHub Pages"
```

## Project Structure

```
wall/
├── badge_generator/
│   ├── services/
│   │   ├── github_service.py    # GitHub API interactions
│   │   └── badge_service.py     # Badge generation logic
│   ├── config/
│   │   └── config_manager.py    # Configuration handling
│   ├── templates/               # HTML templates
│   └── main.py                  # Entry point
├── docs/
│   ├── architecture/           # Architecture documentation
│   └── configuration/          # Configuration guides
└── tests/                      # Test suite
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

For detailed setup instructions and configuration options, see the [Configuration Guide](docs/configuration/options.md).
