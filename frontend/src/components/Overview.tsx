import React from 'react';

interface OverviewProps {
  summary: {
    openPrs: number;
    openIssues: number;
    recentCommits: number;
    repo: string;
  };
}

const Overview: React.FC<OverviewProps> = ({ summary }) => {
  return (
    <div className="mb-6 p-4 rounded border bg-white dark:bg-[#161b22] border-gray-200 dark:border-[#30363d]">
      <h2 className="text-lg font-semibold mb-2">Overview</h2>
      <div className="flex flex-wrap gap-8">
        <div>
          <div className="text-sm text-gray-500">Repository</div>
          <div className="font-mono">{summary.repo}</div>
        </div>
        <div>
          <div className="text-sm text-gray-500">Open PRs</div>
          <div className="font-bold text-[#0969da] dark:text-[#58a6ff]">{summary.openPrs}</div>
        </div>
        <div>
          <div className="text-sm text-gray-500">Open Issues</div>
          <div className="font-bold text-[#0969da] dark:text-[#58a6ff]">{summary.openIssues}</div>
        </div>
        <div>
          <div className="text-sm text-gray-500">Recent Commits</div>
          <div className="font-bold text-[#0969da] dark:text-[#58a6ff]">{summary.recentCommits}</div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
