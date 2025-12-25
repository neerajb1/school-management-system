import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true, // This ensures it fails if 3000 is taken, rather than switching to 5173
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        '.js': 'jsx', // This allows JSX inside .js files
      },
    },
  },
  esbuild: {
    loader: 'jsx',
    include: /src\/.*\.js$/, // Apply the JSX loader to all .js files in the src folder
    exclude: [],
  },
});