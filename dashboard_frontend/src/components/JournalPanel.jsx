import React, { useState, useEffect } from 'react';

export default function JournalPanel() {
  const [activeTab, setActiveTab] = useState('trade'); // 'trade' | 'sentiment'
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // We fetch the journal on mount and when tab changes.
  // We can also poll it every 5 seconds to keep it fresh.
  useEffect(() => {
    const fetchJournal = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/api/mcp/journal?type=${activeTab}`);
        const result = await res.json();
        if (!result.error) {
          setData(result.data || []);
        } else {
          setData([]);
        }
      } catch (err) {
        console.error("Failed to fetch journal:", err);
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchJournal();
    
    const interval = setInterval(fetchJournal, 5000);
    return () => clearInterval(interval);
  }, [activeTab]);

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing flex justify-between items-center shrink-0">
        <span className="font-semibold text-sm uppercase">Journal</span>
        <div className="flex gap-2">
          <button 
            onClick={() => setActiveTab('trade')}
            className={`text-xs px-3 py-1 rounded-full transition-colors ${activeTab === 'trade' ? 'bg-[#2A3241] text-white' : 'text-textSecondary hover:text-white'}`}
          >
            Trade
          </button>
          <button 
            onClick={() => setActiveTab('sentiment')}
            className={`text-xs px-3 py-1 rounded-full transition-colors ${activeTab === 'sentiment' ? 'bg-[#2A3241] text-white' : 'text-textSecondary hover:text-white'}`}
          >
            Sentiment
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto custom-scrollbar">
        {loading && data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-textSecondary text-sm">Loading...</div>
        ) : data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-textSecondary text-sm">No entries found</div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-textSecondary uppercase bg-[#1E2536] sticky top-0">
              <tr>
                <th className="px-4 py-2 font-medium">Time</th>
                <th className="px-4 py-2 font-medium">Ticker</th>
                {activeTab === 'trade' ? (
                  <>
                    <th className="px-4 py-2 font-medium">Strategy</th>
                    <th className="px-4 py-2 font-medium">BSM Price</th>
                    <th className="px-4 py-2 font-medium">Volatility</th>
                  </>
                ) : (
                  <>
                    <th className="px-4 py-2 font-medium">Sentiment Score</th>
                  </>
                )}
                <th className="px-4 py-2 font-medium">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A3241]">
              {data.map((row, idx) => (
                <tr key={idx} className="hover:bg-[#1E2536]/50 transition-colors">
                  <td className="px-4 py-2 text-textSecondary whitespace-nowrap">{new Date(row.timestamp).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</td>
                  <td className="px-4 py-2 font-medium text-white">{row.ticker}</td>
                  
                  {activeTab === 'trade' ? (
                    <>
                      <td className="px-4 py-2 font-semibold text-white">
                        {row.strategy?.toUpperCase()}
                      </td>
                      <td className="px-4 py-2 text-white">${row.bsm_price?.toFixed(2)}</td>
                      <td className="px-4 py-2 text-textSecondary">{row.volatility ? (row.volatility * 100).toFixed(1) + '%' : '-'}</td>
                      <td className="px-4 py-2 text-textSecondary truncate max-w-[150px]" title={row.agent_notes}>{row.agent_notes || '-'}</td>
                    </>
                  ) : (
                    <>
                      {(() => {
                        const scoreNum = row.score || 0;
                        return (
                          <td className={`px-4 py-2 font-semibold ${
                            scoreNum > 50 ? 'text-accentUp' : 
                            scoreNum < 50 ? 'text-accentDown' : 'text-textSecondary'
                          }`}>
                            {scoreNum} / 100
                          </td>
                        );
                      })()}
                      <td className="px-4 py-2 text-textSecondary truncate max-w-[150px]" title={row.theme}>{row.theme || '-'}</td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
