# src/fetchers/issues.py
from typing import List, Dict

def fetch_open_issues(repo, limit=50) -> List[Dict]:
    """
    Fetch open issues (excluding PRs) and return list of dicts.
    """
    results = []
    issues = repo.get_issues(state="open", sort="updated", direction="desc")
    count = 0
    for issue in issues:
        # skip pull requests (GitHub treats PRs as issues)
        if hasattr(issue, "pull_request") and issue.pull_request is not None:
            continue
        if count >= limit:
            break
        results.append({
            "number": issue.number,
            "title": issue.title,
            "user": issue.user.login if issue.user else None,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat() if issue.updated_at else None,
            "body": issue.body or "",
            "html_url": issue.html_url,
            "labels": [label.name for label in issue.get_labels()]
        })
        count += 1
    return results
