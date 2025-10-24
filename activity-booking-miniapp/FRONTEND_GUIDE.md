# 前端开发指南

## 项目概述

这是一个基于 uni-app 的活动预约小程序，采用 Vue 3 + Pinia 技术栈，支持微信小程序和 H5 平台。

## 技术栈

- **框架**: uni-app (Vue 3)
- **状态管理**: Pinia
- **HTTP 请求**: 封装的 request 工具
- **UI 组件**: uni-ui
- **构建工具**: Vite

## 项目结构

```
activity-booking-miniapp/
├── src/
│   ├── api/                    # API 接口
│   │   ├── activity.js         # 活动相关接口
│   │   ├── booking.js          # 预约相关接口
│   │   └── user.js             # 用户相关接口
│   │
│   ├── components/             # 公共组件
│   │   └── README.md
│   │
│   ├── composables/            # 组合式函数
│   │   ├── useActivity.js      # 活动相关逻辑
│   │   └── useUser.js          # 用户相关逻辑
│   │
│   ├── pages/                  # 页面
│   │   ├── activity/           # 活动页面
│   │   ├── auth/               # 认证页面
│   │   ├── booking/            # 预约页面
│   │   ├── index/              # 首页
│   │   ├── login/              # 登录页面
│   │   ├── my/                 # 个人中心
│   │   └── web-login/          # Web 登录
│   │
│   ├── store/                  # 状态管理
│   │   ├── activity.js         # 活动状态
│   │   ├── booking.js          # 预约状态
│   │   └── user.js             # 用户状态
│   │
│   ├── utils/                  # 工具函数
│   │   ├── request.js          # HTTP 请求封装
│   │   ├── response.js         # 响应处理工具
│   │   └── storage.js          # 存储工具
│   │
│   └── styles/                 # 样式文件
│       ├── common.scss         # 公共样式
│       ├── global.scss         # 全局样式
│       └── variables.scss      # 样式变量
│
├── static/                     # 静态资源
├── package.json                # 依赖配置
├── vite.config.js              # Vite 配置
└── manifest.json               # 应用配置
```

## API 使用规范

### 命名规范

**前后端统一使用驼峰命名（camelCase）**

### 请求示例

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

### 字段对照表

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

## 统一响应格式处理

### 响应结构

后端返回的统一响应格式：

```javascript
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "items": [...],
    "total": 10,
    "page": 1,
    "page_size": 10
  },
  "error": null,
  "timestamp": 1640995200
}
```

### 前端处理

请求拦截器会自动处理响应格式：

```javascript
// 发送请求
const res = await request.get('/api/activities')

// 前端接收到的数据（经过拦截器处理）
console.log(res) // 直接是 data 字段的内容
// {
//   "items": [...],
//   "total": 10,
//   "page": 1,
//   "page_size": 10
// }
```

### 错误处理

```javascript
// 错误响应格式
{
  "code": 404,
  "message": "活动不存在",
  "data": null,
  "error": "Activity with id 999 not found",
  "timestamp": 1640995200
}

// 前端处理：
// 1. 自动显示错误提示
// 2. 抛出错误供 catch 处理
```

### 状态码处理

| 状态码 | 处理方式 |
|--------|----------|
| 200/201 | 返回数据，正常处理 |
| 400 | 显示参数错误提示 |
| 401 | 清除 token，跳转登录页 |
| 403 | 显示权限不足提示 |
| 404 | 显示资源不存在提示 |
| 409 | 显示冲突提示 |
| 500 | 显示服务器错误提示 |

## 状态管理 (Pinia)

### Store 结构

```javascript
// store/activity.js
import { defineStore } from 'pinia'
import { getActivityList, getActivityDetail } from '@/api/activity'

export const useActivityStore = defineStore('activity', {
  state: () => ({
    list: [],
    current: null,
    loading: false
  }),

  actions: {
    async fetchList(params = {}) {
      try {
        this.loading = true
        const res = await getActivityList(params)
        // res 已经是处理后的数据（response.data）
        this.list = res.items || []
        return res
      } catch (error) {
        console.error('获取活动列表失败:', error)
        this.list = []
        return null
      } finally {
        this.loading = false
      }
    },

    async fetchDetail(id) {
      try {
        this.loading = true
        const res = await getActivityDetail(id)
        this.current = res
        return res
      } catch (error) {
        console.error('获取活动详情失败:', error)
        this.current = null
        return null
      } finally {
        this.loading = false
      }
    }
  }
})
```

### 在页面中使用

```javascript
// pages/activity/detail.vue
import { useActivityStore } from '@/store/activity'

export default {
  async onLoad(options) {
    const activityStore = useActivityStore()
    const result = await activityStore.fetchDetail(options.id)
    if (result) {
      // 处理成功的数据
      console.log('活动详情:', result)
    } else {
      // 处理失败情况
      console.log('获取活动详情失败')
    }
  }
}
```

## 页面开发示例

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
import { useActivityStore } from '@/store/activity'

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
      const activityStore = useActivityStore()
      const result = await activityStore.fetchList({
        isActive: true,  // 驼峰
        pageSize: 10     // 驼峰
      })
      
      if (result) {
        this.activities = result.items
      }
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
import { useBookingStore } from '@/store/booking'

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
      const bookingStore = useBookingStore()
      const result = await bookingStore.createBooking(this.formData)
      
      if (result) {
        uni.showToast({ title: '预约成功', icon: 'success' })
        uni.navigateBack()
      }
    }
  }
}
</script>
```

## 开发工具配置

### JSDoc 类型提示

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

### 调试技巧

```javascript
// 查看请求数据
const data = {
  activityId: 1,
  name: '张三'
}

console.log('发送数据:', JSON.stringify(data, null, 2))

const response = await request.post('/api/bookings', data)
console.log('返回数据:', JSON.stringify(response, null, 2))
```

## 环境配置

### 开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev:mp-weixin  # 微信小程序
npm run dev:h5         # H5
```

### 生产构建

```bash
# 构建微信小程序
npm run build:mp-weixin

# 构建 H5
npm run build:h5
```

## 注意事项

1. **统一使用驼峰命名**
   - 发送请求时使用驼峰
   - 接收响应时使用驼峰
   - 无需任何转换

2. **错误处理**
   - 所有错误都会被拦截器处理
   - 无需在业务代码中重复处理
   - 自动显示用户友好的错误提示

3. **状态管理**
   - 使用 Pinia 进行状态管理
   - Store 中的数据处理逻辑保持不变
   - 只是数据来源发生了变化

4. **兼容性**
   - 支持微信小程序和 H5 平台
   - 请求拦截器同时支持新旧响应格式
   - 可以逐步升级后端接口

## 相关文件

- **API 接口**: `src/api/`
- **状态管理**: `src/store/`
- **请求工具**: `src/utils/request.js`
- **响应处理**: `src/utils/response.js`
- **页面示例**: `src/pages/`

---

**记住：前后端统一使用驼峰命名，简单高效！** ✨
