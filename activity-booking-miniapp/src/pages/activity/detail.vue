<template>
  <view class="page">
    <view v-if="activity" class="activity-detail">
      <!-- 封面图 -->
      <image :src="activity.coverImage" class="cover-image" mode="aspectFill" />
      
      <!-- 活动信息 -->
      <view class="card activity-info">
        <text class="title">{{ activity.title }}</text>
        
        <view class="info-item">
          <text class="label">时间：</text>
          <text class="value">{{ formatDate(activity.startTime, 'YYYY-MM-DD HH:mm') }} - {{ formatDate(activity.endTime, 'HH:mm') }}</text>
        </view>
        
        <view class="info-item">
          <text class="label">地点：</text>
          <text class="value">{{ activity.location }}</text>
        </view>
        
        <view class="info-item">
          <text class="label">人数：</text>
          <text class="value">{{ activity.bookedCount }}/{{ activity.maxParticipants }}人</text>
        </view>
        
        <view class="info-item">
          <text class="label">费用：</text>
          <text class="value price">{{ activity.price === 0 ? '免费' : `¥${activity.price}` }}</text>
        </view>
      </view>
      
      <!-- 活动描述 -->
      <view class="card activity-desc">
        <text class="section-title">活动详情</text>
        <text class="desc-text">{{ activity.description }}</text>
      </view>
      
      <!-- 主办方信息 -->
      <view class="card organizer-info">
        <text class="section-title">主办方</text>
        <text class="organizer-name">{{ activity.organizer }}</text>
      </view>
    </view>
    
    <!-- 底部操作栏 -->
    <view class="bottom-bar">
      <button class="btn-book" @click="handleBook">立即预约</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onLoad } from '@dcloudio/uni-app'
import { useActivityStore } from '@/store/activity'
import { useUserStore } from '@/store/user'
import { formatDate, showToast } from '@/utils/index'

const activityStore = useActivityStore()
const userStore = useUserStore()
const activity = ref(null)

onLoad((options) => {
  if (options.id) {
    loadActivityDetail(options.id)
  }
})

// 加载活动详情
async function loadActivityDetail(id) {
  const res = await activityStore.fetchDetail(id)
  if (res) {
    activity.value = res
  }
}

// 预约活动
function handleBook() {
  if (!userStore.isLogin) {
    showToast('请先登录')
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login/login'
      })
    }, 1500)
    return
  }
  
  if (activity.value.bookedCount >= activity.value.maxParticipants) {
    showToast('活动已满员')
    return
  }
  
  uni.navigateTo({
    url: `/pages/booking/booking?activityId=${activity.value.id}`
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

.cover-image {
  width: 100%;
  height: 400rpx;
}

.activity-info {
  margin: 20rpx;
  
  .title {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    margin-bottom: 30rpx;
  }
  
  .info-item {
    display: flex;
    margin-bottom: 20rpx;
    font-size: 28rpx;
    
    .label {
      color: #666;
      width: 120rpx;
    }
    
    .value {
      flex: 1;
      color: #333;
      
      &.price {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 32rpx;
      }
    }
  }
}

.activity-desc, .organizer-info {
  margin: 20rpx;
  
  .section-title {
    display: block;
    font-size: 32rpx;
    font-weight: bold;
    margin-bottom: 20rpx;
  }
  
  .desc-text {
    color: #666;
    line-height: 1.6;
    font-size: 28rpx;
  }
  
  .organizer-name {
    color: #333;
    font-size: 28rpx;
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx;
  background-color: #fff;
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.05);
  
  .btn-book {
    width: 100%;
    background-color: #3cc51f;
    color: #fff;
    border-radius: 48rpx;
    height: 88rpx;
    line-height: 88rpx;
    font-size: 32rpx;
    border: none;
  }
}
</style>

