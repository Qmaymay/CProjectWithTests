# ==================== 1. Basic Configuration ====================
cmake_minimum_required(VERSION 3.10)
project(Calculator LANGUAGES C)

if(MSVC)
    add_compile_options(/utf-8)
else()
    add_compile_options(-finput-charset=UTF-8)
endif()

# Detect environment
if(DEFINED ENV{GITHUB_ACTIONS})
    message(STATUS "Running in GitHub Actions environment")
    set(IS_CI TRUE)
else()
    message(STATUS "Running in local development environment")
    set(IS_CI FALSE)
endif()

# ==================== 2. Compiler Options ====================
# Set build type first, then configure options accordingly
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)  # Default to Debug mode
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0)
    message(STATUS "Debug mode enabled")
else()
    add_compile_options(-O2)
    message(STATUS "Release mode: ${CMAKE_BUILD_TYPE}")
endif()

# ==================== 3. Output Directory Configuration ====================
# Unified output directory structure
set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(EXECUTABLE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Use simpler paths in CI environment
if(IS_CI)
    set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
    set(EXECUTABLE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
endif()

# Ensure output directories exist
file(MAKE_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY})
file(MAKE_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY})

# ==================== 4. Source Files Configuration ====================
set(CALC_SOURCES
        calculator.c
        error_handling.c
)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# ==================== 5. Dynamic Library Target ====================
add_library(calc SHARED ${CALC_SOURCES})

# Platform-specific library naming
if(WIN32)
    if(MSVC)
        set_target_properties(calc PROPERTIES
                OUTPUT_NAME "calculator_msvc"
                PREFIX ""
                SUFFIX ".dll"
        )
    else()
        set_target_properties(calc PROPERTIES
                OUTPUT_NAME "calculator"
                PREFIX ""
                SUFFIX ".dll"
        )
    endif()
    target_compile_definitions(calc PRIVATE CALC_EXPORTS)
else()
    # Linux/macOS use default naming (libcalc.so)
    set_target_properties(calc PROPERTIES
            OUTPUT_NAME "calc"
            PREFIX "lib"
            SUFFIX ".so"
    )
endif()

# Set output directories
set_target_properties(calc PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
        RUNTIME_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
)

# Copy library to project lib directory after build (for Python tests)
add_custom_command(TARGET calc POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:calc>
        ${CMAKE_SOURCE_DIR}/../../lib/$<TARGET_FILE_NAME:calc>
        COMMENT "Copying library to project lib directory"
)

# ==================== 6. Executable Target ====================
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/main.c")
    add_executable(calculator_app main.c)
    target_link_libraries(calculator_app calc)

    # Platform-specific naming for GitHub Actions (for test differentiation)
    if(MSVC)
        set_target_properties(calculator_app PROPERTIES
                OUTPUT_NAME "calculator_app_msvc"
                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
        )
    elseif(WIN32)
        set_target_properties(calculator_app PROPERTIES
                OUTPUT_NAME "calculator_app_mingw"
                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
        )
    else()
        set_target_properties(calculator_app PROPERTIES
                OUTPUT_NAME "calculator_app_linux"
                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
        )
    endif()

    # Copy DLL to executable directory for CLion
    if(WIN32)
        add_custom_command(TARGET calculator_app POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                "$<TARGET_FILE:calc>"
                "${EXECUTABLE_OUTPUT_DIRECTORY}/$<TARGET_FILE_NAME:calc>"
                COMMENT "Copying dependent DLL to executable directory"
        )
    endif()
endif()

# ==================== 7. Dependency Configuration ====================
# Math library linking
find_library(MATH_LIB m)
if(MATH_LIB)
    target_link_libraries(calc PRIVATE ${MATH_LIB})
    message(STATUS "Math library found: ${MATH_LIB}")
else()
    message(STATUS "Math library not found, continuing without it")
endif()

# ==================== 8. Compiler Specific Settings ====================
if(MSVC)
    target_compile_options(calc PRIVATE "/utf-8")
    if(TARGET calculator_app)
        target_compile_options(calculator_app PRIVATE "/utf-8")
    endif()
endif()

# ==================== 9. Testing and Validation Targets ====================
# Build validation target (fully cross-platform)
add_custom_target(validate_all
        COMMAND ${CMAKE_COMMAND} -E echo "Build successful!"
        COMMAND ${CMAKE_COMMAND} -E echo "Library file: $<TARGET_FILE:calc>"
        COMMAND ${CMAKE_COMMAND} -E echo "Executable file: $<TARGET_FILE:calculator_app>"
        COMMENT "Validating build results"
        DEPENDS calc calculator_app
)

# Dependencies
add_dependencies(validate_all calc)
if(TARGET calculator_app)
    add_dependencies(validate_all calculator_app)
endif()

