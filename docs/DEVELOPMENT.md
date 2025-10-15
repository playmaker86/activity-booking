# 开发指南

## 概述

本文档介绍活动预约系统的开发环境搭建、代码规范、开发流程等。

## 开发环境搭建

### 前置要求

- **Node.js**: >= 22.0.0
- **Python**: >= 3.8
- **PostgreSQL**: >= 12
- **Redis**: >= 6
- **Git**: >= 2.0

### 快速开始

1. **克隆项目**
```bash
git clone <repository-url>
cd activity-booking
```

2. **启动开发环境**
```bash
# 使用 Docker Compose（推荐）
docker-compose up -d

# 或手动启动各个服务
```

3. **访问应用**
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 前端开发服务器: http://localhost:3000

## 项目结构

```
activity-booking/
├── README.md                    # 项目总览
├── .gitignore                   # 统一忽略规则
├── docker-compose.yml           # 整体服务编排
├── .github/                     # GitHub Actions 工作流
│   └── workflows/
│       ├── frontend.yml         # 前端构建部署
│       └── backend.yml          # 后端构建部署
├── docs/                        # 统一文档
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
├── frontend/                    # 前端代码
│   └── activity-booking-miniapp/
└── backend/                     # 后端代码
    └── activity-booking-server/
```

## 前端开发

### 技术栈

- **框架**: uniapp (Vue 3)
- **状态管理**: Pinia
- **HTTP 客户端**: uni.request 封装
- **样式**: SCSS
- **工具库**: dayjs

### 开发环境

```bash
cd frontend/activity-booking-miniapp

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build

# 类型检查
npm run type-check
```

### 代码规范

#### 文件命名

- 组件文件：PascalCase (如 `UserProfile.vue`)
- 页面文件：kebab-case (如 `user-profile.vue`)
- 工具文件：camelCase (如 `requestUtils.js`)

#### 代码风格

```javascript
// 组件定义
<template>
  <view class="user-profile">
    <text>{{ user.name }}</text>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'

// 响应式数据
const user = ref(null)

// 计算属性
const displayName = computed(() => {
  return user.value?.name || '未知用户'
})

// 方法
const fetchUser = async () => {
  try {
    const response = await api.getUser()
    user.value = response.data
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.user-profile {
  padding: 20rpx;
  
  text {
    font-size: 32rpx;
    color: #333;
  }
}
</style>
```

#### API 调用规范

```javascript
// api/user.js
import request from '@/utils/request'

export const userApi = {
  // 获取用户信息
  getUser: () => request.get('/users/me'),
  
  // 更新用户信息
  updateUser: (data) => request.put('/users/me', data),
  
  // 微信登录
  wxLogin: (code) => request.post('/auth/wx-login', { code })
}
```

### 状态管理

```javascript
// store/user.js
import { defineStore } from 'pinia'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: null,
    isLoggedIn: false
  }),
  
  getters: {
    userInfo: (state) => state.user,
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async login(code) {
      try {
        const response = await userApi.wxLogin(code)
        this.token = response.access_token
        this.user = response.user
        this.isLoggedIn = true
        
        // 保存到本地存储
        uni.setStorageSync('token', this.token)
        uni.setStorageSync('user', this.user)
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      this.isLoggedIn = false
      
      // 清除本地存储
      uni.removeStorageSync('token')
      uni.removeStorageSync('user')
    }
  }
})
```

## 后端开发

### 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **缓存**: Redis
- **认证**: JWT
- **数据验证**: Pydantic
- **数据库迁移**: Alembic

### 开发环境

```bash
cd backend/activity-booking-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 初始化数据库
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 代码规范

#### 文件结构

```
app/
├── api/                 # API 路由
│   ├── __init__.py
│   ├── activities.py
│   ├── auth.py
│   ├── bookings.py
│   └── users.py
├── models/              # 数据库模型
│   ├── __init__.py
│   ├── activity.py
│   ├── booking.py
│   └── user.py
├── schemas/             # Pydantic 模型
│   ├── __init__.py
│   ├── activity.py
│   ├── booking.py
│   └── user.py
├── utils/               # 工具函数
│   ├── __init__.py
│   ├── security.py
│   └── wechat.py
├── config.py            # 配置文件
├── database.py          # 数据库连接
├── main.py              # 应用入口
└── redis_client.py      # Redis 客户端
```

#### API 路由规范

```python
# api/activities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取活动列表"""
    activities = db.query(Activity).offset(skip).limit(limit).all()
    return activities

