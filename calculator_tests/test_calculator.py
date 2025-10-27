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

    # 新增：幂运算函数类型声明
    lib.power.argtypes = [ctypes.c_double, ctypes.c_int]
    lib.power.restype = ctypes.c_double

    # 运行测试
    tests_passed = 0
    total_tests = 8

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

    # 在测试幂运算之前添加调试
    print("调试信息:")
    print(f"power函数地址: {hex(lib.power if hasattr(lib, 'power') else 0)}")

    # 新增4个幂运算测试
    result = lib.power(2.0, 3)
    print(f"调试: power(2.0, 3) = {result}, 期望: 8.0")
    if abs(result - 8.0) < 0.001:
        print("✓ 幂运算测试通过: 2.0 ^ 3 = 8.0")
        tests_passed += 1
    else:
        print(f"❌ 幂运算测试失败: 期望8.0，得到{result}")

    result = lib.power(5.0, 0)
    if abs(result - 1.0) < 0.001:
        print("✓ 零次幂测试通过: 5.0 ^ 0 = 1.0")
        tests_passed += 1
    else:
        print(f"❌ 零次幂测试失败: 期望1.0，得到{result}")

    result = lib.power(2.0, -1)
    if abs(result - 0.5) < 0.001:
        print("✓ 负指数测试通过: 2.0 ^ -1 = 0.5")
        tests_passed += 1
    else:
        print(f"❌ 负指数测试失败: 期望0.5，得到{result}")

    result = lib.power(1.5, 2)
    if abs(result - 2.25) < 0.001:
        print("✓ 小数底数测试通过: 1.5 ^ 2 = 2.25")
        tests_passed += 1
    else:
        print(f"❌ 小数底数测试失败: 期望2.25，得到{result}")

    print(f"\n测试结果: {tests_passed}/{total_tests} 通过")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = test_calculator()
    sys.exit(0 if success else 1)

