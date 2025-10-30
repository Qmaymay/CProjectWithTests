#!/usr/bin/env python3
"""
最简单的测试脚本 - 使用现有的构建系统
在项目根目录运行
"""

import subprocess
import sys
import os

def main():
    print("🎯 简单测试开始")

    # 1. 使用现有的build.bat构建
    print("\\n1️⃣ 使用build.bat构建...")
    result = subprocess.run("build.bat", shell=True)
    if result.returncode == 0:
        print("✅ 构建成功")
    else:
        print("❌ 构建失败")
        return False

    # 2. 检查库文件是否存在
    lib_path = os.path.join("lib", "libcalculator.dll")
    if os.path.exists(lib_path):
        print(f"✅ 库文件存在: {lib_path}")
    else:
        print(f"❌ 库文件不存在: {lib_path}")
        return False

    # 3. 运行测试
    print("\\n2️⃣ 运行测试...")
    tests_dir = "calculator_tests"
    if os.path.exists(tests_dir):
        result = subprocess.run(
            "python test_interfaces.py", 
            shell=True, 
            cwd=tests_dir
        )
        if result.returncode == 0:
            print("\\n🎉 所有测试通过！")
            return True
        else:
            print("\\n💥 测试失败")
            return False
    else:
        print("❌ 测试目录不存在")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
