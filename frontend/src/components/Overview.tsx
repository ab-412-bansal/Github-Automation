import React from 'react';

interface OverviewProps {
  summary: {
    repo: string;
    openPrs: number | string;
    openIssues: number | string;
    recentCommits: number | string;
  };
}

const Overview: React.FC<OverviewProps> = ({ summary }) => {
  const stats = [
    {
      label: 'Open Pull Requests',
      value: summary.openPrs,
      icon: '🔀',
      gradient: 'linear-gradient(to right, #3b82f6, #2563eb)',
      bg: '#eff6ff',
      border: '#bfdbfe',
    },
    {
      label: 'Open Issues',
      value: summary.openIssues,
      icon: '❗',
      gradient: 'linear-gradient(to right, #ef4444, #dc2626)',
      bg: '#fef2f2',
      border: '#fecaca',
    },
    {
      label: 'Recent Commits',
      value: summary.recentCommits,
      icon: '📝',
      gradient: 'linear-gradient(to right, #10b981, #059669)',
      bg: '#f0fdf4',
      border: '#bbf7d0',
    },
  ];

  return (
    <div>
      {/* Repository Info */}
      <div style={{
        background: 'white',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        border: '1px solid #e2e8f0',
        padding: '1.5rem',
        marginBottom: '1.5rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ fontSize: '2rem' }}>📦</div>
          <div>
            <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827', marginBottom: '0.25rem' }}>
              Repository Overview
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', fontFamily: 'monospace' }}>
              {summary.repo}
            </p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1.5rem'
      }}>
        {stats.map((stat, index) => (
          <div
            key={index}
            style={{
              background: stat.bg,
              border: `1px solid ${stat.border}`,
              borderRadius: '0.5rem',
              padding: '1.5rem',
              transition: 'all 0.2s',
              cursor: 'default'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.transform = 'scale(1.02)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <span style={{ fontSize: '2rem' }}>{stat.icon}</span>
              <div style={{ 
                fontSize: '2.25rem', 
                fontWeight: 'bold',
                background: stat.gradient,
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                {stat.value}
              </div>
            </div>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151' }}>
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Overview;