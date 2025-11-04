import os, sys, ctypes

# TODO CMakeLists.txt告诉编译器如何把calculator.c变成.dll文件
#  MSVC默认生成动态库calculator.dll和导入库calculator.lib    # ；
#  MinGW默认生成动态库libcalculator.dll(前面加了个lib)和静态库libcalculator.a
#  当然，我们这里只要.dll文件，lib_loader.py负责将路径取出来给test_interfaces.py用


def load_calculator_lib():
    """智能加载库 - 支持 MSVC 和 MinGW"""
    lib_dir = os.path.join(os.path.dirname(__file__), '../lib')
    possible_names = ['calculator.dll', 'libcalculator.dll'] if sys.platform == 'win32' else ['libcalculator.so']

    for name in possible_names:
        path = os.path.join(lib_dir, name)
        if os.path.exists(path):
            return ctypes.CDLL(path)
    raise FileNotFoundError(f"找不到库文件，尝试了: {possible_names}")


calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")
