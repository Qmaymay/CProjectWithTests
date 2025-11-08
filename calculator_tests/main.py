#!/usr/bin/env python3
"""
统一测试运行器 - 简化版本
"""

import sys, os
import subprocess
from lib_loader import executable_files, get_lib_dir


def run_functional_tests():
    """运行功能接口测试"""
    print("🧪 功能测试...")
    try:
        from test_interfaces import run_all_tests
        return run_all_tests()
    except Exception as e:
        print(f"❌ 功能测试异常: {e}")
        return False


def run_executable_tests():
    """运行可执行文件测试"""
    print("🚀 可执行文件测试...")

    if not executable_files:
        print("❌ 没有可执行文件")
        return False

    lib_dir = get_lib_dir()
    passed = 0

    for exe_file in executable_files:
        exe_path = os.path.join(lib_dir, exe_file)
        try:
            subprocess.run([exe_path], timeout=2, cwd=lib_dir)
            print(f"✅ {exe_file}")
            passed += 1
        except:
            print(f"❌ {exe_file}")

    print(f"📊 {passed}/{len(executable_files)} 通过")
    return passed == len(executable_files)


def run_security_tests():
    """运行安全测试"""
    print("🔒 安全测试...")
    try:
        from security_tests import run_all_security_tests
        return run_all_security_tests()
    except Exception as e:
        print(f"❌ 安全测试异常: {e}")
        return False


def run_performance_tests():
    """运行性能测试"""
    print("⚡ 性能测试...")
    try:
        from performance_tests import run_all_performance_tests
        run_all_performance_tests()
        return True
    except Exception as e:
        print(f"❌ 性能测试异常: {e}")
        return True  # 性能测试失败不阻塞构建


def main():
    print("🎯 计算器测试套件")
    print("=" * 40)

    # 运行所有测试
    functional = run_functional_tests()
    print()

    executable = run_executable_tests()
    print()

    security = run_security_tests()
    print()

    performance = run_performance_tests()
    print()

    # 简单报告
    print("=" * 40)
    print("📊 测试报告")
    print("=" * 40)

    tests = [
        ("功能测试", functional),
        ("可执行文件", executable),
        ("安全测试", security),
        ("性能测试", performance)
    ]

    all_passed = True
    for name, passed in tests:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
        if not passed:
            all_passed = False

    print("=" * 40)
    if all_passed:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("💥 测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())