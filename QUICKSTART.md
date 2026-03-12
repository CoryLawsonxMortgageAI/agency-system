# 🚀 Agency Management System - Production Quickstart

## Immediate Start (Production Ready)

### Option 1: One-Command Start (Recommended)

```powershell
# Windows PowerShell (as Administrator)
cd "C:\Users\GFI CLawson\agency-system"
.\start.ps1
```

Or using batch file:
```cmd
# Windows Command Prompt
cd "C:\Users\GFI CLawson\agency-system"
start.bat
```

This will:
1. ✅ Check/install dependencies
2. ✅ Start API Server (port 8000)
3. ✅ Start UI Server (port 3000)
4. ✅ Open browser automatically
5. ✅ Show live logs

### Option 2: Manual Start (More Control)

**Terminal 1 - API Server:**
```powershell
cd "C:\Users\GFI CLawson\agency-system"
.\venv\Scripts\Activate.ps1
cd api
python main.py
```

**Terminal 2 - UI Server:**
```powershell
cd "C:\Users\GFI CLawson\agency-system\ui"
npm run dev
```

**Terminal 3 - CLI Commands:**
```powershell
cd "C:\Users\GFI CLawson\agency-system"
.\venv\Scripts\Activate.ps1
python agency-cli.py status
```

---

## 🔑 First-Time Setup (Required)

### 1. Create Environment File

```powershell
cd "C:\Users\GFI CLawson\agency-system"
copy .env.example .env
```

### 2. Add Your API Key

Edit `.env` and add at least one AI provider:

```env
# OpenAI (Recommended)
OPENAI_API_KEY=sk-your-key-here

# Or Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or Groq
GROQ_API_KEY=gsk-your-key-here
```

Get keys from:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Groq: https://console.groq.com/

---

## 🌐 Access Points

Once running, access your Agency System at:

| Service | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3000 | Main UI interface |
| **API** | http://localhost:8000 | REST API endpoint |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger docs |
| **Health** | http://localhost:8000/health | System health check |

---

## 🎮 Immediate Usage

### Using the Web Dashboard

1. Open http://localhost:3000
2. Navigate to **Agents** to see 35+ specialized AI agents
3. Click any agent to view details
4. Go to **Autonomous** tab to enable 24/7 operation
5. Check **Terminal** tab for live logs

### Using the CLI

```bash
# Check system status
python agency-cli.py status

# List all agents
python agency-cli.py agents

# View specific agent details
python agency-cli.py agent frontend-developer

# Execute a task with an agent
python agency-cli.py execute -a content-creator -t "Write a blog post about AI agents"

# Run multiple agents in parallel (swarm)
python agency-cli.py swarm --agents content-creator,growth-hacker -t "Create marketing campaign"

# Enable autonomous mode
python agency-cli.py autonomous start

# View help
python agency-cli.py --help
```

---

## 🤖 Available Agents (35 Total)

### Engineering Division (7 agents)
- **Frontend Developer** - React/Vue/Angular expert
- **Backend Architect** - API design & databases
- **AI Engineer** - LLM integration & ML
- **DevOps Automator** - CI/CD & infrastructure
- **Senior Developer** - Code review & architecture
- **Rapid Prototyper** - MVP & proof-of-concepts
- **Security Engineer** - Security audits & hardening

### Marketing Division (4 agents)
- **Growth Hacker** - User acquisition & viral loops
- **Content Creator** - Blog posts, social media, copy
- **SEO Specialist** - Search optimization

### Product Division (2 agents)
- **Trend Researcher** - Market intelligence
- **UX Researcher** - User research & testing

### Testing Division (2 agents)
- **Evidence Collector** - QA & bug documentation
- **Reality Checker** - Production readiness

### Support Division (2 agents)
- **Analytics Reporter** - Dashboards & metrics
- **Infrastructure Maintainer** - System reliability

### Specialized (1 agent)
- **Agents Orchestrator** - Multi-agent coordination

---

## ⚡ Autonomous Mode

Enable 24/7 autonomous operation:

```bash
# Start autonomous mode
python agency-cli.py autonomous start

# Check autonomous status
python agency-cli.py autonomous status

# Stop autonomous mode
python agency-cli.py autonomous stop
```

When enabled, the system will:
- Monitor metrics every 60 seconds
- Auto-scale agents when queue depth > 500
- Self-correct based on outcomes
- Trigger workflows based on conditions

---

## 🔧 Troubleshooting

### Port Already in Use
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Missing Dependencies
```powershell
# Reinstall Python dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Reinstall Node dependencies
cd ui
npm install
```

### API Key Issues
- Check `.env` file exists
- Verify API key is valid
- Try a different provider (OpenAI/Anthropic/Groq)

### CORS Errors
The API allows all origins in development. For production, edit:
```python
# api/main.py
allow_origins=["https://yourdomain.com"]  # Replace * with your domain
```

---

## 📁 Project Structure

```
agency-system/
├── 📁 api/                    # Python FastAPI Backend
│   ├── 📁 core/              # Agent Manager, Workflow Engine
│   ├── 📁 agents/            # 35+ Agent Definitions
│   ├── 📁 models/            # Pydantic Schemas
│   └── main.py               # API Server
│
├── 📁 ui/                     # React + TypeScript Frontend
│   ├── 📁 src/components/    # Dashboard, Agents, Workflows
│   └── package.json
│
├── agency-cli.py             # Terminal Command Interface
├── start.ps1                 # PowerShell startup script
├── start.bat                 # Batch startup script
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

---

## 🚢 Production Deployment

### Deploy to Vercel (Frontend)
```bash
npm install -g vercel
cd ui
vercel --prod
```

### Deploy to Railway (Full Stack)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Deploy to Render
```bash
# Generate render.yaml
bash scripts/deploy.sh production render

# Push to GitHub and connect to Render
```

---

## 📊 System Status

Check if everything is running:

```bash
# API health
curl http://localhost:8000/health

# Full status
python agency-cli.py status
```

Expected output:
```json
{
  "status": "healthy",
  "agents_loaded": 35,
  "active_agents": 0,
  "version": "1.0.0"
}
```

---

## 🆘 Support

**Issues?** Check:
1. All 3 terminals are running
2. `.env` file has valid API key
3. Ports 3000 and 8000 are available
4. Python 3.9+ and Node.js 18+ installed

**Still stuck?** Run the diagnostic:
```powershell
cd "C:\Users\GFI CLawson\agency-system\api"
python test_imports.py
```

---

## 🎉 You're Ready!

Your Agency Management System is now production-ready with:
- ✅ 35 specialized AI agents
- ✅ Autonomous operation mode
- ✅ Real-time web dashboard
- ✅ Terminal CLI interface
- ✅ Workflow orchestration
- ✅ Auto-scaling capabilities

**Start building:** http://localhost:3000
