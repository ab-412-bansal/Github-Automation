# src/fetchers/commits.py
from datetime import datetime, timedelta
from typing import List, Dict

def fetch_commits_last_30_days(repo, limit=200, days=30) -> List[Dict]:
    """
    Fetch commits for last N days. Returns serializable dicts.
    limit: maximum commits to fetch
    days: number of days to look back
    """
    from datetime import datetime, timedelta
    since = datetime.utcnow() - timedelta(days=days)
    results = []
    commits = repo.get_commits(since=since)
    count = 0
    for c in commits:
        if count >= limit:
            break
        # commit author (note: may be None for unlinked commits)
        author = None
        try:
            author = c.author.login if c.author else (c.commit.author.name if c.commit and c.commit.author else None)
        except Exception:
            author = None
        # Attempt to get changed files for commit (slower)
        files = []
        try:
            full = repo.get_commit(c.sha)
            for f in full.files:
                files.append({"filename": f.filename, "additions": f.additions, "deletions": f.deletions})
        except Exception:
            files = []
        results.append({
            "sha": c.sha,
            "author": author,
            "message": c.commit.message,
            "date": c.commit.author.date.isoformat() if c.commit and c.commit.author and c.commit.author.date else None,
            "html_url": c.html_url,
            "files": files
        })
        count += 1
    return results
