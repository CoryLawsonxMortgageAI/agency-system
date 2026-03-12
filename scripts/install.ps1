# Agency Management System - Windows Installation Script
# ======================================================

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════════╗
║              🏢 AGENCY MANAGEMENT SYSTEM INSTALLER              ║
║                   Autonomous Agent Platform                      ║
╚══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "Environment Check..." -ForegroundColor Blue

# Check Python
$pythonVersion = python --version 2>$null
if (-not $pythonVersion) {
    Write-Host "❌ Python is not installed. Please install Python 3.9+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green

# Check Node.js
$nodeVersion = node --version 2>$null
if (-not $nodeVersion) {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+ from nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠ Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠ Please edit .env and add your API keys" -ForegroundColor Yellow
}

# Setup Python environment
Write-Host "`nSetting up Python environment..." -ForegroundColor Blue

if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate and install
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "✓ Python dependencies installed" -ForegroundColor Green

# Setup frontend
Write-Host "`nSetting up frontend..." -ForegroundColor Blue

Set-Location ui
npm install
Set-Location ..

Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

# Create start script
$startScript = @'
@echo off
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
'@

$startScript | Out-File -FilePath "start.bat" -Encoding ASCII

Write-Host @"

══════════════════════════════════════════════════════════════
  ✅ Installation Complete!
══════════════════════════════════════════════════════════════

To start the Agency Management System:

  1. Run: .\start.bat
  
  Or manually:
  - Terminal 1: .\venv\Scripts\Activate.ps1
                cd api
                python main.py
  
  - Terminal 2: cd ui
                npm run dev

Access points:
  - Dashboard: http://localhost:3000
  - API:       http://localhost:8000
  - Docs:      http://localhost:8000/docs

Default Login:
  Username: admin
  Password: admin

CLI Usage:
  python agency-cli.py status
  python agency-cli.py agents
  python agency-cli.py --help

══════════════════════════════════════════════════════════════
"@ -ForegroundColor Green

Read-Host "Press Enter to continue"
