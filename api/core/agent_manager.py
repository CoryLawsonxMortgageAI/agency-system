"""
Agent Manager - Core Orchestration Engine
=========================================
Manages all agents, their lifecycle, task execution, and swarm coordination.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
import logging

from models.schemas import AgentConfig, AgentStatus, TaskRequest, TaskResult, TaskStatus, AgentStatusEnum
from agents.agent_definitions import AGENT_DEFINITIONS

logger = logging.getLogger(__name__)


@dataclass
class AgentInstance:
    """Runtime instance of an agent."""
    config: AgentConfig
    status: AgentStatusEnum = AgentStatusEnum.IDLE
    current_task: Optional[str] = None
    task_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    total_completed: int = 0
    total_failed: int = 0
    last_active: Optional[datetime] = None
    
    @property
    def is_available(self) -> bool:
        return self.status == AgentStatusEnum.IDLE and self.config.active


class AgentManager:
    """
    Central manager for all agents in the system.
    Handles agent lifecycle, task distribution, and swarm coordination.
    """
    
    def __init__(self, metrics_collector):
        self.agents: Dict[str, AgentInstance] = {}
        self.metrics = metrics_collector
        self.task_callbacks: Dict[str, List[Callable]] = {}
        self._running = False
        self._lock = asyncio.Lock()
        
    async def load_agents(self):
        """Load all agent definitions from the definitions module."""
        logger.info("📥 Loading agent definitions...")
        
        for agent_def in AGENT_DEFINITIONS:
            agent_config = AgentConfig(**agent_def)
            await self.register_agent(agent_config)
        
        logger.info(f"✅ Loaded {len(self.agents)} agents")
        
        # Start agent worker loops
        self._running = True
        for agent_id, instance in self.agents.items():
            asyncio.create_task(self._agent_worker(agent_id, instance))
    
    async def register_agent(self, config: AgentConfig):
        """Register a new agent with the system."""
        async with self._lock:
            instance = AgentInstance(config=config)
            self.agents[config.id] = instance
            
            logger.info(f"🤖 Registered agent: {config.name} ({config.id})")
            
            # Record metric
            await self.metrics.record_event("agent_registered", {
                "agent_id": config.id,
                "division": config.division
            })
    
    async def list_agents(self) -> List[AgentConfig]:
        """List all registered agents."""
        return [instance.config for instance in self.agents.values()]
    
    async def get_agent(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration by ID."""
        instance = self.agents.get(agent_id)
        return instance.config if instance else None
    
    async def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get current status of an agent."""
        instance = self.agents.get(agent_id)
        if not instance:
            return None
        
        return AgentStatus(
            agent_id=agent_id,
            status=instance.status,
            current_task=instance.current_task,
            queue_depth=instance.task_queue.qsize(),
            total_tasks_completed=instance.total_completed,
            total_tasks_failed=instance.total_failed,
            average_response_time=0.0,  # Calculated from history
            last_active=instance.last_active
        )
    
    async def get_active_agents(self) -> List[str]:
        """Get list of currently active agent IDs."""
        return [
            agent_id for agent_id, instance in self.agents.items()
            if instance.status == AgentStatusEnum.ACTIVE
        ]
    
    async def activate_agent(self, agent_id: str) -> bool:
        """Activate an agent for task execution."""
        instance = self.agents.get(agent_id)
        if not instance:
            return False
        
        instance.config.active = True
        instance.status = AgentStatusEnum.IDLE
        
        logger.info(f"🟢 Activated agent: {agent_id}")
        await self.metrics.record_event("agent_activated", {"agent_id": agent_id})
        return True
    
    async def deactivate_agent(self, agent_id: str):
        """Deactivate an agent."""
        instance = self.agents.get(agent_id)
        if instance:
            instance.config.active = False
            instance.status = AgentStatusEnum.OFFLINE
            logger.info(f"🔴 Deactivated agent: {agent_id}")
            await self.metrics.record_event("agent_deactivated", {"agent_id": agent_id})
    
    async def execute_task(
        self,
        agent_id: str,
        task_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> TaskResult:
        """
        Execute a single task with a specific agent.
        This is the primary interface for task execution.
        """
        instance = self.agents.get(agent_id)
        if not instance:
            return TaskResult(
                task_id=str(uuid.uuid4()),
                agent_id=agent_id,
                status=TaskStatus.FAILED,
                output=None,
                error=f"Agent {agent_id} not found",
                execution_time=0.0
            )
        
        if not instance.config.active:
            return TaskResult(
                task_id=str(uuid.uuid4()),
                agent_id=agent_id,
                status=TaskStatus.FAILED,
                output=None,
                error=f"Agent {agent_id} is not active",
                execution_time=0.0
            )
        
        task_id = str(uuid.uuid4())
        task_request = {
            "task_id": task_id,
            "agent_id": agent_id,
            "task_data": task_data,
            "context": context or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Create a future to wait for result
        result_future = asyncio.Future()
        
        # Store callback
        if task_id not in self.task_callbacks:
            self.task_callbacks[task_id] = []
        
        def callback(result):
            if not result_future.done():
                result_future.set_result(result)
        
        self.task_callbacks[task_id].append(callback)
        
        # Queue the task
        await instance.task_queue.put((task_request, callback))
        
        logger.info(f"📋 Queued task {task_id} for agent {agent_id}")
        
        # Wait for result with timeout
        try:
            result = await asyncio.wait_for(result_future, timeout=300)
            return result
        except asyncio.TimeoutError:
            return TaskResult(
                task_id=task_id,
                agent_id=agent_id,
                status=TaskStatus.FAILED,
                output=None,
                error="Task execution timed out",
                execution_time=300.0
            )
    
    async def execute_swarm(
        self,
        swarm_id: str,
        tasks: List[TaskRequest]
    ) -> List[TaskResult]:
        """
        Execute multiple tasks in parallel using the agent swarm.
        Distributes tasks optimally across available agents.
        """
        logger.info(f"🐝 Initiating swarm execution: {swarm_id} with {len(tasks)} tasks")
        
        # Group tasks by agent for efficiency
        tasks_by_agent: Dict[str, List[TaskRequest]] = {}
        for task in tasks:
            if task.agent_id not in tasks_by_agent:
                tasks_by_agent[task.agent_id] = []
            tasks_by_agent[task.agent_id].append(task)
        
        # Execute all tasks in parallel
        coroutines = []
        for agent_id, agent_tasks in tasks_by_agent.items():
            for task in agent_tasks:
                coroutines.append(self.execute_task(
                    agent_id=task.agent_id,
                    task_data=task.task_data,
                    context=task.context
                ))
        
        # Run all tasks concurrently
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Process results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(TaskResult(
                    task_id=str(uuid.uuid4()),
                    agent_id="unknown",
                    status=TaskStatus.FAILED,
                    output=None,
                    error=str(result),
                    execution_time=0.0
                ))
            else:
                processed_results.append(result)
        
        # Record metrics
        success_count = sum(1 for r in processed_results if r.status == TaskStatus.COMPLETED)
        await self.metrics.record_event("swarm_completed", {
            "swarm_id": swarm_id,
            "total_tasks": len(tasks),
            "successful": success_count,
            "failed": len(tasks) - success_count
        })
        
        logger.info(f"✅ Swarm {swarm_id} completed: {success_count}/{len(tasks)} successful")
        
        return processed_results
    
    async def _agent_worker(self, agent_id: str, instance: AgentInstance):
        """
        Background worker loop for each agent.
        Processes tasks from the agent's queue.
        """
        from core.ai_interface import AIInterface
        ai_interface = AIInterface()
        
        logger.info(f"🔄 Started worker for agent: {agent_id}")
        
        while self._running:
            try:
                # Wait for a task
                task_request, callback = await instance.task_queue.get()
                
                # Update status
                instance.status = AgentStatusEnum.BUSY
                instance.current_task = task_request["task_id"]
                instance.last_active = datetime.utcnow()
                
                start_time = datetime.utcnow()
                
                try:
                    # Execute the task via AI interface
                    result = await self._execute_with_ai(
                        ai_interface,
                        instance,
                        task_request
                    )
                    
                    instance.total_completed += 1
                    
                except Exception as e:
                    logger.error(f"❌ Task execution failed: {e}", exc_info=True)
                    
                    result = TaskResult(
                        task_id=task_request["task_id"],
                        agent_id=agent_id,
                        status=TaskStatus.FAILED,
                        output=None,
                        error=str(e),
                        execution_time=(datetime.utcnow() - start_time).total_seconds()
                    )
                    
                    instance.total_failed += 1
                
                finally:
                    # Update status
                    instance.status = AgentStatusEnum.IDLE if instance.config.active else AgentStatusEnum.OFFLINE
                    instance.current_task = None
                    
                    # Call callback
                    callback(result)
                    
                    # Execute registered callbacks
                    task_id = task_request["task_id"]
                    if task_id in self.task_callbacks:
                        for cb in self.task_callbacks[task_id]:
                            try:
                                cb(result)
                            except:
                                pass
                        del self.task_callbacks[task_id]
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Agent worker error: {e}", exc_info=True)
                await asyncio.sleep(1)
        
        logger.info(f"🛑 Stopped worker for agent: {agent_id}")
    
    async def _execute_with_ai(
        self,
        ai_interface: 'AIInterface',
        instance: AgentInstance,
        task_request: Dict[str, Any]
    ) -> TaskResult:
        """
        Execute a task using the AI interface.
        This is where the actual AI model interaction happens.
        """
        start_time = datetime.utcnow()
        
        # Build the full prompt
        system_prompt = instance.config.system_prompt
        
        task_data = task_request["task_data"]
        context = task_request.get("context", {})
        
        user_prompt = self._build_task_prompt(task_data, context)
        
        # Call AI
        response = await ai_interface.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=instance.config.model,
            temperature=instance.config.temperature,
            max_tokens=instance.config.max_tokens
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return TaskResult(
            task_id=task_request["task_id"],
            agent_id=instance.config.id,
            status=TaskStatus.COMPLETED,
            output=response["content"],
            execution_time=execution_time,
            tokens_used=response.get("tokens_used"),
            cost=response.get("cost"),
            completed_at=datetime.utcnow()
        )
    
    def _build_task_prompt(self, task_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build the user prompt from task data and context."""
        prompt_parts = []
        
        if "instruction" in task_data:
            prompt_parts.append(f"Task: {task_data['instruction']}")
        
        if "input" in task_data:
            prompt_parts.append(f"\nInput:\n{json.dumps(task_data['input'], indent=2)}")
        
        if "requirements" in task_data:
            prompt_parts.append(f"\nRequirements:\n{task_data['requirements']}")
        
        if context:
            prompt_parts.append(f"\nContext:\n{json.dumps(context, indent=2)}")
        
        if "expected_output" in task_data:
            prompt_parts.append(f"\nExpected Output Format:\n{task_data['expected_output']}")
        
        return "\n".join(prompt_parts)
    
    async def get_logs(
        self,
        level: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get system logs with optional filtering."""
        # In production, this would query a log store
        # For now, return empty list
        return []
    
    async def shutdown(self):
        """Gracefully shut down the agent manager."""
        logger.info("🛑 Shutting down Agent Manager...")
        self._running = False
        
        # Wait for all tasks to complete
        for agent_id, instance in self.agents.items():
            # Cancel remaining tasks in queue
            while not instance.task_queue.empty():
                try:
                    task_request, callback = instance.task_queue.get_nowait()
                    result = TaskResult(
                        task_id=task_request["task_id"],
                        agent_id=agent_id,
                        status=TaskStatus.CANCELLED,
                        output=None,
                        error="System shutdown",
                        execution_time=0.0
                    )
                    callback(result)
                except asyncio.QueueEmpty:
                    break
        
        logger.info("✅ Agent Manager shutdown complete")
