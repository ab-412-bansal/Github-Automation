from datetime import datetime
from typing import List, Dict

def fetch_all_prs(repo, limit=100, days=30) -> List[Dict]:
    """
    Fetch all PRs (open, closed, merged) created or updated within the last N days.
    limit: max number of PRs to fetch (to prevent huge runs)
    days: number of days to look back
    """
    from datetime import datetime, timedelta
    results = []
    since = datetime.utcnow() - timedelta(days=days)
    pulls = repo.get_pulls(state="all", sort="updated", direction="desc")
    count = 0
    for pr in pulls:
        created = pr.created_at if hasattr(pr, 'created_at') else None
        updated = pr.updated_at if hasattr(pr, 'updated_at') else None
        if created and created < since and (not updated or updated < since):
            continue
        if count >= limit:
            break
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
            "state": pr.state,
            "merged": getattr(pr, "merged", False),
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
            "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
            "body": pr.body or "",
            "html_url": pr.html_url,
            "files": files
        })
        count += 1
    return results

def fetch_open_prs(repo, limit=30, days=30) -> List[Dict]:
    """
    Fetch open PRs created or updated within the last N days and return a list of serializable dicts.
    limit: max number of PRs to fetch (to prevent huge runs)
    days: number of days to look back
    """
    from datetime import datetime, timedelta
    results = []
    since = datetime.utcnow() - timedelta(days=days)
    pulls = repo.get_pulls(state="open", sort="updated", direction="desc")
    count = 0
    for pr in pulls:
        created = pr.created_at if hasattr(pr, 'created_at') else None
        updated = pr.updated_at if hasattr(pr, 'updated_at') else None
        if created and created < since and (not updated or updated < since):
            continue
        if count >= limit:
            break
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
