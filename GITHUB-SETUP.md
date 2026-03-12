# 📦 Push to GitHub & Deploy

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `agency-system`
3. **Description:** `Autonomous AI Agent Swarm Platform`
4. **Make it:** Public (or Private)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

You'll see a page with instructions like:
```
git remote add origin https://github.com/YOUR_USERNAME/agency-system.git
```

---

## Step 2: Push Your Code to GitHub

### Option A: Run These Commands (Copy & Paste)

Open PowerShell in your project folder:

```powershell
cd "C:\Users\GFI CLawson\agency-system"

# Set your GitHub username
$env:GIT_USERNAME = "YOUR_GITHUB_USERNAME"

# Add the remote repository
git remote add origin "https://github.com/$env:GIT_USERNAME/agency-system.git"

# Stage all files
git add .

# Commit
git commit -m "Initial production deployment"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Step by Step

```powershell
# 1. Go to your project
cd "C:\Users\GFI CLawson\agency-system"

# 2. Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/agency-system.git

# 3. Add all files
git add .

# 4. Commit
git commit -m "Production ready"

# 5. Push
git branch -M main
git push -u origin main
```

---

## Step 3: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/agency-system
2. You should see all your files:
   - `api/` folder
   - `ui/` folder
   - `Dockerfile`
   - `render.yaml`
   - etc.

---

## Step 4: Deploy to Render

### Connect GitHub to Render:

1. Go to https://dashboard.render.com/
2. Sign up / Log in with **GitHub**
3. Click **"New +"** → **"Blueprint"**
4. You'll see your GitHub repos - select **agency-system**
5. Click **"Connect"**

### Configure Environment Variables:

In the Render dashboard, add these:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
JWT_SECRET=any-random-secret-string-here
```

### Deploy:

Click **"Apply"** or **"Deploy"**

Render will:
- Read the `render.yaml` file
- Build the Python backend
- Deploy to a public URL

**Your backend URL will be:** `https://agency-api.onrender.com`

---

## 🔗 Your Final URLs

| Service | URL |
|---------|-----|
| **Frontend** | https://agency-management-system-chi.vercel.app (already live!) |
| **Backend** | https://agency-api.onrender.com (after deploy) |
| **GitHub Repo** | https://github.com/YOUR_USERNAME/agency-system |

---

## 🆘 Troubleshooting

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/agency-system.git
```

### "failed to push"
```powershell
git pull origin main --rebase
git push origin main
```

### "nothing to commit"
```powershell
git add -A
git commit -m "Update files"
git push origin main
```

### Files too large
The `node_modules` folder is excluded via `.gitignore`, so this shouldn't happen.

---

## 🎯 Quick Checklist

- [ ] Created GitHub repo at https://github.com/new
- [ ] Ran `git remote add origin` with your username
- [ ] Ran `git push -u origin main`
- [ ] Code visible on GitHub
- [ ] Connected to Render
- [ ] Added environment variables
- [ ] Deployed backend

---

## 📹 Alternative: Video Guide

If you prefer video:
1. Create repo: https://www.youtube.com/watch?v=iv8rSLsi1xo
2. Push code: https://www.youtube.com/watch?v=eL_0Ok_Gkas
3. Deploy to Render: https://www.youtube.com/watch?v=7-L2bE4N8Lk

---

## 🚀 After Deployment

Once backend is live:

1. Test login at: https://agency-api.onrender.com/api/v1/auth/login
2. Frontend will auto-connect
3. Your 35 AI agents are ready!

**Need help? Send me any error messages!**
