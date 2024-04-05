import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.BASEURL,
  plugins: [vue()],
  test: {
    globalSetup: './vitest.global-setup.ts',
    environment: 'jsdom'
  },
  envPrefix: "PUBLIC_"
})
