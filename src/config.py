# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()


"""
Configuration loader for environment variables and CLI overrides.
"""

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
if not GITHUB_TOKEN:
	raise RuntimeError("GITHUB_TOKEN missing. Please set it in your .env file or environment.")


WORKING_REPOS = [r.strip() for r in os.getenv("WORKING_REPOS", "").split(",") if r.strip()]
# Default fallback to None; main will decide behavior

# Git automation config
GIT_USER_NAME = os.getenv("GIT_USER_NAME", "").strip()
GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL", "").strip()
