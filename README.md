# GitHub Workflow Status Wall

A Python application that generates an HTML wall displaying GitHub workflow status badges for multiple repositories.

## Project Structure

```
wall/
├── src/
│   ├── badge_generator/
│   │   ├── __init__.py      # Package initialization
│   │   ├── generator.py     # Core badge generation logic
│   │   └── html_generator.py # HTML generation utilities
├── tests/
│   └── test_generator.py    # Basic tests
├── config/
│   └── repos.json          # Repository configuration
└── pyproject.toml         # Project metadata and dependencies
```

## Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   uv pip install -e .
   ```

## Configuration

1. Create a `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token
   ```

2. Configure repositories in `config/repos.json`:
   ```json
   {
     "organization": "your-org",
     "repositories": [
       {
         "name": "repo-name",
         "workflows": ["all"]
       }
     ]
   }
   ```

## Usage

Generate the badge wall:
```bash
generate-badges
```

This will create an `index.html` file with the workflow status wall.

## Development

Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

Run tests:
```bash
pytest
