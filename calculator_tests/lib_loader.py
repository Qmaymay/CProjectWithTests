import os, sys, ctypes

# TODO CMakeLists.txt告诉编译器如何把calculator.c变成.dll文件
#  MSVC默认生成动态库calculator.dll和导入库calculator.lib    # ；
#  MinGW默认生成动态库libcalculator.dll(前面加了个lib)和静态库libcalculator.a
#  当然，我们这里只要.dll文件，lib_loader.py负责将路径取出来给test_interfaces.py用


def load_calculator_lib():
    """智能加载库 - 支持所有平台"""
    lib_dir = os.path.join(os.path.dirname(__file__), '../lib')

    # 扩展搜索范围
    if sys.platform == 'win32':
        possible_names = ['calculator.dll', 'libcalculator.dll']
    else:
        possible_names = ['calculator.so', 'libcalculator.so', 'libcalculator.a', 'calculator.a']

    # 详细的调试信息
    print(f"🔍 平台: {sys.platform}")
    print(f"🔍 搜索库目录: {lib_dir}")
    print(f"🔍 尝试的文件名: {possible_names}")
    print(f"🔍 当前工作目录: {os.getcwd()}")

    # 检查目录是否存在
    if os.path.exists(lib_dir):
        print(f"✅ 库目录存在")
        print(f"📂 目录内容: {os.listdir(lib_dir)}")
    else:
        print(f"❌ 库目录不存在: {lib_dir}")

    for name in possible_names:
        path = os.path.join(lib_dir, name)
        if os.path.exists(path):
            print(f"🎯 找到库文件: {path}")
            print(f"📏 文件大小: {os.path.getsize(path)} 字节")
            return ctypes.CDLL(path)
        else:
            print(f"❌ 文件不存在: {path}")

    # 尝试在更多位置查找
    search_paths = [
        '../lib',
        './lib',
        'lib',
        '../calculator/build',
        './calculator/build'
    ]

    for search_path in search_paths:
        if os.path.exists(search_path):
            print(f"🔍 搜索路径: {search_path}")
            for name in possible_names:
                path = os.path.join(search_path, name)
                if os.path.exists(path):
                    print(f"🎯 在 {search_path} 找到: {path}")
                    return ctypes.CDLL(path)

    raise FileNotFoundError(f"找不到库文件，尝试了所有位置")


calc_lib = load_calculator_lib()
print(f"calc_lib: {calc_lib}")
