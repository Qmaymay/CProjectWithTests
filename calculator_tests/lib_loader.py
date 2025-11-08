# -*- coding: utf-8 -*-
import os


def get_lib_dir():
    """获取库目录"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('项目根目录: ', project_root)
    return os.path.join(project_root, 'build', 'lib')


def scan_lib_directory():
    """扫描lib目录，返回文件名列表"""
    lib_dir = get_lib_dir()

    if not os.path.exists(lib_dir):
        return [], []

    libraries = []
    executables = []

    for filename in os.listdir(lib_dir):
        # 动态库：只保留带编译器标识的
        if filename.endswith(('.dll', '.so')):
            if any(compiler in filename for compiler in ['_mingw', '_msvc', '_linux']):

                libraries.append(filename)
        # 可执行文件
        elif filename.endswith('.exe') or '.' not in filename:
            executables.append(filename)

    return libraries, executables


# 直接提供文件名列表
library_files, executable_files = scan_lib_directory()

if __name__ == "__main__":
    print("=== 构建产物 ===")
    print(f"动态库: {library_files}")
    print(f"可执行文件: {executable_files}")
