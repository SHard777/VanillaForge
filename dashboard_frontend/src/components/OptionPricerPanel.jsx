import React, { useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { useA2UI } from '../hooks/A2UIContext';

export default function OptionPricerPanel() {
  const { a2uiState } = useA2UI();
  const [activeTab, setActiveTab] = useState('inputs'); // 'inputs' | 'payoff'
  
  const data = a2uiState.pricer; // e.g. { type: 'Call', spot: 100, strike: 105, vol: 0.2, rate: 0.05, div_yield: 0, maturity: 1, price: 5.4, delta: 0.45, gamma: 0.02, vega: 12.3, theta: -4.5 }

  const renderInputsAndGreeks = () => {
    if (!data) {
      return (
        <div className="flex-1 flex items-center justify-center text-textSecondary text-sm">
          Ask the agent to price an option to see details
        </div>
      );
    }

    return (
      <div className="flex flex-col gap-4 p-4 overflow-y-auto">
        <div className="flex justify-between items-center bg-[#1E2536] p-3 rounded-lg border border-borderRing">
          <span className="text-sm font-medium">Theoretical Price</span>
          <span className="text-xl font-bold text-brand">${data.price?.toFixed(2) || '0.00'}</span>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider">Inputs</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-textSecondary">Type</span><span className={`font-semibold ${data.type?.toLowerCase() === 'call' ? 'text-accentUp' : 'text-accentDown'}`}>{data.type || 'N/A'}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Spot</span><span>{data.spot}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Strike</span><span>{data.strike}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Volatility</span><span>{data.vol * 100}%</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Rate</span><span>{(data.rate * 100).toFixed(2)}%</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Div Yield</span><span>{(data.div_yield * 100).toFixed(2)}%</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Maturity (Y)</span><span>{data.maturity}</span></div>
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="text-xs font-bold text-textSecondary uppercase tracking-wider">Greeks</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-textSecondary">Delta</span><span>{data.delta?.toFixed(4)}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Gamma</span><span>{data.gamma?.toFixed(4)}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Vega</span><span>{data.vega?.toFixed(4)}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Theta</span><span>{data.theta?.toFixed(4)}</span></div>
              <div className="flex justify-between"><span className="text-textSecondary">Rho</span><span>{data.rho?.toFixed(4)}</span></div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderPayoffChart = () => {
    if (!data || !data.spot) {
      return (
        <div className="flex-1 flex items-center justify-center text-textSecondary text-sm">
          No data for payoff chart
        </div>
      );
    }

    const { type, spot, strike, price } = data;
    const isCall = type?.toLowerCase() === 'call';
    const maxSpot = spot * 2.5; // Per user request
    const step = maxSpot / 50;
    
    const chartData = [];
    for (let s = 0; s <= maxSpot; s += step) {
      let payoff = 0;
      if (isCall) {
        payoff = Math.max(s - strike, 0) - price;
      } else {
        payoff = Math.max(strike - s, 0) - price;
      }
      chartData.push([s, payoff]);
    }

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        formatter: (params) => `Spot: $${params[0].value[0].toFixed(2)}<br/>PnL: $${params[0].value[1].toFixed(2)}`
      },
      grid: { left: '15%', right: '5%', bottom: '15%', top: '10%' },
      xAxis: {
        type: 'value',
        name: 'Spot Price',
        nameLocation: 'middle',
        nameGap: 25,
        splitLine: { show: false },
        axisLabel: { color: '#94A3B8' }
      },
      yAxis: {
        type: 'value',
        name: 'PnL',
        splitLine: { lineStyle: { color: '#2A3241', type: 'dashed' } },
        axisLabel: { color: '#94A3B8' }
      },
      series: [
        {
          type: 'line',
          data: chartData,
          showSymbol: false,
          lineStyle: { width: 3, color: '#6366F1' },
          areaStyle: {
            color: {
              type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(99, 102, 241, 0.4)' },
                { offset: 1, color: 'rgba(99, 102, 241, 0)' }
              ]
            }
          },
          markLine: {
            data: [
              { yAxis: 0, lineStyle: { color: '#94A3B8' } },
              { xAxis: spot, label: { formatter: 'Current Spot' }, lineStyle: { color: '#EF4444', type: 'dashed' } }
            ]
          }
        }
      ]
    };

    return (
      <div className="flex-1 w-full h-full p-2">
        <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
      </div>
    );
  };

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <span className="font-semibold text-sm">OPTION PRICER</span>
          <span className="text-xs text-textSecondary font-medium hidden sm:inline">European options, Black-Scholes-Merton Model</span>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => setActiveTab('inputs')}
            className={`text-xs px-3 py-1 rounded-full transition-colors ${activeTab === 'inputs' ? 'bg-[#2A3241] text-white' : 'text-textSecondary hover:text-white'}`}
          >
            Inputs/Greeks
          </button>
          <button 
            onClick={() => setActiveTab('payoff')}
            className={`text-xs px-3 py-1 rounded-full transition-colors ${activeTab === 'payoff' ? 'bg-[#2A3241] text-white' : 'text-textSecondary hover:text-white'}`}
          >
            Pay-off
          </button>
        </div>
      </div>
      
      {activeTab === 'inputs' ? renderInputsAndGreeks() : renderPayoffChart()}
    </div>
  );
}
