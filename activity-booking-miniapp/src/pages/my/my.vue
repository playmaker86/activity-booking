<template>
  <view class="page">
    <!-- 用户信息 -->
    <view class="user-header card">
      <image 
        :src="userInfo?.avatar || defaultAvatar" 
        class="avatar" 
        mode="aspectFill"
      />
      <view class="user-info">
        <text class="nickname">{{ userInfo?.nickname || '未登录' }}</text>
        <text v-if="!isLogin" class="login-tip" @click="handleLogin">点击登录</text>
      </view>
    </view>
    
    <!-- 菜单列表 -->
    <view class="menu-list">
      <view class="menu-item card" @click="goToMyBookings">
        <view class="menu-left">
          <uni-icons type="calendar" size="20" color="#666"></uni-icons>
          <text class="menu-title">我的预约</text>
        </view>
        <uni-icons type="arrowright" size="16" color="#999"></uni-icons>
      </view>
      
      <view class="menu-item card" @click="handleLogout" v-if="isLogin">
        <view class="menu-left">
          <uni-icons type="back" size="20" color="#666"></uni-icons>
          <text class="menu-title">退出登录</text>
        </view>
        <uni-icons type="arrowright" size="16" color="#999"></uni-icons>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'
import { showModal, showToast } from '@/utils/index'

const userStore = useUserStore()
const defaultAvatar = '/static/images/default-avatar.png'

const isLogin = computed(() => userStore.isLogin)
const userInfo = computed(() => userStore.userInfo)

// 登录
async function handleLogin() {
  // 跳转到登录页面
  uni.navigateTo({
    url: '/pages/login/login'
  })
}

// 退出登录
async function handleLogout() {
  const confirmed = await showModal('确定要退出登录吗？')
  if (confirmed) {
    userStore.logout()
    showToast('已退出登录', 'success')
  }
}

// 跳转到我的预约
function goToMyBookings() {
  if (!isLogin.value) {
    showToast('请先登录')
    return
  }
  
  uni.navigateTo({
    url: '/pages/my/bookings'
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20rpx;
}

.user-header {
  display: flex;
  align-items: center;
  padding: 40rpx 20rpx;
  margin-bottom: 20rpx;
  
  .avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    margin-right: 30rpx;
  }
  
  .user-info {
    flex: 1;
    
    .nickname {
      display: block;
      font-size: 32rpx;
      font-weight: bold;
      margin-bottom: 10rpx;
    }
    
    .login-tip {
      font-size: 24rpx;
      color: #999;
    }
  }
}

.menu-list {
  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx 20rpx;
    margin-bottom: 20rpx;
    
    .menu-left {
      display: flex;
      align-items: center;
      gap: 16rpx;
    }
    
    .menu-title {
      font-size: 28rpx;
      color: #333;
    }
  }
}
</style>

