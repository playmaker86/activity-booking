#!/usr/bin/env python3
"""
Alembic 快速开始脚本

这个脚本演示了 Alembic 的基本使用流程
"""

import os
import sys
import subprocess

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 成功")
        if result.stdout:
            print(result.stdout)
    else:
        print("❌ 失败")
        if result.stderr:
            print(result.stderr)
    
    return result.returncode == 0


def main():
    """演示 Alembic 的基本使用流程"""
    print("🚀 Alembic 快速开始演示")
    print("=" * 50)
    
    alembic_ini = "scripts/db/alembic.ini"
    
    # 1. 查看当前状态
    print("\n📋 步骤 1: 查看当前数据库状态")
    run_command(["uv", "run", "alembic", "-c", alembic_ini, "current"], "查看当前版本")
    
    # 2. 查看迁移历史
    print("\n📜 步骤 2: 查看迁移历史")
    run_command(["uv", "run", "alembic", "-c", alembic_ini, "history"], "查看迁移历史")
    
    # 3. 创建示例迁移（如果有模型变化）
    print("\n🛠️  步骤 3: 创建示例迁移")
    print("注意：只有在模型发生变化时才会生成新的迁移文件")
    
    # 检查是否有模型变化
    result = run_command(
        ["uv", "run", "alembic", "-c", alembic_ini, "revision", "--autogenerate", "-m", "demo migration"],
        "生成迁移文件"
    )
    
    if result:
        print("✅ 迁移文件已生成")
        
        # 4. 查看生成的迁移文件
        print("\n📁 步骤 4: 查看生成的迁移文件")
        versions_dir = "scripts/db/alembic/versions"
        if os.path.exists(versions_dir):
            files = [f for f in os.listdir(versions_dir) if f.endswith('.py')]
            if files:
                latest_file = sorted(files)[-1]
                print(f"最新迁移文件: {latest_file}")
                
                # 显示文件内容的前几行
                with open(os.path.join(versions_dir, latest_file), 'r') as f:
                    lines = f.readlines()[:20]
                    print("\n文件内容预览:")
                    for line in lines:
                        print(line.rstrip())
                    if len(f.readlines()) > 20:
                        print("...")
        
        # 5. 执行迁移（可选）
        print("\n⚠️  步骤 5: 执行迁移")
        print("注意：这将修改数据库结构，请确保已备份重要数据")
        
        confirm = input("是否要执行迁移？(y/N): ").strip().lower()
        if confirm == 'y':
            run_command(["uv", "run", "alembic", "-c", alembic_ini, "upgrade", "head"], "执行数据库迁移")
        else:
            print("跳过迁移执行")
    
    # 6. 最终状态
    print("\n📊 步骤 6: 查看最终状态")
    run_command(["uv", "run", "alembic", "-c", alembic_ini, "current"], "查看当前版本")
    
    print("\n🎉 Alembic 快速开始演示完成！")
    print("\n💡 提示:")
    print("- 使用 'uv run alembic -c scripts/db/alembic.ini --help' 查看所有可用命令")
    print("- 使用 'uv run python scripts/db/migrate.py' 使用便捷脚本")
    print("- 查看 scripts/db/alembic/README.md 获取详细文档")


if __name__ == "__main__":
    main()
