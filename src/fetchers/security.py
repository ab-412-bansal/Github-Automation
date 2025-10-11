# src/fetchers/security.py
"""
Fetches security/vulnerability alerts for a repository using GitHub API.
"""

import os
import requests
from typing import List, Dict, Union

def fetch_security_alerts(repo_full_name: str, github_token: str) -> Union[List[Dict], str]:
    """
    Fetch security/vulnerability alerts for the given repo using the GitHub REST API.
    Returns a list of dicts summarizing each alert, or a string error message.
    """
    url = f"https://api.github.com/repos/{repo_full_name}/dependabot/alerts"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            alerts = []
            for alert in response.json():
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
            return alerts
        elif response.status_code == 404:
            return "Security alerts are not enabled or you lack permission."
        elif response.status_code == 403:
            return "Token does not have required scopes (repo, security_events), or you do not have access to this repository's security alerts."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"
