# 部署指南

## 概述

本文档介绍活动预约系统的部署方法，包括开发环境、测试环境和生产环境的部署配置。

## 环境要求

### 服务器要求

- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 20GB以上
- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / Docker

### 软件要求

- **Node.js**: >= 22.0.0
- **Python**: >= 3.13
- **PostgreSQL**: >= 18
- **Redis**: >= 8
- **Docker**: >= 20.10 (可选)
- **Docker Compose**: >= 2.0 (可选)

## 部署方式

### 1. Docker Compose 部署（推荐）

#### 生产环境配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend/activity-booking-server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/activity_booking
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - WECHAT_APPID=${WECHAT_APPID}
      - WECHAT_SECRET=${WECHAT_SECRET}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:18
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=activity_booking
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:8
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

#### 部署步骤

1. **克隆代码**
```bash
git clone <repository-url>
cd activity-booking
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置生产环境参数
```

3. **启动服务**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. **初始化数据库**
```bash
docker-compose exec backend alembic upgrade head
```

### 2. 传统部署

#### 后端部署

1. **安装依赖**
```bash
cd backend/activity-booking-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件
```

3. **初始化数据库**
```bash
alembic upgrade head
```

4. **启动服务**
```bash
# 使用 Gunicorn (生产环境)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用 Uvicorn (开发环境)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 前端部署

1. **安装依赖**
```bash
cd frontend/activity-booking-miniapp
npm install
```

2. **构建项目**
```bash
npm run build
```

3. **部署到服务器**
```bash
# 将 dist 目录上传到 Web 服务器
scp -r dist/* user@server:/var/www/html/
```

### 3. 小程序部署

1. **使用 HBuilderX**
   - 打开项目
   - 选择"发行" -> "小程序-微信"
   - 配置小程序 AppID
   - 点击"发行"

2. **使用命令行**
```bash
cd frontend/activity-booking-miniapp
npm run build
# 将 unpackage/dist/build/mp-weixin 目录上传到微信开发者工具
```

## Nginx 配置

### 生产环境 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # API 代理
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## 环境变量配置

### 后端环境变量

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/activity_booking

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-very-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 微信小程序配置
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 前端环境变量

```javascript
// config/index.js
const config = {
  development: {
    baseURL: 'http://localhost:8000/api',
    timeout: 10000
  },
  staging: {
    baseURL: 'https://staging-api.your-domain.com/api',
    timeout: 10000
  },
  production: {
    baseURL: 'https://api.your-domain.com/api',
    timeout: 10000
  }
}
```

## 数据库迁移

### 创建迁移

```bash
cd backend/activity-booking-server
alembic revision --autogenerate -m "描述信息"
```

### 执行迁移

```bash
# 升级到最新版本
alembic upgrade head

# 降级到指定版本
alembic downgrade -1

# 查看迁移历史
alembic history
```

## 监控和日志

### 日志配置

```python
# logging.conf
[loggers]
keys=root,app

[handlers]
keys=console,file

[formatters]
keys=default

[logger_root]
level=INFO
handlers=console

[logger_app]
level=INFO
handlers=console,file
qualname=app
propagate=0

[handler_console]
class=StreamHandler
level=INFO
formatter=default
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=INFO
formatter=default
args=('logs/app.log',)

[formatter_default]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查数据库连接
curl http://localhost:8000/api/health/db

# 检查 Redis 连接
curl http://localhost:8000/api/health/redis
```

## 备份和恢复

### 数据库备份

```bash
# 备份数据库
pg_dump -h localhost -U user -d activity_booking > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
psql -h localhost -U user -d activity_booking < backup_20240101_120000.sql
```

### 文件备份

```bash
# 备份上传的文件
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz static/uploads/

# 备份配置文件
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz .env nginx.conf
```

## 安全配置

### SSL 证书

```bash
# 使用 Let's Encrypt
certbot --nginx -d your-domain.com

# 或使用自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/key.pem \
  -out /etc/nginx/ssl/cert.pem
```

### 防火墙配置

```bash
# Ubuntu/Debian
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

# CentOS/RHEL
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

## 性能优化

### 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_activities_start_time ON activities(start_time);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_activity_id ON bookings(activity_id);

-- 分析查询性能
EXPLAIN ANALYZE SELECT * FROM activities WHERE start_time > NOW();
```

### 缓存配置

```python
# Redis 缓存配置
CACHE_TTL = {
    'activities': 300,  # 5分钟
    'user_info': 600,   # 10分钟
    'bookings': 60,     # 1分钟
}
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串是否正确
   - 检查防火墙设置

2. **Redis 连接失败**
   - 检查 Redis 服务状态
   - 验证 Redis URL 配置
   - 检查内存使用情况

3. **API 响应慢**
   - 检查数据库查询性能
   - 查看 Redis 缓存命中率
   - 分析服务器资源使用情况

### 日志查看

```bash
# 查看应用日志
docker-compose logs -f backend

# 查看 Nginx 日志
docker-compose logs -f nginx

# 查看数据库日志
docker-compose logs -f db
```
