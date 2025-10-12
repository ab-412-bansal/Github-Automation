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
    <div className="flex border-b border-gray-200 dark:border-[#30363d] mb-4">
      {tabs.map(tab => (
        <button
          key={tab.key}
          className={`px-4 py-2 -mb-px font-medium border-b-2 transition-colors duration-150 focus:outline-none ${
            activeTab === tab.key
              ? 'border-[#0969da] text-[#0969da] dark:border-[#58a6ff] dark:text-[#58a6ff] bg-white dark:bg-[#161b22]'
              : 'border-transparent text-gray-500 dark:text-[#8b949e] bg-transparent'
          }`}
          onClick={() => onTabChange(tab.key)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
};

export default Tabs;
