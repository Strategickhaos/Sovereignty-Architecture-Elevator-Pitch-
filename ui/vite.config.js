import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  build: {
    outDir: '../dist-ui',
  },
  root: __dirname,
  publicDir: 'public',
  resolve: {
    alias: {
      '/src': path.resolve(__dirname, '../src'),
    },
  },
});
