cmake_minimum_required(VERSION 3.17)
project(CProjectWithTests C)

set(CMAKE_C_STANDARD 11)

# 设置输出目录
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)

# 创建共享库
add_library(calculator SHARED
        calculator/calculator.c
        calculator/calculator.h
)

# 创建可执行文件
add_executable(calculator_exe
        calculator/main.c
)

# 链接库
target_link_libraries(calculator_exe calculator)