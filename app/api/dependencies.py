"""FastAPI dependencies for graph access and configuration."""

from fastapi import Depends, HTTPException
from typing import Dict, Any

from graph.builder import graph, health_check, get_metrics
from config import app_config


def get_graph():
    """Get the LangGraph instance."""
    return graph


def get_health_check():
    """Get the health check function."""
    return health_check


def get_metrics_func():
    """Get the metrics function."""
    return get_metrics


def get_app_config():
    """Get the application configuration."""
    return app_config


def validate_user_id(user_id: str) -> str:
    """Validate and return user ID."""
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required")
    return user_id.strip()


def validate_session_id(session_id: str = None) -> str:
    """Validate and return session ID."""
    if not session_id:
        import uuid
        return str(uuid.uuid4())
    return session_id.strip()
