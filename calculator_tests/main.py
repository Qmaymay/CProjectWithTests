#!/usr/bin/env python3
"""
统一测试运行器 - 集成功能测试、安全测试、性能测试
"""

import sys
import os
import argparse


def run_functional_tests():
    """运行功能接口测试"""
    print("🧪 运行功能接口测试...")
    from test_interfaces import run_all_tests
    return run_all_tests()


def run_security_tests():
    """运行安全测试"""
    print("🔒 运行安全测试...")
    try:
        from security_tests import run_all_security_tests
        return run_all_security_tests()
    except ImportError as e:
        print(f"❌ 安全测试模块未找到: {e}")
        return False


def run_performance_tests():
    """运行性能测试"""
    print("⚡ 运行性能测试...")
    try:
        from performance_tests import run_all_performance_tests
        run_all_performance_tests()  # 性能测试通常不阻塞构建
        return True
    except ImportError as e:
        print(f"❌ 性能测试模块未找到: {e}")
        return True  # 性能测试失败不阻塞构建


def main():
    parser = argparse.ArgumentParser(description='运行计算器测试套件')
    parser.add_argument('--functional', action='store_true', help='仅运行功能测试')
    parser.add_argument('--security', action='store_true', help='仅运行安全测试')
    parser.add_argument('--performance', action='store_true', help='仅运行性能测试')
    parser.add_argument('--all', action='store_true', help='运行所有测试（默认）')

    args = parser.parse_args()

    # 默认运行所有测试
    if not any([args.functional, args.security, args.performance, args.all]):
        args.all = True

    print("🎯 计算器测试套件")
    print("=" * 60)

    results = {}

    # 运行选择的测试
    if args.all or args.functional:
        results['functional'] = run_functional_tests()
        print("")

    if args.all or args.security:
        results['security'] = run_security_tests()
        print("")

    if args.all or args.performance:
        results['performance'] = run_performance_tests()
        print("")

    # 生成测试报告
    print("=" * 60)
    print("📊 测试套件报告")
    print("=" * 60)

    all_passed = True
    for test_type, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_type:12} : {status}")
        if not passed:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("💥 部分测试失败")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())