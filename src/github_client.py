"""
GitHub API client wrapper.
"""

from github import Github
from src.config import GITHUB_TOKEN

# src/github_client.py
from github import Github
from src.config import GITHUB_TOKEN
import sys

if not GITHUB_TOKEN:
    print("ERROR: GITHUB_TOKEN missing in .env. Create .env with GITHUB_TOKEN=..."); sys.exit(1)

gh = Github(GITHUB_TOKEN, per_page=100)

def get_user():
    """Return the authenticated user object."""
    try:
        return gh.get_user()
    except Exception as e:
        raise RuntimeError(f"Failed to get authenticated user: {e}")

def get_repo(full_name: str):
    """Return a repository object by full_name (owner/repo)."""
    try:
        return gh.get_repo(full_name)
    except Exception as e:
        raise RuntimeError(f"Failed to get repo {full_name}: {e}")
