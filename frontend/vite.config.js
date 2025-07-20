import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/upload': 'http://localhost:5000',
      // this redirects localhost:5173/upload to localhost:5000/upload
      '/items': 'http://localhost:5000',
    }
  }
})
