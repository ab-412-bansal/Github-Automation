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

function getRepoListFromJsonFiles(): string[] {
  // This function should scan the data directory for *_summary.json files
  // For demo, hardcode or fetch from backend/static
  return [
    'ab-412-bansal/AlgoVision',
    'torvalds/linux',
    'ab-412-bansal/Startup-Success-Prediction-Project',
    'ab-412-bansal/Test-Security-Repository',
  ];
}

function App() {
  const [repos] = useState<string[]>(getRepoListFromJsonFiles());
  const [selectedRepo, setSelectedRepo] = useState<string>(repos[0]);
  const [summary, setSummary] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<string>(TABS[0].key);

  useEffect(() => {
    async function fetchSummary() {
      // Try to fetch the summary JSON for the selected repo
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
