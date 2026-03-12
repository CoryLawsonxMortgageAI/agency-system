"""
Monitoring & Metrics Collection
===============================
Collects and aggregates system performance metrics.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)

# Optional psutil import
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    logger.warning("psutil not installed. System metrics will be limited.")


class MetricsCollector:
    """Collects and stores system metrics."""
    
    def __init__(self, retention_hours: int = 24):
        self.start_time = datetime.utcnow()
        self.metrics_history: deque = deque(maxlen=10000)
        self.events: deque = deque(maxlen=5000)
        self._lock = None  # Would use asyncio.Lock in async context
        
    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        return (datetime.utcnow() - self.start_time).total_seconds()
    
    async def record_event(self, event_type: str, data: Dict[str, Any]):
        """Record a system event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "data": data
        }
        self.events.append(event)
        
        logger.info(f"Event: {event_type}")
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        # System metrics
        if HAS_PSUTIL:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                memory_usage = memory.percent
                memory_available = memory.available / (1024 * 1024)
            except Exception:
                cpu_percent = 0.0
                memory_usage = 0.0
                memory_available = 0.0
        else:
            cpu_percent = 0.0
            memory_usage = 0.0
            memory_available = 0.0
        
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_usage": cpu_percent,
            "memory_usage": memory_usage,
            "memory_available_mb": memory_available,
            "active_connections": 0,  # Would track actual connections
            "requests_per_second": 0.0,  # Calculate from history
            "average_response_time": 0.0,  # Calculate from history
            "error_rate": 0.0,  # Calculate from events
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    async def get_metrics(self, time_range: str = "1h") -> Dict[str, Any]:
        """Get metrics for a specific time range."""
        # Parse time range
        ranges = {
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7)
        }
        
        delta = ranges.get(time_range, timedelta(hours=1))
        cutoff = datetime.utcnow() - delta
        
        # Filter metrics
        filtered = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        
        if not filtered:
            return {"metrics": [], "time_range": time_range}
        
        # Calculate aggregates
        return {
            "metrics": filtered,
            "time_range": time_range,
            "aggregates": {
                "avg_cpu": sum(m["cpu_usage"] for m in filtered) / len(filtered),
                "avg_memory": sum(m["memory_usage"] for m in filtered) / len(filtered),
                "max_cpu": max(m["cpu_usage"] for m in filtered),
                "max_memory": max(m["memory_usage"] for m in filtered)
            }
        }
    
    async def get_events(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get system events."""
        events_list = list(self.events)
        
        if event_type:
            events_list = [e for e in events_list if e["type"] == event_type]
        
        return events_list[-limit:]
