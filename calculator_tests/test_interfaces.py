import ctypes
import os
import sys

# 加载共享库
lib_path = os.path.join(os.path.dirname(__file__), '../lib/libcalculator.so')
print(f"加载库：{lib_path}")

try:
    lib = ctypes.CDLL(lib_path)
    print("✅ 库加载成功")
except Exception as e:
    print(f"❌ 库加载失败: {e}")
    sys.exit(1)

# 定义函数原型
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
lib.subtract.restype = ctypes.c_int

lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
lib.multiply.restype = ctypes.c_int

lib.divide.argtypes = [ctypes.c_int, ctypes.c_int]
lib.divide.restype = ctypes.c_double

lib.square.argtypes = [ctypes.c_int]
lib.square.restype = ctypes.c_int


def test_add():
    """测试加法接口"""
    print("🧪 测试加法接口...")
    result = lib.add(10, 5)
    assert result == 15, f"加法测试失败: 10 + 5 = {result}, 期望 15"
    print("✅ 加法接口测试通过：10 + 5 = 15")


def test_subtract():
    """测试减法接口"""
    print("🧪 测试减法接口...")
    result = lib.subtract(10, 5)
    assert result == 5, f"减法测试失败: 10 - 5 = {result}, 期望 5"
    print("✅ 减法接口测试通过：10 - 5 = 5")


def test_multiply():
    """测试乘法接口"""
    print("🧪 测试乘法接口...")
    result = lib.multiply(10, 5)
    assert result == 50, f"乘法测试失败: 10 * 5 = {result}, 期望 50"
    print("✅ 乘法接口测试通过：10 * 5 = 50")


def test_divide():
    """测试除法接口"""
    print("🧪 测试除法接口...")
    result = lib.divide(10, 5)
    assert result == 2.0, f"除法测试失败: 10 / 5 = {result}, 期望 2.0"
    print("✅ 除法接口测试通过：10 / 5 = 2.0")


def test_square():
    """测试平方接口"""
    print("🧪 测试平方接口...")
    result = lib.square(5)
    assert result == 25, f"平方测试失败: 5² = {result}, 期望 25"
    print("✅ 平方接口测试通过：5² = 25")

    # 测试另一个值
    result2 = lib.square(3)
    assert result2 == 9, f"平方测试失败: 3² = {result2}, 期望 9"
    print("✅ 平方接口测试通过：3² = 9")


def run_all_tests():
    """运行所有接口测试"""
    print("\n🚀 开始接口单独测试...")
    print("=" * 50)

    tests = [
        test_add,
        test_subtract,
        test_multiply,
        test_divide,
        test_square
    ]

    passed = 0
    total = len(tests)
    failed_tests = []

    for test in tests:
        try:
            test()
            passed += 1
            print("")  # 空行分隔
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}\n")
            failed_tests.append(test.__name__)

    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")

    if failed_tests:
        print(f"❌ 失败的测试: {', '.join(failed_tests)}")
        return False
    else:
        print("🎉 所有接口测试通过！")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)