# API 文档

## 概述

活动预约系统提供 RESTful API 接口，支持活动管理、用户管理、预约管理等功能。

## 基础信息

- **Base URL**: `http://localhost:8000/api` (开发环境)
- **Content-Type**: `application/json`
- **认证方式**: JWT Token

## 认证

### 微信登录

```http
POST /api/auth/wx-login
Content-Type: application/json

{
  "code": "微信授权码",
  "encryptedData": "加密数据",
  "iv": "初始向量"
}
```

**响应示例**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "openid": "o1234567890",
    "nickname": "用户昵称",
    "avatar": "头像URL",
    "phone": "手机号"
  }
}
```

## 用户管理

### 获取当前用户信息

```http
GET /api/users/me
Authorization: Bearer <token>
```

### 更新用户信息

```http
PUT /api/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "nickname": "新昵称",
  "phone": "新手机号"
}
```

## 活动管理

### 获取活动列表

```http
GET /api/activities?page=1&size=10&category=户外&keyword=爬山
```

**查询参数**:
- `page`: 页码 (默认: 1)
- `size`: 每页数量 (默认: 10)
- `category`: 活动分类
- `keyword`: 搜索关键词
- `location`: 地点筛选
- `start_date`: 开始日期
- `end_date`: 结束日期

### 获取活动详情

```http
GET /api/activities/{id}
```

### 创建活动

```http
POST /api/activities
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "活动标题",
  "description": "活动描述",
  "cover_image": "封面图片URL",
  "location": "活动地点",
  "organizer": "主办方",
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T18:00:00",
  "price": 100.0,
  "max_participants": 50
}
```

### 更新活动

```http
PUT /api/activities/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "更新后的标题",
  "description": "更新后的描述"
}
```

### 删除活动

```http
DELETE /api/activities/{id}
Authorization: Bearer <token>
```

### 搜索活动

```http
GET /api/activities/search?q=关键词&category=分类
```

### 获取热门活动

```http
GET /api/activities/hot?limit=10
```

## 预约管理

### 创建预约

```http
POST /api/bookings
Authorization: Bearer <token>
Content-Type: application/json

{
  "activity_id": 1,
  "name": "预约人姓名",
  "phone": "联系电话",
  "participants": 2,
  "remark": "备注信息"
}
```

### 获取我的预约

```http
GET /api/bookings/my?page=1&size=10&status=confirmed
Authorization: Bearer <token>
```

**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `status`: 预约状态 (pending, confirmed, cancelled, completed)

### 获取预约详情

```http
GET /api/bookings/{id}
Authorization: Bearer <token>
```

### 取消预约

```http
PUT /api/bookings/{id}/cancel
Authorization: Bearer <token>
```

### 签到

```http
PUT /api/bookings/{id}/checkin
Authorization: Bearer <token>
```

## 错误处理

### 错误响应格式

```json
{
  "detail": "错误描述",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### 常见错误码

- `400`: 请求参数错误
- `401`: 未认证或 token 无效
- `403`: 权限不足
- `404`: 资源不存在
- `422`: 数据验证失败
- `500`: 服务器内部错误

## 数据模型

### 用户 (User)

```json
{
  "id": 1,
  "openid": "微信openid",
  "nickname": "用户昵称",
  "avatar": "头像URL",
  "phone": "手机号",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 活动 (Activity)

```json
{
  "id": 1,
  "title": "活动标题",
  "description": "活动描述",
  "cover_image": "封面图片URL",
  "location": "活动地点",
  "organizer": "主办方",
  "start_time": "2024-01-01T10:00:00Z",
  "end_time": "2024-01-01T18:00:00Z",
  "price": 100.0,
  "max_participants": 50,
  "booked_count": 10,
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 预约 (Booking)

```json
{
  "id": 1,
  "user_id": 1,
  "activity_id": 1,
  "name": "预约人姓名",
  "phone": "联系电话",
  "participants": 2,
  "remark": "备注信息",
  "status": "confirmed",
  "checked_in": false,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

## 分页响应

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

## 认证说明

大部分 API 需要 JWT token 认证，请在请求头中添加：

```
Authorization: Bearer <your_token>
```

Token 可以通过微信登录接口获取，有效期为 30 分钟（可配置）。
