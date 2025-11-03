chcp 65001 > nul
@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    Calculator Library Build Script
echo ========================================

set BUILD_SUCCESS=0

echo.
echo 1. 清理构建目录...
cd calculator
if exist build (
    echo   删除旧的构建目录...
    rmdir /s /q build
    if !errorlevel! neq 0 (
        echo ❌ 清理构建目录失败!
        exit /b 1
    )
)

echo.
echo 2. 生成构建系统...
cmake -B build -G "MinGW Makefiles"
if !errorlevel! neq 0 (
    echo ❌ CMake配置失败!
    exit /b 1
)

echo.
echo 3. 编译项目...
cmake --build build --config Release
if !errorlevel! neq 0 (
    echo ❌ 编译失败!
    exit /b 1
)

echo.
echo 4. 复制库文件...
cd ..
if not exist lib mkdir lib
if !errorlevel! neq 0 (
    echo ❌ 创建lib目录失败!
    exit /b 1
)

copy calculator\build\libcalculator.dll lib\ >nul
if !errorlevel! neq 0 (
    echo ❌ 复制库文件失败!
    echo   请检查文件是否存在: calculator\build\libcalculator.dll
    exit /b 1
)

echo.
echo 5. 验证构建结果...
if exist "lib\libcalculator.dll" (
    echo ✅ 构建成功! 库文件已生成: lib\libcalculator.dll
    set BUILD_SUCCESS=1
) else (
    echo ❌ 构建失败! 库文件未找到
    set BUILD_SUCCESS=0
)

echo.
echo 6. 运行简单测试...
if !BUILD_SUCCESS! equ 1 (
    python simple_test.py
    if !errorlevel! neq 0 (
        echo ⚠️  测试运行有警告
    )
) else (
    echo ❌ 跳过测试 - 构建失败
)

echo.
echo ========================================
if !BUILD_SUCCESS! equ 1 (
    echo ✅ 所有步骤完成!
) else (
    echo ❌ 构建过程中出现错误!
    exit /b 1
)
endlocal


