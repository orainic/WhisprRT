@echo off
echo ========================================
echo WhisprRT - Starting Production Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo [ERROR] Virtual environment not found!
    echo Please run install.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Starting WhisprRT in production mode...
echo.
echo ========================================
echo Server Information
echo ========================================
echo - Access URL: http://127.0.0.1:8000
echo - Running in production mode (no auto-reload)
echo - Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server without reload for production
uvicorn app.main:app --host 0.0.0.0 --port 8000

REM If server stops, pause to see any error messages
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server stopped with an error
    echo Please check the error message above
    pause
)
