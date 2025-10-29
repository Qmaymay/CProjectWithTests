cmake_minimum_required(VERSION 3.10)
project(calculator)

# 创建共享库
add_library(calculator SHARED calculator.c)

# 创建可执行文件，命名为 main
add_executable(main main.c)
target_link_libraries(main calculator)