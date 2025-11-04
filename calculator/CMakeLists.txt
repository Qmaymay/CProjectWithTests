cmake_minimum_required(VERSION 3.10)
project(Calculator LANGUAGES C)

# 设置输出目录
set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../lib)
set(EXECUTABLE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../lib)

# 确保输出目录存在
file(MAKE_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY})

# 库源文件列表
set(CALC_SOURCES
        calculator.c
        error_handling.c
)

# 头文件目录
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# 创建共享库
add_library(calc SHARED ${CALC_SOURCES})

# 设置库输出属性
# 设置库输出属性 - 去掉 "lib" 前缀
set_target_properties(calc PROPERTIES
        OUTPUT_NAME "calculator"           # 这很重要！
        PREFIX ""                          # 去掉 "lib" 前缀
        LIBRARY_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
        RUNTIME_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
)
# Windows 特定设置
if(WIN32)
    target_compile_definitions(calc PRIVATE CALC_EXPORTS)
endif()

# 链接数学库
find_library(MATH_LIB m)
if(MATH_LIB)
    target_link_libraries(calc ${MATH_LIB})
endif()

# 如果有 main.c，创建可执行文件
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/main.c")
    add_executable(calculator_app main.c)
    target_link_libraries(calculator_app calc)

    # 设置可执行文件输出
    set_target_properties(calculator_app PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
    )
endif()

message(STATUS "Calculator 配置完成")
message(STATUS "库文件输出到: ${LIBRARY_OUTPUT_DIRECTORY}")



#cmake_minimum_required(VERSION 3.10)
#project(calculator LANGUAGES C)
#
## 设置C标准
#set(CMAKE_C_STANDARD 11)
#set(CMAKE_C_STANDARD_REQUIRED ON)
#
#
## 设置跨平台的库输出目录
#set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
#
#
## 创建共享库
#add_library(calculator SHARED calculator.c
#        error_handling.c
#
#)
#
#
#
## 在这里添加 Windows 特定的 DLL 设置
##if(WIN32)
##    set_target_properties(calculator PROPERTIES
##            SUFFIX ".dll"  # Windows 下强制添加 .dll 后缀
##    )
##else()
##    set_target_properties(calculator PROPERTIES
##            SUFFIX ".so"   # Linux 下强制添加 .so 后缀
##    )
##endif()
#
## 设置包含目录: 它解决了C/C++项目中的一个基本问题：头文件查找。
#target_include_directories(calculator
#        PUBLIC
#        ${CMAKE_CURRENT_SOURCE_DIR}
#)
#
#
## 链接数学库（Linux需要）
#if(UNIX AND NOT APPLE)
#    target_link_libraries(calculator m)
#endif()
#
#
## 创建可执行文件
#add_executable(calculator_app main.c)
#target_link_libraries(calculator_app calculator)
#
## 在 target_link_libraries 之后添加——避免属性被覆盖
## 在github的虚拟机的所有平台（包括windows和Linux）里去掉lib前缀，统一命名为calculator
##set_target_properties(calculator PROPERTIES OUTPUT_NAME "calculator" PREFIX "")
## 设置输出属性（确保生成 .so 文件）
#set_target_properties(calculator PROPERTIES
#        OUTPUT_NAME "calculator"
#        PREFIX ""
#        SUFFIX ".so"
#)
## 针对MSVC的设置
#if(MSVC)
#    # 确保同时生成导入库
#    set_target_properties(calculator PROPERTIES
#            WINDOWS_EXPORT_ALL_SYMBOLS ON
#    )
#
#    # 或者禁用特定警告
#    target_compile_options(calculator PRIVATE "/wd4244;/wd4723")
#endif()