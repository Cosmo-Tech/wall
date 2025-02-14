import { Octokit } from '@octokit/rest';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as dotenv from 'dotenv';

dotenv.config();

interface Repository {
  name: string;
  workflows: string[];
}

interface Config {
  organization: string;
  repositories: Repository[];
}

class BadgeGenerator {
  private octokit: Octokit;
  private config: Config = { organization: '', repositories: [] };

  constructor() {
    const token = process.env.GITHUB_TOKEN;
    if (!token) {
      throw new Error('GITHUB_TOKEN environment variable is required');
    }

    this.octokit = new Octokit({
      auth: token
    });
  }

  async loadConfig(): Promise<void> {
    const configPath = path.join(__dirname, '../config/repos.json');
    const configContent = await fs.readFile(configPath, 'utf-8');
    this.config = JSON.parse(configContent);
  }

  private getWorkflowBadgeUrl(owner: string, repo: string, workflow_id: string): string {
    return `https://github.com/${owner}/${repo}/actions/workflows/${workflow_id}/badge.svg`;
  }

  private getWorkflowUrl(owner: string, repo: string, workflow_id: string): string {
    return `https://github.com/${owner}/${repo}/actions/workflows/${workflow_id}`;
  }

  async getRepositoryWorkflows(owner: string, repo: string): Promise<any[]> {
    try {
      const { data } = await this.octokit.actions.listRepoWorkflows({
        owner,
        repo
      });
      return data.workflows;
    } catch (error) {
      console.error(`Error fetching workflows for ${owner}/${repo}:`, error);
      return [];
    }
  }

  generateHtml(badgeData: { repo: string; badges: { url: string; link: string; name: string }[] }[]): string {
    const badges = badgeData.map(repo => `
      <div class="repo-section">
        <h2>${repo.repo}</h2>
        <div class="badge-container">
          ${repo.badges.map(badge => `
            <a href="${badge.link}" target="_blank" class="badge">
              <img src="${badge.url}" alt="${badge.name} workflow status" />
            </a>
          `).join('')}
        </div>
      </div>
    `).join('');

    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Workflow Status Wall</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f6f8fa;
        }
        h1 {
            text-align: center;
            color: #24292e;
            margin-bottom: 40px;
        }
        .repo-section {
            background-color: white;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        h2 {
            margin-top: 0;
            color: #24292e;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 10px;
        }
        .badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .badge {
            text-decoration: none;
            transition: opacity 0.2s;
        }
        .badge:hover {
            opacity: 0.8;
        }
        .badge img {
            height: 20px;
        }
        .updated-at {
            text-align: center;
            color: #586069;
            font-size: 0.9em;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <h1>GitHub Workflow Status Wall</h1>
    ${badges}
    <div class="updated-at">
        Last updated: ${new Date().toLocaleString()}
    </div>
</body>
</html>`;
  }

  async generateBadges(): Promise<void> {
    await this.loadConfig();
    const badgeData = [];

    for (const repo of this.config.repositories) {
      const workflows = await this.getRepositoryWorkflows(
        this.config.organization,
        repo.name
      );

      const repoBadges = workflows
        .filter(workflow => repo.workflows.includes('all') || repo.workflows.includes(workflow.name))
        .map(workflow => ({
          url: this.getWorkflowBadgeUrl(this.config.organization, repo.name, workflow.path.split('/').pop() || ''),
          link: this.getWorkflowUrl(this.config.organization, repo.name, workflow.path.split('/').pop() || ''),
          name: workflow.name
        }));

      badgeData.push({
        repo: repo.name,
        badges: repoBadges
      });
    }

    const html = this.generateHtml(badgeData);
    await fs.writeFile(path.join(__dirname, '../../public/index.html'), html);
  }
}

// Run the badge generator
const generator = new BadgeGenerator();
generator.generateBadges().catch(console.error);
