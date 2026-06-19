/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        // Code-split vendor libs so the initial bundle stays small.
        manualChunks: { react: ["react", "react-dom"] },
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    coverage: { provider: "v8", thresholds: { lines: 90, functions: 90 } },
  },
});
