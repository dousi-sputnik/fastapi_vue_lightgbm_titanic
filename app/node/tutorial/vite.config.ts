import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), vue()],
  server: {
    host: true,
    // これでポート番号を設定する
    port: 4000,
  },
});
