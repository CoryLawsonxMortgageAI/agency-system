#!/usr/bin/env python
"""Test that all imports work correctly."""

import sys
sys.path.insert(0, '.')

print("Testing imports...")

# Test models
from models.schemas import AgentConfig, WorkflowDefinition
print("[OK] Models")

# Test agent definitions  
from agents.agent_definitions import AGENT_DEFINITIONS
print(f"[OK] Agent definitions ({len(AGENT_DEFINITIONS)} agents)")

# Test core modules
from core.monitoring import MetricsCollector
print("[OK] MetricsCollector")

from core.ai_interface import AIInterface
print("[OK] AIInterface")

from core.agent_manager import AgentManager
print("[OK] AgentManager")

from core.workflow_engine import WorkflowEngine
print("[OK] WorkflowEngine")

from core.autonomous_executor import AutonomousExecutor
print("[OK] AutonomousExecutor")

print("\n[SUCCESS] All imports successful!")
