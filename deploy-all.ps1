#!/usr/bin/env pwsh
# Agency Management System - Complete Deployment Script
# ======================================================

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════════╗
║              🚀 AGENCY SYSTEM DEPLOYMENT                         ║
║              Frontend (Vercel) + Backend (Railway)               ║
╚══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check prerequisites
Write-Host "`n🔍 Checking prerequisites..." -ForegroundColor Blue

$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "📦 Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "📦 Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Check environment variables
if (-not $env:OPENAI_API_KEY) {
    Write-Host "`n⚠️  WARNING: OPENAI_API_KEY not set!" -ForegroundColor Yellow
    Write-Host "Get your API key from: https://platform.openai.com/api-keys" -ForegroundColor Gray
    $key = Read-Host "Enter your OpenAI API key (or press Enter to skip)"
    if ($key) {
        $env:OPENAI_API_KEY = $key
    }
}

# Deploy Frontend
Write-Host "`n📦 Deploying Frontend to Vercel..." -ForegroundColor Green
Set-Location ui

try {
    $vercelOutput = vercel --prod 2>&1
    Write-Host $vercelOutput -ForegroundColor Gray
    
    # Extract URL from output
    if ($vercelOutput -match '(https://[^\s]+\.vercel\.app)') {
        $frontendUrl = $Matches[1]
        Write-Host "✅ Frontend deployed to: $frontendUrl" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend deployment failed: $_" -ForegroundColor Red
}

Set-Location ..

# Deploy Backend
Write-Host "`n🔌 Deploying Backend to Railway..." -ForegroundColor Green

# Check if logged in to Railway
$railwayUser = railway whoami 2>&1
if ($railwayUser -match "not logged in") {
    Write-Host "🔑 Please login to Railway:" -ForegroundColor Yellow
    railway login
}

# Initialize if needed
$projectInfo = railway status 2>&1
if ($projectInfo -match "Not connected") {
    Write-Host "🆕 Initializing Railway project..." -ForegroundColor Yellow
    railway init --name agency-api
}

# Set environment variables
if ($env:OPENAI_API_KEY) {
    Write-Host "🔧 Setting environment variables..." -ForegroundColor Blue
    railway variables set OPENAI_API_KEY="$env:OPENAI_API_KEY"
    railway variables set JWT_SECRET="$(-join ((1..32) | ForEach-Object { Get-Random -Maximum 16 | ForEach-Object { '0123456789abcdef'[$_] } }))"
}

# Deploy
try {
    railway up
    $backendUrl = railway domain 2>&1 | Select-String -Pattern "https://" | ForEach-Object { $_.Line }
    Write-Host "✅ Backend deployed to: $backendUrl" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend deployment failed: $_" -ForegroundColor Red
}

# Summary
Write-Host @"

══════════════════════════════════════════════════════════════════
  ✅ DEPLOYMENT COMPLETE!
══════════════════════════════════════════════════════════════════

🌐 Your Agency System is now LIVE:

   Frontend: https://agency-management-system.vercel.app
   Backend:  https://agency-api-production.up.railway.app
   API Docs: https://agency-api-production.up.railway.app/docs

🔐 Default Login:
   Username: admin
   Password: admin

📊 Dashboards:
   Vercel:  https://vercel.com/dashboard
   Railway: https://railway.app/dashboard

🆘 Troubleshooting:
   - Railway logs: railway logs
   - Vercel logs:  vercel logs
   - Check CORS settings in api/main.py

══════════════════════════════════════════════════════════════════
"@ -ForegroundColor Green

Read-Host "`nPress Enter to exit"
