# 环境配置说明

## 📋 环境文件说明

项目支持多环境配置，通过不同的环境变量文件管理不同环境的配置。

### 环境文件列表

```
.env.development        # 开发环境配置（本地开发）
.env.staging           # 测试环境配置（预发布测试）
.env.production        # 生产环境配置（正式环境）
.env.local             # 本地覆盖配置（不提交到版本控制）
```

### 文件优先级

Vite 会按以下顺序加载环境变量（后者覆盖前者）：

1. `.env` - 所有环境加载
2. `.env.[mode]` - 特定环境加载（如 `.env.development`）
3. `.env.local` - 本地覆盖（被 .gitignore 忽略，不提交到版本控制）
4. `.env.[mode].local` - 特定环境的本地覆盖

## 🔧 配置项说明

### API 配置

```bash
# API 基础地址
VITE_API_BASE_URL=http://localhost:8000/api

# 请求超时时间（毫秒）
VITE_REQUEST_TIMEOUT=10000

# 文件上传地址
VITE_UPLOAD_URL=http://localhost:8000/api/upload

# 静态资源地址
VITE_STATIC_URL=http://localhost:8000/static
```

### 应用配置

```bash
# 应用标题
VITE_APP_TITLE=活动预约

# 是否开启调试模式
VITE_DEBUG=true
```

## 🚀 使用方式

### 开发环境

```bash
# 使用开发环境配置
npm run dev

# 或
uni --mode development
```

会加载 `.env.development` 配置：
- API 地址：`http://localhost:8000/api`
- 调试模式：开启
- 应用标题：活动预约（开发环境）

### 测试环境

```bash
# 使用测试环境配置
npm run dev:staging

# 或
uni --mode staging
```

会加载 `.env.staging` 配置：
- API 地址：`https://api-staging.your-domain.com/api`
- 调试模式：开启
- 应用标题：活动预约（测试环境）

### 生产环境

```bash
# 使用生产环境配置构建
npm run build

# 或
uni build --mode production
```

会加载 `.env.production` 配置：
- API 地址：`https://api.your-domain.com/api`
- 调试模式：关闭
- 应用标题：活动预约

## 💻 在代码中使用

### 获取配置

```javascript
import config from '@/config/index'

// 使用配置
console.log(config.baseURL)       // API 基础地址
console.log(config.timeout)       // 请求超时时间
console.log(config.debug)         // 是否调试模式
console.log(config.mode)          // 当前环境
console.log(config.uploadURL)     // 上传地址
console.log(config.staticURL)     // 静态资源地址
```

### 直接访问环境变量

```javascript
// 在组件中访问环境变量
const apiUrl = import.meta.env.VITE_API_BASE_URL
const isDebug = import.meta.env.VITE_DEBUG === 'true'
const mode = import.meta.env.MODE

console.log('API 地址:', apiUrl)
console.log('调试模式:', isDebug)
console.log('当前环境:', mode)
```

### 条件渲染

```vue
<template>
  <view class="app">
    <!-- 开发环境显示调试信息 -->
    <view v-if="config.debug" class="debug-info">
      <text>环境: {{ config.mode }}</text>
      <text>API: {{ config.baseURL }}</text>
    </view>
    
    <!-- 正常内容 -->
    <view class="content">
      <!-- ... -->
    </view>
  </view>
</template>

<script setup>
import config from '@/config/index'
</script>
```

## 📝 本地覆盖配置

如果你需要在本地使用不同的配置（比如连接到其他服务器），可以创建 `.env.local` 文件：

```bash
# .env.local（不会被提交到版本控制）
VITE_API_BASE_URL=http://192.168.1.100:8000/api
VITE_DEBUG=true
```

这个文件会覆盖其他环境配置，且不会被提交到 Git。

## 🔐 环境变量命名规范

- **必须以 `VITE_` 开头**：只有以此开头的变量才会暴露给前端代码
- **使用大写字母和下划线**：`VITE_API_BASE_URL`
- **在代码中使用驼峰**：`config.baseURL`

## 🌍 不同环境配置对照表

| 配置项 | 开发环境 | 测试环境 | 生产环境 |
|--------|---------|---------|---------|
| API 地址 | localhost:8000 | api-staging.your-domain.com | api.your-domain.com |
| 调试模式 | 开启 | 开启 | 关闭 |
| 应用标题后缀 | （开发环境） | （测试环境） | 无 |

## ⚙️ 配置最佳实践

