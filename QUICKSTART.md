# 快速启动指南

> 这是活动预约系统的快速启动指南。如果您是第一次使用本项目，请按照以下步骤操作。

## 🚀 方式一：Docker 启动（推荐）

### 1. 启动所有服务

```bash
# 在项目根目录执行
docker-compose up -d
```

这将自动启动：
- FastAPI 应用（端口 8000）
- PostgreSQL 数据库（端口 5432）
- Redis 缓存（端口 6379）

### 2. 初始化数据库

```bash
# 进入后端容器
docker-compose exec activity-booking-server bash

# 执行数据库迁移
alembic upgrade head

# 初始化示例数据（可选）
python scripts/db/init_db.py

# 退出容器
exit
```

### 3. 启动小程序端

```bash
# 进入小程序目录
cd activity-booking-miniapp

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **小程序**: 使用 HBuilderX 或微信开发者工具打开 `activity-booking-miniapp` 目录

## 方式二：本地开发环境启动

### 前置要求

确保已安装：
- PostgreSQL
- Redis
- Python 3.8+
- Node.js 16+

### 1. 配置数据库

```bash
# 登录 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE activity_booking;

# 创建用户（可选）
CREATE USER activity_user WITH PASSWORD 'activity_pass';
GRANT ALL PRIVILEGES ON DATABASE activity_booking TO activity_user;

# 退出
\q
```

### 2. 启动 Redis

```bash
redis-server
```

### 3. 配置服务端

```bash
cd server

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，填入实际配置
# 至少需要配置：
# - DATABASE_URL
# - SECRET_KEY
# - WECHAT_APPID
# - WECHAT_SECRET
```

### 4. 初始化数据库

```bash
# 执行数据库迁移
alembic upgrade head

# 初始化示例数据（可选）
python init_db.py
```

### 5. 启动服务端

```bash
# 方式1：使用启动脚本
bash run.sh

# 方式2：直接使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 http://localhost:8000 启动

### 6. 配置小程序端

```bash
cd miniapp

# 安装依赖
npm install

# 修改配置文件（如果需要）
# 编辑 config/index.js，确保 baseURL 指向正确的服务端地址
```

### 7. 启动小程序端

```bash
# 开发模式
npm run dev
```

然后使用 HBuilderX 或微信开发者工具打开 miniapp 目录。

## 验证安装

### 1. 测试服务端 API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取活动列表
curl http://localhost:8000/api/activities
```

### 2. 查看 API 文档

浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 测试小程序

在微信开发者工具中打开小程序项目，应该能看到：
- 首页显示活动列表
- 可以查看活动详情
- 可以进行预约（需要先登录）

## 常见问题

### 1. 数据库连接失败

检查：
- PostgreSQL 是否正常运行
- DATABASE_URL 配置是否正确
- 数据库用户权限是否足够

### 2. Redis 连接失败

检查：
- Redis 是否正常运行
- REDIS_URL 配置是否正确

### 3. 微信登录失败

检查：
- WECHAT_APPID 和 WECHAT_SECRET 是否配置正确
- 小程序是否在微信公众平台正确配置

### 4. 小程序无法请求 API

检查：
- 服务端是否正常运行
- 小程序配置文件中的 baseURL 是否正确
- 微信开发者工具中是否勾选了"不校验合法域名"

## 下一步

1. 修改小程序的 appid（manifest.json）
2. 配置微信小程序的合法域名
3. 根据需求修改和扩展功能
4. 准备上线部署

## 停止服务

### Docker 方式

```bash
cd server
docker-compose down
```

### 本地方式

- 按 Ctrl+C 停止服务端
- 按 Ctrl+C 停止 Redis（如果在前台运行）
- 停止 PostgreSQL 服务（根据安装方式而定）

## 清理数据

```bash
# Docker 方式（会删除所有数据）
cd server
docker-compose down -v

# 本地方式
# 删除数据库
psql -U postgres -c "DROP DATABASE activity_booking;"
```

