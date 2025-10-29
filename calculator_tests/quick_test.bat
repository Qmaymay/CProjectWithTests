@echo off
echo Starting quick test...
echo.

echo 1. Building C library...
cd ..
call build.bat
if %errorlevel% neq 0 (
    echo Build failed
    pause
    exit /b 1
)

echo.
echo 2. Running Python tests...
python test_interfaces.py
if %errorlevel% equ 0 (
    echo.
    echo All tests passed! Ready to push to GitHub.
) else (
    echo.
    echo Tests failed, please check issues.
)

pause
