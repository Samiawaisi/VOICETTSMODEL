@echo off
title Edge TTS Studio
echo ========================================
echo        Edge TTS Studio v1.0
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Install dependencies if needed
if not exist "backend\venv" (
    echo [INFO] Installing dependencies...
    cd backend
    pip install -r requirements.txt
    cd ..
    echo.
)

echo [INFO] Starting Edge TTS Studio...
echo [INFO] Open http://localhost:8000 in your browser
echo.

cd backend
python app.py
pause
