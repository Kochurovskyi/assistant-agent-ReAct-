# Troubleshooting Guide

Solutions to common issues when running the Asis Memory Agent.

## 🚨 Common Issues

### Server Won't Start

#### Issue: Port 8000 Already in Use

**Symptoms:**
```
ERROR: [Errno 98] Address already in use
```

**Solutions:**
```bash
# Find process using port 8000
netstat -tulpn | grep :8000
# or
lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### Issue: Module Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'app'
```

**Solutions:**
```bash
# Ensure you're in the project root
cd /path/to/MemA

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Issue: Google API Key Missing

**Symptoms:**
```
ValueError: GOOGLE_API_KEY environment variable is required
```

**Solutions:**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Or set environment variable
export GOOGLE_API_KEY=your_api_key_here

# Verify it's set
echo $GOOGLE_API_KEY
```

### API Endpoints Not Working

#### Issue: 404 Not Found

**Symptoms:**
```
{"detail": "Not Found"}
```

**Solutions:**
```bash
# Check if server is running
curl http://localhost:8000/

# Check correct endpoint
curl http://localhost:8000/api/v1/health

# Verify server logs
# Look for startup messages in terminal
```

#### Issue: 422 Validation Error

**Symptoms:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "message"],
      "msg": "Field required"
    }
  ]
}
```

**Solutions:**
```bash
# Ensure correct request format
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# Check required fields
# - message: required string
# - user_id: optional, defaults to "default-user"
# - session_id: optional
```

#### Issue: 500 Internal Server Error

**Symptoms:**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

**Solutions:**
```bash
# Check server logs for detailed error
# Look for stack traces in terminal output

# Common causes:
# 1. Google API key invalid
# 2. Network connectivity issues
# 3. Memory/CPU resource limits
# 4. Invalid request data
```

### Memory Operations Failing

#### Issue: No Memories Retrieved

**Symptoms:**
```json
{
  "data": {
    "profiles": [],
    "todos": [],
    "instructions": []
  }
}
```

**Solutions:**
```bash
# Ensure user has created memories first
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My name is Asis. I am 34 years old, married with kids.",
    "user_id": "Asis",
    "session_id": "test"
  }'

# Then check memories
curl "http://localhost:8000/api/v1/memories/profile/Asis"
```

#### Issue: Memory Update Failures

**Symptoms:**
```
Error updating memory: ...
```

**Solutions:**
```bash
# Check server logs for specific error
# Common issues:
# 1. Invalid user_id format
# 2. Malformed request data
# 3. Store connectivity issues
```

### WebSocket Issues

#### Issue: WebSocket Connection Failed

**Symptoms:**
```
WebSocket connection failed
```

**Solutions:**
```bash
# Check if server supports WebSocket
curl http://localhost:8000/ | grep websocket

# Test WebSocket connection
# Use the demo script:
python demo_websocket.py

# Check server logs for WebSocket errors
```

#### Issue: WebSocket Messages Not Received

**Symptoms:**
```
No response from WebSocket
```

**Solutions:**
```bash
# Ensure correct message format
{
  "message": "Hello",
  "user_id": "test",
  "session_id": "ws-test"
}

# Check server logs for WebSocket errors
# Verify session_id is provided
```

### Docker Issues

#### Issue: Docker Build Fails

**Symptoms:**
```
ERROR: failed to solve: ...
```

**Solutions:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -t test .
```

#### Issue: Container Won't Start

**Symptoms:**
```
Container exited with code 1
```

**Solutions:**
```bash
# Check container logs
docker-compose logs api

# Check environment variables
docker-compose exec api env

# Verify .env file exists
ls -la .env
```

#### Issue: Port Binding Failed

**Symptoms:**
```
bind: address already in use
```

**Solutions:**
```bash
# Check if port is in use
netstat -tulpn | grep :8000

# Use different port
docker-compose up -p 8001:8000

# Or stop conflicting service
sudo systemctl stop nginx  # if nginx is using port 8000
```

## 🔍 Debugging Steps

### 1. Check Server Status

```bash
# Verify server is running
curl http://localhost:8000/

# Check health endpoint
curl http://localhost:8000/api/v1/health

# Check metrics
curl http://localhost:8000/api/v1/metrics
```

### 2. Review Logs

```bash
# Server logs (if running directly)
# Look for error messages in terminal

# Docker logs
docker-compose logs api

# Follow logs in real-time
docker-compose logs -f api
```

### 3. Test Individual Components

```bash
# Test basic connectivity
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/api/v1/health

# Test chat endpoint
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'
```

### 4. Verify Environment

```bash
# Check environment variables
echo $GOOGLE_API_KEY

# Check Python environment
python --version
pip list | grep langchain

# Check virtual environment
which python
```

## 🛠️ Advanced Troubleshooting

### Performance Issues

#### Slow Response Times

**Symptoms:**
- Chat responses take > 5 seconds
- Memory operations are slow

**Solutions:**
```bash
# Check system resources
htop
# or
docker stats

# Check for memory leaks
docker-compose logs api | grep -i memory

# Restart container
docker-compose restart api
```

#### High Memory Usage

**Symptoms:**
- Container using > 1GB RAM
- System becomes unresponsive

**Solutions:**
```bash
# Check memory usage
docker stats

# Set memory limits
# In docker-compose.yml:
services:
  api:
    deploy:
      resources:
        limits:
          memory: 512M
```

### Network Issues

#### Connection Refused

**Symptoms:**
```
Connection refused
```

**Solutions:**
```bash
# Check if server is listening
netstat -tulpn | grep :8000

# Check firewall
sudo ufw status

# Test local connection
curl http://127.0.0.1:8000/
```

#### CORS Issues

**Symptoms:**
```
CORS error in browser
```

**Solutions:**
```bash
# Check CORS configuration in config.py
# Ensure origins are properly set

# Test with curl (no CORS)
curl http://localhost:8000/api/v1/health
```

### Data Issues

#### Memories Not Persisting

**Symptoms:**
- Memories lost after restart
- Empty memory responses

**Solutions:**
```bash
# This is expected in Phase 1 (in-memory storage)
# Memories are lost on server restart
# Use Phase 2 (Redis) or Phase 3 (PostgreSQL) for persistence
```

#### Invalid Memory Data

**Symptoms:**
```
Validation error in memory operations
```

**Solutions:**
```bash
# Check request format
# Ensure data matches schema requirements

# Check server logs for validation errors
docker-compose logs api | grep -i validation
```

## 📞 Getting Help

### Log Collection

When reporting issues, include:

```bash
# System information
uname -a
docker --version
python --version

# Server logs
docker-compose logs api > server.log

# Environment variables (remove sensitive data)
env | grep -E "(GOOGLE|SERVER|LOG)" > env.log

# Error reproduction steps
# Include exact commands and responses
```

### Common Solutions

1. **Restart the server**: `docker-compose restart api`
2. **Check logs**: `docker-compose logs api`
3. **Verify environment**: Check `.env` file and variables
4. **Test connectivity**: Use `curl` to test endpoints
5. **Check resources**: Ensure sufficient memory and CPU

### When to Seek Help

- Server won't start after following all steps
- API returns 500 errors consistently
- WebSocket connections fail repeatedly
- Memory operations fail with valid data
- Performance issues persist after optimization

### Support Channels

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check `docs/` folder for detailed guides
- **Community**: Join discussions in repository
- **Email**: Contact maintainers for critical issues

This troubleshooting guide should resolve most common issues. For persistent problems, please collect the relevant logs and error messages before seeking additional help.
