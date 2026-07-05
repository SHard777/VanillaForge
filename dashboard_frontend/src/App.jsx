import React from 'react';
import ChatPanel from './components/ChatPanel';
import ChartPanel from './components/ChartPanel';
import OptionPricerPanel from './components/OptionPricerPanel';
import CompanyInfoPanel from './components/CompanyInfoPanel';
import NewsSentimentPanel from './components/NewsSentimentPanel';
import JournalPanel from './components/JournalPanel';
import { Activity } from 'lucide-react';

function App() {
  return (
    <div className="h-screen bg-app text-textPrimary flex flex-col font-sans overflow-hidden">
      {/* Navbar */}
      <header className="h-14 border-b border-borderRing bg-panel flex items-center px-6 justify-between shrink-0">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-brand" />
          <h1 className="font-bold tracking-wide">VanillaForge</h1>
        </div>
        <div className="text-sm text-textSecondary font-medium">Terminal v1.0</div>
      </header>

      {/* Main Grid Layout - 3 rows, 2 columns */}
      <main className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-2 gap-4 overflow-y-auto">
        
        {/* Row 1 */}
        <div className="h-[450px]">
          <ChatPanel />
        </div>
        <div className="h-[450px]">
          <ChartPanel />
        </div>

        {/* Row 2 */}
        <div className="h-[380px]">
          <OptionPricerPanel />
        </div>
        <div className="h-[380px]">
          <CompanyInfoPanel />
        </div>

        {/* Row 3 */}
        <div className="h-[380px]">
          <NewsSentimentPanel />
        </div>
        <div className="h-[380px]">
          <JournalPanel />
        </div>

      </main>
    </div>
  );
}

export default App;
