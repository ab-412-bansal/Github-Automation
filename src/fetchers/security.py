# src/fetchers/security.py
"""
Fetches security/vulnerability alerts for a repository using GitHub API.
"""
from typing import List, Dict

def fetch_security_alerts(repo) -> List[Dict]:
    """
    Fetch security/vulnerability alerts for the given repo.
    Returns a list of dicts summarizing each alert.
    """
    alerts = []
    try:
        # GitHub API: repo.get_vulnerability_alerts() is not in PyGithub as of 2025,
        # so we use the raw API as a workaround.
        alerts_api = repo._requester.requestJson(
            "GET",
            f"/repos/{repo.full_name}/dependabot/alerts",
            headers={"Accept": "application/vnd.github+json"}
        )
        for alert in alerts_api[1]:
            alerts.append({
                "number": alert.get("number"),
                "state": alert.get("state"),
                "dependency": alert.get("dependency", {}).get("package", {}).get("name"),
                "severity": alert.get("security_advisory", {}).get("severity"),
                "summary": alert.get("security_advisory", {}).get("summary"),
                "created_at": alert.get("created_at"),
                "updated_at": alert.get("updated_at"),
                "url": alert.get("html_url")
            })
    except Exception as e:
        alerts.append({"error": str(e)})
    return alerts