# ==================== 10. Clean Target ====================
# Safe clean target - only clean generated files
# 清理目标
add_custom_target(clean_all
        COMMAND ${CMAKE_COMMAND} -E echo "Cleaning generated files..."

        # 更新清理路径
        COMMAND ${CMAKE_COMMAND} -E remove $<TARGET_FILE:calc>
        COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_SOURCE_DIR}/../../lib/$<TARGET_FILE_NAME:calc>

        # 如果有可执行文件，也清理它
        COMMAND ${CMAKE_COMMAND} -E remove $<TARGET_FILE:calculator_app>

        COMMENT "Safe clean: only removing generated target files"
)

# ==================== 11. Installation Target (Optional) ====================
# Installation configuration
install(TARGETS calc
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
)

if(TARGET calculator_app)
    install(TARGETS calculator_app
            RUNTIME DESTINATION bin
    )
endif()

# ==================== 12. Summary Information ====================
message(STATUS "")
message(STATUS "====== Calculator Configuration Complete ======")
message(STATUS "Project Name: ${PROJECT_NAME}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Library Output: ${LIBRARY_OUTPUT_DIRECTORY}")
message(STATUS "Executable Output: ${EXECUTABLE_OUTPUT_DIRECTORY}")
message(STATUS "Available Targets:")
message(STATUS "   - calc (shared library)")
if(TARGET calculator_app)
    message(STATUS "   - calculator_app (executable)")
endif()
message(STATUS "   - validate_all (verify build)")
message(STATUS "   - clean_all (clean build artifacts)")
message(STATUS "")
message(STATUS "Build Command:")
message(STATUS "   cmake --build . --target validate_all")
message(STATUS "Clean Command:")
message(STATUS "   cmake --build . --target clean_all")
message(STATUS "======================================")


