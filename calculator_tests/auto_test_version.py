"""
测试版本管理 - 基于pre-commit的智能版本控制
同步C前两位，只在测试代码变更时自增第三位
"""
import sys
import re
import subprocess


def get_c_version():
    """读取C++版本号前两位"""
    try:
        with open("calculator/version.h", "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open("calculator/version.h", "r", encoding="gbk") as f:
                content = f.read()
        except:
            # 如果还是失败，用二进制读取
            with open("calculator/version.h", "rb") as f:
                content = f.read().decode('utf-8', errors='ignore')

    major = int(re.search(r'CALC_MAJOR_VERSION\s+(\d+)', content).group(1))
    minor = int(re.search(r'CALC_MINOR_VERSION\s+(\d+)', content).group(1))
    return major, minor


def get_current_test_version():
    """读取当前测试版本信息"""
    try:
        with open("calculator_tests/test_version.py", "r") as f:
            test_content = f.read()
        current_major = int(re.search(r'C_MAJOR = (\d+)', test_content).group(1))
        current_minor = int(re.search(r'C_MINOR = (\d+)', test_content).group(1))
        current_rev = int(re.search(r'TEST_REVISION = (\d+)', test_content).group(1))
        return current_major, current_minor, current_rev
    except:
        return None, None, 1


def check_test_files_changed():
    """检查暂存区中test_interfaces.py是否有变更"""
    try:
        # 检查暂存区中test_interfaces.py是否有变化
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "calculator_tests/test_interfaces.py"],
            capture_output=True, text=True
        )

        # 如果有输出，说明在暂存区中有变更
        if result.stdout.strip():
            print(f"📝 检测到test_interfaces.py在暂存区有变更")
            return True
        else:
            print("ℹ️  test_interfaces.py在暂存区无变更")
            return False

    except Exception as e:
        print(f"⚠️  检查文件变更失败: {e}")
        return False


def update_test_version():
    """更新测试版本号"""
    # 1. 读取C++版本
    try:
        c_major, c_minor = get_c_version()
        print(f"📋 C++版本: {c_major}.{c_minor}")
    except Exception as e:
        print(f"❌ 读取C版本失败: {e}")
        return

    # 2. 读取当前测试版本
    current_major, current_minor, current_rev = get_current_test_version()

    # 3. 检查C++版本是否变化
    c_version_changed = (c_major != current_major or c_minor != current_minor)

    if c_version_changed:
        print(f"🔄 C++版本变化: {current_major}.{current_minor} → {c_major}.{c_minor}")
        # C++版本变化，重新从0开始计数
        new_rev = 0
    else:
        # C++版本未变，检查测试文件在暂存区是否有变更
        test_files_changed = check_test_files_changed()

        if test_files_changed:
            new_rev = current_rev + 1
            print(f"🔧 test_interfaces.py在本次提交中有变更，版本号: {current_rev} → {new_rev}")
        else:
            new_rev = current_rev
            print("ℹ️  test_interfaces.py在本次提交中无变更，版本号不变")

    # 4. 更新测试版本文件
    new_content = f"""# 测试版本管理
# 自动生成，请勿手动修改

C_MAJOR = {c_major}
C_MINOR = {c_minor}
TEST_REVISION = {new_rev}

TEST_VERSION = f"{{C_MAJOR}}.{{C_MINOR}}.{{TEST_REVISION}}"


def get_test_version():
    \"\"\"获取当前测试版本号\"\"\"
    return TEST_VERSION
"""

    with open("calculator_tests/test_version.py", "w") as f:
        f.write(new_content)

    print(f"✅ 测试版本: {c_major}.{c_minor}.{new_rev}")

    # 5. 如果版本文件有变化，自动添加到本次commit
    try:
        subprocess.run(["git", "add", "calculator_tests/test_version.py"], check=True)
        print("📦 版本文件已添加到暂存区")
    except:
        print("⚠️  无法自动添加版本文件到暂存区")


def main():
    """主函数"""
    print("🚀 开始测试版本检查...")
    update_test_version()
    print("🎉 版本检查完成")


if __name__ == "__main__":
    main()










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

