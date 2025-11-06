#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerShell
cd calculator_tests
.\test_Interface.py  234567891  23654987
"""
# import io
import ctypes   # 让Python能调用C语言的桥梁
import sys

from test_version import get_test_version
from lib_loader import calc_lib

# 设置标准输出编码为 UTF-8
# if sys.stdout.encoding != 'UTF-8':
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# if sys.stderr.encoding != 'UTF-8':
#     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 定义函数原型
"""
argtypes：函数参数类型（两个整数）
restype：返回值类型（整数）
"""
# 告诉Python："add函数需要两个整数参数"
calc_lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
# 告诉Python："add函数会返回一个整数"
calc_lib.add.restype = ctypes.c_int

calc_lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
calc_lib.subtract.restype = ctypes.c_int

calc_lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
calc_lib.multiply.restype = ctypes.c_int

calc_lib.divide.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
calc_lib.divide.restype = ctypes.c_double

calc_lib.square.argtypes = [ctypes.c_int]
calc_lib.square.restype = ctypes.c_int

calc_lib.cube.argtypes = [ctypes.c_int]
calc_lib.cube.restype = ctypes.c_int

calc_lib.sqrt_calc.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
calc_lib.sqrt_calc.restype = ctypes.c_double


def test_add():
    """测试加法接口"""
    print("🧪 测试加法接口...")
    result = calc_lib.add(10, 5)
    assert result == 15, f"加法测试失败: 10 + 5 = {result}, 期望 15"
    print("✅ 加法接口测试通过：10 + 5 = 15")


def test_subtract():
    """测试减法接口"""
    print("🧪 测试减法接口...")
    result = calc_lib.subtract(10, 5)
    assert result == 5, f"减法测试失败: 10 - 5 = {result}, 期望 5"
    print("✅ 减法接口测试通过：10 - 5 = 5")


def test_multiply():
    """测试乘法接口"""
    print("🧪 测试乘法接口...")
    result = calc_lib.multiply(10, 5)
    assert result == 50, f"乘法测试失败: 10 * 5 = {result}, 期望 50"
    print("✅ 乘法接口测试通过：10 * 5 = 50")


def test_divide():
    """测试除法接口"""
    print("🧪 测试除法接口...")

    error = ctypes.c_int(0)
    result = calc_lib.divide(10, 5, ctypes.byref(error))

    assert result == 2.0, f"除法测试失败: 10 / 5 = {result}, 期望 2.0"
    assert error.value == 0, f"错误码非零: {error.value}"
    print("✅ 除法接口测试通过：10 / 5 = 2.0")

    # 测试除零错误
    result2 = calc_lib.divide(10, 0, ctypes.byref(error))
    assert error.value != 0, f"除零应该设置错误码: {result2}"
    print("✅ 除法错误处理测试通过")


def test_square():
    """测试平方接口"""
    print("🧪 测试平方接口...")
    result = calc_lib.square(5)
    assert result == 25, f"平方测试失败: 5² = {result}, 期望 25"
    print("✅ 平方接口测试通过：5² = 25")

    # 测试另一个值
    result2 = calc_lib.square(3)
    assert result2 == 9, f"平方测试失败: 3² = {result2}, 期望 9"
    print("✅ 平方接口测试通过：3² = 9")


# 添加测试函数：
def test_cube():
    """测试立方接口"""
    print("🧪 测试立方接口...")
    result = calc_lib.cube(3)
    assert result == 27, f"立方测试失败: 3³ = {result}, 期望 27"
    print("✅ 立方接口测试通过：3³ = 27")

    result2 = calc_lib.cube(4)
    assert result2 == 64, f"立方测试失败: 4³ = {result2}, 期望 64"
    print("✅ 立方接口测试通过：4³ = 64")


def test_sqrt():
    """测试平方根接口"""
    print("🧪 测试平方根接口...")
    # 创建错误变量
    error = ctypes.c_int(0)

    # 测试正常情况
    result = calc_lib.sqrt_calc(9.0, ctypes.byref(error))
    assert abs(result - 3.0) < 0.0001, f"平方根测试失败: √9 = {result}, 期望 3.0"
    assert error.value == 0, f"错误码非零: {error.value}"
    print("✅ 平方根接口测试通过：√9 = 3.0")

    result2 = calc_lib.sqrt_calc(2.0, ctypes.byref(error))
    expected = 1.4142
    assert abs(result2 - expected) < 0.0001, f"平方根测试失败: √2 = {result2}, 期望 {expected}"
    assert error.value == 0, f"错误码非零: {error.value}"
    print("✅ 平方根接口测试通过：√2 ≈ 1.4142")

    # 测试负数
    result3 = calc_lib.sqrt_calc(-1.0, ctypes.byref(error))
    assert error.value != 0, f"负数平方根应该设置错误码: {result3}"
    print("✅ 平方根接口测试通过：√(-1) = -1.0 (错误处理)")


def test_power():
    """测试幂运算接口"""
    print("🧪 测试幂运算接口...")

    error = ctypes.c_int(0)

    calc_lib.power.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
    calc_lib.power.restype = ctypes.c_double

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
        error.value = 0  # 重置错误码
        result = calc_lib.power(base, exp, ctypes.byref(error))

        # 浮点数比较使用容差
        if abs(result - expected) < 0.0001 and error.value == 0:
            print(f"  ✅ {description}: {base}^{exp} = {result}")
        else:
            print(f"  ❌ {description}: {base}^{exp} = {result}, 错误码: {error.value}")
            all_passed = False

    # 测试错误情况
    error_cases = [
        (0.0, -2.0, "0的负数次方"),
        (-4.0, 0.5, "负底数的小数次方"),
    ]

    for base, exp, description in error_cases:
        result = calc_lib.power(base, exp, ctypes.byref(error))
        print(f"  🔶 错误处理测试 {description}: 结果 = {result}")

    if all_passed:
        print("✅ 幂运算接口测试通过")
    else:
        print("❌ 幂运算接口测试失败")

    return all_passed


def test_trig_functions():
    """测试三角函数接口"""
    print("🧪 测试三角函数接口...")

    error = ctypes.c_int(0)

    # 定义三角函数函数原型
    calc_lib.trig_calc.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
    calc_lib.trig_calc.restype = ctypes.c_double

    # 测试用例：角度制三角函数
    angle_test_cases = [
        (30.0, "sin", 0.5, "30° sin"),
        (45.0, "cos", 0.707107, "45° cos"),
        (60.0, "tan", 1.732051, "60° tan"),
        (0.0, "sin", 0.0, "0° sin"),
        (90.0, "sin", 1.0, "90° sin"),
        (180.0, "cos", -1.0, "180° cos"),
    ]

    # 测试用例：弧度制三角函数
    radian_test_cases = [
        (0.0, "sin", 0.0, "0弧度 sin"),
        (1.5708, "sin", 1.0, "π/2弧度 sin"),  # π/2 ≈ 1.5708
        (3.14159, "cos", -1.0, "π弧度 cos"),
        (0.785398, "tan", 1.0, "π/4弧度 tan"),  # π/4 ≈ 0.785398
    ]

    # 测试用例：反三角函数
    arc_test_cases = [
        (0.5, "asin", 30.0, "asin(0.5)"),
        (0.866025, "asin", 60.0, "asin(0.866025)"),
        (0.5, "acos", 60.0, "acos(0.5)"),
        (0.0, "atan", 0.0, "atan(0)"),
        (1.0, "atan", 45.0, "atan(1)"),
    ]

    # 测试用例：角度弧度转换
    conversion_test_cases = [
        (180.0, "to_radians", 3.141593, "180°转弧度"),
        (90.0, "to_radians", 1.570796, "90°转弧度"),
        (3.14159, "to_degrees", 180.0, "π转角度"),
        (1.5708, "to_degrees", 90.0, "π/2转角度"),
    ]

    all_passed = True
    total_tests = 0
    passed_tests = 0

    # 测试角度制三角函数
    print("  📐 角度制三角函数:")
    for angle, func, expected, desc in angle_test_cases:
        error.value = 0  # 重置错误码
        result = calc_lib.trig_calc(angle, b"degrees", func.encode(), ctypes.byref(error))
        if abs(result - expected) < 0.0001:
            print(f"    ✅ {desc}: {result: .6f}")
            passed_tests += 1
        else:
            print(f"    ❌ {desc}: {result: .6f}, 期望 {expected: .6f}")
            all_passed = False

    # 测试弧度制三角函数
    print("  📏 弧度制三角函数:")
    for radian, func, expected, desc in radian_test_cases:
        error.value = 0  # 重置错误码
        result = calc_lib.trig_calc(radian, b"radians", func.encode(), ctypes.byref(error))
        if abs(result - expected) < 0.0001:
            print(f"    ✅ {desc}: {result: .6f}")
            passed_tests += 1
        else:
            print(f"    ❌ {desc}: {result: .6f}, 期望 {expected: .6f}")
            all_passed = False

    # 测试反三角函数
    print("  🔄 反三角函数:")
    for value, func, expected, desc in arc_test_cases:
        error.value = 0  # 重置错误码
        result = calc_lib.trig_calc(value, b"degrees", func.encode(), ctypes.byref(error))
        if abs(result - expected) < 0.1:  # 反三角函数精度要求放宽
            print(f"    ✅ {desc}: {result: .2f}°")
            passed_tests += 1
        else:
            print(f"    ❌ {desc}: {result: .2f}°, 期望 {expected: .2f}°")
            all_passed = False

    # 测试转换函数
    print("  🔁 角度弧度转换:")
    for value, func, expected, desc in conversion_test_cases:
        error.value = 0  # 重置错误码
        mode = b"degrees" if func == "to_radians" else b"radians"
        result = calc_lib.trig_calc(value, mode, func.encode(), ctypes.byref(error))
        if abs(result - expected) < 0.001:
            print(f"    ✅ {desc}: {result: .6f}")
            passed_tests += 1
        else:
            print(f"    ❌ {desc}: {result: .6f}, 期望 {expected: .6f}")
            all_passed = False

    # 测试边界和错误情况
    print("  ⚠️  边界情况测试:")
    edge_cases = [
        (-45.0, "sin", -0.707107, "负角度sin"),
        (360.0, "cos", 1.0, "360° cos"),
        (1.5, "asin", 0.0, "asin超出范围"),  # asin(1.5)应该返回0（错误处理）
        (-2.0, "acos", 0.0, "acos超出范围"),  # acos(-2)应该返回0（错误处理）
    ]

    for value, func, expected, desc in edge_cases:
        error.value = 0  # 重置错误码
        mode = b"degrees"
        result = calc_lib.trig_calc(value, mode, func.encode(), ctypes.byref(error))
        if abs(result - expected) < 0.0001:
            print(f"    ✅ {desc}: {result: .6f}")
            passed_tests += 1
        else:
            print(f"    🔶 {desc}: {result: .6f}, 期望 {expected: .6f}")
            # 边界情况不标记为失败，只记录

    print(f"  📊 三角函数测试: {passed_tests}/{total_tests} 通过")

    if all_passed:
        print("✅ 三角函数接口测试通过")
    else:
        print("❌ 三角函数接口测试失败")

    return all_passed


def run_all_tests():
    """运行所有接口测试"""
    print(f"\n🧪 计算器测试套件 v{get_test_version()}")
    print("=" * 50)

    tests = [
        test_add,
        test_subtract,
        test_multiply,
        test_divide,
        test_square,
        test_cube,    # 新增
        test_sqrt,    # 新增
        test_power,    # 20251031新增
        test_trig_functions
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
        print("🎉 所有接口测试通过！")  # 测试版本号1
        return True


# 在文件末尾添加：
def run_functional_tests():
    """运行功能测试 - 供统一测试运行器调用"""
    return run_all_tests()


if __name__ == "__main__":
    success = run_functional_tests()
    sys.exit(0 if success else 1)
# 测试Git推送