## 强制中文编码（不推荐，可能仍有问题）
#if(WIN32 AND NOT MSVC)
#    execute_process(COMMAND chcp 65001)
#endif()
#
#
## ==================== 1. 基础配置 ====================
#cmake_minimum_required(VERSION 3.10)
#project(Calculator LANGUAGES C)
#
## 检测环境
#if(DEFINED ENV{GITHUB_ACTIONS})
#    message(STATUS "? 运行在 GitHub Actions 环境")
#    set(IS_CI TRUE)
#else()
#    message(STATUS "? 运行在本地开发环境")
#    set(IS_CI FALSE)
#endif()
#
## ==================== 2. 编译选项配置 ====================
## 调试模式配置
## 先设置构建类型，再根据类型配置选项
#if(NOT CMAKE_BUILD_TYPE)
#    set(CMAKE_BUILD_TYPE Debug)  # 默认使用Debug模式
#endif()
#
#if(CMAKE_BUILD_TYPE STREQUAL "Debug")
#    add_compile_options(-g -O0)
#    message(STATUS "? 调试模式已启用")
#else()
#    add_compile_options(-O2)
#    message(STATUS "? 发布模式: ${CMAKE_BUILD_TYPE}")
#endif()
#
## ==================== 3. 输出目录配置 ====================
## 统一输出目录结构
#set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
#set(EXECUTABLE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
#
## CI环境下使用更简洁的路径
#if(IS_CI)
#    set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
#    set(EXECUTABLE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
#endif()
#
## 确保输出目录存在
#file(MAKE_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY})
#file(MAKE_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY})
#
## ==================== 4. 源文件配置 ====================
#set(CALC_SOURCES
#        calculator.c
#        error_handling.c
#)
#
## 头文件目录
#include_directories(${CMAKE_CURRENT_SOURCE_DIR})
#
## ==================== 5. 动态库目标 ====================
#add_library(calc SHARED ${CALC_SOURCES})
#
## 平台特定的库命名
#if(WIN32)
#    if(MSVC)
#        set_target_properties(calc PROPERTIES
#                OUTPUT_NAME "calculator_msvc"
#                PREFIX ""
#                SUFFIX ".dll"
#        )
#    else()
#        set_target_properties(calc PROPERTIES
#                OUTPUT_NAME "calculator"
#                PREFIX ""
#                SUFFIX ".dll"
#        )
#    endif()
#    target_compile_definitions(calc PRIVATE CALC_EXPORTS)
#else()
#    # Linux/macOS 使用默认命名 (libcalc.so)
#    set_target_properties(calc PROPERTIES
#            OUTPUT_NAME "calc"
#            PREFIX "lib"
#            SUFFIX ".so"
#    )
#endif()
#
## 设置输出目录
#set_target_properties(calc PROPERTIES
#        LIBRARY_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
#        RUNTIME_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_DIRECTORY}
#)
#
## 构建后复制库文件到项目lib目录（这样Python测试就能找到了）
## 构建后复制库文件到项目lib目录
#add_custom_command(TARGET calc POST_BUILD
#        COMMAND ${CMAKE_COMMAND} -E copy
#        $<TARGET_FILE:calc>
#        ${CMAKE_SOURCE_DIR}/../lib/$<TARGET_FILE_NAME:calc>  # 使用目标文件名
#        COMMENT "复制库文件到项目lib目录"
#)
#
## ==================== 6. 可执行文件目标 ====================
#if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/main.c")
#    add_executable(calculator_app main.c)
#    target_link_libraries(calculator_app calc)
#
#    # GitHub Actions需要：平台特定命名（用于区分测试）
#    if(MSVC)
#        set_target_properties(calculator_app PROPERTIES
#                OUTPUT_NAME "calculator_app_msvc"
#                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
#        )
#    elseif(WIN32)
#        set_target_properties(calculator_app PROPERTIES
#                OUTPUT_NAME "calculator_app_mingw"
#                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
#        )
#    else()
#        set_target_properties(calculator_app PROPERTIES
#                OUTPUT_NAME "calculator_app_linux"
#                RUNTIME_OUTPUT_DIRECTORY ${EXECUTABLE_OUTPUT_DIRECTORY}
#        )
#    endif()
#
#    # 为CLion创建符号链接或复制（解决IDE找不到文件的问题）
#    # 复制DLL文件到可执行文件目录
#    if(WIN32)
#        add_custom_command(TARGET calculator_app POST_BUILD
#                COMMAND ${CMAKE_COMMAND} -E copy
#                "$<TARGET_FILE:calc>"
#                "${EXECUTABLE_OUTPUT_DIRECTORY}/$<TARGET_FILE_NAME:calc>"
#                COMMENT "复制依赖的DLL到可执行文件目录"
#        )
#    endif()
#endif()
#
## ==================== 7. 依赖库配置 ====================
## 数学库链接
#find_library(MATH_LIB m)
#if(MATH_LIB)
#    target_link_libraries(calc PRIVATE ${MATH_LIB})
#    message(STATUS "找到数学库: ${MATH_LIB}")
#else()
#    message(STATUS "未找到数学库，但继续构建")
#endif()
#
## ==================== 8. 编译器特定设置 ====================
#if(MSVC)
#    target_compile_options(calc PRIVATE "/utf-8")
#    if(TARGET calculator_app)
#        target_compile_options(calculator_app PRIVATE "/utf-8")
#    endif()
#endif()
#
## ==================== 9. 测试和验证目标 ====================
## 构建验证目标（完全跨平台）
#add_custom_target(validate_all
#        COMMAND ${CMAKE_COMMAND} -E echo "✅ 构建成功！"
#        COMMAND ${CMAKE_COMMAND} -E echo "库文件已生成: $<TARGET_FILE:calc>"
#        COMMAND ${CMAKE_COMMAND} -E echo "可执行文件已生成: $<TARGET_FILE:calculator_app>"
#        COMMENT "验证构建结果"
#        DEPENDS calc calculator_app
#)
#
## 依赖关系
#add_dependencies(validate_all calc)
#if(TARGET calculator_app)
#    add_dependencies(validate_all calculator_app)
#endif()
#
## ==================== 10. 清理目标 ====================
## 清理所有构建产物
## 安全的清理目标 - 只清理生成的文件
#add_custom_target(clean_all
#        COMMAND ${CMAKE_COMMAND} -E echo "清理生成的文件..."
#
#        # 只删除生成的目标文件，不删除构建目录
#        COMMAND ${CMAKE_COMMAND} -E remove $<TARGET_FILE:calc>
#        COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_SOURCE_DIR}/../lib/$<TARGET_FILE_NAME:calc>
#
#        # 如果有可执行文件，也清理它
#        COMMAND ${CMAKE_COMMAND} -E remove $<TARGET_FILE:calculator_app>
#
#        COMMENT "安全清理：只删除生成的目标文件"
#)
#
## ==================== 11. 安装目标（可选） ====================
## 安装配置
#install(TARGETS calc
#        LIBRARY DESTINATION lib
#        ARCHIVE DESTINATION lib
#        RUNTIME DESTINATION bin
#)
#
#if(TARGET calculator_app)
#    install(TARGETS calculator_app
#            RUNTIME DESTINATION bin
#    )
#endif()
#
## ==================== 12. 总结信息 ====================
## ==================== 12. 总结信息 ====================
#message(STATUS "")
#message(STATUS "====== Calculator Configuration Complete ======")
#message(STATUS "Project Name: ${PROJECT_NAME}")
#message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
#message(STATUS "Library Output: ${LIBRARY_OUTPUT_DIRECTORY}")
#message(STATUS "Executable Output: ${EXECUTABLE_OUTPUT_DIRECTORY}")
#message(STATUS "Available Targets:")
#message(STATUS "   - calc (shared library)")
#if(TARGET calculator_app)
#    message(STATUS "   - calculator_app (executable)")
#endif()
#message(STATUS "   - validate_all (verify build)")
#message(STATUS "   - clean_all (clean build artifacts)")
#message(STATUS "")
#message(STATUS "Build Command:")
#message(STATUS "   cmake --build . --target validate_all")
#message(STATUS "Clean Command:")
#message(STATUS "   cmake --build . --target clean_all")
#message(STATUS "======================================")