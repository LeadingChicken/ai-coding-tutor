import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Proxy tất cả các API requests đến server backend
      '/generate_exercise': 'http://localhost:8000',
      '/run_code': 'http://localhost:8000',
    },
  },
})
