@echo off
echo.
echo ======================================
echo  Advanced Reasoning System - Web UI
echo ======================================
echo.

REM Check if API key is set
if "%DEEPSEEK_API_KEY%"=="" (
    echo WARNING: DEEPSEEK_API_KEY is not set!
    echo.
    echo Please set your API key first:
    echo   set DEEPSEEK_API_KEY=your-api-key-here
    echo.
    echo Or in PowerShell:
    echo   $env:DEEPSEEK_API_KEY = "your-api-key-here"
    echo.
    pause
    exit /b 1
)

echo Starting web server...
echo.
echo The web interface will open at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python web_server.py

pause
