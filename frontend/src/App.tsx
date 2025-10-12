import { useEffect, useState } from 'react';
import { marked } from 'marked';
import RepoDropdown from './components/RepoDropdown';
import Tabs from './components/Tabs';
import Overview from './components/Overview';
import SectionPanel from './components/SectionPanel';
import './index.css';

const TABS = [
  { label: 'Open Pull Requests', key: 'open_prs' },
  { label: 'Pull Request History', key: 'pr_history' },
  { label: 'Open Issues', key: 'open_issues' },
  { label: 'Recent Commits', key: 'recent_commits' },
  { label: 'Commit Activity', key: 'commit_activity' },
  { label: 'Security Alerts', key: 'security_alerts' },
];

async function getRepoListFromJsonFiles(): Promise<string[]> {
  try {
    const files = import.meta.glob('/public/data/*_summary.json');
    return Object.keys(files).map((path) => {
      const file = path.split('/').pop() || '';
      const repo = file.replace('_summary.json', '').replace('__', '/');
      return repo;
    });
  } catch {
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

  const overview = summary ? {
    repo: selectedRepo,
    openPrs: (summary.summary.match(/\*\*Open PRs:\*\* (\d+)/)?.[1]) || 0,
    openIssues: (summary.summary.match(/\*\*Open Issues:\*\* (\d+)/)?.[1]) || 0,
    recentCommits: (summary.summary.match(/\*\*Recent Commits.*? (\d+)/)?.[1]) || 0,
  } : { repo: selectedRepo, openPrs: 0, openIssues: 0, recentCommits: 0 };

  function getTabContent(tabKey: string) {
    if (!summary) return <div style={{ color: '#9ca3af' }}>No data available.</div>;
    const md = summary.summary;
    const sections: Record<string, string> = {
      open_prs: /## 📝 Open Pull Requests\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      pr_history: /## 🕑 Pull Request History\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      open_issues: /## ❗ Open Issues\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      recent_commits: /## 📈 Recent Commits\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
      commit_activity: /### 📈 Commit Activity.*?\n([\s\S]*?)(?:\n---|$)/.exec(md)?.[1] || '',
      security_alerts: /## 🛡️ Security Alerts\n([\s\S]*?)\n---/.exec(md)?.[1] || '',
    };
    return <div style={{ maxWidth: 'none' }} dangerouslySetInnerHTML={{ __html: marked.parse(sections[tabKey] || '') }} />;
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(to bottom right, #f8fafc, #e2e8f0)',
      color: '#1e293b'
    }}>
      {/* Header */}
      <header style={{ 
        background: 'white', 
        borderBottom: '1px solid #e2e8f0',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{ 
          maxWidth: '1280px', 
          margin: '0 auto', 
          padding: '1rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <h1 style={{ 
            fontSize: '1.5rem', 
            fontWeight: 'bold',
            background: 'linear-gradient(to right, #2563eb, #9333ea)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            📊 RepoPulse Analytics
          </h1>
          <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
            Repository Monitoring Dashboard
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '2rem 1.5rem' }}>
        {/* Repository Selection */}
        <div style={{ marginBottom: '2rem' }}>
          <RepoDropdown repos={repos} selectedRepo={selectedRepo} onSelect={setSelectedRepo} />
        </div>

        {/* Overview Cards */}
        <Overview summary={overview} />

        {/* Tabs Navigation */}
        <div style={{ marginTop: '2rem' }}>
          <Tabs tabs={TABS} activeTab={activeTab} onTabChange={setActiveTab} />
        </div>

        {/* Content Panel */}
        <SectionPanel title={TABS.find(t => t.key === activeTab)?.label || ''}>
          {getTabContent(activeTab)}
        </SectionPanel>
      </main>
    </div>
  );
}

export default App;