@echo off
cd /d "%~dp0"
chcp 65001 >nul
title Songyun - Model Download

echo ============================================
echo   모델 미리 다운로드 (0%%에서 멈출 때 사용)
echo ============================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo venv이 없습니다. 먼저 run.bat을 한 번 실행하세요.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
set HF_HUB_ENABLE_HF_TRANSFER=0

echo .env의 HF_ENDPOINT, HF_TOKEN 사용
echo 느리면 .env에 HF_ENDPOINT=https://hf-mirror.com 추가
echo.
python download_model.py

pause
