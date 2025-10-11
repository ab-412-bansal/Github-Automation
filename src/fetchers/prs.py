# src/fetchers/prs.py
from datetime import datetime
from typing import List, Dict

def fetch_open_prs(repo, limit=30) -> List[Dict]:
    """
    Fetch open PRs and return a list of serializable dicts.
    limit: max number of PRs to fetch (to prevent huge runs)
    """
    results = []
    pulls = repo.get_pulls(state="open", sort="updated", direction="desc")
    count = 0
    for pr in pulls:
        if count >= limit:
            break
        # fetch changed files list (small repos OK)
        files = []
        try:
            for f in pr.get_files():
                files.append({"filename": f.filename, "additions": f.additions, "deletions": f.deletions})
        except Exception:
            files = []
        results.append({
            "number": pr.number,
            "title": pr.title,
            "user": pr.user.login if pr.user else None,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
            "body": pr.body or "",
            "html_url": pr.html_url,
            "files": files
        })
        count += 1
    return results
