#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算器安全测试 - 边界值、溢出、异常输入测试
"""

import ctypes
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib_loader import library_files, get_lib_dir
from test_interfaces import setup_library_functions, CalcErrorCode


def test_arithmetic_overflow(lib):
    """测试算术运算溢出"""
    print("🧪 算术运算溢出测试")

    max_int = 2 ** 31 - 1
    min_int = -2 ** 31

    cases = [
        (max_int, 1, "整数加法边界"),
        (min_int, -1, "整数减法边界"),
        (max_int, 2, "整数乘法边界"),
    ]

    for a, b, desc in cases:
        try:
            result = lib.add(a, b)
            print(f"  ✅ {desc}: {a} + {b} = {result} (C语言正常整数环绕)")
        except Exception as e:
            print(f"  ❌ {desc}: 异常 {e}")
            return False
    return True


def test_division_edge_cases(lib):
    """测试除法边界情况"""
    print("🧪 除法边界测试")

    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)

    # 除零测试
    lib.divide(1, 0, ctypes.byref(error))
    if error.value == CalcErrorCode.CALC_SUCCESS:
        print("  ❌ 除零错误未正确捕获")
        return False
    print("  ✅ 除零错误正确处理")

    # 正常除法测试
    cases = [(1, 1), (-1, 1), (0, 1)]
    for a, b in cases:
        error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
        result = lib.divide(a, b, ctypes.byref(error))
        if error.value != CalcErrorCode.CALC_SUCCESS or abs(result - (a / b)) >= 0.001:
            print(f"  ❌ {a}/{b}: 错误码 {error.value}, 结果 {result}")
            return False
        print(f"  ✅ {a}/{b} = {result}")

    return True


def test_power_edge_cases(lib):
    """测试幂运算边界情况"""
    print("🧪 幂运算边界测试")

    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    cases = [
        (0.0, -1.0, "0的负指数", True),
        (-1.0, 0.5, "负底数分数指数", True),
        (2.0, 3.0, "正常幂运算", False),
        (1.0, 1000.0, "大指数", False),
    ]

    for base, exp, desc, should_fail in cases:
        error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
        result = lib.power(base, exp, ctypes.byref(error))

        if should_fail:
            if error.value == CalcErrorCode.CALC_SUCCESS:
                print(f"  ❌ {desc}: 应该报错但未报错")
                return False
            print(f"  ✅ {desc}: 正确返回错误码 {error.value}")
        else:
            if error.value != CalcErrorCode.CALC_SUCCESS or result <= 0:
                print(f"  ❌ {desc}: 错误码 {error.value}, 结果 {result}")
                return False
            print(f"  ✅ {desc}: 结果正常")

    return True


def test_sqrt_edge_cases(lib):
    """测试平方根边界情况"""
    print("🧪 平方根边界测试")

    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
    cases = [
        (-1.0, "负数平方根", True),
        (0.0, "零", False),
        (4.0, "正数平方根", False),
        (1e-10, "极小正数", False),
    ]

    for value, desc, should_fail in cases:
        error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
        result = lib.sqrt_calc(value, ctypes.byref(error))

        if should_fail:
            if error.value == CalcErrorCode.CALC_SUCCESS:
                print(f"  ❌ {desc}: 应该报错但未报错")
                return False
            print(f"  ✅ {desc}: 正确返回错误码 {error.value}")
        else:
            if error.value != CalcErrorCode.CALC_SUCCESS or result < 0:
                print(f"  ❌ {desc}: 错误码 {error.value}, 结果 {result}")
                return False
            print(f"  ✅ {desc}: 结果正常")

    return True


def test_library_security(lib, lib_name):
    """测试单个库的安全功能"""
    print(f"🔒 测试 {lib_name}")

    tests = [
        ("算术溢出", test_arithmetic_overflow),
        ("除法边界", test_division_edge_cases),
        ("幂运算边界", test_power_edge_cases),
        ("平方根边界", test_sqrt_edge_cases)
    ]

    passed = 0
    for name, test in tests:
        try:
            if test(lib):
                print(f"  ✅ {name}")
                passed += 1
            else:
                print(f"  ❌ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")

    print(f"  📊 {passed}/{len(tests)} 通过")
    return passed == len(tests), passed, len(tests)


def run_all_security_tests():
    """运行所有安全测试"""
    print("🔒 计算器安全测试套件")
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
            success, passed, total = test_library_security(lib, lib_file)
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
    print(f"🔒 安全测试通过: {total_passed}/{total_tests}")

    all_success = success_count == len(results)
    print("🎉 所有安全测试通过！" if all_success else "💥 安全测试失败")
    return all_success


if __name__ == "__main__":
    success = run_all_security_tests()
    sys.exit(0 if success else 1)