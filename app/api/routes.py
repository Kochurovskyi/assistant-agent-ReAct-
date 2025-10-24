"""REST API endpoints for the memory agent."""

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from typing import Dict, Any

from .dependencies import get_graph, get_health_check, get_metrics_func, validate_user_id, validate_session_id
from ..models.requests import ChatRequest, ChatResponse, MemoryRequest, MemoryResponse, HealthResponse, MetricsResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    graph=Depends(get_graph)
):
    """Synchronous chat endpoint."""
    try:
        # Validate inputs
        user_id = validate_user_id(request.user_id)
        session_id = validate_session_id(request.session_id)
        
        # Create configuration
        config = {
            "configurable": {
                "thread_id": session_id,
                "user_id": user_id,
                "todo_category": "general"
            }
        }
        
        # Process with LangGraph
        result = graph.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config
        )
        
        # Extract response
        response_message = result["messages"][-1].content
        
        return ChatResponse(
            response=response_message,
            session_id=session_id,
            user_id=user_id,
            metadata={
                "model": "gemini-2.0-flash-lite",
                "timestamp": result.get("timestamp", ""),
                "thread_id": session_id
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.get("/memories/profile/{user_id}", response_model=MemoryResponse)
async def get_profile(
    user_id: str,
    graph=Depends(get_graph)
):
    """Get user profile memories."""
    try:
        user_id = validate_user_id(user_id)
        
        # Search for profile memories
        profile_namespace = ("profile", "general", user_id)
        memories = graph.store.search(profile_namespace)
        
        profile_data = [mem.value for mem in memories] if memories else []
        
        return MemoryResponse(
            user_id=user_id,
            data={"profiles": profile_data},
            success=True,
            message="Profile memories retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve profile: {str(e)}")


@router.post("/memories/profile/{user_id}", response_model=MemoryResponse)
async def update_profile(
    user_id: str,
    request: MemoryRequest,
    graph=Depends(get_graph)
):
    """Update user profile memories."""
    try:
        user_id = validate_user_id(user_id)
        
        # Store profile data
        profile_namespace = ("profile", "general", user_id)
        graph.store.put(profile_namespace, "user_profile", request.data)
        
        return MemoryResponse(
            user_id=user_id,
            data=request.data,
            success=True,
            message="Profile updated successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.get("/memories/todos/{user_id}", response_model=MemoryResponse)
async def get_todos(
    user_id: str,
    graph=Depends(get_graph)
):
    """Get user todo memories."""
    try:
        user_id = validate_user_id(user_id)
        
        # Search for todo memories
        todo_namespace = ("todo", "general", user_id)
        memories = graph.store.search(todo_namespace)
        
        todo_data = [mem.value for mem in memories] if memories else []
        
        return MemoryResponse(
            user_id=user_id,
            data={"todos": todo_data},
            success=True,
            message="Todo memories retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve todos: {str(e)}")


@router.post("/memories/todos/{user_id}", response_model=MemoryResponse)
async def update_todos(
    user_id: str,
    request: MemoryRequest,
    graph=Depends(get_graph)
):
    """Update user todo memories."""
    try:
        user_id = validate_user_id(user_id)
        
        # Store todo data
        todo_namespace = ("todo", "general", user_id)
        graph.store.put(todo_namespace, "user_todos", request.data)
        
        return MemoryResponse(
            user_id=user_id,
            data=request.data,
            success=True,
            message="Todos updated successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update todos: {str(e)}")


@router.get("/memories/instructions/{user_id}", response_model=MemoryResponse)
async def get_instructions(
    user_id: str,
    graph=Depends(get_graph)
):
    """Get user instruction memories."""
    try:
        user_id = validate_user_id(user_id)
        
        # Search for instruction memories
        instructions_namespace = ("instructions", "general", user_id)
        memories = graph.store.search(instructions_namespace)
        
        instruction_data = [mem.value for mem in memories] if memories else []
        
        return MemoryResponse(
            user_id=user_id,
            data={"instructions": instruction_data},
            success=True,
            message="Instruction memories retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve instructions: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health(
    health_func=Depends(get_health_check)
):
    """Health check endpoint."""
    try:
        health_data = health_func()
        return HealthResponse(**health_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/metrics", response_model=MetricsResponse)
async def metrics(
    metrics_func=Depends(get_metrics_func)
):
    """Metrics endpoint."""
    try:
        metrics_data = metrics_func()
        return MetricsResponse(**metrics_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")
