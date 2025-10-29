@echo off
echo Building C library...
cd calculator
if exist build rmdir /s /q build
cmake -B build -G "MinGW Makefiles"
if %errorlevel% neq 0 (
    echo CMake configuration failed!
    pause
    exit /b 1
)
cmake --build build
if %errorlevel% equ 0 (
    cd ..
    mkdir lib 2>nul
    copy calculator\build\libcalculator.dll lib\ >nul
    echo Build successful!
) else (
    echo Build failed!
)
pause
