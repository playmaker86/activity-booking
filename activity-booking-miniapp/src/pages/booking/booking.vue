<template>
  <view class="page">
    <view class="form card">
      <view class="form-item">
        <text class="label">姓名</text>
        <input 
          class="input" 
          type="text" 
          placeholder="请输入姓名" 
          v-model="formData.name"
        />
      </view>
      
      <view class="form-item">
        <text class="label">手机号</text>
        <input 
          class="input" 
          type="number" 
          placeholder="请输入手机号" 
          v-model="formData.phone"
        />
      </view>
      
      <view class="form-item">
        <text class="label">参与人数</text>
        <input 
          class="input" 
          type="number" 
          placeholder="请输入参与人数" 
          v-model="formData.participants"
        />
      </view>
      
      <view class="form-item">
        <text class="label">备注</text>
        <textarea 
          class="textarea" 
          placeholder="请输入备注信息（选填）" 
          v-model="formData.remark"
        />
      </view>
    </view>
    
    <view class="submit-btn">
      <button class="btn-primary" @click="handleSubmit">提交预约</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onLoad } from '@dcloudio/uni-app'
import { createBooking } from '@/api/booking'
import { showToast, showLoading, hideLoading } from '@/utils/index'

const activityId = ref('')
const formData = reactive({
  name: '',
  phone: '',
  participants: 1,
  remark: ''
})

onLoad((options) => {
  if (options.activityId) {
    activityId.value = options.activityId
  }
})

// 提交预约
async function handleSubmit() {
  // 表单验证
  if (!formData.name) {
    showToast('请输入姓名')
    return
  }
  
  if (!formData.phone || !/^1[3-9]\d{9}$/.test(formData.phone)) {
    showToast('请输入正确的手机号')
    return
  }
  
  if (!formData.participants || formData.participants < 1) {
    showToast('请输入正确的参与人数')
    return
  }
  
  try {
    showLoading('提交中...')
    await createBooking({
      activityId: activityId.value,  // 改为驼峰命名
      ...formData
    })
    hideLoading()
    showToast('预约成功', 'success')
    
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    hideLoading()
    console.error('预约失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20rpx;
}

.form {
  .form-item {
    margin-bottom: 30rpx;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .label {
      display: block;
      font-size: 28rpx;
      color: #333;
      margin-bottom: 16rpx;
    }
    
    .input, .textarea {
      width: 100%;
      padding: 20rpx;
      background-color: #f5f5f5;
      border-radius: 8rpx;
      font-size: 28rpx;
    }
    
    .textarea {
      min-height: 150rpx;
    }
  }
}

.submit-btn {
  margin-top: 40rpx;
  
  .btn-primary {
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

