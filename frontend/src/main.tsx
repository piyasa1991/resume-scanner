import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';

// Import performance monitoring in development
if (import.meta.env.DEV) {
  import('../performance-monitor.js');
}

// Performance optimization: Use requestIdleCallback for non-critical initialization
const initApp = () => {
  const rootElement = document.getElementById('root');
  
  if (!rootElement) {
    throw new Error('Root element not found');
  }

  const root = createRoot(rootElement);
  
  root.render(
    <StrictMode>
      <App />
    </StrictMode>
  );
};

// Use requestIdleCallback if available, otherwise fallback to immediate execution
if ('requestIdleCallback' in window) {
  requestIdleCallback(initApp);
} else {
  // Fallback for browsers that don't support requestIdleCallback
  setTimeout(initApp, 0);
}
