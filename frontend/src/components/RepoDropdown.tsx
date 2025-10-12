import React from 'react';

interface RepoDropdownProps {
  repos: string[];
  selectedRepo: string;
  onSelect: (repo: string) => void;
}

const RepoDropdown: React.FC<RepoDropdownProps> = ({ repos, selectedRepo, onSelect }) => {
  return (
    <div style={{
      background: 'white',
      borderRadius: '0.5rem',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      border: '1px solid #e2e8f0',
      padding: '1.5rem'
    }}>
      <label 
        htmlFor="repo-select" 
        style={{ 
          display: 'block', 
          fontSize: '0.875rem', 
          fontWeight: '600', 
          color: '#374151',
          marginBottom: '0.75rem'
        }}
      >
        Select Repository
      </label>
      <div style={{ position: 'relative' }}>
        <select
          id="repo-select"
          value={selectedRepo}
          onChange={(e) => onSelect(e.target.value)}
          style={{
            width: '100%',
            padding: '0.75rem 2.5rem 0.75rem 1rem',
            background: '#f8fafc',
            border: '1px solid #cbd5e1',
            borderRadius: '0.5rem',
            color: '#111827',
            fontFamily: 'monospace',
            fontSize: '0.875rem',
            cursor: 'pointer',
            outline: 'none',
            appearance: 'none'
          }}
          onFocus={(e) => {
            e.target.style.borderColor = '#3b82f6';
            e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
          }}
          onBlur={(e) => {
            e.target.style.borderColor = '#cbd5e1';
            e.target.style.boxShadow = 'none';
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#f1f5f9';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#f8fafc';
          }}
        >
          {repos.map((repo) => (
            <option key={repo} value={repo}>
              {repo}
            </option>
          ))}
        </select>
        <div style={{
          pointerEvents: 'none',
          position: 'absolute',
          top: '50%',
          right: '0.75rem',
          transform: 'translateY(-50%)',
          color: '#6b7280'
        }}>
          <svg style={{ width: '1.25rem', height: '1.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default RepoDropdown;