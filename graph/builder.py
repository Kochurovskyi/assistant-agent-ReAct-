"""Graph builder for the memory agent."""
from datetime import datetime
from typing import Dict, Any

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from config import Configuration
from utils.metrics import metrics
from .nodes import task_asis, update_profile, update_todos, update_instructions
from .edges import route_message

# Create the graph + all nodes
builder = StateGraph(MessagesState, context_schema=Configuration)

# Define the flow of the memory extraction process
builder.add_node(task_asis)
builder.add_node(update_todos)
builder.add_node(update_profile)
builder.add_node(update_instructions)

# Define the flow 
builder.add_edge(START, "task_asis")
builder.add_conditional_edges("task_asis", route_message)
builder.add_edge("update_todos", "task_asis")
builder.add_edge("update_profile", "task_asis")
builder.add_edge("update_instructions", "task_asis")

# Compile the graph
mem_checkpointer = MemorySaver()
mem_store = InMemoryStore()
graph = builder.compile(checkpointer=mem_checkpointer, store=mem_store)

# Generate graph visualization
try:
    png_data = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f: 
        f.write(png_data)
except Exception as e:
    print(f"Could not generate graph visualization: {e}")

# Health check functions
def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    try:
        # Test store connectivity
        test_namespace = ("health", "test", "check")
        test_store = InMemoryStore()
        test_store.put(test_namespace, "test_key", {"test": "value"})
        test_result = test_store.get(test_namespace, "test_key")
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "store_connectivity": "ok" if test_result else "failed",
            "metrics": metrics.get_stats()
        }
    except Exception as e:
        from utils.logging_config import logger
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "metrics": metrics.get_stats()
        }

def get_metrics() -> Dict[str, Any]:
    """Get current metrics"""
    return metrics.get_stats()
