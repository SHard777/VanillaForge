import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { A2UIProvider } from './hooks/A2UIContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <A2UIProvider>
      <App />
    </A2UIProvider>
  </StrictMode>,
)
