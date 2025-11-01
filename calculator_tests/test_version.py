# 测试版本管理
# 自动生成，请勿手动修改

C_MAJOR = 1
C_MINOR = 19
TEST_REVISION = 1

TEST_VERSION = f"{C_MAJOR}.{C_MINOR}.{TEST_REVISION}"


def get_test_version():
    """获取当前测试版本号"""
    return TEST_VERSION
