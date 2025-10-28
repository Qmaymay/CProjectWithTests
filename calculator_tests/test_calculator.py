import ctypes
import os

# 加载共享库
lib_path = os.path.join(os.path.dirname(__file__), '../lib/libcalculator.so')
print(f"加载库：{lib_path}")

try:
    lib = ctypes.CDLL(lib_path)
except Exception as e:
    print(f"库加载失败: {e}")
    exit(1)

# 定义函数原型
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
lib.subtract.restype = ctypes.c_int

lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
lib.multiply.restype = ctypes.c_int

lib.divide.argtypes = [ctypes.c_int, ctypes.c_int]
lib.divide.restype = ctypes.c_double

lib.square.argtypes = [ctypes.c_int]
lib.square.restype = ctypes.c_int


def run_tests():
    """运行所有计算器测试"""
    print("运行计算器测试...")

    # 测试加法
    result = lib.add(10, 5)
    assert result == 15, f"加法测试失败: 10 + 5 = {result}"
    print(f"加法测试通过：10 + 5 = {result}")

    # 测试减法
    result = lib.subtract(10, 5)
    assert result == 5, f"减法测试失败: 10 - 5 = {result}"
    print(f"减法测试通过：10 - 5 = {result}")

    # 测试乘法
    result = lib.multiply(10, 5)
    assert result == 50, f"乘法测试失败: 10 * 5 = {result}"
    print(f"乘法测试通过：10 * 5 = {result}")

    # 测试除法
    result = lib.divide(10, 5)
    assert result == 2.0, f"除法测试失败: 10 / 5 = {result}"
    print(f"除法测试通过：10 / 5 = {result}")

    # 测试平方
    result = lib.square(5)
    assert result == 25, f"平方测试失败: 5² = {result}"
    print(f"平方测试通过：5² = {result}")

    print("所有测试通过！")


if __name__ == "__main__":
    run_tests()