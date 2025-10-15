# 项目结构说明

## 完整目录结构

```
activity-booking/
│
├── README.md                    # 项目说明文档
├── QUICKSTART.md                # 快速启动指南
├── PROJECT_STRUCTURE.md         # 项目结构说明（本文件）
│
├── miniapp/                     # 小程序端（uniapp）
│   ├── api/                     # API 接口封装
│   │   ├── activity.js          # 活动相关 API
│   │   ├── booking.js           # 预约相关 API
│   │   └── user.js              # 用户相关 API
│   │
│   ├── components/              # 组件目录
│   │   └── README.md            # 组件开发规范
│   │
│   ├── config/                  # 配置文件
│   │   └── index.js             # 环境配置
│   │
│   ├── pages/                   # 页面目录
│   │   ├── index/               # 首页
│   │   │   └── index.vue
│   │   ├── activity/            # 活动页面
│   │   │   └── detail.vue
│   │   ├── booking/             # 预约页面
│   │   │   └── booking.vue
│   │   └── my/                  # 个人中心
│   │       ├── my.vue
│   │       └── bookings.vue
│   │
│   ├── static/                  # 静态资源
│   │   ├── images/              # 图片资源
│   │   │   └── README.md
│   │   ├── styles/              # 样式文件
│   │   │   └── common.scss      # 公共样式
│   │   └── tabbar/              # 底部导航图标
│   │
│   ├── store/                   # 状态管理（Pinia）
│   │   ├── activity.js          # 活动状态
│   │   └── user.js              # 用户状态
│   │
│   ├── utils/                   # 工具函数
│   │   ├── index.js             # 通用工具函数
│   │   ├── request.js           # HTTP 请求封装
│   │   └── storage.js           # 本地存储工具
│   │
│   ├── App.vue                  # 应用入口组件
│   ├── main.js                  # 主入口文件
│   ├── index.html               # HTML 模板
│   ├── pages.json               # 页面配置
│   ├── manifest.json            # 应用配置
│   ├── vite.config.js           # Vite 配置
│   ├── package.json             # 依赖管理
│   └── .gitignore               # Git 忽略文件
│
└── server/                      # 服务端（FastAPI）
    ├── alembic/                 # 数据库迁移
    │   ├── versions/            # 迁移版本文件
    │   ├── env.py               # Alembic 环境配置
    │   └── script.py.mako       # 迁移脚本模板
    │
    ├── app/                     # 应用代码
    │   ├── api/                 # API 路由
    │   │   ├── __init__.py
    │   │   ├── deps.py          # 依赖注入
    │   │   ├── auth.py          # 认证路由
    │   │   ├── users.py         # 用户路由
    │   │   ├── activities.py    # 活动路由
    │   │   └── bookings.py      # 预约路由
    │   │
    │   ├── models/              # 数据库模型
    │   │   ├── __init__.py
    │   │   ├── user.py          # 用户模型
    │   │   ├── activity.py      # 活动模型
    │   │   └── booking.py       # 预约模型
    │   │
    │   ├── schemas/             # Pydantic 模型
    │   │   ├── __init__.py
    │   │   ├── user.py          # 用户 Schema
    │   │   ├── activity.py      # 活动 Schema
    │   │   ├── booking.py       # 预约 Schema
    │   │   └── token.py         # Token Schema
    │   │
    │   ├── utils/               # 工具函数
    │   │   ├── security.py      # 安全工具（JWT、密码）
    │   │   └── wechat.py        # 微信相关工具
    │   │
    │   ├── __init__.py
    │   ├── config.py            # 配置文件
    │   ├── database.py          # 数据库连接
    │   ├── redis_client.py      # Redis 客户端
    │   └── main.py              # 应用入口
    │
    ├── .env.example             # 环境变量示例
    ├── .gitignore               # Git 忽略文件
    ├── alembic.ini              # Alembic 配置
    ├── Dockerfile               # Docker 镜像配置
    ├── docker-compose.yml       # Docker Compose 配置
    ├── requirements.txt         # Python 依赖
    ├── run.sh                   # 启动脚本
    └── init_db.py               # 数据库初始化脚本
```

