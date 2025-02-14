# GitHub Workflow Status Wall

A simple Python script that generates a static HTML dashboard displaying GitHub Actions workflow status badges for multiple repositories in an organization.

## Features

- Fetches and displays workflow status badges
- Clean, responsive interface
- Configurable repository list
- Links directly to workflow runs
- Single script execution

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/wall.git
   cd wall
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` and `workflow` scopes
   - Copy the token

4. Create a `.env` file with your token:
   ```bash
   echo "GITHUB_TOKEN=your_token_here" > .env
   ```

5. Configure repositories in `config/repos.json`:
   ```json
   {
     "organization": "your-org-name",
     "repositories": [
       {
         "name": "repo-name",
         "workflows": ["all"]  // or ["specific-workflow-name"]
       }
     ]
   }
   ```

## Usage

Run the script to generate the badge wall:
```bash
python generate_badges.py
```

This will create an `index.html` file in the current directory. Open it in your browser to view the workflow badges.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT
