import { defineConfig } from 'vite';

export default defineConfig({
  server: { proxy: { '/agent': 'http://localhost:8000' } },
});
