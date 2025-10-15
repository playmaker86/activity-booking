# API 命名规范

## 📋 概述

本项目的 API 返回数据使用 **驼峰命名（camelCase）**，这是前端 JavaScript/TypeScript 的标准命名方式。

## 🔄 自动转换机制

### 后端实现

所有的 Pydantic Schema 都继承自 `CamelCaseModel`，它会自动将蛇形命名转换为驼峰命名：

```python
from app.schemas.base import CamelCaseModel

class User(CamelCaseModel):
    id: int
    user_name: str      # 数据库字段：user_name
    created_at: datetime  # 数据库字段：created_at
```

### API 返回示例

**数据库字段（蛇形命名）**：
```python
{
    "id": 1,
    "user_name": "张三",
    "created_at": "2024-01-01T00:00:00Z",
    "is_active": true
}
```

**API 返回（驼峰命名）**：
```json
{
  "id": 1,
  "userName": "张三",
  "createdAt": "2024-01-01T00:00:00Z",
  "isActive": true
}
```

## 📝 常见字段转换对照表

| 数据库字段（蛇形）| API 返回（驼峰）|
|----------------|----------------|
| `user_id` | `userId` |
| `created_at` | `createdAt` |
| `updated_at` | `updatedAt` |
| `is_active` | `isActive` |
| `cover_image` | `coverImage` |
| `start_time` | `startTime` |
| `end_time` | `endTime` |
| `max_participants` | `maxParticipants` |
| `booked_count` | `bookedCount` |
| `activity_id` | `activityId` |
| `checked_in` | `checkedIn` |
| `token_type` | `tokenType` |

## 🎯 前端使用

### TypeScript 接口定义

```typescript
// 用户接口
interface User {
  id: number;
  openid: string;
  nickname?: string;
  avatar?: string;
  phone?: string;
  createdAt: string;
  updatedAt: string;
}

// 活动接口
interface Activity {
  id: number;
  title: string;
  description?: string;
  coverImage?: string;
  location?: string;
  organizer?: string;
  startTime: string;
  endTime: string;
  price: number;
  maxParticipants: number;
  bookedCount: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

// 预约接口
interface Booking {
  id: number;
  userId: number;
  activityId: number;
  name: string;
  phone: string;
  participants: number;
  remark?: string;
  status: string;
  checkedIn: number;
  createdAt: string;
  updatedAt: string;
  activity?: Activity;
}
```

### 前端请求示例

```typescript
// 获取用户信息
const response = await fetch('/api/users/me');
const user: User = await response.json();
console.log(user.createdAt); // 直接使用驼峰命名

// 创建活动
const activity = {
  title: "周末徒步",
  startTime: "2024-01-01T09:00:00Z",
  endTime: "2024-01-01T17:00:00Z",
  maxParticipants: 20
};
await fetch('/api/activities', {
  method: 'POST',
  body: JSON.stringify(activity)
});
```

## 🔧 自定义 Schema

如果需要创建新的 Schema，请继承 `CamelCaseModel`：

```python
from app.schemas.base import CamelCaseModel
from typing import Optional

class MyCustomSchema(CamelCaseModel):
    """自定义 Schema"""
    my_field: str
    another_field: Optional[int] = None
    created_at: datetime
```

API 返回时会自动转换为：
```json
{
  "myField": "value",
  "anotherField": 123,
  "createdAt": "2024-01-01T00:00:00Z"
}
```

## 📤 客户端传参规范

### 推荐方式：使用驼峰命名 ✅

前端发送请求时，**推荐使用驼峰命名**，保持前后端一致：

```typescript
// ✅ 推荐：使用驼峰命名
const activityData = {
  title: "周末徒步",
  coverImage: "https://example.com/cover.jpg",  // 驼峰
  startTime: "2024-01-01T09:00:00Z",            // 驼峰
  endTime: "2024-01-01T17:00:00Z",              // 驼峰
  maxParticipants: 20                            // 驼峰
};

await fetch('/api/activities', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(activityData)
});
```

### 兼容模式：蛇形命名也可以 ⚠️

后端配置了 `populate_by_name=True`，所以蛇形命名也能识别（但不推荐）：

```typescript
// ⚠️ 也可以但不推荐：蛇形命名
const activityData = {
  title: "周末徒步",
  cover_image: "https://example.com/cover.jpg",  // 蛇形
  start_time: "2024-01-01T09:00:00Z",            // 蛇形
  end_time: "2024-01-01T17:00:00Z",              // 蛇形
  max_participants: 20                            // 蛇形
};
```

**建议**：为了代码一致性和可读性，前端请统一使用驼峰命名。

## ⚠️ 注意事项

1. **客户端发送数据**：推荐使用驼峰命名，蛇形命名也兼容

2. **数据库字段**：数据库字段保持蛇形命名（Python 标准）

3. **API 返回**：API 返回数据统一使用驼峰命名（JavaScript 标准）

4. **一致性**：所有 API 端点都遵循这个规范，确保前后端接口的一致性

## 🚀 性能优化

项目使用 `orjson` 作为 JSON 序列化库，相比标准库性能提升约 2-3 倍：

```python
# main.py
app = FastAPI(
    default_response_class=ORJSONResponse,  # 使用 orjson
)
```

## 📚 参考资源

- [Pydantic 文档 - Alias Generator](https://docs.pydantic.dev/latest/concepts/alias/)
- [FastAPI 文档 - Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [JavaScript 命名规范](https://google.github.io/styleguide/jsguide.html#naming)

