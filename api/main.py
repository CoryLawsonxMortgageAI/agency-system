"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AGENCY MANAGEMENT SYSTEM - API SERVER                      ║
║                   Autonomous Agent Swarm Orchestration Platform               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Production-ready API for managing AI agent swarms.
"""

import asyncio
import json
import sys
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

# Add the api directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import auth
from core.auth import auth_manager, get_current_user, get_current_active_user

# Import core modules
try:
    from core.agent_manager import AgentManager
    from core.workflow_engine import WorkflowEngine
    from core.autonomous_executor import AutonomousExecutor
    from core.monitoring import MetricsCollector
    from models.schemas import (
        AgentConfig, WorkflowDefinition, TaskRequest, 
        ExecutionResult, SystemStatus, AgentStatus
    )
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    raise

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL STATE
# ═══════════════════════════════════════════════════════════════════════════════

agent_manager: Optional[AgentManager] = None
workflow_engine: Optional[WorkflowEngine] = None
autonomous_executor: Optional[AutonomousExecutor] = None
metrics_collector: Optional[MetricsCollector] = None


# ═══════════════════════════════════════════════════════════════════════════════
# LIFESPAN MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown."""
    global agent_manager, workflow_engine, autonomous_executor, metrics_collector
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AGENCY MANAGEMENT SYSTEM v1.0.0                            ║
║                   Autonomous Agent Swarm Orchestration Platform               ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Initialize core systems
        print("📦 Initializing core systems...")
        metrics_collector = MetricsCollector()
        agent_manager = AgentManager(metrics_collector)
        workflow_engine = WorkflowEngine(agent_manager, metrics_collector)
        autonomous_executor = AutonomousExecutor(workflow_engine, metrics_collector)
        
        # Load all agent definitions
        print("🤖 Loading agent definitions...")
        await agent_manager.load_agents()
        
        # Start autonomous execution loop
        print("🔄 Starting autonomous execution loop...")
        asyncio.create_task(autonomous_executor.run_execution_loop())
        
        print("✅ AGENCY SYSTEM READY")
        print(f"   🟢 {len(agent_manager.agents)} agents loaded")
        print(f"   🌐 API: http://0.0.0.0:8000")
        print(f"   📚 Docs: http://0.0.0.0:8000/docs")
        print("")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down Agency Management System...")
    try:
        if agent_manager:
            await agent_manager.shutdown()
        if workflow_engine:
            await workflow_engine.shutdown()
    except Exception as e:
        print(f"❌ Shutdown error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="🏢 Agency Management System",
    description="Autonomous Agent Swarm Orchestration Platform - Production API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allow deployed frontend and local development
origins = [
    "https://agency-management-system-chi.vercel.app",
    "https://agency-system.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "*"  # Allow all origins for testing (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET CONNECTION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token."""
    user = auth_manager.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_manager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_manager.create_access_token(
        data={"sub": user["username"], "role": user.get("role", "user")},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": auth_manager.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.get("/api/v1/auth/me")
async def get_me(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """Get current authenticated user info."""
    return {
        "username": current_user["username"],
        "role": current_user.get("role", "user"),
        "disabled": current_user.get("disabled", False)
    }


@app.post("/api/v1/auth/logout")
async def logout():
    """Logout (client should discard token)."""
    return {"message": "Successfully logged out"}


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - AGENT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/agents", response_model=List[Dict[str, Any]])
async def list_agents():
    """List all available agents with their configurations."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    agents = await agent_manager.list_agents()
    return [agent.dict() for agent in agents]


@app.get("/api/v1/agents/{agent_id}", response_model=Dict[str, Any])
async def get_agent(agent_id: str):
    """Get detailed information about a specific agent."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    agent = await agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return agent.dict()


@app.post("/api/v1/agents/{agent_id}/activate")
async def activate_agent(agent_id: str):
    """Activate an agent for immediate task execution."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    success = await agent_manager.activate_agent(agent_id)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to activate agent {agent_id}")
    
    await manager.broadcast({
        "type": "agent_activated",
        "agent_id": agent_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {"status": "activated", "agent_id": agent_id}


@app.post("/api/v1/agents/{agent_id}/deactivate")
async def deactivate_agent(agent_id: str):
    """Deactivate an agent."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    await agent_manager.deactivate_agent(agent_id)
    
    await manager.broadcast({
        "type": "agent_deactivated",
        "agent_id": agent_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {"status": "deactivated", "agent_id": agent_id}


@app.get("/api/v1/agents/{agent_id}/status")
async def get_agent_status(agent_id: str):
    """Get real-time status of an agent."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    status_obj = await agent_manager.get_agent_status(agent_id)
    if not status_obj:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return status_obj.dict()


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - TASK MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/tasks/single")
async def execute_single_task(task: Dict[str, Any]):
    """Execute a single task with a specific agent."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    result = await agent_manager.execute_task(
        agent_id=task.get("agent_id"),
        task_data=task.get("task_data", {}),
        context=task.get("context")
    )
    
    await manager.broadcast({
        "type": "task_completed",
        "agent_id": task.get("agent_id"),
        "task_id": result.task_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return result.dict()


@app.post("/api/v1/tasks/swarm")
async def execute_swarm(
    tasks: List[Dict[str, Any]],
    background_tasks: BackgroundTasks
):
    """Execute multiple tasks in parallel using agent swarm."""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    swarm_id = f"swarm_{datetime.utcnow().timestamp()}"
    
    # Convert dicts to proper format
    task_requests = []
    for t in tasks:
        task_requests.append({
            "agent_id": t.get("agent_id"),
            "task_data": t.get("task_data", {}),
            "context": t.get("context"),
            "priority": t.get("priority", 5)
        })
    
    # Start execution in background
    async def run_swarm():
        results = await agent_manager.execute_swarm(swarm_id, task_requests)
        return results
    
    background_tasks.add_task(run_swarm)
    
    await manager.broadcast({
        "type": "swarm_initiated",
        "swarm_id": swarm_id,
        "task_count": len(tasks),
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "swarm_id": swarm_id,
        "status": "initiated",
        "task_count": len(tasks)
    }


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - WORKFLOW MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/workflows")
async def list_workflows():
    """List all available workflow templates."""
    if not workflow_engine:
        return []
    workflows = await workflow_engine.list_workflows()
    return [wf.dict() for wf in workflows]


@app.post("/api/v1/workflows/execute")
async def execute_workflow(
    workflow_def: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Execute a workflow with multiple agents."""
    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")
    
    execution_id = await workflow_engine.create_execution(WorkflowDefinition(**workflow_def))
    
    # Start execution in background
    background_tasks.add_task(
        workflow_engine.run_workflow,
        execution_id,
        WorkflowDefinition(**workflow_def)
    )
    
    await manager.broadcast({
        "type": "workflow_started",
        "execution_id": execution_id,
        "workflow_name": workflow_def.get("name"),
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "execution_id": execution_id,
        "status": "started",
        "message": f"Workflow '{workflow_def.get('name')}' execution initiated"
    }


@app.get("/api/v1/workflows/execution/{execution_id}")
async def get_execution_status(execution_id: str):
    """Get status of a workflow execution."""
    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")
    status = await workflow_engine.get_execution_status(execution_id)
    if not status:
        raise HTTPException(status_code=404, detail="Execution not found")
    return status.dict()


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - AUTONOMOUS MODE
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/autonomous/start")
async def start_autonomous_mode(config: Dict[str, Any] = None):
    """Start autonomous execution mode with specified parameters."""
    if not autonomous_executor:
        raise HTTPException(status_code=503, detail="Autonomous executor not initialized")
    await autonomous_executor.start(config or {})
    
    await manager.broadcast({
        "type": "autonomous_mode_started",
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {"status": "autonomous_mode_active"}


@app.post("/api/v1/autonomous/stop")
async def stop_autonomous_mode():
    """Stop autonomous execution mode."""
    if not autonomous_executor:
        raise HTTPException(status_code=503, detail="Autonomous executor not initialized")
    await autonomous_executor.stop()
    
    await manager.broadcast({
        "type": "autonomous_mode_stopped",
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {"status": "autonomous_mode_stopped"}


@app.get("/api/v1/autonomous/status")
async def get_autonomous_status():
    """Get current autonomous execution status."""
    if not autonomous_executor:
        return {"enabled": False, "running": False}
    return await autonomous_executor.get_status()


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS - SYSTEM STATUS & METRICS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/system/status")
async def get_system_status():
    """Get overall system health and status."""
    try:
        active_agents = len(await agent_manager.get_active_agents()) if agent_manager else 0
        total_agents = len(await agent_manager.list_agents()) if agent_manager else 0
        active_workflows = await workflow_engine.get_active_count() if workflow_engine else 0
        queue_depth = await workflow_engine.get_queue_depth() if workflow_engine else 0
        
        return {
            "status": "healthy",
            "uptime": metrics_collector.get_uptime() if metrics_collector else 0,
            "active_agents": active_agents,
            "total_agents": total_agents,
            "active_workflows": active_workflows,
            "queue_depth": queue_depth,
            "metrics": await metrics_collector.get_current_metrics() if metrics_collector else {},
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.get("/api/v1/system/metrics")
async def get_metrics(time_range: str = "1h"):
    """Get system performance metrics."""
    if not metrics_collector:
        return {"error": "Metrics collector not initialized"}
    return await metrics_collector.get_metrics(time_range)


@app.get("/api/v1/system/logs")
async def get_logs(
    level: Optional[str] = None,
    agent_id: Optional[str] = None,
    limit: int = 100
):
    """Get system logs with optional filtering."""
    if not agent_manager:
        return []
    return await agent_manager.get_logs(level=level, agent_id=agent_id, limit=limit)


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Agency Management System",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("action") == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "agency-management-system",
        "version": "1.0.0",
        "agents_loaded": len(agent_manager.agents) if agent_manager else 0
    }


@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "name": "🏢 Agency Management System",
        "version": "1.0.0",
        "description": "Autonomous Agent Swarm Orchestration Platform",
        "docs": "/docs",
        "api_version": "v1",
        "status": "operational",
        "agents": len(agent_manager.agents) if agent_manager else 0
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
        workers=1
    )
