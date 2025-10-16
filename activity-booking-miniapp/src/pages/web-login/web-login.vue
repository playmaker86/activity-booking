<template>
  <view class="web-login-page">
    <view class="login-container">
      <!-- 标题 -->
      <view class="title">
        <text class="title-text">微信扫码登录</text>
        <text class="subtitle">使用微信扫描二维码登录</text>
      </view>

      <!-- 二维码容器 -->
      <view class="qrcode-container">
        <view v-if="qrCodeUrl" class="qrcode-wrapper">
          <image 
            :src="qrCodeUrl" 
            class="qrcode-image"
            mode="aspectFit"
          />
          <view class="qrcode-tips">
            <text class="tip-text">请使用微信扫描二维码</text>
          </view>
        </view>
        
        <view v-else-if="loading" class="loading-wrapper">
          <uni-load-more status="loading" />
          <text class="loading-text">生成二维码中...</text>
        </view>
        
        <view v-else class="error-wrapper">
          <uni-icons type="info" size="60" color="#ff4757" />
          <text class="error-text">二维码生成失败</text>
          <button class="retry-btn" @click="generateQrCode">重新生成</button>
        </view>
      </view>

      <!-- 登录状态 -->
      <view class="login-status">
        <view v-if="status === 'waiting'" class="status-item">
          <uni-icons type="scan" size="40" color="#007aff" />
          <text class="status-text">等待扫码</text>
        </view>
        
        <view v-else-if="status === 'scanning'" class="status-item">
          <uni-icons type="scan" size="40" color="#ff9500" />
          <text class="status-text">扫码成功，请在手机上确认</text>
        </view>
        
        <view v-else-if="status === 'success'" class="status-item success">
          <uni-icons type="checkmarkempty" size="40" color="#34c759" />
          <text class="status-text">登录成功</text>
        </view>
        
        <view v-else-if="status === 'error'" class="status-item error">
          <uni-icons type="clear" size="40" color="#ff3b30" />
          <text class="status-text">登录失败，请重试</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="actions">
        <button 
          class="refresh-btn"
          @click="generateQrCode"
          :disabled="loading"
        >
          {{ loading ? '生成中...' : '刷新二维码' }}
        </button>
        
        <button 
          class="cancel-btn"
          @click="cancelLogin"
        >
          取消登录
        </button>
      </view>

      <!-- 登录说明 -->
      <view class="login-tips">
        <text class="tip-text">1. 打开微信扫描上方二维码</text>
        <text class="tip-text">2. 在微信中确认登录</text>
        <text class="tip-text">3. 登录成功后自动跳转</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getWxWebLoginUrl, wxWebLogin } from '@/api/user'
import { showToast } from '@/utils'

const qrCodeUrl = ref('')
const loading = ref(false)
const status = ref('waiting') // waiting, scanning, success, error
const pollTimer = ref(null)
const state = ref('')

// 生成二维码
async function generateQrCode() {
  loading.value = true
  status.value = 'waiting'
  
  try {
    // 生成回调URL
    const redirectUri = encodeURIComponent(`${window.location.origin}/auth/callback`)
    const response = await getWxWebLoginUrl(redirectUri)
    
    qrCodeUrl.value = response.auth_url
    state.value = response.state
    
    // 开始轮询检查登录状态
    startPolling()
    
  } catch (error) {
    console.error('生成二维码失败:', error)
    status.value = 'error'
    showToast('二维码生成失败', 'error')
  } finally {
    loading.value = false
  }
}

// 开始轮询检查登录状态
function startPolling() {
  // 这里应该实现一个轮询机制来检查用户是否已经扫码并确认
  // 由于微信网页授权是回调模式，这里简化处理
  pollTimer.value = setInterval(() => {
    // 实际项目中，这里应该调用后端API检查登录状态
    // 或者通过WebSocket实时通信
  }, 2000)
}

// 停止轮询
function stopPolling() {
  if (pollTimer.value) {
    clearInterval(pollTimer.value)
    pollTimer.value = null
  }
}

// 处理微信回调
async function handleWxCallback(code, callbackState) {
  if (callbackState !== state.value) {
    status.value = 'error'
    showToast('登录状态异常', 'error')
    return
  }
  
  try {
    status.value = 'scanning'
    const response = await wxWebLogin(code, callbackState)
    
    // 保存token
    localStorage.setItem('token', response.token)
    
    status.value = 'success'
    showToast('登录成功', 'success')
    
    // 跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
    
  } catch (error) {
    console.error('登录失败:', error)
    status.value = 'error'
    showToast('登录失败', 'error')
  }
}

// 取消登录
function cancelLogin() {
  stopPolling()
  uni.navigateBack()
}

// 页面挂载时生成二维码
onMounted(() => {
  generateQrCode()
})

// 页面卸载时清理定时器
onUnmounted(() => {
  stopPolling()
})

// 监听URL变化（用于处理微信回调）
onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')
  const callbackState = urlParams.get('state')
  
  if (code && callbackState) {
    handleWxCallback(code, callbackState)
  }
})
</script>

<style lang="scss" scoped>
.web-login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
}

.login-container {
  background: white;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600rpx;
}

.title {
  text-align: center;
  margin-bottom: 60rpx;
  
  .title-text {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
  }
  
  .subtitle {
    font-size: 28rpx;
    color: #666;
  }
}

.qrcode-container {
  display: flex;
  justify-content: center;
  margin-bottom: 40rpx;
}

.qrcode-wrapper {
  text-align: center;
  
  .qrcode-image {
    width: 400rpx;
    height: 400rpx;
    border-radius: 10rpx;
    border: 2rpx solid #eee;
  }
  
  .qrcode-tips {
    margin-top: 20rpx;
    
    .tip-text {
      font-size: 24rpx;
      color: #666;
    }
  }
}

.loading-wrapper, .error-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 0;
  
  .loading-text, .error-text {
    margin-top: 20rpx;
    font-size: 28rpx;
    color: #666;
  }
  
  .retry-btn {
    margin-top: 20rpx;
    padding: 16rpx 32rpx;
    background: #007aff;
    color: white;
    border-radius: 8rpx;
    border: none;
    font-size: 24rpx;
  }
}

.login-status {
  margin-bottom: 40rpx;
  
  .status-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16rpx;
    
    .status-text {
      font-size: 28rpx;
      color: #666;
    }
    
    &.success .status-text {
      color: #34c759;
    }
    
    &.error .status-text {
      color: #ff3b30;
    }
  }
}

.actions {
  display: flex;
  gap: 20rpx;
  margin-bottom: 40rpx;
  
  .refresh-btn, .cancel-btn {
    flex: 1;
    height: 80rpx;
    border-radius: 40rpx;
    border: none;
    font-size: 28rpx;
  }
  
  .refresh-btn {
    background: #007aff;
    color: white;
    
    &:disabled {
      opacity: 0.6;
    }
  }
  
  .cancel-btn {
    background: #f2f2f2;
    color: #666;
  }
}

.login-tips {
  .tip-text {
    display: block;
    font-size: 24rpx;
    color: #999;
    margin-bottom: 8rpx;
    text-align: center;
  }
}
</style>