## 模块说明

### 小程序端（miniapp）

#### 1. API 层（api/）
- 封装所有后端 API 调用
- 统一错误处理
- 请求/响应拦截

#### 2. 页面层（pages/）
- **index**: 活动列表首页，支持下拉刷新、上拉加载
- **activity/detail**: 活动详情页，展示完整活动信息
- **booking/booking**: 预约表单页，收集预约信息
- **my/my**: 个人中心，展示用户信息
- **my/bookings**: 我的预约列表，管理预约记录

#### 3. 状态管理（store/）
- **user**: 管理用户登录状态、用户信息
- **activity**: 管理活动列表、活动详情

#### 4. 工具函数（utils/）
- **request.js**: HTTP 请求封装，统一处理认证和错误
- **storage.js**: 本地存储工具类
- **index.js**: 通用工具函数（日期格式化、弹窗等）

### 服务端（server）

#### 1. API 路由层（app/api/）
- **auth.py**: 处理微信登录认证
- **users.py**: 用户信息的增删改查
- **activities.py**: 活动管理的完整 CRUD
- **bookings.py**: 预约管理功能
- **deps.py**: 依赖注入，如获取当前用户

#### 2. 数据库模型层（app/models/）
- **user.py**: 用户表模型
- **activity.py**: 活动表模型
- **booking.py**: 预约表模型

#### 3. Schema 层（app/schemas/）
- 定义 API 的请求/响应数据结构
- 数据验证和序列化

#### 4. 工具层（app/utils/）
- **security.py**: JWT 令牌生成和验证
- **wechat.py**: 微信小程序登录接口

#### 5. 数据库迁移（alembic/）
- 使用 Alembic 管理数据库版本
- 支持数据库升级和回滚

## 技术架构

### 小程序端技术栈
```
uniapp (Vue 3)
├── Pinia (状态管理)
├── Vue Router (路由，uniapp 内置)
├── SCSS (样式预处理)
└── dayjs (日期处理)
```

### 服务端技术栈
```
FastAPI
├── SQLAlchemy (ORM)
├── PostgreSQL (数据库)
├── Redis (缓存)
├── Alembic (数据库迁移)
├── Pydantic (数据验证)
├── python-jose (JWT)
└── httpx (HTTP 客户端)
```

## 数据流向

### 1. 用户登录流程
```
小程序 → wx.login() → 获取 code
     ↓
POST /api/auth/wx-login
     ↓
微信服务器验证 → 返回 openid
     ↓
创建/查找用户 → 生成 JWT token
     ↓
返回 token → 存储在本地
```

### 2. 活动预约流程
```
用户选择活动 → 填写预约信息
     ↓
POST /api/bookings (携带 JWT token)
     ↓
验证用户身份 → 检查活动名额
     ↓
创建预约记录 → 更新活动人数
     ↓
返回预约成功
```

### 3. 数据查询流程
```
GET /api/activities
     ↓
查询数据库 → 分页处理
     ↓
序列化数据 → 返回 JSON
     ↓
小程序接收 → 更新页面
```

## 扩展建议

### 功能扩展
1. 添加活动分类和标签
2. 实现活动搜索和筛选
3. 添加活动评价和评分
4. 实现消息通知功能
5. 添加活动报名审核流程
6. 支持在线支付
7. 添加活动签到码
8. 实现活动相册功能

### 性能优化
1. 使用 Redis 缓存热门活动
2. 实现图片 CDN 加速
3. 添加数据库索引优化查询
4. 实现接口限流
5. 添加 API 响应缓存

### 安全增强
1. 添加请求签名验证
2. 实现敏感信息加密存储
3. 添加操作日志记录
4. 实现数据备份机制
5. 添加防刷机制

## 维护指南

### 代码规范
- 遵循 PEP 8（Python）
- 遵循 Vue 官方风格指南
- 使用 ESLint 和 Prettier 格式化代码
- 编写必要的注释和文档

### 版本管理
- 使用语义化版本号
- 重要变更记录在 CHANGELOG
- 使用 Git Flow 工作流

### 测试
- 编写单元测试（pytest）
- API 接口测试
- 小程序端到端测试

