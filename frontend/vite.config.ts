import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Zadania na /api trafiaja do backendu Spring Boot (port 8080),
// dzieki temu nie trzeba konfigurowac CORS w trybie deweloperskim.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
})
