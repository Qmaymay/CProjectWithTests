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

from lib_loader import calc_lib


def setup_function_prototypes():
    """设置函数原型"""
    # 基本运算
    calc_lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
    calc_lib.add.restype = ctypes.c_int

    calc_lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
    calc_lib.multiply.restype = ctypes.c_int

    calc_lib.divide.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    calc_lib.divide.restype = ctypes.c_double

    # 高级运算
    calc_lib.power.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
    calc_lib.power.restype = ctypes.c_double

    calc_lib.sqrt_calc.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
    calc_lib.sqrt_calc.restype = ctypes.c_double


def time_function(func, *args, iterations=1000):
    """测量函数执行时间"""
    times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000000)  # 转换为微秒

    return times


def test_basic_operations_performance():
    """测试基本运算性能"""
    print("⚡ 测试基本运算性能...")

    error = ctypes.c_int(0)

    operations = [
        ("加法", calc_lib.add, (123, 456)),
        ("乘法", calc_lib.multiply, (123, 456)),
        ("除法", calc_lib.divide, (1000, 3, ctypes.byref(error))),
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
        print(f"  📊 {name}: {avg_time:.2f} ± {std_dev:.2f} μs (min: {min(times):.2f}, max: {max(times):.2f})")

    return results


def test_throughput():
    """测试吞吐量"""
    print("⚡ 测试运算吞吐量...")

    error = ctypes.c_int(0)

    # 测试连续操作的吞吐量
    operations = 10000
    start_time = time.perf_counter()

    for i in range(operations):
        # 混合操作
        if i % 4 == 0:
            calc_lib.add(i, 1)
        elif i % 4 == 1:
            calc_lib.multiply(i, 2)
        elif i % 4 == 2:
            error.value = 0
            calc_lib.divide(i + 1, 3, ctypes.byref(error))

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

    setup_function_prototypes()

    performance_results = {}

    # 运行各项测试
    performance_results['basic_ops'] = test_basic_operations_performance()
    print("")

    performance_results['throughput'] = test_throughput()
    print("")

    # 生成性能报告
    print("=" * 50)
    print("📊 性能测试报告")
    print("=" * 50)

    # 计算平均操作时间
    all_times = []
    for op_name, data in performance_results['basic_ops'].items():
        all_times.append(data['avg'])
        print(f"📈 {op_name}: {data['avg']:.2f} μs")

    if all_times:
        avg_time = statistics.mean(all_times)
        print(f"\n🎯 平均操作时间: {avg_time:.2f} μs")
        print(f"🚀 理论最大吞吐量: {1000000 / avg_time:.0f} 操作/秒")

    print(f"📈 实测吞吐量: {performance_results['throughput']:.0f} 操作/秒")

    return performance_results


if __name__ == "__main__":
    results = run_all_performance_tests()
