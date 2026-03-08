@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   Hugging Face Space 업로드
echo ============================================
echo.
echo 토큰이 없다면: https://huggingface.co/settings/tokens
echo   - "New token" 클릭
echo   - Write 권한 선택
echo   - 토큰 복사
echo.
echo 아래에서 토큰 입력을 요청하면 붙여넣으세요.
echo.
pause

venv\Scripts\python.exe upload_to_space.py

echo.
pause
