# API 使用说明（JavaScript）

## 📋 命名规范

**前后端统一使用驼峰命名（camelCase）**

## 🚀 快速开始

### 1. 发送请求（使用驼峰）

```javascript
import request from '@/utils/request'

// ✅ GET 请求 - 查询参数使用驼峰
const activities = await request.get('/api/activities', {
  page: 1,
  pageSize: 10,    // 驼峰命名
  keyword: '徒步'   // 驼峰命名
})

// ✅ POST 请求 - JSON 请求体使用驼峰
const activity = await request.post('/api/activities', {
  title: '周末徒步',
  coverImage: 'https://example.com/cover.jpg',  // 驼峰
  startTime: '2024-01-01T09:00:00Z',            // 驼峰
  endTime: '2024-01-01T17:00:00Z',              // 驼峰
  maxParticipants: 20                            // 驼峰
})

// ✅ 创建预约
const booking = await request.post('/api/bookings', {
  activityId: 1,        // 驼峰
  name: '张三',
  phone: '13800138000',
  participants: 2
})
```

### 2. 接收响应（使用驼峰）

```javascript
// ✅ 获取活动详情
const activity = await request.get('/api/activities/1')

// 直接使用驼峰字段
console.log(activity.coverImage)      // 驼峰
console.log(activity.startTime)       // 驼峰
console.log(activity.maxParticipants) // 驼峰
console.log(activity.bookedCount)     // 驼峰
console.log(activity.isActive)        // 驼峰
console.log(activity.createdAt)       // 驼峰
```

## 📝 常用字段对照

| 数据库（后端内部）| API 字段（前端使用）| 说明 |
|-----------------|-------------------|------|
| `user_id` | `userId` | 用户ID |
| `activity_id` | `activityId` | 活动ID |
| `created_at` | `createdAt` | 创建时间 |
| `updated_at` | `updatedAt` | 更新时间 |
| `is_active` | `isActive` | 是否激活 |
| `cover_image` | `coverImage` | 封面图片 |
| `start_time` | `startTime` | 开始时间 |
| `end_time` | `endTime` | 结束时间 |
| `max_participants` | `maxParticipants` | 最大人数 |
| `booked_count` | `bookedCount` | 已预约人数 |
| `checked_in` | `checkedIn` | 已签到人数 |

## 💡 Vue 页面示例

### 活动列表页面

```vue
<template>
  <view class="activity-list">
    <view v-for="activity in activities" :key="activity.id" class="activity-item">
      <image :src="activity.coverImage" />
      <text>{{ activity.title }}</text>
      <text>时间: {{ activity.startTime }}</text>
      <text>人数: {{ activity.bookedCount }}/{{ activity.maxParticipants }}</text>
    </view>
  </view>
</template>

<script>
import request from '@/utils/request'

export default {
  data() {
    return {
      activities: []
    }
  },
  
  onLoad() {
    this.loadActivities()
  },
  
  methods: {
    async loadActivities() {
      // 使用驼峰命名查询
      const data = await request.get('/api/activities', {
        isActive: true,  // 驼峰
        pageSize: 10     // 驼峰
      })
      
      // 返回的数据也是驼峰
      this.activities = data
    }
  }
}
</script>
```

### 预约表单页面

```vue
<template>
  <view class="booking-form">
    <input v-model="formData.name" placeholder="姓名" />
    <input v-model="formData.phone" placeholder="手机号" />
    <input v-model.number="formData.participants" type="number" placeholder="人数" />
    <textarea v-model="formData.remark" placeholder="备注" />
    <button @click="submitForm">提交预约</button>
  </view>
</template>

<script>
import request from '@/utils/request'

export default {
  data() {
    return {
      formData: {
        activityId: 0,  // 驼峰
        name: '',
        phone: '',
        participants: 1,
        remark: ''
      }
    }
  },
  
  onLoad(options) {
    this.formData.activityId = parseInt(options.id)  // 驼峰
  },
  
  methods: {
    async submitForm() {
      // 直接提交驼峰数据
      const booking = await request.post('/api/bookings', this.formData)
      
      // 返回的也是驼峰
      console.log('预约ID:', booking.id)
      console.log('用户ID:', booking.userId)      // 驼峰
      console.log('活动ID:', booking.activityId)  // 驼峰
      console.log('创建时间:', booking.createdAt) // 驼峰
      
      uni.showToast({ title: '预约成功', icon: 'success' })
      uni.navigateBack()
    }
  }
}
</script>
```

## 🎯 使用 JSDoc 获得类型提示

在文件顶部添加类型定义：

```javascript
/**
 * @typedef {import('@/types/api').Activity} Activity
 * @typedef {import('@/types/api').Booking} Booking
 * @typedef {import('@/types/api').User} User
 */

export default {
  data() {
    return {
      /** @type {Activity[]} */
      activities: [],
      /** @type {Booking|null} */
      currentBooking: null
    }
  },
  
  methods: {
    /**
     * 加载活动
     * @returns {Promise<Activity[]>}
     */
    async loadActivities() {
      const data = await request.get('/api/activities')
      return data
    }
  }
}
```

这样在 VSCode 中就能获得智能提示！

## 📚 相关文件

- **使用示例**: `src/examples/api-usage.js`
- **请求工具**: `src/utils/request.js`

## ⚠️ 注意事项

1. **统一使用驼峰命名**
   - 发送请求时使用驼峰
   - 接收响应时使用驼峰
   - 无需任何转换

2. **JSDoc 注释**
   - 使用 JSDoc 注释可以获得更好的代码提示
   - 提高开发效率

3. **字段名称**
   - `activityId` 不是 `activity_id`
   - `createdAt` 不是 `created_at`
   - `maxParticipants` 不是 `max_participants`

## 🔍 调试技巧

### 查看请求数据

```javascript
const data = {
  activityId: 1,
  name: '张三'
}

console.log('发送数据:', JSON.stringify(data, null, 2))
// {
//   "activityId": 1,
//   "name": "张三"
// }

const response = await request.post('/api/bookings', data)
console.log('返回数据:', JSON.stringify(response, null, 2))
```

### 验证字段名称

```javascript
const activity = await request.get('/api/activities/1')

// ✅ 正确
console.log(activity.coverImage)
console.log(activity.maxParticipants)

// ❌ 错误（这些字段不存在）
console.log(activity.cover_image)     // undefined
console.log(activity.max_participants) // undefined
```

---

**记住：前后端统一使用驼峰命名，简单高效！** ✨

