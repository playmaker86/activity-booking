<template>
  <view class="login-page">
    <view class="login-container">
      <!-- 标题 -->
      <view class="title">
        <text class="title-text">欢迎使用活动预约系统</text>
        <text class="subtitle">请选择登录方式</text>
      </view>

      <!-- 微信登录按钮 -->
      <view class="login-buttons">
        <button 
          class="wx-login-btn"
          @click="handleWxLogin"
          :disabled="loginLoading"
        >
          <view class="btn-content">
            <image 
              class="wx-icon" 
              src="/static/icons/wechat.png" 
              mode="aspectFit"
            />
            <text class="btn-text">
              {{ loginLoading ? '登录中...' : '微信授权登录' }}
            </text>
          </view>
        </button>
      </view>

      <!-- 登录说明 -->
      <view class="login-tips">
        <text class="tip-text">登录即表示同意</text>
        <text class="link-text" @click="showPrivacy">《隐私政策》</text>
        <text class="tip-text">和</text>
        <text class="link-text" @click="showTerms">《用户协议》</text>
      </view>
    </view>

    <!-- 隐私政策弹窗 -->
    <uni-popup ref="privacyPopup" type="center">
      <view class="popup-content">
        <view class="popup-header">
          <text class="popup-title">隐私政策</text>
          <uni-icons 
            type="close" 
            size="20" 
            @click="closePrivacy"
          />
        </view>
        <scroll-view class="popup-body" scroll-y>
          <text class="popup-text">
            我们重视您的隐私保护，在使用微信登录时，我们只会获取必要的用户信息用于身份验证和提供服务。
            我们承诺不会泄露您的个人信息给第三方。
          </text>
        </scroll-view>
      </view>
    </uni-popup>

    <!-- 用户协议弹窗 -->
    <uni-popup ref="termsPopup" type="center">
      <view class="popup-content">
        <view class="popup-header">
          <text class="popup-title">用户协议</text>
          <uni-icons 
            type="close" 
            size="20" 
            @click="closeTerms"
          />
        </view>
        <scroll-view class="popup-body" scroll-y>
          <text class="popup-text">
            使用本应用即表示您同意遵守相关服务条款。请合理使用本应用，不得进行任何违法违规的行为。
          </text>
        </scroll-view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { useUser } from '@/composables/useUser'
import { showToast } from '@/utils'

const { login, loginLoading } = useUser()

// 处理微信登录
async function handleWxLogin() {
  const success = await login()
  if (success) {
    showToast('登录成功', 'success')
    // 登录成功后返回上一页或跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  }
}

// 显示隐私政策
function showPrivacy() {
  this.$refs.privacyPopup.open()
}

// 关闭隐私政策
function closePrivacy() {
  this.$refs.privacyPopup.close()
}

// 显示用户协议
function showTerms() {
  this.$refs.termsPopup.open()
}

// 关闭用户协议
function closeTerms() {
  this.$refs.termsPopup.close()
}
</script>

<style lang="scss" scoped>
.login-page {
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
  margin-bottom: 80rpx;
  
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

.login-buttons {
  margin-bottom: 60rpx;
}

.wx-login-btn {
  width: 100%;
  height: 100rpx;
  background: #07c160;
  border-radius: 50rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:disabled {
    opacity: 0.6;
  }
  
  .btn-content {
    display: flex;
    align-items: center;
    gap: 20rpx;
  }
  
  .wx-icon {
    width: 40rpx;
    height: 40rpx;
  }
  
  .btn-text {
    color: white;
    font-size: 32rpx;
    font-weight: 500;
  }
}

.login-tips {
  text-align: center;
  font-size: 24rpx;
  color: #999;
  line-height: 1.5;
  
  .link-text {
    color: #667eea;
    text-decoration: underline;
  }
}

.popup-content {
  background: white;
  border-radius: 20rpx;
  width: 600rpx;
  max-height: 800rpx;
  overflow: hidden;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 40rpx;
  border-bottom: 1rpx solid #eee;
  
  .popup-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }
}

.popup-body {
  padding: 40rpx;
  max-height: 600rpx;
  
  .popup-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
  }
}
</style>
