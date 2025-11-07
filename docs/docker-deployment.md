# Docker Deployment Guide

Complete guide for deploying the Asis Memory Agent using Docker and Docker Compose.

## 🐳 Docker Overview

The Asis Memory Agent is containerized for easy deployment and scaling. This guide covers both development and production deployment scenarios.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for cloning the repository)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Kochurovskyi/assistant-agent-ReAct-.git
cd MemA

# Create environment file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

### 2. Start with Docker Compose

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f api

# Test the API
curl http://localhost:8000/api/v1/health
```

## 🏗️ Docker Configuration

### Dockerfile

The `Dockerfile` creates an optimized production image:

```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

The `docker-compose.yml` defines the service configuration:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=8000
      - LOG_LEVEL=INFO
      - ENABLE_DOCS=true
    volumes:
      - .:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 🔧 Development Setup

### Local Development with Docker

```bash
# Start development environment
docker-compose up --build

# View logs in real-time
docker-compose logs -f

# Execute commands in container
docker-compose exec api bash

# Stop services
docker-compose down
```

### Development with Volume Mounting

```bash
# Start with code volume mounted
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Create `docker-compose.dev.yml`:
```yaml
version: '3.8'
services:
  api:
    volumes:
      - .:/app
      - /app/.venv  # Exclude virtual environment
    environment:
      - LOG_LEVEL=DEBUG
      - ENABLE_DOCS=true
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🚀 Production Deployment

### Environment Configuration

Create `.env.production`:
```bash
# Production environment variables
GOOGLE_API_KEY=your_production_api_key
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=INFO
ENABLE_DOCS=false
CORS_ORIGINS=https://yourdomain.com
WEBSOCKET_MAX_CONNECTIONS=1000
```

### Production Docker Compose

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=8000
      - LOG_LEVEL=INFO
      - ENABLE_DOCS=false
      - CORS_ORIGINS=${CORS_ORIGINS}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

### Deploy to Production

```bash
# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Check deployment status
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f api
```

## 🔍 Monitoring and Logging

### Container Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api

# Follow logs in real-time
docker-compose logs -f api

# View last N lines
docker-compose logs --tail=100 api
```

### Health Monitoring

```bash
# Check container health
docker-compose ps

# Check health endpoint
curl http://localhost:8000/api/v1/health

# Check metrics
curl http://localhost:8000/api/v1/metrics
```

### Resource Monitoring

```bash
# View container resource usage
docker stats

# View specific container stats
docker stats $(docker-compose ps -q api)
```

## 🛠️ Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check container logs
docker-compose logs api

# Check if port is available
netstat -tulpn | grep :8000

# Check Docker daemon
docker info
```

#### API Not Responding

```bash
# Check container status
docker-compose ps

# Check health endpoint
curl http://localhost:8000/api/v1/health

# Check logs for errors
docker-compose logs api | grep ERROR
```

#### Memory Issues

```bash
# Check memory usage
docker stats

# Restart container
docker-compose restart api

# Check for memory leaks
docker-compose logs api | grep -i memory
```

### Debug Mode

```bash
# Run container in debug mode
docker-compose run --rm api bash

# Check environment variables
docker-compose exec api env

# Test API from inside container
docker-compose exec api curl http://localhost:8000/api/v1/health
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin master

# Rebuild and restart
docker-compose up --build -d

# Check update status
docker-compose ps
```

### Backup and Recovery

```bash
# Backup container data (if using volumes)
docker run --rm -v mema_data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restore from backup
docker run --rm -v mema_data:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v

# Clean up unused resources
docker system prune -a
```

## 🌐 Network Configuration

### Port Mapping

```yaml
services:
  api:
    ports:
      - "8000:8000"  # Host:Container
      - "8001:8000"  # Alternative port
```

### Custom Network

```yaml
version: '3.8'

networks:
  mema_network:
    driver: bridge

services:
  api:
    networks:
      - mema_network
    ports:
      - "8000:8000"
```

## 🔒 Security Considerations

### Non-Root User

The Dockerfile creates and uses a non-root user:

```dockerfile
# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app
```

### Environment Variables

```bash
# Secure environment file
chmod 600 .env

# Use Docker secrets for production
echo "your_api_key" | docker secret create google_api_key -
```

### Network Security

```yaml
services:
  api:
    networks:
      - internal_network
    # No external port exposure
    # Access via reverse proxy
```

## 📊 Performance Tuning

### Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

### Health Checks

```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 🚀 Scaling

### Horizontal Scaling

```bash
# Scale to multiple instances
docker-compose up --scale api=3

# Load balance with nginx
# (Requires nginx configuration)
```

### Vertical Scaling

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

This Docker deployment guide provides everything needed to run the Asis Memory Agent in containerized environments, from development to production.
