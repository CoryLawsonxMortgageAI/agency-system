"""
Autonomous Executor - Self-Running Business Operations
======================================================
Monitors metrics, triggers workflows automatically, and scales agents.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

from models.schemas import AutonomousConfig, ScalingDecision, WorkflowDefinition

logger = logging.getLogger(__name__)


class AutonomousExecutor:
    """
    Manages autonomous operation of the agency.
    - Monitors performance metrics
    - Triggers workflows based on conditions
    - Auto-scales agent capacity
    - Self-corrects based on outcomes
    """
    
    def __init__(self, workflow_engine, metrics_collector):
        self.workflow_engine = workflow_engine
        self.metrics = metrics_collector
        self.config: AutonomousConfig = AutonomousConfig()
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self.decision_history: List[ScalingDecision] = []
        self.automation_rules: List[Dict[str, Any]] = []
        
    async def start(self, config: Optional[Dict[str, Any]] = None):
        """Start autonomous execution mode."""
        if config:
            self.config = AutonomousConfig(**config)
        
        self.config.enabled = True
        self._running = True
        
        logger.info("🤖 AUTONOMOUS MODE ACTIVATED")
        logger.info(f"   Scan Interval: {self.config.scan_interval}s")
        logger.info(f"   Max Concurrent: {self.config.max_concurrent_tasks}")
        logger.info(f"   Scaling Threshold: {self.config.scaling_threshold}")
        
        await self.metrics.record_event("autonomous_mode_started", self.config.dict())
    
    async def stop(self):
        """Stop autonomous execution mode."""
        self._running = False
        self.config.enabled = False
        
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 AUTONOMOUS MODE DEACTIVATED")
        await self.metrics.record_event("autonomous_mode_stopped", {})
    
    async def run_execution_loop(self):
        """Main autonomous execution loop."""
        while True:
            try:
                if self._running and self.config.enabled:
                    await self._execute_cycle()
                
                await asyncio.sleep(self.config.scan_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Autonomous execution error: {e}", exc_info=True)
                await asyncio.sleep(10)
    
    async def _execute_cycle(self):
        """Execute one autonomous cycle."""
        # 1. Collect current metrics
        current_metrics = await self._collect_metrics()
        
        # 2. Evaluate automation rules
        triggered_rules = await self._evaluate_rules(current_metrics)
        
        # 3. Execute triggered workflows
        for rule in triggered_rules:
            await self._execute_rule_workflow(rule, current_metrics)
        
        # 4. Check scaling conditions
        await self._evaluate_scaling(current_metrics)
        
        # 5. Self-correction based on outcomes
        await self._self_correct()
    
    async def _collect_metrics(self) -> Dict[str, float]:
        """Collect current system metrics."""
        metrics = await self.metrics.get_current_metrics()
        return {
            "active_agents": metrics.get("active_agents", 0),
            "queue_depth": metrics.get("queue_depth", 0),
            "requests_per_second": metrics.get("requests_per_second", 0),
            "average_response_time": metrics.get("average_response_time", 0),
            "error_rate": metrics.get("error_rate", 0),
            "cpu_usage": metrics.get("cpu_usage", 0),
            "memory_usage": metrics.get("memory_usage", 0)
        }
    
    async def _evaluate_rules(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Evaluate automation rules against current metrics."""
        triggered = []
        
        # High queue depth -> Scale up processing
        if metrics["queue_depth"] > 50:
            triggered.append({
                "name": "high_queue_scale",
                "condition": "queue_depth > 50",
                "workflow": "scale_processing_capacity",
                "priority": "high"
            })
        
        # High error rate -> Alert and investigate
        if metrics["error_rate"] > 0.05:  # 5%
            triggered.append({
                "name": "high_error_rate",
                "condition": "error_rate > 5%",
                "workflow": "error_investigation",
                "priority": "critical"
            })
        
        # Low agent utilization -> Optimize resources
        if metrics["active_agents"] > 10 and metrics["queue_depth"] < 5:
            triggered.append({
                "name": "low_utilization",
                "condition": "agents > 10 AND queue < 5",
                "workflow": "optimize_resources",
                "priority": "low"
            })
        
        return triggered
    
    async def _execute_rule_workflow(self, rule: Dict[str, Any], metrics: Dict[str, float]):
        """Execute a workflow triggered by a rule."""
        logger.info(f"🔔 Rule triggered: {rule['name']} ({rule['condition']})")
        
        # Create workflow based on rule
        workflow_def = self._create_workflow_for_rule(rule)
        
        # Execute
        execution_id = await self.workflow_engine.create_execution(workflow_def)
        
        # Start in background
        asyncio.create_task(
            self.workflow_engine.run_workflow(
                execution_id,
                workflow_def,
                {"triggered_rule": rule, "metrics": metrics}
            )
        )
    
    def _create_workflow_for_rule(self, rule: Dict[str, Any]) -> WorkflowDefinition:
        """Create a workflow definition for a triggered rule."""
        workflows = {
            "scale_processing_capacity": WorkflowDefinition(
                name="Scale Processing Capacity",
                description="Automatically scale agent capacity to handle high load",
                steps=[
                    {
                        "id": "analyze_load",
                        "name": "Analyze Load Pattern",
                        "agent_id": "infrastructure-maintainer",
                        "task_template": {
                            "instruction": "Analyze current system load and determine optimal scaling strategy",
                            "input": {"rule": "{{triggered_rule}}", "metrics": "{{metrics}}"}
                        },
                        "dependencies": []
                    },
                    {
                        "id": "scale_agents",
                        "name": "Scale Agent Pool",
                        "agent_id": "devops-automator",
                        "task_template": {
                            "instruction": "Execute scaling commands based on analysis",
                            "input": {"analysis": "{{analyze_load.output}}"}
                        },
                        "dependencies": ["analyze_load"]
                    }
                ]
            ),
            "error_investigation": WorkflowDefinition(
                name="Error Investigation",
                description="Investigate and remediate high error rates",
                steps=[
                    {
                        "id": "collect_logs",
                        "name": "Collect Error Logs",
                        "agent_id": "evidence-collector",
                        "task_template": {
                            "instruction": "Collect and analyze error logs for patterns"
                        },
                        "dependencies": []
                    },
                    {
                        "id": "diagnose",
                        "name": "Diagnose Root Cause",
                        "agent_id": "reality-checker",
                        "task_template": {
                            "instruction": "Diagnose root cause of errors from collected evidence"
                        },
                        "dependencies": ["collect_logs"]
                    },
                    {
                        "id": "remediate",
                        "name": "Apply Fix",
                        "agent_id": "senior-developer",
                        "task_template": {
                            "instruction": "Implement fix for diagnosed issue"
                        },
                        "dependencies": ["diagnose"]
                    }
                ]
            ),
            "optimize_resources": WorkflowDefinition(
                name="Resource Optimization",
                description="Optimize resource allocation for efficiency",
                steps=[
                    {
                        "id": "analyze_usage",
                        "name": "Analyze Resource Usage",
                        "agent_id": "analytics-reporter",
                        "task_template": {
                            "instruction": "Analyze resource utilization patterns"
                        },
                        "dependencies": []
                    }
                ]
            )
        }
        
        return workflows.get(rule["workflow"], workflows["scale_processing_capacity"])
    
    async def _evaluate_scaling(self, metrics: Dict[str, float]):
        """Evaluate if system needs to scale."""
        # Check if any metric exceeds threshold
        scaling_triggered = False
        trigger_metric = ""
        trigger_value = 0.0
        
        if metrics["queue_depth"] > self.config.scaling_threshold:
            scaling_triggered = True
            trigger_metric = "queue_depth"
            trigger_value = metrics["queue_depth"]
        
        if scaling_triggered:
            decision = ScalingDecision(
                decision_id=f"scale_{datetime.utcnow().timestamp()}",
                trigger_metric=trigger_metric,
                trigger_value=trigger_value,
                threshold=float(self.config.scaling_threshold),
                action="scale_up",
                agents_to_spawn=["rapid-prototyper", "frontend-developer", "backend-architect"],
                reason=f"{trigger_metric} ({trigger_value}) exceeded threshold ({self.config.scaling_threshold})",
                confidence=0.85
            )
            
            self.decision_history.append(decision)
            
            logger.info(f"📈 SCALING DECISION: {decision.action}")
            logger.info(f"   Reason: {decision.reason}")
            logger.info(f"   Agents to spawn: {decision.agents_to_spawn}")
            
            await self.metrics.record_event("scaling_decision", decision.dict())
            
            # Execute scaling workflow
            await self._execute_scaling(decision)
    
    async def _execute_scaling(self, decision: ScalingDecision):
        """Execute a scaling decision."""
        # Create scaling workflow
        scaling_workflow = WorkflowDefinition(
            name=f"Auto-Scale: {decision.action}",
            description=f"Automatic scaling triggered by {decision.trigger_metric}",
            steps=[
                {
                    "id": "prepare_scale",
                    "name": "Prepare Scaling Environment",
                    "agent_id": "devops-automator",
                    "task_template": {
                        "instruction": "Prepare infrastructure for scaling operation",
                        "input": {"decision": decision.dict()}
                    },
                    "dependencies": []
                },
                {
                    "id": "spawn_agents",
                    "name": "Spawn New Agents",
                    "agent_id": "agents-orchestrator",
                    "task_template": {
                        "instruction": "Orchestrate deployment of new agent instances",
                        "input": {"agents_to_spawn": decision.agents_to_spawn}
                    },
                    "dependencies": ["prepare_scale"]
                },
                {
                    "id": "verify_scale",
                    "name": "Verify Scaling Success",
                    "agent_id": "reality-checker",
                    "task_template": {
                        "instruction": "Verify that scaling operation completed successfully"
                    },
                    "dependencies": ["spawn_agents"]
                }
            ]
        )
        
        execution_id = await self.workflow_engine.create_execution(scaling_workflow)
        asyncio.create_task(
            self.workflow_engine.run_workflow(execution_id, scaling_workflow)
        )
    
    async def _self_correct(self):
        """Self-correction based on recent outcomes."""
        # Analyze recent decisions
        if len(self.decision_history) < 5:
            return
        
        recent_decisions = self.decision_history[-10:]
        
        # Check if scaling decisions are having the desired effect
        scale_ups = [d for d in recent_decisions if d.action == "scale_up"]
        
        if len(scale_ups) >= 3:
            # Too many scale-ups might indicate an underlying issue
            logger.warning("⚠️ High frequency of scaling decisions detected - investigating")
            
            # Trigger investigation workflow
            investigation_workflow = WorkflowDefinition(
                name="Scaling Pattern Investigation",
                description="Investigate frequent scaling triggers",
                steps=[
                    {
                        "id": "analyze_pattern",
                        "name": "Analyze Scaling Pattern",
                        "agent_id": "analytics-reporter",
                        "task_template": {
                            "instruction": "Analyze recent scaling decisions and identify root cause of frequent triggers"
                        },
                        "dependencies": []
                    }
                ]
            )
            
            execution_id = await self.workflow_engine.create_execution(investigation_workflow)
            asyncio.create_task(
                self.workflow_engine.run_workflow(execution_id, investigation_workflow)
            )
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current autonomous execution status."""
        return {
            "enabled": self.config.enabled,
            "running": self._running,
            "config": self.config.dict(),
            "decision_history_count": len(self.decision_history),
            "recent_decisions": [d.dict() for d in self.decision_history[-5:]]
        }
