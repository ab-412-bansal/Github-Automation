# tests/test_fetchers.py
from src.fetchers.commits import fetch_commits_last_30_days
from src.fetchers.issues import fetch_open_issues
from src.fetchers.prs import fetch_open_prs
from src.fetchers.security import fetch_security_alerts
from src.github_client import get_repo
import os

# Use a public repo for testing
REPO = os.environ.get('TEST_REPO', 'psf/requests')

def test_fetch_commits():
    repo = get_repo(REPO)
    commits = fetch_commits_last_30_days(repo, limit=5)
    assert isinstance(commits, list)
    assert all('sha' in c for c in commits)

def test_fetch_issues():
    repo = get_repo(REPO)
    issues = fetch_open_issues(repo, limit=5)
    assert isinstance(issues, list)
    assert all('number' in i for i in issues)

def test_fetch_prs():
    repo = get_repo(REPO)
    prs = fetch_open_prs(repo, limit=5)
    assert isinstance(prs, list)
    assert all('number' in p for p in prs)

def test_fetch_security_alerts():
    repo = get_repo(REPO)
    alerts = fetch_security_alerts(repo)
    assert isinstance(alerts, list)
