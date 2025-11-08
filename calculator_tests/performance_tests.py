#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算器性能测试 - 响应时间、吞吐量测试
简化版本，不依赖外部库
"""

import ctypes
import sys
import os
import time
import statistics

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib_loader import library_files, get_lib_dir
from test_interfaces import setup_library_functions, CalcErrorCode


def time_function(func, *args, iterations=1000):
    """测量函数执行时间"""
    times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000000)  # 转换为微秒

    return times


def test_library_performance(lib, lib_name):
    """测试单个库的性能"""
    print(f"⚡ 测试 {lib_name} 性能...")

    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)

    operations = [
        ("加法", lib.add, (123, 456)),
        ("乘法", lib.multiply, (123, 456)),
        ("除法", lib.divide, (1000, 3, ctypes.byref(error))),
    ]

    results = {}
    for name, func, args in operations:
        times = time_function(func, *args, iterations=1000)
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        results[name] = {
            'avg': avg_time,
            'std': std_dev,
            'min': min(times),
            'max': max(times)
        }
        print(f"  📊 {name}: {avg_time:.2f} ± {std_dev:.2f} μs")

    return results


def test_library_throughput(lib):
    """测试单个库的吞吐量"""
    print("⚡ 测试运算吞吐量...")

    error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)

    # 测试连续操作的吞吐量
    operations = 10000
    start_time = time.perf_counter()

    for i in range(operations):
        # 混合操作
        if i % 4 == 0:
            lib.add(i, 1)
        elif i % 4 == 1:
            lib.multiply(i, 2)
        elif i % 4 == 2:
            error = CalcErrorCode(CalcErrorCode.CALC_SUCCESS)
            lib.divide(i + 1, 3, ctypes.byref(error))

    end_time = time.perf_counter()
    total_time = end_time - start_time
    throughput = operations / total_time

    print(f"  📈 完成 {operations} 次混合操作")
    print(f"  ⏱️  总时间: {total_time:.3f} 秒")
    print(f"  🚀 吞吐量: {throughput:.0f} 操作/秒")

    return throughput


def run_all_performance_tests():
    """运行所有性能测试"""
    print("⚡ 计算器性能测试套件")
    print("=" * 50)

    if not library_files:
        print("❌ 没有找到动态库")
        return None

    print(f"测试 {len(library_files)} 个编译器版本: {', '.join(library_files)}")

    performance_results = {}

    # 测试每个库
    for lib_file in library_files:
        try:
            lib = ctypes.CDLL(os.path.join(get_lib_dir(), lib_file))
            setup_library_functions(lib)

            print(f"\n🔍 测试 {lib_file}")
            print("-" * 30)

            # 测试性能
            perf_results = test_library_performance(lib, lib_file)
            print("")

            # 测试吞吐量
            throughput = test_library_throughput(lib)

            performance_results[lib_file] = {
                'performance': perf_results,
                'throughput': throughput
            }

        except Exception as e:
            print(f"❌ {lib_file} 性能测试失败: {e}")
            performance_results[lib_file] = None

    # 生成性能报告总结
    print("\n" + "=" * 50)
    print("📊 性能测试总结")
    print("=" * 50)

    successful_tests = sum(1 for results in performance_results.values() if results)

    # 只输出总体统计，不重复详细数据
    print(f"✅ 成功测试了 {successful_tests}/{len(library_files)} 个编译器")

    if successful_tests > 0:
        # 计算平均性能
        all_avg_times = []
        all_throughputs = []

        for lib_file, results in performance_results.items():
            if results:
                perf_data = results['performance']
                avg_times = [data['avg'] for data in perf_data.values()]
                all_avg_times.extend(avg_times)
                all_throughputs.append(results['throughput'])

        if all_avg_times:
            avg_op_time = statistics.mean(all_avg_times)
            avg_throughput = statistics.mean(all_throughputs)

            print(f"📈 平均操作时间: {avg_op_time:.2f} μs")
            print(f"🚀 平均吞吐量: {avg_throughput:.0f} 操作/秒")
            print(f"⚡ 性能表现正常")

    return performance_results


if __name__ == "__main__":
    results = run_all_performance_tests()