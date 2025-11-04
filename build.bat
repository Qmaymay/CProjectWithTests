chcp 65001 > nul
@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    Calculator Library Build Script
echo ========================================

set BUILD_SUCCESS=1

echo.
echo 1. Cleaning build directory...
if exist build (
    echo   Removing old build directory...
    rmdir /s /q build
    if !errorlevel! neq 0 (
        echo ERROR: Clean build directory failed!
        set BUILD_SUCCESS=0
    )
)

if exist build rmdir /s /q build
if exist lib\calculator.dll del lib\calculator.dll
if exist lib\libcalculator.dll del lib\libcalculator.dll
if exist lib\calculator_app.exe del lib\calculator_app.exe

echo.
echo 2. Generating build system...
cmake -B build -G "MinGW Makefiles"
if !errorlevel! neq 0 (
    echo ERROR: CMake configuration failed!
    set BUILD_SUCCESS=0
)

echo.
echo 3. Compiling project...
cmake --build build --config Release
if !errorlevel! neq 0 (
    echo ERROR: Compilation failed!
    set BUILD_SUCCESS=0
)

echo.
echo 4. Checking build results...
set LIB_FOUND=0
dir lib\*.dll >nul 2>&1
if !errorlevel! equ 0 (
    echo SUCCESS: Found DLL files in lib\
    set LIB_FOUND=1
)

if !LIB_FOUND! equ 0 (
    echo ERROR: No DLL files found in lib\ directory
    echo Available files in lib\:
    dir lib\ 2>nul || echo Directory is empty or does not exist
    set BUILD_SUCCESS=0
)


echo.
echo ========================================
if !BUILD_SUCCESS! equ 1 (
    echo SUCCESS: All steps completed! Build successful!
) else (
    echo ERROR: Build process encountered errors!
    exit /b 1
)

endlocal
