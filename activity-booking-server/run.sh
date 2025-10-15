#!/bin/bash

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

