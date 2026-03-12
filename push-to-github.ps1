#!/usr/bin/env pwsh
# Push Agency System to GitHub
# ============================

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════════╗
║              📦 PUSH TO GITHUB & DEPLOY                          ║
║         Step-by-step guide to get your code on GitHub            ║
╚══════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if git is configured
$gitUser = git config user.name 2>$null
$gitEmail = git config user.email 2>$null

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "`n⚠️  Git not configured!" -ForegroundColor Yellow
    Write-Host "Run these commands first:" -ForegroundColor White
    Write-Host '  git config --global user.name "Your Name"' -ForegroundColor Gray
    Write-Host '  git config --global user.email "your@email.com"' -ForegroundColor Gray
    exit 1
}

Write-Host "`n👤 Git configured for: $gitUser ($gitEmail)" -ForegroundColor Green

# Get GitHub username
$githubUsername = Read-Host "`nEnter your GitHub username"

if (-not $githubUsername) {
    Write-Host "❌ GitHub username required!" -ForegroundColor Red
    exit 1
}

# Check if repo exists on GitHub
Write-Host "`n🔍 Checking GitHub repository..." -ForegroundColor Blue
Write-Host "Make sure you've created: https://github.com/$githubUsername/agency-system" -ForegroundColor Yellow
Write-Host "(Press Enter if you've created it, or Ctrl+C to cancel)"
Read-Host

# Navigate to project
cd "C:\Users\GFI CLawson\agency-system"

# Check if remote already exists
$remoteExists = git remote -v 2>$null | Select-String "origin"

if ($remoteExists) {
    Write-Host "`n⚠️  Remote already exists, updating..." -ForegroundColor Yellow
    git remote remove origin
}

# Add remote
Write-Host "`n🔗 Adding GitHub remote..." -ForegroundColor Blue
try {
    git remote add origin "https://github.com/$githubUsername/agency-system.git"
    Write-Host "✅ Remote added" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to add remote: $_" -ForegroundColor Red
    exit 1
}

# Check git status
Write-Host "`n📊 Checking git status..." -ForegroundColor Blue
git status

# Add all files
Write-Host "`n📁 Adding files to git..." -ForegroundColor Blue
git add .

# Commit
Write-Host "`n💾 Committing changes..." -ForegroundColor Blue
try {
    git commit -m "Production deployment ready - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    Write-Host "✅ Committed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Nothing to commit or commit failed" -ForegroundColor Yellow
}

# Push
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Blue
try {
    git branch -M main
    git push -u origin main -f
    Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "❌ Push failed: $_" -ForegroundColor Red
    Write-Host "`nTry running these commands manually:" -ForegroundColor Yellow
    Write-Host "  git pull origin main --rebase" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
    exit 1
}

# Success message
Write-Host @"

══════════════════════════════════════════════════════════════════
  ✅ SUCCESS! Code pushed to GitHub!
══════════════════════════════════════════════════════════════════

🌐 Your Repository:
   https://github.com/$githubUsername/agency-system

📋 Next Steps:
   1. Visit your repo URL above to verify
   2. Go to https://dashboard.render.com/
   3. Click "New +" → "Blueprint"
   4. Select "agency-system" repo
   5. Add environment variables:
      - OPENAI_API_KEY=sk-your-key-here
      - JWT_SECRET=your-secret
   6. Click "Apply" to deploy!

🔗 After Deploy:
   Backend URL: https://agency-api.onrender.com
   Frontend:    https://agency-management-system-chi.vercel.app

══════════════════════════════════════════════════════════════════
"@ -ForegroundColor Green

# Ask to open browser
$openBrowser = Read-Host "`nOpen GitHub repo in browser? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "https://github.com/$githubUsername/agency-system"
}

Read-Host "`nPress Enter to exit"
