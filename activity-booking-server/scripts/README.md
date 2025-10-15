# 脚本目录

这个目录包含所有管理和运维脚本，按功能分类组织。

## 目录结构

```
scripts/
├── db/                 # 数据库管理脚本
│   ├── alembic/        # 数据库迁移工具
│   ├── alembic.ini     # Alembic 配置
│   ├── init_db.py      # 初始化数据库
│   ├── export_data.py  # 导出数据
│   ├── clear_database.py # 清空数据库
│   └── create_superuser.py # 创建超级用户
├── ops/                # 运维管理脚本
│   ├── run_script.py   # 脚本运行工具
│   └── README.md
└── README.md           # 本文件
```

## 快速开始

### 数据库管理

```bash
# 初始化数据库
uv run python scripts/db/init_db.py

# 执行数据库迁移
uv run alembic -c scripts/db/alembic.ini upgrade head

# 导出数据
uv run python scripts/db/export_data.py
```

### 使用脚本运行工具

```bash
# 查看所有可用脚本
uv run python scripts/ops/run_script.py

# 运行数据库脚本
uv run python scripts/ops/run_script.py db/init_db
uv run python scripts/ops/run_script.py db/export_data
```

## 分类说明

### 📁 db/ - 数据库管理

包含所有与数据库相关的脚本：
- **迁移管理**：Alembic 配置和迁移文件
- **数据初始化**：创建示例数据和基础数据
- **数据操作**：导出、清空、备份等
- **用户管理**：创建管理员账户

### 📁 ops/ - 运维管理

包含系统运维相关的脚本：
- **脚本运行工具**：统一的脚本执行接口
- **系统监控**：（可扩展）
- **部署脚本**：（可扩展）
- **日志分析**：（可扩展）

## 添加新脚本

### 数据库脚本

1. 在 `db/` 目录下创建新的 `.py` 文件
2. 导入必要的模块：
   ```python
   from app.database import SessionLocal
   from app.models import User, Activity, Booking
   ```
3. 更新 `db/README.md` 添加说明

### 运维脚本

1. 在 `ops/` 目录下创建新的 `.py` 文件
2. 实现脚本功能
3. 更新 `ops/README.md` 添加说明

## 设计原则

### 1. 按功能分类
- **db/**: 所有数据库相关的脚本和工具
- **ops/**: 系统运维和管理脚本

### 2. 工具集中化
- Alembic 迁移工具移到 `scripts/db/alembic/`
- 提供便捷的包装脚本
- 统一的脚本执行接口

### 3. 文档完善
- 每个目录都有详细的 README
- 提供示例代码和快速开始指南
- 包含最佳实践和注意事项

## 文档体系

### 主要文档
1. **`scripts/README.md`** - 脚本目录总览（本文件）
2. **`scripts/db/README.md`** - 数据库脚本使用指南
3. **`scripts/db/alembic/README.md`** - Alembic 详细使用指南
4. **`scripts/ops/README.md`** - 运维脚本说明

### 示例和演示
1. **`scripts/db/alembic/example_migration.py`** - 迁移示例代码
2. **`scripts/db/alembic/quick_start.py`** - 交互式演示脚本
3. **`.env.example`** - 环境变量配置示例

## 注意事项

- ⚠️ **危险脚本**：`db/clear_database.py` 会删除所有数据
- 所有脚本都会自动处理数据库连接和异常
- 建议在运行脚本前备份重要数据
- 使用 `scripts/ops/run_script.py` 可以统一管理所有脚本

## 扩展建议

### 可以添加的脚本

#### db/ 目录
- `backup.py` - 数据库备份
- `restore.py` - 数据库恢复
- `seed_data.py` - 种子数据生成
- `performance_test.py` - 数据库性能测试

#### ops/ 目录
- `deploy.py` - 部署脚本
- `health_check.py` - 健康检查
- `log_analyzer.py` - 日志分析
- `monitor.py` - 系统监控
- `cleanup.py` - 清理脚本