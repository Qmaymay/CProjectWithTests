cmake_minimum_required(VERSION 3.17)
project(CProjectWithTests C)

set(CMAKE_C_STANDARD 11)

# 创建共享库 - Python 测试需要这个
add_library(calculator SHARED
    calculator/calculator.c
    calculator/calculator.h
)

# 创建可执行文件用于手动测试
add_executable(calculator_exe
    calculator/main.c
)

# 链接库
target_link_libraries(calculator_exe calculator)

# 设置库文件输出目录
set_target_properties(calculator PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY \/lib
    ARCHIVE_OUTPUT_DIRECTORY \/lib
)
