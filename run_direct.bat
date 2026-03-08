@echo off
cd /d "%~dp0"
chcp 65001 >nul
title Songyun AI Workshop

echo ============================================
echo   Songyun AI Workshop / 宋韵 AI 工作坊
echo ============================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo Error: venv not found. Run run.bat first to create it.
    pause
    exit /b 1
)

echo Starting app (direct mode)...
echo Public URL will appear below when ready.
echo.
set PYTHONIOENCODING=utf-8
venv\Scripts\python.exe app.py

pause
