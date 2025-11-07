#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import sys
import os

from test_version import get_test_version
from lib_loader import library_files, get_lib_dir


def setup_library_functions(lib):
    """为库设置函数原型"""
    lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add.restype = ctypes.c_int

    lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.subtract.restype = ctypes.c_int

    lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.multiply.restype = ctypes.c_int

    lib.divide.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.divide.restype = ctypes.c_double

    lib.square.argtypes = [ctypes.c_int]
    lib.square.restype = ctypes.c_int

    lib.cube.argtypes = [ctypes.c_int]
    lib.cube.restype = ctypes.c_int

    lib.sqrt_calc.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
    lib.sqrt_calc.restype = ctypes.c_double


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
    error = ctypes.c_int(0)
    result = lib.divide(10, 5, ctypes.byref(error))
    assert result == 2.0, f"10 / 5 = {result}"
    assert error.value == 0, f"错误码: {error.value}"
    return "✅ 除法: 10 / 5 = 2.0"


def test_divide_error(lib):
    """测试除法错误处理"""
    error = ctypes.c_int(0)
    result = lib.divide(10, 0, ctypes.byref(error))
    assert error.value != 0, "除零应该设置错误码"
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
    error = ctypes.c_int(0)
    result = lib.sqrt_calc(9.0, ctypes.byref(error))
    assert abs(result - 3.0) < 0.0001, f"√9 = {result}"
    assert error.value == 0, f"错误码: {error.value}"
    return "✅ 平方根: √9 = 3.0"


def test_sqrt_error(lib):
    """测试平方根错误处理"""
    error = ctypes.c_int(0)
    result = lib.sqrt_calc(-1.0, ctypes.byref(error))
    assert error.value != 0, "负数平方根应该设置错误码"
    return "✅ 平方根错误处理"


def test_library_functions(lib, lib_name):
    """测试单个库的所有函数"""
    print(f"🧪 测试 {lib_name}...")

    # 所有测试函数列表
    test_functions = [
        ("加法", test_add),
        ("减法", test_subtract),
        ("乘法", test_multiply),
        ("除法", test_divide),
        ("除法错误处理", test_divide_error),
        ("平方", test_square),
        ("立方", test_cube),
        ("平方根", test_sqrt),
        ("平方根错误处理", test_sqrt_error),
    ]

    total_tests = len(test_functions)
    passed_tests = 0
    failed_tests = []

    for test_name, test_func in test_functions:
        try:
            message = test_func(lib)
            print(f"  {message}")
            passed_tests += 1
        except Exception as e:
            print(f"  ❌ {test_name}失败: {e}")
            failed_tests.append(test_name)

    # 输出单个库的统计
    print(f"  📊 {lib_name}: {passed_tests}/{total_tests} 个功能测试通过")

    return passed_tests == total_tests, failed_tests, total_tests, passed_tests


def run_all_tests():
    """运行所有接口测试"""
    print(f"\n🧪 计算器测试套件 v{get_test_version()}")
    print("=" * 50)

    lib_dir = get_lib_dir()

    if not library_files:
        print("❌ 没有找到可用的动态库")
        return False

    print(f"找到 {len(library_files)} 个动态库: {library_files}")

    total_libs = len(library_files)
    passed_libs = 0
    overall_stats = {
        'total_tests': 0,
        'passed_tests': 0,
        'lib_results': {}
    }

    # 测试每个动态库
    for lib_file in library_files:
        lib_path = os.path.join(lib_dir, lib_file)
        try:
            lib = ctypes.CDLL(lib_path)
            setup_library_functions(lib)
            lib_passed, failed, total_tests, passed_tests = test_library_functions(lib, lib_file)

            overall_stats['lib_results'][lib_file] = {
                'passed': lib_passed,
                'failed_tests': failed,
                'total_tests': total_tests,
                'passed_tests': passed_tests
            }
            overall_stats['total_tests'] += total_tests
            overall_stats['passed_tests'] += passed_tests

            if lib_passed:
                passed_libs += 1
                print(f"✅ {lib_file}: 所有测试通过\n")
            else:
                print(f"❌ {lib_file}: 失败 ({', '.join(failed)})\n")

        except Exception as e:
            print(f"❌ {lib_file}: 加载失败 - {e}\n")
            overall_stats['lib_results'][lib_file] = {
                'passed': False,
                'failed_tests': ['库加载'],
                'total_tests': 0,
                'passed_tests': 0
            }

    # 输出详细统计
    print("=" * 50)
    print("📊 详细统计")
    print("=" * 50)

    for lib_file, results in overall_stats['lib_results'].items():
        status = "✅ 通过" if results['passed'] else "❌ 失败"
        print(f"{status} {lib_file}: {results['passed_tests']}/{results['total_tests']} 个功能测试通过")

    # 总体统计
    print("\n" + "=" * 50)
    print("🎯 总体统计")
    print("=" * 50)

    lib_success_rate = (passed_libs / total_libs) * 100
    test_success_rate = (overall_stats['passed_tests'] / overall_stats['total_tests']) * 100 if overall_stats[
                                                                                                    'total_tests'] > 0 else 0

    print(f"📚 库测试: {passed_libs}/{total_libs} 通过 ({lib_success_rate:.1f}%)")
    print(f"🧪 功能测试: {overall_stats['passed_tests']}/{overall_stats['total_tests']} 通过 ({test_success_rate:.1f}%)")
    print(f"📈 总共测试了 {overall_stats['total_tests']} 个功能函数，通过了 {overall_stats['passed_tests']} 个")

    if passed_libs == total_libs and overall_stats['passed_tests'] == overall_stats['total_tests']:
        print("🎉 所有测试通过！")
        return True
    else:
        print("💥 部分测试失败")
        return False


def run_functional_tests():
    """运行功能测试 - 供统一测试运行器调用"""
    return run_all_tests()


if __name__ == "__main__":
    success = run_functional_tests()
    sys.exit(0 if success else 1)