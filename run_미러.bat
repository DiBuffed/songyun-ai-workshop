@echo off
cd /d "%~dp0"
chcp 65001 >nul
title Songyun - HF 미러 사용

echo ============================================
echo   HF 미러 사용 (다운로드 0%% 멈출 때)
echo ============================================
echo.

set HF_ENDPOINT=https://hf-mirror.com
set HF_HUB_ENABLE_HF_TRANSFER=0

call run.bat
