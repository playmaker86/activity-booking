import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// 创建应用实例
export function createApp() {
  const app = createSSRApp(App)
  
  // 创建 Pinia 实例
  const pinia = createPinia()
  
  // 使用插件
  app.use(pinia)
  
  return {
    app,
    pinia
  }
}

