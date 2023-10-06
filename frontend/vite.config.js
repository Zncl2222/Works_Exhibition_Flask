import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default ({ mode }) => {
  process.env = {
    ...process.env,
    ...loadEnv(mode, resolve(process.cwd(), "../")),
  };
  return defineConfig({
    plugins: [react()],
    test: {
      globals: true,
      environment: "jsdom",
    },
    build: {
      rollupOptions: {
        external: ["react", "react-router", "react-router-dom", "redux"],
        output: {
          globals: {
            react: "React",
          },
        },
        outDir: "build",
      },
    },
    server: {
      host: "0.0.0.0",
      https: false,
      port: process.env.VITE_FRONTEND_PORT,
      proxy: {
        "^/(api)/.*": {
          target: process.env.VITE_BACKEND_HOST,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  });
};
