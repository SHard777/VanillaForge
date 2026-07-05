import React from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import { useA2UI } from '../hooks/A2UIContext';

export default function NewsSentimentPanel() {
  const { a2uiState } = useA2UI();
  const data = a2uiState.sentiment;

  const renderGaugeAndLegend = () => {
    if (!data) return null;
    
    const scoreRaw = data.score || 0;
    // Map [-1, 1] to [0, 100]
    const displayScore = Math.round((scoreRaw + 1) * 50);

    const posCount = (data.headlines || []).filter(h => h.sentiment?.toLowerCase() === 'positive').length;
    const negCount = (data.headlines || []).filter(h => h.sentiment?.toLowerCase() === 'negative').length;
    const neuCount = (data.headlines || []).filter(h => {
      const s = h.sentiment?.toLowerCase();
      return s !== 'positive' && s !== 'negative';
    }).length;

    const option = {
      series: [
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          min: 0,
          max: 100,
          splitNumber: 4,
          radius: '90%',
          center: ['50%', '70%'],
          axisLine: {
            lineStyle: {
              width: 15,
              color: [
                [1, new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#EF4444' }, // Bearish (Red)
                  { offset: 0.5, color: '#EAB308' }, // Yellow
                  { offset: 1, color: '#10B981' }   // Bullish (Green)
                ])]
              ]
            }
          },
          pointer: {
            icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
            length: '55%',
            width: 6,
            offsetCenter: [0, '-20%'],
            itemStyle: { color: '#E2E8F0' } // Silver pointer
          },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: {
            distance: -35,
            color: '#94A3B8',
            fontSize: 10,
            formatter: function (value) {
              if (value === 0 || value === 25 || value === 50 || value === 75 || value === 100) return value;
              return '';
            }
          },
          detail: {
            fontSize: 32,
            fontWeight: 'bold',
            offsetCenter: [0, '15%'],
            valueAnimation: true,
            formatter: '{value}',
            color: '#F8FAFC'
          },
          data: [{ value: displayScore, name: 'Sentiment' }]
        }
      ]
    };

    return (
      <div className="flex items-center justify-between w-full h-[160px] relative">
        <div className="flex-1 h-full relative">
          <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
          {/* Curved Text Simulation using absolute positioning */}
          <div className="absolute left-[20%] bottom-[20%] -rotate-[35deg] text-[10px] font-bold tracking-widest text-[#EF4444]">
            BEARISH
          </div>
          <div className="absolute right-[20%] bottom-[20%] rotate-[35deg] text-[10px] font-bold tracking-widest text-[#10B981]">
            BULLISH
          </div>
        </div>
        
        {/* Side Legend */}
        <div className="w-[120px] flex flex-col justify-center gap-3 text-xs text-textSecondary px-2">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-[#10B981]"></div>
            <span className="text-white">Positive ({posCount})</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-[#64748B]"></div>
            <span className="text-white">Neutral ({neuCount})</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-[#EF4444]"></div>
            <span className="text-white">Bearish ({negCount})</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing font-semibold text-sm flex justify-between items-center shrink-0">
        <span className="uppercase">News Sentiment</span>
        {data?.ticker && <span className="text-xs bg-brand text-white px-2 py-0.5 rounded-full">{data.ticker}</span>}
      </div>

      {!data ? (
        <div className="flex-1 flex items-center justify-center text-textSecondary text-sm">
          Ask the agent for news sentiment to see details
        </div>
      ) : (
        <div className="flex-1 p-4 overflow-y-auto custom-scrollbar flex flex-col gap-2">
          <div className="flex-shrink-0">
            {renderGaugeAndLegend()}
          </div>
          
          <div className="space-y-3 mt-2">
            <h4 className="text-xs font-bold text-textSecondary tracking-wider">Latest news</h4>
            <div className="space-y-3">
              {(data.headlines || []).map((news, idx) => (
                <div key={idx} className="flex flex-col gap-1 border-b border-[#2A3241] pb-2 last:border-0">
                  <div className="flex justify-between items-start">
                    <span className="text-sm text-white font-medium leading-snug">{news.text}</span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-[10px] text-textSecondary">{news.date || 'Today'}</span>
                    <span className={`text-[10px] font-bold tracking-wide uppercase ${
                      news.sentiment === 'positive' ? 'text-[#10B981]' : 
                      news.sentiment === 'negative' ? 'text-[#EF4444]' : 
                      'text-textSecondary'
                    }`}>
                      {news.sentiment || 'NEUTRAL'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
