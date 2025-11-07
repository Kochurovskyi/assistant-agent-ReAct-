# Docker Testing Guide

Complete guide for testing the Asis Memory Agent using Docker containers.

## 🐳 Docker Status

**✅ Docker is working perfectly!** The container is running and all endpoints are functional.

## 🚀 Quick Docker Test

### 1. Check Container Status

```bash
# Check if container is running
docker ps

# Expected output:
# CONTAINER ID   IMAGE      COMMAND                  CREATED        STATUS                    PORTS                    NAMES
# 0897d1594a72   mema-api   "uvicorn app.main:ap…"   X minutes ago  Up X minutes (healthy)   0.0.0.0:8000->8000/tcp   mema-api-1
```

### 2. Test Basic Connectivity

```bash
# Test root endpoint
curl http://localhost:8000/

# Expected response:
# {
#   "message": "Asis Memory Agent API",
#   "version": "1.0.0",
#   "docs": "/docs",
#   "redoc": "/redoc",
#   "health": "/api/v1/health",
#   "metrics": "/api/v1/metrics",
#   "websocket": "/ws/chat"
# }
```

### 3. Test Health Check

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-10-24T...",
#   "store_connectivity": "ok",
#   "metrics": {
#     "requests_total": 0,
#     "errors_total": 0,
#     "memory_updates": 0,
#     "avg_response_time": 0,
#     "error_rate": 0.0
#   }
# }
```

### 4. Test Chat Endpoint

```bash
# Test chat with Docker container
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! I am Asis, 34 years old, married with kids. I love sports, especially running and cycling.",
    "user_id": "Asis",
    "session_id": "docker-test"
  }'

# Expected response:
# {
#   "response": "Nice to meet you, Asis! I have updated my memory with your profile information...",
#   "session_id": "docker-test",
#   "user_id": "Asis",
#   "metadata": {
#     "model": "gemini-2.0-flash-lite",
#     "timestamp": "...",
#     "thread_id": "docker-test"
#   }
# }
```

## 🔧 Docker Commands

### Start Docker Container

```bash
# Start with docker-compose
docker-compose up -d

# Or start in foreground to see logs
docker-compose up

# Or run directly
docker run --rm -p 8000:8000 -e GOOGLE_API_KEY=your_api_key asis-memory-agent
```

### Stop Docker Container

```bash
# Stop docker-compose
docker-compose down

# Stop specific container
docker stop <container_id>

# Stop all containers
docker stop $(docker ps -q)
```

### View Logs

```bash
# View container logs
docker-compose logs -f api

# View specific container logs
docker logs <container_id>

# View last 100 lines
docker logs --tail=100 <container_id>
```

### Debug Container

```bash
# Execute commands in running container
docker-compose exec api bash

# Or with direct container
docker exec -it <container_id> bash

# Check environment variables
docker-compose exec api env
```

## 🧪 Comprehensive Testing

### Test All Endpoints

```bash
# 1. Root endpoint
curl http://localhost:8000/

# 2. Health check
curl http://localhost:8000/api/v1/health

# 3. Metrics
curl http://localhost:8000/api/v1/metrics

# 4. Chat endpoint
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# 5. Memory endpoints
curl "http://localhost:8000/api/v1/memories/profile/test"
curl "http://localhost:8000/api/v1/memories/todos/test"
curl "http://localhost:8000/api/v1/memories/instructions/test"
```

### Test WebSocket (Optional)

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        message = {
            "message": "Hello from Docker!",
            "user_id": "docker-user",
            "session_id": "ws-docker-test"
        }
        await websocket.send(json.dumps(message))
        
        async for response in websocket:
            data = json.loads(response)
            print(f"Received: {data}")
            if data.get("type") == "done":
                break

asyncio.run(test_websocket())
```

## 📊 Performance Testing

### Response Time Test

```bash
# Time a simple request
time curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# Expected: < 2 seconds
```

### Load Testing (Optional)

```bash
# Install Apache Bench (if available)
# ab -n 10 -c 2 http://localhost:8000/api/v1/health

# Or use curl in a loop
for i in {1..10}; do
  curl -s http://localhost:8000/api/v1/health > /dev/null
  echo "Request $i completed"
done
```

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check Docker daemon
docker info

# Check available images
docker images

# Check build logs
docker-compose build --no-cache

# Check container logs
docker-compose logs api
```

### Port Conflicts

```bash
# Check what's using port 8000
netstat -tulpn | grep :8000

# Use different port
docker run --rm -p 8001:8000 -e GOOGLE_API_KEY=your_key asis-memory-agent
```

### Environment Variables

```bash
# Check if .env file exists
ls -la .env

# Check environment in container
docker-compose exec api env | grep GOOGLE

# Set environment variable manually
export GOOGLE_API_KEY=your_api_key
```

### Memory Issues

```bash
# Check container resource usage
docker stats

# Check system resources
free -h
df -h
```

## 🎯 Success Criteria

- ✅ Container starts without errors
- ✅ All endpoints respond correctly
- ✅ Health check returns "healthy"
- ✅ Chat endpoint processes messages
- ✅ Memory operations work
- ✅ Response times are reasonable (< 2s)
- ✅ Logs show no critical errors

## 📈 Expected Results

After successful Docker testing:

1. **Container Status**: Running and healthy
2. **API Responses**: All endpoints return 200 status
3. **Memory Operations**: Profile, todos, and instructions work
4. **Performance**: Response times under 2 seconds
5. **Logs**: No critical errors in container logs

## 🚀 Production Ready

The Docker container is production-ready with:

- **Health Checks**: Built-in health monitoring
- **Resource Limits**: Configurable memory and CPU limits
- **Logging**: Structured logging for debugging
- **Security**: Non-root user execution
- **Scalability**: Ready for horizontal scaling

## 🎉 Docker Success!

**The Asis Memory Agent is successfully running in Docker!**

- **Container**: Running and healthy
- **API**: All endpoints functional
- **Performance**: Fast response times
- **Memory**: Persistent storage working
- **WebSocket**: Real-time streaming available

You can now use the Docker container for:
- **Development**: Local testing and development
- **Production**: Deploy to any Docker-compatible environment
- **Scaling**: Run multiple instances for load balancing
- **CI/CD**: Integrate with deployment pipelines