### 1. 敏感信息处理

```bash
# ❌ 不要在配置文件中直接写入敏感信息
VITE_API_KEY=sk-1234567890abcdef  # 不要这样做

# ✅ 使用 .env.local 或环境变量
# 团队成员各自在本地创建 .env.local
```

### 2. 域名配置

```bash
# 开发环境
VITE_API_BASE_URL=http://localhost:8000/api

# 测试环境
VITE_API_BASE_URL=https://api-staging.your-domain.com/api

# 生产环境
VITE_API_BASE_URL=https://api.your-domain.com/api
```

### 3. 功能开关

```bash
# 通过环境变量控制功能开关
VITE_ENABLE_MOCK=false
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG_TOOLS=true
```

## 🛠️ 故障排查

### 问题1：环境变量未生效

**解决方法**：
1. 确保变量名以 `VITE_` 开头
2. 重启开发服务器（Vite 启动时加载环境变量）
3. 检查文件名是否正确

### 问题2：API 地址错误

**解决方法**：
```javascript
// 在 App.vue 中打印配置
import config from '@/config/index'
console.log('当前配置:', config)
```

### 问题3：构建后配置未生效

**解决方法**：
确保使用正确的构建命令：
```bash
npm run build           # 生产环境
npm run build:staging   # 测试环境
```

## 📚 参考资料

- [Vite 环境变量文档](https://cn.vitejs.dev/guide/env-and-mode.html)
- [uni-app 环境变量](https://uniapp.dcloud.net.cn/tutorial/env.html)

## 📊 不同环境使用示例

### 开发环境（Development）

```bash
# 启动命令
npm run dev

# 或
uni --mode development
```

**加载的配置** (`.env.development`):
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_TITLE=活动预约（开发环境）
VITE_DEBUG=true
VITE_STATIC_URL=http://localhost:8000/static
```

**应用效果**:
- ✅ API 请求发送到本地服务器 `localhost:8000`
- ✅ 控制台打印调试信息
- ✅ 应用标题显示 "活动预约（开发环境）"
- ✅ 图片从本地服务器加载

### 测试环境（Staging）

```bash
# 启动命令
npm run dev:staging

# 或
npm run build:staging
```

**加载的配置** (`.env.staging`):
```env
VITE_API_BASE_URL=https://api-staging.your-domain.com/api
VITE_APP_TITLE=活动预约（测试环境）
VITE_DEBUG=true
VITE_STATIC_URL=https://static-staging.your-domain.com
```

**应用效果**:
- ✅ API 请求发送到测试服务器
- ✅ 保留调试信息（便于测试）
- ✅ 应用标题显示 "活动预约（测试环境）"
- ✅ 图片从测试 CDN 加载

### 生产环境（Production）

```bash
# 构建命令
npm run build

# 或
uni build --mode production
```

**加载的配置** (`.env.production`):
```env
VITE_API_BASE_URL=https://api.your-domain.com/api
VITE_APP_TITLE=活动预约
VITE_DEBUG=false
VITE_STATIC_URL=https://static.your-domain.com
```

**应用效果**:
- ✅ API 请求发送到正式服务器
- ✅ 关闭调试信息
- ✅ 应用标题显示 "活动预约"
- ✅ 图片从生产 CDN 加载

## 🔄 环境切换流程

### 开发 → 测试

```bash
# 1. 停止开发服务器（如果正在运行）
# Ctrl + C

# 2. 启动测试环境
npm run dev:staging

# 3. 在微信开发者工具中预览
# 请求会发送到测试服务器
```

### 测试 → 生产

```bash
# 1. 构建生产版本
npm run build

# 2. 在 unpackage/dist 目录查看构建产物

# 3. 上传到微信小程序后台
```

## 📋 各环境用途对比

| 环境 | 用途 | 服务器 | 调试 |
|------|------|--------|-----|
| **Development** | 本地开发 | localhost:8000 | ✅ |
| **Staging** | 功能测试、预发布 | api-staging.your-domain.com | ✅ |
| **Production** | 正式上线 | api.your-domain.com | ❌ |

## 🚀 快速命令参考

```bash
# 开发
npm run dev                  # 开发环境（localhost）
npm run dev:staging          # 测试环境

# 构建
npm run build                # 构建生产版本
npm run build:staging        # 构建测试版本

# 其他
npm run type-check           # 类型检查
```

---

**通过环境配置，轻松管理不同环境的部署！** ✨

