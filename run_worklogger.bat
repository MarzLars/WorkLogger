@echo off
REM Navigate to the repository directory
cd /d "%~dp0"

REM Find Python executable and Pip paths
setlocal enabledelayedexpansion
set PYTHON_FOUND=0
for /f "delims=" %%i in ('where python') do (
    if "%%i"=="%SystemRoot%\System32\python.exe" (
        REM Skip the Microsoft Store version of Python
        continue
    ) else (
        set PYTHON_PATH=%%i
        set PYTHON_FOUND=1
        goto :found_python
    )
)
:found_python

if !PYTHON_FOUND!==0 (
    echo No valid Python installation found.
    pause
    exit /b 1
)

for /f "delims=" %%i in ('where pip') do set PIP_PATH=%%i

REM Debugging: Print the paths
echo PYTHON_PATH=%PYTHON_PATH%
echo PIP_PATH=%PIP_PATH%

REM Check if Pip executable exists
if "%PIP_PATH%"=="" (
    echo Pip executable not found.
    pause
    exit /b 1
)

REM Check if a virtual environment exists, if not, create one
if not exist venv (
    %PYTHON_PATH% -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Ensure pip is installed
%PYTHON_PATH% -m ensurepip --upgrade

REM Upgrade pip to the latest version
%PIP_PATH% install --upgrade pip

REM Install dependencies
%PIP_PATH% install -r requirements.txt || pause

REM Run the main script
%PYTHON_PATH% main.py || pause

REM Deactivate the virtual environment
call venv\Scripts\deactivate

pause