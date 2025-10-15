import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni.default ? uni.default() : uni()
  ],
  css: {
    preprocessorOptions: {
      scss: {
        // 使用现代 Sass API
        api: 'modern-compiler',
        // 静默弃用警告
        quietDeps: true
      }
    }
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    // uniapp 会自动处理构建配置
    sourcemap: false,
    minify: 'terser'
  }
})

