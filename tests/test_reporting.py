# tests/test_reporting.py
from src.reporting.summary import summarize_prs, summarize_issues, summarize_commits, summarize_security_alerts

def test_summarize_prs():
    prs = [{"number": 1, "html_url": "url", "title": "Fix bug", "user": "alice"}]
    out = summarize_prs(prs)
    assert "Fix bug" in out

def test_summarize_issues():
    issues = [{"number": 2, "html_url": "url", "title": "Crash on load", "user": "bob"}]
    out = summarize_issues(issues)
    assert "Crash on load" in out

def test_summarize_commits():
    commits = [{"sha": "abc1234", "html_url": "url", "message": "Initial commit", "author": "carol"}]
    out = summarize_commits(commits)
    assert "Initial commit" in out

def test_summarize_security_alerts():
    alerts = [{"dependency": "requests", "severity": "high", "summary": "Vuln", "state": "open"}]
    out = summarize_security_alerts(alerts)
    assert "requests" in out
