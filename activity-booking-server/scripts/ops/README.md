# 运维管理脚本

这个目录包含系统运维和管理相关的脚本。

## 目录结构

```
ops/
├── run_script.py    # 脚本运行工具
└── README.md        # 本文件
```

## 脚本运行工具

`run_script.py` 提供统一的脚本执行接口，可以方便地运行任何脚本。

### 使用方法

```bash
# 查看所有可用脚本
uv run python scripts/ops/run_script.py

# 运行特定脚本
uv run python scripts/ops/run_script.py <脚本名>
```

### 示例

```bash
# 运行数据库初始化脚本
uv run python scripts/ops/run_script.py db/init_db

# 运行数据导出脚本
uv run python scripts/ops/run_script.py db/export_data

# 运行超级用户创建脚本
uv run python scripts/ops/run_script.py db/create_superuser
```

## 扩展运维脚本

可以在这个目录下添加更多运维相关的脚本，例如：

- `backup.py` - 系统备份
- `deploy.py` - 部署脚本
- `monitor.py` - 系统监控
- `log_analyzer.py` - 日志分析
- `health_check.py` - 健康检查