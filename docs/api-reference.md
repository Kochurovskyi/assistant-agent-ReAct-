# API Reference

Complete reference for the Asis Memory Agent API endpoints.

## 🌐 Base URL

```
http://localhost:8000
```

## 📋 Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## 🔗 Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and links |
| `/api/v1/chat` | POST | Synchronous chat with memory agent |
| `/api/v1/memories/profile/{user_id}` | GET/POST | User profile management |
| `/api/v1/memories/todos/{user_id}` | GET/POST | Todo management |
| `/api/v1/memories/instructions/{user_id}` | GET | Instruction retrieval |
| `/api/v1/health` | GET | Health check |
| `/api/v1/metrics` | GET | Performance metrics |
| `/ws/chat` | WebSocket | Real-time streaming chat |

## 📖 Detailed Endpoints

### Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response:**
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

### Chat Endpoint

**POST** `/api/v1/chat`

Synchronous chat with the memory agent.

**Request Body:**
```json
{
  "message": "string",
  "user_id": "string (optional, default: 'default-user')",
  "session_id": "string (optional)"
}
```

**Response:**
```json
{
  "response": "string",
  "session_id": "string",
  "user_id": "string",
  "metadata": {
    "model": "string",
    "timestamp": "string",
    "thread_id": "string"
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! I need help with my tasks.",
    "user_id": "Asis",
    "session_id": "session-123"
  }'
```

### Memory Endpoints

#### Get User Profile

**GET** `/api/v1/memories/profile/{user_id}`

Retrieve user profile memories.

**Response:**
```json
{
  "user_id": "string",
  "data": {
    "profiles": [
      {
        "name": "string",
        "location": "string",
        "job": "string",
        "connections": ["string"],
        "interests": ["string"]
      }
    ]
  },
  "success": true,
  "message": "string"
}
```

#### Update User Profile

**POST** `/api/v1/memories/profile/{user_id}`

Update user profile memories.

**Request Body:**
```json
{
  "user_id": "string",
  "data": {
    "name": "string",
    "location": "string",
    "job": "string",
    "connections": ["string"],
    "interests": ["string"]
  }
}
```

#### Get User Todos

**GET** `/api/v1/memories/todos/{user_id}`

Retrieve user todo memories.

**Response:**
```json
{
  "user_id": "string",
  "data": {
    "todos": [
      {
        "task": "string",
        "time_to_complete": "number",
        "deadline": "string",
        "solutions": ["string"],
        "status": "string"
      }
    ]
  },
  "success": true,
  "message": "string"
}
```

#### Update User Todos

**POST** `/api/v1/memories/todos/{user_id}`

Update user todo memories.

**Request Body:**
```json
{
  "user_id": "string",
  "data": {
    "task": "string",
    "time_to_complete": "number",
    "deadline": "string",
    "solutions": ["string"],
    "status": "string"
  }
}
```

#### Get User Instructions

**GET** `/api/v1/memories/instructions/{user_id}`

Retrieve user instruction memories.

**Response:**
```json
{
  "user_id": "string",
  "data": {
    "instructions": [
      {
        "memory": "string"
      }
    ]
  },
  "success": true,
  "message": "string"
}
```

### System Endpoints

#### Health Check

**GET** `/api/v1/health`

Check system health and connectivity.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-24T10:19:03.063896",
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

#### Metrics

**GET** `/api/v1/metrics`

Get performance metrics.

**Response:**
```json
{
  "requests_total": 0,
  "errors_total": 0,
  "memory_updates": 0,
  "avg_response_time": 0,
  "error_rate": 0.0
}
```

## 🔌 WebSocket Endpoint

### Real-time Chat

**WebSocket** `/ws/chat`

Real-time streaming chat with the memory agent.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
```

**Send Message:**
```javascript
ws.send(JSON.stringify({
  message: "Hello! I need help with my marathon training.",
  user_id: "Asis",
  session_id: "ws-session-123"
}));
```

**Receive Responses:**
```javascript
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  if (data.type === 'chunk') {
    console.log('Received chunk:', data.data);
  } else if (data.type === 'done') {
    console.log('Conversation complete');
  } else if (data.type === 'error') {
    console.error('Error:', data.message);
  }
};
```

**Message Types:**
- `chunk`: Streaming response data
- `done`: Conversation complete
- `error`: Error occurred

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## 🔍 Error Handling

### Validation Errors (422)

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "message"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### Server Errors (500)

```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "request_id": "uuid"
}
```

## 🧪 Testing Examples

### Python Client

```python
import requests
import json

# Chat with the agent
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "I need to prepare for a marathon in 3 months",
        "user_id": "Asis",
        "session_id": "python-session"
    }
)

print(response.json())
```

### JavaScript Client

```javascript
// REST API
fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello! I need help with my tasks.',
    user_id: 'Asis',
    session_id: 'js-session'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.onopen = () => {
  ws.send(JSON.stringify({
    message: 'Hello!',
    user_id: 'Asis',
    session_id: 'ws-session'
  }));
};
```

### cURL Examples

```bash
# Basic chat
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# Get profile
curl "http://localhost:8000/api/v1/memories/profile/Asis"

# Health check
curl "http://localhost:8000/api/v1/health"
```

## 📚 Interactive Documentation

Visit the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive testing interfaces where you can:
- Try all endpoints directly in the browser
- See request/response schemas
- Test with different parameters
- View example requests and responses
