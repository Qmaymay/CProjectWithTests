@echo off
echo ?? ???? C ????...
cd calculator
if exist build rmdir /s /q build
cmake -B build -G "MinGW Makefiles" && cmake --build build
if %errorlevel% equ 0 (
    cd ..
    mkdir lib 2>nul
    copy calculator\build\libcalculator.dll lib\ >nul
    echo ? ?????
) else (
    echo ? ????
)
pause
