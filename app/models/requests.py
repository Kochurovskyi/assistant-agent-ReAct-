"""Pydantic models for request/response validation."""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    user_id: str = "default-user"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str
    user_id: str
    metadata: Dict[str, Any]


class WebSocketMessage(BaseModel):
    """Message model for WebSocket communication."""
    message: str
    user_id: str = "default-user"
    session_id: Optional[str] = None


class MemoryRequest(BaseModel):
    """Request model for memory operations."""
    user_id: str
    data: Dict[str, Any]


class MemoryResponse(BaseModel):
    """Response model for memory operations."""
    user_id: str
    data: Dict[str, Any]
    success: bool
    message: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    store_connectivity: str
    metrics: Dict[str, Any]


class MetricsResponse(BaseModel):
    """Response model for metrics endpoint."""
    requests_total: int
    errors_total: int
    memory_updates: int
    avg_response_time: float
    error_rate: float
