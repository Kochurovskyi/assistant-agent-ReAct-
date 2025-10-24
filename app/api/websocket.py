"""WebSocket endpoints for real-time streaming."""

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from langchain_core.messages import HumanMessage

from .dependencies import get_graph
from ..models.requests import WebSocketMessage

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    graph=Depends(get_graph)
):
    """WebSocket endpoint for real-time chat streaming."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Validate message structure
            try:
                message_data = WebSocketMessage(**data)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Invalid message format: {str(e)}"
                })
                continue
            
            # Create configuration for LangGraph
            config = {
                "configurable": {
                    "thread_id": message_data.session_id or "websocket-session",
                    "user_id": message_data.user_id,
                    "todo_category": "general"
                }
            }
            
            try:
                # Stream LangGraph response
                for chunk in graph.stream(
                    {"messages": [HumanMessage(content=message_data.message)]},
                    config,
                    stream_mode="values"
                ):
                    # Send chunk to client
                    await websocket.send_json({
                        "type": "chunk",
                        "data": chunk,
                        "session_id": message_data.session_id,
                        "user_id": message_data.user_id
                    })
                
                # Send completion signal
                await websocket.send_json({
                    "type": "done",
                    "session_id": message_data.session_id,
                    "user_id": message_data.user_id
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Processing error: {str(e)}",
                    "session_id": message_data.session_id,
                    "user_id": message_data.user_id
                })
                
    except WebSocketDisconnect:
        # Client disconnected
        pass
    except Exception as e:
        # Handle any other errors
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Connection error: {str(e)}"
            })
        except:
            # Connection might be closed
            pass
