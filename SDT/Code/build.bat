@echo off
REM Build script for SDT Atomic Calculator

echo Setting up Visual Studio environment...
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

echo.
echo Compiling SDT Atomic Calculator...
cl /std:c++20 /EHsc /O2 demo_atomic_calc.cpp /I. /Fe:sdt_atomic.exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Build successful!
    echo.
    echo Running demo...
    echo.
    sdt_atomic.exe
) else (
    echo.
    echo ✗ Build failed with error code %ERRORLEVEL%
)

pause
