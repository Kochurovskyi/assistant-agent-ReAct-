# Quick Start Guide

Get the Asis Memory Agent running in under 5 minutes!

## 🚀 Prerequisites

- Python 3.12+
- Google API Key for Gemini model
- Git (for cloning)

## ⚡ Quick Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Kochurovskyi/assistant-agent-ReAct-.git
cd MemA

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file with your Google API key
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

### 3. Start the Server

```bash
# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Server

```bash
# Test basic connectivity
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/api/v1/health
```

## 🎯 Quick Test

### Chat with the Agent

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! I am Asis, 34 years old, married with kids. I love sports, especially running and cycling.",
    "user_id": "Asis",
    "session_id": "quick-test"
  }'
```

### Check Stored Memories

```bash
# Check profile
curl "http://localhost:8000/api/v1/memories/profile/Asis"

# Check todos
curl "http://localhost:8000/api/v1/memories/todos/Asis"
```

## 🌐 Web Interface

Once the server is running, visit:

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 🐳 Docker Quick Start

```bash
# Build and run with Docker
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

## 🧪 Demo Scripts

```bash
# Run conversation simulation
python demo_conversation.py

# Run WebSocket demo (requires server running)
python demo_websocket.py
```

## ✅ Success Indicators

You'll know everything is working when:

- ✅ Server starts without errors
- ✅ Health check returns "healthy"
- ✅ Chat endpoint responds with AI-generated content
- ✅ Memories are stored and retrieved
- ✅ API documentation is accessible

## 🆘 Need Help?

- **Detailed Installation**: [Installation Guide](installation.md)
- **Manual Testing**: [Manual Testing Guide](manual-testing.md)
- **Troubleshooting**: [Common Issues](troubleshooting.md)
- **Full Documentation**: [API Reference](api-reference.md)

## 🎉 Next Steps

Once you have the basic setup working:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Run Tests**: `pytest tests/ -v`
3. **Try WebSocket**: Use the WebSocket demo script
4. **Deploy**: Follow the [Docker Deployment Guide](docker-deployment.md)

Ready to dive deeper? Check out the [Development Guide](development.md) for advanced usage!
