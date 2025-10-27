import ctypes
import os
import sys


def load_c_library():
    """动态加载C共享库"""
    # 添加lib目录到路径
    lib_dir = os.path.join(os.path.dirname(__file__), '..', 'lib')

    # 根据操作系统选择库文件
    if sys.platform == "win32":
        lib_name = "calculator.dll"
    elif sys.platform == "darwin":
        lib_name = "libcalculator.dylib"
    else:
        lib_name = "libcalculator.so"

    lib_path = os.path.join(lib_dir, lib_name)

    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"找不到C库文件: {lib_path}")

    print(f"加载库: {lib_path}")
    return ctypes.CDLL(lib_path)


def test_calculator():
    """测试计算器函数"""
    try:
        lib = load_c_library()
    except FileNotFoundError as e:
        print(f"❌ 无法加载C库: {e}")
        print("请先编译C项目: cd calculator && mkdir -p build && cd build && cmake .. && make")
        return False

    # 设置函数参数和返回类型
    lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add.restype = ctypes.c_int

    lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.subtract.restype = ctypes.c_int

    lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.multiply.restype = ctypes.c_int

    lib.divide.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.divide.restype = ctypes.c_double

    # 运行测试
    tests_passed = 0
    total_tests = 4

    # 测试加法
    result = lib.add(10, 5)
    if result == 15:
        print("✓ 加法测试通过: 10 + 5 = 15")
        tests_passed += 1
    else:
        print(f"❌ 加法测试失败: 期望15，得到{result}")

    # 测试减法
    result = lib.subtract(10, 5)
    if result == 5:
        print("✓ 减法测试通过: 10 - 5 = 5")
        tests_passed += 1
    else:
        print(f"❌ 减法测试失败: 期望5，得到{result}")

    # 测试乘法
    result = lib.multiply(10, 5)
    if result == 50:
        print("✓ 乘法测试通过: 10 * 5 = 50")
        tests_passed += 1
    else:
        print(f"❌ 乘法测试失败: 期望50，得到{result}")

    # 测试除法
    result = lib.divide(10, 5)
    if abs(result - 2.0) < 0.001:
        print("✓ 除法测试通过: 10 / 5 = 2.0")
        tests_passed += 1
    else:
        print(f"❌ 除法测试失败: 期望2.0，得到{result}")

    print(f"\n测试结果: {tests_passed}/{total_tests} 通过")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = test_calculator()
    sys.exit(0 if success else 1)