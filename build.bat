@echo off
chcp 65001 >nul

:: 设置测试模式环境变量
set TEST_BUILD=1

echo Building with MinGW...
rmdir /s /q build 2>nul
mkdir build && cd build
cmake .. -G "MinGW Makefiles" && cmake --build .
if %errorlevel% equ 0 echo ✅ Build successful!
cd ..
pause