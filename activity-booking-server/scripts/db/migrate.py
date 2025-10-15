#!/usr/bin/env python3
"""
数据库迁移便捷脚本
提供常用的数据库迁移命令
"""
import sys
import os
import subprocess

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


def run_alembic_command(command):
    """运行 alembic 命令"""
    alembic_ini = os.path.join(os.path.dirname(__file__), "alembic.ini")
    cmd = ["uv", "run", "alembic", "-c", alembic_ini] + command
    return subprocess.run(cmd, cwd=project_root)


def migrate_up():
    """升级到最新版本"""
    print("升级数据库到最新版本...")
    result = run_alembic_command(["upgrade", "head"])
    if result.returncode == 0:
        print("✅ 数据库升级成功")
    else:
        print("❌ 数据库升级失败")


def migrate_down():
    """回滚一个版本"""
    print("回滚数据库一个版本...")
    result = run_alembic_command(["downgrade", "-1"])
    if result.returncode == 0:
        print("✅ 数据库回滚成功")
    else:
        print("❌ 数据库回滚失败")


def create_migration(message):
    """创建新的迁移"""
    if not message:
        print("❌ 请提供迁移描述信息")
        return
    
    print(f"创建迁移: {message}")
    result = run_alembic_command(["revision", "--autogenerate", "-m", message])
    if result.returncode == 0:
        print("✅ 迁移创建成功")
    else:
        print("❌ 迁移创建失败")


def show_current():
    """显示当前版本"""
    print("当前数据库版本:")
    run_alembic_command(["current"])


def show_history():
    """显示迁移历史"""
    print("迁移历史:")
    run_alembic_command(["history"])


def main():
    if len(sys.argv) < 2:
        print("用法: python migrate.py <command> [args...]")
        print()
        print("可用命令:")
        print("  up                 - 升级到最新版本")
        print("  down               - 回滚一个版本")
        print("  create <message>   - 创建新迁移")
        print("  current            - 显示当前版本")
        print("  history            - 显示迁移历史")
        return
    
    command = sys.argv[1]
    
    if command == "up":
        migrate_up()
    elif command == "down":
        migrate_down()
    elif command == "create":
        message = sys.argv[2] if len(sys.argv) > 2 else "auto migration"
        create_migration(message)
    elif command == "current":
        show_current()
    elif command == "history":
        show_history()
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
