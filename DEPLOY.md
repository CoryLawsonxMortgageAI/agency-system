# 🚀 Production Deployment Guide

## Quick Deploy (2 Minutes)

### Step 1: Deploy Frontend to Vercel

```powershell
# Navigate to UI folder
cd "C:\Users\GFI CLawson\agency-system\ui"

# Deploy to Vercel
npx vercel --prod
```

When prompted:
- **Link to existing project?** → No (create new)
- **Project name** → agency-management-system
- **Directory** → ./ (current)

**Expected Output:**
```
🔍  Inspect: https://vercel.com/yourname/agency-management-system/[id]
✅  Production: https://agency-management-system.vercel.app
```

---

### Step 2: Deploy Backend to Railway

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Go to project root
cd "C:\Users\GFI CLawson\agency-system"

# Initialize project
railway init --name agency-api

# Add environment variables
railway variables set OPENAI_API_KEY="sk-your-key-here"
railway variables set JWT_SECRET="your-super-secret-jwt-key"

# Deploy
railway up

# Get deployment URL
railway domain
```

**Expected Output:**
```
🚀 Deployed to https://agency-api-production.up.railway.app
```

---

### Step 3: Update Frontend with Backend URL

After getting your Railway URL, update the frontend:

```powershell
cd "C:\Users\GFI CLawson\agency-system\ui"

# Create .env.production
@"
VITE_API_URL=https://agency-api-production.up.railway.app
"@ | Out-File -FilePath .env.production -Encoding utf8

# Redeploy
npx vercel --prod
```

---

## 📋 Alternative: Deploy to Render

If Railway doesn't work, use Render:

### 1. Push to GitHub First

```powershell
cd "C:\Users\GFI CLawson\agency-system"
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/agency-system.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to https://dashboard.render.com/
2. Click **New +** → **Blueprint**
3. Connect your GitHub repo
4. Render will use `render.yaml` automatically
5. Add environment variables in dashboard:
   - `OPENAI_API_KEY`
   - `JWT_SECRET`

**URLs will be:**
- API: `https://agency-api.onrender.com`
- UI: `https://agency-ui.onrender.com`

---

## ✅ Verify Deployment

### Test Backend Health
```bash
curl https://agency-api-production.up.railway.app/health

# Expected:
{"status":"healthy","agents_loaded":35}
```

### Test Login API
```bash
curl -X POST https://agency-api-production.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Expected:
{"access_token":"...","token_type":"bearer","expires_in":86400}
```

### Open Frontend
Navigate to your Vercel URL:
```
https://agency-management-system.vercel.app
```

Login with:
- Username: `admin`
- Password: `admin`

---

## 🔧 Post-Deployment Configuration

### Update CORS (Required!)

Edit `api/main.py` and update CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agency-management-system.vercel.app",  # Your Vercel URL
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy backend:
```powershell
railway up
```

---

## 📊 Monitoring

### Railway Dashboard
```
https://railway.app/project/[your-project-id]
```

### Vercel Dashboard
```
https://vercel.com/dashboard
```

### View Logs
```powershell
# Railway logs
railway logs

# Vercel logs
npx vercel logs
```

---

## 🆘 Troubleshooting

### CORS Errors
Make sure your Vercel URL is in the CORS allow_origins list in `api/main.py`

### 500 Errors
Check Railway logs:
```powershell
railway logs
```

### Missing Environment Variables
```powershell
railway variables
railway variables set KEY="value"
```

### Frontend Can't Connect to Backend
1. Check `VITE_API_URL` in Vercel environment variables
2. Verify backend is running: `curl [backend-url]/health`
3. Check browser console for CORS errors

---

## 🌐 Your Deployed URLs

After deployment, you'll have:

| Component | URL Example | Status |
|-----------|-------------|--------|
| Frontend | `https://agency-system.vercel.app` | ✅ Vercel |
| Backend API | `https://agency-api.up.railway.app` | ✅ Railway |
| API Docs | `https://agency-api.up.railway.app/docs` | ✅ Swagger |

---

## 🎯 One-Click Deploy Scripts

### Windows (PowerShell)
```powershell
# deploy-all.ps1
Write-Host "🚀 Deploying Agency System..." -ForegroundColor Cyan

cd ui
Write-Host "📦 Deploying Frontend to Vercel..." -ForegroundColor Green
npx vercel --prod

cd ..
Write-Host "🔌 Deploying Backend to Railway..." -ForegroundColor Green
railway up

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
```

### macOS/Linux (Bash)
```bash
#!/bin/bash
echo "🚀 Deploying Agency System..."

cd ui
echo "📦 Deploying Frontend to Vercel..."
vercel --prod

cd ..
echo "🔌 Deploying Backend to Railway..."
railway up

echo "✅ Deployment Complete!"
```

---

## 📝 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for AI agents |
| `JWT_SECRET` | ✅ Yes | Secret for JWT tokens |
| `ANTHROPIC_API_KEY` | ❌ No | Alternative AI provider |
| `GROQ_API_KEY` | ❌ No | Alternative AI provider |

---

## 🎉 Success!

Once deployed, your Agency Management System will be:
- ✅ Accessible from anywhere in the world
- ✅ Running 24/7 on cloud infrastructure
- ✅ Auto-scaling based on demand
- ✅ Secured with JWT authentication

**Start using your deployed system:**
```
https://agency-management-system.vercel.app
```
