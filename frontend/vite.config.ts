import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Development server optimizations
  server: {
    port: 5173,
    host: true,
    // Enable HMR with optimized settings
    hmr: {
      overlay: false, // Disable error overlay for better performance
    },
    // Optimize file watching
    watch: {
      usePolling: false,
      interval: 100,
    },
  },

  // Build optimizations
  build: {
    target: 'esnext',
    minify: 'esbuild',
    sourcemap: false, // Disable sourcemaps in production for better performance
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          icons: ['lucide-react'],
        },
      },
    },
    // Optimize chunk size
    chunkSizeWarningLimit: 1000,
  },

  // Dependency optimization
  optimizeDeps: {
    include: ['react', 'react-dom'],
    exclude: ['lucide-react'], // Exclude from pre-bundling as it's large
  },

  // CSS optimizations
  css: {
    devSourcemap: false, // Disable CSS sourcemaps in development
  },

  // Preload optimizations
  preview: {
    port: 5173,
    host: true,
  },
});
