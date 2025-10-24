#!/usr/bin/env python3
"""Demo WebSocket conversation through FastAPI server."""

import asyncio
import websockets
import json

async def websocket_conversation():
    """Simulate a conversation through WebSocket."""
    
    uri = "ws://localhost:8000/ws/chat"
    
    print('Starting WebSocket conversation simulation...')
    print('=' * 60)
    
    try:
        async with websockets.connect(uri) as websocket:
            print('Connected to WebSocket server')
            
            # Send a test message
            message = {
                "message": "Hello! I'm Asis and I need help with my marathon training.",
                "user_id": "Asis",
                "session_id": "ws-demo-123"
            }
            
            print(f'\nSending: {message["message"]}')
            await websocket.send(json.dumps(message))
            
            # Receive responses
            print('Receiving responses...')
            async for response in websocket:
                try:
                    data = json.loads(response)
                    if data.get("type") == "chunk":
                        print(f'Chunk: {str(data.get("data", ""))[:100]}...')
                    elif data.get("type") == "done":
                        print('Conversation complete!')
                        break
                    elif data.get("type") == "error":
                        print(f'Error: {data.get("message", "Unknown error")}')
                        break
                except json.JSONDecodeError:
                    print(f'Received non-JSON: {response}')
                    
    except websockets.exceptions.ConnectionRefused:
        print('Error: Could not connect to WebSocket server')
        print('Make sure the FastAPI server is running on localhost:8000')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    print('Note: This demo requires the FastAPI server to be running.')
    print('Start the server with: uvicorn app.main:app --host 0.0.0.0 --port 8000')
    print()
    asyncio.run(websocket_conversation())
