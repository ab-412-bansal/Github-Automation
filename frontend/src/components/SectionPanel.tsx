import React from 'react';

interface SectionPanelProps {
  title: string;
  children: React.ReactNode;
}

const SectionPanel: React.FC<SectionPanelProps> = ({ title, children }) => {
  return (
    <div style={{
      background: 'white',
      borderBottomLeftRadius: '0.5rem',
      borderBottomRightRadius: '0.5rem',
      border: '1px solid #e2e8f0',
      borderTop: 'none',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
    }}>
      <div style={{ padding: '2rem' }}>
        <h2 style={{
          fontSize: '1.25rem',
          fontWeight: 'bold',
          color: '#111827',
          marginBottom: '1.5rem',
          paddingBottom: '0.75rem',
          borderBottom: '1px solid #e2e8f0'
        }}>
          {title}
        </h2>
        <div style={{ color: '#374151', lineHeight: '1.6' }}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default SectionPanel;