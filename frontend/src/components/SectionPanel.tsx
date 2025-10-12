import React from 'react';

interface SectionPanelProps {
  title: string;
  children: React.ReactNode;
}

const SectionPanel: React.FC<SectionPanelProps> = ({ title, children }) => (
  <div className="mb-6 p-4 rounded border bg-white dark:bg-[#161b22] border-gray-200 dark:border-[#30363d]">
    <h3 className="text-md font-semibold mb-2">{title}</h3>
    <div>{children}</div>
  </div>
);

export default SectionPanel;
