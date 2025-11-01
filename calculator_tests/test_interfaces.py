
# TODO CMakeLists.txt告诉编译器如何把calculator.c变成libcalculator.dll，
#  test_interfaces.py直接使用这个成果
#  lib是仓库，test_interfaces.py是取货人

"""
PowerShell

cd calculator_tests
.\test_Interface.py
"""

import ctypes   # 让Python能调用C语言的桥梁
import os
import sys

from test_version import get_test_version, sync_with_c_version

# 根据平台选择库文件
if sys.platform == "win32":
    lib_name = "libcalculator.dll"
else:
    lib_name = "libcalculator.so"

# 拼出库文件的完整路径
"""
__file__：当前文件位置
../lib：上级目录的lib文件夹
最终路径如：E:/.../calculator_tests/../lib/libcalculator.dll
"""
lib_path = os.path.join(os.path.dirname(__file__), '../lib', lib_name)
print(f"加载库：{lib_path}")


# 尝试加载C库，失败就退出
try:
    lib = ctypes.CDLL(lib_path)
    print("✅ 库加载成功")
except Exception as e:
    print(f"❌ 库加载失败: {e}")

    # 在 Windows 上，尝试直接加载 DLL（不使用路径）
    if sys.platform == "win32":
        try:
            lib = ctypes.CDLL("./libcalculator.dll")
            print("✅ 库加载成功（直接加载）")
        except Exception as e2:
            print(f"❌ 直接加载也失败: {e2}")
            sys.exit(1)
    else:
        sys.exit(1)

# 定义函数原型
"""
argtypes：函数参数类型（两个整数）
restype：返回值类型（整数）
"""
# 告诉Python："add函数需要两个整数参数"
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
# 告诉Python："add函数会返回一个整数"
lib.add.restype = ctypes.c_int

lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
lib.subtract.restype = ctypes.c_int

lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
lib.multiply.restype = ctypes.c_int

lib.divide.argtypes = [ctypes.c_int, ctypes.c_int]
lib.divide.restype = ctypes.c_double

lib.square.argtypes = [ctypes.c_int]
lib.square.restype = ctypes.c_int


lib.cube.argtypes = [ctypes.c_int]
lib.cube.restype = ctypes.c_int

lib.sqrt.argtypes = [ctypes.c_double]
lib.sqrt.restype = ctypes.c_double


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


# 添加测试函数：
def test_cube():
    """测试立方接口"""
    print("🧪 测试立方接口...")
    result = lib.cube(3)
    assert result == 27, f"立方测试失败: 3³ = {result}, 期望 27"
    print("✅ 立方接口测试通过：3³ = 27")

    result2 = lib.cube(4)
    assert result2 == 64, f"立方测试失败: 4³ = {result2}, 期望 64"
    print("✅ 立方接口测试通过：4³ = 64")


def test_sqrt():
    """测试平方根接口"""
    print("🧪 测试平方根接口...")
    result = lib.sqrt(9.0)
    assert abs(result - 3.0) < 0.0001, f"平方根测试失败: √9 = {result}, 期望 3.0"
    print("✅ 平方根接口测试通过：√9 = 3.0")

    result2 = lib.sqrt(2.0)
    expected = 1.4142
    assert abs(result2 - expected) < 0.0001, f"平方根测试失败: √2 = {result2}, 期望 {expected}"
    print("✅ 平方根接口测试通过：√2 ≈ 1.4142")

    # 测试负数
    result3 = lib.sqrt(-1.0)
    assert result3 == -1.0, f"平方根测试失败: √(-1) = {result3}, 期望 -1.0"
    print("✅ 平方根接口测试通过：√(-1) = -1.0 (错误处理)")


def test_power():
    """测试幂运算接口"""
    print("🧪 测试幂运算接口...")

    # 设置函数原型
    lib.power.argtypes = [ctypes.c_double, ctypes.c_double]
    lib.power.restype = ctypes.c_double

    # 测试用例
    test_cases = [
        (2.0, 3.0, 8.0, "2的3次方"),
        (2.0, 0.0, 1.0, "任何数的0次方"),
        (5.0, -1.0, 0.2, "正数的负指数"),
        (0.0, 5.0, 0.0, "0的正数次方"),
        (1.0, 100.0, 1.0, "1的任何次方"),
        (4.0, 0.5, 2.0, "平方根"),
        (8.0, 1.0 / 3.0, 2.0, "立方根"),
        (-2.0, 3.0, -8.0, "负底数的奇数次方"),
        (-2.0, 2.0, 4.0, "负底数的偶数次方"),
    ]

    all_passed = True
    for base, exp, expected, description in test_cases:
        result = lib.power(base, exp)

        # 浮点数比较使用容差
        if abs(result - expected) < 0.0001:
            print(f"  ✅ {description}: {base}^{exp} = {result}")
        else:
            print(f"  ❌ {description}: {base}^{exp} = {result}, 期望 {expected}")
            all_passed = False

    # 测试错误情况
    error_cases = [
        (0.0, -2.0, "0的负数次方"),
        (-4.0, 0.5, "负底数的小数次方"),
    ]

    for base, exp, description in error_cases:
        result = lib.power(base, exp)
        print(f"  🔶 错误处理测试 {description}: 结果 = {result}")

    if all_passed:
        print("✅ 幂运算接口测试通过")
    else:
        print("❌ 幂运算接口测试失败")

    return all_passed


def run_all_tests():
    """运行所有接口测试"""
    print(f"\n🧪 计算器测试套件 v{get_test_version()}")
    sync_with_c_version(lib)
    print("=" * 50)

    tests = [
        test_add,
        test_subtract,
        test_multiply,
        test_divide,
        test_square,
        test_cube,    # 新增
        test_sqrt,    # 新增
        test_power    # 20251031新增
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
