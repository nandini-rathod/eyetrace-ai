@echo off
echo =====================================
echo  EyeTrace AI — Start Frontend
echo =====================================
cd /d "%~dp0frontend"
if not exist node_modules (
    echo [ERROR] node_modules not found. Run:
    echo   npm install
    pause
    exit /b 1
)
echo [..] Starting React dev server on http://localhost:5173
npm run dev
