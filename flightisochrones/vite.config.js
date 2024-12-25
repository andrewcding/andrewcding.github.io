import { defineConfig } from "vite";
import { viteStaticCopy } from "vite-plugin-static-copy";
import vue from "@vitejs/plugin-vue";

const mapboxSource = "node_modules/mapbox-gl"; // Adjust the source path if needed
const mapboxBaseUrl = "mapbox"; // Base URL for Mapbox assets

export default defineConfig({
  base: "/flightisochrones/",
  plugins: [
    vue(),
    viteStaticCopy({
      targets: [
        // Copy Mapbox GL JS assets if necessary
        { src: `${mapboxSource}/dist`, dest: mapboxBaseUrl },
        // Include additional assets if your project requires them
      ],
    }),
  ],
  server: {
    port: 3000,
    open: true,
  },
  preview: {
    port: 3010,
    open: true,
  },
  define: {
    MAPBOX_BASE_URL: JSON.stringify(mapboxBaseUrl),
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          mapbox: ["mapbox-gl"],
          turf: ["@turf/turf"],
        },
      },
    },
    chunkSizeWarningLimit: 5000,
  },
});
