cmake_minimum_required(VERSION 3.10)
project(calculator)


# 设置跨平台的库输出目录
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib)

# 创建共享库
add_library(calculator SHARED calculator.c
        version.h
)

# 设置包含目录
target_include_directories(calculator PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# 链接数学库（Linux 需要）
target_link_libraries(calculator m)

# 创建可执行文件，命名为 main
add_executable(calculator_app main.c)
target_link_libraries(calculator_app calculator)
