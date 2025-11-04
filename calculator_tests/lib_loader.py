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

    if sys.platform == 'win32':
        # Windows: 直接使用构建目录中的文件
        possible_paths = [
            # MinGW 构建的文件
            os.path.join(os.path.dirname(__file__), '../calculator/build_mingw/calculator.dll'),
            os.path.join(os.path.dirname(__file__), '../calculator/build_mingw/libcalculator.dll'),
            # MSVC 构建的文件
            os.path.join(os.path.dirname(__file__), '../calculator/build_msvc/Release/calculator.dll'),
            os.path.join(os.path.dirname(__file__), '../calculator/build_msvc/Release/libcalculator.dll'),
            # 兼容旧路径
            os.path.join(os.path.dirname(__file__), '../lib/calculator.dll'),
        ]
    else:
        # Linux: 直接使用构建目录中的文件
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '../calculator/build/libcalculator.so'),
            os.path.join(os.path.dirname(__file__), '../calculator/build/calculator.so'),
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
