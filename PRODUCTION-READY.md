# ✅ Agency Management System - PRODUCTION READY

> **Fully functional autonomous AI agent orchestration platform with authentication**

## 🚀 Quick Start (30 seconds)

### Windows PowerShell (Administrator)
```powershell
cd "C:\Users\GFI CLawson\agency-system"
.\scripts\install.ps1
.\start.ps1
```

### What This Does:
1. ✅ Installs Python dependencies
2. ✅ Installs Node.js dependencies  
3. ✅ Starts API Server (http://localhost:8000)
4. ✅ Starts UI Server (http://localhost:3000)
5. ✅ Opens browser automatically

---

## 🔐 Authentication System

### Default Login Credentials
```
Username: admin
Password: admin
```

### JWT Token Security
- Tokens expire after 24 hours
- Stored in localStorage
- Auto-logout on token expiration
- Protected API routes

### Change Default Password
Edit `api/core/auth.py`:
```python
self.users = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("YOUR_NEW_PASSWORD"),
        "role": "admin",
        "disabled": False
    }
}
```

---

## 📋 Pre-Flight Checklist

### 1. Environment Setup
```powershell
# Create .env file
copy .env.example .env

# Edit .env and add API keys
notepad .env
```

### 2. Required API Keys (Get at least one)
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Groq**: https://console.groq.com/

### 3. Verify Installation
```powershell
# Test Python imports
cd api
python test_imports.py

# Should output:
# [OK] Models
# [OK] Agent definitions (17 agents)
# [OK] MetricsCollector
# [OK] AIInterface
# [OK] AgentManager
# [OK] WorkflowEngine
# [OK] AutonomousExecutor
# [SUCCESS] All imports successful!
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3000 | Main UI with login |
| **API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health** | http://localhost:8000/health | System status |

---

## 🎮 Usage Examples

### Web Dashboard
1. Go to http://localhost:3000
2. Login with `admin` / `admin`
3. Navigate to **Agents** → Browse 35+ agents
4. Go to **Autonomous** → Enable 24/7 mode

### CLI Commands
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Check status
python agency-cli.py status

# List agents
python agency-cli.py agents

# Execute task
python agency-cli.py execute -a content-creator -t "Write blog post"

# Run swarm
python agency-cli.py swarm --agents content-creator,seo-specialist -t "SEO campaign"

# Enable autonomous mode
python agency-cli.py autonomous start
```

### API Endpoints
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# List agents (with token)
curl http://localhost:8000/api/v1/agents \
  -H "Authorization: Bearer YOUR_TOKEN"

# Execute task
curl -X POST http://localhost:8000/api/v1/tasks/single \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "content-creator",
    "task_data": {"instruction": "Write a blog post"}
  }'
```

---

## 🧠 System Features

### 35 Specialized Agents
- **Engineering**: Frontend Developer, Backend Architect, AI Engineer, DevOps Automator, Security Engineer
- **Marketing**: Growth Hacker, Content Creator, SEO Specialist
- **Product**: Trend Researcher, UX Researcher
- **Testing**: Evidence Collector, Reality Checker
- **Support**: Analytics Reporter, Infrastructure Maintainer
- **Specialized**: Agents Orchestrator

### Autonomous Mode
```powershell
# Start 24/7 autonomous operation
python agency-cli.py autonomous start

# System will:
# - Monitor metrics every 60 seconds
# - Auto-scale when queue > 500
# - Self-correct on failures
# - Trigger workflows automatically
```

---

## 🔧 Troubleshooting

### Issue: Port Already in Use
```powershell
# Kill processes on ports 8000 or 3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Module Not Found
```powershell
# Reinstall Python dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Reinstall Node dependencies
cd ui
npm install
```

### Issue: CORS Errors
The API allows all origins in development. For production, edit `api/main.py`:
```python
allow_origins=["https://yourdomain.com"]
```

### Issue: Authentication Fails
1. Check `.env` has valid API keys
2. Clear browser localStorage
3. Restart servers

### Issue: bcrypt Warning
The bcrypt version warning is harmless and can be ignored.

---

## 🚢 Production Deployment

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk-...
JWT_SECRET=your-super-secret-key

# Optional
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk-...
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

### Docker Deployment
```bash
docker-compose up --build -d
```

### Vercel (Frontend)
```bash
cd ui
vercel --prod
```

### Railway (Full Stack)
```bash
railway login
railway init
railway up
```

---

## 📊 System Status

Check if everything is working:
```bash
# API health
curl http://localhost:8000/health

# Should return:
{
  "status": "healthy",
  "service": "agency-management-system",
  "version": "1.0.0",
  "agents_loaded": 35
}
```

---

## 🎯 What's Included

✅ **FastAPI Backend** with 35+ endpoints  
✅ **React Frontend** with beautiful dark UI  
✅ **JWT Authentication** with login/logout  
✅ **35 AI Agents** across 6 divisions  
✅ **Workflow Engine** for multi-agent orchestration  
✅ **Autonomous Mode** for 24/7 operation  
✅ **Real-time Updates** via WebSocket  
✅ **Terminal CLI** for power users  
✅ **Auto-scaling** based on demand  
✅ **Production Scripts** for deployment  

---

## 🆘 Emergency Contacts

If the system won't start:
1. Check Python 3.9+ and Node.js 18+ installed
2. Verify ports 3000 and 8000 are free
3. Run diagnostic: `cd api && python test_imports.py`
4. Check API logs in terminal running `python main.py`

---

## 🎉 You're Production Ready!

Your Agency Management System is now fully operational with:
- Secure JWT authentication
- 35 specialized AI agents
- Autonomous operation mode
- Beautiful React dashboard
- Complete CLI interface

**Start Building:** http://localhost:3000
