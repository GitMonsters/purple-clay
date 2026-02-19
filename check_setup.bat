@echo off
REM Setup verification script for Purple Clay (Windows)
REM Checks prerequisites and provides helpful guidance

echo ===============================================================================
echo.
echo                  Purple Clay - Setup Verification Script
echo.
echo ===============================================================================
echo.

set ALL_GOOD=1

echo Checking prerequisites...
echo.

REM Check for Python
echo 1. Checking Python installation...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m[OK][0m Python found
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
    echo    Version: %PYTHON_VERSION%
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [32m[OK][0m Python3 found
        for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%v
        echo    Version: %PYTHON_VERSION%
        set PYTHON_CMD=python3
    ) else (
        echo [31m[ERROR][0m Python not found
        set ALL_GOOD=0
        goto NO_PYTHON
    )
)
echo.

REM Check for pip
echo 2. Checking pip installation...

pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m[OK][0m pip found
    set PIP_CMD=pip
) else (
    pip3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [32m[OK][0m pip3 found
        set PIP_CMD=pip3
    ) else (
        %PYTHON_CMD% -m pip --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo [32m[OK][0m pip available via 'python -m pip'
            set PIP_CMD=%PYTHON_CMD% -m pip
        ) else (
            echo [31m[ERROR][0m pip not found
            set ALL_GOOD=0
        )
    )
)
echo.

REM Check for git
echo 3. Checking git installation...

git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m[OK][0m git found
) else (
    echo [33m[WARNING][0m git not found (optional, but needed to clone repository)
)
echo.

REM Summary
echo ===============================================================================
echo.

if %ALL_GOOD% equ 1 (
    echo [32m[SUCCESS] All prerequisites met![0m
    echo.
    echo You can now install Purple Clay:
    echo.
    echo   %PIP_CMD% install -e .
    echo.
    echo Then run the demo:
    echo.
    echo   %PYTHON_CMD% purple_clay_demo.py
    echo.
) else (
    echo [31m[ERROR] Some prerequisites are missing[0m
    echo.
    echo Please install the missing components:
    echo.
    
    :NO_PYTHON
    if %ALL_GOOD% equ 0 (
        echo Python 3.8+:
        echo   Download from https://www.python.org/downloads/windows/
        echo   IMPORTANT: Check 'Add Python to PATH' during installation
        echo.
        echo After installing, open a NEW command prompt and run this script again.
        echo.
    )
    
    echo For detailed installation instructions, see INSTALLATION.md
)

echo ===============================================================================

pause
