# README.md

# GitHub Automation Suite

A Python tool to automate repository monitoring, summarization, and reporting for GitHub projects.

## Features
- **Repository Security & Vulnerability Monitoring**: Scans repositories for security issues and generates daily summaries.
- **Automated Pull Request / Issue Summarizer**: Summarizes open pull requests and issues for quick review.
- **Developer Activity Summarizer**: Summarizes commit activity, most active contributors, and most modified files.
- **Markdown Reports**: Generates readable Markdown summaries for each repository.
- **Scheduling**: Supports daily or custom-interval automation.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your GitHub token and (optionally) repos.
4. Run the tool:
   ```sh
   python main.py
   ```
   Or, to run on a schedule (e.g., daily):
   ```sh
   python main.py --schedule --interval 1440
   ```

## Configuration
- **GITHUB_TOKEN**: Required. Create a GitHub personal access token with `repo` and `security_events` scopes.
- **WORKING_REPOS**: Optional. Comma-separated list of `owner/repo` to process. If not set, all your repos are processed.

## Testing
Run all tests with:
```sh
pytest
```

## Directory Structure
- `main.py` — Entry point and CLI
- `src/` — Source code
  - `fetchers/` — Data fetchers for PRs, issues, commits, security
  - `reporting/` — Markdown summary/report generation
  - `utils.py` — Utility functions
  - `config.py` — Configuration loader
  - `github_client.py` — GitHub API wrapper
- `data/` — Output data and reports
- `tests/` — Unit tests

## License
MIT
