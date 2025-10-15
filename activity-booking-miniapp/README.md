# 活动预约小程序

基于 uniapp + Vue 3 的活动预约小程序前端。

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 运行项目

```bash
# 开发环境（默认使用 localhost:8000）
npm run dev

# 测试环境
npm run dev:staging

# 构建生产环境
npm run build

# 构建测试环境
npm run build:staging
```

## 📁 项目结构

```
src/
├── api/                # API 接口封装
│   ├── activity.js     # 活动相关 API
│   ├── booking.js      # 预约相关 API
│   └── user.js         # 用户相关 API
├── composables/        # 组合式 API
│   └── useActivity.js  # 活动相关逻辑
├── config/             # 配置文件
│   └── index.js        # 应用配置（自动读取环境变量）
├── examples/           # 使用示例
│   └── api-usage.js    # API 使用示例
├── pages/              # 页面
│   ├── index/          # 首页
│   ├── activity/       # 活动详情
│   ├── booking/        # 预约页面
│   └── my/             # 个人中心
├── static/             # 静态资源
│   ├── images/         # 图片
│   └── styles/         # 样式
├── store/              # 状态管理（Pinia）
│   ├── activity.js     # 活动状态
│   └── user.js         # 用户状态
├── utils/              # 工具函数
│   ├── index.js        # 通用工具
│   ├── request.js      # HTTP 请求封装
│   └── storage.js      # 本地存储
├── App.vue             # 应用入口
└── pages.json          # 页面配置
```

## 🌍 环境配置

### 配置文件

- **`.env.development`** - 开发环境（localhost）
- **`.env.staging`** - 测试环境
- **`.env.production`** - 生产环境
- **`.env.example`** - 配置示例
- **`.env.local`** - 本地覆盖（不提交到版本控制）

### 修改配置

1. 复制示例文件创建本地配置：
```bash
cp .env.example .env.local
```

2. 编辑 `.env.local` 修改为你的配置
3. 重启开发服务器使配置生效

详细说明请查看 [ENV_CONFIG.md](./ENV_CONFIG.md)

## 🔧 配置项

所有配置项都在 `src/config/index.js` 中，包括：

- `baseURL` - API 基础地址
- `timeout` - 请求超时时间
- `debug` - 调试模式
- `uploadURL` - 文件上传地址
- `staticURL` - 静态资源地址
- `pageSize` - 默认分页大小
- `imageMaxSize` - 图片最大大小
- 等等...

## 📝 API 命名规范

本项目前后端统一使用 **驼峰命名（camelCase）**：

```javascript
// ✅ 正确
const activity = {
  coverImage: 'url',
  startTime: '2024-01-01',
  maxParticipants: 20,
  bookedCount: 5
}

// ❌ 错误
const activity = {
  cover_image: 'url',    // 蛇形命名
  start_time: '2024-01-01',
  max_participants: 20,
  booked_count: 5
}
```

详细说明请查看 [README_API.md](./README_API.md)

## 🛠️ 开发指南

### 1. 创建新页面

在 `pages.json` 中配置页面，然后在 `src/pages/` 目录下创建对应的 vue 文件。

### 2. 调用 API

```javascript
import request from '@/utils/request'

// GET 请求
const data = await request.get('/api/activities', {
  page: 1,
  pageSize: 10
})

// POST 请求
const result = await request.post('/api/bookings', {
  activityId: 1,
  name: '张三',
  phone: '13800138000'
})
```

### 3. 状态管理

```javascript
import { useActivityStore } from '@/store/activity'

const activityStore = useActivityStore()
const activities = await activityStore.fetchList()
```

### 4. 使用组合式 API

```javascript
import { useActivity } from '@/composables/useActivity'

const { 
  activityList, 
  loading, 
  fetchActivityList 
} = useActivity()
```

## 📱 支持平台

- [x] 微信小程序
- [x] H5
- [ ] App（可扩展）
- [ ] 支付宝小程序（可扩展）

## 🔗 相关文档

- [环境配置说明](./ENV_CONFIG.md)
- [API 使用说明](./README_API.md)
- [后端 API 文档](../activity-booking-server/README.md)

## 📞 开发提示

### 查看当前配置

在浏览器控制台或小程序调试器中运行：

```javascript
import config from '@/config/index'
console.log(config)
```

### 切换环境

```bash
# 开发 → 测试
npm run dev:staging

# 开发 → 生产（构建）
npm run build
```

### 调试技巧

1. 开发环境会自动打印配置信息
2. 网络请求在 `utils/request.js` 中可以添加拦截器
3. 使用微信开发者工具的调试功能

## ⚠️ 注意事项

1. **环境变量必须以 `VITE_` 开头**才能在代码中访问
2. **修改环境变量后需要重启开发服务器**
3. **`.env.local` 不要提交到版本控制**
4. **生产环境记得修改 API 域名**

---

Happy Coding! 🎉

