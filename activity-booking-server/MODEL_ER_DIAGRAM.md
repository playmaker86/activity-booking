# 活动预约系统 - 数据库 ER 图

## 实体关系图

```mermaid
erDiagram
    USERS {
        int id PK "主键"
        string openid UK "微信openid"
        string unionid "微信unionid"
        string nickname "昵称"
        string avatar "头像"
        string phone "手机号"
        int gender "性别"
        string country "国家"
        string province "省份"
        string city "城市"
        string language "语言"
        boolean is_active "是否激活"
        datetime created_at "创建时间"
        datetime updated_at "更新时间"
    }

    ACTIVITIES {
        int id PK "主键"
        string title "活动标题"
        text description "活动描述"
        string cover_image "封面图片"
        string location "活动地点"
        string organizer "主办方"
        datetime start_time "开始时间"
        datetime end_time "结束时间"
        float price "价格"
        int max_participants "最大参与人数"
        int booked_count "已预约人数"
        boolean is_active "是否启用"
        datetime created_at "创建时间"
        datetime updated_at "更新时间"
    }

    BOOKINGS {
        int id PK "主键"
        int user_id FK "用户ID"
        int activity_id FK "活动ID"
        string name "预约人姓名"
        string phone "联系电话"
        int participants "参与人数"
        string remark "备注"
        enum status "状态"
        int checked_in "是否签到"
        datetime created_at "创建时间"
        datetime updated_at "更新时间"
    }

    BOOKING_STATUS {
        string PENDING "待确认"
        string CONFIRMED "已确认"
        string CANCELLED "已取消"
        string COMPLETED "已完成"
    }

    %% 关系定义
    USERS ||--o{ BOOKINGS : "用户预约"
    ACTIVITIES ||--o{ BOOKINGS : "活动预约"
    BOOKINGS }o--|| BOOKING_STATUS : "预约状态"
```

## 关系说明

### 1. 用户 (USERS) ↔ 预约 (BOOKINGS)
- **关系类型**: 一对多 (1:N)
- **外键**: `bookings.user_id` → `users.id`
- **说明**: 一个用户可以预约多个活动

### 2. 活动 (ACTIVITIES) ↔ 预约 (BOOKINGS)
- **关系类型**: 一对多 (1:N)
- **外键**: `bookings.activity_id` → `activities.id`
- **说明**: 一个活动可以被多个用户预约

### 3. 预约状态 (BOOKING_STATUS)
- **类型**: 枚举值
- **可选值**: 
  - `pending` - 待确认
  - `confirmed` - 已确认
  - `cancelled` - 已取消
  - `completed` - 已完成

## 数据库约束

### 主键约束
- `users.id` - 用户主键
- `activities.id` - 活动主键
- `bookings.id` - 预约主键

### 唯一约束
- `users.openid` - 微信openid唯一

### 外键约束
- `bookings.user_id` → `users.id`
- `bookings.activity_id` → `activities.id`

### 索引
- `users.openid` - 微信登录索引
- `users.unionid` - 微信unionid索引
- `activities.is_active` - 活动状态索引

## 业务规则

1. **用户管理**
   - 用户通过微信openid唯一标识
   - 支持微信unionid跨应用识别
   - 用户信息可选择性填写

2. **活动管理**
   - 活动有明确的时间范围
   - 支持设置最大参与人数限制
   - 实时统计已预约人数
   - 支持软删除（is_active字段）

3. **预约管理**
   - 预约需要用户和活动信息
   - 支持多人预约（participants字段）
   - 预约状态流转：待确认 → 已确认 → 已完成
   - 支持取消操作
   - 支持签到功能

## 数据完整性

- **参照完整性**: 外键约束确保数据一致性
- **域完整性**: 枚举类型限制状态值
- **实体完整性**: 主键约束确保记录唯一性
- **用户定义完整性**: 业务规则约束（如时间范围、人数限制等）
