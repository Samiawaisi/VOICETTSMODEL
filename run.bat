@echo off
title Edge TTS Studio
color 0A
echo ===================================================
echo             🎙️ EDGE TTS STUDIO v1.0
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/2] Checking & Installing dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt --quiet

echo.
echo [2/2] Launching Edge TTS Studio App...
echo.
echo ===================================================
echo   App is running at: http://localhost:8000
echo   Browser will open automatically in 2 seconds!
echo   (Keep this window open while using the app)
echo ===================================================
echo.

python app.py
pause
