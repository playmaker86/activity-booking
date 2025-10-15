<template>
  <view class="page">
    <view class="booking-list">
      <view 
        v-for="item in bookingList" 
        :key="item.id" 
        class="booking-item card"
      >
        <view class="booking-header">
          <text class="activity-title">{{ item.activity?.title }}</text>
          <text class="status" :class="'status-' + item.status">{{ getStatusText(item.status) }}</text>
        </view>
        
        <view class="booking-info">
          <text class="info-text">预约人：{{ item.name }}</text>
          <text class="info-text">手机号：{{ item.phone }}</text>
          <text class="info-text">人数：{{ item.participants }}人</text>
          <text class="info-text">预约时间：{{ formatDate(item.createdAt, 'YYYY-MM-DD HH:mm') }}</text>
        </view>
        
        <view class="booking-actions" v-if="item.status === 'confirmed'">
          <button class="btn-cancel" @click="handleCancel(item.id)">取消预约</button>
        </view>
      </view>
    </view>
    
    <view v-if="!loading && bookingList.length === 0" class="empty">
      <text>暂无预约记录</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyBookings, cancelBooking } from '@/api/booking'
import { formatDate, showModal, showToast } from '@/utils/index'

const bookingList = ref([])
const loading = ref(false)

onMounted(() => {
  loadBookings()
})

// 加载预约列表
async function loadBookings() {
  try {
    loading.value = true
    const res = await getMyBookings()
    bookingList.value = res.items || []
  } catch (error) {
    console.error('加载预约列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    'pending': '待确认',
    'confirmed': '已确认',
    'cancelled': '已取消',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 取消预约
async function handleCancel(id) {
  const confirmed = await showModal('确定要取消预约吗？')
  if (!confirmed) return
  
  try {
    await cancelBooking(id)
    showToast('取消成功', 'success')
    loadBookings()
  } catch (error) {
    console.error('取消预约失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20rpx;
}

.booking-list {
  .booking-item {
    margin-bottom: 20rpx;
    
    .booking-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20rpx;
      padding-bottom: 20rpx;
      border-bottom: 1rpx solid #f5f5f5;
      
      .activity-title {
        font-size: 32rpx;
        font-weight: bold;
        flex: 1;
      }
      
      .status {
        font-size: 24rpx;
        padding: 8rpx 16rpx;
        border-radius: 4rpx;
        
        &.status-pending {
          background-color: #fff3cd;
          color: #856404;
        }
        
        &.status-confirmed {
          background-color: #d4edda;
          color: #155724;
        }
        
        &.status-cancelled {
          background-color: #f8d7da;
          color: #721c24;
        }
        
        &.status-completed {
          background-color: #d1ecf1;
          color: #0c5460;
        }
      }
    }
    
    .booking-info {
      margin-bottom: 20rpx;
      
      .info-text {
        display: block;
        font-size: 26rpx;
        color: #666;
        margin-bottom: 10rpx;
      }
    }
    
    .booking-actions {
      display: flex;
      justify-content: flex-end;
      
      .btn-cancel {
        background-color: #ff6b6b;
        color: #fff;
        border: none;
        border-radius: 8rpx;
        padding: 16rpx 32rpx;
        font-size: 26rpx;
      }
    }
  }
}

.empty {
  text-align: center;
  padding: 100rpx;
  color: #999;
}
</style>

