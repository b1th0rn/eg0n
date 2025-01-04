import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from 'bootstrap-vue-next'
// import { resolve } from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    Components({
      resolvers: [BootstrapVueNextResolver()],
    }),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },

  build: {
    outDir: '../static/bundle',
    emptyOutDir: true,
    rollupOptions: {
        input: {
            app: './src/main.js' //entry point
        },
        output: {
            entryFileNames: `eg0nPortal.js`, // 
            chunkFileNames: `[name].js`,
            assetFileNames: `[name].[ext]`,
        },
    },
    minify: 'esbuild',
    cssCodeSplit: false
  }
})
