<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-box">
        <uni-icons type="search" size="20" color="#999"></uni-icons>
        <input 
          class="search-input" 
          type="text" 
          placeholder="搜索活动" 
          v-model="keyword"
          @confirm="handleSearch"
        />
      </view>
    </view>

    <!-- 活动列表 -->
    <view class="activity-list">
      <view 
        v-for="item in activityList" 
        :key="item.id" 
        class="activity-item card"
        @click="goToDetail(item.id)"
      >
        <!-- 左侧正方形图片 -->
        <view class="activity-image-container">
          <image 
            :src="item.coverImage" 
            class="activity-image" 
            mode="aspectFill"
            @error="handleImageError"
          />
        </view>
        
        <!-- 右侧文字信息 -->
        <view class="activity-info">
          <text class="activity-title">{{ item.title }}</text>
          
          <!-- 活动简介 -->
          <view class="activity-description">
            <text class="description-text">{{ item.description || '暂无简介' }}</text>
          </view>
          
          <!-- 活动元信息 -->
          <view class="activity-meta">
            <view class="meta-item">
              <uni-icons type="calendar" size="14" color="#999"></uni-icons>
              <text>{{ formatDate(item.startTime, 'MM-DD HH:mm') }}</text>
            </view>
            <view class="meta-item">
              <uni-icons type="location" size="14" color="#999"></uni-icons>
              <text>{{ item.location }}</text>
            </view>
          </view>
          
          <!-- 底部价格和状态 -->
          <view class="activity-footer flex-between">
            <view class="price">
              <text class="price-num">{{ item.price === 0 ? '免费' : `¥${item.price}` }}</text>
            </view>
            <view class="status">
              <text class="status-text">{{ item.bookedCount }}/{{ item.maxParticipants }}人</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 加载更多 -->
    <view v-if="loading" class="loading">
      <text>加载中...</text>
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && activityList.length === 0" class="empty">
      <text>暂无活动</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useActivityStore } from '@/store/activity'
import { formatDate } from '@/utils/index'
import config from '@/config/index'

const activityStore = useActivityStore()
const activityList = ref([])
const keyword = ref('')
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const defaultImage = `${config.staticURL}/images/placeholder.jpg`  // 使用环境配置

onMounted(() => {
  loadActivities()
})

// 加载活动列表
async function loadActivities(refresh = false) {
  if (refresh) {
    page.value = 1
    activityList.value = []
  }
  
  loading.value = true
  console.log("loadActivities")
  const res = await activityStore.fetchList({
    page: page.value,
    pageSize: pageSize.value  // 改为驼峰命名
  })
  
  if (res && res.items) {
    activityList.value = [...activityList.value, ...res.items]
  }
  loading.value = false
}

// 搜索
function handleSearch() {
  console.log('搜索:', keyword.value)
  // TODO: 实现搜索功能
}

// 跳转到详情页
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/activity/detail?id=${id}`
  })
}

// 下拉刷新
function onPullDownRefresh() {
  loadActivities(true).then(() => {
    uni.stopPullDownRefresh()
  })
}

// 上拉加载
function onReachBottom() {
  page.value++
  loadActivities()
}

// 图片加载失败处理
function handleImageError(e) {
  console.log('图片加载失败，使用默认图片')
  // 将失败的图片替换为默认图片
  const target = e.target
  if (target && target.src !== defaultImage) {
    target.src = defaultImage
  }
}

defineExpose({
  onPullDownRefresh,
  onReachBottom
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.search-bar {
  padding: 20rpx;
  background-color: #fff;
  
  .search-box {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 32rpx;
    padding: 16rpx 32rpx;
    gap: 12rpx;
  }
  
  .search-input {
    flex: 1;
    font-size: 28rpx;
    background-color: transparent;
  }
}

.activity-list {
  padding: 20rpx;
}

.activity-item {
  display: flex;
  margin-bottom: 20rpx;
  overflow: hidden;
  gap: 20rpx;
  padding: 20rpx;
  
  // 左侧图片容器
  .activity-image-container {
    flex-shrink: 0;
    width: 200rpx;
    height: 200rpx;
    
    .activity-image {
      width: 100%;
      height: 100%;
      border-radius: 16rpx;
    }
  }
  
  // 右侧信息容器
  .activity-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0; // 防止文字溢出
    
    .activity-title {
      font-size: 32rpx;
      font-weight: bold;
      display: block;
      margin-bottom: 12rpx;
      color: #333;
      line-height: 1.4;
      // 文字溢出处理
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    // 活动简介
    .activity-description {
      margin-bottom: 16rpx;
      
      .description-text {
        font-size: 26rpx;
        color: #666;
        line-height: 1.5;
        // 限制显示2行
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
    
    .activity-meta {
      display: flex;
      flex-direction: column;
      gap: 8rpx;
      color: #999;
      font-size: 24rpx;
      margin-bottom: 16rpx;
      
      .meta-item {
        display: flex;
        align-items: center;
        gap: 6rpx;
        
        text {
          // 文字溢出处理
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }
    
    .activity-footer {
      margin-top: auto;
      
      .price {
        .price-num {
          font-size: 28rpx;
          color: #ff6b6b;
          font-weight: bold;
        }
      }
      
      .status {
        .status-text {
          font-size: 24rpx;
          color: #999;
        }
      }
    }
  }
}

.loading, .empty {
  text-align: center;
  padding: 60rpx;
  color: #999;
}
</style>

