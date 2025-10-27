cmake_minimum_required(VERSION 3.17)
project(calculator C)

set(CMAKE_C_STANDARD 11)

# 创建共享库
add_library(calculator SHARED calculator.h calculator.c
        calculator.c)

# 同时创建可执行文件用于手动测试
add_executable(calculator_exe main.c)
target_link_libraries(calculator_exe calculator)

# 设置输出目录，让库文件在固定位置
set_target_properties(calculator PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
        ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib
)