import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api/': {
        target: 'http://127.0.0.1:8000',
        // Keep the browser's Host and Origin aligned for Django's CSRF check.
        changeOrigin: false,
      },
    },
  },
});
// VA
