import ctypes
import os


# 加载C库
def load_c_library():
    # 根据你的系统调整库文件路径
    if os.name == 'nt':  # Windows
        lib_path = '../calculator/cmake-build-debug/libcalculator.dll'
    else:  # Linux/Mac
        lib_path = '../calculator/cmake-build-debug/libcalculator.so'

    # 如果上面的路径不存在，尝试其他可能的路径
    possible_paths = [
        '../calculator/cmake-build-debug/libcalculator.dll',
        '../calculator/cmake-build-debug/libcalculator.so',
        '../calculator/cmake-build-debug/libcalculator.dylib',
        '../calculator/libcalculator.dll',
        '../calculator/libcalculator.so',
        '../calculator/libcalculator.dylib'
    ]

    for path in possible_paths:
        if os.path.exists(path):
            lib_path = path
            break
    else:
        raise FileNotFoundError("找不到C库文件，请先编译C项目")

    return ctypes.CDLL(lib_path)


# 加载库
lib = load_c_library()

# 设置函数参数和返回类型
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
lib.subtract.restype = ctypes.c_int

lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
lib.multiply.restype = ctypes.c_int

lib.divide.argtypes = [ctypes.c_int, ctypes.c_int]
lib.divide.restype = ctypes.c_double


def test_add():
    result = lib.add(10, 5)
    assert result == 15, f"期望15，得到{result}"
    print("✓ 加法测试通过")


def test_subtract():
    result = lib.subtract(10, 5)
    assert result == 5, f"期望5，得到{result}"
    print("✓ 减法测试通过")


def test_multiply():
    result = lib.multiply(10, 5)
    assert result == 50, f"期望50，得到{result}"
    print("✓ 乘法测试通过")


def test_divide():
    result = lib.divide(10, 5)
    assert result == 2.0, f"期望2.0，得到{result}"
    print("✓ 除法测试通过")


if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    print("所有测试通过！🎉")