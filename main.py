# main.py
import argparse
import time
from src.github_client import get_user, get_repo
from src import config

from src.fetchers.prs import fetch_open_prs, fetch_all_prs
from src.fetchers.issues import fetch_open_issues
from src.fetchers.commits import fetch_commits_last_30_days
from src.fetchers.security import fetch_security_alerts
from src.utils import save_json, ensure_data_dir
from src.reporting.summary import (
    summarize_prs, summarize_issues, summarize_commits, summarize_security_alerts
)
from rich.console import Console
import schedule
import logging


# Setup logging
logging.basicConfig(filename='automation.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
console = Console()

def get_repos_to_process():
    # prefer WORKING_REPOS if specified, otherwise use authenticated user's repos
    if config.WORKING_REPOS:
        return config.WORKING_REPOS
    console.print("[yellow]WORKING_REPOS not set in .env — fetching repos from authenticated user (this may return many repos).[/yellow]")
    user = get_user()
    # You might want to restrict to only your own repos; here we return full_name strings
    repos = [r.full_name for r in user.get_repos()]
    return repos


def process_repo(full_name, days=30):
    """
    Process a single repository: fetch PRs, issues, commits, security alerts, and generate a Markdown summary.
    """
    console.print(f"\n[bold cyan]Processing {full_name}[/bold cyan]")
    try:
        repo = get_repo(full_name)
    except Exception as e:
        console.print(f"[red]Failed to access {full_name}: {e}[/red]")
        logging.error(f"Failed to access {full_name}: {e}")
        return


    # Fetch PRs (open and all history)
    console.print("Fetching open PRs...")
    prs = fetch_open_prs(repo, days=days)
    pr_file = save_json(prs, f"{full_name.replace('/', '__')}_prs.json")
    console.print(f"[green]Saved PRs to[/green] {pr_file}")

    console.print(f"Fetching all PRs (last {days} days)...")
    all_prs = fetch_all_prs(repo, limit=100, days=days)
    all_prs_file = save_json(all_prs, f"{full_name.replace('/', '__')}_all_prs.json")
    console.print(f"[green]Saved all PRs to[/green] {all_prs_file}")

    # Fetch Issues
    console.print("Fetching open issues...")
    issues = fetch_open_issues(repo, days=days)
    issues_file = save_json(issues, f"{full_name.replace('/', '__')}_issues.json")
    console.print(f"[green]Saved issues to[/green] {issues_file}")

    # Fetch commits for last N days
    console.print(f"Fetching commits (last {days} days)...")
    commits = fetch_commits_last_30_days(repo, days=days)
    commits_file = save_json(commits, f"{full_name.replace('/', '__')}_commits.json")
    console.print(f"[green]Saved commits to[/green] {commits_file}")

    # Fetch security alerts
    console.print("Fetching security alerts...")
    github_token = config.GITHUB_TOKEN
    alerts = fetch_security_alerts(full_name, github_token)
    alerts_file = save_json(alerts, f"{full_name.replace('/', '__')}_security.json")
    console.print(f"[green]Saved security alerts to[/green] {alerts_file}")

    # Generate Markdown summary
    from src.reporting.summary import summarize_all_prs, build_beautiful_summary
    summary_md = build_beautiful_summary(full_name, prs, all_prs, issues, commits, alerts, days=days)
    summary_file = save_json({'summary': summary_md}, f"{full_name.replace('/', '__')}_summary.json")
    # Ensure summaries directory exists
    import os
    summaries_dir = os.path.join("data", "summaries")
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    summary_md_path = os.path.join(summaries_dir, f"{full_name.replace('/', '__')}_summary.md")
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    console.print(f"[bold green]Summary written to {summary_md_path}[/bold green]")
    logging.info(f"Processed {full_name}")


def main(repos=None, schedule_mode=False, interval_minutes=1440, days=30):
    """
    Main entry point. If schedule_mode is True, runs periodically every interval_minutes.
    """
    ensure_data_dir()
    if repos:
        repo_list = repos
    else:
        repo_list = get_repos_to_process()

    def run_all():
        max_repos = 5
        console.print(f"[blue]Processing up to {max_repos} repos (for safety). Edit main.py to change this limit.[/blue]")
        count = 0
        for r in repo_list:
            if count >= max_repos:
                break
            process_repo(r, days=days)
            count += 1
            time.sleep(1)  # small delay to be polite to API

    if schedule_mode:
        console.print(f"[magenta]Scheduling automation every {interval_minutes} minutes.[/magenta]")
        schedule.every(interval_minutes).minutes.do(run_all)
        while True:
            schedule.run_pending()
            time.sleep(10)
    else:
        run_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Automation: fetch PRs, issues, commits, security alerts, and generate summaries.")
    parser.add_argument("--repos", nargs="*", help="List of repos owner/repo (overrides .env WORKING_REPOS)")
    parser.add_argument("--schedule", action="store_true", help="Run in scheduled mode (default: off)")
    parser.add_argument("--interval", type=int, default=1440, help="Schedule interval in minutes (default: 1440, i.e., daily)")
    parser.add_argument("--days", type=int, default=30, help="Number of days to look back for PRs, issues, and commits (default: 30)")
    args = parser.parse_args()
    main(repos=args.repos, schedule_mode=args.schedule, interval_minutes=args.interval, days=args.days)
