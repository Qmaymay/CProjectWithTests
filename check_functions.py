
import ctypes
import os

def detailed_check():
    dll_path = "lib/calculator.dll"
    print(f"检查DLL: {dll_path}")

    try:
        dll = ctypes.CDLL(dll_path)
        print("✅ DLL加载成功")

        # 尝试获取所有应该导出的函数
        functions = [
            'add', 'subtract', 'multiply', 'divide',
            'power', 'square', 'cube', 'square_root',
            'get_last_error', 'get_last_error_code', 'clear_error'
        ]

        print("\n🔍 检查函数导出:")
        found_count = 0
        for func_name in functions:
            try:
                func = getattr(dll, func_name)
                print(f"   ✅ {func_name}")
                found_count += 1
            except AttributeError:
                print(f"   ❌ {func_name} - 未找到")

        print(f"\n📊 统计: 找到 {found_count}/{len(functions)} 个函数")

        if found_count == 0:
            print("\n⚠️ 可能的问题:")
            print("1. 函数没有正确导出")
            print("2. 函数名称修饰问题")
            print("3. 需要检查头文件中的导出声明")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    detailed_check()