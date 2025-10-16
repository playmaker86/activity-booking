<template>
  <view class="callback-page">
    <view class="callback-container">
      <view v-if="loading" class="loading-state">
        <uni-load-more status="loading" />
        <text class="loading-text">处理登录信息中...</text>
      </view>
      
      <view v-else-if="success" class="success-state">
        <uni-icons type="checkmarkempty" size="80" color="#34c759" />
        <text class="success-text">登录成功</text>
        <text class="success-desc">正在跳转到首页...</text>
      </view>
      
      <view v-else class="error-state">
        <uni-icons type="clear" size="80" color="#ff3b30" />
        <text class="error-text">登录失败</text>
        <text class="error-desc">{{ errorMessage }}</text>
        <button class="retry-btn" @click="retryLogin">重新登录</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { wxWebLogin } from '@/api/user'
import { showToast } from '@/utils'

const loading = ref(true)
const success = ref(false)
const errorMessage = ref('')

// 处理微信回调
async function handleCallback() {
  try {
    loading.value = true
    
    // 获取URL参数
    const urlParams = new URLSearchParams(window.location.search)
    const code = urlParams.get('code')
    const state = urlParams.get('state')
    
    if (!code) {
      throw new Error('缺少授权码')
    }
    
    // 调用登录API
    const response = await wxWebLogin(code, state)
    
    // 保存token到localStorage
    localStorage.setItem('token', response.token)
    
    success.value = true
    showToast('登录成功', 'success')
    
    // 跳转到首页
    setTimeout(() => {
      window.location.href = '/pages/index/index'
    }, 2000)
    
  } catch (error) {
    console.error('登录失败:', error)
    errorMessage.value = error.message || '登录失败，请重试'
    showToast(errorMessage.value, 'error')
  } finally {
    loading.value = false
  }
}

// 重新登录
function retryLogin() {
  window.location.href = '/pages/web-login/web-login'
}

// 页面挂载时处理回调
onMounted(() => {
  handleCallback()
})
</script>

<style lang="scss" scoped>
.callback-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
}

.callback-container {
  background: white;
  border-radius: 20rpx;
  padding: 80rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500rpx;
  text-align: center;
}

.loading-state, .success-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.loading-text, .success-text, .error-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.success-text {
  color: #34c759;
}

.error-text {
  color: #ff3b30;
}

.success-desc, .error-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.retry-btn {
  margin-top: 20rpx;
  padding: 16rpx 32rpx;
  background: #007aff;
  color: white;
  border-radius: 8rpx;
  border: none;
  font-size: 28rpx;
}
</style>
