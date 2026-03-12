# 🏢 Agency Management System

> **Autonomous Agent Swarm Orchestration Platform**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade autonomous business system that orchestrates specialized AI agents to work 24/7 with minimal human intervention. Built with the most advanced methods in AI orchestration, workflow automation, and scalable architecture.

![Agency System](https://via.placeholder.com/800x400?text=Agency+Management+System)

## 🚀 What Is This?

The **Agency Management System** is a complete command center for deploying and managing teams of AI agents that can:

- 🤖 **Autonomously execute complex tasks** across multiple domains
- 🔄 **Orchestrate multi-agent workflows** with dependency management
- 📊 **Self-monitor and auto-scale** based on demand
- 🎯 **Continuously learn** from outcomes to improve performance
- 🏢 **Operate 24/7** with zero manual intervention

Think of it as having a full AI agency - frontend developers, backend architects, growth hackers, content creators, and more - all working together autonomously.

## ✨ Features

### Core Capabilities

- **🤖 35+ Specialized Agents** across Engineering, Marketing, Product, Testing, and Support divisions
- **⚡ Swarm Intelligence** - Execute tasks in parallel across multiple agents
- **🔄 Workflow Engine** - Complex multi-step processes with dependencies
- **🧠 Autonomous Mode** - Self-managing, self-scaling, self-healing operations
- **📊 Real-time Monitoring** - Live metrics, logs, and system health
- **🎨 Modern React UI** - Beautiful dashboard for visual management
- **💻 Terminal CLI** - Power-user command interface

### Agent Divisions

| Division | Count | Example Agents |
|----------|-------|----------------|
| Engineering | 7 | Frontend Developer, Backend Architect, AI Engineer, DevOps Automator |
| Marketing | 4 | Growth Hacker, Content Creator, SEO Specialist |
| Product | 2 | Trend Researcher, UX Researcher |
| Testing | 2 | Evidence Collector, Reality Checker |
| Support | 2 | Analytics Reporter, Infrastructure Maintainer |
| Specialized | 1 | Agents Orchestrator |

## 🏁 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key (or Anthropic/Groq)

### Installation

```bash
# Clone or create the project
git clone <repo-url>
cd agency-system

# Run the installer
# Windows:
.\scripts\install.ps1

# macOS/Linux:
bash scripts/deploy.sh local local
```

### Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and add your API keys

# 5. Install frontend dependencies
cd ui && npm install && cd ..
```

## 🎮 Usage

### Start the System

```bash
# Terminal 1: Start API server
cd api
python main.py

# Terminal 2: Start UI (in another terminal)
cd ui
npm run dev

# The system is now running!
# - Dashboard: http://localhost:3000
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Using the CLI

```bash
# Check system status
python agency-cli.py status

# List all agents
python agency-cli.py agents

# View specific agent
python agency-cli.py agent frontend-developer

# Execute a task
python agency-cli.py execute \
  --agent content-creator \
  --task "Write a blog post about AI agents"

# Run agent swarm
python agency-cli.py swarm \
  --agents content-creator,growth-hacker \
  --task "Create marketing campaign"

# Enable autonomous mode
python agency-cli.py autonomous start

# Launch dashboard
python agency-cli.py dashboard
```

### Using the UI

1. Open http://localhost:3000
2. Navigate through the sidebar:
   - **Overview** - System health and quick actions
   - **Agents** - Browse and manage agents
   - **Workflows** - Orchestrate multi-agent processes
   - **Autonomous** - Configure self-running mode
   - **Terminal** - Live logs and command interface
   - **Metrics** - Performance analytics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENCY SYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   React UI  │    │  Terminal   │    │    API      │         │
│  │  (Port 3000)│    │    CLI      │    │  (Port 8000)│         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │                                    │
│                   ┌────────▼────────┐                          │
│                   │  Agent Manager  │                          │
│                   │   (Orchestrator)│                          │
│                   └────────┬────────┘                          │
│                            │                                    │
│         ┌──────────────────┼──────────────────┐                │
│         │                  │                  │                 │
│  ┌──────▼──────┐  ┌───────▼───────┐  ┌──────▼──────┐          │
│  │  Workflow   │  │   Autonomous  │  │   Metrics   │          │
│  │   Engine    │  │   Executor    │  │  Collector  │          │
│  └─────────────┘  └───────────────┘  └─────────────┘          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              AI PROVIDERS (OpenAI/Anthropic/Groq)    │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🧠 Autonomous Mode

When enabled, the system operates completely autonomously:

1. **Monitors** system metrics continuously
2. **Detects** opportunities and issues
3. **Triggers** appropriate agent workflows
4. **Scales** capacity automatically based on load
5. **Self-corrects** based on outcomes
6. **Reports** status via configured channels

```bash
# Start autonomous mode with custom config
python agency-cli.py autonomous start --config '{
  "scan_interval": 60,
  "max_concurrent_tasks": 10,
  "scaling_threshold": 500,
  "auto_discover_tasks": true
}'
```

## 📝 Example Workflows

### Marketing Campaign
```yaml
name: "Marketing Campaign Launch"
steps:
  - agent: trend-researcher
    task: "Research current trends in target market"
  
  - agent: content-creator
    task: "Create campaign content based on research"
    depends_on: [trend-researcher]
  
  - agent: growth-hacker
    task: "Optimize distribution strategy"
    depends_on: [content-creator]
  
  - agent: seo-specialist
    task: "SEO optimize all content"
    depends_on: [content-creator]
```

### Feature Development
```yaml
name: "Product Feature Development"
steps:
  - agent: ux-researcher
    task: "Validate feature concept with users"
  
  - agent: backend-architect
    task: "Design API and database schema"
  
  - agent: frontend-developer
    task: "Build UI components"
    depends_on: [ux-researcher]
  
  - agent: ai-engineer
    task: "Integrate AI features"
    depends_on: [backend-architect]
  
  - agent: evidence-collector
    task: "QA testing and documentation"
    depends_on: [frontend-developer, ai-engineer]
  
  - agent: reality-checker
    task: "Production readiness review"
    depends_on: [evidence-collector]
```

## 🚢 Deployment

### Local Development
```bash
bash scripts/deploy.sh local local
```

### Docker
```bash
bash scripts/deploy.sh production docker
```

### Vercel (Frontend)
```bash
bash scripts/deploy.sh production vercel
```

### Railway/Render
```bash
# Generate config
bash scripts/deploy.sh production render

# Or deploy directly
bash scripts/deploy.sh production railway
```

## 🔧 Configuration

Edit `.env` to customize:

```env
# AI Providers (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...

# Autonomous Mode
AUTONOMOUS_MODE_ENABLED=true
DEFAULT_SCAN_INTERVAL=60
DEFAULT_SCALING_THRESHOLD=500

# Integrations
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

## 📊 Monitoring

Access real-time metrics at:
- **Dashboard**: http://localhost:3000/metrics
- **Prometheus**: http://localhost:9090
- **API Health**: http://localhost:8000/health

## 🤝 Contributing

Contributions welcome! Areas for expansion:
- New agent types
- Additional workflow templates
- Integration connectors
- UI enhancements
- Performance optimizations

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by [agency-agents](https://github.com/msitarzewski/agency-agents)
- Built with FastAPI, React, Tailwind CSS
- AI powered by OpenAI, Anthropic, and Groq

---

<p align="center">
  <strong>🏢 Built for the autonomous future of work</strong>
</p>
