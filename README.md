# GitHub Workflow Status Wall

A dashboard that displays GitHub Actions workflow status badges for multiple repositories in an organization.

## Features

- Automatically fetches and displays workflow status badges
- Updates hourly via GitHub Actions
- Responsive design with a clean interface
- Configurable repository list
- Links directly to workflow runs
- Hosted on GitHub Pages

## Setup

1. Fork this repository

2. Configure GitHub Pages:
   - Go to repository Settings > Pages
   - Set source branch to `gh-pages`
   - Save the configuration

3. Create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` and `workflow` scopes
   - Add the token as a repository secret named `GITHUB_TOKEN`

4. Configure repositories:
   - Edit `src/config/repos.json`
   - Add repositories you want to monitor:
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

5. Install dependencies and build:
   ```bash
   npm install
   npm run build
   ```

6. The GitHub Action will automatically run every hour to update the badges. You can also trigger it manually from the Actions tab.

## Development

- `npm run dev` - Watch mode for TypeScript compilation
- `npm run build` - Build the TypeScript code
- `npm start` - Generate badges manually

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT
