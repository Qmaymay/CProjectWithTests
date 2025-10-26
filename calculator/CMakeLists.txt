cmake_minimum_required(VERSION 3.17)
project(calculator C)

set(CMAKE_C_STANDARD 11)

# 创建共享库
add_library(calculator SHARED calculator.h main.c)

# 同时创建可执行文件（可选）
add_executable(calculator_exe main.c)
target_link_libraries(calculator_exe calculator)