# API 响应格式规范

## 统一响应格式

所有 API 接口现在都使用统一的响应格式，包含以下字段：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "error": null,
  "timestamp": 1640995200
}
```

### 字段说明

- **code**: 业务状态码（数字）
- **message**: 响应消息（字符串）
- **data**: 响应数据（对象或数组，可为空）
- **error**: 错误信息（字符串，仅在错误时设置）
- **timestamp**: 响应时间戳（Unix 时间戳）

## 业务状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | 正常操作成功 |
| 201 | 创建成功 | 创建资源成功 |
| 400 | 请求参数错误 | 参数验证失败、业务逻辑错误 |
| 401 | 未授权 | 未登录或 token 无效 |
| 403 | 禁止访问 | 权限不足 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 409 | 冲突 | 资源冲突（如重复创建） |
| 500 | 服务器内部错误 | 系统异常 |
| 503 | 服务不可用 | 服务暂时不可用 |

## 响应示例

### 成功响应

#### 获取活动列表
```json
{
  "code": 200,
  "message": "获取活动列表成功",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "瑜伽课程",
        "description": "放松身心的瑜伽课程",
        "location": "瑜伽馆",
        "start_time": "2024-01-15T10:00:00",
        "end_time": "2024-01-15T11:00:00",
        "price": 50.0,
        "max_participants": 20,
        "booked_count": 5
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10
  },
  "error": null,
  "timestamp": 1640995200
}
```

#### 创建活动
```json
{
  "code": 201,
  "message": "创建活动成功",
  "data": {
    "id": 2,
    "title": "编程课程",
    "description": "Python 编程入门",
    "location": "计算机实验室",
    "start_time": "2024-01-16T14:00:00",
    "end_time": "2024-01-16T16:00:00",
    "price": 100.0,
    "max_participants": 15,
    "booked_count": 0
  },
  "error": null,
  "timestamp": 1640995200
}
```

### 错误响应

#### 资源不存在
```json
{
  "code": 404,
  "message": "活动不存在",
  "data": null,
  "error": "Activity with id 999 not found",
  "timestamp": 1640995200
}
```

#### 参数错误
```json
{
  "code": 400,
  "message": "活动不存在或已满员",
  "data": null,
  "error": "Activity not found or fully booked",
  "timestamp": 1640995200
}
```

#### 服务器错误
```json
{
  "code": 500,
  "message": "获取活动列表失败",
  "data": null,
  "error": "Database connection failed",
  "timestamp": 1640995200
}
```

## 前端处理建议

### JavaScript 示例

```javascript
// 处理 API 响应
function handleApiResponse(response) {
  const { code, message, data, error } = response;
  
  if (code === 200 || code === 201) {
    // 成功处理
    console.log('操作成功:', message);
    return data;
  } else {
    // 错误处理
    console.error('操作失败:', message);
    if (error) {
      console.error('错误详情:', error);
    }
    
    // 根据状态码进行不同处理
    switch (code) {
      case 400:
        // 参数错误，显示错误信息
        showError(message);
        break;
      case 401:
        // 未授权，跳转到登录页
        redirectToLogin();
        break;
      case 404:
        // 资源不存在，显示提示
        showNotFound(message);
        break;
      case 500:
        // 服务器错误，显示通用错误信息
        showServerError();
        break;
      default:
        showError(message);
    }
    
    return null;
  }
}

// 使用示例
fetch('/api/activities')
  .then(response => response.json())
  .then(handleApiResponse)
  .then(data => {
    if (data) {
      // 处理成功的数据
      renderActivities(data);
    }
  });
```

## 优势

1. **统一性**: 所有 API 接口使用相同的响应格式
2. **可读性**: 清晰的字段命名和结构
3. **可扩展性**: 易于添加新字段或状态码
4. **错误处理**: 统一的错误信息格式
5. **调试友好**: 包含时间戳和详细错误信息

## 注意事项

1. **向后兼容**: 现有的 API 接口保持兼容
2. **错误处理**: 所有异常都会被捕获并返回统一格式
3. **状态码**: 使用业务状态码而非 HTTP 状态码
4. **时间戳**: 所有响应都包含时间戳便于调试
