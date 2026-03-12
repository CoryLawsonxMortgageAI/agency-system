"""
Workflow Engine - Multi-Agent Coordination
==========================================
Orchestrates complex workflows across multiple agents with dependency management.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict
import logging

from models.schemas import (
    WorkflowDefinition, WorkflowExecution, WorkflowStatus,
    WorkflowStep, TaskResult, TaskStatus
)

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Manages workflow definitions and executes multi-agent workflows.
    Handles dependencies, parallel execution, and error recovery.
    """
    
    def __init__(self, agent_manager, metrics_collector):
        self.agent_manager = agent_manager
        self.metrics = metrics_collector
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self._lock = asyncio.Lock()
    
    async def load_workflow(self, workflow: WorkflowDefinition):
        """Load a workflow definition."""
        workflow.id = workflow.id or str(uuid.uuid4())
        self.workflows[workflow.id] = workflow
        logger.info(f"📋 Loaded workflow: {workflow.name}")
    
    async def list_workflows(self) -> List[WorkflowDefinition]:
        """List all available workflows."""
        return list(self.workflows.values())
    
    async def create_execution(self, workflow_def: WorkflowDefinition) -> str:
        """Create a new workflow execution instance."""
        execution_id = str(uuid.uuid4())
        
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_def.id or str(uuid.uuid4()),
            status=WorkflowStatus.PENDING,
            input_data={}
        )
        
        async with self._lock:
            self.executions[execution_id] = execution
        
        return execution_id
    
    async def run_workflow(
        self,
        execution_id: str,
        workflow_def: WorkflowDefinition,
        input_data: Optional[Dict[str, Any]] = None
    ):
        """
        Execute a workflow.
        This is the main execution entry point.
        """
        execution = self.executions.get(execution_id)
        if not execution:
            logger.error(f"Execution {execution_id} not found")
            return
        
        execution.status = WorkflowStatus.RUNNING
        execution.input_data = input_data or {}
        
        logger.info(f"🚀 Starting workflow execution: {execution_id}")
        
        try:
            # Build dependency graph
            dependency_graph = self._build_dependency_graph(workflow_def.steps)
            
            # Execute steps in topological order
            completed_steps = set()
            failed_steps = set()
            
            while len(completed_steps) + len(failed_steps) < len(workflow_def.steps):
                # Find ready steps (dependencies satisfied)
                ready_steps = self._get_ready_steps(
                    workflow_def.steps,
                    dependency_graph,
                    completed_steps,
                    failed_steps
                )
                
                if not ready_steps:
                    if failed_steps:
                        logger.error(f"Workflow blocked by failed steps: {failed_steps}")
                        execution.status = WorkflowStatus.FAILED
                        execution.error_message = f"Blocked by failed steps: {failed_steps}"
                        break
                    break
                
                # Execute ready steps in parallel
                step_results = await asyncio.gather(*[
                    self._execute_step(execution_id, step, execution.step_results)
                    for step in ready_steps
                ])
                
                # Process results
                for step, result in zip(ready_steps, step_results):
                    execution.step_results[step.id] = result
                    
                    if result.status == TaskStatus.COMPLETED:
                        completed_steps.add(step.id)
                        logger.info(f"✅ Step {step.id} completed")
                    else:
                        failed_steps.add(step.id)
                        logger.error(f"❌ Step {step.id} failed: {result.error}")
                        
                        if not workflow_def.auto_retry:
                            execution.status = WorkflowStatus.FAILED
                            execution.error_message = f"Step {step.id} failed"
                            break
                
                # Update progress
                execution.progress_percentage = len(completed_steps) / len(workflow_def.steps) * 100
                
                if execution.status == WorkflowStatus.FAILED:
                    break
            
            # Check final status
            if execution.status != WorkflowStatus.FAILED:
                if len(completed_steps) == len(workflow_def.steps):
                    execution.status = WorkflowStatus.COMPLETED
                    execution.completed_at = datetime.utcnow()
                    logger.info(f"✅ Workflow {execution_id} completed successfully")
                elif failed_steps:
                    execution.status = WorkflowStatus.FAILED
                    execution.error_message = f"Steps failed: {failed_steps}"
            
            # Record metrics
            await self.metrics.record_event("workflow_execution", {
                "execution_id": execution_id,
                "workflow_id": workflow_def.id,
                "status": execution.status.value,
                "steps_completed": len(completed_steps),
                "steps_failed": len(failed_steps)
            })
            
        except Exception as e:
            logger.error(f"❌ Workflow execution error: {e}", exc_info=True)
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
    
    def _build_dependency_graph(self, steps: List[WorkflowStep]) -> Dict[str, List[str]]:
        """Build a dependency graph from workflow steps."""
        graph = defaultdict(list)
        
        for step in steps:
            for dep in step.dependencies:
                graph[step.id].append(dep)
        
        return dict(graph)
    
    def _get_ready_steps(
        self,
        steps: List[WorkflowStep],
        dependency_graph: Dict[str, List[str]],
        completed_steps: set,
        failed_steps: set
    ) -> List[WorkflowStep]:
        """Get steps that are ready to execute (dependencies satisfied)."""
        ready = []
        
        for step in steps:
            if step.id in completed_steps or step.id in failed_steps:
                continue
            
            deps = dependency_graph.get(step.id, [])
            if all(dep in completed_steps for dep in deps):
                ready.append(step)
        
        return ready
    
    async def _execute_step(
        self,
        execution_id: str,
        step: WorkflowStep,
        previous_results: Dict[str, TaskResult]
    ) -> TaskResult:
        """Execute a single workflow step."""
        
        # Build context from previous steps
        context = {
            "execution_id": execution_id,
            "step_id": step.id,
            "previous_results": {
                step_id: result.output if result.status == TaskStatus.COMPLETED else None
                for step_id, result in previous_results.items()
            }
        }
        
        # Execute with agent
        result = await self.agent_manager.execute_task(
            agent_id=step.agent_id,
            task_data=step.task_template,
            context=context
        )
        
        # Retry logic
        if result.status == TaskStatus.FAILED and step.retry_count > 0:
            for attempt in range(step.retry_count):
                logger.warning(f"🔄 Retrying step {step.id} (attempt {attempt + 1})")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                result = await self.agent_manager.execute_task(
                    agent_id=step.agent_id,
                    task_data=step.task_template,
                    context=context
                )
                
                if result.status == TaskStatus.COMPLETED:
                    break
        
        return result
    
    async def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get the status of a workflow execution."""
        return self.executions.get(execution_id)
    
    async def get_active_count(self) -> int:
        """Get number of active workflow executions."""
        return sum(
            1 for e in self.executions.values()
            if e.status == WorkflowStatus.RUNNING
        )
    
    async def get_queue_depth(self) -> int:
        """Get total task queue depth across all workflows."""
        return sum(
            e.status == WorkflowStatus.PENDING
            for e in self.executions.values()
        )
    
    async def shutdown(self):
        """Gracefully shut down the workflow engine."""
        logger.info("🛑 Shutting down Workflow Engine...")
        
        # Cancel pending executions
        for execution in self.executions.values():
            if execution.status in [WorkflowStatus.PENDING, WorkflowStatus.RUNNING]:
                execution.status = WorkflowStatus.FAILED
                execution.error_message = "System shutdown"
