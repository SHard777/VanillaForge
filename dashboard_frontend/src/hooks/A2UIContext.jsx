import React, { createContext, useContext, useState, useCallback } from 'react';

const A2UIContext = createContext(null);

export function A2UIProvider({ children }) {
  // Global state holding the latest A2UI data for each panel type
  const [a2uiState, setA2uiState] = useState({
    chart: null,        // { ticker: "AAPL" }
    pricer: null,       // { spot: 100, strike: 105, ... }
    company_info: null, // { name: "Apple", pe_ratio: 25, ... }
    sentiment: null,    // { score: 0.8, headlines: [...] }
  });

  // Central Registry Dispatcher
  const dispatchA2UIEvent = useCallback((action, data) => {
    setA2uiState((prev) => {
      switch (action) {
        case 'UPDATE_CHART':
          return { ...prev, chart: data };
        case 'UPDATE_PRICER':
          return { ...prev, pricer: data };
        case 'UPDATE_COMPANY_INFO':
          return { ...prev, company_info: data };
        case 'UPDATE_SENTIMENT':
          return { ...prev, sentiment: data };
        default:
          console.warn(`Unknown A2UI action: ${action}`);
          return prev;
      }
    });
  }, []);

  return (
    <A2UIContext.Provider value={{ a2uiState, dispatchA2UIEvent }}>
      {children}
    </A2UIContext.Provider>
  );
}

export function useA2UI() {
  const context = useContext(A2UIContext);
  if (!context) {
    throw new Error('useA2UI must be used within an A2UIProvider');
  }
  return context;
}
