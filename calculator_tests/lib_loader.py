import os, sys, ctypes

# TODO CMakeLists.txt告诉编译器如何把calculator.c变成.dll文件
#  MSVC默认生成动态库calculator.dll和导入库calculator.lib    # ；
#  MinGW默认生成动态库libcalculator.dll(前面加了个lib)和静态库libcalculator.a
#  当然，我们这里只要.dll文件，lib_loader.py负责将路径取出来给test_interfaces.py用

import ctypes
import os
import sys


def load_calculator_lib():
    """Load library intelligently - support all platforms"""
    print("=== lib_loader.py Debug Info ===", flush=True)
    print(f"Platform: {sys.platform}", flush=True)

    if sys.platform == 'win32':
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '../calculator/build_mingw/calculator.dll'),
            os.path.join(os.path.dirname(__file__), '../calculator/build_msvc/Release/calculator.dll'),
            os.path.join(os.path.dirname(__file__), '../lib/calculator.dll'),
        ]
    else:
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '../calculator/build/libcalculator.so'),
            os.path.join(os.path.dirname(__file__), '../calculator/build/calculator.so'),
        ]

    print(f"Trying paths: {possible_paths}", flush=True)

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found library: {path}", flush=True)
            return ctypes.CDLL(path)

    print("❌ All paths failed to find library", flush=True)
    raise FileNotFoundError("Cannot find library file")


calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")
