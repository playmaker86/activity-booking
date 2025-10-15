# Alembic 数据库迁移工具使用指南

Alembic 是一个数据库迁移工具，用于管理数据库结构的变化。本指南将展示如何在活动预约系统中使用 Alembic。

## 目录结构

```
alembic/
├── versions/          # 迁移版本文件目录
│   ├── 001_initial_migration.py
│   ├── 002_add_user_avatar.py
│   └── ...
├── env.py            # Alembic 环境配置
├── script.py.mako    # 迁移脚本模板
└── README.md         # 本文件
```

## 基本概念

### 迁移版本 (Revision)
每个迁移都有一个唯一的版本号，通常格式为：`revision_id_description`

### 升级 (Upgrade)
应用新的数据库更改，向前迁移

### 回滚 (Downgrade)
撤销之前的数据库更改，向后迁移

## 常用命令

### 1. 创建迁移

```bash
# 从项目根目录运行
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "描述信息"

# 示例：添加用户头像字段
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "add user avatar field"
```

### 2. 执行迁移

```bash
# 升级到最新版本
uv run alembic -c scripts/db/alembic.ini upgrade head

# 升级一个版本
uv run alembic -c scripts/db/alembic.ini upgrade +1

# 升级到特定版本
uv run alembic -c scripts/db/alembic.ini upgrade <revision_id>
```

### 3. 回滚迁移

```bash
# 回滚一个版本
uv run alembic -c scripts/db/alembic.ini downgrade -1

# 回滚到特定版本
uv run alembic -c scripts/db/alembic.ini downgrade <revision_id>

# 回滚到基础版本
uv run alembic -c scripts/db/alembic.ini downgrade base
```

### 4. 查看状态

```bash
# 查看当前版本
uv run alembic -c scripts/db/alembic.ini current

# 查看迁移历史
uv run alembic -c scripts/db/alembic.ini history

# 查看详细的迁移历史
uv run alembic -c scripts/db/alembic.ini history --verbose
```

## 实际使用示例

### 示例 1：初始迁移

```bash
# 1. 首次创建迁移（初始化所有表）
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "Initial migration"

# 2. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### 示例 2：添加新字段

假设我们要为用户表添加头像字段：

```python
# 1. 修改 app/models/user.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True, nullable=False)
    nickname = Column(String(100))
    avatar = Column(String(500))  # 新增字段
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

```bash
# 2. 生成迁移
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "add user avatar field"

# 3. 检查生成的迁移文件
# 查看 scripts/db/alembic/versions/ 目录下的新文件

# 4. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### 示例 3：修改字段类型

```python
# 1. 修改模型
class Activity(Base):
    __tablename__ = "activities"
    
    # 将 price 从 Float 改为 Integer（以分为单位）
    price = Column(Integer, default=0)  # 原来是 Float
```

```bash
# 2. 生成迁移
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "change price to integer"

# 3. 可能需要手动编辑迁移文件，添加数据转换逻辑
# 4. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### 示例 4：创建索引

```python
# 1. 在模型中添加索引
class Booking(Base):
    __tablename__ = "bookings"
    
    # 为 user_id 和 activity_id 创建复合索引
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, index=True)
    
    __table_args__ = (
        Index('ix_booking_user_activity', 'user_id', 'activity_id'),
    )
```

```bash
# 2. 生成迁移
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "add booking indexes"

# 3. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### 示例 5：数据迁移

有时需要在结构变更的同时迁移数据：

```bash
# 1. 生成空迁移（不自动检测变化）
uv run alembic -c scripts/db/alembic.ini revision -m "migrate user data"

# 2. 手动编辑迁移文件
```

```python
# 生成的迁移文件示例
def upgrade() -> None:
    # 添加新字段
    op.add_column('users', sa.Column('full_name', sa.String(200), nullable=True))
    
    # 数据迁移：将 nickname 复制到 full_name
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = nickname WHERE full_name IS NULL"
    )

def downgrade() -> None:
    # 删除新字段
    op.drop_column('users', 'full_name')
```

## 使用便捷脚本

项目提供了便捷的迁移脚本：

```bash
# 使用便捷脚本
uv run python scripts/db/migrate.py up          # 升级
uv run python scripts/db/migrate.py down        # 回滚
uv run python scripts/db/migrate.py create "描述" # 创建迁移
uv run python scripts/db/migrate.py current     # 查看当前版本
uv run python scripts/db/migrate.py history     # 查看历史
```

## 最佳实践

### 1. 迁移文件命名

- 使用描述性的名称
- 包含操作类型：`add_`, `remove_`, `change_`, `create_`
- 示例：
  - `001_initial_migration.py`
  - `002_add_user_avatar.py`
  - `003_change_price_to_integer.py`

### 2. 迁移文件内容

- 总是提供 `upgrade()` 和 `downgrade()` 函数
- 对于数据迁移，先执行结构变更，再执行数据操作
- 使用事务确保操作的原子性

### 3. 团队协作

- 每次修改模型后立即生成迁移
- 不要修改已提交的迁移文件
- 在合并代码前确保迁移文件同步

### 4. 生产环境

- 在应用部署前备份数据库
- 先在小范围测试迁移
- 监控迁移执行时间，避免长时间锁表

## 常见问题

### Q: 迁移失败怎么办？

```bash
# 查看当前状态
uv run alembic -c scripts/db/alembic.ini current

# 查看迁移历史
uv run alembic -c scripts/db/alembic.ini history

# 回滚到上一个版本
uv run alembic -c scripts/db/alembic.ini downgrade -1

# 修复问题后重新执行
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### Q: 如何合并多个开发分支的迁移？

```bash
# 1. 合并冲突的迁移文件
# 2. 重新生成迁移ID
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "merge migrations"

# 3. 手动编辑生成的迁移文件
```

### Q: 如何重置数据库？

```bash
# 回滚到基础版本
uv run alembic -c scripts/db/alembic.ini downgrade base

# 重新执行所有迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

## 配置文件说明

### alembic.ini

```ini
[alembic]
# 迁移脚本位置
script_location = scripts/db/alembic

# 数据库连接URL（从环境变量读取）
sqlalchemy.url = driver://user:pass@localhost/dbname
```

### env.py

主要配置：
- 导入模型：`from app.models import *`
- 设置目标元数据：`target_metadata = Base.metadata`
- 数据库URL：从环境变量读取

## 注意事项

1. **备份数据**：执行迁移前务必备份重要数据
2. **测试迁移**：在开发环境充分测试后再应用到生产环境
3. **版本控制**：将迁移文件纳入版本控制
4. **文档记录**：为复杂迁移编写详细的注释
5. **性能考虑**：大表迁移可能需要分批处理

通过遵循这些指南，你可以安全、高效地管理数据库结构的变化。
