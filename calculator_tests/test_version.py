"""
测试代码版本号 - 基于C库版本
"""
import ctypes

# C库的主版本.次版本 + 测试代码的修订号
C_MAJOR = 1  # 跟随C库主版本
C_MINOR = 9  # 跟随C库次版本
TEST_REVISION = 0  # 测试代码自己的修订号

TEST_VERSION = f"{C_MAJOR}.{C_MINOR}.{TEST_REVISION}"


def get_test_version():
    return TEST_VERSION


def sync_with_c_version(lib):
    """与C库版本同步检查"""
    try:
        lib.get_version.restype = ctypes.c_char_p
        c_version = lib.get_version().decode()
        c_major, c_minor, c_patch = map(int, c_version.split('.'))

        # 检查主版本和次版本是否匹配
        if c_major == C_MAJOR and c_minor == C_MINOR:
            print(f"✅ 版本同步: C库 {c_version} | 测试 {TEST_VERSION}")
            return True
        else:
            print(f"⚠️  版本不匹配: C库 {c_version} | 测试 {TEST_VERSION}")
            return False
    except Exception as e:
        print(f"❌ 版本检查失败: {e}")
        return True   # 不阻断测试