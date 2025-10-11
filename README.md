
# GitHub Automation Suite

A Python tool to automate repository monitoring, summarization, and reporting for GitHub projects.

---

## Features

- **Repository Security & Vulnerability Monitoring**
   - Automatically scans each configured repository for security issues (Dependabot alerts, vulnerabilities).
   - Requires a GitHub token with `repo` and `security_events` scopes.
   - Summarizes all detected security alerts in the generated reports.

- **Automated Pull Request Summarizer**
   - Fetches and summarizes all open pull requests for each repository.
   - Includes PR number, title, author, and direct links for review.
   - Tracks PR history (opened/closed/merged) within a configurable time window.

- **Automated Issue Summarizer**
   - Lists all open issues (excluding PRs) for each repository.
   - Shows issue number, title, author, and direct links.
   - Filters issues by configurable time window (e.g., last N days).

- **Developer Activity & Commit Summarizer**
   - Summarizes recent commit activity, including commit messages, authors, and timestamps.
   - Highlights most active contributors and most modified files.
   - Configurable lookback period for commit history.

- **Beautiful Markdown Reports**
   - Generates visually appealing Markdown summaries for each repository.
   - Reports include sections for PRs, issues, commits, security alerts, and overall activity.
   - **Where to find summaries:**
      - Markdown summary files are saved in the `data/summaries/` directory (e.g., `data/summaries/owner__repo_summary.md`).
      - JSON summary files are saved in the `data/` directory for further processing.

- **Scheduling & Automation**
   - Supports running on a schedule (e.g., daily, hourly) using the `--schedule` and `--interval` options.
   - Can be run manually or as a background process for continuous monitoring.

- **Configurable & Extensible**
   - Easily add or remove repositories via the `.env` file.
   - Modular codebase for adding new fetchers or report types.

- **Testing & Reliability**
   - Includes unit tests for all major components.
   - Robust error handling and logging.

---

## Setup
1. Clone the repository.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Copy `.env.example` to `.env` and fill in your GitHub token and (optionally) repos.
4. Run the tool with the following arguments:
    ```sh
    python main.py [--days N] [--schedule] [--interval MINUTES] [--repos owner1/repo1,owner2/repo2]
    ```
    - `--days N` : Number of days to look back for PRs, issues, and commits (default: 3)
    - `--schedule` : Run the tool in scheduled/recurring mode
    - `--interval MINUTES` : Interval in minutes for scheduled runs (default: 1440, i.e., daily)
    - `--repos owner1/repo1,owner2/repo2` : Comma-separated list of repositories to process (overrides WORKING_REPOS in .env)

**Examples:**
```sh
# Run for the last 7 days for all configured repos
python main.py --days 7

# Run every 2 hours for specific repos
python main.py --schedule --interval 120 --repos ab-412-bansal/AlgoVision,ab-412-bansal/Test-Security-Repository
```

---

## Configuration

- **GITHUB_TOKEN**: Required. Create a GitHub personal access token with `repo` and `security_events` scopes. For public repos, `public_repo` and `security_events` are sufficient.
- **WORKING_REPOS**: Optional. Comma-separated list of `owner/repo` to process. If not set, all your repos are processed.

---

## Output & Summaries

- **Markdown summaries** are saved in the `data/summaries/` directory. Each file is named as `<owner>__<repo>_summary.md`.
- **JSON summaries** and raw data are saved in the `data/` directory for each repository.
- Review the Markdown files for a human-friendly overview, or use the JSON files for further automation.

---

## Testing

Run all tests with:
```sh
pytest
```

---

## Directory Structure

- `main.py` — Entry point and CLI
- `src/` — Source code
   - `fetchers/` — Data fetchers for PRs, issues, commits, security
   - `reporting/` — Markdown summary/report generation
   - `utils.py` — Utility functions
   - `config.py` — Configuration loader
   - `github_client.py` — GitHub API wrapper
- `data/` — Output data and reports (including summaries)
- `tests/` — Unit tests

---

## License

MIT License

Copyright (c) 2025 [**Ayush Bansal**](https://www.linkedin.com/in/ayush-bansal-5b4706283/)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author

- **[Ayush Bansal](https://www.linkedin.com/in/ayush-bansal-5b4706283/)**  
   [ayush4bansal@gmail.com](mailto:ayush4bansal@gmail.com)  
   [GitHub: ab-412-bansal](https://github.com/ab-412-bansal)
