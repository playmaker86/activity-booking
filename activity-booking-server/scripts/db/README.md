# 数据库管理脚本

这个目录包含所有与数据库相关的管理脚本和工具。

## 目录结构

```
db/
├── alembic/                    # 数据库迁移工具
│   ├── versions/               # 迁移版本文件目录
│   ├── env.py                  # Alembic 环境配置
│   ├── script.py.mako          # 迁移脚本模板
│   ├── README.md               # Alembic 详细使用指南
│   ├── example_migration.py    # 迁移示例代码
│   └── quick_start.py          # 快速开始演示脚本
├── alembic.ini                 # Alembic 配置文件
├── migrate.py                  # 便捷迁移脚本
├── init_db.py                  # 初始化数据库和示例数据
├── clear_database.py           # 清空数据库（⚠️ 危险）
├── export_data.py              # 导出数据为 JSON
└── create_superuser.py         # 创建超级用户
```

## 数据库迁移

### 快速开始

```bash
# 运行快速开始演示
uv run python scripts/db/alembic/quick_start.py
```

### 使用便捷脚本

```bash
# 升级到最新版本
uv run python scripts/db/migrate.py up

# 回滚一个版本
uv run python scripts/db/migrate.py down

# 创建新迁移
uv run python scripts/db/migrate.py create "描述信息"

# 查看当前版本
uv run python scripts/db/migrate.py current

# 查看迁移历史
uv run python scripts/db/migrate.py history
```

### 直接使用 Alembic

```bash
# 创建迁移
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "描述信息"

# 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head

# 回滚迁移
uv run alembic -c scripts/db/alembic.ini downgrade -1

# 查看状态
uv run alembic -c scripts/db/alembic.ini current
uv run alembic -c scripts/db/alembic.ini history
```

### 📚 详细文档

- **完整指南**: `scripts/db/alembic/README.md` - Alembic 详细使用指南
- **示例代码**: `scripts/db/alembic/example_migration.py` - 各种迁移示例
- **快速演示**: `scripts/db/alembic/quick_start.py` - 交互式演示脚本

## 数据管理脚本

### 初始化数据库

```bash
uv run python scripts/db/init_db.py
```

### 导出数据

```bash
uv run python scripts/db/export_data.py
```

### 清空数据库

```bash
uv run python scripts/db/clear_database.py
```

⚠️ **警告**：`clear_database.py` 会删除所有数据，请谨慎使用！

### 创建超级用户

```bash
uv run python scripts/db/create_superuser.py
```

## 常用工作流程

### 1. 初始化新环境

```bash
# 1. 创建初始迁移
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "Initial migration"

# 2. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head

# 3. 初始化示例数据
uv run python scripts/db/init_db.py
```

### 2. 添加新字段后的迁移

```bash
# 1. 修改模型文件（app/models/）
# 2. 生成迁移文件
uv run alembic -c scripts/db/alembic.ini revision --autogenerate -m "add new field"

# 3. 检查生成的迁移文件
# 4. 执行迁移
uv run alembic -c scripts/db/alembic.ini upgrade head
```

### 3. 数据备份和恢复

```bash
# 备份
uv run python scripts/db/export_data.py

# 清空（谨慎！）
uv run python scripts/db/clear_database.py

# 恢复（需要手动实现恢复脚本）
```
