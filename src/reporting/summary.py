# Add missing imports
from typing import List, Dict
from datetime import datetime
from collections import Counter

def summarize_all_prs(all_prs: List[Dict], days: int = 30) -> str:
    """
    Generate a Markdown summary of all PRs (open, closed, merged) for the last N days.
    """
    if not all_prs:
        return f"No pull request history in the last {days} days."
    lines = [f"### Pull Request History (Last {days} Days)\n"]
    for pr in all_prs:
        state = pr.get('state', 'unknown').capitalize()
        merged = ' (merged)' if pr.get('merged') else ''
        closed = f", closed at {pr['closed_at']}" if pr.get('closed_at') else ''
        lines.append(f"- [#{pr['number']}]({pr['html_url']}): {pr['title']} (by @{pr['user']}) — **{state}{merged}{closed}**")
    return "\n".join(lines)
# src/reporting/summary.py
"""
Reporting utilities for generating Markdown summaries of PRs, issues, commits, and security alerts.
"""
from typing import List, Dict

def summarize_prs(prs: List[Dict], days: int = 30) -> str:
    """
    Generate a Markdown summary of open pull requests for the last N days.
    """
    if not prs:
        return f"No open pull requests in the last {days} days."
    lines = [f"### Open Pull Requests (Last {days} Days)\n"]
    for pr in prs:
        created = datetime.fromisoformat(pr['created_at']).strftime('%Y-%m-%d') if pr.get('created_at') else ''
        lines.append(f"- [#{pr['number']}]({pr['html_url']}): {pr['title']} (by @{pr['user']}, opened {created})")
    return "\n".join(lines)

def summarize_issues(issues: List[Dict], days: int = 30) -> str:
    """
    Generate a Markdown summary of open issues for the last N days.
    """
    if not issues:
        return f"No open issues in the last {days} days."
    lines = [f"### Open Issues (Last {days} Days)\n"]
    for issue in issues:
        created = datetime.fromisoformat(issue['created_at']).strftime('%Y-%m-%d') if issue.get('created_at') else ''
        lines.append(f"- [#{issue['number']}]({issue['html_url']}): {issue['title']} (by @{issue['user']}, opened {created})")
    return "\n".join(lines)

def summarize_commits(commits: List[Dict], days: int = 30) -> str:
    """
    Generate a Markdown summary of recent commits for the last N days.
    """
    if not commits:
        return f"No recent commits in the last {days} days."
    lines = [f"### Recent Commits (Last {days} Days)\n"]
    for c in commits:
        date = c.get('date', '')
        date_str = datetime.fromisoformat(date).strftime('%Y-%m-%d') if date else ''
        lines.append(f"- [{c['sha'][:7]}]({c['html_url']}): {c['message'].splitlines()[0]} (by @{c['author']}, {date_str})")
    return "\n".join(lines)

def summarize_security_alerts(alerts: List[Dict]) -> str:
    """
    Generate a Markdown summary of security/vulnerability alerts.
    Handles cases where alerts may contain error strings or malformed data.
    """
    if not alerts or not isinstance(alerts, list):
        return "No security alerts."
    # If the API returns a string or error, show a friendly message
    if isinstance(alerts[0], dict) and 'error' in alerts[0]:
        return f"⚠️ Could not fetch security alerts: {alerts[0]['error']}"
    lines = ["### Security Alerts\n"]
    for alert in alerts:
        if not isinstance(alert, dict):
            continue
        dep = alert.get('dependency', 'Unknown')
        sev = alert.get('severity', 'N/A')
        summ = alert.get('summary', 'No summary')
        state = alert.get('state', 'N/A')
        url = alert.get('url', '')
        lines.append(f"- **{dep}** [`{sev}`] - {summ} (state: {state})" + (f" [View Alert]({url})" if url else ""))
    if len(lines) == 1:
        return "No security alerts."
    return "\n".join(lines)

def summarize_commit_activity(commits: List[Dict], days: int = 30, top_n: int = 3) -> str:
    """
    Summarize commit activity: top contributors and most modified files in the last N days.
    """
    if not commits:
        return f"No commit activity in the last {days} days."
    author_counter = Counter()
    file_counter = Counter()
    for c in commits:
        author = c.get('author', 'unknown')
        author_counter[author] += 1
        for f in c.get('files', []):
            file_counter[f.get('filename', 'unknown')] += 1
    lines = [f"### 📈 Commit Activity (Last {days} Days)"]
    if author_counter:
        lines.append("- **Top Contributors:**")
        for author, count in author_counter.most_common(top_n):
            lines.append(f"  - @{author} — {count} commits")
    if file_counter:
        lines.append("- **Most Modified Files:**")
        for fname, count in file_counter.most_common(top_n):
            lines.append(f"  - {fname} ({count} changes)")
    return "\n".join(lines)

def build_beautiful_summary(full_name, prs, all_prs, issues, commits, alerts, days=30):
    """
    Build a beautiful, presentable Markdown summary for the repository.
    """
    repo_title = f"# 🚀 GitHub Automation Summary for `{full_name}`\n"
    divider = "\n---\n"
    sections = [
        repo_title,
        "## 📂 Overview\n",
        f"- **Open PRs:** {len(prs)}\n- **Open Issues:** {len(issues)}\n- **Recent Commits ({days}d):** {len(commits)}\n",
        divider,
        "## 📝 Open Pull Requests\n",
        summarize_prs(prs, days=days),
        divider,
        "## 🕑 Pull Request History\n",
        summarize_all_prs(all_prs, days=days),
        divider,
        "## ❗ Open Issues\n",
        summarize_issues(issues, days=days),
        divider,
        "## 📈 Recent Commits\n",
        summarize_commits(commits, days=days),
        divider,
        summarize_commit_activity(commits, days=days),
        divider,
        "## 🛡️ Security Alerts\n",
        summarize_security_alerts(alerts),
        divider
    ]
    return "\n".join(sections)
