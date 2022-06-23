import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";
import tsConfigPaths from "vite-tsconfig-paths";
import WindiCSS from 'vite-plugin-windicss'
import jotaiDebugLabel from "jotai/babel/plugin-debug-label";
import jotaiReactRefresh from "jotai/babel/plugin-react-refresh";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({ babel: { plugins: [jotaiDebugLabel, jotaiReactRefresh] } }),
    tsConfigPaths(),
    WindiCSS()
  ],
  resolve: {
    alias: [
      { find: "@", replacement: resolve(__dirname, "./src") },
    ]
  },
  server: {
    proxy: {
      "/graphql": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        secure: false,
        ws: true,
        // rewrite: path => path.replace(/^\/graphql/, "")
      }
      // with RegEx
      // "^/fallback/.*": {
      //   target: "http://localhost:8000",
      //   changeOrigin: true,
      //   rewrite: path => path.replace(/^\/fallback/, "")
      // }
    }
  },
  esbuild: {
    jsxFactory: "h",
    jsxFragment: "Fragment",
  }
});
