#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import sys
import os

from test_version import get_test_version
from lib_loader import library_files, get_lib_dir


class CalcErrorCode(ctypes.c_int):
    CALC_SUCCESS = 0
    CALC_ERROR_DIVISION_BY_ZERO = -1
    CALC_ERROR_NEGATIVE_SQRT = -2
    CALC_ERROR_INVALID_POWER = -3
    CALC_ERROR_INVALID_TRIG = -4
    CALC_ERROR_INVALID_INPUT = -5
    CALC_ERROR_TANGENT_UNDEFINED = -6


def setup_library_functions(lib):
    """为库设置函数原型 - 统一使用 CalcErrorCode"""
    lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add.restype = ctypes.c_int

    lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.subtract.restype = ctypes.c_int

    lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.multiply.restype = ctypes.c_int

    # 统一使用 CalcErrorCode
    lib.divide.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(CalcErrorCode)]
    lib.divide.restype = ctypes.c_double

    lib.square.argtypes = [ctypes.c_int]
    lib.square.restype = ctypes.c_int

    lib.cube.argtypes = [ctypes.c_int]
    lib.cube.restype = ctypes.c_int

    lib.sqrt_calc.argtypes = [ctypes.c_double, ctypes.POINTER(CalcErrorCode)]
    lib.sqrt_calc.restype = ctypes.c_double

    lib.power.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(CalcErrorCode)]
    lib.power.restype = ctypes.c_double


def test_add(lib):
    """测试加法"""
    result = lib.add(10, 5)
    assert result == 15, f"10 + 5 = {result}"
    return "✅ 加法: 10 + 5 = 15"


def test_subtract(lib):
    """测试减法"""
    result = lib.subtract(10, 5)
    assert result == 5, f"10 - 5 = {result}"
    return "✅ 减法: 10 - 5 = 5"


def test_multiply(lib):
    """测试乘法"""
    result = lib.multiply(10, 5)
    assert result == 50, f"10 * 5 = {result}"
    return "✅ 乘法: 10 * 5 = 50"


def test_divide(lib):
    """测试除法"""
    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    result = lib.divide(10, 5, ctypes.byref(error))
    assert result == 2.0, f"10 / 5 = {result}"
    assert error.value == CalcErrorCode.CALC_SUCCESS, f"错误码: {error.value}"
    return "✅ 除法: 10 / 5 = 2.0"


def test_divide_error(lib):
    """测试除法错误处理"""
    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    result = lib.divide(10, 0, ctypes.byref(error))
    assert error.value == CalcErrorCode.CALC_ERROR_DIVISION_BY_ZERO, f"除零错误码应该是 {CalcErrorCode.CALC_ERROR_DIVISION_BY_ZERO}, 实际是 {error.value}"
    return "✅ 除法错误处理"


def test_square(lib):
    """测试平方"""
    result = lib.square(5)
    assert result == 25, f"5² = {result}"
    return "✅ 平方: 5² = 25"


def test_cube(lib):
    """测试立方"""
    result = lib.cube(3)
    assert result == 27, f"3³ = {result}"
    return "✅ 立方: 3³ = 27"


def test_sqrt(lib):
    """测试平方根"""
    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    result = lib.sqrt_calc(9.0, ctypes.byref(error))
    assert abs(result - 3.0) < 0.0001, f"√9 = {result}"
    assert error.value == CalcErrorCode.CALC_SUCCESS, f"错误码: {error.value}"
    return "✅ 平方根: √9 = 3.0"


def test_sqrt_error(lib):
    """测试平方根错误处理"""
    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    result = lib.sqrt_calc(-1.0, ctypes.byref(error))
    assert error.value == CalcErrorCode.CALC_ERROR_NEGATIVE_SQRT, f"负数平方根错误码应该是 {CalcErrorCode.CALC_ERROR_NEGATIVE_SQRT}, 实际是 {error.value}"
    return "✅ 平方根错误处理"


def test_library(lib, lib_name):
    """测试单个库"""
    print(f"🧪 测试 {lib_name}")

    tests = [test_add, test_subtract, test_multiply, test_divide,
             test_divide_error, test_square, test_cube, test_sqrt, test_sqrt_error]

    passed = 0
    for test in tests:
        try:
            print(f"  {test(lib)}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")

    print(f"  📊 {passed}/{len(tests)}")
    return passed == len(tests), passed, len(tests)


def run_all_tests():
    """运行所有接口测试"""
    print(f"\n🧪 计算器测试套件 v{get_test_version()}")
    print("=" * 50)

    if not library_files:
        print("❌ 没有找到动态库")
        return False

    print(f"测试 {len(library_files)} 个编译器版本: {', '.join(library_files)}")

    # 测试每个库
    results = []
    for lib_file in library_files:
        try:
            lib = ctypes.CDLL(os.path.join(get_lib_dir(), lib_file))
            setup_library_functions(lib)
            success, passed, total = test_library(lib, lib_file)
            results.append((lib_file, success, passed, total))
        except Exception as e:
            print(f"❌ {lib_file}: {e}")
            results.append((lib_file, False, 0, 0))

    # 输出结果
    print("\n" + "=" * 50)
    total_passed = sum(passed for _, _, passed, _ in results)
    total_tests = sum(total for _, _, _, total in results)

    for lib_file, success, passed, total in results:
        status = "✅" if success else "❌"
        print(f"{status} {lib_file}: {passed}/{total}")

    success_count = sum(1 for _, success, _, _ in results if success)
    print(f"\n🎯 编译器通过: {success_count}/{len(results)}")
    print(f"🧪 功能测试通过: {total_passed}/{total_tests}")

    all_success = success_count == len(results)
    print("🎉 所有测试通过！" if all_success else "💥 测试失败")
    return all_success


if __name__ == "__main__":
    success= run_all_tests()
    sys.exit(0 if success else 1)