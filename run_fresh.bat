@echo off
cd /d "%~dp0"
chcp 65001 >nul
title Songyun AI Workshop

echo Stopping any existing app...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo.
echo Starting fresh...
call run.bat
