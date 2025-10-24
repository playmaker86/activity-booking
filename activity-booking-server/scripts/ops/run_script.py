#!/usr/bin/env python3
"""
脚本运行工具
提供统一的脚本执行接口
"""
import importlib.util
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def run_script(script_name):
    """运行指定的脚本"""
    scripts_dir = os.path.dirname(os.path.dirname(__file__))  # 回到 scripts 目录
    script_path = os.path.join(scripts_dir, f"{script_name}.py")
    
    if not os.path.exists(script_path):
        print(f"错误：脚本 '{script_name}.py' 不存在")
        print("可用的脚本：")
        list_scripts()
        return
    
    print(f"运行脚本: {script_name}.py")
    print("-" * 50)
    
    # 动态导入并执行脚本
    spec = importlib.util.spec_from_file_location(script_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def list_scripts():
    """列出所有可用的脚本"""
    scripts_dir = os.path.dirname(os.path.dirname(__file__))  # 回到 scripts 目录
    scripts = []
    
    # 递归查找所有 Python 脚本
    for root, dirs, files in os.walk(scripts_dir):
        # 跳过 __pycache__ 目录
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py') and file not in ['__init__.py', 'run_script.py', 'migrate.py']:
                # 计算相对路径
                rel_path = os.path.relpath(os.path.join(root, file), scripts_dir)
                script_name = rel_path[:-3].replace(os.sep, '/')  # 移除 .py 扩展名并替换路径分隔符
                scripts.append(script_name)
    
    if scripts:
        for script in sorted(scripts):
            print(f"  - {script}")
    else:
        print("  没有找到可用的脚本")


def main():
    if len(sys.argv) < 2:
        print("用法: python run_script.py <脚本名>")
        print()
        print("可用的脚本：")
        list_scripts()
        return
    
    script_name = sys.argv[1]
    run_script(script_name)


if __name__ == "__main__":
    main()
