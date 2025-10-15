# 活动预约系统

一个基于 uniapp + FastAPI + PostgreSQL 的活动预约小程序系统。

## 📁 项目结构

```
activity-booking/
├── README.md                    # 项目总览（本文件）
├── QUICKSTART.md                # 快速启动指南
├── PROJECT_STRUCTURE.md         # 详细项目结构说明
├── docker-compose.yml           # 整体服务编排
├── docs/                        # 统一文档
│   ├── API.md                   # API 文档
│   ├── DEPLOYMENT.md            # 部署指南
│   └── DEVELOPMENT.md           # 开发指南
├── activity-booking-miniapp/    # 小程序前端
└── activity-booking-server/     # 后端服务
```

> 详细的目录结构和模块说明请查看 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 功能特性

### 小程序端

- ✅ 活动列表展示
- ✅ 活动详情查看
- ✅ 活动预约
- ✅ 我的预约
- ✅ 预约取消
- ✅ 微信登录
- ✅ 用户信息管理

### 服务端

- ✅ RESTful API
- ✅ JWT 认证
- ✅ 微信小程序登录
- ✅ 活动管理（CRUD）
- ✅ 预约管理（CRUD）
- ✅ 用户管理
- ✅ PostgreSQL 数据库
- ✅ Redis 缓存支持
- ✅ 数据库迁移（Alembic）

## 技术栈

### 小程序端

- **框架**: uniapp (Vue 3)
- **状态管理**: Pinia
- **HTTP 客户端**: uni.request 封装
- **样式**: SCSS
- **工具库**: dayjs

### 服务端

- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **缓存**: Redis
- **认证**: JWT
- **数据验证**: Pydantic
- **数据库迁移**: Alembic

## 🚀 快速开始

> **新用户请查看 [QUICKSTART.md](./QUICKSTART.md) 获取详细的启动指南**

### 环境要求

- Node.js >= 22
- Python >= 3.13
- PostgreSQL >= 18
- Redis >= 8

### 一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd activity-booking

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 本地开发

详细的本地开发环境搭建请参考：
- **快速启动**: [QUICKSTART.md](./QUICKSTART.md)
- **开发指南**: [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)
- **项目结构**: [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 配置说明

### 小程序端配置

修改 `activity-booking-miniapp/config/index.js`:

```javascript
const config = {
  development: {
    baseURL: 'http://localhost:8000/api',
    timeout: 10000
  },
  production: {
    baseURL: 'https://your-domain.com/api',
    timeout: 10000
  }
}
```

### 服务端配置

修改 `activity-booking-server/.env`:

```env
# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/activity_booking

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 微信小程序配置
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret
```

## 📚 文档

- **API 文档**: [docs/API.md](./docs/API.md)
- **开发指南**: [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)
- **部署指南**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **小程序环境配置**: [activity-booking-miniapp/ENV_CONFIG.md](./activity-booking-miniapp/ENV_CONFIG.md)
- **小程序API使用**: [activity-booking-miniapp/README_API.md](./activity-booking-miniapp/README_API.md)

### 在线 API 文档

服务启动后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ 开发指南

详细的开发指南请参考：
- **开发环境搭建**: [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)
- **数据库设计**: [docs/API.md](./docs/API.md)
- **部署指南**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)

## License

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！