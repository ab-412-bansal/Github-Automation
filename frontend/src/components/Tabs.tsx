import React from 'react';

interface Tab {
  label: string;
  key: string;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onTabChange: (key: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, onTabChange }) => {
  return (
    <div style={{
      background: 'white',
      borderTopLeftRadius: '0.5rem',
      borderTopRightRadius: '0.5rem',
      border: '1px solid #e2e8f0',
      borderBottom: 'none',
      overflow: 'hidden'
    }}>
      <div style={{ 
        display: 'flex', 
        overflowX: 'auto',
        scrollbarWidth: 'thin'
      }}>
        {tabs.map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => onTabChange(tab.key)}
              style={{
                padding: '1rem 1.5rem',
                fontSize: '0.875rem',
                fontWeight: '500',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s',
                border: 'none',
                borderBottom: isActive ? '2px solid #2563eb' : '2px solid transparent',
                background: isActive ? 'rgba(239, 246, 255, 0.5)' : 'transparent',
                color: isActive ? '#2563eb' : '#64748b',
                cursor: 'pointer',
                position: 'relative'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = '#111827';
                  e.currentTarget.style.background = '#f8fafc';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = '#64748b';
                  e.currentTarget.style.background = 'transparent';
                }
              }}
            >
              {tab.label}
              {isActive && (
                <div style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: '2px',
                  background: 'linear-gradient(to right, #2563eb, #9333ea)'
                }} />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default Tabs;