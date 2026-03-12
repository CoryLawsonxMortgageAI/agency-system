@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              🏢 AGENCY MANAGEMENT SYSTEM                         ║
echo ║                   Starting Production Server                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Running installer...
    powershell -ExecutionPolicy Bypass -File scripts\install.ps1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo 🚀 Starting API Server...
start "Agency API Server" cmd /k "cd api && python main.py"

echo ⏳ Waiting for API to start...
timeout /t 3 /nobreak >nul

echo 🎨 Starting UI Server...
start "Agency UI Server" cmd /k "cd ui && npm run dev"

echo ⏳ Waiting for UI to start...
timeout /t 5 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════════
echo  ✅ Agency System Started!
echo ════════════════════════════════════════════════════════════════
echo.
echo  📱 Dashboard: http://localhost:3000
echo  🔌 API:       http://localhost:8000
echo  📚 Docs:      http://localhost:8000/docs
echo.
echo  💻 CLI Commands:
echo     python agency-cli.py status
echo     python agency-cli.py agents
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Open browser
start http://localhost:3000

echo Press any key to stop all services...
pause >nul

echo.
echo 🛑 Stopping services...
taskkill /F /FI "WINDOWTITLE eq Agency API Server" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Agency UI Server" >nul 2>&1

echo ✅ Services stopped.
pause
