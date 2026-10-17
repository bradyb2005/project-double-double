import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The FastAPI backend has no CORS middleware, so the dev server proxies /api to it.
// Run the backend with: uvicorn app.main:app --reload (port 8000).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
