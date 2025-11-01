"""
测试版本 - 同步C前两位，自增第三位
"""
import sys
import re


def update_test_version():
    # 读取C版本前两位
    try:
        with open("../calculator/version.h", "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open("../calculator/version.h", "r", encoding="gbk") as f:
                content = f.read()
        except:
            # 如果还是失败，用二进制读取
            with open("../calculator/version.h", "rb") as f:
                content = f.read().decode('utf-8', errors='ignore')
    major = int(re.search(r'CALC_MAJOR_VERSION\s+(\d+)', content).group(1))
    minor = int(re.search(r'CALC_MINOR_VERSION\s+(\d+)', content).group(1))

    # 读取当前测试修订号
    try:
        with open("test_version.py", "r") as f:
            test_content = f.read()
        current_rev = int(re.search(r'TEST_REVISION = (\d+)', test_content).group(1))
        new_rev = current_rev + 1
    except:
        new_rev = 1

    # 更新测试版本
    new_content = f"""
                C_MAJOR = {major}
                C_MINOR = {minor}
                TEST_REVISION = {new_rev}
                
                TEST_VERSION = f"{{C_MAJOR}}.{{C_MINOR}}.{{TEST_REVISION}}"
                
                def get_test_version():
                    return TEST_VERSION
                """
    with open("test_version.py", "w") as f:
        f.write(new_content)

    print(f"✅ 测试版本: {major}.{minor}.{new_rev}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test_bug":
        update_test_version()
    else:
        update_test_version()  # 默认也执行

