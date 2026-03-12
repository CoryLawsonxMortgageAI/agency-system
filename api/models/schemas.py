"""
Pydantic Models for Agency Management System
============================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class AgentStatusEnum(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class AgentCapability(BaseModel):
    """Defines what an agent can do."""
    name: str
    description: str
    skills: List[str]
    tools: List[str] = []


class AgentPersonality(BaseModel):
    """Agent personality and communication style."""
    name: str
    role: str
    tone: str = "professional"
    catchphrase: Optional[str] = None
    communication_style: str = "direct"
    expertise_areas: List[str] = []


class AgentConfig(BaseModel):
    """Complete agent configuration."""
    id: str
    name: str
    division: str
    personality: AgentPersonality
    capabilities: AgentCapability
    system_prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class AgentStatus(BaseModel):
    """Real-time agent status."""
    agent_id: str
    status: AgentStatusEnum
    current_task: Optional[str] = None
    queue_depth: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_response_time: float = 0.0
    last_active: Optional[datetime] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# TASK MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class TaskRequest(BaseModel):
    """Request to execute a task with an agent."""
    agent_id: str
    task_data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    priority: int = 5  # 1-10, higher = more urgent
    timeout: Optional[int] = 300  # seconds
    callback_url: Optional[str] = None


class TaskResult(BaseModel):
    """Result of a task execution."""
    task_id: str
    agent_id: str
    status: TaskStatus
    output: Any
    error: Optional[str] = None
    execution_time: float  # seconds
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class ExecutionResult(BaseModel):
    """Aggregated execution results."""
    execution_id: str
    tasks: List[TaskResult]
    overall_status: TaskStatus
    total_execution_time: float
    total_cost: float
    summary: str


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class WorkflowStep(BaseModel):
    """Single step in a workflow."""
    id: str
    name: str
    agent_id: str
    task_template: Dict[str, Any]
    dependencies: List[str] = []  # Step IDs that must complete first
    condition: Optional[str] = None  # Conditional execution
    retry_count: int = 3
    timeout: int = 300


class WorkflowDefinition(BaseModel):
    """Complete workflow definition."""
    id: Optional[str] = None
    name: str
    description: str
    steps: List[WorkflowStep]
    parallel_groups: List[List[str]] = []  # Groups of steps that can run in parallel
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    timeout: int = 3600
    auto_retry: bool = True
    created_by: Optional[str] = None
    tags: List[str] = []


class WorkflowExecution(BaseModel):
    """Workflow execution instance."""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    input_data: Dict[str, Any]
    step_results: Dict[str, TaskResult] = Field(default_factory=dict)
    current_step: Optional[str] = None
    progress_percentage: float = 0.0
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class SystemMetrics(BaseModel):
    """System performance metrics."""
    cpu_usage: float
    memory_usage: float
    active_connections: int
    requests_per_second: float
    average_response_time: float
    error_rate: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SystemStatus(BaseModel):
    """Overall system status."""
    status: str
    uptime: float
    active_agents: int
    total_agents: int
    active_workflows: int
    queue_depth: int
    metrics: SystemMetrics
    timestamp: str


class LogEntry(BaseModel):
    """System log entry."""
    timestamp: datetime
    level: str
    agent_id: Optional[str]
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTONOMOUS MODE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class AutonomousConfig(BaseModel):
    """Configuration for autonomous execution mode."""
    enabled: bool = False
    scan_interval: int = 60  # seconds
    max_concurrent_tasks: int = 10
    scaling_threshold: int = 500  # Trigger scaling at this metric value
    auto_discover_tasks: bool = True
    task_sources: List[str] = ["email", "calendar", "tickets", "api"]
    notification_channels: List[str] = ["webhook", "slack"]
    learning_enabled: bool = True


class ScalingDecision(BaseModel):
    """Autonomous scaling decision."""
    decision_id: str
    trigger_metric: str
    trigger_value: float
    threshold: float
    action: str  # scale_up, scale_down, launch_new_agent
    agents_to_spawn: List[str]
    reason: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
