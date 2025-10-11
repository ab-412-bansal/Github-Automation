# src/reporting/summary.py
"""
Reporting utilities for generating Markdown summaries of PRs, issues, commits, and security alerts.
"""
from typing import List, Dict

def summarize_prs(prs: List[Dict]) -> str:
    """
    Generate a Markdown summary of open pull requests.
    """
    if not prs:
        return "No open pull requests."
    lines = ["## Open Pull Requests\n"]
    for pr in prs:
        lines.append(f"- [#{pr['number']}]({pr['html_url']}): {pr['title']} (by @{pr['user']})")
    return "\n".join(lines)

def summarize_issues(issues: List[Dict]) -> str:
    """
    Generate a Markdown summary of open issues.
    """
    if not issues:
        return "No open issues."
    lines = ["## Open Issues\n"]
    for issue in issues:
        lines.append(f"- [#{issue['number']}]({issue['html_url']}): {issue['title']} (by @{issue['user']})")
    return "\n".join(lines)

def summarize_commits(commits: List[Dict]) -> str:
    """
    Generate a Markdown summary of recent commits (last 30 days).
    """
    if not commits:
        return "No recent commits."
    lines = ["## Recent Commits (Last 30 Days)\n"]
    for c in commits:
        lines.append(f"- [{c['sha'][:7]}]({c['html_url']}): {c['message'].splitlines()[0]} (by @{c['author']})")
    return "\n".join(lines)

def summarize_security_alerts(alerts: List[Dict]) -> str:
    """
    Generate a Markdown summary of security/vulnerability alerts.
    Handles cases where alerts may contain error strings or malformed data.
    """
    if not alerts:
        return "No security alerts."
    if isinstance(alerts[0], dict) and 'error' in alerts[0]:
        return f"Error fetching security alerts: {alerts[0]['error']}"
    lines = ["## Security Alerts\n"]
    for alert in alerts:
        if not isinstance(alert, dict):
            continue
        dep = alert.get('dependency', 'Unknown')
        sev = alert.get('severity', 'N/A')
        summ = alert.get('summary', 'No summary')
        state = alert.get('state', 'N/A')
        lines.append(f"- {dep} [{sev}] - {summ} (state: {state})")
    if len(lines) == 1:
        return "No security alerts."
    return "\n".join(lines)
