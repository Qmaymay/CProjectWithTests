import os, sys, ctypes

# TODO CMakeLists.txt告诉编译器如何把calculator.c变成.dll文件
#  MSVC默认生成动态库calculator.dll和导入库calculator.lib    # ；
#  MinGW默认生成动态库libcalculator.dll(前面加了个lib)和静态库libcalculator.a
#  当然，我们这里只要.dll文件，lib_loader.py负责将路径取出来给test_interfaces.py用

import ctypes
import os
import sys


def load_calculator_lib():
    """智能加载库 - 支持所有平台"""
    print("=== lib_loader.py 调试信息 ===", flush=True)
    print(f"平台: {sys.platform}", flush=True)

    # 根据平台确定库文件位置和名称
    if sys.platform == 'win32':
        # Windows: 使用 lib 目录中的 calculator.dll
        lib_path = os.path.join(os.path.dirname(__file__), '../lib/calculator.dll')
        possible_paths = [lib_path]
    else:
        # Linux: 直接使用构建目录中的库文件
        build_path = os.path.join(os.path.dirname(__file__), '../calculator/build/libcalculator.so')
        possible_paths = [
            build_path,  # 直接使用构建目录
            os.path.join(os.path.dirname(__file__), '../lib/libcalculator.so'),
            os.path.join(os.path.dirname(__file__), '../lib/calculator.so')
        ]

    print(f"尝试的路径: {possible_paths}", flush=True)

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到库文件: {path}", flush=True)
            return ctypes.CDLL(path)

    print("❌ 所有路径都找不到库文件", flush=True)
    raise FileNotFoundError(f"找不到库文件")


calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")

calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")
