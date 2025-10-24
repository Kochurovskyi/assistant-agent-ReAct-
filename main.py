"""Memory Agent - Production-ready task management assistant."""
import asyncio
from graph.builder import graph, health_check, get_metrics
from tests.test_agent import test_production_agent

if __name__ == "__main__":
    test_production_agent()
