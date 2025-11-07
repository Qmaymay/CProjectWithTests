@echo off
chcp 65001 > nul

echo ========================================
echo   Multi-Platform Build Script
echo ========================================

set PROJECT_ROOT=%~dp0
set OUTPUT_DIR=%PROJECT_ROOT%all_builds

echo.
echo 1. Building MinGW version...
mkdir build_mingw 2>nul
cmake -B build_mingw -S %PROJECT_ROOT%calculator -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build build_mingw
if %errorlevel% equ 0 (
    echo ✅ MinGW build successful
) else (
    echo ❌ MinGW build failed
)

echo.
echo 2. Creating output directory...
mkdir %OUTPUT_DIR% 2>nul

echo.
echo 3. Copying MinGW artifacts...
copy build_mingw\lib\calculator_mingw.dll %OUTPUT_DIR%\ 2>nul
copy build_mingw\lib\calculator_app_mingw.exe %OUTPUT_DIR%\ 2>nul

echo.
echo ========================================
echo Build Summary
echo ========================================
echo Generated Files in %OUTPUT_DIR%:
dir %OUTPUT_DIR% /B

echo.
echo Platform Notes:
echo - MinGW: ✅ Built successfully
echo - MSVC:  ⚠️  Requires Visual Studio
echo - Linux: ⚠️  Requires Linux system
echo ========================================