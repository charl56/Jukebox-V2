import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.VITE_FRONT_URI || '',
  plugins: [
    vue(),
  ],
})