@router.post("/", response_model=ActivityResponse)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建活动"""
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
```

#### 数据模型规范

```python
# models/activity.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    cover_image = Column(String(500))
    location = Column(String(200))
    organizer = Column(String(100))
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, default=0.0)
    max_participants = Column(Integer, default=0)
    booked_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

#### Pydantic 模型规范

```python
# schemas/activity.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ActivityBase(BaseModel):
    title: str = Field(..., max_length=200, description="活动标题")
    description: Optional[str] = Field(None, description="活动描述")
    cover_image: Optional[str] = Field(None, description="封面图片")
    location: Optional[str] = Field(None, max_length=200, description="活动地点")
    organizer: Optional[str] = Field(None, max_length=100, description="主办方")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    price: float = Field(0.0, ge=0, description="价格")
    max_participants: int = Field(0, ge=0, description="最大参与人数")

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    # ... 其他字段

class ActivityResponse(ActivityBase):
    id: int
    booked_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### 数据库迁移

#### 创建迁移

```bash
# 创建新的迁移文件
alembic revision --autogenerate -m "添加活动表"

# 手动创建迁移文件
alembic revision -m "添加用户表索引"
```

#### 执行迁移

```bash
# 升级到最新版本
alembic upgrade head

# 降级到指定版本
alembic downgrade -1

# 查看迁移历史
alembic history
```

#### 迁移文件示例

```python
# alembic/versions/xxx_add_activity_table.py
"""添加活动表

Revision ID: xxx
Revises: yyy
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxx'
down_revision = 'yyy'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('cover_image', sa.String(length=500), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('organizer', sa.String(length=100), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('max_participants', sa.Integer(), nullable=True),
    sa.Column('booked_count', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activities_id'), 'activities', ['id'], unique=False)
    op.create_index(op.f('ix_activities_title'), 'activities', ['title'], unique=False)
    op.create_index(op.f('ix_activities_start_time'), 'activities', ['start_time'], unique=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_activities_start_time'), table_name='activities')
    op.drop_index(op.f('ix_activities_title'), table_name='activities')
    op.drop_index(op.f('ix_activities_id'), table_name='activities')
    op.drop_table('activities')
    # ### end Alembic commands ###
```

## 测试

### 前端测试

```bash
# 运行测试
npm test

# 运行测试并生成覆盖率报告
npm run test:coverage
```

### 后端测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/test_activities.py
```

### 测试示例

```python
# tests/test_activities.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models.activity import Activity

client = TestClient(app)

def test_get_activities():
    response = client.get("/api/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_activity():
    activity_data = {
        "title": "测试活动",
        "description": "这是一个测试活动",
        "start_time": "2024-01-01T10:00:00",
        "end_time": "2024-01-01T18:00:00",
        "price": 100.0,
        "max_participants": 50
    }
    response = client.post("/api/activities/", json=activity_data)
    assert response.status_code == 201
    assert response.json()["title"] == "测试活动"
```

## 调试

### 前端调试

1. **使用浏览器开发者工具**
2. **使用 HBuilderX 调试器**
3. **添加 console.log 调试信息**

```javascript
// 调试示例
const fetchActivities = async () => {
  try {
    console.log('开始获取活动列表')
    const response = await api.getActivities()
    console.log('活动列表响应:', response)
    return response.data
  } catch (error) {
    console.error('获取活动列表失败:', error)
    throw error
  }
}
```

### 后端调试

1. **使用 IDE 调试器**
2. **添加日志输出**
3. **使用 FastAPI 的调试模式**

```python
# 调试示例
import logging

logger = logging.getLogger(__name__)

@router.get("/activities/")
async def get_activities(db: Session = Depends(get_db)):
    logger.info("开始获取活动列表")
    try:
        activities = db.query(Activity).all()
        logger.info(f"成功获取 {len(activities)} 个活动")
        return activities
    except Exception as e:
        logger.error(f"获取活动列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取活动列表失败")
```

## 代码提交规范

### Git 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 类型 (type)

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 示例

```
feat(api): 添加活动搜索功能

- 支持按标题和描述搜索
- 添加分页支持
- 优化查询性能

Closes #123
```

### 分支管理

- `main`: 主分支，用于生产环境
- `develop`: 开发分支，用于集成开发
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支
- `release/*`: 发布分支

### Pull Request 规范

1. **标题**: 简洁明了地描述变更内容
2. **描述**: 详细说明变更原因和影响
3. **测试**: 说明如何测试变更
4. **检查清单**: 确保代码质量

## 性能优化

### 前端优化

1. **代码分割**
2. **图片懒加载**
3. **缓存策略**
4. **减少 HTTP 请求**

### 后端优化

1. **数据库查询优化**
2. **Redis 缓存**
3. **异步处理**
4. **连接池配置**

## 常见问题

### 前端问题

1. **跨域问题**: 配置代理或 CORS
2. **网络请求失败**: 检查 API 地址和网络状态
3. **页面渲染问题**: 检查数据格式和组件逻辑

### 后端问题

1. **数据库连接失败**: 检查连接字符串和数据库服务
2. **Redis 连接失败**: 检查 Redis 服务状态
3. **API 响应慢**: 优化数据库查询和添加缓存

## 开发工具推荐

### 前端工具

- **HBuilderX**: uniapp 官方 IDE
- **VSCode**: 轻量级编辑器
- **微信开发者工具**: 小程序调试

### 后端工具

- **PyCharm**: Python IDE
- **VSCode**: 轻量级编辑器
- **Postman**: API 测试工具
- **pgAdmin**: PostgreSQL 管理工具

### 通用工具

- **Git**: 版本控制
- **Docker**: 容器化
- **Postman**: API 测试
- **Insomnia**: API 测试
