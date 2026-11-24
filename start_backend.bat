@echo off
echo =====================================
echo  EyeTrace AI — Start Backend
echo =====================================
cd /d "%~dp0backend"
if not exist venv (
    echo [ERROR] Virtual environment not found. Run:
    echo   python -m venv venv
    echo   venv\Scripts\pip.exe install -r requirements.txt
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo [..] Starting FastAPI backend on http://127.0.0.1:8000
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
