/**
 * 应用配置
 * 根据环境变量自动加载对应的配置
 */

// 获取环境变量
const env = import.meta.env

// 当前环境模式
const MODE = env.MODE || 'development'

// 基础配置
const baseConfig = {
  // 应用信息
  appName: env.VITE_APP_TITLE || '活动预约',
  appVersion: '1.0.0',
  
  // 请求配置
  baseURL: env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: parseInt(env.VITE_REQUEST_TIMEOUT) || 10000,
  
  // 调试模式
  debug: env.VITE_DEBUG === 'true' || MODE === 'development',
  
  // 当前环境
  mode: MODE,
  
  // 分页配置
  pageSize: 10,
  
  // 缓存配置
  cachePrefix: 'activity_booking_',
  
  // 图片配置
  imageMaxSize: 5 * 1024 * 1024, // 5MB
  imageTypes: ['jpg', 'jpeg', 'png', 'gif', 'webp'],
  
  // 文件上传地址
  uploadURL: env.VITE_UPLOAD_URL || `${env.VITE_API_BASE_URL}/upload`,
  
  // 静态资源地址
  staticURL: env.VITE_STATIC_URL || 'http://localhost:8000/static'
}

// 开发环境下打印配置信息
if (baseConfig.debug) {
  console.log('='.repeat(50))
  console.log('当前环境:', baseConfig.mode)
  console.log('API 地址:', baseConfig.baseURL)
  console.log('调试模式:', baseConfig.debug)
  console.log('='.repeat(50))
}

export default baseConfig


