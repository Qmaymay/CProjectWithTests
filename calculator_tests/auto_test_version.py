"""
测试版本管理 - 基于文件哈希的智能版本控制
同一个C版本号下，只有test_interfaces.py内容变化时才增加版本号
"""
import subprocess
import re
import hashlib
import os


def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def get_previous_file_hash():
    """获取上一次commit中test_interfaces.py的哈希值"""
    try:
        # 获取上一次commit的文件内容
        result = subprocess.run(
            ["git", "show", "HEAD:calculator_tests/test_interfaces.py"],
            capture_output=True
        )
        if result.returncode == 0:
            return hashlib.md5(result.stdout).hexdigest()
    except:
        pass
    return None


def update_test_version():
    # 🎯 修复路径问题：直接从项目根目录读取
    version_h_path = "calculator/version.h"
    test_version_path = "calculator_tests/test_version.py"
    test_interfaces_path = "calculator_tests/test_interfaces.py"

    # 1. 读取C++版本号
    try:
        with open(version_h_path, "r", encoding="utf-8") as f:
            content = f.read()
        major = int(re.search(r'CALC_MAJOR_VERSION\s+(\d+)', content).group(1))
        minor = int(re.search(r'CALC_MINOR_VERSION\s+(\d+)', content).group(1))
    except FileNotFoundError:
        print(f"❌ 找不到文件: {version_h_path}")
        return
    except Exception as e:
        print(f"❌ 读取C版本失败: {e}")
        return

    # 2. 读取当前测试版本号
    try:
        with open(test_version_path, "r") as f:
            test_content = f.read()
        current_rev = int(re.search(r'TEST_REVISION = (\d+)', test_content).group(1))
    except:
        current_rev = 1

    # 3. 🎯 核心检查：比较文件哈希值
    current_hash = get_file_hash(test_interfaces_path)
    previous_hash = get_previous_file_hash()

    print(f"🔍 文件哈希比较:")
    print(f"   当前: {current_hash}")
    print(f"   上次: {previous_hash}")

    if current_hash and previous_hash and current_hash != previous_hash:
        new_rev = current_rev + 1
        print(f"🔧 test_interfaces.py 内容有变化，版本号: {current_rev} → {new_rev}")
    else:
        new_rev = current_rev
        print("ℹ️  test_interfaces.py 内容无变化，版本号不变")

    # 4. 更新版本文件
    new_content = f"""
C_MAJOR = {major}
C_MINOR = {minor}
TEST_REVISION = {new_rev}

TEST_VERSION = f"{{C_MAJOR}}.{{C_MINOR}}.{{TEST_REVISION}}"


def get_test_version():
    return TEST_VERSION
"""
    with open(test_version_path, "w") as f:
        f.write(new_content)

    print(f"✅ 测试版本: {major}.{minor}.{new_rev}")

    # 5. 自动把版本文件变更加入commit
    subprocess.run(["git", "add", test_version_path])
    print("📦 版本文件已添加到暂存区")


if __name__ == "__main__":
    update_test_version()



















# """
# 测试版本 - 同步C前两位，自增第三位
# """
# import sys
# import re
#
#
# def update_test_version():
#     # 读取C版本前两位
#     try:
#         with open("../calculator/version.h", "r", encoding="utf-8") as f:
#             content = f.read()
#     except UnicodeDecodeError:
#         try:
#             with open("../calculator/version.h", "r", encoding="gbk") as f:
#                 content = f.read()
#         except:
#             # 如果还是失败，用二进制读取
#             with open("../calculator/version.h", "rb") as f:
#                 content = f.read().decode('utf-8', errors='ignore')
#
#     major = int(re.search(r'CALC_MAJOR_VERSION\s+(\d+)', content).group(1))
#     minor = int(re.search(r'CALC_MINOR_VERSION\s+(\d+)', content).group(1))
#
#     # 读取当前测试修订号
#     try:
#         with open("test_version.py", "r") as f:
#             test_content = f.read()
#         current_rev = int(re.search(r'TEST_REVISION = (\d+)', test_content).group(1))
#         new_rev = current_rev + 1
#     except:
#         new_rev = 1
#
#     # 更新测试版本
#     new_content = f"""
# C_MAJOR = {major}
# C_MINOR = {minor}
# TEST_REVISION = {new_rev}
#
# EST_VERSION = f"{{C_MAJOR}}.{{C_MINOR}}.{{TEST_REVISION}}"
#
# def get_test_version():
# return TEST_VERSION
# """
#     with open("test_version.py", "w") as f:
#         f.write(new_content)
#
#     print(f"✅ 测试版本: {major}.{minor}.{new_rev}")
#
#
# if __name__ == "__main__":
#     if len(sys.argv) > 1 and sys.argv[1] == "test_bug":
#         update_test_version()
#     else:
#         update_test_version()  # 默认也执行

