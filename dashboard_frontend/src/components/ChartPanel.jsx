import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { useA2UI } from '../hooks/A2UIContext';

export default function ChartPanel() {
  const { a2uiState } = useA2UI();
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ticker = a2uiState.chart?.ticker;
  const companyName = a2uiState.chart?.company_name;

  const getHeaderInfo = () => {
    if (!chartData || chartData.length === 0) return null;
    const lastPoint = chartData[chartData.length - 1];
    return {
      price: lastPoint.Close.toFixed(2),
      date: lastPoint.Date
    };
  };

  const headerInfo = getHeaderInfo();

  useEffect(() => {
    if (!ticker) return;

    const fetchChartData = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`http://localhost:8000/api/data/chart?ticker=${ticker}`);
        const result = await res.json();
        
        if (result.error) {
          setError(result.error);
        } else {
          setChartData(result.data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChartData();
  }, [ticker]);

  const getOption = () => {
    if (!chartData || chartData.length === 0) return {};

    // ECharts Candlestick expects: [open, close, lowest, highest]
    const dates = chartData.map(item => item.Date);
    const data = chartData.map(item => [
      item.Open,
      item.Close,
      item.Low,
      item.High
    ]);

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' }
      },
      grid: {
        left: '10%',
        right: '5%',
        bottom: '15%',
        top: '10%'
      },
      xAxis: {
        type: 'category',
        data: dates,
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false, lineStyle: { color: '#2A3241' } },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisLabel: { color: '#94A3B8' }
      },
      yAxis: {
        scale: true,
        splitArea: { show: false },
        splitLine: { lineStyle: { color: '#2A3241', type: 'dashed' } },
        axisLabel: { color: '#94A3B8' }
      },
      dataZoom: [
        { type: 'inside', start: 0, end: 100 },
        { show: true, type: 'slider', bottom: 10, start: 0, end: 100, borderColor: '#2A3241', textStyle: { color: '#94A3B8' } }
      ],
      series: [
        {
          name: ticker,
          type: 'candlestick',
          data: data,
          itemStyle: {
            color: '#10B981',      // Up body (Close > Open)
            color0: '#EF4444',     // Down body (Close < Open)
            borderColor: '#10B981',
            borderColor0: '#EF4444'
          }
        }
      ]
    };
  };

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing font-semibold text-sm flex justify-between items-center shrink-0">
        <div className="flex items-center gap-2">
          <span>CHART</span>
          {companyName && <span className="text-xs text-textSecondary font-normal hidden sm:inline">{companyName}</span>}
        </div>
        {ticker && (
          <div className="flex items-center gap-3">
            {headerInfo && (
              <div className="flex items-center gap-2 text-xs">
                <span className="text-textSecondary">{headerInfo.date}</span>
                <span className="text-white font-mono">${headerInfo.price}</span>
              </div>
            )}
            <span className="text-xs bg-brand text-white px-2 py-0.5 rounded-full">{ticker}</span>
          </div>
        )}
      </div>
      
      <div className="flex-1 relative">
        {!ticker && (
          <div className="absolute inset-0 flex items-center justify-center text-textSecondary text-sm">
            Ask the agent to plot a ticker to view chart
          </div>
        )}
        
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center text-textSecondary text-sm bg-panel/50 z-10 backdrop-blur-sm">
            Loading {ticker} data...
          </div>
        )}
        
        {error && (
          <div className="absolute inset-0 flex items-center justify-center text-accentDown text-sm px-4 text-center">
            {error}
          </div>
        )}

        {chartData && !error && (
          <ReactECharts 
            option={getOption()} 
            style={{ height: '100%', width: '100%' }}
            notMerge={true}
          />
        )}
      </div>
    </div>
  );
}
