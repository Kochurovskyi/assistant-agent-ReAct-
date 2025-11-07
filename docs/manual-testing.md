# Manual Testing Guide

Step-by-step guide for manually testing the Asis Memory Agent FastAPI server.

## 🚀 Server Status
The FastAPI server should be running at: **http://localhost:8000**

## 📋 Testing Checklist

### 1. Basic Server Health Check

**Test the root endpoint:**
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Asis Memory Agent API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/api/v1/health",
  "metrics": "/api/v1/metrics",
  "websocket": "/ws/chat"
}
```

### 2. Health Check Endpoint

**Test health status:**
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-24T...",
  "store_connectivity": "ok",
  "metrics": {
    "requests_total": 0,
    "errors_total": 0,
    "memory_updates": 0,
    "avg_response_time": 0,
    "error_rate": 0.0
  }
}
```

### 3. Metrics Endpoint

**Test metrics:**
```bash
curl http://localhost:8000/api/v1/metrics
```

**Expected Response:**
```json
{
  "requests_total": 0,
  "errors_total": 0,
  "memory_updates": 0,
  "avg_response_time": 0,
  "error_rate": 0.0
}
```

### 4. Chat Endpoint Testing

**Test basic chat:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! I am Asis, 34 years old, married with kids. I love sports, especially running and cycling.",
    "user_id": "Asis",
    "session_id": "test-session-1"
  }'
```

**Expected Response:**
```json
{
  "response": "Hello Asis! I've updated my memory with your profile information...",
  "session_id": "test-session-1",
  "user_id": "Asis",
  "metadata": {
    "model": "gemini-2.5-flash-lite",
    "timestamp": "...",
    "thread_id": "test-session-1"
  }
}
```

### 5. Memory Management Testing

**Get user profile:**
```bash
curl "http://localhost:8000/api/v1/memories/profile/Asis"
```

**Get user todos:**
```bash
curl "http://localhost:8000/api/v1/memories/todos/Asis"
```

**Get user instructions:**
```bash
curl "http://localhost:8000/api/v1/memories/instructions/Asis"
```

### 6. Interactive Chat Session

**Step 1: Create profile**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My name is Asis. I am 34 years old, married with kids. I love sports, especially running and cycling.",
    "user_id": "Asis",
    "session_id": "interactive-session"
  }'
```

**Step 2: Add tasks**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to prepare for the upcoming marathon in 3 months and help my son with his cycling competition.",
    "user_id": "Asis",
    "session_id": "interactive-session"
  }'
```

**Step 3: Add instructions**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "When creating or updating ToDo items, focus on sports training schedules and family activities.",
    "user_id": "Asis",
    "session_id": "interactive-session"
  }'
```

**Step 4: Check stored memories**
```bash
# Check profile
curl "http://localhost:8000/api/v1/memories/profile/Asis"

# Check todos
curl "http://localhost:8000/api/v1/memories/todos/Asis"

# Check instructions
curl "http://localhost:8000/api/v1/memories/instructions/Asis"
```

### 7. Error Handling Testing

**Test invalid request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "invalid_field": "test"
  }'
```

**Expected Response:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "message"],
      "msg": "Field required",
      "input": {"invalid_field": "test"}
    }
  ]
}
```

**Test invalid endpoint:**
```bash
curl "http://localhost:8000/api/v1/invalid"
```

**Expected Response:**
```json
{
  "detail": "Not Found"
}
```

### 8. WebSocket Testing (Optional)

**Using Python WebSocket client:**
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        message = {
            "message": "Hello! I need help with my marathon training.",
            "user_id": "Asis",
            "session_id": "ws-test"
        }
        await websocket.send(json.dumps(message))
        
        async for response in websocket:
            data = json.loads(response)
            print(f"Received: {data}")
            if data.get("type") == "done":
                break

asyncio.run(test_websocket())
```

### 9. API Documentation

**Visit the interactive API docs:**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 10. Performance Testing

**Test response times:**
```bash
# Time a simple request
time curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'
```

**Expected**: Response time should be < 2 seconds

## 🎯 Success Criteria

- ✅ Server starts without errors
- ✅ All endpoints respond correctly
- ✅ Health check returns "healthy"
- ✅ Chat endpoint processes messages
- ✅ Memory CRUD operations work
- ✅ Error handling works properly
- ✅ API documentation is accessible
- ✅ Response times are reasonable (< 2s)

## 🐛 Troubleshooting

**If server doesn't start:**
1. Check if port 8000 is available
2. Verify virtual environment is activated
3. Check for missing dependencies

**If endpoints don't work:**
1. Verify server is running
2. Check logs for errors
3. Test with curl first, then browser

**If memory operations fail:**
1. Check GOOGLE_API_KEY is set
2. Verify LangGraph is working
3. Check logs for specific errors

## 📊 Expected Results

After successful testing, you should see:
- Profile memories stored and retrieved
- Todo items created and managed
- Instructions learned and applied
- Consistent session management
- Proper error handling
- Fast response times
