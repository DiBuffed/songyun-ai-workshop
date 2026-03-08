@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Hugging Face 로그인

echo ============================================
echo   Hugging Face 로그인
echo ============================================
echo.
echo 브라우저가 열리면 로그인하세요.
echo 또는 토큰을 입력하세요: https://huggingface.co/settings/tokens
echo.

venv\Scripts\python.exe -c "from huggingface_hub import login; login()"

echo.
echo 완료. 아무 키나 누르면 종료합니다.
pause >nul
