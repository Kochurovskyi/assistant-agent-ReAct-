"""Metrics tracking for the memory agent."""
from typing import Dict, Any

class Metrics:
    """Metrics tracking for monitoring the memory agent."""
    
    def __init__(self):
        self.requests_total = 0
        self.errors_total = 0
        self.memory_updates = 0
        self.response_times = []
    
    def record_request(self, response_time: float):
        """Record a request with its response time."""
        self.requests_total += 1
        self.response_times.append(response_time)
        if len(self.response_times) > 1000:  # Keep only last 1000
            self.response_times = self.response_times[-1000:]
    
    def record_error(self):
        """Record an error occurrence."""
        self.errors_total += 1
    
    def record_memory_update(self):
        """Record a memory update operation."""
        self.memory_updates += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics statistics."""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "memory_updates": self.memory_updates,
            "avg_response_time": avg_response_time,
            "error_rate": self.errors_total / max(self.requests_total, 1)
        }

# Global metrics instance
metrics = Metrics()
