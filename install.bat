@echo off
echo ========================================
echo WhisprRT Installation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists, skipping creation...
) else (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

echo.
echo [3/4] Installing dependencies...
echo This may take a few minutes, please wait...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install fastapi>=0.115.12 faster-whisper>=1.1.1 jinja2>=3.1.6 numpy>=2.2.5 sounddevice>=0.5.1 "uvicorn[standard]>=0.34.2" websockets>=15.0.1

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Installation complete!
echo.
echo ========================================
echo Installation Summary
echo ========================================
echo - Virtual environment created at: .venv
echo - All dependencies installed
echo - Ready to start the server
echo.
echo To start the server, run: start.bat
echo Or manually: .venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo.
echo Note: First run will download the Whisper model (~1-2 GB)
echo This may take a few minutes depending on your internet connection.
echo ========================================
echo.
pause
