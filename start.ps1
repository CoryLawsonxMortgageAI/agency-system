#!/usr/bin/env pwsh
# Agency Management System - Production Startup Script
# =====================================================

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════════╗
║              🏢 AGENCY MANAGEMENT SYSTEM                         ║
║                   Starting Production Server                     ║
╚══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Running installer..." -ForegroundColor Red
    & ".\scripts\install.ps1"
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Function to check if a port is in use
function Test-PortInUse {
    param($Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $connection
}

# Check ports
if (Test-PortInUse -Port 8000) {
    Write-Host "⚠️  Port 8000 is already in use. API may already be running." -ForegroundColor Yellow
}
if (Test-PortInUse -Port 3000) {
    Write-Host "⚠️  Port 3000 is already in use. UI may already be running." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Starting API Server..." -ForegroundColor Green
$apiJob = Start-Job -ScriptBlock {
    Set-Location "$using:PWD\api"
    python main.py
}

Write-Host "⏳ Waiting for API to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if API is responding
$apiReady = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2
        if ($response.status -eq "healthy") {
            $apiReady = $true
            break
        }
    } catch {}
    Start-Sleep -Seconds 1
}

if ($apiReady) {
    Write-Host "✅ API Server is ready!" -ForegroundColor Green
} else {
    Write-Host "⚠️  API Server may not be ready yet. Check logs." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎨 Starting UI Server..." -ForegroundColor Green
$uiJob = Start-Job -ScriptBlock {
    Set-Location "$using:PWD\ui"
    npm run dev
}

Write-Host "⏳ Waiting for UI to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ Agency System Started!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  📱 Dashboard: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  🔌 API:       http://localhost:8000" -ForegroundColor Cyan
Write-Host "  📚 Docs:      http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  💻 CLI Commands:" -ForegroundColor White
Write-Host "     python agency-cli.py status" -ForegroundColor Gray
Write-Host "     python agency-cli.py agents" -ForegroundColor Gray
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop all services..." -ForegroundColor Yellow
Write-Host ""

# Open browser
Start-Process "http://localhost:3000"

# Keep the script running and show logs
try {
    while ($true) {
        Receive-Job -Job $apiJob -Keep | ForEach-Object { Write-Host "[API] $_" -ForegroundColor Blue }
        Receive-Job -Job $uiJob -Keep | ForEach-Object { Write-Host "[UI] $_" -ForegroundColor Magenta }
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "🛑 Stopping services..." -ForegroundColor Red
    Stop-Job -Job $apiJob -ErrorAction SilentlyContinue
    Stop-Job -Job $uiJob -ErrorAction SilentlyContinue
    Remove-Job -Job $apiJob -ErrorAction SilentlyContinue
    Remove-Job -Job $uiJob -ErrorAction SilentlyContinue
    Write-Host "✅ Services stopped." -ForegroundColor Green
}
