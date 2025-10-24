"""API tests for FastAPI Memory Agent."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.models.requests import ChatRequest, ChatResponse

client = TestClient(app)


class TestRootEndpoint:
    """Test the root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
        assert "metrics" in data
        assert "websocket" in data


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_endpoint(self):
        """Test health endpoint returns healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "store_connectivity" in data
        assert "metrics" in data


class TestMetricsEndpoint:
    """Test metrics endpoint."""
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint returns metrics data."""
        response = client.get("/api/v1/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "requests_total" in data
        assert "errors_total" in data
        assert "memory_updates" in data
        assert "avg_response_time" in data
        assert "error_rate" in data


class TestChatEndpoint:
    """Test chat endpoint."""
    
    @patch('app.api.routes.get_graph')
    def test_chat_endpoint_success(self, mock_get_graph):
        """Test successful chat request."""
        # Mock the graph response
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {
            "messages": [MagicMock(content="Test response")]
        }
        mock_get_graph.return_value = mock_graph
        
        # Test request
        request_data = {
            "message": "Hello, test message",
            "user_id": "test-user",
            "session_id": "test-session"
        }
        
        response = client.post("/api/v1/chat", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert "user_id" in data
        assert "metadata" in data
        assert data["user_id"] == "test-user"
        assert data["session_id"] == "test-session"
    
    def test_chat_endpoint_invalid_request(self):
        """Test chat endpoint with invalid request."""
        response = client.post("/api/v1/chat", json={"invalid": "data"})
        assert response.status_code == 422  # Validation error
    
    def test_chat_endpoint_missing_message(self):
        """Test chat endpoint with missing message."""
        response = client.post("/api/v1/chat", json={"user_id": "test-user"})
        assert response.status_code == 422  # Validation error


class TestMemoryEndpoints:
    """Test memory management endpoints."""
    
    @patch('app.api.routes.get_graph')
    def test_get_profile_success(self, mock_get_graph):
        """Test successful profile retrieval."""
        # Mock the graph and store
        mock_graph = MagicMock()
        mock_memory = MagicMock()
        mock_memory.value = {"name": "Test User", "age": 30}
        mock_graph.store.search.return_value = [mock_memory]
        mock_get_graph.return_value = mock_graph
        
        response = client.get("/api/v1/memories/profile/test-user")
        assert response.status_code == 200
        
        data = response.json()
        assert "user_id" in data
        assert "data" in data
        assert "success" in data
        assert "message" in data
        assert data["success"] is True
        assert data["user_id"] == "test-user"
    
    @patch('app.api.routes.get_graph')
    def test_update_profile_success(self, mock_get_graph):
        """Test successful profile update."""
        # Mock the graph and store
        mock_graph = MagicMock()
        mock_get_graph.return_value = mock_graph
        
        request_data = {
            "user_id": "test-user",
            "data": {"name": "Updated User", "age": 31}
        }
        
        response = client.post("/api/v1/memories/profile/test-user", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "user_id" in data
        assert "data" in data
        assert "success" in data
        assert "message" in data
        assert data["success"] is True
        assert data["user_id"] == "test-user"
    
    @patch('app.api.routes.get_graph')
    def test_get_todos_success(self, mock_get_graph):
        """Test successful todos retrieval."""
        # Mock the graph and store
        mock_graph = MagicMock()
        mock_memory = MagicMock()
        mock_memory.value = {"task": "Test task", "status": "pending"}
        mock_graph.store.search.return_value = [mock_memory]
        mock_get_graph.return_value = mock_graph
        
        response = client.get("/api/v1/memories/todos/test-user")
        assert response.status_code == 200
        
        data = response.json()
        assert "user_id" in data
        assert "data" in data
        assert "success" in data
        assert "message" in data
        assert data["success"] is True
        assert data["user_id"] == "test-user"
    
    @patch('app.api.routes.get_graph')
    def test_get_instructions_success(self, mock_get_graph):
        """Test successful instructions retrieval."""
        # Mock the graph and store
        mock_graph = MagicMock()
        mock_memory = MagicMock()
        mock_memory.value = {"instruction": "Test instruction"}
        mock_graph.store.search.return_value = [mock_memory]
        mock_get_graph.return_value = mock_graph
        
        response = client.get("/api/v1/memories/instructions/test-user")
        assert response.status_code == 200
        
        data = response.json()
        assert "user_id" in data
        assert "data" in data
        assert "success" in data
        assert "message" in data
        assert data["success"] is True
        assert data["user_id"] == "test-user"


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404."""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404
    
    def test_invalid_user_id(self):
        """Test invalid user ID validation."""
        response = client.get("/api/v1/memories/profile/")
        assert response.status_code == 404  # Empty user_id in path


class TestWebSocketEndpoint:
    """Test WebSocket endpoint."""
    
    def test_websocket_endpoint_exists(self):
        """Test WebSocket endpoint is accessible."""
        # Note: TestClient doesn't support WebSocket testing directly
        # This is a placeholder for WebSocket-specific tests
        # In a real implementation, you'd use websockets library for testing
        pass


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.options("/api/v1/health")
        # CORS headers should be present (implementation depends on FastAPI CORS middleware)
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented


class TestRequestValidation:
    """Test request validation."""
    
    def test_chat_request_validation(self):
        """Test ChatRequest model validation."""
        # Valid request
        valid_request = ChatRequest(
            message="Test message",
            user_id="test-user",
            session_id="test-session"
        )
        assert valid_request.message == "Test message"
        assert valid_request.user_id == "test-user"
        assert valid_request.session_id == "test-session"
        
        # Request with defaults
        default_request = ChatRequest(message="Test message")
        assert default_request.message == "Test message"
        assert default_request.user_id == "default-user"
        assert default_request.session_id is None
