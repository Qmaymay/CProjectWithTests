import os, sys, ctypes

# TODO CMakeLists.txt告诉编译器如何把calculator.c变成.dll文件
#  MSVC默认生成动态库calculator.dll和导入库calculator.lib    # ；
#  MinGW默认生成动态库libcalculator.dll(前面加了个lib)和静态库libcalculator.a
#  当然，我们这里只要.dll文件，lib_loader.py负责将路径取出来给test_interfaces.py用


import os, sys, ctypes


def load_calculator_lib():
    """智能加载库 - 支持所有平台"""
    print("=== lib_loader.py 调试信息 ===", flush=True)
    print(f"平台: {sys.platform}", flush=True)

    # 根据平台确定库文件位置和名称
    if sys.platform == 'win32':
        # Windows: 尝试多个可能的库文件名
        lib_dir = os.path.join(os.path.dirname(__file__), '../lib/')
        possible_paths = [
            os.path.join(lib_dir, 'calculator.dll'),  # MinGW默认
            os.path.join(lib_dir, 'calculator_msvc.dll'),  # MSVC生成
            os.path.join(lib_dir, 'libcalculator.dll'),  # 可能的其他命名
        ]
    else:
        # Linux/macOS
        lib_dir = os.path.join(os.path.dirname(__file__), '../lib/')
        possible_paths = [
            os.path.join(lib_dir, 'libcalc.so'),  # 您的CMake配置
            os.path.join(lib_dir, 'libcalculator.so'),
            os.path.join(lib_dir, 'calculator.so')
        ]

    print(f"尝试的路径: {possible_paths}", flush=True)

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到库文件: {path}", flush=True)
            return ctypes.CDLL(path)

    # 如果标准路径没找到，尝试构建目录
    fallback_paths = []
    if sys.platform == 'win32':
        fallback_paths = [
            os.path.join(os.path.dirname(__file__), '../build/lib/calculator.dll'),
            os.path.join(os.path.dirname(__file__), '../build/lib/calculator_msvc.dll'),
        ]
    else:
        fallback_paths = [
            os.path.join(os.path.dirname(__file__), '../build/lib/libcalc.so'),
        ]

    for path in fallback_paths:
        if os.path.exists(path):
            print(f"✅ 在构建目录找到库文件: {path}", flush=True)
            return ctypes.CDLL(path)

    print("❌ 所有路径都找不到库文件", flush=True)
    print("请先运行构建脚本生成库文件", flush=True)
    raise FileNotFoundError(f"找不到库文件")


calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")

# def load_calculator_lib():
#     """智能加载库 - 支持所有平台"""
#     print("=== lib_loader.py 调试信息 ===", flush=True)
#     print(f"平台: {sys.platform}", flush=True)
#
#     # 根据平台确定库文件位置和名称
#     if sys.platform == 'win32':
#         # Windows: 使用 lib 目录中的 calculator.dll
#         lib_path = os.path.join(os.path.dirname(__file__), '../lib/calculator.dll')
#         possible_paths = [lib_path]
#     else:
#         # Linux: 直接使用构建目录中的库文件
#         build_path = os.path.join(os.path.dirname(__file__), '../calculator/build/libcalculator.so')
#         possible_paths = [
#             build_path,  # 直接使用构建目录
#             os.path.join(os.path.dirname(__file__), '../lib/libcalculator.so'),
#             os.path.join(os.path.dirname(__file__), '../lib/calculator.so')
#         ]
#
#     print(f"尝试的路径: {possible_paths}", flush=True)
#
#     for path in possible_paths:
#         if os.path.exists(path):
#             print(f"✅ 找到库文件: {path}", flush=True)
#             return ctypes.CDLL(path)
#
#     print("❌ 所有路径都找不到库文件", flush=True)
#     raise FileNotFoundError(f"找不到库文件")
#
#
# calc_lib = load_calculator_lib()
# print(f"calc_lib: {calc_lib}")
