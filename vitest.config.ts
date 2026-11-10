import { defineConfig } from 'vitest/config'
import viteReact from '@vitejs/plugin-react'

// Separate from vite.config.ts so the devtools/router plugins don't run in tests.
export default defineConfig({
  resolve: { tsconfigPaths: true },
  plugins: [viteReact()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
  },
})
