@echo off
cd /d "%~dp0"
chcp 65001 >nul
title Songyun AI Workshop

echo ============================================
echo   Songyun AI Workshop / 宋韵 AI 工作坊
echo ============================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/4] Virtual environment exists.
)

echo [2/4] Activating...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo [4/4] Creating .env from template...
    copy .env.example .env >nul
) else (
    echo [4/4] Config found.
)

echo.
echo Starting app... (공개 링크 생성 시 팝업으로 표시됩니다)
echo.
set PYTHONIOENCODING=utf-8
set HF_HUB_ENABLE_HF_TRANSFER=0
venv\Scripts\python.exe run_with_url.py

pause
