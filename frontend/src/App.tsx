import React, { useEffect, useState } from 'react';
import { marked } from 'marked';
import RepoDropdown from './components/RepoDropdown';
import Tabs from './components/Tabs';
import Overview from './components/Overview';
import SectionPanel from './components/SectionPanel';
import './index.css';
import 'github-markdown-css/github-markdown-light.css';
import 'github-markdown-css/github-markdown-dark.css';

const TABS = [
  { label: 'Open Pull Requests', key: 'open_prs' },
  { label: 'Pull Request History', key: 'pr_history' },
  { label: 'Open Issues', key: 'open_issues' },
  { label: 'Recent Commits', key: 'recent_commits' },
  { label: 'Commit Activity', key: 'commit_activity' },
  { label: 'Security Alerts', key: 'security_alerts' },
];

// Dynamically scan the /data directory for *_summary.json files
async function getRepoListFromJsonFiles(): Promise<string[]> {
  try {
    // Vite cannot read the filesystem at runtime, but we can use import.meta.glob for static files
    // This will create an object with keys like '/public/data/ab-412-bansal__Github-Automation_summary.json'
    const files = import.meta.glob('/public/data/*_summary.json');
    // Extract repo names from filenames
    return Object.keys(files).map((path) => {
      // path: '/public/data/ab-412-bansal__Github-Automation_summary.json'
      const file = path.split('/').pop() || '';
      const repo = file.replace('_summary.json', '').replace('__', '/');
      return repo;
    });
  } catch {
    // fallback: empty list
    return [];
  }
}

function App() {
  const [repos, setRepos] = useState<string[]>([]);
  const [selectedRepo, setSelectedRepo] = useState<string>('');
  const [summary, setSummary] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<string>(TABS[0].key);

  useEffect(() => {
    getRepoListFromJsonFiles().then((repoList) => {
      setRepos(repoList);
      if (repoList.length > 0) setSelectedRepo(repoList[0]);
    });
  }, []);

  useEffect(() => {
    async function fetchSummary() {
      if (!selectedRepo) return;
      const fileName = `${selectedRepo.replace('/', '__')}_summary.json`;
      try {
        const res = await fetch(`/data/${fileName}`);
        const data = await res.json();
        setSummary(data);
      } catch (e) {
        setSummary(null);
      }
    }
    fetchSummary();
  }, [selectedRepo]);

  // Parse overview numbers from summary
  const overview = summary ? {
    repo: selectedRepo,
    openPrs: (summary.summary.match(/\*\*Open PRs:\*\* (\d+)/)?.[1]) || 0,
    openIssues: (summary.summary.match(/\*\*Open Issues:\*\* (\d+)/)?.[1]) || 0,
    recentCommits: (summary.summary.match(/\*\*Recent Commits.*? (\d+)/)?.[1]) || 0,
  } : { repo: selectedRepo, openPrs: 0, openIssues: 0, recentCommits: 0 };

  // Extract tab content from markdown summary (very basic, for demo)
  function getTabContent(tabKey: string) {
    if (!summary) return <div className="text-gray-400">No data.</div>;
    const md = summary.summary;
    const sections: Record<string, string> = {
      open_prs: /## 📝 Open Pull Requests\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      pr_history: /## 🕑 Pull Request History\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      open_issues: /## ❗ Open Issues\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      recent_commits: /## 📈 Recent Commits\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      commit_activity: /### 📈 Commit Activity.*?\n([\s\S]*?)(?:\n---|$)/.exec(md)?.[1] || '',
      security_alerts: /## 🛡️ Security Alerts\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
    };
    return <div className="prose prose-sm dark:prose-invert" dangerouslySetInnerHTML={{ __html: marked.parse(sections[tabKey] || '') }} />;
  }

  return (
    <div className="min-h-screen bg-[#f6f8fa] dark:bg-[#0d1117] text-[#24292f] dark:text-[#c9d1d9] font-sans">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-2xl font-bold mb-6 tracking-tight text-[#24292f] dark:text-[#c9d1d9]">RepoPulse</h1>
        <RepoDropdown repos={repos} selectedRepo={selectedRepo} onSelect={setSelectedRepo} />
        <Overview summary={overview} />
        <Tabs tabs={TABS} activeTab={activeTab} onTabChange={setActiveTab} />
        <SectionPanel title={TABS.find(t => t.key === activeTab)?.label || ''}>
          {getTabContent(activeTab)}
        </SectionPanel>
      </div>
    </div>
  );
}

export default App;
