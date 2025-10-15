# 活动预约系统 - 服务端

基于 FastAPI + PostgreSQL + Redis 的活动预约系统服务端。

## 快速开始

```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
