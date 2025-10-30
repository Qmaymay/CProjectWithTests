@echo off
echo Starting quick test...
echo.

echo 1. Building C library...
cd ..
call build.bat

echo.
echo 2. Running Python tests...
cd calculator_tests
python test_interfaces.py
if %errorlevel% equ 0 (
    echo.
    echo All tests passed! Ready to push to GitHub.
) else (
    echo.
    echo Tests failed, please check issues.
)

pause
