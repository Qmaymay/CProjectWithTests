cmake_minimum_required(VERSION 3.10)
project(calculator LANGUAGES C)

# 设置C标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 针对MSVC编译器设置UTF-8编码
if(MSVC)
    # 禁用特定编码警告
    add_compile_options("/wd4828")
endif()

# 设置跨平台的库输出目录
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../lib)


# 创建共享库
add_library(calculator SHARED calculator.c
        version.h
        error_handling.c
        error_handling.h
)

# 针对MSVC的设置
if(MSVC)
    # 确保同时生成导入库
    set_target_properties(calculator PROPERTIES
            WINDOWS_EXPORT_ALL_SYMBOLS ON
    )

    # 或者禁用特定警告
    target_compile_options(calculator PRIVATE "/wd4244;/wd4723")
endif()

# 设置包含目录: 它解决了C/C++项目中的一个基本问题：头文件查找。
target_include_directories(calculator
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# 链接数学库（Linux需要）
if(UNIX AND NOT APPLE)
    target_link_libraries(calculator m)
endif()


# 创建可执行文件
add_executable(calculator_app main.c)
target_link_libraries(calculator_app calculator)

# 针对MSVC的设置
if(MSVC)
    # 确保同时生成导入库
    set_target_properties(calculator PROPERTIES
            WINDOWS_EXPORT_ALL_SYMBOLS ON
    )

    # 或者禁用特定警告
    target_compile_options(calculator PRIVATE "/wd4244;/wd4723")
endif()