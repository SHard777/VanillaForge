import React from 'react';
import { useA2UI } from '../hooks/A2UIContext';

export default function CompanyInfoPanel() {
  const { a2uiState } = useA2UI();
  const data = a2uiState.company_info;

  if (!data) {
    return (
      <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
        <div className="px-4 py-3 border-b border-borderRing font-semibold text-sm">COMPANY INFORMATION</div>
        <div className="flex-1 flex items-center justify-center text-textSecondary text-sm">
          Ask the agent for company info to see details
        </div>
      </div>
    );
  }

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing font-semibold text-sm flex justify-between items-center shrink-0">
        <span>COMPANY INFORMATION</span>
        <span className="text-xs bg-brand text-white px-2 py-0.5 rounded-full">{data.ticker}</span>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto custom-scrollbar flex flex-col gap-5 text-sm">
        <div>
          <h2 className="text-lg font-bold text-white mb-1">{data.name}</h2>
          <div className="flex gap-2 text-xs text-textSecondary">
            <span className="bg-[#1E2536] px-2 py-1 rounded">{data.sector}</span>
            <span className="bg-[#1E2536] px-2 py-1 rounded">{data.industry}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">Market Cap</span>
              <span className="font-medium text-white">{data.marketCap}</span>
            </div>
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">P/E Ratio</span>
              <span className="font-medium text-white">{data.peRatio}</span>
            </div>
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">Beta</span>
              <span className="font-medium text-white">{data.beta}</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">52W High</span>
              <span className="font-medium text-accentUp">{data.fiftyTwoWeekHigh}</span>
            </div>
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">52W Low</span>
              <span className="font-medium text-accentDown">{data.fiftyTwoWeekLow}</span>
            </div>
            <div className="flex justify-between border-b border-[#2A3241] pb-1">
              <span className="text-textSecondary">Div Yield</span>
              <span className="font-medium text-white">{data.dividendYield}</span>
            </div>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mb-2">Description</h4>
          <p className="text-textSecondary leading-relaxed">{data.description}</p>
        </div>

        {data.businessSegments && (
          <div>
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mt-4 mb-2">Business Segments</h4>
            <p className="text-textSecondary leading-relaxed">{data.businessSegments}</p>
          </div>
        )}

        {data.competitivePosition && (
          <div>
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mt-4 mb-2">Competitive Position & Industry Context</h4>
            <p className="text-textSecondary leading-relaxed">{data.competitivePosition}</p>
          </div>
        )}

        {data.keyFinancialMetrics && (
          <div>
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mt-4 mb-2">Key Financial Metrics</h4>
            <p className="text-textSecondary leading-relaxed">{data.keyFinancialMetrics}</p>
          </div>
        )}

        {data.keyValuationMetrics && (
          <div>
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mt-4 mb-2">Key Valuation Metrics</h4>
            <p className="text-textSecondary leading-relaxed">{data.keyValuationMetrics}</p>
          </div>
        )}

        {data.investorTakeaways && (
          <div>
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider mt-4 mb-2">Investor Takeaways</h4>
            <p className="text-textSecondary leading-relaxed">{data.investorTakeaways}</p>
          </div>
        )}

      </div>
    </div>
  );
}
