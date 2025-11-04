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
    # 强制刷新输出缓冲区
    sys.stdout.flush()
    sys.stderr.flush()

    lib_dir = os.path.join(os.path.dirname(__file__), '../lib')

    # 扩展搜索范围
    if sys.platform == 'win32':
        possible_names = ['calculator.dll', 'libcalculator.dll']
    else:
        possible_names = ['calculator.so', 'libcalculator.so', 'libcalculator.a', 'calculator.a']

    # 强制输出调试信息
    print("=== lib_loader.py 调试信息 ===", flush=True)
    print(f"平台: {sys.platform}", flush=True)
    print(f"Python版本: {sys.version}", flush=True)
    print(f"当前工作目录: {os.getcwd()}", flush=True)
    print(f"脚本位置: {__file__}", flush=True)
    print(f"搜索库目录: {lib_dir}", flush=True)
    print(f"尝试的文件名: {possible_names}", flush=True)

    # 检查目录是否存在
    if os.path.exists(lib_dir):
        print(f"✅ 库目录存在", flush=True)
        try:
            contents = os.listdir(lib_dir)
            print(f"📂 目录内容: {contents}", flush=True)
        except Exception as e:
            print(f"❌ 无法读取目录: {e}", flush=True)
    else:
        print(f"❌ 库目录不存在: {lib_dir}", flush=True)

    # 尝试在更多位置查找
    search_paths = [
        '../lib',
        './lib',
        'lib',
        '../../lib',
        '../calculator/build',
        './calculator/build',
        '../../calculator/build'
    ]

    for search_path in search_paths:
        full_path = os.path.join(os.path.dirname(__file__), search_path)
        if os.path.exists(full_path):
            print(f"🔍 搜索路径: {full_path}", flush=True)
            try:
                contents = os.listdir(full_path)
                print(f"  内容: {contents}", flush=True)
            except:
                pass
            for name in possible_names:
                path = os.path.join(full_path, name)
                if os.path.exists(path):
                    print(f"🎯 找到库文件: {path}", flush=True)
                    return ctypes.CDLL(path)

    print("❌ 所有搜索路径都找不到库文件", flush=True)
    raise FileNotFoundError(f"找不到库文件，尝试了: {possible_names}")


# 加载库
print("=== 开始加载库 ===", flush=True)
calc_lib = load_calculator_lib()
print(f"=== 库加载成功: {calc_lib} ===", flush=True)

calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")
