import React from 'react';

interface RepoDropdownProps {
  repos: string[];
  selectedRepo: string;
  onSelect: (repo: string) => void;
}

const RepoDropdown: React.FC<RepoDropdownProps> = ({ repos, selectedRepo, onSelect }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-semibold mb-1" htmlFor="repo-select">
        Select Repository
      </label>
      <select
        id="repo-select"
        className="w-full p-2 border rounded bg-white dark:bg-[#161b22] dark:text-[#c9d1d9] border-gray-300 dark:border-[#30363d]"
        value={selectedRepo}
        onChange={e => onSelect(e.target.value)}
      >
        {repos.map(repo => (
          <option key={repo} value={repo}>
            {repo}
          </option>
        ))}
      </select>
    </div>
  );
};

export default RepoDropdown;
